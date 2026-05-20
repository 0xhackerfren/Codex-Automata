# Glossary



Definitions use Codex Automata terminology consistently across specifications, SDK, design identity, molds, casting, bounded contexts, interface contracts, quality gates, agent tasks, human review, and flow.



**Agent Task**  

A bounded unit of work assigned to an AI agent with explicit inputs, outputs, and acceptance criteria. Elaboration: must cite an authoritative specification or interface contract section, include a backlog identifier where the process uses one, and stop with a structured escalation when prerequisites are missing.



**Accessibility**  

A specification constraint ensuring that user-facing behaviors are perceivable, operable, understandable, and robust for users with disabilities. Elaboration: accessibility requirements enter at the specification level, flow through design identity (contrast ratios, keyboard navigation, screen reader support), are enforced by test molds (automated accessibility checks), and verified through product testing with accessibility-constrained user profiles. Target WCAG level is declared in the design identity document. See `reference/accessibility.md`.



**Action Classification**  

A three-tier system for categorizing agent actions by risk: AUTO (proceed without approval), LOG (proceed and record for audit), APPROVE (halt for human approval). Elaboration: the classification determines which agent behaviors can proceed autonomously and which require human judgment. Default classification is defined in `reference/guardrails.md` and can be overridden per project using the guardrail config template. When an action's classification is unclear, treat it as APPROVE.



**Bounded Context**  

An independent partition of the system where a specific domain model applies; the natural unit of parallel execution. Elaboration: communicates outward only through published interface contracts, owns its invariants, and carries its own molds aligned to its specification.



**Building Block**  

A composable unit within the SDK constraint surface: a type, interface, trait, event schema, or extension point that downstream work must use. Elaboration: building blocks are the vocabulary of the constraint surface; agents compose them rather than inventing ad hoc abstractions; new building blocks are added only through SDK extension following the specification pipeline.



**Brownfield**  

An existing codebase that predates methodology adoption. Elaboration: brownfield onboarding applies the recovery protocol systematically to existing modules, progressively establishing specifications, SDK types, and tests retroactively. Modules are prioritized by risk and change frequency. See `reference/brownfield-onboarding.md`.



**Casting**  

The implementation code produced by satisfying a mold derived from a specification; treated as a commodity artifact. Elaboration: defects often indicate an underspecified mold or specification drift rather than a need for ad hoc test bending.



**Code Casting**  

The phase where agents write or refactor implementation until all relevant molds pass under the governing interface contracts. Elaboration: parallelizes across contexts when contracts and repository ownership boundaries are clear.



**Constraint Surface**  

The programmatic boundary defined by the SDK that determines what abstractions, types, and patterns are available to tests and implementation. Elaboration: enforced mechanically by the type system; prevents agent drift by making it impossible to compile code that references undefined building blocks; see also SDK.



**Contract Gap**  

A gap class where a module boundary defined in the architecture has no contract tests despite a documented interface contract. Elaboration: the interface contract document may exist, but nothing mechanically verifies that both sides honor it; recovery writes contract tests from the interface contract and runs them against both sides.



**Cost Budget**  

An estimated token allocation for an agent task or pipeline phase, used to control spending and prevent unbounded execution. Elaboration: cost budgets are informed by the phase-specific estimates in `reference/cost-awareness.md` and interact with the iteration protocol's attempt limits. Model tiering (standard vs. frontier) is a primary cost lever.



**Convergence**  

The tendency of AI agents to produce output that regresses toward the statistical mode of training data, resulting in generic, undifferentiated artifacts across projects. Elaboration: caused by RLHF rewarding safe outputs, narrow training corpora skewed toward popular frameworks, and vague instructions without identity constraints; affects visual design, copy, naming, architecture, and every other human-perceptible surface; Intentional Divergence is the countermeasure.



**Coverage Erosion**  

A gap class where tests once existed but were deleted, disabled, marked as skipped, or allowed to become flaky without remediation. Elaboration: the mold has degraded over time; recovery restores or rewrites tests from the current specification, not from the original test code, since the specification may have evolved.



**Design Identity**  

