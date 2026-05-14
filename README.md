# Codex Automata

**The hard part of software was never the code.**

A spec-first, test-first development methodology for the agentic era. Copy one directory into any project and the methodology is active: specifications first, tests second, code last. Documentation is the primary engineering artifact. Tests are the mold. Code is the casting.

[Read the Manifesto](MANIFESTO.md) | [Browse the Playbook](harness/PLAYBOOK.md) | [MIT License](LICENSE)

## What Is This?

Codex Automata is a development methodology for the agentic era. It inverts the traditional pipeline:

1. **Documentation comes first.** Specify the system before implementing it.
2. **Tests come second.** Derive tests from the specification. The tests are the mold.
3. **Code comes last.** Agents fill the mold. The code is the casting.

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
4. Follow the phases: Intake, Architecture, Specification, Test Molding, Code Casting, Review, Deployment.

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
Specification --> Tests --> Code
     (docs)        (mold)    (casting)
```

- **Specifications** are the primary engineering artifact. They define what the system must do.
- **Tests** are the mold. Derived from specifications, they constrain the shape of the implementation.
- **Code** is the casting. Agents pour implementation into the mold until all tests pass.

If the casting is defective, fix the mold. If the mold is wrong, fix the specification. Do not debug the implementation directly.

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
3. **Patch the mold** by deriving tests from the specification.
4. **Recast** the implementation if the new tests fail.
5. **Re-review** the complete recovery unit.

Recovery tasks are first-class kanban work items, not invisible tech debt. See `reference/recovery.md` for the full protocol.

## How Agents Operate

Agents working in a Codex Automata project follow strict rules (enforced by `.cursor/rules/` and `AGENTS.md`):

1. Do not write implementation before the specification and tests exist.
2. Do not expand scope without updating the specification.
3. Do not silently change interface contracts.
4. Do not bypass failing tests.
5. Prefer small, atomic commits traceable to specification sections.
6. Surface ambiguity instead of guessing.

See `agent/AGENT_RULES.md` (inside the harness) for the complete operating manual.

## How Humans Operate

Humans own the upstream work:

1. **Architecture and decomposition.** Break the system into bounded contexts.
2. **Specification writing.** Define what the system must do, precisely.
3. **Test design.** Derive the mold from the specification.
4. **Review.** Verify castings match the mold and intent.
5. **Deployment decisions.** Ship and observe.

Read `MANIFESTO.md` for the full philosophy, or browse `reference/` for detailed methodology documentation.

## License

MIT. See [LICENSE](LICENSE).
