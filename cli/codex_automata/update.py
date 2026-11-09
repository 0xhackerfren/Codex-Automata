"""Stage an upstream harness for review without replacing consumer files."""

from pathlib import Path

from codex_automata.init import run_init


def run_update(target_str: str, staging_str: str | None = None,
               profile: str = "standard", agent: str = "cursor") -> int:
    target = Path(target_str).resolve()
    if not (target / "AGENTS.md").is_file():
        print(f"Error: {target} has no AGENTS.md; select the intended project.")
        return 1
    staging = (Path(staging_str).resolve() if staging_str else
               target.with_name(target.name + "-automata-update"))
    if staging == target or target in staging.parents or staging in target.parents:
        print("Error: staging must be separate from the project directory.")
        return 1
    if staging.exists() or staging.is_symlink():
        print(f"Error: staging path already exists: {staging}")
        return 1
    rc = run_init(str(staging), profile, agent)
    if rc == 0:
        print(f"Upstream candidate staged at {staging}.")
        print(f"Review and merge the diff into {target}; no project files were changed.")
    return rc
