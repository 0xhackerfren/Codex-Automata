# Quick-Change Path

This document defines when and how to use the quick-change path for small modifications that do not need the full eight-phase pipeline. Quick-change is a principled shortcut: it preserves traceability and constraint-surface discipline without the ceremony of research, architecture, SDK design, and full review cycles for work that already fits inside approved artifacts.

For phase-by-phase forward workflow when quick-change does not apply, see [PLAYBOOK.md](../harness/PLAYBOOK.md) in the harness. For agent operating constraints, see [AGENT_RULES.md](../harness/agent/AGENT_RULES.md) in the harness.

## Why Quick Changes Need a Defined Path

The full Codex Automata pipeline—research, specification, SDK design, test molding, code casting, review, product testing, and deployment—is designed for new modules, significant features, and cross-cutting work. Real projects also accumulate bug fixes, configuration tweaks, copy corrections, dependency bumps, and small behavioral adjustments that touch a single file in a single bounded context.

Forcing every such change through the full pipeline creates ceremony that discourages adoption and slows teams down. Work that legitimately fits inside existing specs, SDK surfaces, and molds gets delayed behind templates and phase gates that add no value for that scope.

Competing methodologies address this gap explicitly. BMAD offers Quick Dev. GSD uses Slices for incremental delivery. Codex Automata’s quick-change path provides a defined, principled shortcut that maintains traceability without full overhead: read existing artifacts, change within the constraint surface, verify existing tests, self-review, commit with spec traceability.

Quick-change is not “skip the methodology.” It is the methodology applied at minimum viable depth when all prerequisites are already satisfied.

## Qualification Criteria

**All** of the following must be true before using the quick-change path. If **any** criterion is false, use the full pipeline starting at the appropriate phase.

| # | Criterion |
|---|-----------|
| 1 | The change touches a **single bounded context** |
| 2 | An **approved specification** already covers the affected behavior |
| 3 | **SDK interfaces** already exist for the affected module |
| 4 | **Tests already exist** that cover the affected area |
| 5 | **No new SDK types, interfaces, or extensions** are needed |
| 6 | **No new specifications** need to be written |
| 7 | The change does **not modify interface contracts** |

When in doubt, run the criteria explicitly before starting. Ambiguity on criterion 2 (spec coverage) or criterion 4 (test coverage) usually means escalation, not quick-change.

## The Quick-Change Sequence

Follow these steps in order. Do not skip reading artifacts before editing.

### 1. Read the existing specification

Locate the specification section that covers the behavior being changed. Understand intended behavior, edge cases, and any explicit non-goals before touching code.

### 2. Read the existing SDK interfaces

Read the SDK types and interfaces for the module. The change must stay inside this constraint surface. If the fix “needs” a new type or method on the SDK, stop and escalate.

### 3. Read the existing tests

Read tests that cover the affected behavior. Know what the mold already enforces and what assertions will break if you change semantics unintentionally.

### 4. Make the change within the constraint surface

Implement the fix or adjustment using only existing SDK building blocks and patterns. Do not widen public APIs, alter shared contracts, or introduce abstractions outside the SDK.

### 5. Verify all existing tests pass

Run the full test suite relevant to the module (at minimum, all tests for the affected area). No regressions. Failing tests mean the change is wrong, the tests are wrong, or the spec does not match reality—diagnose before proceeding.

### 6. Handle newly revealed edge cases

If the change exposes an edge case that existing tests did not cover but that **fits within the existing specification**, add tests for that edge case and ensure they pass.

If the edge case requires **entirely new behaviors** not described in the spec, stop and escalate to the full pipeline (or recovery if the gap is in existing code).

### 7. Self-review with abbreviated checklist

Before marking work complete, confirm:

- Does the change stay within the specification? (**Yes** required)
- Does it stay within the SDK surface? (**Yes** required)
- Do all tests pass? (**Yes** required)
- Were any interface contracts modified? (**No** required)

This is a reduced form of Phase 6 review, not a substitute for human review when contracts, security, or cross-context impact are in play.

### 8. Commit with spec traceability

