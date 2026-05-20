# Brownfield API Example (Codex Automata)

## What This Is

A worked example of **brownfield adoption**: applying Codex Automata to a pre-existing Express.js REST API for a bookmarks service. The hypothetical codebase shipped without specifications, with partial tests, and no SDK constraint surface. This example shows how to inventory, prioritize, and onboard retroactively—not how to build greenfield from intake forward.

Compare with `examples/task-manager/`, which demonstrates the forward pipeline on a new module.

## Pretend Legacy State

Before adoption, the bookmarks service had:

- Three modules: **BookmarkManager**, **TagService**, **SearchIndex**
- Express routes and handlers with tribal knowledge
- Jest tests covering happy paths only (no spec traceability)
- No `docs/spec-*.md`, no `sdk/types.ts` aligned to domain intent
- An undocumented **archive** feature in BookmarkManager (discovered during recovery)

No runnable application code ships in this repository. Artifacts show the methodology layer only.

## What The Example Demonstrates

1. **Brownfield audit** (`audit.md`) — inventory, risk classification, gap summary, phased onboarding plan
2. **Recovery as onboarding** — specification written from domain knowledge for BookmarkManager first
3. **SDK from spec** (`sdk/types.ts`) — types extracted from the spec, not scraped from legacy code
4. **Test mold** (`tests/test-plan.md`) — cases derived from specification behaviors
5. **Gap assessment** (`gap-assessment-001.md`) — spec gap for the archive feature found during verify

## Directory Structure

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Nested agent instructions (reference only; do not modify) |
| `README.md` | This overview |
| `audit.md` | Filled brownfield audit for the bookmarks API |
| `docs/spec-bookmark-manager.md` | Retroactive specification for BookmarkManager (Phase 1 onboard) |
| `sdk/types.ts` | SDK constraint surface from spec |
| `tests/test-plan.md` | Test plan derived from spec |
| `gap-assessment-001.md` | Spec gap: archive behavior in code, not in spec |

## Suggested Reading Order

1. `audit.md` — understand priority and gaps
2. `docs/spec-bookmark-manager.md` — intended behavior (domain-driven)
3. `sdk/types.ts` — constraint surface
4. `tests/test-plan.md` — mold
5. `gap-assessment-001.md` — recovery in action

## Adopting On Your Own Brownfield Project

1. Run `scripts/init.ps1` or `init.sh` into your existing repo.
2. Copy and fill `harness/templates/brownfield-audit-template.md`.
3. Follow `reference/brownfield-onboarding.md` and use `/brownfield-onboarding` in Cursor.
4. Onboard the highest-priority module with Essential profile and the recovery protocol.
