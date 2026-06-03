# Brownfield Onboarding Protocol

This document defines how teams adopt Codex Automata on an existing codebase that predates the methodology. Brownfield onboarding is not a shortcut around the pipeline; it is the pipeline applied in reverse, then forward again. You start from code, work backward to specifications and SDK types, derive tests, verify or recast the implementation, and expand outward module by module until the system is wrapped in the same artifacts the forward pipeline would have produced from day one.

For the recovery sequence applied to a single module, see [recovery.md](recovery.md). For adoption profile tiers, see [adoption-profiles.md](adoption-profiles.md). For phase-by-phase forward workflow after onboarding begins, see [PLAYBOOK.md](../harness/PLAYBOOK.md) in the harness.

## Why Brownfield Adoption Is Different

The forward pipeline assumes a greenfield start: intake, architecture, specification, SDK, tests, then code. Every artifact exists before the next phase begins. Existing codebases violate this assumption in predictable ways.

**Implicit contracts.** Modules communicate through conventions that were never written down. Function signatures, error shapes, and side effects are tribal knowledge. New contributors read the code to learn what the system does, which encodes accidents as truth.

**Undocumented invariants.** Assumptions about ordering, idempotency, concurrency, and data shape live only in comments, test names, or the heads of original authors. When those authors leave, the invariants leave with them.

**Code without specifications.** Production behavior exists with partial READMEs, outdated API docs, or no documentation at all. Tests may exist but were often written against the implementation (characterization tests), not against intended behavior.

**The forward pipeline does not fit day one.** You cannot run Phase 0 through Phase 5 on a system that already shipped. Attempting to "start over" with a full greenfield pass is a rewrite disguised as adoption. Teams burn out, stakeholders lose confidence, and the methodology gets blamed for the disruption.

Brownfield adoption reverses the order for each module, then rejoins the forward pipeline:

```text
Inventory --> Classify --> Select module --> Recovery (spec <-- domain, SDK <-- spec, tests <-- spec) --> Verify/Recast --> Expand --> Incremental gates
```

Recovery is not a separate track for brownfield work. **Recovery is onboarding.** Every existing module that lacks specifications, SDK coverage, or sharp tests goes through the recovery protocol until it meets the active adoption profile. The difference from ad hoc recovery is scale and planning: you inventory first, prioritize by risk and change frequency, and expand in dependency order rather than reacting to gaps one at a time.

## The Onboarding Sequence

### 1. Install the Harness

Copy the methodology harness into the existing project root using `scripts/init.ps1` (Windows) or `scripts/init.sh` (Unix). The init script places templates, agent rules, and optional Cursor configuration without replacing application source.

Declare the starting adoption profile in the intake document (usually **Essential** for the first module). Do not activate every template and gate on day one; the profile controls ceremony.

### 2. Inventory Existing Modules

Run a brownfield audit using `templates/brownfield-audit-template.md` in the harness. List every significant module, service, or bounded context. For each entry, record:

- Bounded context affiliation
- Risk level (Critical / High / Medium / Low)
- Change frequency (Daily / Weekly / Monthly / Rare)
- Test coverage (percentage, None, or Unknown)
- Whether a specification and SDK already exist

The audit is a human-led activity with agent assistance for scanning directories, mapping imports, and surfacing test files. Agents do not guess risk levels; humans classify based on production exposure, incident history, and business value.

### 3. Classify Modules

Apply consistent criteria so prioritization is defensible, not political.

**Risk level:**

- **Critical:** Production-facing, revenue-impacting, handles sensitive data, or has caused incidents.
- **High:** Production-facing, frequently changed, or complex business logic.
- **Medium:** Internal tooling, moderately changed, or straightforward logic.
- **Low:** Rarely changed, well-understood, or scheduled for replacement.

**Change frequency:** How often the module's code changes in practice (Daily through Rare), not how often stakeholders wish it would change.

**Priority:** Risk and change frequency combine. Critical modules that change daily onboard first. Low-risk modules that change rarely onboard last—or not at all if replacement is imminent.

### 4. Select the First Module

Choose the highest-priority module from the inventory. The first module should be where pain concentrates: production exposure plus frequent change. Onboarding a stable, low-risk utility first wastes effort and fails to demonstrate value.

