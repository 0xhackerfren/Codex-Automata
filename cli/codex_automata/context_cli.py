"""CLI adapter. Authority commands are operator-only, never model tools."""
import json
from pathlib import Path
import sqlite3
import sys
from .control import Controller, ControlError, require
from .isolation import ContextController, read_json, migration_report


def add_parser(subparsers):
    parser = subparsers.add_parser('context', help='Explicit execution-context authority and decisions')
    cmds = parser.add_subparsers(dest='context_action', required=True)
    for action in ('bootstrap', 'authorize', 'select', 'show', 'check', 'selftest'):
        cmd = cmds.add_parser(action)
        cmd.add_argument('--state', required=True)
        if action == 'authorize':
            cmd.add_argument('--authority-file', required=True)
            cmd.add_argument('--grant', required=True)
        if action == 'select':
            cmd.add_argument('--grant-file', required=True, help='Controller-issued token file, outside agent read scope')
        if action in ('show', 'check', 'selftest'):
            cmd.add_argument('--project', required=True)
            cmd.add_argument('--task', required=True)
            cmd.add_argument('--actor', required=True)
        if action == 'check':
            cmd.add_argument('--capability', required=True)
            cmd.add_argument('--path')
        if action == 'selftest':
            cmd.add_argument('--payload', required=True)
    migration = subparsers.add_parser('migration', help='Report legacy ownership without deleting files')
    migration.add_argument('target')


def hook_decision(context, root, task, actor, payload):
    # Exact, explicit payload contract; never infer shell safety by substrings.
    require(isinstance(payload, dict), 'Invalid hook payload')
    event = payload.get('event', 'preToolUse')
    tool = payload.get('tool_name')
    if event == 'beforeMCPExecution' or (isinstance(tool, str) and tool.startswith('MCP:')):
        require(nonempty_server(payload.get('mcp_server_name')) and isinstance(tool, str)
                and tool.startswith('MCP:') and len(tool) > 4, 'Explicit MCP server and MCP:<tool> required')
        capability = 'mcp:' + payload['mcp_server_name'] + ':' + tool[4:]
        return context.evaluate(root, task, actor, capability)
    args = payload.get('input', {})
    require(isinstance(args, dict), 'Invalid hook input')
    if tool in ('Read', 'Write', 'Edit'):
        path = args.get('path', args.get('filePath'))
        return context.evaluate(root, task, actor, 'file:read' if tool == 'Read' else 'file:write', path)
    raise ControlError('Unknown or unrestricted tool denied; register an exact runtime capability or plan-bound check. '
                       'Operator bootstrap: context bootstrap, authorize, select; do not edit mode files from the agent.')


def nonempty_server(value):
    return isinstance(value, str) and bool(value.strip()) and ':' not in value


def run(args):
    c = None
    try:
        if args.command == 'migration':
            result = migration_report(args.target)
        else:
            c = Controller(args.state)
            context = ContextController(c)
            action = args.context_action
            if action == 'bootstrap':
                result = {'authority_token': context.bootstrap(), 'operator_only': True}
            elif action == 'authorize':
                grant = read_json(args.grant)
                authority_path = Path(args.authority_file).resolve()
                require(not authority_path.is_relative_to(Path(grant['repository']).resolve()),
                        'Authority secret must remain outside repository')
                result = context.authorize(authority_path.read_text().strip(), grant)
            elif action == 'select':
                result = context.select(read_json(args.grant_file)['token'])
            elif action == 'show':
                result = context.current(args.project, args.task, args.actor)
            elif action == 'selftest':
                result = hook_decision(context, args.project, args.task, args.actor, read_json(args.payload))
            else:
                result = context.evaluate(args.project, args.task, args.actor, args.capability, args.path)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ControlError, OSError, ValueError, TypeError, KeyError, sqlite3.Error) as exc:
        print(json.dumps({'allowed': False, 'error': str(exc)}), file=sys.stderr)
        return 1
    finally:
        if c:
            c.close()
