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

## Pipeline Design as Architectural Concern

Pipeline as First Citizen (Principle 12) elevates CI/CD pipeline design to an architecture-time decision. During Phase 1, the architecture specification should document:

- **Branch strategy.** How branches are named, how merges are ordered, what protections apply to shared branches, and how multi-agent parallel execution coordinates through sequential merges or integration branches.
- **Pipeline stages.** Which quality gates run at which points (push, pull request, merge to main, release tag), and how they map to the project's mold, contract, and policy requirements.
- **Deployment strategy.** Progressive delivery approach (canary, blue-green, feature flags), rollback automation, and how deployment cadence aligns with bounded context independence.
- **Pipeline configuration ownership.** Pipeline configuration files live in version control alongside application code and follow the same specification-first flow. Changes to pipeline configuration are architecture events that require review and traceability.

Pipeline tooling decisions (CI platform, container registry, artifact storage, deployment targets) benefit from the same structured research (Principle 4) applied to application technology choices. Record these decisions in ADRs.

## Anti-Patterns

**Monolithic specifications.** Single giant documents obscure ownership, delay molding, inflate review entropy, collide parallel agents. Split along bounded contexts and cross cutting appendices referencing authoritative sections.

**Tightly coupled modules.** Shared mutable globals, shotgun surgery across unrelated packages, covert RPC fan out, cyclic imports, leaky ORM mappings across aggregates, transactional spans that stitch unrelated aggregates, undeclared saga couplings breaking compensation discipline.

**Implicit interfaces.** Side channels through logging fields, undocumented environment variables coupling microservices behavior, undocumented cache keys coupling invalidation choreography, tacit reliance on operational ordering in deployment scripts, undocumented idempotency requirements, undocumented ordering dependence in message consumers, undocumented partial failure amplification.

**Bypassing specification for convenience.** Shortcutting ambiguity resolution by encoding truth only in molds or casts causes drift between human governance and artifacts agents optimize.

Each anti-pattern lengthens cycle time through rework and weakens mechanical quality gates that assume explicit contracts.

## Design Identity in the Constraint Surface

For projects with user-facing surfaces, the SDK constraint surface extends beyond types and interfaces to include design tokens and identity vocabulary. The design identity document feeds into the SDK the same way the system specification feeds into it: identity decisions are translated into importable, enforceable building blocks.

**Design tokens as SDK building blocks.** Colors, typography sizes, spacing values, shadows, border radii, and motion timing become named tokens in the constraint surface. Agents reference tokens, not raw values. If a casting contains a hardcoded hex color, pixel value, or font-family declaration that does not trace to a token, it is a constraint surface violation, the same category as inventing an ad hoc type outside the SDK.

**Pattern catalogs.** The design identity document defines explicitly permitted and banned patterns for the project. Permitted patterns are the compositional primitives agents may use for layout, navigation, component structure, and interaction. Banned patterns are slop fingerprints: known AI-default patterns that the project must not exhibit. The catalog is project-specific because different products have different identity requirements.

**Naming registries.** Module names, route names, API endpoint names, and user-facing terminology follow project-specific conventions defined in the design identity document. Generic names like `utils`, `helpers`, `service`, and `handler` are banned unless the design identity explicitly permits them. The naming registry is part of the SDK vocabulary the same way type names are.

**Copy voice guides.** Tone, vocabulary constraints, banned phrases, error message style, and CTA patterns are documented in the design identity and enforced during casting and review. Agents do not invent copy. They compose within the voice guide's vocabulary.

**Divergence gates in CI/CD.** Quality gates check castings for slop fingerprints cataloged in the design identity. Divergence detection runs alongside mold execution and contract checks. Fingerprint matching is objective and measurable: does the casting use a banned font, a default color value, a cataloged boilerplate layout, a banned copy phrase? Flagged matches require human review. The gate does not judge aesthetics. It detects convergence.

## Repository Templates

When bootstrapping or extending documentation, reuse the canonical templates shipped with projects using Codex Automata:

- `templates/architecture-decision-record.md`: capture reversible decisions affecting boundaries, storage, cryptography, interoperability, rollout, tenancy, and operational sovereignty.

- `templates/module-boundary-template.md`: state scope, invariants, authoritative data ownership, ingress and egress dependencies, molding layout, onboarding notes for casting agents, operators, reviewers.

- `templates/interface-contract-template.md`: articulate versioned schemas, behavioral obligations, temporal guarantees, error taxonomy, quotas, observability facets, compatibility promises, SLA relevant commitments, deprecation windows tied to rollout policy.

- `templates/design-identity-template.md`: define aesthetic direction, typography system, color system, spatial system, motion philosophy, copy voice, naming conventions, anti-patterns, reference targets, and slop fingerprints for projects with user-facing surfaces.

Adapt fields to project policy without diluting contractual clarity across contexts.
