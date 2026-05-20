# Iteration and Loop Management

This document covers the structured approach to agent iteration, re-dispatch, and loop management in Codex Automata. Iteration is how the methodology survives long-running work across many sessions without relying on conversation memory.

For checkpoint handoff and context state updates, see [context-persistence.md](context-persistence.md). For gap escalation when iteration reveals missing specs or tests, see [recovery.md](recovery.md).

## Why Iteration Needs Structure

AI agents exhibit predictable failure modes in long-running conversations:

- **Context rot:** Accumulated chat history degrades attention to early decisions; the agent forgets constraints or repeats resolved debates.
- **Goal drift:** The agent gradually shifts away from the original objective toward tangential polish or unrelated refactors.
- **Premature completion:** The agent declares success before tests pass, review approves, or artifacts are updated.

Other methodologies address these with explicit loop discipline. The Ralph Loop methodology destroys conversation history between iterations and uses the file system as persistent memory. GSD clears context between tasks. SaifCTL locks agents in loops until tests pass. Codex Automata integrates structured iteration with its **artifact pipeline**: specifications, SDK, tests, code, context state—not chat transcripts.

## The Codex Automata Iteration Model

**Short, artifact-anchored sessions.** Each session:

1. Reads the context state file first (checkpoint, current work, blockers)
2. Performs **bounded** work mapped to spec section, SDK interface, and tests
3. Ends by updating context state (especially Checkpoint and Session History)

**Persistent memory is the file system.** Specifications, SDK interfaces, test plans, test code, and `context-state.md` survive session boundaries. Conversation history is **disposable**. A new session should reach full effectiveness by reading artifacts, not by reading prior chat.

**Progress is measured by artifact completion**, not conversation length: tests passing, spec sections approved, SDK modules frozen, review records filed, gaps closed—not “we discussed it for an hour.”

This model aligns with the **local-first** principle: structure tasks so the smallest viable model can complete them using retrievable artifact fragments, not entire repository history in prompt context.

## Iteration Within a Phase (Inner Loop)

The inner loop handles **failure and retry inside a single phase** without restarting the full pipeline.

### Trigger

A quality gate fails: test failure, review rejection, linter errors, contract test failure, divergence gate flag, or incomplete agent task acceptance criteria.

### Procedure

1. Read the failure output and identify the failing gate.
2. Read the relevant **specification section**, **SDK interfaces**, and **tests** for the affected behavior—not the entire codebase.
3. Attempt a fix **within the current phase’s authority** (for example, casting fixes implementation; it does not rewrite spec without escalation).
4. Re-run the failed gate and dependent tests.
5. Log the attempt in context state **Session History** (timestamp, gate, outcome, brief note).

### Attempt budget

Default: **three attempts** per failure cluster in the same session or consecutive sessions on the same checkpoint. After N failures, **escalate to human** with:

- What was tried
- Current failure output
- Whether the failure suggests spec error, test error, or implementation error

Humans may reset the budget after clarifying spec or fixing a broken test.

### When inner loop must stop

If the fix requires **specification change**, escalate to Phase 2 (or recovery for retroactive spec gaps)—do not iterate casting indefinitely.

If the fix requires **SDK extension**, escalate to Phase 3.

If the fix requires **new or rewritten tests** beyond edge cases already covered by spec, escalate to Phase 4.

Inner-loop iteration is for **implementation alignment**, not for renegotiating design.

## Iteration Across Phases (Outer Loop)

The outer loop handles **send-back** when a later phase invalidates earlier artifacts.

### Trigger

Review sends work back to specification (or any earlier phase). Architecture change ripples to contracts. SDK change invalidates tests. Security audit requires new failure modes in spec.

### Cascade

Typical cascade when spec changes:

```
Spec change → SDK may need update → tests may need update → code needs recast
```

Each phase runs its **own inner loop** until that phase’s gates are green before the next phase resumes.

The outer loop continues until:

- All active phases for the work unit are green
- Review approves (human for Standard/Complete; self-review checklist for qualified quick-change)
- Context state records completion and next checkpoint

### Checkpoint tracking

Context state **Checkpoint** must reflect outer-loop position:

- **Resume from:** Current phase and artifact (for example, “Phase 4, module billing, test plan §2”)
- **Prerequisites met:** What downstream phases can assume
- **Next action:** Single first step for the next session

When review sends work to Phase 2, do not leave Checkpoint pointing at Phase 5 casting.

## Token Budget Guidance

Long context windows do not replace artifact discipline. Structure work to stay within practical limits.

