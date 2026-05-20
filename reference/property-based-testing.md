# Property-Based Testing

This document defines how Codex Automata projects use property-based testing (PBT) as an advanced form of the mold. Property-based tests verify invariants that must hold for any valid input, complementing example-based tests that verify specific input/output pairs.

For module-level example-based molds, see the test molding phase in `harness/PLAYBOOK.md`. For test plan structure, see `harness/templates/test-plan-template.md`. For molding rules, see `harness/agent/TEST_MOLDING_RULES.md`. For adoption profile requirements, see [adoption-profiles.md](adoption-profiles.md).

## What Property-Based Testing Is

Traditional tests—**example-based tests**—verify specific input/output pairs: "given input A, expect output B." The developer chooses the examples. Five title lengths might mean five separate test cases. Edge cases the developer never imagined remain untested.

**Property-based tests** verify invariants that must hold for **any** valid input: "for all valid titles, `createTask` returns a task with that title." Instead of the developer choosing test inputs, a framework generates hundreds or thousands of random inputs and verifies the property holds for each. When a property fails, the framework **shrinks** the failing case to a minimal counterexample, making failures easier to diagnose.

Property-based testing does not replace example-based testing. It extends the mold with a different shape: invariants instead of instances.

## How PBT Extends the Mold Concept

In Codex Automata, tests are **molds**. They constrain what the casting (implementation) may become.

- **Traditional molds** are shaped by specific examples from the specification. Each example is a point constraint: this input must produce this output.
- **Property molds** are shaped by **invariants** from the specification. Each property is a region constraint: every valid input in this class must satisfy this rule.

Both constrain the casting. Traditional molds catch specific failures—the cases the author thought to write. Property molds catch **classes** of failures, including edge cases the developer never imagined: off-by-one lengths, unicode normalization surprises, empty collections combined with filters, and inconsistent state after sequences of operations.

A specification that says "title is required, max 200 characters" implies infinitely many valid and invalid strings. Example-based tests sample a few. Property-based tests assert the rule across the sampled space the framework explores.

## Deriving Properties from Specifications

Every specification section implies properties. Read constraints and behaviors as invariants, not only as examples.

### Input constraints

**"Title is required, max 200 characters"** implies:

- For any non-empty string of length 1 to 200, `createTask` succeeds.
- For any empty string, `createTask` returns `InvalidTaskInputError` (or the specified error type).
- For any string of length greater than 200, `createTask` returns `InvalidTaskInputError`.

### Query and list behaviors

**"List Tasks returns all tasks, optional filter by status"** implies:

- For any set of tasks, `listTasks` returns all of them (when no filter).
- For any set with N pending tasks, `listTasks({ status: "pending" })` returns exactly N results.
- The `listTasks` result is always a subset of all tasks—no invented tasks appear in the response.

### Mutations and consistency

**"Delete Task removes the task"** implies:

- For any existing task, after `deleteTask`, `findById` returns null (or equivalent not-found).
- For any non-existent id, `deleteTask` returns `TaskNotFoundError`.

### General derivation checklist

When reading a specification section, ask:

1. **What must always be true** after this operation, for any valid input?
2. **What must always be rejected**, for any invalid input matching a constraint class?
3. **What roundtrip or consistency** relationships hold (create then read, serialize then deserialize)?
4. **What subset or ordering** invariants apply (filters, sorts, pagination)?

Document each property in the test plan's Property-Based Tests section with: property statement, spec reference, generator strategy, expected invariant, and priority.

## When to Use PBT vs. Traditional Tests

| Use property-based tests for | Use traditional (example-based) tests for |
|------------------------------|----------------------------------------|
| Input validation (length, type, format) | Specific business logic paths with named scenarios |
| Data transformations and pure functions | Sequence-dependent behavior with explicit ordering |
| Serialization/deserialization roundtrips | Integration scenarios with fixed environment setup |
| Mathematical or algebraic properties | Error message **content** (exact strings) |
| Sorting, filtering, pagination invariants | UI-specific interactions and layout |
| CRUD consistency (create/find/delete laws) | Regulatory or audit cases requiring documented examples |
| API contracts where "for all valid X" is the spec | Behaviors that depend on clock, random seed, or external IDs you must pin |

