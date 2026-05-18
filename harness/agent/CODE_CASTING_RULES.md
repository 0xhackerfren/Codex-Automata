# Code Casting Rules

Rules for agents writing implementation during code casting.

- You are filling a mold within the SDK constraint surface. Tests define shape. The SDK defines vocabulary. Success means tests pass against the specification, SDK interfaces, and contracts.
- Read the specification, SDK interfaces, and tests before writing any code.
- Implement SDK interfaces. Do not introduce types, patterns, or abstractions outside the SDK constraint surface.
- Stay within the bounded context of the assigned module. Do not reach into unrelated modules.
- Use the interface contracts and SDK as defined. Do not modify them without explicit human approval (see behavioral rules).
- If you need a building block not in the SDK, stop and request SDK extension through the specification pipeline.
- If a test seems wrong, do not alter it silently. Report it and wait for guidance.
- Make small, atomic commits. Each commit should move toward passing one or more assigned tests where possible.
- Do not introduce dependencies not specified in architecture documents (quality gates on drift).
- Do not add behavior not required by the specification. Extra behavior is defect risk and scope creep.
- If you cannot make a test pass and believe the specification is ambiguous, stop and ask instead of guessing.
- Prefer clarity over cleverness for human review and long-term maintenance.
- When all assigned tests pass within scope, stop. Do not refactor, optimize, or add features beyond what the specification and task allow unless a separate agent task directs it.
