# Codex Automata

**The hard part of software was never the code.**

A research-driven, spec-first, SDK-first, local-first development methodology for the agentic era. Copy one directory into any project and the methodology is active: research informs decisions, specifications first, SDK second, tests third, code last. Build for the smallest viable model, expand to frontier as needed. Documentation is the primary engineering artifact. The SDK is the constraint surface. Tests are the mold. Code is the casting.

[Read the Manifesto](MANIFESTO.md) | [Browse the Playbook](harness/PLAYBOOK.md) | [MIT License](LICENSE)

## What Is This?

Codex Automata is a development methodology for the agentic era. It inverts the traditional pipeline to **Research → Documentation → SDK → Tests → Code**:

1. **Research informs decisions.** Agents investigate technologies, patterns, and the landscape before specifying.
2. **Documentation comes first.** Specify the system before implementing it.
3. **SDK comes second.** Express the architecture as compilable building blocks. The SDK is the constraint surface.
4. **Tests come third.** Derive tests from the specification, written against SDK interfaces. The tests are the mold.
5. **Code comes last.** Agents fill the mold within the SDK boundary. The code is the casting.

The methodology rests on [twelve core principles](reference/principles.md): Specification First, SDK as Constraint Surface, Local-First, Research as Foundation, Tests as Molds, Code as Casting, Modularity and Bounded Contexts, Continuous Flow, Quality Gates, Intentional Divergence, Assembly Pressure, and Pipeline as First Citizen. Build local-first: design for the smallest viable model, expand to frontier as needed.

This repository contains the harness (the thing you copy into projects) and reference material (the methodology documentation you read).

## Quickstart

### Option 1: Python CLI (recommended)

Install the CLI once, then initialize any project:

```powershell
# Install with uv (recommended)
uv tool install codex-automata --from git+https://github.com/0xhackerfren/Codex-Automata.git --subdirectory cli

# Or with pip
pip install git+https://github.com/0xhackerfren/Codex-Automata.git#subdirectory=cli

# Initialize a new project
codex-automata init D:\projects\my-new-app
codex-automata init D:\projects\my-new-app --profile essential
codex-automata init D:\projects\my-new-app --profile complete --agent claude
```

The CLI handles platform detection automatically (PowerShell hooks on Windows, bash on Unix). See [`cli/README.md`](cli/README.md) for `update` and `verify` commands.

### Option 2: Init script

Clone this repo somewhere permanent, then initialize any project:

```powershell
# Clone once
git clone https://github.com/0xhackerfren/Codex-Automata.git D:\tools\Codex-Automata

# Initialize a new project (Windows)
D:\tools\Codex-Automata\scripts\init.ps1 -TargetPath D:\projects\my-new-app
```

On Linux or macOS:

```bash
git clone https://github.com/0xhackerfren/Codex-Automata.git ~/tools/Codex-Automata
~/tools/Codex-Automata/scripts/init.sh ~/projects/my-new-app
```

### Option 3: GitHub template (planned)

Once this repository is configured as a GitHub template, you can create a new project directly from GitHub:

```powershell
gh repo create my-app --template 0xhackerfren/Codex-Automata --clone
cd my-app
# The harness is pre-wired; trim to your profile if needed
```

### Option 4: Manual copy

Copy the contents of `harness/` into your project root:

```powershell
xcopy /s /e /h harness\* D:\projects\my-new-app\
```

On Linux or macOS:

```bash
cp -r harness/. ~/projects/my-new-app/
```

## What You Get

After initialization, your project contains:

```
my-project/
  AGENTS.md              Agent instructions (active in Cursor automatically)
  PLAYBOOK.md            Phase-by-phase methodology guide
  .cursor/               Cursor IDE rules, skills, subagents, hooks
  .github/               PR template, issue templates, CI workflow
  agent/                 Detailed agent operating rules
  templates/             22+ templates: spec, test plan, ADR, contract, task, review, gap assessment, design identity,
                         block registry, SDK design, deployment checklist, incident postmortem, retrospective, security audit,
                         brownfield audit, guardrail config, and more
                         Design identity: aesthetic direction, typography, color system, copy voice, accessibility commitments, anti-patterns (user-facing surfaces)
                         Block registry: project-level index of SDK building blocks
  docs/                  Empty, ready for your project specifications
  sdk/                   Empty, ready for SDK constraint surface (types, interfaces)
  tests/                 Empty, ready for test plans and test code
  tasks/                 Empty, ready for agent task definitions
  review/                Empty, ready for human review records
  src/                   Empty, ready for source code
  scripts/               Enforcement scripts (divergence gate, spec check, commit lint)
```

Open the project in Cursor IDE and the methodology enforces itself:

