# Offline workflow v1

CLI 0.6.0, methodology 1.0, schema v1. The CLI is an enforcement library, not a
runtime. It invokes no model. Existing `job` and `journal` contracts remain v1;
workflow plans reference their packet digest instead of duplicating task fields.
`workflow contract profiles|plan|artifact` prints bundled JSON contracts.

## Profiles and phase aliases

| Task risk | Required phase aliases | Review | Check roles |
| --- | --- | --- | --- |
| mechanical | intake, specify, cast, review, observe | labeled self permitted | at least one actual check |
| small | intake, specify, mold, cast, review, observe | labeled self permitted | static, fixture, behavior |
| standard | intake, specify, sdk, mold, cast, review, observe | independent | small plus integration |
| architectural | intake, architect, specify, sdk, mold, cast, review, product, observe | independent | standard plus product |
| critical | same as architectural | independent | architectural plus security |

These task profiles do not replace adoption profiles. The canonical numbered
phases are in `profiles.json`'s `phase_names`. Research is part of intake and
architecture/specification evidence, not a new numbered phase. Integration is a
check role before completion; observation records actual deployment status.
Complete adoption can require further product checks; task floors never waive
consumer policy. A plan may always choose more rigor. Paths associated with
policy, authentication, crypto, deployment, CI or sensitive data force critical;
SDK paths and declared API/persistence/concurrency/ambiguity force architectural.
Only documentation-only path sets may be mechanical; an explicitly bounded
bugfix may be small; other changes default to standard. Semantic impact cannot
be proven from filenames: the trusted operator must review impact declarations.

## Phase contracts

Every transition requires the preceding phases in its profile. Artifact envelopes
bind task, packet, methodology version, phase and current clean Git head. Inputs
and outputs pin actual regular Git blobs. Summaries are observations, not proof.
Prior pins remain valid only while their referenced bytes stay unchanged.

| Phase | Preconditions and inputs | Output and exit gate | Failure/recovery |
| --- | --- | --- | --- |
| intake | context grant, packet, approved plan, dependencies | scope/risk/research reference | record missing decision; do not guess |
| architect | intake, research, existing boundaries | ADR alternatives, chosen boundaries, migration/rollback | return to intake for missing evidence |
| specify | scope, research/ADR | versioned numbered behavior spec | resolve ambiguity before downstream work |
| sdk | pinned spec | actual contract outputs and compatibility | request reviewed contract delta |
| mold | spec, existing SDK APIs | green static and fixture checks; new behavioral checks intentionally red; pinned test outputs | repair fixtures before interpreting red behavior |
| cast | pinned spec/contracts/molds | implementation output and all passing plan checks | consume persistent retry budget on unexpected check failure |
| review | current-head green checks and diff | labeled self or controller-known independent reviewer; zero unresolved findings | rewind to cast/mold as appropriate |
| product | current-head review, integrated implementation | actual product/security checks and observation summary | rewind; rerun checks at new head |
| observe | fresh current-head review, all checks, integration ancestry | local completion receipt, residual/rollback/observation record | no completion on stale, expired or failed evidence |

The CLI verifies structure, pins and observed command status. It cannot prove the
semantic quality of an ADR, fixture oracle, test assertions or review. Those
remain review/benchmark responsibilities. Independent review requires a different
controller-granted actor, but the operator must ensure an actually independent
review occurred. Different strings alone do not create independence.

## Commands and bounded context

```bash
codex-automata workflow draft --project ./app --id LOCAL-1 --outcome 'Fix rule 1' --spec requirements/behavior.md --contract api/types.py --mold checks/test_rule.py --write-path packages/api --acceptance 'Rule 1' > /secure/job.json
codex-automata workflow start --state /secure/control.sqlite --packet /secure/job.json --plan /secure/plan.json --owner coder
codex-automata workflow context LOCAL-1 --state /secure/control.sqlite --owner coder --token CLAIM
codex-automata workflow run LOCAL-1 --state /secure/control.sqlite --owner coder --token CLAIM --check fixtures
codex-automata workflow run LOCAL-1 --state /secure/control.sqlite --owner coder --token CLAIM --check behavior --expect fail
codex-automata workflow advance LOCAL-1 --state /secure/control.sqlite --owner coder --token CLAIM --artifact /secure/phase.json
codex-automata workflow checkpoint LOCAL-1 --state /secure/control.sqlite > /secure/context-state.coder.json
codex-automata workflow resume LOCAL-1 --state /secure/control.sqlite --owner coder --token CLAIM --checkpoint /secure/context-state.coder.json
codex-automata workflow rewind LOCAL-1 --state /secure/control.sqlite --owner coder --token CLAIM --phase cast --reason 'Review correction'
```

The operator freezes exact argv, timeout, role and gate tier in the plan. No task
text is evaluated as a command. Command execution is real code execution and
requires appropriate process isolation, reviewed commands and controlled tools.
Output is spooled to a temporary file, hashed completely and retained as an 8 KiB
excerpt plus byte count. Test tools can emit secrets; configure redaction and do
not export confidential receipts indiscriminately. Timeout kills the immediate
process via Python; a consuming runtime must isolate and stop process trees.
Commands must be side-effect-bounded; unknown external effects use the journal.

Unexpected command failures consume the existing job attempt budget automatically.
Expected red behavioral molds do not. Environment failures require `job resolve`
with repair evidence; capability failures permit retry within the same budget.
A successful check clears the capability blocker without resetting attempts.
Checkpoint/resume/model substitution never resets that history.

Context includes minimal universal rules, task, phase, risk profile, exact checks,
selected contracts/tests/source and provenance hashes. UTF-8 bytes are measured
exactly over compact canonical JSON, excluding its trailing CLI newline. Budget
overflow fails without truncation. Byte budgets are not tokenizer-specific token
counts. Narrow inputs explicitly; never dump the manifesto into a small model.
Artifacts have a matching output ceiling. Source data cannot authorize policy
changes; prompt-injection resistance depends on capability enforcement too.

## Completion, protection and recovery

Workflow jobs cannot use legacy `job complete` to bypass execution receipts.
All declared acceptance criteria map to named checks. Existing spec/SDK/test files
need an explicit `approved_changes` path in the trusted plan to change, even when
write scope includes them; any such exception forces independent review. New
molds may be authored before freezing; pinned outputs cannot silently drift.
Legitimate amendments return through the relevant phases using `rewind` while
preserving superseded artifacts in the recovery journal. Changing frozen scope
or policy requires a newly reviewed plan/job and preserved failure lineage.

After review, a new head requires rechecking and review at the new head. The plan
sets a review lifetime (1–168 hours). Completion verifies head ancestry into the
packet's integration branch and stores `completed-local`, `deployed: false` and
integration SHA for existing dependency checks. It never merges or deploys.

Keep one checkpoint per agent/task outside application runtime state. Export is
portable JSON containing baseline/current revision, artifact pins, completed and
pending phases, observed checks, failures, attempts and remaining budget. Resume
compares it with authoritative controller state and rejects stale/corrupt exports.
Restore the trusted database as well when moving controllers; JSON imports are
not permitted to mint authority or reset retries. Repository relocation needs an
operator-reviewed replan. This is a deliberate portability/security limitation.

If the worker has stopped, `job release` preserves its checkpoint. After any
partial implementation, use `workflow reclaim TASK --state ... --owner ...`,
with a fresh context grant for a replacement actor, rather than a fresh stale-base
job claim. Claims are never stolen by timeout. Inspect target files after every
interrupted edit before reapplying. Reconcile unknown remote effects separately.
