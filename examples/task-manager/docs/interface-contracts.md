# Interface Contracts: Task Manager

This document freezes **interface contracts** before casting. Agents must not change these contracts without a specification update and human review.

## Contract 1: TaskManager Interface

**Provided by:** TaskManager module.

| Method | Signature |
|--------|-----------|
| Create | `create_task(title: string, description?: string) -> Task \| Error` |
| List | `list_tasks(filter?: { status: "pending" \| "complete" }) -> Task[]` |
| Complete | `complete_task(id: string) -> Task \| Error` |
| Delete | `delete_task(id: string) -> void \| Error` |

## Contract 2: Storage Interface

**Consumed by:** TaskManager.  
**Provided by:** Storage implementations (in-memory, file, etc.).

| Method | Signature |
|--------|-----------|
| Save | `save(task: Task) -> void \| Error` |
| Find all | `find_all(filter?: { status: string }) -> Task[]` |
| Find by id | `find_by_id(id: string) -> Task \| null` |
| Delete | `delete(id: string) -> void \| Error` |

## Data Model (Contract Shape)

**Task:**

```text
{
  id: string
  title: string
  description: string | null
  status: "pending" | "complete"
  created_at: string   // ISO 8601
  completed_at: string | null  // ISO 8601
}
```

## Error Types

| Error | Shape |
|-------|--------|
| Task not found | `{ code: "TASK_NOT_FOUND", task_id: string }` |
| Validation | `{ code: "VALIDATION_ERROR", field: string, message: string }` |
| Already complete | `{ code: "ALREADY_COMPLETE", task_id: string }` |
| Storage | `{ code: "STORAGE_ERROR", message: string }` |
