# Specification: Task Manager Core

## Overview

A module for managing tasks with create, list, complete, and delete operations. The specification is the primary artifact; tests form the mold; implementation is casting.

## Scope

- Create, list, complete, and delete tasks.
- Single-user usage (no multi-tenant or auth in this specification).
- Persistence is either in-memory or durable; the choice is fixed in architecture, not in this behavioral specification.

## Domain Model

**Task** entity:

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | string | UUID |
| `title` | string | Required, max 200 characters |
| `description` | string | Optional, max 2000 characters |
| `status` | enum | `pending`, `complete` |
| `created_at` | timestamp | Set on create |
| `completed_at` | timestamp | Nullable; set when status becomes `complete` |

## Behaviors

1. **Create Task**  
   Given a title and optional description, create a new task with status `pending`, a generated `id`, and `created_at`. Return the created task.  
   **Errors:** Empty title; title longer than 200 characters.

2. **List Tasks**  
   Return all tasks. Optional filter by `status`.  
   Return an empty list if no tasks exist or if the filter matches nothing.

3. **Complete Task**  
   Given a task `id`, set `status` to `complete` and set `completed_at`.  
   **Errors:** Task not found; task already `complete`.

4. **Delete Task**  
   Given a task `id`, remove the task.  
   **Errors:** Task not found.

## Edge Cases

- Empty title on create.
- Title at exactly max length (200 characters).
- Description at exactly max length (2000 characters).
- Completing a task that is already `complete`.
- Deleting a task that does not exist.
- Listing when no tasks exist.
- Listing with a filter that matches no tasks.

## Failure Modes

- Storage unavailable (implementation must surface a storage-level failure).
- Invalid input types (implementation must reject or validate before use).

## Non-Functional Requirements

Operations complete in under 100 ms for up to 10,000 tasks in the configured storage (per quality gate for this module).

## Interface Dependencies

- **Provides:** `TaskManager` interface (see interface contract).
- **Depends on:** `Storage` interface (see interface contract).
