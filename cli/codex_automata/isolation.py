"""Namespaced adoption and explicit, controller-authorized execution contexts.

The database/authority secret must be outside agent write/read scope. This is a
policy decision boundary for tool adapters, not an OS sandbox.
"""
import hashlib
import json
from pathlib import Path
import secrets
import shutil
import tempfile
from datetime import datetime, timezone

from .control import Controller, require, safe_path, nonempty, canonical
from .init import _harness_dir

METHODOLOGY = '1.0'
CONTEXTS = ('DEVELOP', 'OPERATE', 'MAINTAIN_METHODOLOGY')
PATH_FIELDS = ('source', 'tests', 'specifications', 'sdk', 'generated', 'runtime_state',
               'operational_entrypoints', 'agent_instructions', 'sensitive', 'allowed', 'forbidden')


def read_json(path):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            require(key not in obj, 'Duplicate JSON field: ' + key)
            obj[key] = value
        return obj
    def invalid(value):
        raise ValueError('Non-finite JSON value: ' + value)
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique,
                      parse_constant=invalid)


def digest_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def project_config(profile='standard'):
    return dict(schema_version=1, methodology_version=METHODOLOGY, project_root='.',
                adoption_profile=profile, paths={k: [] for k in PATH_FIELDS},
                capabilities={'DEVELOP': ['file:read', 'file:write', 'check:run'],
                              'OPERATE': [], 'MAINTAIN_METHODOLOGY': ['file:read', 'file:write']},
                review_policy='self-for-low-risk' if profile == 'essential' else 'independent', checks=[])


def validate_config(config, root):
    require(isinstance(config, dict) and set(config) == set(project_config()), 'Invalid project fields')
    require(type(config['schema_version']) is int and config['schema_version'] == 1
            and config['methodology_version'] == METHODOLOGY, 'Unsupported project version')
    require(config['project_root'] == '.', 'Project root is relative to installation parent')
    require(config['adoption_profile'] in ('essential', 'standard', 'complete'), 'Invalid adoption profile')
    require(config['review_policy'] in ('self-for-low-risk', 'independent'), 'Explicit review policy required')
    require(isinstance(config['paths'], dict) and set(config['paths']) == set(PATH_FIELDS), 'Invalid path map')
    root = Path(root).resolve()
    for values in config['paths'].values():
        require(isinstance(values, list) and len(values) == len(set(values)), 'Paths must be unique lists')
        for path in values:
            safe_path(path)
            require((root / path).resolve().is_relative_to(root), 'Configured path escapes project')
            require(path != '.automata' and not path.startswith('.automata/'),
                    'Application paths cannot own methodology assets')
    caps = config['capabilities']
    require(isinstance(caps, dict) and set(caps) == set(CONTEXTS), 'Invalid context capabilities')
    for values in caps.values():
        require(isinstance(values, list) and all(nonempty(x) for x in values)
                and len(set(values)) == len(values), 'Invalid capabilities')
    require(isinstance(config['checks'], list), 'Checks must be a list')
    for check in config['checks']:
        require(isinstance(check, dict) and set(check) == {'name', 'argv'}, 'Invalid check command')
        require(nonempty(check['name']) and isinstance(check['argv'], list) and check['argv']
                and all(nonempty(x) for x in check['argv']), 'Invalid check argv')
    return config


ADAPTER = '''# Codex Automata context router

Consumer instructions remain authoritative. Installation does not activate development.
Obtain the effective context from the trusted controller before using tools.
DEVELOP: request a bounded workflow context; methodology assets are under .automata/assets/.
OPERATE: use only the application's operational instructions and registered tools.
MAINTAIN_METHODOLOGY: requires a separate explicit controller grant.
Missing context: deny changes and request operator bootstrap. A prompt cannot grant permissions.
See .automata/INTEGRATION.md. This file is a routing hint, not a security boundary.
'''


