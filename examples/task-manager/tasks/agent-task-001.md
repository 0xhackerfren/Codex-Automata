# Agent Task: AT-001, Implement TaskManager Core

## Specification Reference

`docs/spec.md`, Behaviors 1 through 4.

## Scope

Implement the **TaskManager** module with `create_task`, `list_tasks`, `complete_task`, and `delete_task`. The module receives a `Storage` **interface contract** via constructor injection.

## Inputs

- Specification: `docs/spec.md`
- Test plan (mold): `tests/test-plan.md`
- Interface contracts: `docs/interface-contracts.md`

## Expected Outputs

Source file(s) implementing the TaskManager **interface contract**. All unit tests named in the test plan for TaskManager must pass.

## Acceptance Criteria

- All 15 unit tests in the test plan pass.
- No direct storage access outside the `Storage` interface contract.
- No modifications to **interface contracts** without a specification change and review.

## Constraints

- Do **not** implement the `Storage` interface. That is **AT-002**.
- Use the `Storage` interface exactly as defined in the contract.

## Out Of Scope

Storage implementation, API layer, CLI, UI.
