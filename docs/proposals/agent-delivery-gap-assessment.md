# Gap assessment: Codex, Linear, and GitHub delivery

Date: 2026-11-03. Status: Open, assessment complete, recovery proposed.
Task: [PER-10](https://linear.app/jacobkrell/issue/PER-10).
Assessed baseline: `0eadaff08798a668af098084edd69cd6eb29f9f8`.
Classification: integration specification gap. Severity: Significant (proposed).

## Discovery and scope

The project owner requested operational adoption of the existing methodology
before adding a new development workflow to an existing application. This
assessment inspects repository artifacts, not external service guarantees.
It does not establish production exposure, legal ownership, or measured coverage.

The [operating model](agent-delivery-operating-model.md) is a proposal. No
application harness, webhook, agent launcher, or enforcement behavior is changed.

## Existing foundation

| Artifact | Verified capability | Operational gap |
| --- | --- | --- |
| [Multi-agent reference](../../reference/multi-agent.md) | Frozen interfaces, worktree isolation, scoped writers, independent review, sequential merge | No concrete issue-to-session identity, claim record, stale review handling, or service synchronization protocol |
| [Kanban reference](../../reference/kanban.md) | Pull-based stations and readiness policies | No mapping to a Linear installation; unlimited casting guidance needs an explicit pilot concurrency cap |
| [Context persistence](../../reference/context-persistence.md) | Versioned session checkpoint and current work | No authority rule for discrepancies between Linear, GitHub, and the checkpoint |
| [Agent task template](../../harness/templates/agent-task-template.md) | Specification, molds, scope, inputs, and acceptance | No required workspace identity, pinned base SHA, claim owner, reviewer SHA, or interrupted-session reconciliation |
| [Brownfield onboarding](../../reference/brownfield-onboarding.md) | Audit and incremental adoption with preserved application source | No verified safe import procedure for a consumer with existing AGENTS.md, CI, and templates |
| [CLI init](../../cli/codex_automata/init.py) | Profile selection; Codex selection omits Cursor configuration | Directory copy permits overwriting existing harness-path files; selecting Codex does not install a native subagent orchestrator |
| [Shipped CI](../../harness/.github/workflows/codex-gates.yml) | Spec, divergence, commit, and test jobs | Python fallback can finish successfully after runner failures; divergence job conditions inspect files before checkout; spec checks target src by default |

The CI findings are static observations. Failure propagation and job selection
need executable regression cases before changes to the shipped template.
Existing gate names do not prove semantic specification coverage.

## Required state and recovery

| Gap | Proposed requirement | Acceptance evidence before implementation closes it |
| --- | --- | --- |
| G1: artifact authority | Separate intent, execution ownership, and integration evidence | Conflicting-state walkthrough resolves without losing a checkpoint or closing an unmerged issue |
| G2: agent assignment | One coordinator serializes claims and assigns isolated worktrees | Duplicate claim rejected; paused session cannot be replaced without reconciliation |
| G3: lifecycle projection | Explicit readiness and state mapping without replacing pipeline phases | Missing specification or mold prevents casting even when Linear says Todo |
| G4: unreliable synchronization | Manual reconciliation first; idempotent, version-aware events later | Duplicate, stale, out-of-order, and unavailable-service scenarios preserve authority |
| G5: gate reliability | Required checks bind to the current reviewed commit | A deliberately failing Python runner remains a failure; stale review blocks merge; paths are tested against representative consumers |
| G6: brownfield adoption | Inventory and diff harness changes before applying them | Existing instructions, CI, source, tests, and secrets remain preserved in a disposable-copy adoption rehearsal |

Recovery follows the existing pipeline:

1. Review this assessment and the proposed operating contract.
2. Specify task and evidence records using the existing template vocabulary.
3. Define SDK interfaces only if an executable coordinator is approved. A manual
   pilot needs documented records, not a new service or framework.
4. Derive molds from the acceptance scenarios in the operating model.
5. Implement narrowly scoped template or adapter changes after those gates.
6. Review the recovery unit and run the pilot before broader adoption.

No effort or token estimate is asserted without a scoped implementation task.

## Recurrence prevention and resolution

Treat a provider connection as a capability to verify, not as proof that its
workflow is configured. Keep reusable method changes upstream and consumer
configuration downstream. Do not turn a design document into an active policy
before its adoption decision is recorded.

Resolution remains open. Closing G1 through G6 requires the evidence above;
merging this assessment alone does not close them.