Write a commit message that references the specification section (for example: `fix(auth): align token TTL with spec §3.2 session expiry`). Atomic commits preferred.

### 9. Update context state if significant

For trivial fixes (typo, comment, config value within documented bounds), context state update may be optional per project policy. For behavioral changes, dependency bumps that affect runtime, or anything the next session must know about, update `context-state.md` per [context-persistence.md](context-persistence.md).

## When to Escalate

Escalation is mandatory when quick-change prerequisites fail or when work during quick-change reveals hidden debt.

| Situation | Escalation path |
|-----------|-----------------|
| Spec does not cover the behavior | **Spec gap** → [recovery.md](recovery.md) or full pipeline from Phase 2 |
| New SDK type or interface needed | Full pipeline from **Phase 3** (SDK Design) onward |
| Tests do not exist for the area | **Mold gap** → recovery or full pipeline from **Phase 4** (Test Molding) |
| Change affects **multiple bounded contexts** | Full pipeline; decompose and coordinate per [multi-agent.md](multi-agent.md) if parallel |
| Change modifies an **interface contract** | Human approval required + full review; not quick-change |
| New behaviors needed beyond existing spec | Full pipeline or spec amendment through normal phase gates |
| Security or compliance impact discovered | Security audit path; not quick-change |

When escalating, document the reason in context state Session History and Known Gaps if applicable. Do not leave partial quick-change work uncommitted without a clear handoff in Checkpoint.

## Relationship to Adoption Profiles

Quick-change is available at **all** adoption profiles: Essential, Standard, and Complete. Profile choice affects which other phases run for *new* work, not whether quick-change is allowed when criteria are met.

**Essential.** The lighter profile already assumes a simpler process for small scope. Quick-change is often the **default** for day-to-day fixes once a specification and tests exist for the module. Teams still must not bypass criteria 1–7.

**Standard.** Full pipeline runs for new modules and features. Quick-change **supplements** the pipeline for qualified small changes so teams do not open a full phase cycle for a one-line fix inside a mature context.

**Complete.** Same as Standard, with the addition that product testing and heavier gates apply to releases—not to every quick-change commit. If a quick-change affects user-visible behavior covered by product tests, run the relevant product test objectives before release even when the change itself used the quick-change path.

Profile upgrades do not invalidate quick-change; they expand when full pipeline is required for *new* capability.

## Anti-Patterns

Avoid these common mistakes that turn quick-change into ungoverned patching:

- **Spec-less fixes:** Changing behavior because “the code obviously should” without a spec section to trace to.
- **SDK creep:** Adding types or public methods during a “small fix” without Phase 3.
- **Contract edits:** Tweaking interface contracts to make tests pass instead of fixing implementation within the contract.
- **Cross-context drive-by:** Fixing a bug in context A by editing files in context B “while you’re there.”
- **Test deletion:** Removing failing tests instead of fixing implementation or escalating spec/test gaps.
- **Skipping verification:** Committing without running existing tests because the change “looks small.”

## Practical Tips

- **Name the spec section** in the PR or session report, not only in the commit message.
- **Prefer the smallest diff** that satisfies the spec and passes tests.
- **Time-box discovery:** If reading spec/SDK/tests takes longer than implementing the fix, the area may be under-documented—consider a gap assessment.
- **Use the quick-change skill** in Cursor: `/quick-change` invokes the harness workflow in `harness/.cursor/skills/quick-change/SKILL.md`.

## Companion Documents

- [PLAYBOOK.md](../harness/PLAYBOOK.md) — Full phase-by-phase execution when quick-change does not apply
- [AGENT_RULES.md](../harness/agent/AGENT_RULES.md) — Agent operating rules and escalation behavior
- [recovery.md](recovery.md) — Gap classification and remediation when quick-change reveals spec or mold debt
- [adoption-profiles.md](adoption-profiles.md) — Essential, Standard, and Complete profile definitions
- [context-persistence.md](context-persistence.md) — When and how to update context state after significant quick-changes
- [iteration.md](iteration.md) — Inner-loop retries when verification fails during quick-change