A specification document defining the deliberate aesthetic, tonal, and structural choices that distinguish a product from training-data defaults. Elaboration: covers visual design (typography, color, layout, motion), copy voice (tone, vocabulary, banned phrases), naming conventions, and architectural patterns where applicable; created during Phase 1 (Architecture) for projects with user-facing surfaces; feeds into the SDK as design tokens and vocabulary registries; uses `templates/design-identity-template.md` in the harness.



**Design Token**  

A named, structured value (color, type size, spacing, shadow, radius) that agents must use instead of raw values. Elaboration: part of the SDK constraint surface for visual design; agents reference tokens, not hardcoded hex, px, rem, or font-family values; zero hardcoded visual values in implementation; derived from the design identity document following the same pipeline as other SDK building blocks.



**Deployment Checklist**  

A structured verification document used during Phase 7 (Deployment and Observation) to confirm pre-deployment quality gates, execute deployment steps, verify post-deployment health, and document the rollback plan. Elaboration: ensures no deployment proceeds without verified tests, approved reviews, and confirmed environment readiness; includes smoke tests and monitoring checks for post-deploy verification.



**Divergence Gate**  

A quality gate that detects convergence toward known AI-default patterns and flags or blocks castings that fail to diverge. Elaboration: catalogs slop fingerprints (banned fonts, default color values, generic copy, boilerplate layouts) and checks castings against them; does not judge aesthetics subjectively but detects measurable convergence toward training-data means; runs alongside mold execution, contract checks, and policy enforcement.



**Flow**  

The continuous movement of work through the pipeline, managed with kanban mechanics and WIP limits. Elaboration: measured with cycle time, throughput, and WIP age rather than sprint velocity metaphors.



**Gap Assessment**  

A structured document recording a discovered gap in specification, tests, or coverage for an existing module. Elaboration: captures the affected module, gap class, discovery trigger, severity, current and required state, recovery plan, and recurrence prevention; uses `templates/gap-assessment-template.md` in the harness.



**Generator**  

In property-based testing, a strategy for producing random valid inputs that exercise a specification invariant. Elaboration: generators derive from the input constraints in the specification (e.g., "arbitrary non-empty string, length 1-200" for a title field). Frameworks like fast-check, Hypothesis, and proptest provide generator combinators. See `reference/property-based-testing.md`.



**Guardrail**  

A human-judgment safety boundary that determines whether an agent action can proceed, should be logged, or requires explicit approval. Elaboration: guardrails complement quality gates. Quality gates are mechanical (automated pass/fail). Guardrails are about human oversight and risk calibration. Configured per-project using the guardrail config template. See `reference/guardrails.md`.



**Human Review**  

The phase where humans verify that implementation matches specification, intent, and systemic risk expectations beyond what automated checks encode. Elaboration: may reject work and return it upstream to specification, molding, or casting with explicit rationale.



**Incident Postmortem**  

A blameless analysis document created after a production incident to trace root causes, assess impact, identify which methodology quality gates should have caught the failure, and file gap assessments for the recovery pipeline. Elaboration: connects incidents back to the specification-first pipeline by classifying what the methodology missed (spec gap, mold gap, SDK gap, contract gap, coverage erosion, review miss, product test miss).



**Interface Contract**  

A formal agreement between bounded contexts defining the API surface, data formats, behaviors, version rules, and failure semantics at the boundary. Elaboration: stability and minimal surface area reduce coordination cost; evolution is deliberate and test backed.



**Iteration**  

A structured cycle of agent work bounded by attempt counts and quality gate results. Elaboration: inner-loop iteration occurs within a single phase when a quality gate fails (test fails, review rejects); outer-loop iteration cascades across phases when review sends work back to specification. Each iteration is logged in the context state Session History. After a bounded number of failed attempts, the agent escalates to human rather than continuing. See `reference/iteration.md`.



**Invariant**  

In property-based testing, a condition that must hold for any valid input to a specified behavior. Elaboration: invariants derive from specification sections. "For any valid title, createTask returns a task with that title" is an invariant derived from the create behavior specification. Invariants become property-based test molds. See `reference/property-based-testing.md`.



**Local-First**  

