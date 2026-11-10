"""CLI entry point for the codex-automata command."""

import argparse
import json
import sqlite3
from pathlib import Path

from codex_automata.control import Controller, ControlError, validate_job
import sys

from codex_automata import __version__
from codex_automata.init import run_init
from codex_automata.update import run_update
from codex_automata.verify import run_verify


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="codex-automata",
        description="Codex Automata methodology harness for the agentic era.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize a new project with the Codex Automata harness")
    init_parser.add_argument("target", help="Path to the project directory")
    init_parser.add_argument(
        "--profile",
        choices=["essential", "standard", "complete"],
        default="standard",
        help="Adoption profile (default: standard)",
    )
    init_parser.add_argument(
        "--agent",
        choices=["cursor", "claude", "copilot", "codex", "generic"],
        default="cursor",
        help="Primary AI agent integration (default: cursor)",
    )

    update_parser = subparsers.add_parser("update", help="Stage an upstream harness for review without changing project files")
    update_parser.add_argument("target", nargs="?", default=".", help="Project directory (default: current)")

    update_parser.add_argument("--staging", help="New separate staging directory")
    update_parser.add_argument("--profile", choices=["essential", "standard", "complete"], default="standard")
    update_parser.add_argument("--agent", choices=["cursor", "claude", "copilot", "codex", "generic"], default="cursor")

    verify_parser = subparsers.add_parser("verify", help="Run spec-check and divergence-gate against a project")
    verify_parser.add_argument("target", nargs="?", default=".", help="Project directory (default: current)")

    job_parser = subparsers.add_parser("job", help="Validate and coordinate local delivery jobs")
    jobs = job_parser.add_subparsers(dest="job_action", required=True)
    for action in ("validate", "route", "claim", "complete"):
        cmd = jobs.add_parser(action)
        cmd.add_argument("packet", help="Versioned job JSON file")
        if action != "validate":
            cmd.add_argument("--state", required=True, help="Shared local SQLite database path")
        if action == "route":
            cmd.add_argument("--policy", required=True, help="Operator-controlled approved-model inventory")
        if action in ("claim", "complete"):
            cmd.add_argument("--owner", required=True)
        if action == "complete":
            cmd.add_argument("--token", required=True)
            cmd.add_argument("--evidence", required=True)
            cmd.add_argument("--required-check", action="append", required=True,
                             help="Operator-selected required check; repeat for each check")
    for action in ("state", "checkpoint", "release", "attempt", "resolve"):
        cmd = jobs.add_parser(action)
        cmd.add_argument("job_id")
        cmd.add_argument("--state", required=True)
        if action != "state":
            cmd.add_argument("--owner", required=True)
            cmd.add_argument("--token", required=True)
            cmd.add_argument("--detail", required=True)
        if action == "attempt":
            cmd.add_argument("--classification", required=True,
                             choices=["capability", "environment", "design", "authority"])

    journal = subparsers.add_parser("journal", help="Record/reconcile external-operation intent; never sends it")
    journal.add_argument("action", choices=["prepare", "uncertain", "reconcile"])
    journal.add_argument("operation_id")
    journal.add_argument("--state", required=True)
    journal.add_argument("--payload", help="Operation or remote-observation JSON")

    from .context_cli import add_parser as add_context_parser
    add_context_parser(subparsers)
    from .workflow_cli import add_parser as add_workflow_parser
    add_workflow_parser(subparsers)
    from .qualification import add_parser as add_model_parser
    add_model_parser(subparsers)
    from .benchmark import add_parser as add_benchmark_parser
    add_benchmark_parser(subparsers)
    from .session import add_parser as add_session_parser
    add_session_parser(subparsers)
    init_parser.add_argument('--layout', choices=['namespaced', 'legacy'], default='namespaced')
    init_parser.add_argument('--config', help='Consumer-owned project configuration JSON')
    update_parser.add_argument('--layout', choices=['namespaced', 'legacy'], default='namespaced')
    verify_parser.add_argument('--state')
    verify_parser.add_argument('--task')
    verify_parser.add_argument('--actor')
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    if args.command == 'session':
        from .session import run
        return run(args)

    if args.command == 'benchmark':
        from .benchmark import run
        return run(args)

    if args.command == 'model':
        from .qualification import run
        return run(args)

    if args.command == 'workflow':
        from .workflow_cli import run
        return run(args)

    if args.command in ('context', 'migration'):
        from .context_cli import run
        return run(args)

    if args.command in ("job", "journal"):
        controller = None
        try:
            def read_json(path):
                def unique_pairs(pairs):
                    result = {}
                    for key, value in pairs:
                        if key in result:
                            raise ControlError("Duplicate JSON field: " + key)
                        result[key] = value
                    return result
                return json.loads(Path(path).read_text(encoding="utf-8"),
                                  object_pairs_hook=unique_pairs)
            if args.command == "job" and args.job_action == "validate":
                packet = read_json(args.packet)
                validate_job(packet)
                result = {"valid": True, "packet_digest": Controller.digest(packet)}
            else:
                controller = Controller(args.state)
                if args.command == "journal":
                    if args.action == "prepare":
                        result = controller.prepare_operation(args.operation_id, read_json(args.payload))
                    elif args.action == "uncertain":
                        controller.uncertain_operation(args.operation_id)
                        result = {"status": "uncertain"}
                    else:
                        controller.reconcile_operation(args.operation_id, read_json(args.payload))
                        result = {"status": "confirmed"}
                elif args.job_action in ("route", "claim", "complete"):
                    packet = read_json(args.packet)
                    if args.job_action == "route":
                        result = controller.route(packet, read_json(args.policy))
                    elif args.job_action == "claim":
                        result = controller.claim(packet, args.owner)
                    else:
                        controller.complete(packet, args.owner, args.token,
                                            read_json(args.evidence), args.required_check)
                        result = {"status": "completed"}
                elif args.job_action == "state":
                    result = controller.state(args.job_id)
                else:
                    if args.job_action == "attempt":
                        controller.attempt(args.job_id, args.owner, args.token,
                                           args.classification, args.detail)
                    else:
                        getattr(controller, args.job_action)(args.job_id, args.owner,
                                                             args.token, args.detail)
                    result = {"recorded": True}
            print(json.dumps(result, sort_keys=True))
            return 0
        except (ControlError, OSError, ValueError, TypeError, sqlite3.Error) as exc:
            print(json.dumps({"error": str(exc)}), file=sys.stderr)
            return 1
        finally:
            if controller is not None:
                controller.close()

    if args.command == "init":
        from .isolation import read_json
        try:
            return run_init(args.target, args.profile, args.agent, args.layout,
                            read_json(args.config) if args.config else None)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            print(json.dumps({'error': str(exc)}), file=sys.stderr)
            return 1
    elif args.command == "update":
        return run_update(args.target, args.staging, args.profile, args.agent, args.layout)
    elif args.command == "verify":
        return run_verify(args.target, args.state, args.task, args.actor)

    return 1


if __name__ == "__main__":
    sys.exit(main())