Check the dependency map. When practical, onboard dependencies before dependents so interface contracts and SDK types stabilize before downstream modules consume them.

### 5. Apply Recovery to the First Module

Execute the recovery protocol for the selected module:

1. **Spec patch:** Write the specification from domain knowledge, stakeholder intent, and architectural requirements—not from the current code.
2. **SDK patch:** Extract types and interfaces from the specification (Essential may colocate types; Standard requires a dedicated SDK surface).
3. **Mold patch:** Derive tests from the specification against SDK interfaces.
4. **Verify:** Run tests against the existing implementation. Passing tests mean the casting was accidentally correct; failing tests trigger gap assessments.
5. **Recast (if needed):** Fix implementation to satisfy specification and tests.
6. **Re-review:** Human review of the recovery unit as a whole.

File gap assessments (`templates/gap-assessment-template.md`) for every discovered mismatch. Undocumented features in code (for example, an "archive" endpoint with no spec) are spec gaps until a human decides intended behavior.

### 6. Expand Outward

Repeat recovery for adjacent modules in priority order. As boundaries between onboarded modules stabilize:

- Define interface contracts between them (Standard profile).
- Add contract tests at boundaries.
- Update context state and block registry so agents know which modules are methodology-complete.

Follow dependency order where cycles exist, extract shared types into the SDK early, and avoid two agents recasting the same boundary without a frozen contract.

### 7. Establish Quality Gates Incrementally

Do not require full methodology coverage on day one. Gates tighten as modules complete onboarding:

- **Immediately:** New code and new modules require specifications and tests before merge (scope: new PRs only).
- **After first module:** Tests must trace to spec sections for touched onboarded modules.
- **After Standard upgrade:** SDK interfaces required at public boundaries; contract tests for cross-module calls.
- **After Complete upgrade:** Product testing, design identity, divergence gates as applicable.

Old code outside onboarded modules is not blocked by gates it has not yet earned. It is scheduled through the recovery pipeline on its own timeline.

## Progressive Adoption Strategy

Profiles scale ceremony with coverage. Brownfield projects almost always start Essential and upgrade when criteria are met, not on a calendar alone.

### Essential (First Module)

**Active artifacts:** Specification, test plan, implementation verification. Types may live alongside code without a separate SDK package.

**Brownfield use:** Apply to a single high-risk module. Prove the loop: domain spec, derived tests, verify or recast. No architecture decomposition ceremony unless the module itself spans contexts.

**Upgrade trigger:** Project grows beyond one bounded context, a second high-priority module is ready, or multiple contributors need shared interfaces.

### Standard (Three or More Modules Onboarded)

**Added artifacts:** SDK constraint surface, interface contracts, architecture notes, context persistence, block registry, full recovery protocol for remaining gaps.

**Brownfield use:** Upgrade when three or more modules are onboarded and boundaries between them need frozen interfaces. Run recovery for SDK gaps on modules that were Essential-only.

**Upgrade trigger:** User-facing product quality matters, compliance demands full traceability, or product testing would catch defects code tests miss.

### Complete (Full System Onboarded)

**Added artifacts:** Product testing, design identity, divergence gates, all templates, maximum quality gates.

**Brownfield use:** Upgrade when critical paths are onboarded and remaining work is expansion plus polish, not foundational spec debt on revenue paths.

Downgrading profiles after brownfield work has begun is discouraged; orphaned SDK and contract artifacts create confusion.

## Integration with Existing CI/CD

Pipeline as First Citizen (Principle 12) applies to brownfield adoption incrementally. Brownfield adoption succeeds when it augments existing pipelines rather than replacing them on day one.

**Honor existing tests.** If tests assert behavior that matches the new specification, keep them. Add spec-traced tests where coverage is thin. If tests only characterize current code (asserting implementation details without domain intent), flag them for review during mold patch; they may encode bugs as expected behavior.

**Gate new work first.** Require specifications and tests for new modules and new features immediately. Do not retroactively fail builds on legacy directories that have not been scheduled for recovery.

**Retroactive gates follow onboarding.** When a module completes recovery, extend CI rules to that module's paths: spec file exists, test plan exists, coverage thresholds if the team uses them.

**Integrate, do not duplicate.** Linters, type checkers, security scanners, and deployment pipelines that already run should remain. Codex Automata gates add spec presence, test traceability, and optional divergence or contract checks—not a second unrelated CI system.

