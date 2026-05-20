# Core Principles

This document defines the ten foundational principles of Codex Automata. Together they constrain how research, specification, SDK, local-first design, molds, casting, bounded contexts, flow, identity, agents, humans, interface contracts, and quality gates interact throughout the lifecycle of a software system.

## 1. Specification First

**Summary.** The specification is the primary engineering artifact; every downstream artifact is derived from or checked against it.

**Explanation.** Specification First means that authoritative intent lives in prose and structured constraints that humans can deliberate over before implementation exists. Requirements are not reconstructed from tests or code alone: tests encode acceptance, but specifications explain invariants, edge cases, failure modes, rationale, and the boundaries between modules. Without a crisp specification, agent tasks lack a stable compass, reviewers lack a definitive comparison target, and quality gates degrade into brittle pattern matching instead of conformance checks.

Operational discipline follows from this artifact hierarchy. Humans invest attention in specs because they amortize ambiguity across molding, casting, and review cycles. Specifications should be falsifiable enough to drive molds (tests) yet rich enough that human reviewers can distinguish correct behavior from plausible but incorrect implementations. Traceability flows one way in authority (spec leads), while feedback from production and review can still refine the spec when evidence demands it.

**Connections.** Specification First supplies the raw material for SDK as Constraint Surface: you cannot define building blocks without knowing what the system must do. It feeds Tests as Molds indirectly through the SDK. It defines the obligations that Code as Casting must satisfy. It sets the vocabulary and rules for Modularity and Bounded Contexts (what each context must guarantee at its boundary). It gives Continuous Flow a defined unit of work that can move between stations. Finally, it underpins Quality Gates: automated checks compare castings and molds to published specifications and interface contracts, not to informal chat history.

## 2. SDK as Constraint Surface

**Summary.** The SDK defines the programmatic boundary that all molds and castings must operate within; it is the enforceable, compilable expression of architectural decisions.

**Explanation.** SDK as Constraint Surface means that architectural intent is rendered as importable code (types, interfaces, extension points, compositional primitives) before tests or implementation exist. The SDK is not a utility library. It is the grammar that downstream work must speak. When agents write tests, they assert against SDK interfaces. When agents write implementation, they implement SDK contracts. The type system mechanically prevents drift outside the constraint surface without instruction or discipline.

This principle exists because constraint is the primary control mechanism for AI code generation. You do not control an agent by telling it what to do. You control it by defining what it is allowed to do. The SDK is that definition. It forces a level-up in abstraction: you cannot design an SDK for a tangled monolith. The very act of defining composable building blocks requires clean decomposition, consistent error models, and explicit extension points. Modularity becomes structural rather than aspirational.

The SDK grows incrementally. As the application demands new capabilities that the initial surface does not provide, the response is to return to the specification, define the new capability, and extend the SDK. Extension follows the pipeline. You cannot add a building block without updating the spec that justifies it. This keeps the constraint surface intentional rather than emergent.

**Connections.** The SDK derives directly from Specification First: specs define what the system must do, and the SDK expresses the vocabulary available to do it. Tests as Molds are written against SDK interfaces, ensuring molds cannot reference abstractions outside the constraint surface. Code as Casting implements SDK contracts, meaning implementation is bounded by the SDK's type system. Modularity and Bounded Contexts map to SDK modules: each context's public surface is an SDK package. Continuous Flow gains a station (SDK Design) between Spec Writing and Test Molding. Quality Gates verify that castings import only from the published SDK surface and that no out-of-band abstractions bypass the constraint.

## 3. Local-First

**Summary.** Systems are designed to function on the smallest viable model first, then expanded to frontier models as capability demands; constraint forces engineering discipline that benefits every model tier.

**Explanation.** Local-First means that the architecture, prompts, context management, task decomposition, and error handling of an AI-driven system are designed against the constraints of small, local models before any frontier model is assumed. A local model has a limited context window, weaker reasoning, less tolerance for ambiguity, and no room for bloated instructions. A system that functions within these constraints has necessarily solved problems that systems built for frontier models defer indefinitely: precise context retrieval, minimal and structured prompts, atomic task decomposition, output validation, and graceful degradation on partial completions.

