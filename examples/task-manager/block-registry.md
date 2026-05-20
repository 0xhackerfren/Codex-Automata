# Building Block Registry: Task Manager

A project-level index of SDK building blocks for the Task Management bounded context. Consult this registry before adding new abstractions.

## Registry

| Building Block | Bounded Context | SDK Surface | Molds Satisfied | Contracts Honored | Status |
|----------------|----------------|-------------|-----------------|-------------------|--------|
| Task | TaskManagement | `Task`, `TaskStatus`, `CreateTaskInput`, `ListTasksFilter` | `tests/test-plan.md` TC-01 through TC-04 | N/A (domain type) | Active |
| TaskManager | TaskManagement | `TaskManager` interface: `createTask()`, `listTasks()`, `completeTask()`, `deleteTask()` | `tests/test-plan.md` TC-01 through TC-12 | `docs/interface-contracts.md` TaskManager contract | Active |
| Storage | TaskManagement | `Storage` interface: `save()`, `findById()`, `findAll()`, `delete()` | `tests/test-plan.md` TC-13 through TC-18 | `docs/interface-contracts.md` Storage contract | Active |
| InMemoryStorage | TaskManagement | Implements `Storage` | `tests/test-plan.md` TC-13 through TC-18 | `docs/interface-contracts.md` Storage contract | Active |

## Entry Field Definitions

**Building Block.** The composable unit in the SDK constraint surface (`sdk/types.ts` or casting under `src/`).

**Bounded Context.** The context this block belongs to (exactly one).

**SDK Surface.** Published types, interfaces, and extension points consumers depend on.

**Molds Satisfied.** Test plan sections or cases that verify this block.

**Contracts Honored.** Interface contract documents this block implements; N/A for pure domain types.

**Status.** Active, Deprecated, or Proposed.
