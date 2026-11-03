# Proposed operating model: Codex, Linear, and GitHub

Status: Proposed, not activated. Version: draft 1. Date: 2026-11-03.
Task: [PER-10](https://linear.app/jacobkrell/issue/PER-10).
Companion: [gap assessment](agent-delivery-gap-assessment.md).

This proposal operationalizes the existing Research → Documentation → SDK →
Tests → Code pipeline. It adds no principle or pipeline phase. Codex executes
scoped tasks, Linear exposes flow, and GitHub records integration evidence.
The first pilot is manual and coordinator-driven; no webhook or unattended
merge/deployment service is assumed.

## 1. Authority and identity

| Question | Authority |
| --- | --- |
| What behavior is intended? | Reviewed specification and interface contracts at pinned Git revisions |
| What is the allowed constraint surface? | SDK and block registry at the assigned revision |
| What must pass? | Specification-derived test plan and required CI checks |
| Who may write which files now? | Committed agent-task assignment and context-state Current Work, maintained by one coordinator |
| What should be worked next? | Linear priority and dependencies, subject to repository readiness gates |
| What was integrated? | GitHub PR, reviewed head SHA, required check results, merge commit, and target branch |
| Where does the next session resume? | Committed context-state checkpoint |

Linear is a projection of execution state, not a second specification or a
distributed lock. If sources disagree, stop affected work, inspect authoritative
artifacts, and record reconciliation before resuming. Chat may notify an agent
where to look; it must not silently change contracts or task decisions.

Every assignment records: issue ID and URL; task ID; exact repository and target
branch; base SHA; specification sections; contract/SDK revision or explicit
not-applicable rationale; test plan; allowed write paths; agent/session identity;
worktree and branch; iteration/time budget; checkpoint; blockers; evidence paths.
Use stable provider IDs as well as display names for workspace and repository
checks. Credentials never belong in assignment records.

## 2. Roles, ownership, and isolation

The human owns intent, domain/risk classification, scope decisions, and approvals
required by existing guardrails. One coordinator handles task claims, phase
readiness, context-state updates, and sequential integration. The caster writes
only assigned files. The reviewer examines a pinned head in a separate worktree,
does not edit casting, and records findings tied to specification and file lines.
An agent review supplements human review; it does not impersonate approval.

Pilot concurrency: one caster plus one reviewer, with one implementation item
active. This bounds the kanban guide's unlimited casting station using the
multi-agent guide's practical scaling rules. Parallel implementers are deferred
until independent bounded contexts and frozen contracts exist.

The coordinator commits the claim before launching a writer. A second claim for
overlapping paths is rejected. A claim is not abandoned merely because a timer
expires: verify the prior session stopped, inspect its worktree and uncommitted
changes, record a checkpoint, then release or reassign it. Preserve unfinished
work. If the coordinator is interrupted, reconcile before launching any writer.
No parallel coordinators or claims are supported by this manual pilot.

Declare the coordination branch and context-state path in the task packet. Before
claim, handoff, reassignment, or resume, refresh that branch and read its latest
committed ownership record, not the stale copy in an agent worktree. A stale or
unavailable coordination ref prevents new claims. The coordinator serializes
ownership commits and records their SHA in each assignment.

Follow the [iteration budget](../../reference/iteration.md): three attempts per
failure cluster across consecutive sessions on the same checkpoint by default.
Redispatch does not reset that count. On budget exhaustion, preserve the work,
checkpoint attempts and failure evidence, and escalate to the human before a
clarified or repaired task receives a reset budget.

Only the coordinator writes shared context-state ownership records. Review
findings live in a task-specific review artifact. SDK/contract changes stop all
affected casting and follow the existing approval and revision process.

## 3. Linear projection and readiness

Use existing workspace statuses initially. Record station and blocked reason in
the issue description; no API capability to create custom statuses is assumed.

| Linear state | Meaning and transition condition |
| --- | --- |
| Backlog | Candidate, missing intake decisions, or work deliberately deferred |
| Todo | Scoped next task; assigned station and prerequisites are explicit |
| In Progress | Coordinator has claimed the task and recorded its active phase |
| In Review | Output and evidence are ready for the required review at a pinned SHA |
| Done | Task acceptance is satisfied and changes merged; required post-merge verification recorded |
| Canceled | Explicitly abandoned, with rationale and preserved checkpoints |

Blocked work keeps its truthful non-completed status and carries a blocker,
dependency ID, owner, and next unblock condition. Do not invent a Blocked status.
A merged specification task may be Done while its dependent casting task remains
Backlog. Merged application work may be Done without deployment only when its
scope excludes deployment; release acceptance is tracked separately.

Todo never bypasses station gates. Casting requires a reviewed specification,
available frozen constraint surface (or profile-appropriate colocated types),
derived molds, authorized write scope, and available review capacity. A quick
change must justify the existing spec/SDK/test coverage it relies on.

## 4. GitHub handoff and gates

Declare the integration branch at intake, using main only if the consumer has
chosen it as the single integration line. Branch names include the issue ID.
Each PR links its task, exact spec sections, bounded context, changed behavior,
validation commands/results, evidence, and material limitations.

Before review, pin the PR head SHA. Any subsequent commit invalidates the pilot's
review evidence until re-reviewed. Require current checks at that head, resolved
blocking findings, and the existing human approval rules. Record whether branch
protection is actually configured; a workflow file alone does not enforce merge
policy. Never report remote checks as passing from a local run.

Merge one PR at a time. Rebase or merge the updated integration branch into the
next candidate, rerun affected checks, and review its resulting head. On semantic
conflict, consult specifications; ambiguity stops the line. After merge, update
context-state and then Linear. Failure to update Linear leaves a reconciliation
item, not a second merge or a repeated external effect.

## 5. Service failure, events, and action boundaries

At session start verify the intended Linear workspace ID, team ID, repository,
and target branch. Never route work into another accessible workspace by default.
For the Tidal pilot the approved workspace is Personal at
`https://linear.app/jacobkrell`, ID `4689e010-c8a0-45e1-927e-ecb382ff66c7`;
the team is PER, ID `080e9c6e-c441-417d-b08d-7a78de25183f`.
These values are consumer configuration examples, not harness defaults.

If Linear is unavailable, already claimed work may continue within its frozen
scope; record a pending update locally. No new assignment is launched without a
verified claim. If GitHub is unavailable, local evidence may be prepared but no
merge or remote check result is inferred. Re-read service state before retrying
a mutation whose outcome was uncertain.

A future event adapter must use provider event IDs for deduplication, PR SHA and
entity version for freshness, and a durable pending-operation journal. Never
order events solely by delivery time. An old PR-close event cannot close a
reopened task or one now linked to a different PR. Duplicate merge events must
not repeat transitions or external actions. Reconciliation reads current remote
state before projecting it into Linear. This is a required future contract,
not an implemented exactly-once guarantee.

Use existing authenticated tooling and least necessary scopes. CI must not run
untrusted PR code with write tokens. Do not add secrets to issues, prompts,
artifacts, or logs. External messaging, deployment, payment, and publishing stay
under the user's authorization and existing guardrails. An issue assignment is
not blanket authorization for unrelated external actions.

## 6. Brownfield pilot and acceptance scenarios

Proposed consumer: `0xhackerfren/Model-Hosting-Website`. Do not import unrelated
company code, prompts, specifications, or artifacts. Removing an earlier import
does not establish IP ownership. This proposal does not modify the consumer.

Start with the brownfield audit and Essential profile on one selected module.
The human confirms its risk and intended behavior. The initial two-agent pair
uses one caster and one reviewer; multiple implementers require the Standard
profile and frozen cross-context contracts. Rehearse harness adoption in a
disposable copy, diff every existing instruction/CI path, and preserve consumer
source and configuration. Do not run a blanket initializer over the live checkout.

The existing Windows report-test portability issue is a candidate pilot, subject
to confirming specification intent. Do not weaken privacy checks to obtain green
tests. Hardware qualification and new swarm features remain separate tasks.

| Scenario | Required observable outcome |
| --- | --- |
| A1: missing specification or molds | Coordinator refuses casting; issue records the unmet gate |
| A2: two writers claim the same files | Only the first committed claim launches; the second waits |
| A3: session interruption and reassignment | Worktree is inspected, checkpoint preserved, prior writer stopped before replacement |
| A4: contract change requested | Affected work pauses; updated spec/SDK approval and revision precede resumption |
| A5: commit added after review | Old review SHA is rejected; current checks and renewed review are required |
| A6: failing test runner or unsupported source layout | Gate fails explicitly or reports not configured; neither counts as acceptance |
| A7: duplicate/stale remote update | Manual reconciliation makes no duplicate merge and does not close newer work |
| A8: wrong workspace or unavailable service | No cross-workspace write; bounded local continuation and pending update recorded |
| A9: successful small task | Spec → mold → casting → review → current checks → sequential merge → checkpoint → Done is traceable |
| A10: consumer harness collision | Adoption rehearsal exposes the diff and preserves original files before any approved application |

A1 through A10 are manual pilot walkthroughs initially. Executable coordinator
or synchronization code requires specification-derived automated molds for the
same cases before casting. Record observed results separately from expectations.

## 7. Rollout and exit decision

1. Review this proposal and explicitly choose the pilot scope and profile.
2. Prepare the consumer audit, task packet, and adoption rehearsal as a separate
   change. Update the existing provisional backlog to reflect readiness.
3. Run one bounded task with a caster/reviewer pair and human integration owner.
4. Record elapsed task time, blocked time/reason, review rounds, overlap attempts,
   stale evidence rejections, and reconciliation failures. Record cost only when
   observed; do not infer model cost from an uninstrumented session.
5. Expand only after all applicable scenarios have evidence and unresolved gaps
   are explicit. Stop and restore single-agent flow if ownership or evidence
   cannot be reconciled. Preserve worktrees and artifacts during rollback.

Manual coordination comes first. CLI record validation, native Codex agent task
dispatch, and automated provider synchronization are separately scoped future
changes, in that order. They are not prerequisites for adopting the method.
