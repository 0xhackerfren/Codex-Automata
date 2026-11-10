"""Read-only evidence-surface observations; no publication or synchronization."""
import json
import os
from pathlib import Path
import subprocess
import sys
from .control import ControlError, Controller, git, require, validate_job
from .isolation import read_json


def inspect_surface(project, publication_required=False, remote='origin', branch='main'):
    root = Path(project).resolve()
    head = git(root, 'rev-parse', 'HEAD')
    git(root, 'check-ref-format', '--branch', branch)
    require(remote and not remote.startswith('-') and all(c.isalnum() or c in '._-' for c in remote), 'Invalid remote name')
    remotes = git(root, 'remote').splitlines()
    result = dict(schema_version=1, local_head=head, publication_required=publication_required,
                  remote_configured=remote in remotes, remote_ref_present=None, remote_head=None,
                  last_pushed_head_matches=None, publication_state='not-required-local-only', valid=True)
    if not publication_required:
        return result
    result.update(valid=False, publication_state='blocked-missing-remote')
    if remote not in remotes:
        return result
    try:
        observation = subprocess.run(['git', '-C', str(root), 'ls-remote', '--exit-code', remote,
                                      'refs/heads/' + branch], capture_output=True, text=True, timeout=30,
                                     env=dict(os.environ, GIT_TERMINAL_PROMPT='0'))
    except (OSError, subprocess.TimeoutExpired):
        result['publication_state'] = 'blocked-remote-observation-failed'
        return result
    lines = observation.stdout.splitlines()
    if observation.returncode or len(lines) != 1:
        result.update(remote_ref_present=False, publication_state='blocked-remote-ref-unavailable')
        return result
    remote_head = lines[0].split()[0]
    result.update(remote_ref_present=True, remote_head=remote_head, last_pushed_head_matches=remote_head == head,
                  valid=remote_head == head, publication_state='published' if remote_head == head else 'pending-publication')
    return result


def readiness(controller, job):
    validate_job(job)
    controller._ready(job)
    receipts = []
    for dependency in job['dependencies']:
        state = controller.state(dependency)
        evidence = json.loads(state['evidence'])
        receipts.append(dict(task_id=dependency, packet_digest=state['digest'], integration_sha=evidence['integration_sha']))
    return dict(schema_version=1, task_id=job['id'], ready=True, base_sha=job['base_sha'],
                artifact_paths=job['specs'] + job['contracts'] + job['molds'], dependencies=receipts,
                remote_transition='proposed-only; authenticated adapter must re-read remote state')


def add_parser(subparsers):
    parser = subparsers.add_parser('session', help='Read-only session evidence and child-readiness checks')
    commands = parser.add_subparsers(dest='session_action', required=True)
    inspect = commands.add_parser('inspect')
    inspect.add_argument('--project', required=True)
    inspect.add_argument('--publication-required', action='store_true')
    inspect.add_argument('--remote', default='origin')
    inspect.add_argument('--branch', default='main')
    ready = commands.add_parser('readiness')
    ready.add_argument('--packet', required=True)
    ready.add_argument('--state', required=True)


def run(args):
    c = None
    try:
        if args.session_action == 'inspect':
            result = inspect_surface(args.project, args.publication_required, args.remote, args.branch)
        else:
            c = Controller(args.state)
            result = readiness(c, read_json(args.packet))
        print(json.dumps(result, sort_keys=True))
        return 0 if result.get('valid', result.get('ready', False)) else 1
    except (ControlError, ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 1
    finally:
        if c:
            c.close()
