# Linear-first delivery: PLAN → EXECUTE → RECONCILE

## Purpose and authority

Concentrate scarce frontier reasoning on architecture, executable specifications,
and reconciliation. Route bounded implementation to the least expensive approved
model that passes verification. Optimize reviewed functionality per frontier
window, not issue count or specification length. Never infer credit availability,
reset times, model access, pricing or approval.

When available, Linear is the preferred durable work specification: goals, scope, milestones, dependencies,
priorities, acceptance criteria and status. Git is authoritative for versioned
behavior specifications, ADRs, SDK contracts, tests and actual implementation.
An issue links the required contract/spec revision rather than duplicating it.
Chat is not a source of hidden requirements. If sources conflict, pause affected
work and reconcile explicitly; issue edits never silently unfreeze an SDK.

This cadence wraps the existing pipeline and quality gates. It adds no phase or
principle. Upstream planning may specify SDK and test work as separate issues;
casting is Ready only after its profile-appropriate contracts and molds exist.
Discovery and documentation tasks need appropriate outputs, not artificial SDKs.
The same policy applies in this methodology repository and consuming projects.

## Select a mode

Use explicit mode when supplied. A direct request authorizes its stated scope;
mode syntax is not a permission ritual. If a broad build request has no executable
backlog, begin with PLAN. Existing covered small fixes may use quick-change.
Do not force unrelated maintenance through a new project or invented issue.

### MODE=PLAN

1. Read current local work packets or available Linear work, repository, tests and constraints. Verify the intended
   workspace/team/project before writes. Record observed facts separately from
   assumptions. Do not invent paths or commands.
2. Record a project brief using `templates/linear-project-brief-template.md`:
   outcome, non-goals, architecture, data boundaries, API contracts, failure cases,
   rollout and unresolved decisions. Link versioned ADRs.
3. Before mass creation, inspect available workspace quota/capabilities; record unknown limits as unknown and publish a bounded batch. Keep overflow drafts local with stable dependency keys. Decompose milestones into reviewable tasks using
   `templates/linear-issue-template.md`. Include research, contract, mold,
   implementation, integration and release work where relevant. Prefer near-term
   vertical slices; keep distant work coarse until evidence supports detail.
4. Review the dependency graph for cycles, missing integration work, shared-file
   conflicts and assumptions that would force an executor to redesign.
5. Publish only verified work as Ready. Output an ordered execution queue using
   `templates/execution-queue-template.md`. Identify unresolved decisions.

PLAN changes planning artifacts by default; implement product code only when the
user also requests it. Deep planning is useful only while it reduces downstream
uncertainty. Stop expanding speculative detail when a usable queue exists.

### MODE=EXECUTE ISSUE=<ID>

1. Fetch the current issue, dependencies and linked contracts; read relevant code
   and applicable instructions. Check the Ready gate below. Confirm the assigned
   base revision still matches current interfaces before beginning.
2. Use an issue branch/worktree, one bounded issue per PR. Record write ownership
   before any authorized parallel work; Linear status is not a lock. Do not launch
   additional agents merely because this workflow supports parallel execution.
3. Implement the smallest complete change under the frozen contracts. Derive
   tests from acceptance criteria; preserve independent molds. Never weaken tests
   simply to obtain a pass. Run only relevant checks, then self-review.
4. Record commands, outcomes, skipped checks, changed files, PR/head SHA and risks
   on the issue. Move to Review when required; Done requires the project's review
   and integration policy. Local tests do not prove remote CI or human approval.
5. Preserve unfinished work and checkpoint at interruption. A retry in a new
   session does not reset the existing iteration budget (three grounded attempts
   by default). Design contradictions, missing access or risk can block earlier.
   Record observed/expected behavior, attempts, evidence and the missing decision;
   move to another unblocked task rather than guessing repeatedly.

### MODE=RECONCILE PROJECT=<ID>

Read actual diffs, reviewed SHAs, checks, blockers and changed requirements.
Compare them to the intended work and versioned contracts. Update affected
issues/ADRs, preserve completed work, repair dependencies, and refill the queue.
A commit after review requires renewed evidence at the new head. Track first-pass
completion, escalation causes, integration defects and reviewed throughput.
Record costs only when measured.

## Ready gate

