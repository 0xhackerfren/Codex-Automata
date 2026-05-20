# Recovery Protocol

This document defines how Codex Automata projects handle the discovery of gaps in specifications, SDK, tests, or coverage after code already exists. Recovery is not an exception to the methodology; it is the methodology applied retroactively. The same pipeline that governs forward work governs remediation: specification first, then SDK, then molds, then casting.

For systematic adoption of the methodology on an existing codebase (brownfield onboarding), see `reference/brownfield-onboarding.md`. Brownfield onboarding applies the recovery protocol at scale: every existing module goes through recovery to establish specifications, SDK types, and tests retroactively.

For phase-by-phase forward workflow, see `PLAYBOOK.md` in the harness. For the gap assessment template used during recovery, see `templates/gap-assessment-template.md` in the harness.

## Why Recovery Needs a Protocol

The forward pipeline assumes disciplined execution: every module gets a spec, every spec gets tests, every test precedes code. In practice, gaps accumulate. Production incidents expose unspecified failure modes. Code reviews reveal missing edge-case tests. A new team member walks through a module and finds no contract tests at all. A dependency upgrade invalidates assumptions that were never documented. A security scan surfaces behaviors that exist in code but nowhere in the specification.

Without a structured recovery process, teams respond to these discoveries in one of two ways. They either ignore the gap and accept silent debt, or they slap a test onto the existing code and call it covered. Both responses violate the methodology. The first erodes the mold. The second builds a mold around a casting instead of a specification, encoding whatever the code happens to do rather than what it should do.

Recovery requires the same rigor as forward work because the risks are identical. A gap in the mold is a gap in the mold whether it was missed on the first pass or discovered six months later.

## Discovery Triggers

Gaps surface through predictable channels. Teams should treat these as detection mechanisms, not surprises.

**Production incidents.** An outage, data corruption event, or SLO breach reveals behavior that was never specified or tested. The incident postmortem traces the failure to a missing specification clause or an absent test.

**Review findings.** A human reviewer identifies behaviors in the casting that have no corresponding specification section or test coverage. The review template's "Gaps" field captures these explicitly.

**Coverage audits.** Periodic or automated measurement of test coverage (statement, branch, behavioral) reveals modules below project thresholds or with no coverage at all.

**Team walkthroughs.** A new team member, a rotating reviewer, or a cross-team dependency audit exposes modules where institutional knowledge substitutes for written specification.

**Dependency upgrades.** Updating a library, framework, or platform surfaces assumptions that were encoded in code but never documented in a specification. The upgrade breaks behavior that no test guards.

**Security scans.** Static analysis, penetration testing, or threat modeling identifies attack surfaces that exist in code but have no corresponding failure-mode specification or adversarial test.

**Agent-detected gaps.** During routine tasks, agents encounter code without a corresponding specification or tests. Per agent operating rules, they halt and report rather than working around the gap.

**Security audits.** Dedicated security reviews, whether performed by human auditors, automated scanning tools, or security audit agents, identify vulnerabilities and security gaps that should be routed through the recovery pipeline. Use the security audit template (`templates/security-audit-template.md`) to document findings.

## Gap Classification

Every discovered gap falls into one of five categories. Classification determines the recovery sequence.

### Spec Gap

Behavior exists in the codebase but is not documented in any specification. The code does something, but no one wrote down what it should do or why. This is the most dangerous class because without a spec, you cannot determine whether the current behavior is correct or accidental.

**Recovery sequence:** Write the specification first (determine intended behavior), then derive tests, then verify or recast the implementation.

### Mold Gap

Behavior is documented in the specification but has no tests, or tests exist but are too weak to constrain the implementation meaningfully. The spec says what should happen, but no mold enforces it.

**Recovery sequence:** Derive tests from the existing specification, verify they fail against known-bad inputs (or pass against the current implementation if it is believed correct), then review for alignment.

### Coverage Erosion

Tests once existed but were deleted, disabled, marked as skipped, or allowed to become flaky without remediation. The mold has degraded over time.

**Recovery sequence:** Audit the erosion (version control history reveals when and why tests were removed or disabled), restore or rewrite the affected tests, and verify they align with the current specification.

### Contract Gap

A module boundary defined in the architecture has no contract tests. The interface contract document may exist, but nothing mechanically verifies that both sides honor it.

