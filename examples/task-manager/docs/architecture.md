# Architecture: Task Manager

## Bounded Context

A **single bounded context** covers the task manager. The domain is small enough that one context keeps the flow simple and avoids duplicate abstractions.

## Modules

Two modules:

1. **TaskManager**  
   Business logic: validation, task lifecycle, orchestration of persistence through the `Storage` interface.

2. **Storage**  
   Persistence: save, query, and delete tasks according to the `Storage` interface contract.

## Interface Contract Between TaskManager And Storage

`TaskManager` depends only on the `Storage` **interface contract**, not on concrete storage. Casting may supply `InMemoryStorage`, `FileStorage`, or other implementations that honor the contract.

## Architecture Decision Records

### ADR-001: Repository Pattern For Storage Abstraction

**Decision:** Use a repository-style boundary (the `Storage` interface) between domain logic and persistence.

**Rationale:** Swapping storage implementations does not require changes to TaskManager business logic.

**Alternatives considered:** Direct storage access from TaskManager; ORM embedded in TaskManager.

### ADR-002: UUIDs For Task IDs

**Decision:** Use UUID strings for `id`.

**Rationale:** ID generation does not require coordination across nodes for this specification.

**Alternatives considered:** Auto-increment integers; nanoid-style strings.

## Dependency Graph

- `TaskManager` depends on the `Storage` interface.
- Concrete castings (for example `InMemoryStorage`, `FileStorage`) implement `Storage` and are injected into `TaskManager`.
