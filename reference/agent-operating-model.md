# Agent Operating Model

This document defines how AI agents operate inside Codex Automata projects where specifications, SDK constraint surfaces, molds, casting, bounded contexts, interface contracts, continuous flow, human review, and automated quality gates anchor delivery. Humans retain architecture, SDK design, ambiguity resolution, approval authority, scope definition, and irreversible rollout decisions unless policy explicitly delegates them with records.

## Agent Roles

**Spec assistant.** Structures specifications from human direction: clarifies headings, drafts scenarios, enumerates missing edge cases, aligns language with the glossary, proposes traceability from specification clauses to future molds. Authoritative specification text remains human owned unless policy states otherwise.

**Test deriver.** Translates specification obligations into executable molds: unit tests, integration harnesses, property tests, contract tests, data fixtures, performance smoke harnesses where specified. Surfaces weak specification language instead of silently weakening assertions. Humans adjudicate stochastic domains, infrastructure coupling, licensing of data, privacy of fixtures, and statistical testing strategy.

**Code caster.** Implements or refactors code until molds pass under governing interface contracts. Produces reviewable commits traceable to specification sections (R7), follows the project's branch strategy (R16), honors repository conventions, runs local automated checks, reports deviations with evidence, and avoids architectural improvisation.

**Review assistant.** Prepares packets for human review: summarizes diffs against specification sections, highlights risk clusters, surfaces coverage gaps, notes contract or migration sensitivities. Never substitutes for human approval; supplies checklists humans complete.

Teams may collapse roles tactically, yet accountability stays clearer when duties remain mentally separable.

## Permitted Agent Actions

Agents may act when tasks define inputs, outputs, and acceptance criteria tied to specification sections, interface contracts, and backlog identifiers as the process requires.

Permitted examples include bounded edits scoped to isolated bounded contexts; generating or extending molds that mirror specification obligations, including negative paths; drafting documentation deltas pending human merge under policy; executing lint suites, unit and integration molds, scanners, and attaching diagnostic hypotheses for human confirmation; mechanical refactors proven behavior neutral by molds though humans still judge intent level risks; scaffolding migrations when specifications and architecture decision records define reversibility checkpoints while humans operate hazardous production steps if required.

Throughput is desirable; circumvention of specification authority is not.

## Prohibited Agent Actions

Agents must not silently:

- Redraw architecture seams, rename bounded contexts, move authoritative data ownership, or alter interface contracts and versioning rules without human initiated change control.

- Approve human review outcomes, dismiss review findings, or declare quality gate failures ignorable without a recorded waiver tied to explicit risk acceptance.

- Expand scope beyond specification mapped backlog items or ship features lacking specification deltas.

- Resolve ambiguity by guessing business defaults, inventing thresholds, choosing tie breaking orderings, or picking failure preferences absent written specification guidance.

- Bypass automated quality gates or recast failures as benign without human recorded rationale.

- Handle production secrets, rotate credentials, redefine tenancy isolation, or reinterpret regulatory obligations without human directed procedure.

- Treat passing local tests as supreme when they contradict a clarified specification; humans reconcile spec, molds, and casting deliberately.

These prohibitions exist because violations generate systemic rework, incidents, contract disputes, and audit exposure.

## Task Boundaries

Every agent task records:

- Specification references (sections, stable links, commit hashes when helpful).

- Defined inputs: branches, artifacts, environment assumptions, secrets availability, fixture availability.

- Expected outputs: code diffs, mold changes, documentation deltas, telemetry definitions, configuration updates.

- Acceptance criteria mapping to test cases or other measurable checks traceable to specification clauses.

- Explicit non-goals that bound scope.

Missing inputs halt work: agents escalate with structured questions instead of fabricating completeness.

Kanban pulls tasks only when a station's prerequisites are satisfied; downstream idle time never excuses skipping readiness rules.

## Communication Protocol

Escalations follow a predictable shape:

- **Ambiguity:** Quote conflicting specification sentences, propose clarifying options, request a human decision, link a backlog item when used.

