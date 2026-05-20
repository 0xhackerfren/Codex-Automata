# Design Identity: Task Manager

<!--
Filled example for a CLI/library module with no visual UI. Demonstrates naming conventions, copy voice, and slop fingerprints that apply to API design and error messages.
-->

## Product Identity

**Product name:** TaskManager Module

**What is this product?** A TypeScript module for managing tasks with CRUD operations and pluggable storage.

**Who uses it?** Developers integrating task management into their applications.

**What feeling should it evoke?** Confidence in correctness. The API should feel predictable and unsurprising.

## Aesthetic Direction

**Direction:** N/A (no visual UI). Focus on API design identity: predictable method names, explicit error types, and domain-specific module boundaries.

## Anti-Patterns and Slop Fingerprints

Patterns that this project must not exhibit. Checked during review and divergence gates.

### Banned Naming

- No `utils.ts`, `helpers.ts`, `misc.ts`, or `common.ts`. Module names must be domain-specific.
- No single-letter variables outside loop counters. No abbreviated names (`mgr`, `cfg`, `ctx`) when full words are clear.

### Banned Copy

- No generic error messages such as "Something went wrong. Please try again later." Errors must name the problem specifically.

### Banned Structural

- No god objects. TaskManager does not also handle users, authentication, or notifications.

## Typography, Color, and Spatial Systems

N/A (no user interface). Design tokens for visual presentation are not part of this module's SDK.

## Copy Voice

**Tone:** Direct and technical.

**Error message style:** Name the specific problem and suggest the fix. Example: `Task not found: no task exists with id '{id}'` — not "An error occurred."

### Banned Phrases

- "Something went wrong. Please try again later."
- "An error occurred."
- "Oops" or other casual error openers.

## Naming Conventions

**Module naming:** Domain-noun pattern: `task-manager`, `in-memory-storage`. Never `utils`, `helpers`, `misc`, or `common`.

**Interface naming:** Capability pattern: `TaskManager`, `Storage`. Never `ITaskManager` or `TaskManagerInterface`.

**Method naming:** Verb-noun: `createTask`, `listTasks`, `completeTask`, `deleteTask`. Never `handleTask` or `processTask`.

**Error naming:** Condition pattern: `TaskNotFoundError`, `TaskAlreadyCompleteError`, `InvalidTaskInputError`. Never `GenericError` or `Error1`.

## Architectural Divergence

| Decision | Default (avoided) | Chosen alternative | Rationale |
|----------|-------------------|-------------------|-----------|
| Storage wiring | Singleton storage instance shared globally | Constructor injection of `Storage` | Testability and pluggability without modifying TaskManager when swapping backends |