The principle that AI-driven systems are designed to function on the smallest viable model first, then expanded to frontier models as capability demands. Elaboration: constraint forces engineering discipline (precise context management, atomic task decomposition, structured prompts, output validation, graceful degradation) that benefits every model tier; a system proven on local models scales cleanly to frontier, while the reverse path produces fragile frontier dependencies.



**Mold**  

The executable test suite and fixtures derived from a specification that define the exact shape implementation must take. Elaboration: rigid by design; changing a mold without a specification change is a process violation unless governed as an emergency fix with follow up specification alignment.



**Mold Gap**  

A gap class where behavior is documented in the specification but has no tests, or the tests are too weak to constrain the implementation meaningfully. Elaboration: the specification says what should happen, but no mold enforces it; recovery derives tests from the existing specification following standard test molding rules.



**Multi-Agent Orchestration**  

The coordination of multiple AI agents working simultaneously on a project. Elaboration: Codex Automata coordinates agents through shared artifacts (frozen SDK interfaces, interface contracts, specifications) rather than direct agent-to-agent communication. The SDK constraint surface serves as the coordination protocol. Agents are isolated by bounded context, work in separate git worktrees, and merge sequentially. See `reference/multi-agent.md`.



**Product Test**  

A verification scenario where an AI agent operates the assembled application as a real user, given a user profile and a goal-oriented objective. Elaboration: measures both functional completion (did the agent accomplish the goal?) and experience quality (click count, backtracking, navigation depth, error encounters, time to completion); see `product-testing.md` in this directory.



**Property-Based Test**  

A test that verifies a specification invariant holds for any valid input, using a framework that generates hundreds or thousands of random inputs. Elaboration: extends the Tests as Molds concept. Traditional molds test specific input/output pairs. Property-based molds test classes of behavior. Catches edge cases the developer never imagined. Frameworks: fast-check (TypeScript), Hypothesis (Python), proptest (Rust), gopter (Go). See `reference/property-based-testing.md`.



**Quality Gate**  

An automated check in the CI/CD pipeline that enforces process discipline mechanically (build, test, policy, security, signing, compatibility, performance budgets as applicable). Elaboration: failures block progression by default; waivers require explicit human risk acceptance tied to records.



**Quick Change**  

An abbreviated workflow for small modifications that touch a single bounded context with existing specifications, SDK interfaces, and tests. Elaboration: bypasses the full 8-phase pipeline when all qualification criteria are met (single context, existing spec/SDK/tests, no new interfaces needed). If any criterion fails, the change escalates to the full pipeline. Available at all adoption profiles. See `reference/quick-change.md`.



**Recovery**  

The process of closing gaps in specification, tests, or coverage after code already exists. Elaboration: follows the same pipeline as forward work (specification first, then molds, then casting) but applied retroactively; recovery tasks are first-class kanban work items, not invisible background chores; see `recovery.md` in this directory for the full protocol.



**Research**  

Structured investigation into the technology landscape, existing solutions, current best practices, and ecosystem state that precedes specification and architectural decisions. Elaboration: agents parallelize research across libraries, implementations, market solutions, and trade-off analyses; outputs are formal artifacts (landscape documents, comparison matrices, risk assessments) that specifications and ADRs cite; research recurs throughout the lifecycle whenever decisions require current evidence.



**Retrospective**  

A periodic team reflection on methodology effectiveness, process friction, and continuous improvement opportunities. Elaboration: examines pipeline metrics (cycle time, test pass rate, recovery volume, gap discovery rate), adoption profile fit, context persistence health, and methodology friction points. Produces actionable process improvements. Uses `templates/retrospective-template.md`.



**SDK**  

The compilable, importable package of types, interfaces, extension points, and compositional primitives that defines the constraint surface for a project. Elaboration: derived from specifications and interface contracts; sits between specification and tests in the pipeline (Documentation, SDK, Tests, Code); makes architectural decisions enforceable at the type system level; see also Constraint Surface, Building Block.



**SDK Design**  

The phase where architectural boundaries and specifications are translated into a compilable constraint surface. Elaboration: produces SDK packages with no implementation behind them; forces abstraction by requiring clean decomposition into building blocks; precedes test molding so that all tests are written against SDK interfaces.



