# End-to-End Workflow

This reference describes the Codex Automata flow from earliest intent through production observability. It ties together bounded contexts, interface contracts, agent tasks, molds, casting, human review, and quality gates. For phase-by-phase agent behavior, constraints, and checklists, see `PLAYBOOK.md` at the repository root.

## 1. Idea Intake

An intake document captures the motivating problem, user outcomes, measurable signals, constraints, non goals, stakeholders, timelines, regulatory or security sensitivities, and known unknowns. The intake is deliberately not a specification: it aligns humans on direction before decomposition and commitment.

Outputs: a prioritized problem statement linked to backlog items sized for architectural discussion.

## 2. Architectural Decomposition (Human Owned)

Humans propose bounded contexts, candidate module boundaries, data ownership, transactional seams, synchronous versus asynchronous integrations, versioning policies, anticipated failure domains, operational ownership, and initial interface contract sketches.

Outputs: architecture notes, provisional interface contracts referencing `templates/interface-contract-template.md`, and backlog slices aligned to contexts.

## 3. Specification Authoring Per Context

For each bounded context (and cross-cutting concern), humans write specifications that enumerate behaviors, invariants, non functional targets, telemetry expectations, rollback attitudes, migrations, observability probes, adversarial assumptions, compatibility promises, error contracts, idempotency, and explicit open questions tied to backlog items never silently resolved inside agents.

Specifications are falsifiable artifacts: every normative clause should map forward to molds and backward to rationale in review.

Outputs: authoritative specifications stamped with versioning or change metadata where the project mandates it.

## 4. Test Molding (Agent Task or Human Driven)

Specifications drive test planning: equivalence partitions, boundary values, concurrency cases, fuzz targets, compatibility matrices, regression harnesses mirroring defects, snapshot policies, and deterministic fixtures. Executable molds implement those plans strictly.

Agents may synthesize scaffolding; humans adjudicate nondeterministic domains, flaky infrastructure, ambiguous ordering, statistical tests, timing windows, external systems, licensing and privacy of fixtures, performance budgets, security cases, compliance evidence, migration and dual write strategies, rollout toggles that interact with molds, and distributed behaviors (retries, backoff, jitter, timeouts, quotas, partial failure, transactional outbox patterns, saga compensation) where they apply.

Outputs: committed molds that fail when behavior regresses absent an intentional specification change.

## 5. Code Casting With Parallel Agents

With frozen interface contracts within the slicing window for a change, casting agents produce implementation constrained by molds across independent contexts concurrently. Conflict surfaces only at merges or contract checkpoints; branch policies and quality gates arbitrate merges.

Agents perform bounded edits, scaffolding, and refactors that respect interface contracts, keep builds and tests deterministic, and control randomness and time through explicit test doubles or harnesses where needed.

Outputs: feature branches meeting local mold execution and static analysis policies.

## 6. Human Review

Reviewers evaluate casting against specification and intent even when tests pass: security assumptions, secret handling, failure clarity for operators, rollout and rollback behavior, graceful degradation, misuse resistance, logging and telemetry quality (including cardinality discipline), compatibility across environments, and whether tests meaningfully lock the specified behavior rather than coincidentally matching it.

Unresolved mismatches escalate to revised specifications or contracts before weakening molds or bypassing gates.

Outputs: approvals, rework instructions referencing spec clauses, backlog follow ups for ambiguity removal.

## 7. Integration and CI/CD Gates

Merged changes proceed through centralized quality gates that bundle mold execution, static analysis, supply chain and license checks, signing and provenance where required, contract tests across bounded contexts, integration smoke suites, performance and reliability budgets tied to SLOs, schema and API compatibility checks for migrations, progressive delivery controls (feature flags, canaries, rollbacks), and operational readiness checks (alert routes, runbooks, synthetic monitors) appropriate to the system class.

Outputs: immutable artifacts destined for deployment with provenance appropriate to organizational policy.

## 8. Deployment and Observation

Deploy using agreed progressive strategies. Observability verifies golden signals correlated with intake metrics. Incident learning updates specifications rather than patching undocumented behavior indefinitely.

Operational feedback informs architecture decision records capturing tradeoffs and reversibility.

Outputs: dashboards, curated log queries, trace exemplars, post incident updates, specification amendments, contract revisions, mold extensions, defensive casting hardening when genuinely required.

## Text Flow Diagram

```text
Intake
  |
  v
Architecture (bounded contexts, interface contracts)
  |
  v
Spec Writing  <-------------------------+
  |                                     |
  v                                     |
Test Molding                            |
  |                                     |
  v                                     |
Code Casting (parallel agent tasks)     |
  |                                     |
  v                                     |
Human Review ---------------------------+
  |
  | (approve)
  v
CI/CD Quality Gates (molds + policy)
  |
  v
Deploy / Observe ----------------------> feedback to Spec / Contracts / Architecture (ADRs)
```

## Feedback Loops

**Review rejects casting.** Typical causes include intent drift, brittle coverage, covert coupling, leaky abstractions crossing contexts, latent security constraints, rollout hazards, ambiguity masquerading as implementation freedom. Rework routing: revise specification or contracts when the rejection reveals a latent requirement; regenerate or extend molds accordingly; resume casting rather than patching through review comments alone.

**Deployment or production signals contradict intent.** Incident or SLO regressions propagate upstream: formulate a corrective specification delta, enlarge molds guarding the failure class, revisit architecture if boundaries mis sliced the causal domain. Architecture decision records codify reversible choices so future casts do not reintroduce revoked assumptions.

Avoid bypass loops where pressure forces gate weakening without specification amendment; that forfeits Mechanical Discipline emphasized in Codex Automata doctrine.

## Kanban Stations Alignment

Operational tracking mirrors stations:

| Station | Responsibility | Typical Owner |
|---------|----------------|---------------|
| Spec Writing | Authoritative specifications per context | Human |
| Test Molding | Derive molds and fixtures from specs | Agent with human adjudication |
| Code Casting | Implement to satisfy molds within contracts | Agent |
| Human Review | Confirm casting matches specification and systemic risk posture | Human |
| Deployment | Progressive release and verification | Humans with automation gates |

Treat integration testing and CI/CD quality gates either as implicit sub stages within molding and pre deployment review lanes or explicit columns when WIP instrumentation demands finer grain. Naming remains consistent across boards: Specification, molds, casting, review, gates, rollout, observation tie back to the same vocabulary referenced in dashboards and retrospective notes.

Consult `PLAYBOOK.md` when expanding any station into granular agent operating instructions, escalation patterns, tooling responsibilities, branching strategies, backlog hygiene, and risk aware batch sizing.

## Companion Documents

For pull policies, limits, bottleneck interpretation, Toyota Production System parallels, metric guidance, consult `docs/kanban.md`. For vocabulary alignment across teams, consult `docs/glossary.md`.