**Recovery sequence:** Write contract tests from the interface contract document, run them against both sides of the boundary, and remediate any failures.

### SDK Gap

Behavior exists in the codebase but has no corresponding types or interfaces in the SDK constraint surface. The implementation bypassed the constraint surface, meaning architectural decisions are not mechanically enforced for this code.

**Recovery sequence:** Write the missing SDK types and interfaces from the specification (not from the code), then derive or update tests against the new SDK surface, then verify or recast the implementation to use the SDK types.

## Triage

Not all gaps carry equal risk. Triage determines the order in which recovery work enters the kanban board.

### Severity Levels

**Critical.** The gap is in a production-facing code path and has already caused or could plausibly cause an incident. Recovery enters the board immediately, ahead of forward work if WIP limits require a choice.

**Significant.** The gap is in a production-facing code path but has not yet caused an incident. The behavior is exercised regularly. Recovery is scheduled within the current planning cycle.

**Moderate.** The gap is in internal tooling, rarely exercised paths, or code with partial coverage. Recovery is scheduled but does not preempt forward work.

**Low.** The gap is theoretical (the unspecified behavior is unlikely to be exercised) or the module is scheduled for replacement. Recovery is documented and tracked but may be deferred.

### Triage Decisions

Triage is a human responsibility. Agents surface gaps and provide evidence; humans decide priority. The triage decision is recorded in the gap assessment document so future reviewers understand why a gap was or was not addressed immediately.

When multiple gaps are discovered simultaneously (common after an incident or a comprehensive audit), triage them as a batch. Group related gaps by module or bounded context to enable efficient recovery rather than scattering effort across the system.

## The Recovery Sequence

Recovery follows the forward pipeline but starts from an existing codebase. The sequence is:

```text
Audit --> Spec Patch --> SDK Patch --> Mold Patch --> Recast (if needed) --> Re-review
```

### Step 1: Audit

Document the gap using the gap assessment template (`templates/gap-assessment-template.md`). Identify:

- Which module is affected.
- What class of gap it is (spec, SDK, mold, coverage erosion, contract).
- How it was discovered.
- What currently exists (partial spec? weak tests? nothing?).
- What should exist according to the methodology.

The audit is a human task. Agents assist by scanning for related gaps in adjacent modules, checking version control history for when coverage was lost, and surfacing specification sections that reference the affected behavior.

### Step 2: Spec Patch

If the specification is missing or incomplete, write the missing sections. This follows the same rules as Phase 2 (Specification Writing) in the forward pipeline. The specification describes intended behavior, edge cases, and failure modes.

If the specification exists and is correct, skip to Step 2b.

If the specification exists but is wrong (the code does something different, and the code is correct), update the specification to match intended behavior and document the rationale for the change.

The critical constraint: do not derive the specification from the code. Derive the specification from domain knowledge, stakeholder intent, and architectural requirements. The code may be accidentally correct, or it may be wrong. The specification must reflect what the system should do, not what it happens to do.

### Step 2b: SDK Patch

If the SDK constraint surface is missing types or interfaces for the specified behavior, extend the SDK following the same rules as Phase 3 (SDK Design) in the forward pipeline. The SDK extension derives from the specification, not from the existing code.

If the SDK already covers the behavior, skip to Step 3.

If the SDK exists but the implementation bypasses it (uses ad hoc types instead of SDK types), note this for Step 4 (Recast).

### Step 3: Mold Patch

Derive tests from the patched specification. This follows the same rules as Phase 4 (Test Molding) in the forward pipeline. Tests must trace back to specification sections. Tests must be sharp enough to constrain implementation.

For mold gaps, verify that new tests fail against known-bad inputs before relying on them.

For coverage erosion, compare restored tests against the original test intent (version control history) and the current specification. The specification is authoritative; if the original tests were wrong, write new ones rather than restoring incorrect tests.

### Step 4: Recast (If Needed)

If the existing implementation passes the new tests, recasting is unnecessary. The code was correct; it was just unverified.

If the existing implementation fails the new tests, recast the affected code. This follows Phase 5 (Code Casting) rules. Agents receive the specification, the updated test suite, and the interface contracts. They modify the implementation until all tests pass.

