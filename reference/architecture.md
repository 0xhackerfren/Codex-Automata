# Architecture Patterns

Architecture in Codex Automata exists to create stable seams: bounded contexts separated by explicit interface contracts, molds aligned to responsibilities, and casting work that can execute in parallel without hidden coupling. Humans own architectural decisions; specifications and ADRs make those decisions legible to agents, reviewers, and quality gates.

## Identifying Bounded Contexts from a Domain

Start from language, not from folders. When two subsystems use the same word with different invariants, lifecycle rules, ownership, or reconciliation logic, you usually have a boundary candidate. Look for natural transaction boundaries, authoritative data owners, distinct failure domains, independent deployment cadence, regulatory isolation, or teams with irreconcilable vocabularies without translation.

Prefer contexts that encapsulate cohesive behavior with a crisp external promise. Boundaries trade local simplicity for coordination overhead: excessive fragmentation multiplies molds and governance; oversized contexts hide coupling and collide parallel agent execution. Iterate with thin vertical slices anchored to observable outcomes in the intake document.

Document candidate boundaries alongside open questions deliberately deferred from specification until slicing stabilizes unresolved risks.

## Interface Contract Design Principles

An interface contract is the formal handshake between bounded contexts: API shapes, schemas, versioning rules, sequencing guarantees, concurrency semantics, idempotency keys, timeouts, backoff and quota expectations, pagination, deprecation windows, compatibility matrices, failure models, telemetry correlation conventions, authentication and authorization scopes, auditing expectations, confidentiality constraints, throughput and latency envelopes, load shedding semantics, deterministic behaviors where promised, caching semantics plus invalidation and coherence rules, replay policies, cross environment compatibility statements, rollout coupling expectations.

Keep contracts minimal: expose the smallest durable surface compatible with foreseeable evolution. Stability beats convenience at boundaries: callers should not infer hidden state from undocumented fields. Prefer explicit evolution (version bumps, additive changes, deprecation schedules) rather than implicitly coupled rollouts across contexts.

Version intentionally. Maintain compatibility tests or consumer driven molds at the boundary. Treat breaking changes as architecture events recorded in architecture decision records and reflected in phased migrations.

## Dependency Management Across Modules

Forbid circular dependencies among bounded contexts at the logical dependency graph layer. Prefer acyclic layering or explicit dependency inversion via narrow ports and adapters only when the domain demands it. Dependencies must reference published interface contracts, not transitive internals of another context.

Shared libraries are allowed when they carry no domain invariants that belong inside a single context. When shared code begins smuggling domain logic, split or duplicate judiciously rather than creating a latent monolith. Cross cutting concerns (observability, identity parsing, transport) remain infrastructure level unless they redefine domain truths.

Govern dependency growth with architecture reviews when new edges appear outside established patterns.

## Parallel Agent Execution Behind Module Boundaries

Parallelism requires independence: disjoint file ownership, disjoint molds, deterministic merges, predictable conflict surfaces at contract seams. Assign agent tasks keyed to bounded context slices anchored to backlog items with frozen contracts for the slicing window.

When two tasks must coordinate, isolate shared work explicitly: provisional contract stubs, façade modules, spike branches that never merge alone, synchronous human integration checkpoints, sequencing policies for ordering dependent migrations across databases or topics.

Treat merge contention as telemetry: recurrent collisions signal underspecified boundaries, overly broad tasks, unstable contracts, or missing integration molds.

## Architecture Decision Records (ADRs)

ADRs encode the motivating context, the decision taken, credible alternatives discarded, downstream consequences for molds and casts, reversible versus irreversible commitments, rollout coupling, deprecation posture, linkage to superseding decisions, owning role, explicit status transitions (proposed, accepted, superseded), and staleness cues so readers know when doctrine drifted without a superseding ADR.

They matter because agents and reviewers inherit assumptions across time without oral tradition. Agents should not forge architecture silently; humans record tradeoffs explicitly so molds and implementations align with reversible paths.

Use ADRs when changing bounded context seams, persistence technology, interoperability guarantees, cryptographic posture, tenancy and isolation posture, rollout constraints, irreversible migrations, throughput or sovereignty assumptions, or observability correlation contracts anchored to incidents.

Record status (proposed, accepted, superseded) and cite affected specifications.

## Anti-Patterns

**Monolithic specifications.** Single giant documents obscure ownership, delay molding, inflate review entropy, collide parallel agents. Split along bounded contexts and cross cutting appendices referencing authoritative sections.

**Tightly coupled modules.** Shared mutable globals, shotgun surgery across unrelated packages, covert RPC fan out, cyclic imports, leaky ORM mappings across aggregates, transactional spans that stitch unrelated aggregates, undeclared saga couplings breaking compensation discipline.

**Implicit interfaces.** Side channels through logging fields, undocumented environment variables coupling microservices behavior, undocumented cache keys coupling invalidation choreography, tacit reliance on operational ordering in deployment scripts, undocumented idempotency requirements, undocumented ordering dependence in message consumers, undocumented partial failure amplification.

**Bypassing specification for convenience.** Shortcutting ambiguity resolution by encoding truth only in molds or casts causes drift between human governance and artifacts agents optimize.

Each anti-pattern lengthens cycle time through rework and weakens mechanical quality gates that assume explicit contracts.

## Repository Templates

When bootstrapping or extending documentation, reuse the canonical templates shipped with projects using Codex Automata:

- `templates/architecture-decision-record.md`: capture reversible decisions affecting boundaries, storage, cryptography, interoperability, rollout, tenancy, and operational sovereignty.

- `templates/module-boundary-template.md`: state scope, invariants, authoritative data ownership, ingress and egress dependencies, molding layout, onboarding notes for casting agents, operators, reviewers.

- `templates/interface-contract-template.md`: articulate versioned schemas, behavioral obligations, temporal guarantees, error taxonomy, quotas, observability facets, compatibility promises, SLA relevant commitments, deprecation windows tied to rollout policy.

Adapt fields to project policy without diluting contractual clarity across contexts.
