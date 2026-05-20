# Brownfield Audit: Bookmarks API

<!--
Filled example for examples/brownfield-api. See reference/brownfield-onboarding.md for the full protocol.
-->

## Metadata

| Field | Value |
|-------|-------|
| Project name | Bookmarks API |
| Audited by | Platform team |
| Date | 2026-05-20 |
| Codebase age | ~3 years |
| Estimated module count | 3 |
| Current test coverage | ~45% (happy paths only) |
| Current CI/CD | GitHub Actions: lint, unit tests on PR; deploy main to staging |

## Module Inventory

| Module | Bounded Context | Risk Level | Change Frequency | Test Coverage | Spec Exists | SDK Exists | Priority |
|--------|----------------|------------|-----------------|---------------|-------------|------------|----------|
| BookmarkManager | Bookmarks | Critical | Daily | ~50% | No | No | 1 |
| TagService | Bookmarks | High | Weekly | ~40% | No | No | 2 |
| SearchIndex | Search | Medium | Monthly | ~30% | No | No | 3 |

### Risk Level Criteria

- **Critical:** Production-facing, revenue-impacting, handles sensitive data, or has caused incidents
- **High:** Production-facing, frequently changed, or has complex business logic
- **Medium:** Internal tooling, moderately changed, or straightforward logic
- **Low:** Rarely changed, well-understood, or scheduled for replacement

### Priority Ranking Logic

Priority = Risk Level x Change Frequency. Critical modules that change frequently are onboarded first. Low-risk, rarely-changed modules are onboarded last (or not at all if scheduled for replacement).

## Dependency Map

| Module | Depends On | Depended On By |
|--------|-----------|---------------|
| BookmarkManager | TagService (tag assignment) | SearchIndex (index updates) |
| TagService | — | BookmarkManager |
| SearchIndex | BookmarkManager (bookmark documents) | — |

Onboarding order: BookmarkManager first (highest priority), then TagService (dependency of BookmarkManager), then SearchIndex.

## Gap Summary

| Gap Type | Count | Notes |
|----------|-------|-------|
| Spec gaps (code without spec) | 3 | All modules lack formal specifications |
| Mold gaps (spec without tests) | 2 | TagService and SearchIndex tests do not trace to behavior |
| SDK gaps (code without SDK types) | 3 | Ad hoc types in route handlers |
| Contract gaps (boundaries without contract tests) | 1 | BookmarkManager ↔ TagService boundary |
| Coverage erosion (tests lost over time) | 0 | No known deleted suites |

## Existing Assets to Preserve

- **Existing tests worth keeping:** `bookmark-crud.test.js` create/list/update/delete happy paths—align to spec after BookmarkManager spec is written
- **Existing documentation:** OpenAPI stub in `openapi.yaml` (stale; use for gap discovery only, not as spec source)
- **Existing CI/CD gates:** ESLint, Jest on PR—extend with "spec file required for touched onboarded paths" after Phase 1

## Onboarding Plan

### Phase 1: First Module (Week 1-2)

**Target module:** BookmarkManager
**Profile:** Essential
**Steps:**
1. [x] Write specification from domain knowledge (`docs/spec-bookmark-manager.md`)
2. [x] Derive tests from specification (`tests/test-plan.md`)
3. [ ] Verify existing implementation against new tests
4. [ ] File gap assessments for any failures (see `gap-assessment-001.md` — archive feature)
5. [ ] Recast if needed (archive: spec decision pending)

### Phase 2: Adjacent Modules (Week 3-6)

**Target modules:** TagService, then SearchIndex
**Profile upgrade:** Standard (after BookmarkManager verify completes)
**Steps:**
1. [ ] Repeat recovery process for each module
2. [ ] Extract SDK types for shared interfaces (`sdk/types.ts` extended)
3. [ ] Define interface contracts between BookmarkManager and TagService
4. [ ] Establish quality gates for new PRs (spec + tests for new routes)

### Phase 3: Expansion (Month 2+)

**Target:** Remaining medium-priority paths, operational hardening
**Profile upgrade:** Standard
**Steps:**
1. [ ] Continue recovery-based onboarding for SearchIndex
2. [ ] Implement context persistence (`context-state.md`)
3. [ ] Activate SDK and contract quality gates on onboarded paths

## CI/CD Integration Plan

| Gate | When to Activate | Scope |
|------|-----------------|-------|
| Spec required for new modules/routes | Immediately | New PRs only |
| Tests required for new behavior | Immediately | New PRs only |
| Spec + test plan for `src/bookmarks/**` | After Phase 1 verify | Onboarded BookmarkManager paths |
| SDK interface check (TypeScript) | After Standard upgrade | `sdk/` and module boundaries |
| Contract tests BookmarkManager ↔ TagService | After Phase 2 | Integration test job |
