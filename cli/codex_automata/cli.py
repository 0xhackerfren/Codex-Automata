"""CLI entry point for the codex-automata command."""

import argparse
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

    update_parser = subparsers.add_parser("update", help="Refresh harness files without overwriting project docs")
    update_parser.add_argument("target", nargs="?", default=".", help="Project directory (default: current)")

    verify_parser = subparsers.add_parser("verify", help="Run spec-check and divergence-gate against a project")
    verify_parser.add_argument("target", nargs="?", default=".", help="Project directory (default: current)")

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    if args.command == "init":
        return run_init(args.target, args.profile, args.agent)
    elif args.command == "update":
        return run_update(args.target)
    elif args.command == "verify":
        return run_verify(args.target)

    return 1


if __name__ == "__main__":
    sys.exit(main())
