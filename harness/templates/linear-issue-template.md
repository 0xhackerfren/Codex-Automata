# Linear Issue Template: Agent-Executable Work Unit

> Use as the description of a Linear implementation issue. Configure a corresponding native Linear issue template in Workspace/Team Settings -> Templates if desired. Replace every placeholder before marking Ready.

## Outcome / user value
[What observable change should exist, for whom, and why?]

## Scope
**In:** [Exact feature, subsystem, interfaces, behavior]
**Out:** [Explicit non-goals and forbidden adjacent changes]

## Source references

- Repository / integration branch / inspected base SHA: [values]
- Work phase: [research / specification / SDK / mold / casting / integration / review]
- Approved model/data restrictions: [engagement policy; no secrets]
- Project/parent: [link or ID]
- Architecture / ADR: [link + decision]
- Code / tests to inspect: [`path`, `path`]
- Existing relevant patterns: [brief description]

## Dependencies and parallelization
- Blocked by: [issue IDs or None]
- Enables: [issue IDs or None]
- Files/interfaces shared with other tasks: [ownership/coordination notes]
- Compatible with parallel work on: [IDs or None]

## Technical contract
- Inputs / triggers: [schema, API, UI events, CLI arguments]
- Outputs / state transitions: [exact observable result]
- Errors / retries / edge cases: [specific outcomes]
- Data model / migrations: [schema + backward compatibility]
- Security / privacy: [authorization, validation, logging, secrets, tenant isolation, data restrictions]
- Performance / reliability / accessibility: [only applicable measurable constraints]

## Implementation guidance
1. [Step with relevant module and expected behavior]
2. [Step with integration touchpoints]
3. [Step for error paths, telemetry, migration, documentation if applicable]

Implementation flexibility: [What is fixed vs deliberately left to implementer?]

## Acceptance criteria (testable)
- [ ] Given [precondition], when [action], then [observable expected result].
- [ ] Given [negative/error case], when [action], then [failure/handling result].
- [ ] Existing [named behavior] continues to work.
- [ ] [Security/privacy or contract requirement if applicable].

## Verification and evidence
- Automated tests to add/update: [test file + scenarios]
- Commands: [`unit test command`, `lint/typecheck/build command`]
- Manual/integration validation: [steps, test environment, expected outputs]
- Evidence for review: [test logs, screenshot, sample API response, PR]

## Rollout / rollback
[Deployment, feature flag, migration, reversibility; write `Not applicable` if none]

## Assumptions and unresolved questions
- Confirmed: [grounded facts]
- Assumed: [explicit nonblocking assumptions]
- Blockers: [must be **None** for Ready]

## Completion record (executor fills out)
- Summary of implementation:
- Changed files:
- Tests/commands run and outcomes:
- Deviations from plan:
- Commit/PR:
- Follow-up issues / remaining risks:


## Routing and checkpoint record

- Job kind / phase / risk: [values]
- Approved provider/model policy reference: [no credentials]
- Selected model / routing rationale: [values or not yet assigned]
- Issue revision / base SHA / contract revision: [values]
- Attempt count / failure class / remaining budget: [values]
- Escalation destination and trigger: [values]
- Branch / worktree / owner / checkpoint: [values]
- Required review / integration / release gate: [values]
- Pending external updates: [values or none]

## Frozen process contract

- Execution context / controller grant / superseded restrictions: [references]
- Adoption profile / task risk profile / methodology version: [values]
- Review gate chosen at adoption: [labeled low-risk self-review / independent / domain diverse-verifier]
- Static conformance / real SDK-TCK fixture / behavioral check commands: [separate commands]
- Gate tiers and required hosts: [T0 targeted / T1 suite / T2 configured matrix]
- Acceptance-to-check map and mold-to-rule table: [references]
- Quota observation / pending drafts / archive procedure: [measured values or unknown; no inferred limit]
- Child readiness updates: [dependency receipts, exact head and artifact paths; proposed vs observed state]
