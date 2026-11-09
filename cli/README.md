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

Initialize a new project with the methodology harness. Requires Python 3.10+.
Existing harness destinations cause a no-write failure; rehearse adoption in a
fresh directory and merge a reviewed diff into an existing project.

```powershell
codex-automata init D:\projects\my-app
codex-automata init D:\projects\my-app --profile essential
codex-automata init D:\projects\my-app --profile complete --agent claude
```

Options:
- `--profile` (essential, standard, complete) - Adoption profile. Default: standard.
- `--agent` (cursor, claude, copilot, codex, generic) - Primary AI agent. Default: cursor.

### `codex-automata update [path]`

Stage an upstream harness in a new sibling directory (`<project>-automata-update`)
without modifying any project file. Review and merge the diff yourself. Existing
staging directories are never overwritten. Use `--staging`, `--profile` and
`--agent` to select a new staging path and the intended installation settings.
This intentionally replaces the older destructive in-place update behavior.

```powershell
codex-automata update
codex-automata update D:\projects\my-app
```

### `codex-automata verify [path]`

Run spec-check and divergence-gate enforcement scripts against a project.
Missing scripts and unavailable runners fail verification. These structural
checks do not replace acceptance tests, review or CI evidence. Automatically selects the platform-appropriate script (.ps1 on Windows, .sh elsewhere).

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

## Local delivery control plane (v1)

`job` and `journal` are executable local controls. They do not call models, send
provider requests, change Linear, merge PRs or deploy. The operator controls packet,
policy, database, identities, required checks and evidence inputs. These tools
protect against accidental agent coordination errors, not a malicious process
with unrestricted access to the same files. Keep the shared SQLite database and
claim tokens outside model write scope and outside the Git worktree.

```bash
codex-automata job validate job.json
codex-automata job route job.json --policy approved-models.json --state /secure/control.sqlite
codex-automata job claim job.json --owner worker-1 --state /secure/control.sqlite
codex-automata job state JOB-1 --state /secure/control.sqlite
codex-automata job checkpoint JOB-1 --owner worker-1 --token TOKEN --detail "Resume from failing boundary test" --state /secure/control.sqlite
codex-automata job attempt JOB-1 --owner worker-1 --token TOKEN --classification capability --detail "Expected X, observed Y; attempt evidence path" --state /secure/control.sqlite
codex-automata job release JOB-1 --owner worker-1 --token TOKEN --detail "Worker stopped; preserved branch and checkpoint" --state /secure/control.sqlite
```

`claim` requires a clean worktree at the assigned base. The returned token belongs
to that claim; `state` never reveals it. SQLite allows one active writer per
repository across processes sharing the database. No timeout steals a claim.
Release only after the worker has stopped; this tool cannot prove an arbitrary
external process has stopped. Lost-token recovery is deliberately not automatic.
Use one coordinator/database; different databases or machines do not coordinate.

`attempt` persists failure classification and consumes the job's fixed budget.
Capability failure routes toward an eligible frontier model. Environment, design
and authority failures block routing; `job resolve` with the same owner/token and
repair evidence clears the block without resetting attempts. Changed scope needs
a new reviewed packet. The operator must preserve the same failure-cluster history
when splitting/replanning tasks; cross-ID lineage enforcement is not implemented.

`job complete job.json --owner worker-1 --token TOKEN --evidence evidence.json
--required-check unit --state /secure/control.sqlite` validates supplied check and
review observations against the actual current clean Git head, packet digest,
allowed changed paths and integration-branch ancestry. Repeat `--required-check`
for every operator-required check. Evidence's own list cannot reduce these gates.
Do not let a ticket choose required checks or self-attest provider approvals.
This command validates observations; it does not authenticate GitHub observations
or reviewer identities. Never use manually supplied observations for unattended
merge/release. No merge/release command exists here.

`journal prepare OP-ID --payload expected-observation.json --state ...` records
a stable operation ID and expected entity/revision/desired-state observation.
`journal uncertain OP-ID --state ...` marks an unknown result without retrying.
`journal reconcile OP-ID --payload current-observation.json --state ...` confirms
only an exact expected observation. A changed revision or payload blocks automatic
acknowledgement. These commands never send remote effects; the adapter must obtain
fresh authenticated observations and explicitly reconcile unexpected revisions.

See [the contract](../docs/development/control-plane-spec.md) and
[control-plane tests](tests/test_control.py) for the v1 field definitions and
adversarial acceptance cases. Example packet/policy/evidence shapes ship in
`templates/delivery-control-example.json`; replace all placeholders. Example
models are disabled and do not imply any provider approval.