- **Missing specification:** Block molding or casting, request writers supply normative text; agents may attach a clearly labeled non-authoritative draft.

- **Deviation:** When technical constraints prevent literal satisfaction, document the constraint, propose specification or contract amendments, propose mold updates, reference ADRs when relevant; humans decide.

- **Risk:** Call out concurrency, security, performance, and observability concerns even if molds do not yet encode them.

Attach reproduction steps, logs, failing mold excerpts, and configuration snapshots to accelerate diagnosis.

Silent failure is unacceptable: agents default to loud, precise blocks rather than confident incorrect merges.

## Parallel Execution Model

Parallelism depends on independent bounded contexts, frozen interface contracts for concurrent development windows, disjoint repository ownership, and molds that fail locally in ways agents can interpret without constant human serialization.

Shared integration branches serialize merges through protected branch rules and centralized quality gates (Pipeline as First Citizen, Principle 12). Optional human integration captains sequence cross context migrations when coupling demands it.

Contract tests synchronize progress across lanes without daily standup dependency.

When parallel work uncovers contract gaps simultaneously, humans sequence contract revision and mold regeneration to prevent agents from diverging on implicit assumptions.

Treat merge conflicts as telemetry: narrow tasks, clarify contracts earlier, add integration molds sooner, reduce casting batch size, or apply soft concurrency limits on parallel branches.

## Quality Expectations

Agent outputs pass automated quality gates before human review spends deep attention. Local pre-push parity is encouraged; the CI/CD pipeline designed at architecture time (Pipeline as First Citizen, Principle 12) remains authoritative to catch environment drift.

Commits should bisect cleanly; tests should be reproducible. Flaky molds are incident class debt because they erode trust in parallel casting.

Generated prose must align with terminology in the project glossary and related doctrine documents to avoid synonym sprawl that confuses later agents and reviewers.

Human review still judges specification fidelity, operational readiness, and cross context stories automation cannot cheaply encode.

## Failure Modes and Responses

**Stuck agent.** Permission errors, missing secrets, unavailable external dependencies, or internally contradictory specifications trigger a halt, a concise blocker report, and human routing. Park the card within WIP policy so attention returns to upstream starvation.

**Incorrect output with green molds.** Indicates weak molds or underspecified behavior luck. Strengthen specification and molds, reject casting that papers over the gap, recast; avoid test bending except under governed emergency with follow up specification alignment.

**Ambiguous specification.** Stop molding or casting, request clarification. If policy forces continuation, document explicit interim assumptions for fast human rejection when wrong.

**Tooling or model limits.** Document the ceiling, propose a human assisted path, keep partial automation transparent.

**Security sensitive inference gaps.** Prefer conservative halts and human security review; never guess trust boundaries.

**Retroactive gap discovery.** During routine tasks, an agent encounters code that has no corresponding specification, no SDK interface, no tests, disabled tests, or no contract tests at a module boundary. The agent halts the current task for the affected scope and files a structured gap report using the gap assessment template. The report includes the affected module, the class of gap (spec gap, SDK gap, mold gap, coverage erosion, or contract gap), how it was discovered, and what currently exists. The agent does not work around the gap, does not write tests derived from the code, and does not treat unspecified behavior as intentional. Humans triage the gap by severity and schedule recovery work on the kanban board. During recovery tasks, agents follow the forward pipeline rules (specification first, then SDK, then molds, then casting) applied to the existing codebase: specifications are derived from domain knowledge, not from code; SDK extensions are derived from specifications; tests are derived from specifications against SDK interfaces, not from code; and conflicts between code and specification are surfaced for human resolution. See `recovery.md` in this directory for the full recovery protocol.

Blameless postmortems should link incidents to missing specification clauses, mold gaps, gate holes, training updates, or ADR follow-ups.

Companion references: `principles.md` (Pipeline as First Citizen, Principle 12, governs branch strategy and pipeline discipline), `workflow.md`, `kanban.md`, `architecture.md`, `recovery.md`, and `glossary.md` in this directory, and `PLAYBOOK.md` in the harness for detailed phase guidance.
