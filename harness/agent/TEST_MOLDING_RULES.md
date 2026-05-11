# Test Molding Rules

Rules for agents deriving tests from specifications (test molding builds the mold; casting follows).

- Every behavior in the specification must have at least one test.
- Every edge case must have a dedicated test.
- Test names must clearly reference the specification section they verify (for example `test_create_task_empty_title` maps to Behavior 1, Error Condition 1).
- Tests must be sharp: they constrain the implementation so incorrect behavior fails. A test that passes for arbitrary implementations fails as a quality gate.
- Tests must not over-specify: assert behavior required by the specification, not incidental implementation detail. Do not assert on internal data structures unless the specification requires observable behavior tied to those structures.
- Contract tests must exist for every interface between modules (honor interface contracts explicitly).
- All tests must compile. All targeted tests must fail before code casting begins (red state).
- Do not write implementation code during test molding. The mold must exist before casting.
- If a specification section is untestable, flag it and request clarification rather than skipping it.