**SDK Extension**  

The disciplined process of adding new building blocks to the SDK when the application requires capabilities the current surface does not provide. Elaboration: extension follows the full pipeline (specification first, then SDK update, then tests, then code); agents cannot extend the SDK unilaterally; prevents emergent, unplanned growth of the constraint surface.



**SDK Gap**  

A gap class where behavior exists in the codebase but has no corresponding types or interfaces in the SDK constraint surface. Elaboration: indicates that the implementation bypassed the constraint surface; recovery writes the missing SDK types from the specification, then derives tests against those types; often co-occurs with spec gaps.



**Security Audit**  

A systematic review of implementation code for security vulnerabilities, producing structured findings that route to the gap assessment and recovery pipeline. Elaboration: checks for injection, authentication/authorization issues, data exposure, dependency vulnerabilities, input validation, cryptographic weaknesses, and configuration problems. Findings are classified by severity and linked to specification sections. Uses `templates/security-audit-template.md`.



**Slop Fingerprint**  

A known AI-default pattern cataloged for detection by divergence gates. Elaboration: examples include Inter/Roboto/Arial as body font, indigo-600 as accent color, purple-to-blue gradient heroes, three-column feature grids at identical breakpoints, hero-features-pricing-FAQ page structures, "Unlock the power of..." copy, `utils.ts`/`helpers.ts` naming; projects define their own fingerprint catalog in the design identity document; fingerprints are objective, measurable patterns, not subjective aesthetic judgments.



**Spec Gap**  

A gap class where behavior exists in the codebase but is not documented in any specification. Elaboration: the most dangerous class because without a specification you cannot determine whether the current behavior is correct or accidental; recovery writes the specification first from domain knowledge, not from the code.



**Spec Writing**  

The phase where humans produce or revise specifications and contracts; typically the first human constrained station in the flow. Elaboration: WIP limits preserve depth and reduce ambiguous drafts that would pollute molding and casting.



**Specification**  

A precise, testable document defining what a module or bounded context must do, including behaviors, edge cases, non-functional expectations, and failure modes. Elaboration: the primary human authored engineering artifact that downstream molds and reviews reference.



**Test Molding**  

The phase where tests and fixtures are derived from specifications to build the mold. Elaboration: separates acceptance shape from implementation and enables mechanical enforcement through quality gates.



**Test Objective**  

A goal-oriented statement of what a simulated user must accomplish during a product test, stated as an outcome rather than a script of steps. Elaboration: "create an account and reach the dashboard" is an objective; "click the signup button, fill in the email field" is a script; objectives test discoverability and usability, scripts test only a predetermined path.



**Token Budget**  

The estimated token count for an agent task, used for cost planning and session sizing. Elaboration: informed by phase-specific estimates (e.g., Phase 5 Code Casting typically consumes 50-150K tokens per module). Interacts with the local-first principle (keep context lean) and the iteration protocol (attempt budgets implicitly cap spending). See `reference/cost-awareness.md`.



**User Profile**  

A test fixture that defines who a simulated user is during a product test, constraining agent behavior to simulate a specific class of user. Elaboration: includes technical literacy, domain knowledge, goals, constraints (accessibility, device, network), and behavioral tendencies; derived from the specification's user-facing sections; uses `templates/user-profile-template.md` in the harness.



**UX Budget**  

A quantitative threshold for acceptable user experience during a product test, such as maximum clicks, navigation depth, backtracking count, error encounters, or time to completion. Elaboration: transforms subjective experience assessments into falsifiable metrics; set per objective and per profile; calibrated from baselines and product standards.



**WIP Limit**  

A cap on work in process at a station to prevent overload, shorten feedback loops, and expose bottlenecks. Elaboration: pulling work only when capacity exists pairs with explicit definitions of ready for each station.



**WCAG**  

Web Content Accessibility Guidelines, published by the W3C. Elaboration: WCAG defines four principles (Perceivable, Operable, Understandable, Robust) and three conformance levels (A, AA, AAA). Level AA is the recommended minimum for production products. WCAG criteria are cited in specifications as accessibility constraints and verified through automated testing and accessibility-constrained product test profiles. See `reference/accessibility.md`.

