# Core Principles

This document defines the six foundational principles of Codex Automata. Together they constrain how specification, molds, casting, bounded contexts, flow, agents, humans, interface contracts, and quality gates interact throughout the lifecycle of a software system.

## 1. Specification First

**Summary.** The specification is the primary engineering artifact; every downstream artifact is derived from or checked against it.

**Explanation.** Specification First means that authoritative intent lives in prose and structured constraints that humans can deliberate over before implementation exists. Requirements are not reconstructed from tests or code alone: tests encode acceptance, but specifications explain invariants, edge cases, failure modes, rationale, and the boundaries between modules. Without a crisp specification, agent tasks lack a stable compass, reviewers lack a definitive comparison target, and quality gates degrade into brittle pattern matching instead of conformance checks.

Operational discipline follows from this artifact hierarchy. Humans invest attention in specs because they amortize ambiguity across molding, casting, and review cycles. Specifications should be falsifiable enough to drive molds (tests) yet rich enough that human reviewers can distinguish correct behavior from plausible but incorrect implementations. Traceability flows one way in authority (spec leads), while feedback from production and review can still refine the spec when evidence demands it.

**Connections.** Specification First supplies the raw material for Tests as Molds: you cannot build a precise mold from a vague brief. It defines the obligations that Code as Casting must satisfy. It sets the vocabulary and rules for Modularity and Bounded Contexts (what each context must guarantee at its boundary). It gives Continuous Flow a defined unit of work that can move between stations. Finally, it underpins Quality Gates: automated checks compare castings and molds to published specifications and interface contracts, not to informal chat history.

## 2. Tests as Molds

**Summary.** Tests define the exact shape implementation must take; they are rigid constraints, not rough guidance.

**Explanation.** Tests as Molds reframes automated tests from optional safety nets into structural fixtures that determine pass or fail unequivocally. A mold is built from specification language: behaviors, equivalence classes, adversarial edges, serialization rules, concurrency expectations, and error semantics. Passing tests proves conformance to those constraints; ambiguity in the specification must surface during molding rather than being papered over with forgiving assertions.

Treat molds as invariant across multiple casting passes. Agents may refactor or rewrite internals, but the mold remains until the specification changes deliberately. Where the mold contradicts clarified intent after review, revise the specification first, then regenerate or adjust molds. This inversion (mold fidelity over implementation convenience) is what makes agentic casting trustworthy at scale.

**Connections.** Molds embody Specification First without replacing it (tests cannot carry full rationale alone). Code as Casting is literally the pouring of implementations into molds. Modular boundaries imply separate molds aligned to interface contracts, enabling partitioned failure analysis. Continuous Flow relies on molds to mark clear completion at the Code Casting station. Quality Gates treat mold execution as blocking evidence that castings conform before deployment.

## 3. Code as Casting

**Summary.** Implementation is a commodity artifact produced against a fixed mold; if the commodity is defective, repair the mold or the spec before patching around tests.

**Explanation.** Code as Casting means implementation is mechanically guided work once molds exist. The creative phase shifts upstream to specification and molding; casting becomes search within a narrow corridor defined by acceptance criteria. When castings fail, prefer classification: is the mold wrong, the spec underspecified, or the implementation simply incorrect? Overfitting code to tests (sleight of hand in setup, hidden coupling, environment dependence) is a casting defect that often signals mold weakness.

This principle calibrates human attention. Reviewers spend less time bikeshedding style when architecture, contracts, and molds already bound the solution space. Agents can parallelize casting across bounded contexts because each context has an independent mold and interface contract surface. Commodity casting also reframes maintenance: refactors are safe when molds keep behavior pinned.

**Connections.** Casting consumes outputs of Specification First and Tests as Molds. Bounded contexts limit casting blast radius so parallel agents do not collide. Continuous Flow pulls castings toward review once molds pass locally. Quality Gates repeat mold execution centrally so casting cannot rely on flaky local hacks. Review compares casting to specification intent, not only green tests.

## 4. Modularity and Bounded Contexts

**Summary.** Systems decompose into independent bounded contexts with explicit interface contracts, enabling partitioned molds and parallel agent execution.

**Explanation.** Bounded contexts isolate domain vocabulary, invariants, and lifecycle rules. Independence is contractual: exchanged types, temporal guarantees, versioning, compatibility, error propagation, idempotency, and performance envelopes are spelled out where contexts meet. Contracts are minimized to reduce coordination cost and stabilize molds that span boundaries (contract tests and consumer-driven checks live here).

Effective decomposition aligns agent tasks with seams in the domain, not incidental file splits. Parallel execution emerges when contexts do not cycle depend on hidden shared state or implicit coupling. Humans own architecture boundaries; agents inhabit them. When ambiguity appears at integration seams, escalate to specification and contract revision rather than patching through leaky abstractions.

**Connections.** Contexts carve specifications into parcels that Specification First already distinguished conceptually. Each context yields molds localized to responsibilities described in Tests as Molds. Code as Casting runs concurrently per context when contracts freeze. Continuous Flow manifests as lanes or swim lanes keyed to contexts. Quality gates include contract conformance checks alongside unit and integration molds. Review validates both internal conformance and boundary adherence.

## 5. Continuous Flow

**Summary.** Work moves continuously through bounded stations under WIP limits; kanban regulates flow rather than Sprint theater.

**Explanation.** Continuous Flow organizes work like a production pipeline: backlog converts into specs, molds, castings, reviewed increments, integrated artifacts, deployed services, observed behavior, and iterative refinement. Stations include Spec Writing, Test Molding, Code Casting, Human Review, and deployment-related integration (see `kanban.md` in this directory). Limits on work-in-progress expose bottlenecks and prevent starving downstream quality.

Pull-based sequencing matters: downstream stations pull when ready rather than maximizing local heroics upstream. Agents expand throughput where tasks are bounded; humans remain the governors of ambiguity, architecture, approvals, and policy. Flow metrics (cycle time, throughput, aging of WIP) decide process tuning, staffing, or specification investment, not guesses.

**Connections.** Flow operationalizes Specification First by pacing how fast partially formed ideas flood molding. Tests as Molds and Code as Casting become stations with predictable entry and exit criteria. Bounded contexts multiply parallel pipelines that merge at contracts. Quality Gates anchor flow with automation at integration boundaries. Feedback from review or production retriggers upstream stations deliberately instead of collapsing into emergency bypasses.

## 6. Quality Gates

**Summary.** CI/CD pipelines enforce molds, contracts, and policy mechanically; disciplined delivery does not depend on memory or willpower.

**Explanation.** Quality gates are automated checkpoints (build, lint, type checks, suites, mutation testing where warranted, licensing, SBOM scans, vulnerability policies, artifact signing, rollout policies). They embody the organization's non-negotiable guarantees so every casting is measured the same before human review invests depth. Gates fail closed: regressions surface before merge rather than accumulating as silent debt.

Treat gates as the extrusion press that aligns individual contributor behavior with systemic standards. They complement human review rather than substitute it; humans judge intent and edge nuance gates cannot codify efficiently. Extend gates deliberately when repeating review findings signal missing automation. Contract drift and mold gaps often appear first as flaky or skipped checks; treat instability as urgent process debt.

**Connections.** Gates validate outputs of Tests as Molds continuously. They protect Code Casting merges into shared trunk or protected branches. They enforce interface contracts and visibility rules across Bounded Contexts. They sustain Continuous Flow by making station completion objective. Specification First remains authoritative: when gates and spec clash, escalate to specification resolution instead of weakening gates casually.
