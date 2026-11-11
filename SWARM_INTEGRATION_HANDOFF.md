# Codex Automata runtime integration handoff

Contract: methodology **1.0**, CLI **0.6.0**, artifacts/job/control database **v1**,
installation **namespaced-v1**, Python **3.10+** with `jsonschema>=4.18,<5`.
Read `METHODOLOGY.json`. Pin the exact reviewed Git commit from the delivery PR;
never integrate an unpinned moving branch. No private runtime implementation is
included or required. Start with one coding worker, not distributed orchestration.

## 1. Verify the pinned release before integration

```bash
git checkout YOUR_REVIEWED_COMMIT
python -m pip install ./cli
codex-automata --version
python -m unittest discover -s cli/tests -v
python examples/standalone_workflow_demo.py
codex-automata workflow contract profiles
codex-automata workflow contract plan
```

Require the tests to pass and demo to report completed-local, six phases, six
observed commands, explicit self-review, bounded context and no external services.
The demo uses a real temporary Git repo/SQLite/subprocesses, then removes it.
`YOUR_REVIEWED_COMMIT` is an integration input, not a fabricated release SHA.
Record the actual `git rev-parse HEAD`, wheel hash and host test results in your
runtime's dependency lock and integration evidence.

## 2. Ownership and installation

```bash
codex-automata init ./consumer --config /operator/reviewed-project.json --agent generic
codex-automata migration ./legacy-consumer
codex-automata update ./consumer --staging ./reviewed-candidate
```

Project configuration schema: `cli/codex_automata/contracts/project.schema.json`.
Managed assets and schemas install under `.automata/`, with hashes in manifest.json.
Application code, SDK, tests, documentation, runtime data, tools and entry points
remain at configured consumer-owned paths. Existing AGENTS/IDE/hooks/CI are never
overwritten. Review routing adapter candidates; do not activate full development
rules globally. Legacy migration reports ambiguous ownership and deletes nothing.
Remove old always-on rules only after ownership review. Updates stage candidates
and customization reports; apply reviewed diffs rather than replacing application
files. Maintenance can edit managed assets under explicit authority; DEVELOP
stays blocked until integrity is reconciled through a reviewed manifest/update.

## 3. Isolate the actual authority boundary

The runtime owns inference, capacity, scheduling, host agents, GPU management,
process isolation, operational tools, credential access and remote adapters.
Codex Automata makes methodology decisions and runs frozen checks only.

Run controller authority outside model-readable/writeable scope. Keep one shared
SQLite database outside Git/application runtime state. Do not expose `bootstrap`,
`authorize`, `approve`, unrestricted SQL/filesystem access or authority secrets as
model tools. The Python CLI is not a sandbox. If workers can run arbitrary shell
as the controller user, these boundaries are advisory until you isolate them.
Use a broker/tool service or constrained process credentials for enforcement.

Operator steps:

1. `context bootstrap --state /secure/control.sqlite` returns an authority token.
   Store it in an operator-only file outside the repository; never log it to agents.
2. Create a grant following `grant.schema.json`: actor/task/repository/context,
   exact capabilities/write paths, policy version, reason and superseded grant IDs.
3. `context authorize --state ... --authority-file /secure/authority.key --grant grant.json`
   returns a separate task grant/token. Retain it under the intended actor's control.
4. `context select --state ... --grant-file /secure/task-grant.json` records transition
   evidence and effective capability intersection. Grant selection, not prompt text,
   determines context. Missing context denies changes.

Use DEVELOP for development, OPERATE for application operations, and separately
granted MAINTAIN_METHODOLOGY for managed policy changes. Configured forbidden paths
always deny. DEVELOP excludes application runtime state and methodology writes.
OPERATE can invoke only configured exact runtime/MCP capabilities and cannot gain
source writes through a development prompt. Do not load PLAYBOOK/phase rules in
operation context. Persist supersession-aware grants, not a mutable mode flag.

Before each actual tool side effect call:

```python
from codex_automata.control import Controller
from codex_automata.isolation import ContextController
controller = Controller('/secure/control.sqlite')
try:
    decision = ContextController(controller).evaluate(
        project_root, task_id, actor, 'file:write', 'packages/api/service.py')
    # Perform exactly that scoped action only after decision succeeds.
finally:
    controller.close()
```

`evaluate(root, task, actor, capability, path=None)` raises ControlError on denial.
Do not convert denial to success. Read/Write/Edit hooks map exact input.path or
input.filePath. MCP uses tool_name `MCP:<tool>` plus mcp_server_name, mapped to
`mcp:<server>:<tool>`. `context selftest --state ... --project ... --task ... --actor ...
--payload event.json` evaluates synthetic events; it does not intercept execution.
Unknown/unrestricted tools deny. Validate your actual host payload schema first.

