# Gap assessment v1: 2026-11-10

Baseline: `28e36509c2632c4f9a77fc0fb9a41e9715116735`, 28 Linux tests pass.
This is a single-agent audit. Documentation is not functional evidence.

| Severity | Gap and evidence | Remediation | Acceptance mold |
| --- | --- | --- | --- |
| High | `Controller.complete` accepts caller-authored passed checks | Add opt-in plan-bound execution receipts in trusted state | Forged JSON cannot satisfy workflow verification |
| High | Job phase is a string, no lifecycle history | Transactional ordered workflow and artifact pins | Skip, missing output and stale blob rejected |
| High | Risk is caller-selected, tests/contracts writable when scope permits | Conservative risk floors and protected-path checks | Critical path downgrade and unauthorized test edit rejected |
| High | No bounded context generator | Deterministic progressive packet with exact byte ceiling | Overflow fails; same inputs reproduce same bytes |
| High | Checkpoint is free text | Portable typed export with authoritative-state comparison | Corruption, stale head and budget reset rejected |
| Medium | Local completion requires a different reviewer identity | Explicit low-risk self-review, independent review above low risk | Self-review cannot masquerade as independence |
| Medium | Routing uses only two capability labels | Add capability-based eligibility API alongside v1 | Unapproved, unavailable and unqualified models rejected |
| Medium | No empirical evaluation runner | Three-arm task corpus and observed-check runner | Paired budget and result validation; live results pending |
| Medium | Windows restart test closes original connection only | Cleanup current reopened controller | Reopened connection closed before temporary directory deletion |
| High | Documentation workflow is invalid YAML | Change colon-bearing run scalar to block; run parser/lint/link checks | Workflow parses and docs validation runs |
| Medium | Test molding demands every existing test fail | Limit red requirement to newly introduced regression tests | Existing green suite explicitly retained |
| Medium | Offline work described only as unsynchronized drafts | First-class local task workflow, optional Linear mapping | No network/model/service in standalone demonstration |

Remote baseline inspected: CLI run 42706941008 failed on Windows/Python 3.13;
Linux 3.10/3.13 passed. Documentation run 42706937023 failed before jobs were
created. SQLite cleanup bug is reproducible by observing the leaked reopened
connection; Linux permits unlinking open files, Windows does not.

Audit boundaries: hooks warn; structural shell gates do not prove semantics.
Review identities, approval policy, command meaning, declared impact, and database
isolation remain trusted-operator responsibilities. No daemon or private adapter
belongs in this repository. Existing explanations remain human references;
short execution packets must not load them all by default.

## After implementation

| Original gap | Result and evidence | Residual limitation |
| --- | --- | --- |
| Root namespace/role ambiguity (added P0) | Namespaced manifest/config, explicit grants, capability evaluator, populated-monorepo/operation/maintenance/update/rollback tests | Tool adapter/process isolation and legacy rule cleanup remain consumer responsibilities |
| Fabricated completion/phase skipping | Approved-plan workflow, observed subprocess receipts, ordered pinned artifacts, legacy-bypass rejection | Command/test semantic quality still requires review |
| Risk/protected artifact bypass | Conservative deterministic floors, operator-approved impacts/checks, protected deltas and separate reviewer attestation | Unknown semantic impact and authentic reviewer independence require operator judgment |
| Unbounded context/recovery | Deterministic byte-bounded packets, optional pinned line excerpts, supplied-context journal, typed snapshot/resume/reclaim/rewind | Byte budgets are not model token counts; repository relocation needs reviewed replan |
| Coarse model routing/no benchmark | Capability eligibility schema/API and three-arm eight-category evaluator | Live model outcomes, statistical effectiveness and candidate test-quality scoring remain pending |
| Windows SQLite cleanup | Cleanup closes current reopened controller, retained in cross-platform CI matrix | Hosted Windows results must be observed for delivered revision |
| Invalid docs workflow | Valid YAML, checked-in lint configuration, formatting fixes, actual local link check | External web availability excluded from local-link validation |
| Undefined adoption/review and mold fixtures | Explicit configured review policy, two-layer mold gates, retrospective adoption matrix | Next real campaign must validate adoption; no synthetic result substitutes for it |

The serious local bypasses found during implementation were fixed and given
regression molds. Remaining items are stated constraints and external validation
work, not claims that unattended production use is ready.
