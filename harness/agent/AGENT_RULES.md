# Agent Operating Rules

Operating manual for agents executing tasks under Codex Automata. Specifications define intent, tests are the mold, and casting produces code within strict quality gates.

## 1. Core Principles

- Specifications are the source of truth. Behavior and scope flow from them.
- Tests are the acceptance criteria. Passing tests define done for an agent task.
- Code is the output, not the goal. Casting satisfies the specification and tests under human oversight.

## 2. Behavioral Rules (Strict)

R1. Do not write implementation code before the specification and test plan exist for the target module.

R2. Do not expand scope beyond what the specification defines. If you discover needed work outside that scope, report it.

R3. Do not silently change interface contracts. Any interface change requires explicit human approval and review.

R4. Do not bypass, skip, or delete failing tests. Fix the implementation or report the test as incorrect.

R5. Do not create duplicate abstractions. Check existing modules and interfaces first.

R6. Prefer small, atomic commits. Each commit addresses one logical change traceable to a specification section.

R7. Surface ambiguity instead of guessing. If the specification does not answer your question, stop and ask.

R8. Explain deviations. If you must deviate from the specification, document the reason in the commit message and flag it for human review.

R9. Every agent task must map to a specification section and at least one test case.

R10. Do not introduce external dependencies not specified in the architecture documents.

R11. When you discover code without a corresponding specification or tests, halt and report the gap. Do not silently work around it, do not write tests derived from the code, and do not treat unspecified behavior as intentional. Report the gap using the gap assessment template (`templates/gap-assessment-template.md`) so a human can triage and schedule recovery.

R12. During recovery tasks, follow rules R1-R11 in the context of an existing codebase. Derive specifications from domain knowledge and stakeholder intent, not from the current implementation. Derive tests from the specification, not from the code. If the specification and the code conflict, surface the conflict for human resolution.

## 3. Task Execution Protocol

- Step 1: Read the agent task definition and locate the specification reference.
- Step 2: Read the relevant specification sections.
- Step 3: Read the test plan and locate the test cases for this agent task.
- Step 4: Read the interface contracts for modules this task touches.
- Step 5: Implement, making small commits as you go.
- Step 6: Verify all assigned tests pass.
- Step 7: Run any available linters and quality gates.
- Step 8: Report completion with a summary of what was implemented and which tests pass.

## 4. Communication Protocol

- When blocked: report what you need and why progress is blocked.
- When ambiguous: quote the unclear specification section and suggest plausible interpretations without choosing one arbitrarily.
- When deviating: explain the deviation, its justification, and request alignment in human review.
- When complete: summarize changes, test results, and notes for the reviewer.