Prefer one strong property over many redundant examples when the specification states a rule over a **class** of inputs.

## Framework Guidance

Choose a mature PBT library for your language:

| Language | Recommended framework | Notes |
|----------|----------------------|-------|
| TypeScript | [fast-check](https://github.com/dubzzz/fast-check) | Most mature in TS ecosystem; excellent shrinking |
| Python | [Hypothesis](https://hypothesis.readthedocs.io/) | Industry standard; stateful testing support |
| Go | [gopter](https://github.com/leanovate/gopter) or [rapid](https://github.com/flyingmutant/rapid) | rapid is newer and fast |
| Rust | [proptest](https://github.com/proptest-rs/proptest) | Idiomatic for Rust projects |
| Java / Kotlin | [jqwik](https://jqwik.net/) | JUnit 5 integration |

Configure generators to match **specification constraints**, not arbitrary random data. A generator that produces invalid inputs when testing a "valid input succeeds" property will produce noisy failures—split valid and invalid properties instead.

## Integration with the Test Plan

The test plan template includes a **Property-Based Tests** section alongside unit, integration, contract, and product tests. During **Phase 4 (Test Molding)**:

1. Read each specification section for invariants.
2. Define properties in the test plan table (property, spec reference, generator strategy, expected invariant, priority).
3. Implement property tests against **SDK interfaces**, same as example-based tests.
4. Properties are **red-state** just like traditional tests: written before implementation exists; they must fail until casting satisfies them.

If the PBT framework requires types to compile, SDK types for the module must exist first (Phase 3 complete). The property definition and generator exist before the implementation body.

## PBT as a Quality Gate

Profile requirements for property-based coverage:

| Profile | PBT requirement |
|---------|-----------------|
| **Complete** | Every specification section that defines input constraints or data transformations should have at least one property-based test |
| **Standard** | PBT recommended; not required for gate passage |
| **Essential** | PBT optional |

When PBT is required, the test plan's Property-Based Tests section must be filled and traceable to spec sections in the coverage matrix. Reviewers verify that invariants match the specification, not implementation accidents.

## Workflow Summary

1. **Specification (Phase 2)** — Constraints and behaviors stated precisely enough to derive invariants.
2. **SDK (Phase 3)** — Types and interfaces property tests call.
3. **Test molding (Phase 4)** — Example-based tests plus properties in red state.
4. **Code casting (Phase 5)** — Implementation until all properties and examples pass.
5. **Review (Phase 6)** — Confirm properties trace to spec; generators match constraints.

## Anti-Patterns

- **Properties without spec traceability** — Every property must cite a specification section.
- **One mega-property** — Split valid-input success, invalid-input rejection, and consistency laws into separate properties.
- **Generators that ignore the spec** — Random strings of any length do not test "max 200 characters"; bound generators to the spec.
- **PBT as implementation oracle** — Do not derive properties by reading code; derive from specification invariants.
- **Skipping shrinking failures** — Minimal counterexamples are the fastest path to root cause; fix the invariant or the casting.

## Companion Documents

- [principles.md](principles.md) — Principle 2: Tests as Molds; Principle 6: Quality Gates
- [adoption-profiles.md](adoption-profiles.md) — Profile-specific PBT requirements
- [glossary.md](glossary.md) — Mold, casting, quality gate, specification
- [product-testing.md](product-testing.md) — User-facing verification (complements module-level PBT)
- [iteration.md](iteration.md) — Inner-loop retry when properties fail
- `harness/templates/test-plan-template.md` — Property-Based Tests section
- `harness/agent/TEST_MOLDING_RULES.md` — Agent rules for deriving properties
- `harness/.cursor/skills/test-molding/SKILL.md` — Step-by-step molding workflow
- `examples/task-manager/tests/test-plan.md` — Worked example of property table