## 4. Use the existing workflow rather than rebuilding gates

Task packet: existing `job.schema.json` plus Git-aware `validate_job` validation.
Use real local IDs; no Linear identifier is required. `workflow draft --help`
emits packet v1 with current Git baseline. The packet's legacy entry-job phase
is distinct from the recorded lifecycle; workflow phases come from profiles.json.

Operator execution plan: `plan.schema.json`. Freeze profile/impact declarations,
exact argv/role/tier/timeouts, optional per-check `output_limit_bytes`, acceptance-to-check mapping, selected context paths,
byte budget, review policy/lifetime and protected-change exceptions. Task risk
floors can raise requested rigor. The operator must review semantic impacts and
command meaning; filenames and green exit codes do not prove those properties.

```bash
codex-automata workflow approve --state /secure/control.sqlite --authority-file /secure/authority.key --packet job.json --plan plan.json
codex-automata workflow start --state /secure/control.sqlite --packet job.json --plan plan.json --owner coder
# Save returned claim token under the owning worker/controller, not in Git.
codex-automata workflow context LOCAL-1 --state /secure/control.sqlite --owner coder --token CLAIM
codex-automata workflow run LOCAL-1 --state /secure/control.sqlite --owner coder --token CLAIM --check static
codex-automata workflow run LOCAL-1 --state /secure/control.sqlite --owner coder --token CLAIM --check fixtures
codex-automata workflow run LOCAL-1 --state /secure/control.sqlite --owner coder --token CLAIM --check behavior --expect fail
codex-automata workflow advance LOCAL-1 --state /secure/control.sqlite --owner coder --token CLAIM --artifact phase.json
```

Only behavioral checks in mold phase may expect fail. Static/API/schema and real
fixture checks must pass first. After implementation, run all frozen plan checks
with expected pass. T0/T1/T2 name targeted/suite/configured host matrix; the local
executor records its host observation only. A wrapper claiming T2 must genuinely
run the required remote matrix and retain authenticated results; a tier label is
not proof of multiple hosts.

Workflow output defaults to a 1 MiB cap (operator-configurable up to 16 MiB).
Overflow is a failed environment attempt even for expected red molds; receipt
hash/count covers the captured prefix only. POSIX cleanup kills the command's
process group on timeout, overflow, interruption and parent completion. Windows
direct-child termination and detached POSIX descendants require external process
containment. These limits cover captured output, not arbitrary file writes.

Commands commit durable intent before launch, with one unresolved command per
repository in a shared controller database. Checkpoints and `workflow runs` expose
history. Interruption blocks replay until operator-only `workflow reconcile-run`
records evidence and confirmation that the original command/descendants stopped.
Reconciliation consumes a failure attempt and invalidates reuse of prior passing
receipts; resolve the environment failure before retry. The runtime must stop and
inspect processes/side effects before asserting `--confirm-stopped`. See
[execution recovery](docs/development/execution-recovery-spec.md).

CLI 0.6.2 defaults to a separate raw-blob commit snapshot for every check. Supply
dependency bootstrap in the approved command or a reviewed dependency adapter;
ignored dependencies and `.git` are absent. Exact-plan `verified-worktree` mode
supports compatibility while retaining tracked-content checks and flag rejection;
its receipt does not claim ignored-source exclusion. Process environment secrets
and import paths are not inherited. Neither mode is an OS sandbox or a dependency
attestation. See [evidence and lifecycle corrections](docs/development/evidence-lifecycle-fixes.md)
for size/path restrictions, planned future outputs and reviewer issuance/rewind
rules. Legacy job-only APIs still require existing references. Do not issue the
reviewer token to the coding worker or treat a coder-side timestamp as renewal.

Artifact schema: `artifact.schema.json`; phase-specific outputs pin committed
regular Git blobs. Current-head checks precede cast/review/product/observe exits.
All prior contract/mold pins must remain unchanged. Existing protected artifacts
need an operator-approved exception and independent review; do not make tests
permanently immutable. Invalid output/phase/version/pin/check/scope fails closed.

Independent review uses a separately granted reviewer process:

```bash
codex-automata workflow attest-review LOCAL-1 --state /secure/control.sqlite --reviewer-grant-file /secure/reviewer-grant.json --artifact review.json
# Owning controller then advances using exactly that attested review artifact.
```

A different reviewer name alone is insufficient. The reviewer token must be kept
from the implementer. The operator remains responsible for actual independent
reasoning. Low-risk self-review is explicitly labeled; it never promotes security
findings to verified truth or waives application-specific diverse-verifier policy.

Completion at observe requires fresh review, all current-head checks and ancestry
into the task's integration branch. It emits completion.schema.json with local
status and `deployed: false`; the runtime owns merging/deployment authority.
Legacy `job complete` cannot complete workflow jobs using supplied observations.

