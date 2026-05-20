# Guardrails

Agent guardrails and action classification calibrate AI autonomy to risk. Quality gates enforce mechanical correctness; guardrails enforce human judgment about whether an action should proceed at all.

---

## Why Guardrails Exist

AI agents are powerful but not infallible. The methodology defines quality gates for mechanical enforcement (tests, linters, coverage, contract checks, divergence gates), but some actions require human judgment that no automated gate can replace.

Guardrails define which agent actions can proceed autonomously, which should be logged for audit, and which require explicit human approval before execution. Without guardrails, agents either do too much (making irreversible or scope-changing changes without oversight) or too little (asking permission for every file edit).

The action classification system calibrates autonomy to risk:

- Low-risk, read-only, or easily reversible work proceeds without friction.
- Auditable work proceeds but leaves a trail for retroactive review.
- High-stakes, irreversible, or constraint-changing work halts until a human explicitly approves.

Guardrails complement quality gates; they do not replace them. A team can pass every mechanical check and still need human approval before changing the specification or deleting tests.

---

## The Three-Tier Classification

Every agent action maps to one of three tiers:

### AUTO

Safe to proceed without human intervention. Read-only operations and reversible low-risk actions. The agent executes and continues.

**Examples:** Reading specifications, SDK interfaces, test plans, and context state; running tests and linters.

### LOG

Safe to proceed, but the action is recorded for audit. The agent executes, logs the action (typically in context state Session History or project audit logs), and continues. If a pattern of problematic LOG actions emerges, the team can reclassify the action to APPROVE.

**Examples:** Writing code within the SDK boundary, adding tests, updating context state, making atomic commits.

### APPROVE

The agent halts and waits for explicit human approval before proceeding. Reserved for irreversible, high-stakes, or scope-changing actions. The agent must surface what it intends to do, why, and what artifacts are affected; it must not execute until approval is recorded.

**Examples:** Modifying SDK interfaces, changing specifications, deleting tests, deploying to production.

**Default when uncertain:** Treat ambiguous actions as APPROVE. It is safer to ask than to act.

---

## Default Classification for Codex Automata Actions

| Action | Default Tier | Rationale |
|--------|-------------|-----------|
| Reading specifications | AUTO | Read-only |
| Reading SDK interfaces | AUTO | Read-only |
| Reading test plans | AUTO | Read-only |
| Running tests | AUTO | Non-destructive verification |
| Running linters | AUTO | Non-destructive verification |
| Reading context state | AUTO | Read-only |
| Writing code within SDK boundary | LOG | Reversible (git), but should be auditable |
| Adding new tests | LOG | Additive, aligned with spec |
| Updating context state | LOG | Tracking, not production impact |
| Making atomic commits | LOG | Reversible (git revert) |
| Updating existing tests | LOG | May indicate spec drift, worth auditing |
| Modifying SDK interfaces | APPROVE | Changes the constraint surface for all agents |
| Modifying interface contracts | APPROVE | Changes cross-module boundaries |
| Deleting tests | APPROVE | Reduces coverage, may mask regressions |
| Changing specifications | APPROVE | Changes the source of truth |
| Deploying to production | APPROVE | Irreversible user impact |
| Creating new bounded contexts | APPROVE | Architectural decision |
| Adding external dependencies | APPROVE | Supply chain and security implications |
| Modifying quality gate thresholds | APPROVE | Weakens enforcement |
| Disabling linters or checks | APPROVE | Weakens enforcement |
| Bulk file operations (rename/delete multiple files) | APPROVE | Broad impact, hard to review incrementally |

Teams may override defaults using the guardrail configuration template (`harness/templates/guardrail-config-template.md`).

---

## Relationship to Quality Gates

**Quality gates** are mechanical: they run automatically in CI/CD or local tooling and produce pass/fail results. They answer: *Did the change meet defined technical criteria?*

**Guardrails** are about human judgment: they decide whether an action should happen at all. They answer: *Should this agent be allowed to perform this class of action without oversight?*

| Dimension | Quality gates | Guardrails |
|-----------|---------------|------------|
| Enforcement | Automated scripts, CI jobs, hooks | Agent behavior + human approval workflow |
| Question asked | Does it pass tests, lint, coverage, contracts? | Is this action category permitted autonomously? |
| Failure mode | Block merge or fail build | Halt agent and request approval |
| Override | Waiver with documented risk acceptance | Emergency override protocol (tracked) |

An action can pass all quality gates and still require APPROVE if it changes scope, constraints, or enforcement. For example, deleting a failing test might leave CI green while violating methodology; guardrails block that path.

