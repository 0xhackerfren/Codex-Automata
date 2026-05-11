# Codex Automata: Agent Operating Instructions

This repository follows the Codex Automata methodology. All AI agents operating in this codebase must follow these rules.

## Core Doctrine

1. Documentation comes first. Tests come second. Code comes last.
2. Specifications are the primary engineering artifact.
3. Tests are the mold. Code is the casting.
4. Do not write implementation before the specification and tests exist.

## Constraints

- Do not expand scope without updating the specification first.
- Do not silently change interfaces. Interface contracts are frozen before code casting begins.
- Do not bypass failing tests. Fix the implementation or surface the test as incorrect.
- Do not create duplicate abstractions. Check existing modules and interfaces before adding new ones.
- Prefer small, atomic commits traceable to specification sections.
- Surface ambiguity instead of guessing. If the specification is unclear, stop and ask.
- Every task must map to a specification section and at least one test case.
- Explain deviations. If you must deviate from the specification, document why.

## Workflow

When given a task:

1. Locate the relevant specification in `docs/` or the project's spec directory.
2. Locate the corresponding test plan and test cases.
3. Implement only what the specification and tests require.
4. Verify all tests pass before marking the task complete.
5. If the specification or tests are missing, stop and report this before proceeding.

## Directory Guide

- `docs/` is for project documentation: specifications, architecture decisions, interface contracts.
- `tests/` is for test plans and test code.
- `tasks/` is for agent task definitions.
- `review/` is for human review records.
- `src/` is for source code (the castings).
- `templates/` contains reusable templates. Copy them into `docs/`, `tests/`, or `tasks/` as needed.
- `agent/` contains detailed agent operating rules for each phase.
- `.cursor/rules/` contains Cursor-native rules automatically applied to agent context.
- `.cursor/skills/` contains invocable workflows (trigger with `/skill-name` in chat).
- `.cursor/agents/` contains custom subagent definitions for specialized roles.

For the complete agent operating manual, see `agent/AGENT_RULES.md`.