The expansion path runs from constrained to powerful, never the reverse. Once the system works on a small model with tight specifications, sharp SDK boundaries, and well-decomposed tasks, moving to a larger model relaxes constraints incrementally: larger context windows reduce retrieval pressure, stronger reasoning tolerates slightly looser instructions, faster inference allows more ambitious single-pass generation. Each relaxation is a measured trade-off with a known baseline, not a dependency discovered under load.

Building frontier-first produces the opposite: systems structurally dependent on capabilities they should never have assumed. Monolithic prompts that cannot be shortened. Tasks that cannot be decomposed without redesigning workflows. Implicit reliance on reasoning power that smaller models lack. The architecture collapses when the frontier model is unavailable, rate-limited, or replaced. Local-first avoids this fragility by ensuring the architecture never depends on capabilities beyond its proven minimum.

**Connections.** Local-First reinforces Specification First by demanding that specifications be modular and retrievable in fragments rather than consumed whole. It reinforces SDK as Constraint Surface by requiring that SDK types and interfaces be small enough for a constrained model to process without exceeding its window. It makes Tests as Molds more rigorous because validation of agent output becomes mandatory when model reliability is not assumed. It aligns with Modularity and Bounded Contexts because context-window pressure forces the same atomization that parallelism demands. It strengthens Quality Gates by requiring output validation and retry logic as first-class infrastructure rather than optional hardening. Continuous Flow benefits because local models expose throughput bottlenecks earlier, enabling honest capacity planning.

## 4. Research as Foundation

**Summary.** Structured research precedes specification; agents investigate technologies, patterns, and the current landscape so that decisions are informed by evidence rather than habit or assumption.

**Explanation.** Research as Foundation means that every significant specification and architectural decision is preceded by systematic investigation into the relevant technology landscape, existing solutions, current best practices, known failure modes, and ecosystem maturity. AI agents can parallelize this research at a scale and speed no individual human can match: surveying libraries, comparing implementations, analyzing trade-offs, reading documentation, examining community health, and synthesizing structured findings.

This principle formalizes what competent engineers have always done informally and makes it visible, traceable, and repeatable. Research produces artifacts: technology landscape documents, comparison matrices, trade-off analyses, risk assessments grounded in evidence. These artifacts become explicit inputs to the specification phase. Architectural decision records cite the research that informed them. The chain from investigation to decision to specification to implementation is documented rather than implicit.

Research is not a one-time activity at project inception. It recurs throughout the lifecycle: when dependencies change, when performance bottlenecks require new approaches, when security advisories demand reassessment, when the ecosystem evolves. The research capability is always available and always cheaper than uninvestigated decisions. When research costs minutes of agent computation, omitting it is negligent rather than pragmatic.

**Connections.** Research as Foundation feeds directly into Specification First: specifications reference research findings and landscape analyses rather than encoding assumptions. It informs SDK as Constraint Surface by surfacing proven patterns, established conventions, and ecosystem standards that the SDK should adopt rather than reinvent. It leverages Local-First by using constrained models for focused research tasks (survey one library, compare two APIs) rather than requiring frontier models for monolithic investigations. Modularity and Bounded Contexts benefit because research identifies natural domain boundaries observed in existing systems. Continuous Flow gains a research activity that runs in parallel with or just ahead of spec writing, feeding the pipeline without blocking it. Quality Gates can enforce that ADRs and specifications cite research artifacts, preventing uninvestigated decisions from entering the pipeline.

## 5. Tests as Molds

**Summary.** Tests define the exact shape implementation must take; they are rigid constraints, not rough guidance.

**Explanation.** Tests as Molds reframes automated tests from optional safety nets into structural fixtures that determine pass or fail unequivocally. A mold is built from specification language: behaviors, equivalence classes, adversarial edges, serialization rules, concurrency expectations, and error semantics. Passing tests proves conformance to those constraints; ambiguity in the specification must surface during molding rather than being papered over with forgiving assertions.

