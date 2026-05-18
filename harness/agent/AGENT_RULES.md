# Agent Operating Rules

Operating manual for agents executing tasks under Codex Automata. Specifications define intent, the SDK defines the constraint surface, tests are the mold, and casting produces code within strict quality gates.

## 1. Core Principles

- Research informs decisions. Investigate technologies, patterns, and the landscape before specifying.
- Specifications are the source of truth. Behavior and scope flow from them.
- The SDK is the constraint surface. It defines the building blocks agents must use.
- Build local-first. Assume the smallest viable model. Keep context lean, tasks atomic, and prompts structured.
- Tests are the acceptance criteria. Passing tests define done for an agent task.
- Code is the output, not the goal. Casting satisfies the specification, SDK interfaces, and tests under human oversight.

## 2. Behavioral Rules (Strict)

R1. Do not write implementation code before the specification, SDK constraint surface, and test plan exist for the target module.

R2. Do not expand scope beyond what the specification defines. If you discover needed work outside that scope, report it.

R3. Do not silently change interface contracts or SDK interfaces. Any interface change requires explicit human approval and review.

R4. Do not bypass, skip, or delete failing tests. Fix the implementation or report the test as incorrect.

R5. Do not create abstractions outside the SDK constraint surface. If you need a type, interface, or pattern not in the SDK, stop and request SDK extension through the specification pipeline.

R6. Do not create duplicate abstractions. Check existing SDK modules and interfaces first.

R7. Prefer small, atomic commits. Each commit addresses one logical change traceable to a specification section.

R8. Surface ambiguity instead of guessing. If the specification does not answer your question, stop and ask.

R9. Explain deviations. If you must deviate from the specification, document the reason in the commit message and flag it for human review.

R10. Every agent task must map to a specification section, an SDK interface, and at least one test case.

R11. Do not introduce external dependencies not specified in the architecture documents.

R12. Keep context lean. Do not assume unlimited context windows or frontier-model capabilities. Structure tasks, specifications, and prompts to be modular and retrievable in fragments suitable for the smallest viable model.

R13. When you discover code without a corresponding specification, SDK interface, or tests, halt and report the gap. Do not silently work around it, do not write tests derived from the code, and do not treat unspecified behavior as intentional. Report the gap using the gap assessment template (`templates/gap-assessment-template.md`) so a human can triage and schedule recovery.

R14. During recovery tasks, follow rules R1-R13 in the context of an existing codebase. Derive specifications from domain knowledge and stakeholder intent, not from the current implementation. Derive SDK extensions from specifications. Derive tests from the specification against SDK interfaces, not from the code. If the specification and the code conflict, surface the conflict for human resolution.

## 3. Task Execution Protocol

- Step 1: Read the agent task definition and locate the specification reference.
- Step 2: If the task involves technology decisions or unfamiliar domains, perform research and produce structured findings.
- Step 3: Read the relevant specification sections.
- Step 4: Locate the SDK interfaces that define the constraint surface for this task.
- Step 5: Read the test plan and locate the test cases for this agent task.
- Step 6: Read the interface contracts for modules this task touches.
- Step 7: Implement within the SDK boundary, making small commits as you go.
- Step 8: Verify all assigned tests pass.
- Step 9: Run any available linters and quality gates.
- Step 10: Report completion with a summary of what was implemented and which tests pass.

## 4. Communication Protocol

- When blocked: report what you need and why progress is blocked.
- When ambiguous: quote the unclear specification section and suggest plausible interpretations without choosing one arbitrarily.
- When deviating: explain the deviation, its justification, and request alignment in human review.
- When complete: summarize changes, test results, and notes for the reviewer.