Do not patch the implementation to pass tests without reading the specification. The specification, not the test, is the source of truth. The test encodes the specification mechanically; the implementation satisfies both.

### Step 5: Re-review

A human reviews the recovery work as a unit: the spec patch, the mold patch, and any recast code. The review verifies:

- The specification accurately reflects intended behavior.
- Tests trace to specification sections.
- The implementation passes all tests.
- No new gaps were introduced by the recovery work.
- The gap assessment document is complete, including the recurrence prevention section.

## Kanban Integration

Recovery tasks are first-class work items on the kanban board. They are not invisible background chores, side projects, or "tech debt we will get to later."

### Card Type

Use a distinct card type or tag (e.g., "Recovery" or "Gap Remediation") so recovery work is visible and measurable separately from forward work. This enables tracking of recovery volume as a system health metric.

### Station Flow

Recovery cards flow through the same stations as forward work:

| Station | Recovery Activity |
|---------|-------------------|
| Spec Writing | Write or patch the missing specification sections |
| SDK Design | Extend the SDK constraint surface from the specification |
| Test Molding | Derive or restore tests from the specification |
| Code Casting | Recast if the implementation fails new tests |
| Human Review | Review the complete recovery unit |

### WIP Limits

Recovery cards count against the same WIP limits as forward cards. If a critical gap displaces forward work, that displacement is visible on the board and subject to the same flow management. Recovery is not free; treating it as invisible is how gaps accumulate in the first place.

### Batch Sizing

When an audit discovers many gaps in a single module, batch them into a single recovery card scoped to that module rather than creating dozens of micro-cards. The recovery unit is the module, not the individual test.

When gaps span multiple modules, create one recovery card per module to maintain bounded context independence.

## Recurrence Prevention

Every completed recovery includes a brief retrospective answering one question: what process gap allowed this debt to accumulate?

Common answers and their remediation:

**The review checklist did not require coverage verification.** Add the check to the human review template and the PR template.

**Contract tests were not required at the boundary.** Update the architecture document and the module boundary template to mandate contract tests.

**The spec was reviewed by someone unfamiliar with the domain.** Establish domain-owner review requirements for specifications in that bounded context.

**Tests were disabled to unblock a deadline and never re-enabled.** Add a policy that disabled tests require a tracking issue with a due date and an owner.

**The module predates the methodology and was never retroactively specified.** Schedule a systematic audit of pre-methodology modules and prioritize them by production exposure.

**Agent-generated code bypassed the forward pipeline due to an emergency.** Review the emergency bypass policy and ensure it includes mandatory recovery scheduling.

The recurrence prevention section of the gap assessment is not optional. It is the mechanism by which recovery improves the system rather than simply patching the current gap.

## Metrics

Track recovery as a system health indicator, not a shame metric.

**Gap discovery rate.** How many gaps are discovered per period? A rising rate after adopting the methodology may indicate improving detection rather than worsening quality. A sustained high rate after the system matures signals a process failure.

**Recovery cycle time.** How long from gap discovery to closed recovery card? Long cycle times indicate that recovery work is being deprioritized or blocked.

**Gap class distribution.** Which classes of gap (spec, SDK, mold, erosion, contract) appear most frequently? Persistent patterns in one class indicate a systemic weakness in the corresponding pipeline phase.

**Recurrence rate.** Are the same classes of gap reappearing after recovery? If so, the recurrence prevention measures are not working.

**Recovery-to-forward ratio.** What fraction of board capacity is consumed by recovery work? A high ratio sustained over time indicates that the forward pipeline is producing gaps faster than the team can close them. This is an architectural or process problem, not a staffing problem.

## Companion Documents

- `workflow.md` in this directory for end-to-end pipeline context and feedback loops.
- `kanban.md` in this directory for WIP limits, pull policies, and flow metrics.
- `agent-operating-model.md` in this directory for agent behavior during recovery tasks.
- `principles.md` in this directory for the foundational principles recovery enforces.
- `PLAYBOOK.md` in the harness for phase-by-phase execution guidance including the recovery procedure.
- `templates/gap-assessment-template.md` in the harness for the structured gap documentation template.
- `brownfield-onboarding.md` in this directory for systematic adoption on existing codebases.
- `templates/brownfield-audit-template.md` in the harness for codebase inventory and prioritization.
