# Code Casting Rules

Rules for agents writing implementation during code casting.

- You are filling a mold. Tests define shape. Success means tests pass against the specification and contracts.
- Read the specification and tests before writing any code.
- Stay within the bounded context of the assigned module. Do not reach into unrelated modules.
- Use the interface contracts as defined. Do not modify them without routed human approval (see behavioral rules).
- If a test seems wrong, do not alter it silently. Report it and wait for guidance.
- Make small, atomic commits. Each commit should move toward passing one or more assigned tests where possible.
- Do not introduce dependencies not specified in architecture documents (quality gates on drift).
- Do not add behavior not required by the specification. Extra behavior is defect risk and scope creep.
- If you cannot make a test pass and believe the specification is ambiguous, stop and ask instead of guessing.
- Prefer clarity over cleverness for human review and long-term maintenance.
- When all assigned tests pass within scope, stop. Do not refactor, optimize, or add features beyond what the specification and task allow unless a separate agent task directs it.
