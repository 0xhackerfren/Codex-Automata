#!/usr/bin/env bash
set -euo pipefail

# Initialize a new project with the Codex Automata harness.
# Usage: ./init.sh [--profile essential|standard|complete] <target-path>

PROFILE="standard"
TARGET=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --profile)
            if [[ $# -lt 2 ]]; then
                echo "Error: --profile requires a value (essential, standard, or complete)"
                exit 1
            fi
            PROFILE="$(echo "$2" | tr '[:upper:]' '[:lower:]')"
            shift 2
            ;;
        --profile=*)
            PROFILE="$(echo "${1#*=}" | tr '[:upper:]' '[:lower:]')"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--profile essential|standard|complete] <target-path>"
            echo ""
            echo "Copies the Codex Automata harness into the target directory."
            echo "Default profile is standard when --profile is omitted."
            exit 0
            ;;
        -*)
            echo "Unknown option: $1"
            echo "Usage: $0 [--profile essential|standard|complete] <target-path>"
            exit 1
            ;;
        *)
            if [[ -n "$TARGET" ]]; then
                echo "Error: unexpected argument: $1"
                echo "Usage: $0 [--profile essential|standard|complete] <target-path>"
                exit 1
            fi
            TARGET="$1"
            shift
            ;;
    esac
done

if [[ -z "$TARGET" ]]; then
    echo "Usage: $0 [--profile essential|standard|complete] <target-path>"
    echo ""
    echo "Copies the Codex Automata harness into the target directory."
    exit 1
fi

case "$PROFILE" in
    essential|standard|complete) ;;
    *)
        echo "Error: invalid profile '$PROFILE' (use essential, standard, or complete)"
        exit 1
        ;;
esac

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HARNESS_DIR="$SCRIPT_DIR/../harness"
TEMPLATES_DIR="$HARNESS_DIR/templates"

if [[ ! -d "$HARNESS_DIR" ]]; then
    echo "Error: Harness directory not found at $HARNESS_DIR"
    exit 1
fi

essential_templates=(
    spec-template.md
    test-plan-template.md
    agent-task-template.md
)

standard_templates=(
    "${essential_templates[@]}"
    interface-contract-template.md
    module-boundary-template.md
    architecture-decision-record.md
    context-state-template.md
    block-registry-template.md
    brownfield-audit-template.md
    human-review-template.md
    project-intake-template.md
    sdk-design-template.md
    deployment-checklist-template.md
    guardrail-config-template.md
    retrospective-template.md
)

complete_extra_templates=(
    product-test-template.md
    user-profile-template.md
    design-identity-template.md
    gap-assessment-template.md
    security-audit-template.md
    incident-postmortem-template.md
)

profile_templates=()
case "$PROFILE" in
    essential)
        profile_templates=("${essential_templates[@]}")
        ;;
    standard)
        profile_templates=("${standard_templates[@]}")
        ;;
    complete)
        profile_templates=("${standard_templates[@]}" "${complete_extra_templates[@]}")
        ;;
esac

mkdir -p "$TARGET"

for item in "$HARNESS_DIR"/*; do
    base="$(basename "$item")"
    [[ "$base" == "templates" ]] && continue
    if [[ "$PROFILE" == "essential" && ( "$base" == "sdk" || "$base" == "review" ) ]]; then
        continue
    fi
    cp -r "$item" "$TARGET/"
done

mkdir -p "$TARGET/templates"
if [[ -f "$TEMPLATES_DIR/AGENTS.md" ]]; then
    cp "$TEMPLATES_DIR/AGENTS.md" "$TARGET/templates/"
fi

for name in "${profile_templates[@]}"; do
    src="$TEMPLATES_DIR/$name"
    if [[ ! -f "$src" ]]; then
        echo "Error: template not found: $src"
        exit 1
    fi
    cp "$src" "$TARGET/templates/"
done

if [[ "$PROFILE" != "essential" ]]; then
    for dir in sdk review; do
        mkdir -p "$TARGET/$dir"
        if [[ -f "$HARNESS_DIR/$dir/.gitkeep" ]]; then
            cp "$HARNESS_DIR/$dir/.gitkeep" "$TARGET/$dir/"
        fi
    done
fi

# Copy enforcement scripts
SCRIPTS_SRC="$HARNESS_DIR/scripts"
if [[ -d "$SCRIPTS_SRC" ]]; then
    mkdir -p "$TARGET/scripts"
    cp "$SCRIPTS_SRC"/*.sh "$TARGET/scripts/" 2>/dev/null || true
    cp "$SCRIPTS_SRC"/*.ps1 "$TARGET/scripts/" 2>/dev/null || true
    cp "$SCRIPTS_SRC"/*.json "$TARGET/scripts/" 2>/dev/null || true
    chmod +x "$TARGET/scripts/"*.sh 2>/dev/null || true
fi

profile_label="$(echo "$PROFILE" | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}')"

echo ""
echo "Codex Automata harness initialized at: $TARGET"
echo "Adoption profile: $profile_label"
echo ""
echo "Your project now contains:"
echo "  AGENTS.md        Root agent instructions"
echo "  PLAYBOOK.md      Phase-by-phase methodology guide"
echo "  .cursor/         Cursor IDE rules, skills, subagents, hooks"
echo "  .github/         PR template, issue templates, CI workflow"
echo "  agent/           Detailed agent operating rules"
echo "  templates/       ${#profile_templates[@]} profile template(s)"
echo "  docs/            Project documentation (empty, ready for specs)"
echo "  tests/           Test plans and test code (empty)"
echo "  tasks/           Agent task definitions (empty)"
if [[ "$PROFILE" != "essential" ]]; then
    echo "  review/          Human review records (empty)"
    echo "  sdk/             SDK constraint surface (empty)"
fi
echo "  src/             Source code (empty)"
echo "  scripts/         Enforcement scripts (divergence gate, spec check, commit lint)"
echo ""
echo "Next steps:"
echo "  1. Open the project in Cursor IDE"
echo "  2. Read PLAYBOOK.md for the phase-by-phase guide"
echo "  3. See reference/adoption-profiles.md for profile details"
if [[ "$PROFILE" != "essential" ]]; then
    echo "  4. Copy templates/project-intake-template.md to docs/intake.md"
    echo "  5. Or use /project-intake in Cursor chat to get started"
else
    echo "  4. Create docs/intake.md with project name, goal, constraints, and Profile: Essential"
    echo "  5. Or use /project-intake in Cursor chat to get started"
fi
echo ""
