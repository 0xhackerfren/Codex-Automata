"""Initialize a new project with the Codex Automata harness."""

import json
import os
import platform
import shutil
from pathlib import Path

ESSENTIAL_TEMPLATES = [
    "spec-template.md",
    "test-plan-template.md",
    "agent-task-template.md",
]

STANDARD_TEMPLATES = ESSENTIAL_TEMPLATES + [
    "interface-contract-template.md",
    "module-boundary-template.md",
    "architecture-decision-record.md",
    "context-state-template.md",
    "block-registry-template.md",
    "brownfield-audit-template.md",
    "human-review-template.md",
    "project-intake-template.md",
    "sdk-design-template.md",
    "deployment-checklist-template.md",
    "guardrail-config-template.md",
    "retrospective-template.md",
]

COMPLETE_EXTRA_TEMPLATES = [
    "product-test-template.md",
    "user-profile-template.md",
    "design-identity-template.md",
    "gap-assessment-template.md",
    "security-audit-template.md",
    "incident-postmortem-template.md",
]


def _harness_dir() -> Path:
    """Locate the bundled harness directory shipped with the package."""
    pkg_dir = Path(__file__).parent
    bundled = pkg_dir / "_harness"
    if bundled.is_dir():
        return bundled
    # Fallback: running from source checkout
    repo_root = pkg_dir.parent.parent
    source = repo_root / "harness"
    if source.is_dir():
        return source
    raise FileNotFoundError(
        "Harness directory not found. Ensure the package is installed correctly "
        "or run from the Codex-Automata repository root."
    )


def _profile_templates(profile: str) -> list[str]:
    if profile == "essential":
        return list(ESSENTIAL_TEMPLATES)
    elif profile == "standard":
        return list(STANDARD_TEMPLATES)
    else:
        return STANDARD_TEMPLATES + COMPLETE_EXTRA_TEMPLATES


def _patch_hooks_for_windows(target: Path) -> None:
    """Replace .sh hook commands with .ps1 equivalents on Windows."""
    hooks_json = target / ".cursor" / "hooks.json"
    if not hooks_json.exists():
        return
    content = hooks_json.read_text(encoding="utf-8")
    patched = content.replace(".sh", ".ps1")
    if patched != content:
        hooks_json.write_text(patched, encoding="utf-8")


def _skip_cursor_dir(agent: str) -> bool:
    """Non-Cursor agents do not need the .cursor directory."""
    return agent not in ("cursor", "generic")


def run_init(target_str: str, profile: str, agent: str) -> int:
    target = Path(target_str).resolve()
    harness = _harness_dir()
    templates_dir = harness / "templates"

    profile_templates = _profile_templates(profile)
    skip_dirs = {"templates"}
    if profile == "essential":
        skip_dirs.update({"sdk", "review"})
    if _skip_cursor_dir(agent):
        skip_dirs.add(".cursor")

    target.mkdir(parents=True, exist_ok=True)

    for item in harness.iterdir():
        if item.name in skip_dirs:
            continue
        dest = target / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)

    # Copy selected templates
    tmpl_dest = target / "templates"
    tmpl_dest.mkdir(exist_ok=True)
    agents_tmpl = templates_dir / "AGENTS.md"
    if agents_tmpl.exists():
        shutil.copy2(agents_tmpl, tmpl_dest)
    for name in profile_templates:
        src = templates_dir / name
        if not src.exists():
            print(f"Warning: template not found: {src}")
            continue
        shutil.copy2(src, tmpl_dest)

    # Create non-Essential dirs
    if profile != "essential":
        for d in ("sdk", "review"):
            (target / d).mkdir(exist_ok=True)
            gitkeep = harness / d / ".gitkeep"
            if gitkeep.exists():
                shutil.copy2(gitkeep, target / d)

    # Copy enforcement scripts
    scripts_src = harness / "scripts"
    if scripts_src.is_dir():
        scripts_dest = target / "scripts"
        scripts_dest.mkdir(exist_ok=True)
        for f in scripts_src.iterdir():
            if f.is_file():
                shutil.copy2(f, scripts_dest)

    # Windows: patch hooks.json
    if platform.system() == "Windows":
        _patch_hooks_for_windows(target)

    profile_label = profile.capitalize()
    tmpl_count = len(profile_templates)

    print()
    print(f"Codex Automata harness initialized at: {target}")
    print(f"Adoption profile: {profile_label}")
    print(f"Agent integration: {agent}")
    print()
    print("Your project now contains:")
    print("  AGENTS.md        Root agent instructions")
    print("  PLAYBOOK.md      Phase-by-phase methodology guide")
    if agent in ("cursor", "generic"):
        print("  .cursor/         Cursor IDE rules, skills, subagents, hooks")
    print("  .github/         PR template, issue templates, CI workflow")
    print("  agent/           Detailed agent operating rules")
    print(f"  templates/       {tmpl_count} profile template(s)")
    print("  docs/            Project documentation (empty, ready for specs)")
    print("  tests/           Test plans and test code (empty)")
    print("  tasks/           Agent task definitions (empty)")
    if profile != "essential":
        print("  review/          Human review records (empty)")
        print("  sdk/             SDK constraint surface (empty)")
    print("  src/             Source code (empty)")
    print("  scripts/         Enforcement scripts (divergence gate, spec check, commit lint)")
    print()
    print("Next steps:")
    print("  1. Open the project in your IDE")
    print("  2. Read PLAYBOOK.md for the phase-by-phase guide")
    print("  3. See reference/adoption-profiles.md for profile details")
    if profile != "essential":
        print("  4. Copy templates/project-intake-template.md to docs/intake.md")
    else:
        print("  4. Create docs/intake.md with project name, goal, constraints, and Profile: Essential")
    print()

    return 0
