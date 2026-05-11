# Agent Task: AT-002, Implement InMemoryStorage

## Specification Reference

`docs/spec.md` (persistence dependency), `docs/interface-contracts.md` (Contract 2, Storage Interface).

## Scope

Implement an in-memory storage backend that satisfies the **Storage** **interface contract**.

## Inputs

- Interface contract: `docs/interface-contracts.md`, Contract 2
- Contract tests: `tests/test-plan.md`, Contract Tests section

## Expected Outputs

Source file(s) implementing `InMemoryStorage`. All contract tests pass.

## Acceptance Criteria

- All 4 contract tests pass.
- Implements the `Storage` interface exactly as defined.
- Data lives in process memory only (no external dependencies).

## Constraints

- Satisfy the `Storage` **interface contract** without changing it.
- Do not add methods not listed on the contract.

## Out Of Scope

TaskManager implementation, durable or file-based storage.
