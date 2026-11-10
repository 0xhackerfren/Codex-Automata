"""Small JSON CLI for offline development workflows; no model invocation."""
import json
from pathlib import Path
import sqlite3
import sys
from .control import Controller, ControlError, require, git
from .isolation import read_json
from .workflow import Workflow, contract, PROFILES


def add_parser(subparsers):
    parser = subparsers.add_parser('workflow', help='Offline single-agent methodology gates')
    commands = parser.add_subparsers(dest='workflow_action', required=True)
    draft = commands.add_parser('draft', help='Emit a local job v1 packet; no remote issue is created')
    draft.add_argument('--project', required=True)
    draft.add_argument('--id', required=True)
    draft.add_argument('--outcome', required=True)
    draft.add_argument('--spec', action='append', required=True)
    draft.add_argument('--contract', action='append', default=[])
    draft.add_argument('--mold', action='append', default=[])
    draft.add_argument('--write-path', action='append', required=True)
    draft.add_argument('--acceptance', action='append', required=True)
    draft.add_argument('--branch', default='main')
    schema = commands.add_parser('contract', help='Print the pinned machine-readable definition or schema')
    schema.add_argument('name', choices=['profiles', 'plan', 'artifact', 'model', 'benchmark'])
    for action in ('start', 'advance', 'run', 'context', 'checkpoint', 'resume', 'rewind', 'reclaim'):
        cmd = commands.add_parser(action)
        cmd.add_argument('--state', required=True)
        if action == 'start':
            cmd.add_argument('--packet', required=True)
            cmd.add_argument('--plan', required=True)
        else:
            cmd.add_argument('task')
        if action != 'checkpoint':
            cmd.add_argument('--owner', required=True)
        if action not in ('start', 'checkpoint', 'reclaim'):
            cmd.add_argument('--token', required=True)
        if action == 'advance':
            cmd.add_argument('--artifact', required=True)
        if action == 'resume':
            cmd.add_argument('--checkpoint', required=True)
        if action == 'rewind':
            cmd.add_argument('--phase', required=True)
            cmd.add_argument('--reason', required=True)
        if action == 'run':
            cmd.add_argument('--check', required=True)
            cmd.add_argument('--expect', choices=['pass', 'fail'], default='pass')


def run(args):
    c = None
    try:
        action = args.workflow_action
        if action == 'draft':
            repo = str(Path(args.project).resolve())
            result = dict(schema_version=1, id=args.id, repository=repo, branch=args.branch,
                          base_sha=git(repo, 'rev-parse', 'HEAD'),
                          phase='cast' if args.contract and args.mold else 'discover',
                          outcome=args.outcome, risk='routine', write_paths=args.write_path,
                          acceptance=args.acceptance, dependencies=[], specs=args.spec,
                          contracts=args.contract, molds=args.mold, policy_id='local-manual',
                          data_class='private', max_attempts=3)
            from .control import validate_job
            validate_job(result)
        elif action == 'contract':
            result = contract('profiles.json' if args.name == 'profiles' else args.name + '.schema.json')
        else:
            c = Controller(args.state)
            w = Workflow(c)
            if action == 'start':
                result = w.start(read_json(args.packet), read_json(args.plan), args.owner)
            elif action == 'checkpoint':
                result = w.snapshot(args.task)
            elif action == 'reclaim':
                result = w.reclaim(args.task, args.owner)
            elif action == 'advance':
                raw = Path(args.artifact).read_bytes()
                _, _, plan, _, _ = w._load(args.task)
                require(len(raw) <= plan['context_budget'], 'Artifact output budget exceeded')
                result = w.advance(args.task, args.owner, args.token, read_json(args.artifact))
            elif action == 'run':
                result = w.execute(args.task, args.owner, args.token, args.check, args.expect)
                print(json.dumps(result, sort_keys=True))
                return 0 if result['unchanged'] and result['failure'] is None and (result['exit_code'] == 0) == (args.expect == 'pass') else 1
            elif action == 'resume':
                result = w.resume(args.task, args.owner, args.token, read_json(args.checkpoint))
            elif action == 'rewind':
                result = w.rewind(args.task, args.owner, args.token, args.phase, args.reason)
            else:
                result = w.context_packet(args.task, args.owner, args.token)
        # Context size is defined against compact canonical JSON, without newline.
        from .control import canonical
        print(canonical(result))
        return 0
    except (ControlError, OSError, ValueError, TypeError, KeyError, sqlite3.Error) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 1
    finally:
        if c:
            c.close()
