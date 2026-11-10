# Codex Automata

A portable, local-first engineering methodology and executable quality harness:
**Research → Specification → SDK/Contracts → Tests → Implementation → Review →
Product Testing → Deployment/Observation**. Build for the smallest qualified
model; use stronger approved reasoning when evidence warrants it.

[Manifesto](MANIFESTO.md) · [Playbook](harness/PLAYBOOK.md) ·
[CLI](cli/README.md) · [Swarm integration handoff](SWARM_INTEGRATION_HANDOFF.md)

## What it owns

Codex Automata owns engineering rules, task/artifact contracts, risk profiles,
context generation, gates, evidence and checkpoints. It does not own application
runtime behavior, scheduling, inference serving, GPUs, distributed workers or
production deployment. One coding agent can use it offline without Linear,
GitHub API access, a cloud model or a swarm.

The [twelve principles](reference/principles.md) and existing numbered phases
remain canonical. Specifications define intent, SDK/contracts constrain interfaces,
independently derived tests form molds, and code satisfies them. Passing checks
are evidence within their coverage, not a claim of universal correctness.

## Install without taking over the application

```bash
python -m pip install ./cli
codex-automata init ./my-project --agent codex --profile essential
# Brownfield and monorepo paths come from reviewed consumer configuration:
codex-automata init ./existing-project --config reviewed-project.json --agent cursor
```

Installation creates `.automata/` with managed assets, schemas and a manifest.
Application source, SDK, tests, documentation, runtime state, CI and existing agent
instructions remain consumer-owned. No `src/`, `sdk/` or `tests/` paths are assumed
or created. Configure paths, capabilities and checks in `.automata/project.json`.
A minimal root routing adapter is created only when AGENTS.md is absent. Existing
integration files are preserved; review candidates under `.automata/adapters/`.
Full development rules/hooks are never silently activated.

| Location | Ownership |
| --- | --- |
| `.automata/assets/`, `.automata/schemas/`, manifest | Managed methodology assets |
| `.automata/project.json` | Consumer project configuration |
| Configured application code, tests, SDK, docs and runtime state | Consumer application |
| Reviewed root/IDE routing adapters | Consumer integration |
| Control DB, authority secrets, checkpoints | External trusted controller |

`update` stages a candidate and migration report without replacing application
files. `migration` reports legacy ownership ambiguities without deleting anything.
The older root-copy layout remains available with explicit `--layout legacy`;
remove old always-on integrations only after reviewing their ownership.
See [isolation and migration](docs/development/isolation.md).

## Explicit execution context

| Context | Scope |
| --- | --- |
| DEVELOP | Scoped application development under engineering gates |
| OPERATE | Application operational instructions and registered tools |
| MAINTAIN_METHODOLOGY | Separately authorized methodology policy maintenance |

Missing context grants no development privileges. Installation alone never
selects DEVELOP. Operator/controller grants are dated, scoped and supersession-aware.
A prompt cannot issue authority. Context decisions must be enforced by the actual
tool adapter; the CLI is not an OS sandbox. Protect authority state from agent
access. See [bootstrap and hook selftest](docs/development/isolation.md).

## Standalone engineering loop

```bash
codex-automata workflow contract profiles
codex-automata workflow contract plan
codex-automata workflow contract artifact
# Runnable complete example, from this source checkout:
PYTHONPATH=cli python examples/standalone_workflow_demo.py
```

The operator grants context and approves an exact execution plan. A coding agent
uses `workflow start`, `context`, `run`, `advance`, `checkpoint` and `resume`.
Mechanical, small, standard, architectural and critical task profiles determine
required phases and review. They are separate from adoption profiles.

Checks execute approved argv and record exit statuses, output hashes, timings and
Git head in trusted state. Completion rejects missing/failed checks, changed code,
stale/expired review, scope violations, unauthorized test/contract changes and
exhausted retries. New behavioral molds begin red only after static contract/API
and real fixture checks pass. Independent reviews require a separate reviewer
grant-token attestation; low-risk self-review is labeled honestly.

Progressive context includes only universal rules, task/phase/risk requirements
and selected source references, with exact byte budgets and provenance hashes.
Checkpoints preserve revisions, artifacts, actual checks, failures and attempts;
exports cannot reset the controller's authoritative history.
See [workflow contract](docs/development/workflow-v1.md).

## Linear-first collaboration and GitHub

[PLAN → EXECUTE → RECONCILE](harness/agent/LINEAR_FIRST.md) remains preferred when
Linear is configured: spend scarce frontier reasoning on architecture, executable
specifications and reconciliation; implement bounded work with qualified economical
models. First-class local packets supply the same intent offline. Git preserves
versioned contracts and implementation truth. Issues are planned intent, never
proof that features exist. Remote synchronization, archiving, dispatch and merging
require optional authenticated adapters and are not implemented by prose.

## Qualification and evidence

`model eligible` filters measured capability/approval/availability profiles without
scheduling compute. `benchmark prepare` and `benchmark evaluate` support paired bare,
concise and Automata instruction treatments over eight deterministic task categories.
Live-model results remain pending. The small fixture corpus validates the evaluator,
not the methodology's superiority or production readiness. See
[qualification and evaluation](docs/development/benchmark-and-qualification.md).

## Validation and limitations

```bash
PYTHONPATH=cli python -m unittest discover -s cli/tests -v
npx markdownlint-cli2 --config .markdownlint.yaml '**/*.md'
git diff --check
```

See the [versioned gap assessment](docs/development/gap-assessment-2026-11-10.md),
[adversarial review](docs/development/adversarial-audit-2026-11-10.md), and
[retrospective adoption matrix](docs/development/retrospective-amendments.md).
Semantic review, authentic approvals, process isolation, test quality and real
consumer/model qualification remain essential. No unattended deployment or
production-readiness claim is made.

## License

[MIT](LICENSE).