Treat molds as invariant across multiple casting passes. Agents may refactor or rewrite internals, but the mold remains until the specification changes deliberately. Where the mold contradicts clarified intent after review, revise the specification first, then regenerate or adjust molds. This inversion (mold fidelity over implementation convenience) is what makes agentic casting trustworthy at scale.

**Connections.** Molds embody Specification First without replacing it (tests cannot carry full rationale alone). Code as Casting is literally the pouring of implementations into molds. Modular boundaries imply separate molds aligned to interface contracts, enabling partitioned failure analysis. Continuous Flow relies on molds to mark clear completion at the Code Casting station. Quality Gates treat mold execution as blocking evidence that castings conform before deployment.

## 6. Code as Casting

**Summary.** Implementation is a commodity artifact produced against a fixed mold; if the commodity is defective, repair the mold or the spec before patching around tests.

**Explanation.** Code as Casting means implementation is mechanically guided work once molds exist. The creative phase shifts upstream to specification and molding; casting becomes search within a narrow corridor defined by acceptance criteria. When castings fail, prefer classification: is the mold wrong, the spec underspecified, or the implementation simply incorrect? Overfitting code to tests (sleight of hand in setup, hidden coupling, environment dependence) is a casting defect that often signals mold weakness.

This principle calibrates human attention. Reviewers spend less time bikeshedding style when architecture, contracts, and molds already bound the solution space. Agents can parallelize casting across bounded contexts because each context has an independent mold and interface contract surface. Commodity casting also reframes maintenance: refactors are safe when molds keep behavior pinned.

**Connections.** Casting consumes outputs of Specification First, SDK as Constraint Surface, and Tests as Molds. The SDK bounds what abstractions casting may use; the type system enforces this mechanically. Bounded contexts limit casting blast radius so parallel agents do not collide. Continuous Flow pulls castings toward review once molds pass locally. Quality Gates repeat mold execution centrally so casting cannot rely on flaky local hacks. Review compares casting to specification intent, not only green tests.

## 7. Modularity and Bounded Contexts

**Summary.** Systems decompose into independent bounded contexts with explicit interface contracts, enabling partitioned molds and parallel agent execution.

**Explanation.** Bounded contexts isolate domain vocabulary, invariants, and lifecycle rules. Independence is contractual: exchanged types, temporal guarantees, versioning, compatibility, error propagation, idempotency, and performance envelopes are spelled out where contexts meet. Contracts are minimized to reduce coordination cost and stabilize molds that span boundaries (contract tests and consumer-driven checks live here).

Effective decomposition aligns agent tasks with seams in the domain, not incidental file splits. Parallel execution emerges when contexts do not cycle depend on hidden shared state or implicit coupling. Humans own architecture boundaries; agents inhabit them. When ambiguity appears at integration seams, escalate to specification and contract revision rather than patching through leaky abstractions.

**Connections.** Contexts carve specifications into parcels that Specification First already distinguished conceptually. Each context yields molds localized to responsibilities described in Tests as Molds. Code as Casting runs concurrently per context when contracts freeze. Continuous Flow manifests as lanes or swim lanes keyed to contexts. Quality gates include contract conformance checks alongside unit and integration molds. Review validates both internal conformance and boundary adherence.

## 8. Continuous Flow

**Summary.** Work moves continuously through bounded stations under WIP limits; kanban regulates flow rather than Sprint theater.

**Explanation.** Continuous Flow organizes work like a production pipeline: backlog converts into specs, SDK surfaces, molds, castings, reviewed increments, integrated artifacts, deployed services, observed behavior, and iterative refinement. Stations include Spec Writing, SDK Design, Test Molding, Code Casting, Human Review, and deployment-related integration (see `kanban.md` in this directory). Limits on work-in-progress expose bottlenecks and prevent starving downstream quality.

Pull-based sequencing matters: downstream stations pull when ready rather than maximizing local heroics upstream. Agents expand throughput where tasks are bounded; humans remain the governors of ambiguity, architecture, approvals, and policy. Flow metrics (cycle time, throughput, aging of WIP) decide process tuning, staffing, or specification investment, not guesses.

