# Codex Automata

**The hard part of software was never the code.**

A research-driven, spec-first, SDK-first, local-first development methodology for the agentic era. Copy one directory into any project and the methodology is active: research informs decisions, specifications first, SDK second, tests third, code last. Build for the smallest viable model, expand to frontier as needed. Documentation is the primary engineering artifact. The SDK is the constraint surface. Tests are the mold. Code is the casting.

[Read the Manifesto](MANIFESTO.md) | [Browse the Playbook](harness/PLAYBOOK.md) | [MIT License](LICENSE)

## What Is This?

Codex Automata is a development methodology for the agentic era. It inverts the traditional pipeline:

1. **Research informs decisions.** Agents investigate technologies, patterns, and the landscape before specifying.
2. **Documentation comes first.** Specify the system before implementing it.
3. **SDK comes second.** Express the architecture as compilable building blocks. The SDK is the constraint surface.
4. **Tests come third.** Derive tests from the specification, written against SDK interfaces. The tests are the mold.
5. **Code comes last.** Agents fill the mold within the SDK boundary. The code is the casting.
6. **Build local-first.** Design for the smallest viable model. Expand to frontier as needed. Constraint forces discipline.

This repository contains the harness (the thing you copy into projects) and reference material (the methodology documentation you read).

## Quickstart

### Option 1: Init script (recommended)

Clone this repo somewhere permanent, then initialize any project:

```powershell
# Clone once
git clone https://github.com/0xhackerfren/Codex-Automata.git D:\tools\Codex-Automata

# Initialize a new project
D:\tools\Codex-Automata\scripts\init.ps1 -TargetPath D:\projects\my-new-app
```

On Linux or macOS:

```bash
git clone https://github.com/0xhackerfren/Codex-Automata.git ~/tools/Codex-Automata
~/tools/Codex-Automata/scripts/init.sh ~/projects/my-new-app
```

### Option 2: Manual copy

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
  templates/             Spec, test plan, ADR, contract, task, review templates
  docs/                  Empty, ready for your project specifications
  sdk/                   Empty, ready for SDK constraint surface (types, interfaces)
  tests/                 Empty, ready for test plans and test code
  tasks/                 Empty, ready for agent task definitions
  review/                Empty, ready for human review records
  src/                   Empty, ready for source code
```

Open the project in Cursor IDE and the methodology enforces itself:

- **Rules** (`.cursor/rules/`) load automatically into every agent session. They enforce spec-first development, test-before-code constraints, and interface contract discipline.
- **Skills** (`.cursor/skills/`) provide guided workflows. Type `/spec-writing`, `/test-molding`, `/code-casting`, or `/project-intake` in chat.
- **Subagents** (`.cursor/agents/`) handle specialized tasks: spec review, test derivation, code casting. They run in isolated contexts and can work in parallel.
- **Hooks** (`.cursor/hooks.json`) remind agents to check spec and test coverage when source files are edited.
- **AGENTS.md** provides root-level instructions that any AI agent (Cursor or otherwise) picks up automatically.

## First Steps After Init

1. Read `PLAYBOOK.md` for the phase-by-phase guide.
2. Copy `templates/project-intake-template.md` to `docs/intake.md` and fill it in.
3. Or type `/project-intake` in Cursor chat to start guided setup.
4. Follow the phases: Intake, Architecture, Specification, SDK Design, Test Molding, Code Casting, Review, Deployment.

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
|   |-- agent/               Detailed agent operating rules
|   |-- templates/           All project templates (spec, test, ADR, contract, task, review, gap assessment)
|   |-- docs/                Empty project docs directory
|   |-- sdk/                 Empty SDK constraint surface directory
|   |-- tests/               Empty project tests directory
|   |-- tasks/               Empty agent tasks directory
|   |-- review/              Empty human review directory
|   |-- src/                 Empty source code directory
|
|-- reference/               METHODOLOGY DOCS (read, don't copy)
|   |-- principles.md        Core principles explained
|   |-- workflow.md           End-to-end workflow reference
|   |-- architecture.md      Architecture patterns and guidance
|   |-- kanban.md             Flow-based project management
|   |-- agent-operating-model.md  How agents operate
|   |-- recovery.md           Recovery protocol for closing gaps
|   |-- product-testing.md    Agentic product testing reference
|   |-- glossary.md           Terminology reference
|
|-- examples/                WORKED EXAMPLES (read, don't copy)
|   |-- task-manager/        Complete example: spec, tests, tasks, review
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
Specification --> SDK --> Tests --> Code
     (docs)      (constraint)  (mold)    (casting)
```

- **Specifications** are the primary engineering artifact. They define what the system must do.
- **SDK** is the constraint surface. It expresses the architecture as compilable building blocks that constrain all downstream work.
- **Tests** are the mold. Derived from specifications and written against SDK interfaces, they constrain the shape of the implementation.
- **Code** is the casting. Agents pour implementation into the mold, within the SDK boundary, until all tests pass.

If the casting is defective, fix the mold. If the mold is wrong, fix the specification. If new building blocks are needed, extend the SDK through the specification pipeline. Do not debug the implementation directly.

## Product Testing

After the code is assembled, AI agents verify the product by operating it as real users. Each agent receives a user profile (technical literacy, domain knowledge, constraints) and a goal-oriented objective ("as a first-time user, create an account and reach the dashboard"). The agent navigates the application through the UI, and the journey produces measurable signals:

- **Click count and navigation depth** measure friction.
- **Backtracking and dead ends** measure discoverability.
- **Error encounters** measure input guidance quality.
- **Abandonment** flags critical usability failures.

UX budgets set quantitative thresholds for each metric. Product tests run as quality gates in CI, staging, and production canaries. See `reference/product-testing.md` for the full reference.

## When Gaps Are Discovered

Real projects discover gaps after code exists: a production incident exposes an unspecified failure mode, a review reveals missing tests, or a new team member finds a module with no contract tests. Codex Automata defines a formal recovery protocol for these situations.

Recovery follows the same pipeline as forward work, applied retroactively:

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
2. **Specification writing.** Define what the system must do, precisely.
3. **SDK design.** Express the architecture as compilable building blocks.
4. **Test design.** Derive the mold from the specification against SDK interfaces.
5. **Review.** Verify castings match the mold, SDK, and intent.
6. **Deployment decisions.** Ship and observe.

Read `MANIFESTO.md` for the full philosophy, or browse `reference/` for detailed methodology documentation.

## License

MIT. See [LICENSE](LICENSE).
