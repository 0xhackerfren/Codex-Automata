# Codex Automata

This repository contains the Codex Automata development methodology: a specification-first, SDK-constrained, test-molded approach for the agentic era.

## For AI Agents Reading This File

You are in the Codex Automata methodology repository itself. The methodology harness lives in `harness/`. When working in this repository:

1. **This is a documentation project.** The harness is a collection of templates, rules, reference documents, and configuration files that teams copy into their own projects. There is no application code to build.

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

4. **The ten principles are:**
   1. Specification First
   2. Tests as Molds
   3. Code as Casting
   4. Modularity and Bounded Contexts
   5. Continuous Flow
   6. Quality Gates
   7. SDK as Constraint Surface
   8. Local-First
   9. Research as Foundation
   10. Intentional Divergence

5. **Terminology:** Use the glossary at `reference/glossary.md` for canonical definitions. Key terms: specification, SDK, constraint surface, building block, mold, casting, bounded context, interface contract, iteration, quality gate, quick change, accessibility, action classification, agent task, brownfield, cost budget, generator, guardrail, human review, invariant, flow, recovery, gap assessment, design identity, design token, deployment checklist, divergence gate, slop fingerprint, product test, property-based test, user profile, test objective, token budget, UX budget, multi-agent orchestration, security audit, incident postmortem, retrospective, WCAG.

6. **When editing harness files:** Ensure changes propagate to all files that reference the modified concept. Use the following as cross-reference anchors:
   - Principles: `reference/principles.md`
   - Phases: `harness/PLAYBOOK.md`
   - Rules: `harness/agent/AGENT_RULES.md`
   - Glossary: `reference/glossary.md`
   - Architecture: `reference/architecture.md`
   - Workflow: `reference/workflow.md`

## For Teams Adopting the Methodology

Copy the `harness/` directory into your project root. The harness includes:

- `AGENTS.md` — Tool-agnostic agent instructions (works with Claude Code, Copilot, Codex, Windsurf, etc.)
- `agent/` — Agent operating rules and casting rules
- `templates/` — Specification, test plan, architecture, design identity, and other templates
- `.cursor/` — Cursor-specific rules, skills, subagents, and hooks (optional, Cursor-only)
- `scripts/` — Init scripts for project scaffolding
- `PLAYBOOK.md` — Phase-by-phase execution guide

The `.cursor/` directory is Cursor-specific. Everything else works with any AI coding tool that reads AGENTS.md or can be instructed via project-level configuration.

See `reference/adoption-profiles.md` for Essential, Standard, and Complete profile options.
