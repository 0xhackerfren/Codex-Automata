# Codex Automata

This repository contains the Codex Automata development methodology: a specification-first, SDK-constrained, test-molded approach for the agentic era.

## For AI Agents Reading This File

You are in the Codex Automata methodology repository itself. The methodology harness lives in `harness/`. When working in this repository:

1. **This is a documentation project.** The harness is a collection of templates, rules, reference documents, and configuration files that teams copy into their own projects. The Python CLI in `cli/` and initialization/enforcement scripts are executable tooling; changes require meaningful regression checks.

2. **Consistency is critical.** Cross-references between files must be accurate. Phase numbers, rule numbers, principle counts, glossary terms, and terminology must be consistent across all documents.

3. **The canonical pipeline phases are:**
   - Phase 0: Intake
   - Phase 1: Architecture and Decomposition
   - Phase 2: Specification Writing
   - Phase 3: SDK Design
   - Phase 4: Test Molding
   - Phase 5: Code Casting
   - Phase 6: Review
   - Phase 6b: Product Testing
   - Phase 7: Deployment and Observation

4. **The twelve principles are:**
   1. Specification First
   2. SDK as Constraint Surface
   3. Local-First
   4. Research as Foundation
   5. Tests as Molds
   6. Code as Casting
   7. Modularity and Bounded Contexts
   8. Continuous Flow
   9. Quality Gates
   10. Intentional Divergence
   11. Assembly Pressure
   12. Pipeline as First Citizen

5. **Terminology:** Use the glossary at `reference/glossary.md` for canonical definitions. Key terms: specification, SDK, constraint surface, building block, mold, casting, bounded context, interface contract, iteration, quality gate, quick change, accessibility, action classification, agent task, assembly pressure, pipeline as first citizen, branch strategy, pipeline configuration, brownfield, cost budget, generator, guardrail, human review, invariant, flow, recovery, gap assessment, design identity, design token, deployment checklist, divergence gate, slop fingerprint, product test, property-based test, user profile, test objective, token budget, UX budget, multi-agent orchestration, security audit, incident postmortem, retrospective, WCAG.

6. **When editing harness files:** Ensure changes propagate to all files that reference the modified concept. Use the following as cross-reference anchors:
   - Principles: `reference/principles.md`
   - Phases: `harness/PLAYBOOK.md`
   - Rules: `harness/agent/AGENT_RULES.md`
   - Glossary: `reference/glossary.md`
   - Architecture: `reference/architecture.md`
   - Workflow: `reference/workflow.md`

## For Teams Adopting the Methodology

Use the CLI isolated installation by default. Managed rules, templates and schemas
live under `.automata/`; application code, tests, SDK, documentation and runtime
state remain consumer-owned at configured paths. Existing agent instructions are
preserved. Root and IDE integration use minimal context-routing adapters.

DEVELOP applies engineering gates. OPERATE uses application instructions/tools.
MAINTAIN_METHODOLOGY requires separate explicit authority. Installation alone
never activates development. See `docs/development/isolation.md` and
`SWARM_INTEGRATION_HANDOFF.md`. Legacy root-copy adoption requires explicit
`--layout legacy` and an ownership-reviewed migration.

## Linear-first delivery

Use `harness/agent/LINEAR_FIRST.md` for delivery cadence. Root instructions govern
this methodology repository; harness instructions are the portable consumer copy.
Template maintenance is authorized when changing the methodology itself.
GitHub remains the version-control, review, CI and release system. Linear holds
work specifications and links pinned Git contracts. See
`docs/development/linear-first-change-spec.md` for this change contract.