**Example gate progression:**

| Gate | When to activate | Scope |
|------|------------------|-------|
| Spec required for new files/modules | Immediately | New PRs only |
| Tests required for new behavior | Immediately | New PRs only |
| Spec + test plan for onboarded paths | After each module recovery | Paths listed in audit |
| SDK / contract tests | After Standard upgrade | Onboarded module boundaries |
| Product test objectives | After Complete upgrade | Release candidates |

## Anti-Patterns

| Anti-pattern | Why it fails | What to do instead |
|--------------|--------------|-------------------|
| Spec everything at once | Analysis paralysis, team burnout, no production value for weeks | One module at a time; highest priority first |
| Derive specs from code | Encodes bugs and accidents as requirements | Spec from domain knowledge; use code only to discover gaps |
| Treat adoption as a rewrite | Stakeholders fear regression; methodology blamed | Wrap existing code; verify with new tests; recast minimally |
| Skip the inventory | Unknown scope, wrong priorities, duplicate effort | Complete brownfield audit before first recovery |
| Onboard low-risk, stable modules first | No pain relief; skeptics question ROI | Start where risk × change frequency is highest |
| Disable legacy tests to pass new molds | Coverage erosion | Align tests to spec; restore or replace with spec-traced cases |
| Full Complete profile on day one | Ceremony exceeds value; gates block all PRs | Essential first; upgrade on criteria |

## Timeline Expectations

Timelines assume part-time methodology work alongside feature delivery, not a dedicated migration team.

| Context | Codebase scale | Target | Typical duration |
|---------|----------------|--------|------------------|
| Solo developer | 5–10 modules | Essential on critical paths | 2–4 weeks |
| Small team (2–5) | 20–50 modules | Standard on high-risk modules | 1–2 months |
| Large team | 100+ modules | Standard on critical paths | 3–6 months |
| Any | 100+ modules | Complete full coverage | Ongoing; months to years |

Critical path onboarding (revenue, security, incident-prone modules) should complete before low-priority utilities. Modules scheduled for deletion may never be onboarded; record that decision in the audit.

## Relationship to Recovery and Forward Work

After a module completes brownfield onboarding, it behaves like a greenfield module in the forward pipeline. New features in that module follow intake → spec → SDK → tests → code (or quick-change when criteria are met). Gaps discovered later use recovery the same way whether the module was onboarded yesterday or built greenfield last sprint.

Brownfield onboarding volume should appear on the kanban board as recovery cards grouped by module, visible alongside forward work. A sustained high ratio of recovery to forward work after initial onboarding may indicate the forward pipeline is still producing gaps—address process, not just backlog.

## Metrics

Track onboarding health without treating legacy debt as shame.

**Modules onboarded / total inventoried.** Progress indicator; expect slow growth on large codebases.

**Time to Essential per critical module.** Should decrease as teams repeat the recovery sequence.

**Gap class distribution from audits.** Persistent spec gaps suggest weak domain review; mold gaps suggest skipped test derivation after spec.

**Gate scope expansion.** Document which paths are under new PR gates versus full recovery gates.

**Recovery cycle time for onboarded modules.** Long cycles mean recovery is deprioritized after the initial push.

## Companion Documents

- [recovery.md](recovery.md) — Per-module recovery sequence (the onboarding mechanism)
- [adoption-profiles.md](adoption-profiles.md) — Essential, Standard, and Complete tiers for brownfield upgrades
- [PLAYBOOK.md](../harness/PLAYBOOK.md) — Forward pipeline phases after modules are onboarded
- [gap-assessment-template.md](../harness/templates/gap-assessment-template.md) — Structured gap documentation during recovery
- [brownfield-audit-template.md](../harness/templates/brownfield-audit-template.md) — Codebase inventory and prioritization template
- [context-persistence.md](context-persistence.md) — Tracking onboarding progress across sessions
- [architecture.md](architecture.md) — Bounded contexts and decomposition for Standard+ brownfield
- [quick-change.md](quick-change.md) — Abbreviated workflow for onboarded modules with full artifacts
- [examples/brownfield-api/](../examples/brownfield-api/) — Worked brownfield adoption example (bookmarks API)
