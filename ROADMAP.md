# Roadmap

This document sketches planned evolution of the Codex Automata methodology harness, templates, examples, tooling, and quality gates. Priorities may shift based on community feedback and real-world usage.

## v0.5.0 (Current)

### Achieved

- **Pipeline as First Citizen principle** (Principle 12): CI/CD pipeline and git workflow elevated to first-class engineering artifacts designed at architecture time. Agent rules R16-R18 govern branch strategy, pipeline config, and release tagging. Pipeline design added as Phase 1 output. Full cross-reference propagation across all reference docs, skills, subagents, templates, and agent rules.
- **Assembly Pressure principle** (Principle 11): after each cast increment, exercise the running assembly under realistic conditions. Incremental alpha checkpoints in the playbook, distinct from Phase 6b formal product testing.
- **Expanded Intentional Divergence** (Principle 10): broadened from human-perceptible surfaces to all output surfaces including code structure, covering over-abstraction, cargo-cult patterns, and speculative generality. Core thesis: "good" is trivially achievable; the differentiator is statistical divergence from the bell-curve center.
- **Python CLI** (`cli/`): `codex-automata init`, `update`, and `verify` commands. Installable via pip or uv. Cross-platform with automatic Windows/Unix detection.
- **Windows parity**: PowerShell equivalents for all Cursor hooks (`.cursor/hooks/*.ps1`), platform-aware hooks.json patching in init scripts, `windows-latest` CI jobs in shipped workflow.
- **Principle ordering consistency**: root `AGENTS.md` principle list aligned with `reference/principles.md` canonical order.

### Still planned

- Language-specific starter kits (planned for v1.0.0).
- PyPI/npm package publication (currently install from git).
- GitHub template repository for one-click project creation.
- Automated specification-to-test generation tooling where it respects frozen contracts and bounded context seams.
- Reusable CI/CD quality gate library extending Pipeline as First Citizen (Principle 12) beyond the current `codex-gates.yml` workflow.
- Real worked examples with actual application code spanning molds, casting, agent tasks, and flow documentation.
- Visual regression testing integration (screenshot diffing, layout analysis) for design identity compliance.
- Product test runner reference implementation with browser agent orchestration and journey log capture.
- WCAG contrast ratio validator for design token color pairings.
- Coverage threshold configuration and enforcement scripts.

## v0.4.0

### Achieved

- **Brownfield onboarding protocol** with audit template and worked example (`reference/brownfield-onboarding.md`, `brownfield-audit-template.md`, `examples/brownfield-api/`).
- **Agent guardrails** with three-tier action classification (AUTO/LOG/APPROVE) (`reference/guardrails.md`, guardrail config template, playbook and agent rules integration).
- **Property-based testing** as advanced molds (`reference/property-based-testing.md`, test molding rules, test plan template section).
- **Cost-conscious development guide** with token budgets and model tiering (`reference/cost-awareness.md`, agent rules core principle).
- **Accessibility** as first-class methodology concern (`reference/accessibility.md`, design identity and test plan template sections, code-casting rule).

## v0.3.0

### Achieved

- **Full skill and subagent coverage**: Nine Cursor skills (including `/quick-change`) spanning all pipeline phases; six subagents (`spec-reviewer`, `test-deriver`, `code-caster`, `sdk-designer`, `product-tester`, `security-auditor`).
- **Quick-change workflow**: Abbreviated path for bug fixes and small changes within existing spec/SDK/test coverage (`reference/quick-change.md`, `/quick-change` skill). Available at all adoption profiles.
- **Multi-agent orchestration guide** (`reference/multi-agent.md`): SDK-as-coordination-surface model, isolation patterns, merge protocol, scaling guidance, and anti-patterns.
- **Iteration protocol** (`reference/iteration.md`): Structured inner/outer loops, attempt budgets, token budget guidance, stop conditions, and context state integration. Wired into `AGENT_RULES.md` and playbook.
- **Security audit workflow**: `security-auditor` subagent, `security-audit-template.md`, and security audit as a formal discovery trigger in the recovery protocol.
- **Four new templates**: SDK design (Phase 3), deployment checklist (Phase 7), incident postmortem, and retrospective (methodology health review). Template count now 20.
- **Enriched worked example** (`examples/task-manager/`): Project intake, design identity, SDK types (`sdk/types.ts`), context state at Phase 5, and block registry.

### Enforcement tooling (achieved)

- **Divergence gate scripts** (bash + PowerShell): scan source files for slop fingerprints from the design identity's banned pattern catalog. Default catalog covers banned fonts, hardcoded colors, generic copy, structural anti-patterns. Configurable via JSON for project-specific fingerprints. CI-ready exit codes.
- **Spec-check scripts** (bash + PowerShell): verify spec-before-code (R1) by checking that every source module has a corresponding specification document.
- **Commit-lint scripts** (bash + PowerShell): validate commit messages for specification traceability (R7) via recognized prefixes, spec section references, or task references. Usable as git hooks or CI checks.
- **Command-type Cursor hooks**: afterFileEdit hook warns on hardcoded visual values; preToolUse hook requires human approval for SDK/contract modifications (R3).
- **CI quality gate workflow** (`codex-gates.yml`): GitHub Actions running spec-check, divergence gate, commit lint, and auto-detected test suite for adopter projects.
- **SDK design rules** (`SDK_DESIGN_RULES.md`) and `/sdk-design` skill completing Phase 3 coverage.
- **Five new Cursor skills**: `/sdk-design`, `/architecture`, `/review`, `/product-testing`, `/recovery` (9 total, full phase coverage).
- **Profile field** added to project intake template; naming mismatches fixed in adoption profiles.

## v0.2.0

- **Recovery protocol**: Formal process for closing gaps in specification, SDK, tests, or coverage after code exists. Includes gap classification taxonomy (spec, SDK, mold, coverage erosion, contract), severity-based triage, six-step recovery sequence (audit, spec patch, SDK patch, mold patch, recast, re-review), kanban integration, gap assessment template, recurrence prevention, and health metrics. Wired into manifesto, playbook, agent rules, Cursor rules, and glossary.
- **Product testing**: Agentic verification layer where AI agents operate the assembled application as real users. Agents receive user profiles (technical literacy, domain knowledge, constraints) and goal-oriented objectives, then navigate the product through its UI. Captures UX quality metrics (click count, navigation depth, backtracking, error encounters, time budgets). Includes product test template, user profile template, Phase 6b in the playbook, and glossary terms.
- SDK as Constraint Surface, Local-First, Research as Foundation, and Intentional Divergence principles; design identity and block registry templates; context persistence; progressive adoption profiles; multi-tool `AGENTS.md` support.

## v1.0.0 (goals)

- Stable methodology narrative and templates proven across multiple bounded contexts.
- Comprehensive example library showing diverse flows end to end.
- Tooling ecosystem (spec authoring helpers, molds, validators) interoperable with common stacks.
- Broader adoption and maintainer playbook for onboarding contributors and agent task operators.

## Future considerations

- IDE integration beyond Cursor where interface contracts and agent task models still map cleanly.
- Exploration of a formal specification language or constraint layer over natural-language specifications.
- Agent benchmarking framework tied to quality gates and human review baselines.

## Living document

This roadmap is not a commitment schedule. Version goals express direction: adjust scope only when specifications and human review signal a change in priority.
