# Changelog

All notable changes to this project are documented here.

Format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to semantic versioning concepts where versioning applies to the methodology harness and documented releases.

Types of changes: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**.

## [Unreleased]

### Added

- **Enforcement tooling (closes critical methodology gaps):**
  - Divergence gate scripts (`harness/scripts/divergence-gate.sh`, `.ps1`): scan source files for slop fingerprints (banned fonts, hardcoded colors, generic copy, structural anti-patterns). Configurable via JSON catalog or default fingerprint set. CI-ready with non-zero exit on violations.
  - Divergence config example (`harness/scripts/divergence-config-example.json`): reference configuration for project-specific fingerprint catalogs derived from the design identity document.
  - Spec-check scripts (`harness/scripts/spec-check.sh`, `.ps1`): verify every source module has a corresponding specification document. Enforces R1 (spec before code) mechanically.
  - Commit-lint scripts (`harness/scripts/commit-lint.sh`, `.ps1`): validate commit messages for specification traceability (recognized prefixes, spec section references, task references). Enforces R7 mechanically. Usable as git commit-msg hook or CI check.
- **New Cursor skills (5):** `/sdk-design` (Phase 3), `/architecture` (Phase 1), `/review` (Phase 6), `/product-testing` (Phase 6b), `/recovery` (gap remediation). Skill coverage now spans all pipeline phases (9 skills total, up from 4).
- **SDK Design Rules** (`harness/agent/SDK_DESIGN_RULES.md`): phase-specific rules for agents translating specifications into the SDK constraint surface. Covers building block design, design token creation, extension points, and traceability.
- **Command-type Cursor hooks:**
  - `harness/.cursor/hooks/check-hardcoded-values.sh`: afterFileEdit hook that warns when edited files contain hardcoded visual values that should use design tokens.
  - `harness/.cursor/hooks/contract-guard.sh`: preToolUse hook that requires human approval before modifying SDK or interface contract files (enforces R3).
- **CI quality gate workflow** (`harness/.github/workflows/codex-gates.yml`): GitHub Actions workflow running spec-check, divergence gate, commit lint, and test suite detection for adopter projects.
- Init scripts now copy `harness/scripts/` into target projects for enforcement tooling out of the box.
- Profile field added to `harness/templates/project-intake-template.md` (previously referenced in adoption-profiles.md but missing from the template).
- Brownfield onboarding protocol (`reference/brownfield-onboarding.md`): structured approach for adopting the methodology on existing codebases. Progressive adoption starting with recovery on highest-risk modules.
- Brownfield audit template (`harness/templates/brownfield-audit-template.md`): module inventory, dependency mapping, gap summary, and phased onboarding plan.
- `/brownfield-onboarding` Cursor skill for guided brownfield adoption workflow.
- Brownfield worked example (`examples/brownfield-api/`): Express.js bookmarks API showing audit, retroactive specification, SDK extraction, test derivation, and gap assessment for undocumented features.
- Agent guardrails and action classification (`reference/guardrails.md`): three-tier system (AUTO/LOG/APPROVE) defining which agent actions can proceed autonomously, which are logged, and which require human approval.
- Guardrail config template (`harness/templates/guardrail-config-template.md`): project-level action classification overrides.
- Property-based testing as advanced molds (`reference/property-based-testing.md`): extends Tests as Molds with specification-derived invariants verified against random inputs using PBT frameworks (fast-check, Hypothesis, proptest).
- Cost-conscious development guide (`reference/cost-awareness.md`): token budget estimation by phase, model tiering, cost optimization patterns, and monitoring recommendations.
- Accessibility as first-class concern (`reference/accessibility.md`): WCAG as specification constraint, accessibility in design identity, accessibility molds, product testing with accessibility profiles.
- Guardrails section added to `harness/agent/AGENT_RULES.md` (section 6).
- Accessibility commitments section added to `harness/templates/design-identity-template.md`.
- Property-based tests section added to `harness/templates/test-plan-template.md`.
- Accessibility tests section added to `harness/templates/test-plan-template.md`.
- Accessibility-constrained example profile added to `harness/templates/user-profile-template.md`.
- PBT rules added to `harness/agent/TEST_MOLDING_RULES.md`.
- PBT step added to `/test-molding` skill workflow.
- Accessibility rule added to `harness/.cursor/rules/code-casting.mdc`.
- Guardrail constraint added to `harness/.cursor/rules/codex-automata.mdc`.
- Cost-conscious principle added to `harness/agent/AGENT_RULES.md` Core Principles.
- Guardrails section and Brownfield Adoption section added to `harness/PLAYBOOK.md`.

### Added (prior unreleased work)

