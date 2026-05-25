"""Refresh harness infrastructure files without overwriting project-specific docs."""

import platform
import shutil
from pathlib import Path

from codex_automata.init import _harness_dir, _patch_hooks_for_windows

PROTECTED_DIRS = {"docs", "sdk", "src", "tests", "tasks", "review"}
PROTECTED_FILES = {"context-state.md"}


def run_update(target_str: str) -> int:
    target = Path(target_str).resolve()
    harness = _harness_dir()

    if not (target / "AGENTS.md").exists():
        print(f"Error: {target} does not appear to be a Codex Automata project (no AGENTS.md found).")
        return 1

    updated = []

    # Update infrastructure files (AGENTS.md, PLAYBOOK.md, agent/, .cursor/, .github/, scripts/)
    infra_items = ["AGENTS.md", "PLAYBOOK.md", "agent", ".cursor", ".github", "scripts"]
    for name in infra_items:
        src = harness / name
        if not src.exists():
            continue
        dest = target / name
        if src.is_dir():
            shutil.copytree(src, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dest)
        updated.append(name)

    # Update templates (add new ones, update existing, but don't remove user-added files)
    tmpl_src = harness / "templates"
    tmpl_dest = target / "templates"
    if tmpl_src.is_dir() and tmpl_dest.is_dir():
        for f in tmpl_src.iterdir():
            if f.is_file():
                shutil.copy2(f, tmpl_dest)
        updated.append("templates/")

    if platform.system() == "Windows":
        _patch_hooks_for_windows(target)

    print()
    print(f"Codex Automata harness updated at: {target}")
    print(f"Refreshed: {', '.join(updated)}")
    print("Project-specific directories (docs/, sdk/, src/, tests/, tasks/, review/) were not modified.")
    print()

    return 0