Conversely, a simple LOG action might fail a quality gate (test failure, linter error), triggering the **iteration protocol** (`reference/iteration.md`) rather than a guardrail escalation. The agent may retry within bounded inner-loop attempts; it does not need new approval for each fix attempt if the action remains within the same LOG category and scope.

---

## Per-Profile Configuration

Adoption profiles (`reference/adoption-profiles.md`) adjust guardrail strictness alongside phases, templates, and quality gates.

### Essential

Lighter guardrails for small teams and low-risk projects. Only **APPROVE** for:

- Modifying specifications
- Deleting tests
- Deploying to production (or equivalent release)

Everything else is **AUTO** or **LOG**. Agents move faster; humans focus approval on source-of-truth and release impact.

### Standard

Uses the default classification table in this document. Balances autonomy and oversight for typical product development.

### Complete

Stricter guardrails for regulated, high-exposure, or brand-critical work. **Additional APPROVE** actions beyond the default table:

- Any change to user-facing code without design identity review (when design identity applies)
- Any product test budget change (UX budgets, journey scope)
- Any security-related code change (auth, crypto, PII handling, dependency with security implications)

Complete profile teams should document these additions in their guardrail configuration file.

---

## Emergency Override Protocol

Overrides are not forbidden. They are tracked so the team can assess whether guardrail classification needs updating.

When a human decides to override a guardrail (approve an action that would normally be blocked, or skip an approval gate), they must:

1. **Document the override reason** in the context state file (`context-state.md`, from `templates/context-state-template.md`).
2. **Log the override** as a tracking item in the project's guardrail configuration override log (see `templates/guardrail-config-template.md`). The entry may need retroactive review.
3. **Schedule a follow-up review** within the current planning cycle to confirm the override was appropriate and whether the default tier should change.

Agents must not self-authorize overrides. Only humans may record an override and explicitly instruct the agent to proceed.

---

## Customization

Teams override default classification using the guardrail config template. Copy `harness/templates/guardrail-config-template.md` into the project (commonly `docs/guardrail-config.md` or alongside other governance docs) and fill in:

- Adoption profile alignment
- Per-action tier overrides with rationale
- Project-specific APPROVE actions not in the default table
- Reduced tiers (moving APPROVE → LOG) with documented justification
- Override log for retroactive review

Unlisted actions inherit methodology defaults from this document. When project tier and default tier differ, the **project tier** wins.

Reclassify tiers based on evidence: repeated problematic LOG actions → APPROVE; stable low-risk APPROVE actions with strong automation → LOG (document justification).

---

## Logging LOG Actions

For **LOG** tier actions, record enough context for audit without blocking flow:

- **What** changed (files, modules, bounded context)
- **Why** (specification section, agent task ID, quick-change reference)
- **When** (session timestamp in context state Session History)
- **Outcome** (tests passed/failed, commit hash if applicable)

Context state is the primary audit trail for agent sessions. Teams with compliance requirements may mirror LOG entries to external systems; the methodology does not mandate a specific logging backend.

---

## Agent Behavior Summary

| Tier | Agent behavior |
|------|----------------|
| AUTO | Execute immediately; no approval prompt |
| LOG | Execute; append audit entry; continue |
| APPROVE | Stop; describe intended action and impact; wait for explicit human approval |

If classification is unclear, default to **APPROVE**. See `harness/agent/AGENT_RULES.md` section 6 and `harness/PLAYBOOK.md` for phase-specific guidance.

---

## Companion Documents

| Document | Role |
|----------|------|
| `harness/agent/AGENT_RULES.md` | Operating rules; section 6 summarizes guardrail tiers for agents |
| `harness/templates/guardrail-config-template.md` | Project-specific classification overrides and override log |
| `harness/PLAYBOOK.md` | Phase-specific AUTO / LOG / APPROVE guidance across the pipeline |
| `harness/.cursor/rules/codex-automata.mdc` | Cursor constraint enforcing tier respect |
| `reference/adoption-profiles.md` | Essential / Standard / Complete profile guardrail differences |
| `reference/iteration.md` | Inner/outer loops when quality gates fail (distinct from APPROVE halts) |
| `reference/quick-change.md` | Abbreviated workflow; APPROVE still applies to spec/SDK/test deletion |
| `reference/principles.md` | Principle 6 (Quality Gates) and Principle 10 (Intentional Divergence) relate to mechanical vs human judgment |
| `reference/glossary.md` | Canonical terminology |
| `templates/context-state-template.md` | Session History and override documentation |
