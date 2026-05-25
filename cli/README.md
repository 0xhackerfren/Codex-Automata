# codex-automata CLI

Command-line tool for initializing, updating, and verifying [Codex Automata](https://github.com/0xhackerfren/Codex-Automata) projects.

## Install

```bash
# With uv (recommended)
uv tool install codex-automata --from git+https://github.com/0xhackerfren/Codex-Automata.git --subdirectory cli

# With pip
pip install git+https://github.com/0xhackerfren/Codex-Automata.git#subdirectory=cli
```

## Commands

### `codex-automata init <path>`

Initialize a new project with the methodology harness.

```powershell
codex-automata init D:\projects\my-app
codex-automata init D:\projects\my-app --profile essential
codex-automata init D:\projects\my-app --profile complete --agent claude
```

Options:
- `--profile` (essential, standard, complete) - Adoption profile. Default: standard.
- `--agent` (cursor, claude, copilot, codex, generic) - Primary AI agent. Default: cursor.

### `codex-automata update [path]`

Refresh harness infrastructure files (AGENTS.md, PLAYBOOK.md, agent rules, Cursor config, scripts, templates) without overwriting project-specific directories (docs/, sdk/, src/, tests/, tasks/, review/).

```powershell
codex-automata update
codex-automata update D:\projects\my-app
```

### `codex-automata verify [path]`

Run spec-check and divergence-gate enforcement scripts against a project. Automatically selects the platform-appropriate script (.ps1 on Windows, .sh elsewhere).

```powershell
codex-automata verify
codex-automata verify D:\projects\my-app
```

## Development

```bash
cd cli
pip install -e .
codex-automata --version
```
