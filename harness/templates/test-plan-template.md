# Test Plan: [Module Name]

<!--
[Link this plan to the specification version. Tests are the mold; every behavior should map to at least one test. Contract tests lock interface contracts.]
-->

## Metadata

| Field | Value |
|-------|-------|
| Module name | [same as spec] |
| Specification reference | [path or ID, with version] |
| Version | [test plan version] |
| Date | [YYYY-MM-DD] |
| Author | [name or role] |

## Specification Coverage Matrix

| Spec behavior (ID or section) | Test case ID | Test type (unit / integration / contract) | Notes |
|-------------------------------|--------------|---------------------------------------------|-------|
| [e.g., §3.1] | [TC-001] | [unit] | [ ] |
| [ ] | [ ] | [ ] | [ ] |

[Every numbered behavior in the specification should appear in at least one row.]

## Unit Tests

| Test name | Spec reference | Input | Expected output | Notes |
|-----------|----------------|-------|-----------------|-------|
| [test_function_scenario] | [§x.y] | [fixtures, parameters] | [assertions, state] | [edge focus, mocks] |

## Integration Tests

| Test name | Modules in flow | Spec reference | Scenario | Expected outcome | Notes |
|-----------|-----------------|----------------|----------|------------------|-------|
| [test_end_to_end_slice] | [A, B] | [§] | [steps] | [observable result] | [environment] |

## Contract Tests

| Test name | Interface contract | Spec reference | Checks | Notes |
|-----------|-------------------|----------------|--------|-------|
| [test_provider_shape] | [Contract ID] | [§] | [schema, errors, idempotency] | [consumer vs provider] |

## Edge Case Tests

| Test name | Spec edge case | Input / setup | Expected behavior |
|-----------|----------------|---------------|-------------------|
| [ ] | [§ Edge Cases #n] | [ ] | [ ] |

## Performance Tests

[Include only if the specification defines non-functional targets.]

| Test name | Requirement | Method | Pass threshold | Notes |
|-----------|-------------|--------|----------------|-------|
| [ ] | [latency / throughput] | [load tool, benchmark] | [ ] | [ ] |

## Test Environment Requirements

- **Dependencies:** [services, databases, queues]
- **Fixtures:** [data sets, seeds]
- **Mock services:** [which boundaries are stubbed]
- **Secrets / config:** [how provided in CI and local]

## Exit Criteria

- [ ] All listed tests **compile** (or equivalent for the stack).
- [ ] All new tests **fail** against the current casting until implementation exists (red phase of the flow).
- [ ] Coverage targets: [statement / branch / critical paths; or explicit rationale if not numeric]
- [ ] Contract tests run in quality gate: [where, e.g., CI job name]
- [ ] Human review can verify traceability from spec to mold via the coverage matrix