- **Rules** (`.cursor/rules/`) load automatically into every agent session. They enforce spec-first development, test-before-code constraints, and interface contract discipline.
- **Skills** (`.cursor/skills/`) provide ten guided workflows across all pipeline phases: `/project-intake`, `/spec-writing`, `/sdk-design`, `/test-molding`, `/code-casting`, `/review`, `/product-testing`, `/recovery`, `/brownfield-onboarding`, and `/quick-change` (abbreviated path for small changes within existing coverage).
- **Subagents** (`.cursor/agents/`) handle six specialized tasks: spec review, test derivation, code casting, SDK design, product testing, and security audit. They run in isolated contexts and can work in parallel.
- **Hooks** (`.cursor/hooks.json`) enforce methodology constraints: prompt hooks remind agents to check spec/test coverage, command hooks warn on hardcoded visual values and require human approval for SDK/contract changes.
- **Enforcement scripts** (`scripts/`) run in CI or locally: `divergence-gate` scans for slop fingerprints, `spec-check` verifies spec-before-code, `commit-lint` validates commit traceability.
- **Guardrails** classify agent actions into three tiers—AUTO (proceed autonomously), LOG (proceed with audit trail), and APPROVE (require human approval before execution)—complementing quality gates and human oversight.
- **AGENTS.md** provides root-level instructions that any AI agent picks up automatically.

While `.cursor/` provides Cursor-specific integration (rules, skills, subagents, hooks), the `AGENTS.md` file and `agent/` directory work with any tool that reads agent instructions—Claude Code, GitHub Copilot, OpenAI Codex, Windsurf, and others.

## First Steps After Init

1. Read `PLAYBOOK.md` for the phase-by-phase guide.
2. Copy `templates/project-intake-template.md` to `docs/intake.md` and fill it in.
3. Or type `/project-intake` in Cursor chat to start guided setup.
4. Follow the phases: Phase 0 Intake, Phase 1 Architecture, Phase 2 Specification, Phase 3 SDK Design, Phase 4 Test Molding, Phase 5 Code Casting, Phase 6 Review, Phase 6b Product Testing, Phase 7 Deployment. For bug fixes and small changes already covered by spec, SDK, and tests, use the [quick-change workflow](reference/quick-change.md) or `/quick-change` in Cursor.

## Repository Structure

```
codex-automata/
|
|-- README.md                This file
|-- MANIFESTO.md             The full Codex Automata philosophy
|
|-- harness/                 THE HARNESS (copy into your projects)
|   |-- AGENTS.md            Root agent operating instructions
|   |-- PLAYBOOK.md          Phase-by-phase methodology guide
|   |-- .cursor/             Cursor IDE integration
|   |   |-- rules/           Auto-applied rules (.mdc)
|   |   |-- skills/          Invocable workflows (/skill-name)
|   |   |-- agents/          Custom subagent definitions
|   |   |-- hooks.json       Event-driven enforcement
|   |-- .github/             GitHub CI and templates
|   |-- agent/               Detailed agent operating rules (spec writing, SDK design, test molding, code casting, review)
|   |-- scripts/             Enforcement scripts (divergence gate, spec check, commit lint)
|   |-- templates/           22+ project templates (spec, test, ADR, contract, task, review, gap assessment, design identity,
|   |                        block registry, SDK design, deployment checklist, incident postmortem, retrospective, security audit,
|   |                        brownfield audit, guardrail config, and more)
|   |-- docs/                Empty project docs directory
|   |-- sdk/                 Empty SDK constraint surface directory
|   |-- tests/               Empty project tests directory
|   |-- tasks/               Empty agent tasks directory
|   |-- review/              Empty human review directory
|   |-- src/                 Empty source code directory
|
|-- reference/               METHODOLOGY DOCS (read, don't copy)
|   |-- principles.md        Twelve core principles explained
|   |-- adoption-profiles.md Essential, Standard, and Complete adoption profiles
|   |-- workflow.md           End-to-end workflow reference
|   |-- architecture.md      Architecture patterns and guidance
|   |-- kanban.md             Flow-based project management
|   |-- agent-operating-model.md  How agents operate
|   |-- recovery.md           Recovery protocol for closing gaps
|   |-- product-testing.md    Agentic product testing reference
|   |-- quick-change.md       Abbreviated workflow for small changes within existing coverage
|   |-- multi-agent.md        Multi-agent orchestration and SDK-as-coordination-surface
|   |-- iteration.md          Iteration protocol: loops, budgets, and stop conditions
|   |-- brownfield-onboarding.md  Adopting the methodology on existing codebases
|   |-- guardrails.md         Three-tier agent action classification (AUTO/LOG/APPROVE)
|   |-- property-based-testing.md  Advanced molds: specification-derived invariants with PBT
|   |-- cost-awareness.md     Token budgets, model tiering, and cost optimization
|   |-- accessibility.md      WCAG constraints, accessibility molds, and testing profiles
|   |-- glossary.md           Terminology reference (18 reference documents)
|
|-- examples/                WORKED EXAMPLES (read, don't copy)
|   |-- task-manager/        Greenfield example: spec, tests, tasks, review, design identity, SDK types, context state, block registry
|   |-- brownfield-api/      Brownfield example: Express.js bookmarks API—audit, retroactive spec, SDK extraction, tests, gap assessment
|
|-- cli/                     PYTHON CLI PACKAGE
|   |-- pyproject.toml       Package config (pip/uv installable)
|   |-- codex_automata/      CLI source: init, update, verify commands
|   |-- README.md            CLI usage docs
|
|-- scripts/                 AUTOMATION
|   |-- init.ps1             PowerShell init script
|   |-- init.sh              Bash init script
|
|-- .github/                 CI and templates for THIS repo
```

