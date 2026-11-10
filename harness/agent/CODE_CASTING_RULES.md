# Code Casting Rules

Rules for agents writing implementation during code casting.

- You are filling a mold within the SDK constraint surface. Tests define shape. The SDK defines vocabulary. Success means tests pass against the specification, SDK interfaces, and contracts.
- Read the specification, SDK interfaces, and tests before writing any code.
- Implement SDK interfaces. Do not introduce types, patterns, or abstractions outside the SDK constraint surface.
- Stay within the bounded context of the assigned module. Do not reach into unrelated modules.
- Use the interface contracts and SDK as defined. Do not modify them without explicit human approval (see behavioral rules).
- If you need a building block not in the SDK, stop and request SDK extension through the specification pipeline.
- If a test seems wrong, do not alter it silently. Report it and wait for guidance.
- Make small, atomic commits traceable to specification sections (R7). Each commit should move toward passing one or more assigned tests where possible.
- Follow the project's declared branch strategy (R16): create feature branches from the correct base, use meaningful names referencing bounded contexts or spec sections, keep branches short-lived. Do not force-push or rewrite shared branch history without approval.
- Do not modify pipeline configuration (CI/CD workflows, Dockerfiles, deploy scripts) without approval (R17). Pipeline config changes follow the same spec-first flow as application code.
- Do not create or move release tags without approval (R18).
- Do not introduce dependencies not specified in architecture documents (quality gates on drift).
- Do not add behavior not required by the specification. Extra behavior is defect risk and scope creep.
- If you cannot make a test pass and believe the specification is ambiguous, stop and ask instead of guessing.
- Prefer clarity over cleverness for human review and long-term maintenance.
- For user-facing code, all visual values (colors, fonts, sizes, spacing, shadows, radii) must reference design tokens from the SDK. Zero hardcoded hex, px, rem, or font-family values.
- Do not use known AI-default patterns when the design identity document specifies alternatives. Banned defaults include: Inter/Roboto/Arial as primary typeface, framework-default color palettes, purple-blue gradient heroes, three-column feature grids at identical breakpoints, and generic copy phrases cataloged in the design identity.
- When implementing UI, reference the design identity document for aesthetic direction, permitted patterns, and banned patterns. If no design identity exists for user-facing work, stop and report the gap.
- When all assigned tests pass within scope, stop. Do not refactor, optimize, or add features beyond what the specification and task allow unless a separate agent task directs it.

## Verification tiers and determinism

- T0: targeted molds after relevant edits. T1: full project suite per completed unit. T2: configured platform/host matrix per commit/PR. Record exact tier, host, command and current-head result. One host does not prove both hosts passed.
- Run the tier appropriate to the change; repeat broader checks only after relevant changes or failures. Completion requires the frozen plan's checks.
- Every generator/projection is a pure function of declared inputs, with deterministic ordering and a `--check` drift mode wired into the shared gate. Document necessary time/random/external inputs explicitly.
- Static contract checks and fixture checks pass separately from intentionally red new behavioral molds. Never reinterpret a fixture exception as proof of the intended failing behavior.
- After interruption, inspect files before reapplying. Preserve per-agent/task checkpoint journals and retry history.