A fresh approved economical agent must be able to implement and verify the task
using only the issue, linked documents and repository. Require:

- Bounded outcome, scope, exclusions and prerequisite IDs with no open blockers.
- Exact interfaces, input/output/error behavior and relevant files or a separate
  discovery task. Casting requires existing specs, SDK/types and molds appropriate
  to the adoption profile.
- Observable positive and negative acceptance criteria, runnable verification
  commands, and evidence expectations. Unknown commands require discovery.
- Security/privacy restrictions, migration/rollback and review requirements where
  relevant. No secrets or client artifacts in unapproved systems.
- A single reviewable slice, usually 30 minutes to four hours; split tasks that
  require unrelated decisions. Time is a sizing heuristic, not a guarantee.

Use existing workspace statuses: Ready may be Todo plus a recorded readiness
check. Do not create statuses or claim transitions without observing them.

## Provider and failure boundaries

Use only engagement-approved models/providers for confidential client material.
Local execution also requires access and isolation controls. Pass only the issue
and relevant context; cheap capacity does not justify dumping full repositories.
No automatic model switching or provider upload is implemented by these rules.

If Linear is unavailable or intentionally unused, use first-class local job packets and completion records. Mark remote synchronization status explicitly; a local task does not need a fabricated issue ID. Continue authorized bounded work through the same gates. Re-read remote state before retrying an uncertain write; never invent an
issue ID or report drafts as published. Native templates require manual setup.
Do not place secrets, credentials or sensitive evidence in issues or checkpoints.

Consumer adoption is a separate reviewable change. Rehearse in a disposable
checkout, diff instructions/hooks/CI, and preserve local customizations. This
workflow authorizes no unattended merge, deployment or external messaging.

## First-class work graph

Linear is the preferred shared durable map when configured; local packets provide the same intent contract offline.
A fresh session reconstructs the intended system from project brief, issue graph,
linked versioned contracts and execution evidence. A conversation decision becomes
reliable handoff state only after it is recorded in the appropriate artifact.
A ticket establishes planned existence; it does not establish implemented reality.
Never infer a feature, integration or passing check from an issue's description.

Use [MODEL_ROUTING.md](MODEL_ROUTING.md) for job types, capability escalation,
failure classification and dispatch records. Job packets carry one phase and its
exit gate. Preserve GitHub's commit history, PRs, current-head checks, reviews and
release records as first-class evidence throughout the work lifecycle.

## Executable local gates

The Codex Automata CLI now supplies `job validate`, `job route`, `job claim`,
`job checkpoint`, `job attempt`, `job resolve`, `job release`, `job complete`
and `journal` commands. See the CLI README in the methodology repository for
usage and `templates/delivery-control-example.json` for packet shapes.

Before autonomous execution, the coordinator must configure one shared local
state database, an operator-owned approval inventory and trusted evidence inputs.
Validate the packet, check routing eligibility, then acquire a claim. Workers
receive only their bounded packet and claim. Record attempts/checkpoints before
redispatch. Complete only through current-head evidence validation. A claim
reserves ownership; it does not itself approve a model or authorize dispatch.
Absent that configuration, remain in explicitly manual coordination; never imply
that prose, a Ready label or a route recommendation enforces autonomous execution.

This v1 executes no model/provider calls, merges, deployments or remote writes.
It validates supplied observations; authenticated adapters must supply real
provider evidence before unattended integration is enabled. Keep the state
outside agent write scope. Separate state databases do not coordinate each other.

## Closure and child readiness

At closure, retain exact completed head, artifact paths, check tiers and review.
Reconcile children in dependency order: fill readiness from actual upstream
completion receipts and pinned Git artifacts, validate every dependency, then
propose the configured Ready/Todo transition. Never infer readiness from an
upstream title or Done label. The local controller already checks evidenced
ancestry; optional remote adapters must fetch fresh state and journal writes.

Archive completed issues only under the workspace's standing authorization,
after retaining linked evidence and confirming dependents can still resolve
artifacts. Archiving is reversible and distinct from deletion. Never delete work
to free quota. Verify current plan limits and archival semantics; do not assume
Done frees capacity. If the connected adapter lacks archive/quota APIs, record
that limitation and provide an operator UI reconciliation step. No remote archive
or child transition is implemented merely by this document.