def install(target, profile='standard', agent='cursor', config=None):
    root = Path(target).resolve()
    require(profile in ('essential', 'standard', 'complete'), 'Invalid adoption profile')
    require(agent in ('cursor', 'generic', 'codex', 'claude', 'copilot'), 'Invalid agent')
    config = validate_config(config or project_config(profile), root)
    require(config['adoption_profile'] == profile, 'Config/profile mismatch')
    destination = root / '.automata'
    require(not destination.exists() and not destination.is_symlink(), 'Existing .automata installation')
    root.mkdir(parents=True, exist_ok=True)
    # Prepare on same filesystem; no consumer files change until atomic rename.
    stage = Path(tempfile.mkdtemp(prefix='.automata-stage-', dir=root))
    created = []
    try:
        assets = stage / 'assets'
        assets.mkdir()
        for name in ('agent', 'prompts', 'templates', 'scripts', 'PLAYBOOK.md'):
            source = _harness_dir() / name
            if source.is_dir():
                shutil.copytree(source, assets / name)
            else:
                shutil.copy2(source, assets / name)
        shutil.copytree(Path(__file__).parent / 'contracts', stage / 'schemas')
        (stage / 'project.json').write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
        (stage / '.gitattributes').write_text('assets/** -text\nschemas/** -text\nadapters/** -text\nINTEGRATION.md -text\n', encoding='utf-8')
        (stage / 'INTEGRATION.md').write_text(ADAPTER + '\nRuntime state and authority secrets belong outside this installation and worktree.\n', encoding='utf-8')
        adapters = stage / 'adapters'
        adapters.mkdir()
        (adapters / 'AGENTS.md').write_text(ADAPTER, encoding='utf-8')
        if agent in ('cursor', 'generic'):
            (adapters / 'automata-context.mdc').write_text('---\ndescription: Explicit context routing only\nalwaysApply: true\n---\n\n' + ADAPTER, encoding='utf-8')
        managed = {p.relative_to(stage).as_posix(): digest_file(p) for p in sorted(stage.rglob('*'))
                   if p.is_file() and p.name != 'project.json'}
        manifest = dict(schema_version=1, methodology_version=METHODOLOGY, managed=managed,
                        consumer_owned=['project.json'], adapters_installed=[], adapters_pending=[])
        # Root instructions are created only when absent. Existing integrations are
        # never merged automatically; candidates are always reviewable inside namespace.
        root_adapter = root / 'AGENTS.md'
        if not root_adapter.exists() and not root_adapter.is_symlink():
            with root_adapter.open('x', encoding='utf-8') as stream:
                stream.write(ADAPTER)
            created.append(root_adapter)
            manifest['adapters_installed'].append('AGENTS.md')
        else:
            manifest['adapters_pending'].append('AGENTS.md')
        if agent in ('cursor', 'generic'):
            manifest['adapters_pending'].append('.cursor/rules/automata-context.mdc')
        (stage / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        stage.rename(destination)
    except BaseException:
        for path in created:
            if path.is_file() and path.read_text(encoding='utf-8') == ADAPTER:
                path.unlink()
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return manifest


def verify_installation(root, allow_modified=False):
    root = Path(root).resolve()
    base = root / '.automata'
    require(not base.is_symlink(), 'Installation cannot be a symlink')
    config = validate_config(read_json(base / 'project.json'), root)
    manifest = read_json(base / 'manifest.json')
    require(manifest.get('schema_version') == 1 and manifest.get('methodology_version') == METHODOLOGY,
            'Unsupported installation manifest')
    require(isinstance(manifest.get('managed'), dict) and manifest['managed'], 'Missing managed file manifest')
    for name, digest in manifest['managed'].items():
        safe_path(name)
        path = base / name
        require(path.resolve().is_relative_to(base) and not path.is_symlink()
                and (allow_modified or (path.is_file() and digest_file(path) == digest)), 'Managed asset changed or missing: ' + name)
    return config, manifest


def migration_report(root):
    root = Path(root).resolve()
    # Legacy ownership cannot be inferred from path names. Preserve everything.
    names = ('AGENTS.md', 'PLAYBOOK.md', 'agent', 'templates', 'scripts', '.cursor', '.github',
             'src', 'sdk', 'tests', 'docs', 'tasks', 'context-state.md')
    return dict(schema_version=1, automatic_deletions=[], ambiguous_ownership=[name for name in names
                if (root / name).exists() or (root / name).is_symlink()],
                action='Install isolated layout, review adapter candidates, archive old policy only after ownership review')


def under(path, prefixes):
    return any(path == prefix or path.startswith(prefix + '/') for prefix in prefixes)


class ContextController:
    def __init__(self, controller):
        self.c = controller
        self.db = controller.db
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS context_authority (id INTEGER PRIMARY KEY CHECK(id=1), digest TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS grants (id TEXT PRIMARY KEY, token_digest TEXT NOT NULL, payload TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS context_events (sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                repository TEXT NOT NULL, task TEXT NOT NULL, actor TEXT NOT NULL, payload TEXT NOT NULL);
        ''')

    def bootstrap(self):
        require(not self.db.execute('SELECT 1 FROM context_authority').fetchone(), 'Authority already initialized')
        token = secrets.token_hex(32)
        self.db.execute('INSERT INTO context_authority VALUES(1,?)', (Controller.digest(token),))
        return token

    def authorize(self, authority, grant):
        row = self.db.execute('SELECT digest FROM context_authority WHERE id=1').fetchone()
        require(row and secrets.compare_digest(row['digest'], Controller.digest(authority)), 'Operator authority required')
        require(isinstance(grant, dict) and set(grant) == {'id', 'actor', 'task_id', 'repository',
                'context', 'capabilities', 'write_paths', 'policy_version', 'supersedes', 'reason'}, 'Invalid grant fields')
        require(all(nonempty(grant[k]) for k in ('id', 'actor', 'task_id', 'reason')), 'Grant identity/reason required')
        require(grant['context'] in CONTEXTS and grant['policy_version'] == METHODOLOGY, 'Unsupported context/policy')
        root = Path(grant['repository']).resolve()
        require(not self.c.path.is_relative_to(root), 'Context authority state must remain outside project')
        verify_installation(root, allow_modified=grant['context'] == 'MAINTAIN_METHODOLOGY')
        require(grant['repository'] == str(root), 'Absolute canonical repository required')
        for key in ('capabilities', 'write_paths', 'supersedes'):
            require(isinstance(grant[key], list) and all(nonempty(x) for x in grant[key])
                    and len(set(grant[key])) == len(grant[key]), 'Invalid grant list: ' + key)
        for path in grant['write_paths']:
            safe_path(path)
        token = secrets.token_hex(32)
        payload = dict(grant, issued_at=datetime.now(timezone.utc).isoformat())
        self.c._begin()
        try:
            for old in grant['supersedes']:
                oldrow = self.db.execute('SELECT payload FROM grants WHERE id=?', (old,)).fetchone()
                require(oldrow is not None, 'Unknown superseded grant')
                previous = json.loads(oldrow['payload'])
                require(all(previous[k] == grant[k] for k in ('actor', 'task_id', 'repository')),
                        'Cannot supersede unrelated authority')
            self.db.execute('INSERT INTO grants VALUES(?,?,?)', (grant['id'], Controller.digest(token), canonical(payload)))
            self.db.execute('COMMIT')
        except Exception:
            self.db.execute('ROLLBACK')
            raise
        return dict(grant=payload, token=token)

    def _grant(self, token):
        row = self.db.execute('SELECT payload FROM grants WHERE token_digest=?', (Controller.digest(token),)).fetchone()
        require(row is not None, 'Unknown context grant token')
        grant = json.loads(row['payload'])
        for newer in self.db.execute('SELECT payload FROM grants'):
            require(grant['id'] not in json.loads(newer['payload'])['supersedes'], 'Grant superseded')
        return grant

    def select(self, token):
        self.c._begin()
        try:
            grant = self._grant(token)
            config, manifest = verify_installation(grant['repository'], allow_modified=grant['context'] == 'MAINTAIN_METHODOLOGY')
            capabilities = sorted(set(grant['capabilities']) & set(config['capabilities'][grant['context']]))
            previous = self.current(grant['repository'], grant['task_id'], grant['actor'], required=False)
            event = dict(schema_version=1, current_context=previous['requested_context'] if previous else None,
                         requested_context=grant['context'], task_id=grant['task_id'], actor=grant['actor'],
                         grant_id=grant['id'], policy_version=METHODOLOGY, capabilities=capabilities,
                         write_paths=grant['write_paths'], config_digest=Controller.digest(config),
                         manifest_digest=Controller.digest(manifest), valid=True)
            self.db.execute('INSERT INTO context_events(repository,task,actor,payload) VALUES(?,?,?,?)',
                            (grant['repository'], grant['task_id'], grant['actor'], canonical(event)))
            self.db.execute('COMMIT')
            return event
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def current(self, root, task, actor, required=True):
        row = self.db.execute('SELECT payload FROM context_events WHERE repository=? AND task=? AND actor=? '
                              'ORDER BY sequence DESC LIMIT 1', (str(Path(root).resolve()), task, actor)).fetchone()
        require(not required or row is not None, 'No context: operator must bootstrap authority and grant explicit context')
        return json.loads(row['payload']) if row else None

    def evaluate(self, root, task, actor, capability, path=None):
        event = self.current(root, task, actor)
        config, manifest = verify_installation(root, allow_modified=event['requested_context'] == 'MAINTAIN_METHODOLOGY')
        require(event['config_digest'] == Controller.digest(config)
                and event['manifest_digest'] == Controller.digest(manifest), 'Policy changed; operator must select context again')
        row = self.db.execute('SELECT token_digest,payload FROM grants WHERE id=?', (event['grant_id'],)).fetchone()
        require(row is not None, 'Context grant missing')
        for newer in self.db.execute('SELECT payload FROM grants'):
            require(event['grant_id'] not in json.loads(newer['payload'])['supersedes'], 'Context grant superseded')
        require(capability in event['capabilities'], 'Capability denied; request a scoped operator grant: ' + capability)
        if capability.startswith('file:'):
            require(path is not None, 'File capability requires exact path')
        if path is not None:
            safe_path(path)
            root = Path(root).resolve()
            require((root / path).resolve().is_relative_to(root), 'Path escapes project')
            require(not under(path, config['paths']['forbidden']), 'Forbidden path')
            if under(path, config['paths']['sensitive']):
                require('sensitive:access' in event['capabilities'], 'Sensitive path requires explicit authority')
            if capability == 'file:write':
                require(under(path, event['write_paths']), 'Path outside task grant')
                if under(path, ['.automata']):
                    require(event['requested_context'] == 'MAINTAIN_METHODOLOGY', 'Methodology maintenance grant required')
                elif event['requested_context'] == 'DEVELOP':
                    require(under(path, config['paths']['allowed']), 'Path outside configured development ownership')
                    require(not under(path, config['paths']['runtime_state']), 'Application runtime state is not development output')
                else:
                    require(event['requested_context'] != 'OPERATE', 'Operational source writes are forbidden')
        return dict(allowed=True, context=event['requested_context'], capability=capability, path=path,
                    grant_id=event['grant_id'], policy_version=METHODOLOGY)
