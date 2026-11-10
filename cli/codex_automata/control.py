"""Local deterministic delivery controls. No model calls or remote mutations."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import secrets
import sqlite3
import subprocess

PHASES = {'discover', 'architect', 'sdk', 'mold', 'cast', 'review', 'integrate', 'reconcile'}
FAILURES = {'capability', 'environment', 'design', 'authority'}


class ControlError(ValueError):
    """A fail-closed delivery gate rejected the request."""


def require(condition, message):
    if not condition:
        raise ControlError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def git(repo, *args):
    try:
        return subprocess.check_output(['git', '-C', str(repo), *args],
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ControlError('Git observation failed: ' + ' '.join(args[:2])) from exc


def safe_path(path):
    require(nonempty(path) and '\\' not in path and ':' not in path,
            'Paths must be nonempty relative POSIX paths')
    p = PurePosixPath(path)
    require(not p.is_absolute() and all(part not in ('.', '..', '.git') for part in path.split('/'))
            and not any(ch in path for ch in '*?[]\x00\n'), 'Unsafe or wildcard path')
    return path


def string_list(obj, field, required=True):
    value = obj.get(field)
    require(isinstance(value, list) and all(nonempty(x) for x in value),
            field + ' must be a string list')
    require(len(value) == len(set(value)), field + ' contains duplicates')
    require(not required or bool(value), field + ' cannot be empty')
    return value


def validate_job(job, current_base=True):
    require(isinstance(job, dict) and type(job.get('schema_version')) is int
            and job['schema_version'] == 1, 'Unsupported job schema')
    allowed = {'schema_version', 'id', 'repository', 'branch', 'base_sha', 'phase',
               'outcome', 'risk', 'write_paths', 'acceptance', 'dependencies', 'specs',
               'contracts', 'molds', 'policy_id', 'data_class', 'max_attempts'}
    require(set(job) == allowed, 'Job fields missing or unknown')
    for field in ('id', 'repository', 'branch', 'base_sha', 'phase', 'outcome',
                  'policy_id', 'data_class'):
        require(nonempty(job.get(field)), field + ' must be nonempty')
    require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', job['id']), 'Invalid job ID')
    require(job['phase'] in PHASES, 'Unknown phase')
    require(job.get('risk') in ('routine', 'elevated', 'critical'), 'Explicit risk classification required')
    require(type(job['max_attempts']) is int and 1 <= job['max_attempts'] <= 10,
            'max_attempts must be an integer from 1 to 10')
    require(re.fullmatch(r'[0-9a-f]{40}', job['base_sha']), 'Full Git SHA required')
    repo = Path(job['repository'])
    require(repo.is_absolute() and repo.is_dir(), 'Repository must be an existing absolute directory')
    repo = repo.resolve()
    require(Path(git(repo, 'rev-parse', '--show-toplevel')).resolve() == repo,
            'Repository must identify the Git root')
    git(repo, 'check-ref-format', '--branch', job['branch'])
    git(repo, 'rev-parse', '--verify', 'refs/heads/' + job['branch'])
    if current_base:
        require(git(repo, 'rev-parse', 'HEAD') == job['base_sha'], 'Stale base SHA')
    paths = string_list(job, 'write_paths')
    string_list(job, 'acceptance')
    deps = string_list(job, 'dependencies', False)
    require(job['id'] not in deps, 'Job cannot depend on itself')
    for path in paths:
        safe_path(path)
        require((repo / path).resolve().is_relative_to(repo), 'Write path escapes repository')
    for field in ('specs', 'contracts', 'molds'):
        required = field == 'specs' or (job['phase'] == 'cast' and field in ('contracts', 'molds'))
        for path in string_list(job, field, required):
            safe_path(path)
            # Only a regular tracked blob at the frozen revision qualifies.
            entry = git(repo, 'ls-tree', job['base_sha'], '--', path)
            require(entry.startswith(('100644 blob ', '100755 blob ')),
                    field + ' reference is not a versioned regular file: ' + path)
    return job


class Controller:
    """One local database is the coordination authority for its workers."""
    def __init__(self, path):
        path = Path(path)
        self.path = path.resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        require(not path.is_symlink(), 'State database cannot be a symlink')
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            pass
        else:
            os.close(fd)
        self.db = sqlite3.connect(path, timeout=30, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        version = self.db.execute('PRAGMA user_version').fetchone()[0]
        if version not in (0, 1):
            self.db.close()
            raise ControlError('Unsupported state database schema')
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY, digest TEXT NOT NULL, packet TEXT NOT NULL,
                repo TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'queued',
                owner TEXT, token TEXT, checkpoint TEXT NOT NULL DEFAULT '',
                attempts INTEGER NOT NULL DEFAULT 0, failure TEXT,
                evidence TEXT);
            CREATE TABLE IF NOT EXISTS resolutions (
                job_id TEXT NOT NULL, actor TEXT NOT NULL, reason TEXT NOT NULL,
                attempt_number INTEGER NOT NULL);
            CREATE UNIQUE INDEX IF NOT EXISTS one_writer ON jobs(repo)
                WHERE status = 'active';
            CREATE TABLE IF NOT EXISTS attempts (
                job_id TEXT NOT NULL, number INTEGER NOT NULL,
                classification TEXT NOT NULL, detail TEXT NOT NULL,
                PRIMARY KEY(job_id, number));
            CREATE TABLE IF NOT EXISTS operations (
                id TEXT PRIMARY KEY, digest TEXT NOT NULL,
                payload TEXT NOT NULL, status TEXT NOT NULL);
        ''')
        self.db.execute('PRAGMA user_version=1')

    def close(self):
        self.db.close()

    @staticmethod
    def digest(value):
        return hashlib.sha256(canonical(value).encode()).hexdigest()

    def _begin(self):
        self.db.execute('BEGIN IMMEDIATE')

    def _register(self, job):
        digest = self.digest(job)
        row = self.db.execute('SELECT * FROM jobs WHERE id=?', (job['id'],)).fetchone()
        if row:
            require(row['digest'] == digest, 'Job packet changed; reconcile under a new job ID')
        else:
            self.db.execute('INSERT INTO jobs(id,digest,packet,repo) VALUES(?,?,?,?)',
                            (job['id'], digest, canonical(job), str(Path(job['repository']).resolve())))
        return self.state(job['id'])

    def state(self, job_id):
        row = self.db.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
        require(row is not None, 'Unknown job')
        # Tokens are returned only to the original successful claimant.
        return {k: row[k] for k in row.keys() if k != 'token'}

    def _ready(self, job):
        for dependency in job['dependencies']:
            dep = self.db.execute('SELECT * FROM jobs WHERE id=?', (dependency,)).fetchone()
            require(dep is not None and dep['status'] == 'completed' and dep['evidence'],
                    'Dependency not completed with evidence: ' + dependency)
            require(dep['repo'] == str(Path(job['repository']).resolve()),
                    'Cross-repository dependencies require a verified adapter')
            integrated = json.loads(dep['evidence'])['integration_sha']
            git(job['repository'], 'merge-base', '--is-ancestor', integrated, job['base_sha'])

    def route(self, job, policy):
        validate_job(job)
        require(isinstance(policy, dict) and type(policy.get('schema_version')) is int
                and policy['schema_version'] == 1, 'Unsupported policy schema')
        require(set(policy) == {'schema_version', 'id', 'models'}, 'Unknown or missing policy fields')
        require(policy['id'] == job['policy_id'], 'Approval policy mismatch')
        require(isinstance(policy['models'], list), 'Models must be a list')
        seen = set()
        for model in policy['models']:
            require(isinstance(model, dict) and set(model) ==
                    {'id', 'tier', 'available', 'phases', 'data_classes'}, 'Invalid model record')
            require(nonempty(model['id']) and model['id'] not in seen, 'Duplicate/invalid model ID')
            seen.add(model['id'])
            require(model['tier'] in ('economical', 'frontier') and type(model['available']) is bool,
                    'Invalid capability or availability')
            require(set(string_list(model, 'phases')) <= PHASES, 'Unknown model phase')
            string_list(model, 'data_classes')
        self._begin()
        try:
            state = self._register(job)
            self._ready(job)
            require(state['status'] != 'completed', 'Job already completed')
            require(state['attempts'] < job['max_attempts'], 'Persistent attempt budget exhausted')
            require(state['failure'] not in ('environment', 'design', 'authority'),
                    'Unresolved prerequisite/design/authority failure; reconcile before routing')
            tier = ('frontier' if job['phase'] in ('architect', 'reconcile', 'sdk', 'review')
                    or job['risk'] != 'routine' or state['failure'] == 'capability' else 'economical')
            candidates = [m for m in policy['models'] if m['available']
                          and job['phase'] in m['phases'] and job['data_class'] in m['data_classes']
                          and (tier != 'frontier' or m['tier'] == 'frontier')]
            candidates.sort(key=lambda m: m['tier'] != tier)
            require(candidates, 'No eligible available approved model')
            self.db.execute('COMMIT')
            return dict(job_id=job['id'], packet_digest=self.digest(job),
                        model=candidates[0]['id'], tier=candidates[0]['tier'],
                        attempts=state['attempts'], recommendation_only=True)
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def claim(self, job, owner):
        validate_job(job)
        require(nonempty(owner), 'Owner required')
        require(not git(job['repository'], 'status', '--porcelain'), 'Claim requires a clean worktree')
        self._begin()
        try:
            state = self._register(job)
            self._ready(job)
            require(state['status'] == 'queued', 'Job not available for claim')
            require(state['attempts'] < job['max_attempts'] and state['failure'] in (None, 'capability'),
                    'Job requires reconciliation before claim')
            token = secrets.token_hex(24)
            self.db.execute("UPDATE jobs SET status='active',owner=?,token=? WHERE id=?",
                            (owner, token, job['id']))
            self.db.execute('COMMIT')
            return dict(job_id=job['id'], owner=owner, token=token,
                        packet_digest=self.digest(job))
        except Exception as exc:
            self.db.execute('ROLLBACK')
            if isinstance(exc, sqlite3.IntegrityError):
                raise ControlError('Repository already has an active writer') from exc
            raise

    def _owned(self, job_id, owner, token):
        row = self.db.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
        require(row is not None and row['status'] == 'active' and row['owner'] == owner
                and secrets.compare_digest(row['token'] or '', token), 'Active claim ownership/token mismatch')
        return row

    def checkpoint(self, job_id, owner, token, text):
        require(nonempty(text), 'Checkpoint required')
        self._begin()
        try:
            self._owned(job_id, owner, token)
            self.db.execute('UPDATE jobs SET checkpoint=? WHERE id=?', (text, job_id))
            self.db.execute('COMMIT')
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def release(self, job_id, owner, token, checkpoint):
        require(nonempty(checkpoint), 'Preserved checkpoint required')
        self._begin()
        try:
            self._owned(job_id, owner, token)
            self.db.execute("UPDATE jobs SET status='queued',owner=NULL,token=NULL,checkpoint=? WHERE id=?",
                            (checkpoint, job_id))
            self.db.execute('COMMIT')
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def attempt(self, job_id, owner, token, classification, detail):
        require(classification in FAILURES and nonempty(detail), 'Failure class and evidence required')
        self._begin()
        try:
            row = self._owned(job_id, owner, token)
            packet = json.loads(row['packet'])
            require(row['attempts'] < packet['max_attempts'], 'Attempt budget exhausted')
            number = row['attempts'] + 1
            self.db.execute('INSERT INTO attempts VALUES(?,?,?,?)', (job_id, number, classification, detail))
            self.db.execute('UPDATE jobs SET attempts=?,failure=?,checkpoint=? WHERE id=?',
                            (number, classification, detail, job_id))
            self.db.execute('COMMIT')
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def resolve(self, job_id, owner, token, detail):
        """Record prerequisite repair; never resets attempts or changes the packet."""
        require(nonempty(detail), 'Resolution evidence required')
        self._begin()
        try:
            row = self._owned(job_id, owner, token)
            require(row['failure'] in ('environment', 'design', 'authority'),
                    'No prerequisite failure to resolve')
            self.db.execute('INSERT INTO resolutions VALUES(?,?,?,?)',
                            (job_id, owner, detail, row['attempts']))
            self.db.execute('UPDATE jobs SET failure=NULL,checkpoint=? WHERE id=?',
                            (detail, job_id))
            self.db.execute('COMMIT')
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def complete(self, job, owner, token, evidence, required_checks):
        validate_job(job, current_base=False)
        if self.db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='workflows'").fetchone():
            require(not self.db.execute('SELECT 1 FROM workflows WHERE id=?', (job['id'],)).fetchone(),
                    'Workflow jobs require executor-backed workflow completion')
        require(isinstance(evidence, dict), 'Evidence must be an object')
        require(isinstance(required_checks, list) and required_checks
                and all(nonempty(x) for x in required_checks)
                and len(set(required_checks)) == len(required_checks), 'Trusted required check names needed')
        head = git(job['repository'], 'rev-parse', 'HEAD')
        require(not git(job['repository'], 'status', '--porcelain'), 'Completion requires clean worktree')
        require(evidence.get('head_sha') == head and evidence.get('packet_digest') == self.digest(job),
                'Stale head or packet evidence')
        git(job['repository'], 'merge-base', '--is-ancestor', job['base_sha'], head)
        changed = git(job['repository'], 'diff', '--name-only', '--no-renames',
                      job['base_sha'], head).splitlines()
        for path in changed:
            require(any(path == allowed or path.startswith(allowed + '/')
                        for allowed in job['write_paths']), 'Out-of-scope changed path: ' + path)
            mode = git(job['repository'], 'ls-tree', head, '--', path)
            require(not mode or mode.startswith(('100644 blob ', '100755 blob ')),
                    'Symlink/submodule output requires a separate reviewed contract')
        checks = evidence.get('checks')
        require(isinstance(checks, list), 'Check observations required')
        by_name = {}
        for check in checks:
            require(isinstance(check, dict) and nonempty(check.get('name')), 'Invalid check')
            require(check['name'] not in by_name, 'Duplicate check observation')
            by_name[check['name']] = check
        for name in required_checks:
            check = by_name.get(name, {})
            require(check.get('status') == 'passed' and check.get('head_sha') == head,
                    'Required current-head check missing or failing: ' + name)
        review = evidence.get('review', {})
        require(isinstance(review, dict) and review.get('head_sha') == head
                and review.get('approved') is True and type(review.get('unresolved')) is int
                and review['unresolved'] == 0 and nonempty(review.get('reviewer'))
                and review['reviewer'] != owner, 'Independent current-head approval required')
        require('required_checks' not in evidence or evidence['required_checks'] == required_checks,
                'Evidence cannot override operator-required checks')
        integrated = evidence.get('integration_sha')
        require(isinstance(integrated, str) and re.fullmatch(r'[0-9a-f]{40}', integrated),
                'Full integration SHA required')
        git(job['repository'], 'merge-base', '--is-ancestor', head, integrated)
        git(job['repository'], 'merge-base', '--is-ancestor', integrated, 'refs/heads/' + job['branch'])
        self._begin()
        try:
            row = self._owned(job['id'], owner, token)
            require(row['digest'] == self.digest(job), 'Claim packet mismatch')
            self.db.execute("UPDATE jobs SET status='completed',token=NULL,evidence=? WHERE id=?",
                            (canonical(evidence), job['id']))
            self.db.execute('COMMIT')
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def prepare_operation(self, operation_id, payload):
        require(nonempty(operation_id) and isinstance(payload, dict)
                and set(payload) == {'entity', 'revision', 'desired'}
                and all(nonempty(x) for x in payload.values()), 'Invalid operation identity/payload')
        digest = self.digest(payload)
        self._begin()
        try:
            row = self.db.execute('SELECT * FROM operations WHERE id=?', (operation_id,)).fetchone()
            if row:
                require(row['digest'] == digest, 'Operation ID reused with changed payload')
            else:
                self.db.execute('INSERT INTO operations VALUES(?,?,?,?)',
                                (operation_id, digest, canonical(payload), 'pending'))
            self.db.execute('COMMIT')
            return dict(self.db.execute('SELECT * FROM operations WHERE id=?', (operation_id,)).fetchone())
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def uncertain_operation(self, operation_id):
        changed = self.db.execute("UPDATE operations SET status='uncertain' WHERE id=? AND status='pending'",
                                  (operation_id,)).rowcount
        require(changed == 1, 'Operation is not pending')

    def reconcile_operation(self, operation_id, observation):
        self._begin()
        try:
            row = self.db.execute('SELECT * FROM operations WHERE id=?', (operation_id,)).fetchone()
            require(row is not None and self.digest(observation) == row['digest'],
                    'Remote observation differs; reconcile entity revision/state before acknowledgement')
            self.db.execute("UPDATE operations SET status='confirmed' WHERE id=?", (operation_id,))
            self.db.execute('COMMIT')
        except Exception:
            self.db.execute('ROLLBACK')
            raise
