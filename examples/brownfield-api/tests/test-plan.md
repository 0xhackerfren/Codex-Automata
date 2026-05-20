# Test Plan: BookmarkManager

Mold derived from `docs/spec-bookmark-manager.md` during brownfield onboarding. Tests should be written against `BookmarkManager` SDK interface before recasting legacy Express handlers.

## Coverage Matrix

| Spec behavior | Test cases (names) |
|---------------|-------------------|
| Create Bookmark | `test_create_bookmark_valid_url`, `test_create_bookmark_with_tags`, `test_create_bookmark_invalid_url`, `test_create_bookmark_duplicate_url`, `test_create_bookmark_tag_limit`, `test_create_bookmark_url_validation_timeout` |
| List Bookmarks | `test_list_bookmarks_empty`, `test_list_bookmarks_all`, `test_list_bookmarks_filter_by_tag`, `test_list_bookmarks_filter_no_match` |
| Update Bookmark | `test_update_bookmark_success`, `test_update_bookmark_not_found`, `test_update_bookmark_duplicate_url`, `test_update_bookmark_invalid_url` |
| Delete Bookmark | `test_delete_bookmark_success`, `test_delete_bookmark_not_found` |
| Bulk Import | `test_bulk_import_all_success`, `test_bulk_import_partial_failure`, `test_bulk_import_empty_list`, `test_bulk_import_exceeds_limit` |
| Failure modes | `test_storage_unavailable_on_create`, `test_tag_service_unavailable_on_create` |

## Unit Tests (BookmarkManager)

| Test | Description |
|------|-------------|
| `test_create_bookmark_valid_url` | Create with HTTPS URL and title; expect persisted bookmark with timestamps. |
| `test_create_bookmark_with_tags` | Create with 3 valid tags; expect tags on returned bookmark. |
| `test_create_bookmark_invalid_url` | `javascript:` URL; expect `InvalidUrlError`. |
| `test_create_bookmark_duplicate_url` | Same user, same URL twice; expect `DuplicateBookmarkUrlError`. |
| `test_create_bookmark_tag_limit` | 21 tags; expect `TagLimitExceededError`. |
| `test_create_bookmark_url_validation_timeout` | Mock validator hangs; expect `UrlValidationTimeoutError`, no persist. |
| `test_list_bookmarks_empty` | New user; expect `[]`. |
| `test_list_bookmarks_all` | Create 2; list returns 2 sorted `created_at` desc. |
| `test_list_bookmarks_filter_by_tag` | Filter `reading`; only matching bookmarks returned. |
| `test_list_bookmarks_filter_no_match` | Filter unknown tag; empty list. |
| `test_update_bookmark_success` | Update title and description; `updated_at` advances. |
| `test_update_bookmark_not_found` | Random id; expect `BookmarkNotFoundError`. |
| `test_update_bookmark_duplicate_url` | Update URL to another bookmark's URL; conflict. |
| `test_update_bookmark_invalid_url` | Bad URL on update; `InvalidUrlError`. |
| `test_delete_bookmark_success` | Delete then list; bookmark absent. |
| `test_delete_bookmark_not_found` | Delete missing id; `BookmarkNotFoundError`. |
| `test_bulk_import_all_success` | 10 valid URLs; `imported === 10`, `failed` empty. |
| `test_bulk_import_partial_failure` | Mix valid and invalid; partial `imported`, failures listed. |
| `test_bulk_import_empty_list` | Empty array; validation error before processing. |
| `test_bulk_import_exceeds_limit` | 501 URLs; reject before processing. |
| `test_storage_unavailable_on_create` | Storage throws; no bookmark persisted. |
| `test_tag_service_unavailable_on_create` | TagService down; create fails fast. |

## Tests Explicitly Excluded (Pending Gap Resolution)

| Legacy behavior | Status |
|-----------------|--------|
| Archive bookmark (soft-delete) | Not in spec; see `gap-assessment-001.md` — do not add tests until spec patched |

## Exit Criteria

- All listed tests compile against SDK interfaces.
- On brownfield verify: run against existing implementation; failures become gap assessments or recast work.
- After recast: all tests pass for BookmarkManager paths.
