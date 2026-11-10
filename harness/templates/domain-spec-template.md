# Domain specification: [name]

## Metadata

Task ID, owner, baseline Git revision, methodology version, task risk, review gate.

## Problem statement

Observable domain problem, affected actors, outcome, scope and exclusions.

## Research summary and decision

Observed current state with sources/revisions. Enumerate alternatives, tradeoffs,
chosen decision and rationale. Separate observations, assumptions and unknowns.

## Numbered rules

R1: [Inputs, preconditions, postconditions, errors, boundaries and invariant.]
R2: [Authorization/protected case and explicit failure behavior.]
R3: [Ambiguity, missing prerequisites, retry/stop and recovery behavior.]

## Scenario traces (mold basis)

Given exact initial state, enumerate actions and expected observations. Include
positive, protected and ambiguous cases; avoid describing implementation internals.

## Paper fixture

Enumerate exact input records and expected output records, IDs, counts, revisions,
provenance references, content digests, order and restart state. Validate these
assumptions against the real SDK/TCK before freezing behavioral molds.

## Compatibility, migration and rollback

Contract versions, affected consumers, authorized deltas and safe recovery steps.

## Open questions

Explicit unresolved decisions, recommended answer, evidence needed and blocking
status. No question disappears silently into implementation.

## Handoff

Downstream contract, static/fixture validation, behavioral mold and casting task
IDs (local IDs accepted), dependency order, artifact paths and completion gates.

| Mold name | Spec basis | Class (positive/protected/ambiguous) |
| --- | --- | --- |
| [name] | [R1] | [class] |
