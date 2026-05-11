# Test Plan: Task Manager Core

This **test plan** is the mold derived from the specification. Tests should exist and fail (red state) before code casting begins.

## Coverage Matrix

| Spec behavior | Test cases (names) |
|---------------|-------------------|
| Create Task | `test_create_task_with_valid_title`, `test_create_task_with_description`, `test_create_task_empty_title`, `test_create_task_title_too_long`, `test_create_task_description_at_max` |
| List Tasks | `test_list_tasks_empty`, `test_list_tasks_returns_all`, `test_list_tasks_filter_pending`, `test_list_tasks_filter_complete`, `test_list_tasks_filter_no_match` |
| Complete Task | `test_complete_task_success`, `test_complete_task_not_found`, `test_complete_task_already_complete` |
| Delete Task | `test_delete_task_success`, `test_delete_task_not_found` |
| Storage contract | `test_storage_save_and_retrieve`, `test_storage_find_all_empty`, `test_storage_delete`, `test_storage_filter_by_status` |

## Unit Tests (TaskManager)

| Test | Description |
|------|-------------|
| `test_create_task_with_valid_title` | Create with title `Buy groceries`; expect `pending` task with generated `id`. |
| `test_create_task_with_description` | Create with title and description; expect both stored. |
| `test_create_task_empty_title` | Expect `ValidationError`. |
| `test_create_task_title_too_long` | 201-character title; expect `ValidationError`. |
| `test_create_task_description_at_max` | 2000-character description; expect success. |
| `test_list_tasks_empty` | No tasks; expect empty array. |
| `test_list_tasks_returns_all` | Create 3 tasks; expect all 3 returned. |
| `test_list_tasks_filter_pending` | Create 3, complete 1, filter `pending`; expect 2. |
| `test_list_tasks_filter_complete` | Filter `complete`; expect 1. |
| `test_list_tasks_filter_no_match` | Filter `complete` with no complete tasks; expect empty. |
| `test_complete_task_success` | Create then complete; expect `complete` and `completed_at` set. |
| `test_complete_task_not_found` | Complete missing id; expect `TaskNotFoundError`. |
| `test_complete_task_already_complete` | Complete same task twice; expect `AlreadyCompleteError`. |
| `test_delete_task_success` | Create then delete; task absent from list. |
| `test_delete_task_not_found` | Delete missing id; expect `TaskNotFoundError`. |

## Contract Tests (Storage)

| Test | Description |
|------|-------------|
| `test_storage_save_and_retrieve` | Save a task; `find_by_id` returns it. |
| `test_storage_find_all_empty` | Nothing saved; `find_all` returns empty. |
| `test_storage_delete` | Save then delete; `find_by_id` returns null. |
| `test_storage_filter_by_status` | Save mixed statuses; filtered `find_all` returns correct subset. |

## Exit Criteria

All listed tests compile and **fail** (red) before casting begins. After casting, they pass as the quality gate for the corresponding agent tasks.
