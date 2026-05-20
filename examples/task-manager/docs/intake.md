# Project Intake: Task Manager

<!--
Filled example for Phase 0 (Idea Intake). This document constrained architecture, specifications, and adoption profile for the worked example.
-->

## Metadata

| Field | Value |
|-------|-------|
| Project name | Task Manager |
| Date | 2026-05-01 |
| Profile | Essential (solo developer example, spec + tests + code pipeline) |

## Problem Statement

Need a simple task management module for creating, tracking, and completing tasks.

## Goal

Deliver a TaskManager module with CRUD operations, pluggable storage, and clear interface contracts for future integration.

## Target Users

Developers integrating task management into their applications.

## Constraints

- Single-user usage; no authentication or multi-tenant support in the initial scope.
- In-memory storage for the first implementation.
- Storage backends must remain pluggable via interface abstraction (no hard-coded persistence inside TaskManager).

## Success Criteria

1. **Specified behaviors pass tests:** All behaviors documented in the specification are covered by the test plan and pass when casting is complete.
2. **Interface contracts frozen and verified:** TaskManager and Storage contracts are defined before casting and honored by implementations.
3. **Pluggable storage:** Persistence is supplied through the Storage interface; TaskManager does not depend on a concrete storage implementation.

## Bounded Contexts

| Context | Notes |
|---------|-------|
| TaskManagement | Single bounded context for the entire module (create, list, complete, delete, persistence boundary). |

## Open Questions

None remaining. Questions about storage abstraction and ID strategy were resolved during architecture (see `docs/architecture.md` ADR-001 and ADR-002).
