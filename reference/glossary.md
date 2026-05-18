# Glossary

Definitions use Codex Automata terminology consistently across specifications, SDK, molds, casting, bounded contexts, interface contracts, quality gates, agent tasks, human review, and flow.

**Agent Task**  
A bounded unit of work assigned to an AI agent with explicit inputs, outputs, and acceptance criteria. Elaboration: must cite an authoritative specification or interface contract section, include a backlog identifier where the process uses one, and stop with a structured escalation when prerequisites are missing.

**Bounded Context**  
An independent partition of the system where a specific domain model applies; the natural unit of parallel execution. Elaboration: communicates outward only through published interface contracts, owns its invariants, and carries its own molds aligned to its specification.

**Building Block**  
A composable unit within the SDK constraint surface: a type, interface, trait, event schema, or extension point that downstream work must use. Elaboration: building blocks are the vocabulary of the constraint surface; agents compose them rather than inventing ad hoc abstractions; new building blocks are added only through SDK extension following the specification pipeline.

**Casting**  
The implementation code produced by satisfying a mold derived from a specification; treated as a commodity artifact. Elaboration: defects often indicate an underspecified mold or specification drift rather than a need for ad hoc test bending.

**Contract Gap**  
A gap class where a module boundary defined in the architecture has no contract tests despite a documented interface contract. Elaboration: the interface contract document may exist, but nothing mechanically verifies that both sides honor it; recovery writes contract tests from the interface contract and runs them against both sides.

**Constraint Surface**  
The programmatic boundary defined by the SDK that determines what abstractions, types, and patterns are available to tests and implementation. Elaboration: enforced mechanically by the type system; prevents agent drift by making it impossible to compile code that references undefined building blocks; see also SDK.

**Coverage Erosion**  
A gap class where tests once existed but were deleted, disabled, marked as skipped, or allowed to become flaky without remediation. Elaboration: the mold has degraded over time; recovery restores or rewrites tests from the current specification, not from the original test code, since the specification may have evolved.

**Code Casting**  
The phase where agents write or refactor implementation until all relevant molds pass under the governing interface contracts. Elaboration: parallelizes across contexts when contracts and repository ownership boundaries are clear.

**Flow**  
The continuous movement of work through the pipeline, managed with kanban mechanics and WIP limits. Elaboration: measured with cycle time, throughput, and WIP age rather than sprint velocity metaphors.

**Gap Assessment**  
A structured document recording a discovered gap in specification, tests, or coverage for an existing module. Elaboration: captures the affected module, gap class, discovery trigger, severity, current and required state, recovery plan, and recurrence prevention; uses `templates/gap-assessment-template.md` in the harness.

**Human Review**  
The phase where humans verify that implementation matches specification, intent, and systemic risk expectations beyond what automated checks encode. Elaboration: may reject work and return it upstream to specification, molding, or casting with explicit rationale.

**Interface Contract**  
A formal agreement between bounded contexts defining the API surface, data formats, behaviors, version rules, and failure semantics at the boundary. Elaboration: stability and minimal surface area reduce coordination cost; evolution is deliberate and test backed.

**Local-First**  
The principle that AI-driven systems are designed to function on the smallest viable model first, then expanded to frontier models as capability demands. Elaboration: constraint forces engineering discipline (precise context management, atomic task decomposition, structured prompts, output validation, graceful degradation) that benefits every model tier; a system proven on local models scales cleanly to frontier, while the reverse path produces fragile frontier dependencies.

**Mold**  
The executable test suite and fixtures derived from a specification that define the exact shape implementation must take. Elaboration: rigid by design; changing a mold without a specification change is a process violation unless governed as an emergency fix with follow up specification alignment.

**Mold Gap**  
A gap class where behavior is documented in the specification but has no tests, or the tests are too weak to constrain the implementation meaningfully. Elaboration: the specification says what should happen, but no mold enforces it; recovery derives tests from the existing specification following standard test molding rules.

**Product Test**  
A verification scenario where an AI agent operates the assembled application as a real user, given a user profile and a goal-oriented objective. Elaboration: measures both functional completion (did the agent accomplish the goal?) and experience quality (click count, backtracking, navigation depth, error encounters, time to completion); see `product-testing.md` in this directory.

