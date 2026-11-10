"""Stage an upstream harness for review without replacing consumer files."""

from pathlib import Path

from codex_automata.init import run_init


def run_update(target_str: str, staging_str: str | None = None,
               profile: str = "standard", agent: str = "cursor", layout: str = "namespaced") -> int:
    target = Path(target_str).resolve()
    if not (target / "AGENTS.md").is_file() and not (target / '.automata').is_dir():
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
    config = None
    report = None
    if layout == 'namespaced':
        from .isolation import read_json, verify_installation, migration_report, digest_file
        from .control import ControlError, safe_path, require
        import json
        if (target / '.automata').exists():
            try:
                # Read the original manifest even when customized assets fail integrity;
                # stage everything, never discard those local edits.
                old = read_json(target / '.automata/manifest.json')
                config = read_json(target / '.automata/project.json')
                profile = config['adoption_profile']
                require(old.get('schema_version') == 1 and old.get('methodology_version') == '1.0', 'Unsupported installation version')
                for name in old['managed']:
                    safe_path(name)
                    managed_path = target / '.automata' / name
                    require(managed_path.resolve().is_relative_to(target / '.automata')
                            and not managed_path.is_symlink(), 'Unsafe managed manifest path')
                custom = [name for name, digest in old['managed'].items()
                          if not (target / '.automata' / name).is_file()
                          or digest_file(target / '.automata' / name) != digest]
                report = dict(from_version=old['methodology_version'], to_version='1.0',
                              customized_managed_files=custom, consumer_files_replaced=[],
                              action='Review staged candidate; preserve customizations; no automatic replacement')
            except (OSError, ValueError, KeyError, TypeError) as exc:
                print('Error: cannot inspect installation: ' + str(exc))
                return 1
        else:
            report = migration_report(target)
    rc = run_init(str(staging), profile, agent, layout, config)
    if rc == 0 and report is not None:
        (staging / '.automata/migration-report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    if rc == 0:
        print(f"Upstream candidate staged at {staging}.")
        print(f"Review and merge the diff into {target}; no project files were changed.")
    return rc
