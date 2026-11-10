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

Default `init` installs managed assets under `.automata/`, preserves application
files and existing agent instructions, and leaves execution context unselected.
Provide `--config` for custom/monorepo source, test, spec, SDK and runtime paths.
No application directories are created. `--layout legacy` explicitly retains the
old root-copy behavior for compatibility.

```bash
codex-automata init ./app --profile essential --agent codex
codex-automata init ./monorepo --config reviewed-project.json
codex-automata update ./app --staging ./candidate
codex-automata migration ./legacy-app
codex-automata verify ./app --state /secure/control.sqlite --task LOCAL-1 --actor coder
```

`update` stages a candidate and reports customized managed files and ambiguous
legacy ownership; it replaces no project files. `verify` on the isolated layout
requires DEVELOP and configured checks; installation integrity alone is not a
behavioral pass. Legacy verification retains the structural shell gates.

`context` supplies operator bootstrap/grants, selection, decisions and hook
selftests. Do not expose bootstrap or authorization to agent tools. `workflow`
provides exact-plan approval, local task drafting, phase transitions, command
execution, bounded context, reviewer-token attestation and recovery. `model
eligible` makes capability decisions without dispatch. `benchmark` prepares and
evaluates three instruction arms without invoking a model.

See the [isolation contract](../docs/development/isolation.md),
[workflow contract](../docs/development/workflow-v1.md),
[evaluation contract](../docs/development/benchmark-and-qualification.md) and
[integration handoff](../SWARM_INTEGRATION_HANDOFF.md) for executable interfaces.

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
