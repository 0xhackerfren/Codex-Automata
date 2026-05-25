"""Run spec-check and divergence-gate against a project."""

import platform
import subprocess
import sys
from pathlib import Path


def _find_script(target: Path, base_name: str) -> Path | None:
    """Find the platform-appropriate enforcement script."""
    scripts_dir = target / "scripts"
    if platform.system() == "Windows":
        ps1 = scripts_dir / f"{base_name}.ps1"
        if ps1.exists():
            return ps1
    sh = scripts_dir / f"{base_name}.sh"
    if sh.exists():
        return sh
    return None


def _run_script(script: Path, extra_args: list[str] | None = None) -> int:
    """Execute an enforcement script and return its exit code."""
    args = extra_args or []
    if script.suffix == ".ps1":
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script)] + args
    else:
        cmd = ["bash", str(script)] + args

    result = subprocess.run(cmd, cwd=script.parent.parent)
    return result.returncode


def run_verify(target_str: str) -> int:
    target = Path(target_str).resolve()

    if not (target / "AGENTS.md").exists():
        print(f"Error: {target} does not appear to be a Codex Automata project (no AGENTS.md found).")
        return 1

    failures = 0

    # Spec check
    spec_script = _find_script(target, "spec-check")
    if spec_script:
        print(f"Running spec-check ({spec_script.name})...")
        src_flag = "--src-dir" if spec_script.suffix == ".sh" else "-SrcDir"
        spec_flag = "--spec-dir" if spec_script.suffix == ".sh" else "-SpecDir"
        rc = _run_script(spec_script, [src_flag, "src", spec_flag, "docs"])
        if rc != 0:
            failures += 1
            print("  FAILED: spec-check found issues.")
        else:
            print("  PASSED.")
    else:
        print("Skipping spec-check: script not found in scripts/")

    # Divergence gate
    div_script = _find_script(target, "divergence-gate")
    if div_script:
        print(f"Running divergence-gate ({div_script.name})...")
        config = target / "divergence.json"
        extra = []
        if config.exists():
            cfg_flag = "--config" if div_script.suffix == ".sh" else "-Config"
            extra = [cfg_flag, str(config)]
        rc = _run_script(div_script, extra)
        if rc != 0:
            failures += 1
            print("  FAILED: divergence-gate found violations.")
        else:
            print("  PASSED.")
    else:
        print("Skipping divergence-gate: script not found in scripts/")

    print()
    if failures > 0:
        print(f"Verification completed with {failures} failure(s).")
        return 1
    else:
        print("All checks passed.")
        return 0