**Quality Gate**  
An automated check in the CI/CD pipeline that enforces process discipline mechanically (build, test, policy, security, signing, compatibility, performance budgets as applicable). Elaboration: failures block progression by default; waivers require explicit human risk acceptance tied to records.

**Research**  
Structured investigation into the technology landscape, existing solutions, current best practices, and ecosystem state that precedes specification and architectural decisions. Elaboration: agents parallelize research across libraries, implementations, market solutions, and trade-off analyses; outputs are formal artifacts (landscape documents, comparison matrices, risk assessments) that specifications and ADRs cite; research recurs throughout the lifecycle whenever decisions require current evidence.

**Recovery**  
The process of closing gaps in specification, tests, or coverage after code already exists. Elaboration: follows the same pipeline as forward work (specification first, then molds, then casting) but applied retroactively; recovery tasks are first-class kanban work items, not invisible background chores; see `recovery.md` in this directory for the full protocol.

**Spec Gap**  
A gap class where behavior exists in the codebase but is not documented in any specification. Elaboration: the most dangerous class because without a specification you cannot determine whether the current behavior is correct or accidental; recovery writes the specification first from domain knowledge, not from the code.

**SDK**  
The compilable, importable package of types, interfaces, extension points, and compositional primitives that defines the constraint surface for a project. Elaboration: derived from specifications and interface contracts; sits between specification and tests in the pipeline (Documentation, SDK, Tests, Code); makes architectural decisions enforceable at the type system level; see also Constraint Surface, Building Block.

**SDK Design**  
The phase where architectural boundaries and specifications are translated into a compilable constraint surface. Elaboration: produces SDK packages with no implementation behind them; forces abstraction by requiring clean decomposition into building blocks; precedes test molding so that all tests are written against SDK interfaces.

**SDK Extension**  
The disciplined process of adding new building blocks to the SDK when the application requires capabilities the current surface does not provide. Elaboration: extension follows the full pipeline (specification first, then SDK update, then tests, then code); agents cannot extend the SDK unilaterally; prevents emergent, unplanned growth of the constraint surface.

**SDK Gap**  
A gap class where behavior exists in the codebase but has no corresponding types or interfaces in the SDK constraint surface. Elaboration: indicates that the implementation bypassed the constraint surface; recovery writes the missing SDK types from the specification, then derives tests against those types; often co-occurs with spec gaps.

**Spec Writing**  
The phase where humans produce or revise specifications and contracts; typically the first human constrained station in the flow. Elaboration: WIP limits preserve depth and reduce ambiguous drafts that would pollute molding and casting.

**Specification**  
A precise, testable document defining what a module or bounded context must do, including behaviors, edge cases, non-functional expectations, and failure modes. Elaboration: the primary human authored engineering artifact that downstream molds and reviews reference.

**Test Objective**  
A goal-oriented statement of what a simulated user must accomplish during a product test, stated as an outcome rather than a script of steps. Elaboration: "create an account and reach the dashboard" is an objective; "click the signup button, fill in the email field" is a script; objectives test discoverability and usability, scripts test only a predetermined path.

**Test Molding**  
The phase where tests and fixtures are derived from specifications to build the mold. Elaboration: separates acceptance shape from implementation and enables mechanical enforcement through quality gates.

**User Profile**  
A test fixture that defines who a simulated user is during a product test, constraining agent behavior to simulate a specific class of user. Elaboration: includes technical literacy, domain knowledge, goals, constraints (accessibility, device, network), and behavioral tendencies; derived from the specification's user-facing sections; uses `templates/user-profile-template.md` in the harness.

**UX Budget**  
A quantitative threshold for acceptable user experience during a product test, such as maximum clicks, navigation depth, backtracking count, error encounters, or time to completion. Elaboration: transforms subjective experience assessments into falsifiable metrics; set per objective and per profile; calibrated from baselines and product standards.

**WIP Limit**  
A cap on work in process at a station to prevent overload, shorten feedback loops, and expose bottlenecks. Elaboration: pulling work only when capacity exists pairs with explicit definitions of ready for each station.
