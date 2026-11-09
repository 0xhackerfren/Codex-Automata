# Adversarial audit: delivery foundation

Date: 2026-11-09. Scope: local repository instructions, CLI adoption paths,
routing/job contracts and shipped CI. This is a single-agent audit, not an
independent review or a consumer end-to-end qualification. No remote service
state, branch protection, Windows execution or model benchmark is asserted.

## Findings and disposition

| Severity | Attack / failure | Evidence | Disposition |
| --- | --- | --- | --- |
| High | Detailed tickets mistaken for delivered features | No artifact can infer runtime behavior from issue text | Fixed wording in manifesto and delivery policy: durable intent requires separate GitHub implementation evidence |
| High | Failing tests converted into a successful CI job | Original Python shell chain ended in a successful echo | Fixed runner selection/failure propagation; regression injects installation and test exit failures |
| High | Adopting/updating harness destroys customized policy | Original init/update unconditionally merged files | Init now preflights collisions; update stages a separate candidate; regressions preserve original bytes and reject overlapping staging |
| High, open | Ready labels or routing prose treated as enforcement | No dispatcher/record validator checks job packets, prerequisites or approved inventory | Implement a provider-neutral job schema and validator before autonomous dispatch; negative molds must reject missing dependencies, unauthorized provider and stale revisions |
| High, open | Concurrent agents both believe they own shared paths | Linear status is not atomic ownership; coordinator remains a proposal | Keep single-writer/manual coordination until durable claims, interruption recovery and overlap rejection are implemented and tested |
| High, open | Stale evidence approves a changed implementation | Policy pins review heads; no automatic enforcement of that association | Validate current head, checks and approvals in a future integration adapter; do not claim branch protections are configured |
| High, open | Stale/duplicate service mutations corrupt work state | No durable operation journal or synchronization adapter exists | Implement idempotent operation identity, entity version checks and reconciliation before unattended synchronization |
| Medium | Missing verification scripts produce success | Original verify skipped both scripts and returned success | Fixed missing/unavailable runner failures; regression tests exercise both |
| Medium | Task types and escalation lack an executable handoff shape | Earlier policy only named broad modes | Added MODEL_ROUTING job table, decision order, failure classes and packet fields; schema enforcement remains open |
| Medium | Frontier retries reset budgets or override data policy | Model replacement can hide repeated failure | Policy carries attempts across models/sessions and filters approval before capability; no approval registry is implemented |
| Medium, open | Structural checks appear to prove semantic coverage | spec-check/divergence are heuristics, not acceptance or integration tests | Explicitly documented limit; qualify on a real consumer with injected contract violations and broken journeys before adoption |
| Medium, open | SDK/mold ceremony applied to research and documentation | Existing broad core rules say every task needs SDK and test mappings | Delivery policy scopes readiness by phase and permits explicit N/A; older phase guidance still needs a systematic consistency review |
| Medium, open | Security reviewer shares the implementer's blind spot | Single-agent self-review cannot establish independence | Obtain independent review and adversarial consumer pilot evidence before unattended integration |

## Verification observed locally

`PYTHONPATH=cli python -m unittest discover -s cli/tests -v`: ten tests passed.
Coverage includes all fifteen profile/agent combinations, portable routing files,
hidden integration files through Bash init, preflight collisions, broken symlinks,
source preservation, overlapping staging rejection, customized-policy preservation,
missing/unavailable/failing gates, installation failure and test failure propagation.
`git diff --check` passed. No Windows execution or remote CI pass is claimed.

## Recommended implementation order

1. Define a versioned job/evidence schema and validate one task packet locally.
   Require phase-specific prerequisites, repository identity, revision, write
   ownership, approval-policy reference, acceptance and attempt history. Reject
   unknown schema versions; treat ticket content as data, not authority to alter
   higher-priority instructions or execute arbitrary commands.
2. Add a deterministic readiness/routing decision engine against a consumer-owned
   approved model inventory. Test missing evidence, denied provider, exhausted
   budget, environment failure and required human decision. A route recommendation
   is distinct from dispatch permission.
3. Implement durable claims/checkpoints and a bounded single-worker execution
   adapter. Test interruption before/after writes, recovery, stale bases and retry
   budgets across restarts before adding parallel writers.
4. Add GitHub evidence validation and manual integration rehearsal tied to exact
   heads. Failure injection must reject stale reviews, failed checks and semantic
   interface drift. Keep release authority explicit.
5. Add journaled Linear/GitHub synchronization and reconcile duplicate, stale,
   out-of-order, permission-denied and uncertain-result operations.
6. Pilot one real vertical slice from specification through product acceptance,
   then qualify economical/local models by measured reviewed outcomes. Expand
   concurrency only after claim and integration failure tests pass.

These are recommended work definitions, not published Linear issues. No issue IDs,
model qualification results, provider approvals or automation are fabricated.

## Implementation follow-up: local control plane

The local enforcement portion is now implemented in
`cli/codex_automata/control.py`, exposed through `job` and `journal` CLI commands.

| Earlier gap | Implemented evidence | Remaining boundary |
| --- | --- | --- |
| No job/readiness validator | Strict versioned fields, phase prerequisites, tracked Git references, actual base SHA and evidenced dependencies | Operator must supply authentic Linear-derived packets and approval policy |
| No deterministic routing | Approved inventory filters, phase/risk tiers, availability, failure classification and persistent attempts | No provider invocation or automatic credit discovery |
| No durable claims | SQLite immediate transactions, unique active writer per repository, opaque owner tokens and checkpoints | Only workers sharing the same database coordinate; stopping an external worker is an operator responsibility |
| Stale check/review evidence | Current-head and packet binding, independent reviewer field, required-check allowlist, actual changed-path checks and integration ancestry | Supplied observations are not authenticated GitHub attestations; no unattended merge exists |
| No operation journal | Stable ID plus canonical payload, replay rejection, uncertain outcome state and exact-observation reconciliation | No remote write adapter; actual provider observations require authenticated collection |
| Ceremony blocks upstream work | Root, detailed agent rules and Cursor core now scope gates to job phase | Consumer-specific instruction overrides need adoption review |

Observed verification: 28 tests passed locally, including real disposable Git
branch/commit/integration/dependency flow and concurrent SQLite claimant rejection.
Compilation and whitespace checks pass. No provider output, remote CI, Windows
execution, independent reviewer or production consumer qualification is claimed.

These controls close local enforcement gaps within a trusted-operator boundary.
They do not claim protection from a process that can edit the control database,
approval policy and evidence directly. Unattended multi-host dispatch and remote
integration require separate authenticated adapters and deployment isolation.

The built wheel was also installed into an isolated target; all 28 tests passed
against that installed package. No additional remote action was performed.
