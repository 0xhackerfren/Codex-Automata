# Task Manager Example (Codex Automata)

## What This Is

A worked example of Codex Automata applied to a simple task manager. It shows documentation, specs, tests, contracts, and agent-executable tasks in one place without application source code.

## Domain

Tasks support CRUD operations: create, list, complete (status change), and delete. Each task has a title, optional description, status (pending or complete), and timestamps.

## What The Example Demonstrates

The **Docs to Tests to Code** pipeline: specification drives the mold (tests); code is casting that fits the mold. This repository holds only specifications, architecture notes, interface contracts, a test plan, agent tasks, and a sample human review. No runnable application code ships here.

## Directory Structure

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Nested agent instructions for this example reference |
| `README.md` | This overview |
| `docs/spec.md` | Specification for Task Manager Core |
| `docs/architecture.md` | Bounded context, modules, decisions |
| `docs/interface-contracts.md` | TaskManager and Storage interface contracts |
| `tests/test-plan.md` | Test plan derived from the specification |
| `tasks/agent-task-001.md` | Agent task: implement TaskManager |
| `tasks/agent-task-002.md` | Agent task: implement InMemoryStorage |
| `review/human-review.md` | Example completed human review |

## Using This Example For Your Own Project

1. Read the documents in order: specification, architecture, interface contracts, test plan.
2. Compare how each quality gate (spec, contracts, tests) constrains agent tasks.
3. To start your own project, run `scripts/init.ps1` (or `init.sh`) from the Codex Automata repo, or manually copy `harness/` contents into your project root.

**Note:** No application code is included. The point is to show the harness: how specifications, molds, and agent tasks align before casting.
