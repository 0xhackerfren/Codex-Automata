#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$SCRIPT_DIR/../cli${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m codex_automata.cli init "$@"
