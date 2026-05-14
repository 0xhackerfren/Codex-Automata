# Glossary

Definitions use Codex Automata terminology consistently across specifications, molds, casting, bounded contexts, interface contracts, quality gates, agent tasks, human review, and flow.

**Agent Task**  
A bounded unit of work assigned to an AI agent with explicit inputs, outputs, and acceptance criteria. Elaboration: must cite an authoritative specification or interface contract section, include a backlog identifier where the process uses one, and stop with a structured escalation when prerequisites are missing.

**Bounded Context**  
An independent partition of the system where a specific domain model applies; the natural unit of parallel execution. Elaboration: communicates outward only through published interface contracts, owns its invariants, and carries its own molds aligned to its specification.

**Casting**  
The implementation code produced by satisfying a mold derived from a specification; treated as a commodity artifact. Elaboration: defects often indicate an underspecified mold or specification drift rather than a need for ad hoc test bending.

**Contract Gap**  
A gap class where a module boundary defined in the architecture has no contract tests despite a documented interface contract. Elaboration: the interface contract document may exist, but nothing mechanically verifies that both sides honor it; recovery writes contract tests from the interface contract and runs them against both sides.

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

**Mold**  
The executable test suite and fixtures derived from a specification that define the exact shape implementation must take. Elaboration: rigid by design; changing a mold without a specification change is a process violation unless governed as an emergency fix with follow up specification alignment.

**Mold Gap**  
A gap class where behavior is documented in the specification but has no tests, or the tests are too weak to constrain the implementation meaningfully. Elaboration: the specification says what should happen, but no mold enforces it; recovery derives tests from the existing specification following standard test molding rules.

**Quality Gate**  
An automated check in the CI/CD pipeline that enforces process discipline mechanically (build, test, policy, security, signing, compatibility, performance budgets as applicable). Elaboration: failures block progression by default; waivers require explicit human risk acceptance tied to records.

**Recovery**  
The process of closing gaps in specification, tests, or coverage after code already exists. Elaboration: follows the same pipeline as forward work (specification first, then molds, then casting) but applied retroactively; recovery tasks are first-class kanban work items, not invisible background chores; see `recovery.md` in this directory for the full protocol.

**Spec Gap**  
A gap class where behavior exists in the codebase but is not documented in any specification. Elaboration: the most dangerous class because without a specification you cannot determine whether the current behavior is correct or accidental; recovery writes the specification first from domain knowledge, not from the code.

**Spec Writing**  
The phase where humans produce or revise specifications and contracts; typically the first human constrained station in the flow. Elaboration: WIP limits preserve depth and reduce ambiguous drafts that would pollute molding and casting.

**Specification**  
A precise, testable document defining what a module or bounded context must do, including behaviors, edge cases, non-functional expectations, and failure modes. Elaboration: the primary human authored engineering artifact that downstream molds and reviews reference.

**Test Molding**  
The phase where tests and fixtures are derived from specifications to build the mold. Elaboration: separates acceptance shape from implementation and enables mechanical enforcement through quality gates.

**WIP Limit**  
A cap on work in process at a station to prevent overload, shorten feedback loops, and expose bottlenecks. Elaboration: pulling work only when capacity exists pairs with explicit definitions of ready for each station.