- Four new Cursor skills: `/sdk-design` (Phase 3 SDK constraint surface design), `/review` (Phase 6 human review assistance), `/product-testing` (Phase 6b agentic product verification), `/recovery` (gap remediation workflow).
- Three new Cursor subagents: `sdk-designer` (translates specs into SDK types and interfaces), `product-tester` (operates application as simulated user against UX budgets), `security-auditor` (read-only security vulnerability analysis).
- Quick-change workflow (`reference/quick-change.md`, `/quick-change` skill): abbreviated path for bug fixes and small changes within existing spec/SDK/test coverage. Available at all adoption profiles.
- Multi-agent orchestration guide (`reference/multi-agent.md`): SDK-as-coordination-surface model, isolation patterns, merge protocol, scaling guidance, and anti-patterns.
- Iteration protocol (`reference/iteration.md`): structured inner/outer loops, attempt budgets, token budget guidance, stop conditions, and context state integration.
- Security audit workflow: `security-auditor` subagent, `templates/security-audit-template.md`, and security audit added as formal discovery trigger in recovery protocol.
- Four new templates: `sdk-design-template.md` (Phase 3 scaffold), `deployment-checklist-template.md` (Phase 7 scaffold), `incident-postmortem-template.md` (post-incident analysis with gap assessment integration), `retrospective-template.md` (periodic methodology health review).
- Expanded worked example (`examples/task-manager/`): added project intake, design identity (API naming and copy voice), SDK constraint surface (`sdk/types.ts`), context state at Phase 5, and block registry.
- Iteration Protocol section added to `harness/agent/AGENT_RULES.md`.
- Quick Changes section added to `harness/PLAYBOOK.md`.

### Changed

- Reference document count increased to 18 (up from 13).
- Template count increased to 22+ (up from 20).
- Cursor skill count increased to 10 (up from 9).
- Worked examples increased to 2 (greenfield task-manager + brownfield bookmarks API).
- Test plan template now includes property-based tests and accessibility tests sections.
- Design identity template now includes accessibility commitments section.
- Cursor skill coverage now spans all pipeline phases (9 skills total, up from 4).
- Cursor subagent coverage expanded to 6 (up from 3).
- Template count increased to 20 (up from 16).
- Reference document count increased to 13 (up from 10).
- `AGENT_RULES.md` reorganized: Communication Protocol renumbered to section 5 to accommodate new Iteration Protocol section 4.
- `hooks.json` upgraded from prompt-only to include command-type hooks with executable scripts for design token and contract enforcement.
- `.github/workflows/codex-gates.yml` added alongside existing `validate-docs.yml` for methodology-level quality gates.

### Fixed

- Template naming mismatches in `reference/adoption-profiles.md`: `specification-template.md` corrected to `spec-template.md`, `interface-contracts-template.md` corrected to `interface-contract-template.md`, `architecture-template.md` split into `architecture-decision-record.md` + `module-boundary-template.md`.
- Profile field missing from `project-intake-template.md` despite being referenced in adoption profiles documentation.

## [0.2.0] - 2026-05-20

### Added

- Recovery protocol (`reference/recovery.md`): formal process for closing gaps in specification, tests, or coverage after code already exists. Covers discovery triggers, gap classification (spec gap, SDK gap, mold gap, coverage erosion, contract gap), severity-based triage, the six-step recovery sequence (audit, spec patch, SDK patch, mold patch, recast, re-review), kanban integration, recurrence prevention, and health metrics.
- Gap assessment template (`harness/templates/gap-assessment-template.md`): structured template for documenting discovered gaps during recovery.
- Recovery acknowledgment in `MANIFESTO.md` Section XI (The Fracture Lines): recognizes that gaps are inevitable and defines recovery as the methodology applied in reverse.
- Recovery procedure in `harness/PLAYBOOK.md`: expanded Iteration and Feedback section with recovery sequence, exit criteria, human and agent responsibilities, and kanban treatment.
- Agent rules R13 (halt and report gaps) and R15 (recovery task behavior) in `harness/agent/AGENT_RULES.md`.
- Retroactive gap discovery failure mode in `reference/agent-operating-model.md`.
- Retroactive Gap Discovery section in `reference/workflow.md` feedback loops.
- Recovery terms added to `reference/glossary.md`: contract gap, coverage erosion, gap assessment, mold gap, recovery, spec gap.
- Recovery constraint and terminology added to `harness/.cursor/rules/codex-automata.mdc`.
- Agentic product testing (`reference/product-testing.md`): verification layer where AI agents operate the assembled application as real users with defined profiles and goal-oriented objectives. Measures UX quality through click counts, navigation depth, backtracking, error encounters, and time budgets.
- Product test template (`harness/templates/product-test-template.md`): structured template for defining product test scenarios with objectives, UX budgets, and specification traceability.
- User profile template (`harness/templates/user-profile-template.md`): test fixture template for defining simulated user personas with technical literacy, domain knowledge, constraints, and behavioral tendencies.
- Phase 6b (Product Testing) added to `harness/PLAYBOOK.md` between Review and Deployment.
- Product test section added to `harness/templates/test-plan-template.md`.
- Product testing terms added to `reference/glossary.md`: product test, test objective, user profile, UX budget.
- Product testing section added to `harness/.cursor/rules/codex-automata.mdc`.
- Product testing section added to `MANIFESTO.md` Section IX (The Machine).
- SDK as Constraint Surface principle (`reference/principles.md`).
- Local-First principle (`reference/principles.md`).
- Research as Foundation principle (`reference/principles.md`).
- Intentional Divergence principle (`reference/principles.md`).
- Design identity template (`harness/templates/design-identity-template.md`).
- Block registry template (`harness/templates/block-registry-template.md`).
- Context persistence mechanism for agent sessions and task continuity.
- Progressive adoption profiles for phased methodology rollout.
- Multi-tool `AGENTS.md` support for Cursor, Claude Code, and other agent runtimes.

### Changed

- Deep consistency audit and corrections across manifesto, playbook, reference docs, templates, and agent rules for version and terminology alignment.

## [0.1.0] - 2026-05-11

### Added

- Initial repository scaffold, manifesto, playbook, documentation, templates, example project, agent rules, Cursor IDE integration (rules, skills, subagents, hooks), and GitHub configuration.