| Guideline | Recommendation |
|-----------|----------------|
| Per-task context | Keep individual agent tasks under **~100K tokens** of loaded context |
| Oversized tasks | Split into subtasks within the **same bounded context**; bridge with context state Checkpoint |
| Essential context for casting | Specification section, SDK interfaces for the module, assigned tests, design identity/tokens if UI |
| Avoid loading | Implementation source from **other** bounded contexts except via interface types in SDK |
| Subtask boundaries | Each subtask ends with Checkpoint update: prerequisites, next action |
| Model choice | Local-first: smallest model that can complete the subtask; escalate model only when task complexity requires it |

If an agent repeatedly hits context limits, the task granularity is wrong—split the agent task or the specification section, do not paste more chat history.

**Cost dimension.** Each iteration attempt has a token cost. The 3-attempt inner-loop budget implicitly caps per-problem spending. If a problem consistently consumes all 3 attempts across multiple modules, it may indicate a specification or architecture issue rather than an implementation issue. Escalate to human rather than spending more tokens on iteration.

Model tiering also controls cost: if the first attempt fails with a standard model, the second attempt may warrant a frontier model. If the third attempt fails with a frontier model, the problem is beyond iteration—escalate. See `reference/cost-awareness.md` for model tiering guidance.

## Stop Conditions

Work is **complete** only when **all** of the following are true:

1. **All assigned tests pass** (module tests, contract tests for provided interfaces, product tests if release-bound)
2. **Human review approves** (Standard/Complete), or **self-review checklist passes** for qualified [quick-change](quick-change.md)
3. **All quality gates clear:** lint, coverage thresholds, divergence gate, contract unchanged unless approved
4. **Context state updated:** completion noted in Current Work, Checkpoint set for next work or explicit idle, Session History appended
5. **No open blockers or escalations** on this work unit (Open Decisions resolved or explicitly deferred with human sign-off)

Declaring complete without updating context state fails the next session and causes duplicate or contradictory work—especially under [multi-agent](multi-agent.md) orchestration.

## Integration with Context State

Context state is the **control plane** for iteration and re-dispatch.

| Section | Iteration role |
|---------|----------------|
| **Checkpoint → Resume from** | Tells the next session exactly where to start after inner or outer loop pause |
| **Checkpoint → Prerequisites met** | Prevents redundant re-reads and rework; lists frozen artifacts safe to assume |
| **Checkpoint → Next action** | First concrete step; reduces goal drift at session open |
| **Session History** | Audit trail of inner-loop attempts, escalations, phase send-backs |
| **Current Work → Blocked** | Holds iteration stopped on human decisions or failed gates |
| **Known Gaps** | Links to recovery when iteration discovers spec/mold/SDK gaps |

### Re-dispatch protocol

When starting a new session (human or automated re-dispatch):

1. Read `context-state.md` in full.
2. Run context health checks from [context-persistence.md](context-persistence.md).
3. Execute **Next action** only after confirming **Resume from** still matches reality (phase drift check).
4. On session end, append Session History and rewrite Checkpoint even if work is incomplete—handoff must be honest.

Automated agents should treat stale Checkpoint (>3 sessions without update) as a blocker until reconciled with a human.

## Relationship to Quick-Change and Recovery

**Quick-change** uses a compressed inner loop (fix → test → self-review) without phase transitions. Escalate to outer loop or recovery when stop conditions cannot be met.

**Recovery** is a structured outer loop across phases applied retroactively when gaps are discovered. Iteration logging in Session History should reference gap assessment IDs when recovery is active.

## Anti-Patterns

- **Infinite inner loop:** Retrying casting when tests fail because spec is wrong—escalate after attempt budget.
- **Chat as source of truth:** Decisions only in conversation, not in spec or context state.
- **Mega-sessions:** One session spans multiple phases; no Checkpoint update until “everything is done.”
- **Skipping Session History:** Next agent repeats failed attempts.
- **Premature checkpoint to Phase 5** while SDK or tests are known stale.

## Companion Documents

- [context-persistence.md](context-persistence.md) — Context state file, update protocol, checkpoint discipline
- [PLAYBOOK.md](../harness/PLAYBOOK.md) — Phase gates that define outer-loop boundaries
- [AGENT_RULES.md](../harness/agent/AGENT_RULES.md) — Agent halt, escalation, and task mapping rules
- [recovery.md](recovery.md) — When iteration reveals spec, mold, SDK, or contract gaps
- [quick-change.md](quick-change.md) — Abbreviated iteration path for qualified small changes
- [multi-agent.md](multi-agent.md) — Parallel sessions and merge discipline across iterations
- [cost-awareness.md](cost-awareness.md) — Token estimates, model tiering, and cost optimization patterns
- [workflow.md](workflow.md) — End-to-end methodology and feedback loops
