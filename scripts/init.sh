#!/usr/bin/env bash
set -euo pipefail

# Initialize a new project with the Codex Automata harness.
# Usage: ./init.sh <target-path>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <target-path>"
    echo ""
    echo "Copies the Codex Automata harness into the target directory."
    exit 1
fi

TARGET="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HARNESS_DIR="$SCRIPT_DIR/../harness"

if [ ! -d "$HARNESS_DIR" ]; then
    echo "Error: Harness directory not found at $HARNESS_DIR"
    exit 1
fi

mkdir -p "$TARGET"
cp -r "$HARNESS_DIR"/. "$TARGET"/

echo ""
echo "Codex Automata harness initialized at: $TARGET"
echo ""
echo "Your project now contains:"
echo "  AGENTS.md        Root agent instructions"
echo "  PLAYBOOK.md      Phase-by-phase methodology guide"
echo "  .cursor/         Cursor IDE rules, skills, subagents, hooks"
echo "  .github/         PR template, issue templates, CI workflow"
echo "  agent/           Detailed agent operating rules"
echo "  templates/       Specification, test, task, and review templates"
echo "  docs/            Project documentation (empty, ready for specs)"
echo "  tests/           Test plans and test code (empty)"
echo "  tasks/           Agent task definitions (empty)"
echo "  review/          Human review records (empty)"
echo "  src/             Source code (empty)"
echo ""
echo "Next steps:"
echo "  1. Open the project in Cursor IDE"
echo "  2. Read PLAYBOOK.md for the phase-by-phase guide"
echo "  3. Copy templates/project-intake-template.md to docs/intake.md"
echo "  4. Or use /project-intake in Cursor chat to get started"
echo ""
