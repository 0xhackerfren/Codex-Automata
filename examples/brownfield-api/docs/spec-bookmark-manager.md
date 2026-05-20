# Specification: BookmarkManager

## Overview

BookmarkManager is the core module for storing and managing user bookmarks in the Bookmarks bounded context. This specification was written retroactively during brownfield onboarding from domain knowledge and product requirements—not derived from the existing Express handlers.

## Scope

- CRUD operations on bookmarks for a single authenticated user (auth is out of scope for this spec; assume `user_id` is provided by middleware).
- Tag association via TagService (interface dependency only; tag rules live in TagService spec).
- Bulk import from a URL list file or JSON payload.
- Out of scope: full-text search (SearchIndex module), tag CRUD (TagService module), sharing between users.

## Domain Model

**Bookmark** entity:

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | string | UUID, server-generated |
| `user_id` | string | Required; from auth context |
| `url` | string | Required; valid HTTP/HTTPS URL |
| `title` | string | Required after create; max 500 characters |
| `description` | string | Optional; max 2000 characters |
| `tags` | string[] | Max 20 tags per bookmark; each tag max 50 characters |
| `created_at` | timestamp | Set on create; immutable |
| `updated_at` | timestamp | Set on create; updated on modify |

## Behaviors

1. **Create Bookmark**  
   Given `url`, optional `title`, `description`, and `tags`, validate the URL, resolve or default `title` (fetch page title if omitted and network allows), persist bookmark with `created_at` and `updated_at`. Return the created bookmark.  
   **Errors:** Invalid URL; duplicate URL for same user; tag count exceeds 20; tag length exceeds 50 characters.

2. **List Bookmarks**  
   Return all bookmarks for the user. Optional filter by tag name (exact match on any assigned tag). Sort by `created_at` descending by default.  
   Return empty list when none exist or filter matches nothing.

3. **Update Bookmark**  
   Given bookmark `id`, allow updating `title`, `description`, `url`, and `tags`. Refresh `updated_at`.  
   **Errors:** Bookmark not found; invalid URL; duplicate URL for same user; tag constraints violated.

4. **Delete Bookmark**  
   Given bookmark `id`, remove the bookmark for the user.  
   **Errors:** Bookmark not found.

5. **Bulk Import**  
   Accept a list of URLs (max 500 per request). For each URL, apply create rules; collect successes and per-item failures without aborting the whole batch. Return summary: `{ imported: number, failed: { url, reason }[] }`.  
   **Errors:** Empty import list; import list exceeds 500 URLs.

## Edge Cases

- Duplicate URL for the same user on create or update (reject with conflict).
- Invalid URL schemes (`javascript:`, missing scheme, malformed host).
- Tag limit: exactly 20 tags allowed; 21st tag rejected.
- Empty tag strings stripped; all-empty tags after strip treated as no tags.
- List with tag filter when no bookmarks have that tag (empty list).
- Bulk import: partial success when some URLs invalid or duplicate.
- Title defaulting when URL validation service times out (see failure modes).

## Failure Modes

- **Storage unavailable:** Operations fail with a storage-level error; no partial writes for single-item CRUD.
- **External URL validation timeout:** On create/update when live URL check is enabled, timeout after 5 seconds; surface `UrlValidationTimeout` and do not persist until retried or validation skipped per product policy.
- **TagService unavailable:** Create/update that require tag normalization fail fast; do not persist bookmark with unvalidated tags.

## Non-Functional Requirements

- Single bookmark CRUD completes in under 200 ms at p95 excluding optional URL title fetch.
- Bulk import processes at least 50 URLs per second for valid URLs (local validation only).

## Interface Dependencies

- **Provides:** `BookmarkManager` interface (see SDK).
- **Depends on:** `TagService` for tag normalization and validation; storage adapter (not specified here).

## Open Questions (Brownfield)

- Legacy code implements **archive** (soft-delete with `archived_at`). Not in product docs. Tracked in `gap-assessment-001.md` for human decision: add to spec or remove from code.