**Connections.** Flow operationalizes Specification First by pacing how fast partially formed ideas flood molding. Tests as Molds and Code as Casting become stations with predictable entry and exit criteria. Bounded contexts multiply parallel pipelines that merge at contracts. Quality Gates anchor flow with automation at integration boundaries. Feedback from review or production retriggers upstream stations deliberately instead of collapsing into emergency bypasses.

## 9. Quality Gates

**Summary.** CI/CD pipelines enforce molds, contracts, and policy mechanically; disciplined delivery does not depend on memory or willpower.

**Explanation.** Quality gates are automated checkpoints (build, lint, type checks, suites, mutation testing where warranted, licensing, SBOM scans, vulnerability policies, artifact signing, rollout policies). They embody the organization's non-negotiable guarantees so every casting is measured the same before human review invests depth. Gates fail closed: regressions surface before merge rather than accumulating as silent debt.

Treat gates as the extrusion press that aligns individual contributor behavior with systemic standards. They complement human review rather than substitute it; humans judge intent and edge nuance gates cannot codify efficiently. Extend gates deliberately when repeating review findings signal missing automation. Contract drift and mold gaps often appear first as flaky or skipped checks; treat instability as urgent process debt.

**Connections.** Gates validate outputs of Tests as Molds continuously. They protect Code Casting merges into shared trunk or protected branches. They enforce interface contracts and visibility rules across Bounded Contexts. They sustain Continuous Flow by making station completion objective. Specification First remains authoritative: when gates and spec clash, escalate to specification resolution instead of weakening gates casually.

## 10. Intentional Divergence

**Summary.** Every human-perceptible surface of the product reflects deliberate design decisions documented in the specification, not the statistical defaults of the agent's training data; identity is specified upstream, constrained by the SDK, and verified by quality gates that detect convergence.

**Explanation.** AI agents optimize for the statistical mode of their training data. Without constraint, every output regresses toward the mean. For frontends this produces the recognizable AI aesthetic: Inter font at default weights, purple-to-blue gradients, three-column feature grids, hero-features-pricing-FAQ page structures. For copy it produces "Unlock the power of..." filler. For naming it produces `utils.ts` and `helpers.ts`. For architecture it produces the same popular stack regardless of domain fit. The output passes every mold and honors every contract while remaining indistinguishable from every other AI-generated product.

This convergence has a structural cause. Reinforcement learning from human feedback rewards safe, median outputs. Training corpora skew toward popular frameworks and starter templates. Vague instructions without explicit identity constraints guarantee generic results. The agent is not producing bad work. It is producing the average of its training data, which is indistinguishable from every other agent producing the average of the same training data.

Intentional Divergence counters this through three enforcement layers. First, the specification: a design identity document captures deliberate aesthetic, tonal, and structural choices before any casting begins. It defines what this product looks and sounds like, what it must never look or sound like, and which reference targets anchor its identity. Second, the SDK constraint surface: design tokens (colors, typography, spacing, shadows, radii), naming registries, copy voice guides, and pattern catalogs become building blocks that agents must use. Hardcoded values and ad hoc defaults become compilation failures. Third, quality gates: divergence gates detect known AI-default patterns (slop fingerprints) and flag or block castings that fail to diverge from training-data means.

A human-perceptible surface is anything a user, customer, or reviewer sees and judges: visual design, microcopy, error messages, naming conventions, API endpoints, documentation tone. Intentional Divergence applies to all of them. The scope is not limited to frontends.

**Connections.** Specification First supplies the identity decisions that Intentional Divergence enforces. SDK as Constraint Surface provides the mechanical enforcement layer through design tokens and vocabulary registries. Research as Foundation informs what the training-data default looks like for a given domain, making divergence measurable rather than subjective. Local-First benefits because constrained models are even more prone to defaulting, making explicit identity constraints essential at every model tier. Tests as Molds can include visual regression and copy tone checks. Code as Casting is bounded by both structural constraints (SDK) and identity constraints (design tokens, banned patterns). Quality Gates run divergence detection alongside mold execution, contract checks, and policy enforcement. Continuous Flow gains identity review as a dimension of the Review station without adding a new station.
