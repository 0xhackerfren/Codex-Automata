# Gap Assessment: BookmarkManager — Archive Feature

<!--
Spec gap discovered during brownfield verify: legacy code exposes POST /bookmarks/:id/archive
with no product documentation. Recovery pipeline in action.
-->

## Metadata

| Field | Value |
|-------|-------|
| Module name | BookmarkManager |
| Assessed by | Platform team |
| Date discovered | 2026-05-20 |
| Severity | Significant |
| Status | Open |

## Gap Classification

- [x] **Spec gap:** behavior exists in code but is not documented in any specification.
- [ ] **Mold gap:** behavior is documented in the specification but has no tests, or tests are too weak.
- [ ] **Coverage erosion:** tests existed but were deleted, disabled, or made flaky without remediation.
- [ ] **Contract gap:** a module boundary has no contract tests despite a defined interface contract.
- [ ] **SDK gap:** behavior exists in code but has no corresponding types or interfaces in the SDK constraint surface.

## Discovery Trigger

- [ ] Production incident
- [ ] Review finding
- [ ] Coverage audit
- [x] Team walkthrough
- [ ] Dependency upgrade
- [ ] Security scan
- [x] Agent-detected during routine task
- [ ] Other: [ ]

During Step 4 (verify) of brownfield onboarding, an agent scanning `src/routes/bookmarks.js` found `archiveBookmark` handler setting `archived_at` without a corresponding section in `docs/spec-bookmark-manager.md`. Product owner confirmed the feature is not in current docs or roadmap slides.

## Current State

- **Specification:** `docs/spec-bookmark-manager.md` covers CRUD and bulk import only; no archive or soft-delete behavior.
- **Tests:** `bookmark-crud.test.js` does not mention archive; no mold cases.
- **Code:** `POST /api/bookmarks/:id/archive` sets `archived_at`, excludes row from default list queries; `POST .../unarchive` clears field (also undocumented).
- **Contract tests:** N/A for archive; TagService contract not yet written.

## Required State

- **Specification should cover:** If archive is intended: soft-delete semantics, list/filter behavior, whether delete is hard or soft, unarchive, retention. If not intended: spec should state hard-delete only and archive routes are deprecated.
- **Tests should cover:** Archive/unarchive flows traced to spec section, or routes removed after recast.
- **Implementation changes (if any):** Either add `archiveBookmark` / `unarchiveBookmark` to SDK and implementation per spec, or remove routes and migrate data.

## Recovery Plan

1. **Spec patch:** Human decision meeting scheduled — product owner + tech lead. Options: (A) add Archive/Unarchive behaviors to spec, (B) deprecate and remove code in recast.
2. **SDK patch:** If (A), add `archived_at` optional field and `archiveBookmark` / `unarchiveBookmark` to `BookmarkManager` interface.
3. **Mold patch:** Derive tests from chosen spec sections; exclude archive from test plan until spec patch merges.
4. **Recast (if needed):** If (B), remove handlers and migration script for `archived_at` column; if (A), align list filters with spec.
5. **Re-review:** Reviewer confirms spec, SDK, tests, and code agree on archive semantics.

**Estimated effort:** 1–2 days after product decision

**Assigned to:** Tech lead (pending decision)

## Recurrence Prevention

- **Root cause:** Feature shipped via emergency PR without intake or spec; brownfield audit did not list undocumented routes.
- **Process change:** Add “route inventory vs spec” check to brownfield verify step; PR template requires spec section link for new endpoints.

## Resolution

| Field | Value |
|-------|-------|
| Date closed | — |
| Reviewed by | — |
| Spec patch commit/PR | — |
| SDK patch commit/PR | — |
| Mold patch commit/PR | — |
| Recast commit/PR | — |
| Review approval | — |