## 5. APIs, outputs and compatibility

Public pinned entry points:

- `Controller(path)`: existing validate/route/claim/attempt/resolve/checkpoint/release,
  state and operation journal methods. Explicitly close it; no connection leak.
- `ContextController(controller)`: bootstrap(), authorize(authority, grant),
  select(grant_token), current(root, task, actor), evaluate(...).
- `Workflow(controller)`: approve(authority, job, plan), start(job, plan, owner),
  context_packet(task, owner, claim_token), execute(task, owner, token, check_name,
  expect='pass'), advance(task, owner, token, artifact),
  attest_review(task, reviewer_token, artifact), snapshot(task),
  resume(task, owner, token, checkpoint), rewind(task, owner, token, phase, reason),
  reclaim(task, owner).
- `qualification.eligible(models, request)`: capability eligibility, never dispatch.
- `benchmark.prepare(...)`, `benchmark.evaluate(...)`: external-driver evaluation,
  not inference or a methodology effectiveness claim.

`workflow contract NAME` prints profiles or job/project/grant/plan/artifact/
verification/checkpoint/completion/model/benchmark schemas. JSON CLI success is
exit 0, gate rejection exit 1 (argparse syntax errors exit 2). Workflow execution
returns a receipt even on a failed check and exits nonzero. Evidence source is
local-executor; supplied review/model telemetry is explicitly distinguished.
Context uses compact canonical JSON with exact UTF-8 byte ceiling, excluding its
trailing CLI newline. Output budget is enforced too. Tokens require your model's
actual tokenizer; do not equate bytes and tokens.

Pin the Git revision and wheel. Unknown schema/database versions fail closed.
Active workflow state records a digest of the CLI version, workflow definition,
schemas and phase instructions. Mismatch blocks continuation; keep the original
release installed or explicitly replan/migrate with preserved history. Never
silently rewrite active packets. Existing legacy job/journal v1 remains supported;
legacy evidence is still observation-only and is unsuitable for unattended release.

## 6. Recovery and optional external services

Export `workflow checkpoint TASK --state ...` to a per-agent/task file outside
application runtime data. Resume validates authoritative DB history, clean head,
pins, failures and budget. Exports cannot recreate lost authority or reset attempts.
Restore the trusted DB too when moving controllers; repository relocation requires
a reviewed replan. Unexpected command failures consume persistent attempts.
Environment failures require `job resolve` with evidence; capability retries stay
within budget. Model substitution preserves the same task and attempts.

After a stopped worker, `job release` then `workflow reclaim` preserve partial
implementation. Never steal claims by elapsed time. `workflow rewind` retains
superseded artifacts and revisits required earlier phases after review rejection.
Re-read files after interrupted edits; do not replay unknown side effects.
Existing journal prepare/uncertain/reconcile provides intent identity only, not
remote execution. Authenticated Linear/GitHub adapters remain runtime-owned.

Linear maps outcome/scope/acceptance/dependencies to packet fields and pins Git
contracts. Publish bounded quota-aware batches, preserve overflow drafts, propose
child readiness from actual completion receipts and archive authorized completed
work through available adapter/UI. No remote synchronization or archive API is
implemented here. Record proposed versus observed remote state honestly.

## 7. Integration acceptance gate

Before broad deployment, demonstrate in your own runtime:

1. Populated monorepo install/update preserve application files and custom rules.
2. A single worker completes an actual task through this CLI/API and bounded context.
3. The same application operates without development rules/hooks or source writes.
4. Prompt text, model substitution, stale grants and fabricated receipts cannot
   bypass adapter checks, approval, risk, review, scope or retry gates.
5. Static and real SDK fixture checks catch intentionally malformed fixtures before
   interpreting behavioral red; test/contract changes require reviewed exceptions.
6. Interrupted/rejected tasks resume/reclaim/rewind without duplicate side effects
   or reset attempts; new-head work cannot reuse old check/review evidence.
7. Required platforms/hosts pass actual current-head checks. Retain independent
   review, process-tree isolation and provider approval evidence.
8. Run repeated paired live-local-model benchmark trials before claiming improved
   engineering outcomes; the shipped eight-task corpus is only a smoke benchmark.

Keep scheduling/inference/operational policy in the consuming runtime. Do not copy
private runtime code into this public methodology or reimplement its gates as
prompts. Remaining trust boundaries are in the adversarial audit and runbooks.

Session entry checks: `session inspect --project PATH --publication-required
--branch BRANCH` observes current remote HEAD and fails an unmet publication
requirement. Omit the flag for explicit local-only N/A. `session readiness
--packet child.json --state ...` produces a dependency-receipt-backed Ready proposal,
without remote writes. Optional plan context_excerpts supplies pinned inclusive
line ranges; every supplied context packet is journaled with its exact digest.