Note: `.github/` exists at both the repo root (for the Codex Automata project itself) and inside `harness/` (the copy shipped into initialized projects).

## The Core Pipeline

```
Research --> Documentation --> SDK --> Tests --> Code
              (docs)         (constraint)  (mold)    (casting)
```

- **Research** grounds specifications and architectural decisions in evidence before documentation is written.
- **Specifications** are the primary engineering artifact. They define what the system must do.
- **SDK** is the constraint surface. It expresses the architecture as compilable building blocks that constrain all downstream work.
- **Tests** are the mold. Derived from specifications and written against SDK interfaces, they constrain the shape of the implementation. [Property-based testing](reference/property-based-testing.md) extends molds with specification-derived invariants verified against random inputs (fast-check, Hypothesis, proptest).
- **Code** is the casting. Agents pour implementation into the mold, within the SDK boundary, until all tests pass.

If the casting is defective, fix the mold. If the mold is wrong, fix the specification. If new building blocks are needed, extend the SDK through the specification pipeline. Do not debug the implementation directly.

## Product Testing

Phase 6b runs after review and before deployment. After the code is assembled, AI agents verify the product by operating it as real users. Each agent receives a user profile (technical literacy, domain knowledge, constraints) and a goal-oriented objective ("as a first-time user, create an account and reach the dashboard"). The agent navigates the application through the UI, and the journey produces measurable signals:

- **Click count and navigation depth** measure friction.
- **Backtracking and dead ends** measure discoverability.
- **Error encounters** measure input guidance quality.
- **Abandonment** flags critical usability failures.

UX budgets set quantitative thresholds for each metric. Product tests run as quality gates in CI, staging, and production canaries. User profiles can include accessibility constraints (screen reader, keyboard-only, reduced motion) per [accessibility guidance](reference/accessibility.md). See `reference/product-testing.md` for the full reference.

## When Gaps Are Discovered

Real projects discover gaps after code exists: a production incident exposes an unspecified failure mode, a review reveals missing tests, or a new team member finds a module with no contract tests. Codex Automata defines a formal recovery protocol for these situations.

Recovery follows the same pipeline as forward work (Research → Documentation → SDK → Tests → Code), applied retroactively:

1. **Audit** the gap using `templates/gap-assessment-template.md`.
2. **Patch the spec** from domain knowledge (not from the existing code).
3. **Patch the SDK** if the constraint surface lacks types for the affected behavior.
4. **Patch the mold** by deriving tests from the specification against SDK interfaces.
5. **Recast** the implementation if the new tests fail.
6. **Re-review** the complete recovery unit.

Recovery tasks are first-class kanban work items, not invisible tech debt. See `reference/recovery.md` for the full protocol.

## How Agents Operate

Agents working in a Codex Automata project follow strict rules (enforced by `.cursor/rules/` and `AGENTS.md`):

1. Do not write tests or implementation before the specification and SDK exist.
2. Do not introduce abstractions outside the SDK constraint surface.
3. Keep context lean. Do not assume frontier capabilities or unlimited context windows.
4. Do not expand scope without updating the specification.
5. Do not silently change interface contracts or SDK interfaces.
6. Do not bypass failing tests.
7. Prefer small, atomic commits traceable to specification sections.
8. Surface ambiguity instead of guessing.

See `agent/AGENT_RULES.md` (inside the harness) for the complete operating manual.

## How Humans Operate

Humans own the upstream work:

1. **Architecture and decomposition.** Break the system into bounded contexts.
2. **Specification writing.** Define what the system must do, precisely. For user-facing surfaces, the design identity captures aesthetic direction and [accessibility commitments](reference/accessibility.md) (WCAG as specification constraint).
3. **SDK design.** Express the architecture as compilable building blocks.
4. **Test design.** Derive the mold from the specification against SDK interfaces.
5. **Review.** Verify castings match the mold, SDK, and intent.
6. **Product testing.** Define user profiles, objectives, and UX budgets; agents exercise the assembled product as real users (Phase 6b).
7. **Deployment decisions.** Ship and observe.

## Adoption Profiles

Teams can adopt Codex Automata at different depths. Three profiles—**Essential**, **Standard**, and **Complete**—match team size and project scale. All profiles include the [quick-change workflow](reference/quick-change.md) for bug fixes and small changes within existing spec, SDK, and test coverage. See [reference/adoption-profiles.md](reference/adoption-profiles.md) for guidance on which profile fits your situation.

Read `MANIFESTO.md` for the full philosophy, or browse `reference/` (18 documents) for detailed methodology documentation—including [multi-agent orchestration](reference/multi-agent.md), the [iteration protocol](reference/iteration.md), [agent guardrails](reference/guardrails.md), and [brownfield onboarding](reference/brownfield-onboarding.md).

## License

MIT. See [LICENSE](LICENSE).
