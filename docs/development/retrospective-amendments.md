# Retrospective amendments and adoption tests

Methodology 1.0 / CLI 0.6.0. Sources: operator-supplied campaign retrospective,
selected domain specs, contract/mold files, hook and quota-blocker artifacts,
and the consumer's actual pinned SDK. Reviewed API/fixture details corroborate
key lessons. Historical counts, timing, zero-reopen and every-defect-caught claims
are retrospective observations, not independently reproduced campaign results.
No private consumer code, policy or documentation is copied into this public repo.
A clean next campaign remains the adoption test; these changes alone do not prove it.

| Item | Amendment and local enforcement | Next-campaign adoption test |
| --- | --- | --- |
| 1: two-layer molds | TEST_MOLDING_RULES, template traceability; workflow requires green static/fixture and red behavior separately | Commit molds only after actual SDK/schema/TCK fixture checks pass; new behavior fails for intended reason |
| 2: supersession | SESSION_START, append-only dated grants, superseded tokens invalidated; exact-plan operator approval | Session reconciles standing push/PR grant and remote refs/head; stale restriction does not suppress authorized publication |
| 3: defined review | Consumer configuration and issue template declare review gate; risk floor and reviewer-token attestation enforce it | Low-risk self-review is labeled; higher risk/truth promotion obtains configured separate verifier before Done |
| 4: planning capacity | LINEAR_FIRST quota-aware batches; reversible authorized Done archival; no deletion | Observe real workspace limits, retain evidence and archive eligible Done records through available adapter/UI; verify capacity afterward |
| 5: child readiness | LINEAR_FIRST closure protocol; local `_ready` checks evidenced integration ancestry | RECONCILE derives exact child pins from upstream receipt and confirms all dependencies before proposing/performing Ready transition |
| 6: self-access/bootstrap | Isolation runbook, external context authority, exact payload evaluator and selftest with remedy | Fresh operational checkout needs explicit operator development bootstrap; agent cannot grant itself privilege or weaken runtime hook |
| 7: interruption | Per-agent/task checkpoints, re-read-before-replay rule, reclaim/rewind preserve attempts/history | Interrupt a landed edit, inspect actual bytes, resume without duplicate insertion or shared-checkpoint collision |
| 8: tiers/determinism | Casting rules specify T0/T1/T2 and pure declared-input generators with check mode; plan receipts record tiers | Relevant T0 runs after edit, T1 at unit completion, configured T2 hosts at PR; generator drift is detected by shared check |
| 9: domain template | New domain-spec-template with alternatives/decision, numbered rules, traces, exact paper fixture and handoff | New domain spec supplies exact expected records and derives molds without inventing implementation internals |
| 10: tool schemas | SESSION_START requires current dynamic schema before first session call | First server use follows actual schema; observed quirks are recorded, not guessed or generalized |

Remote automation remains optional: no quota API, archive operation, child issue
transition or authenticated synchronization is claimed here. When unavailable,
record a concrete operator UI step and preserve pending drafts. Current service
limits/plan semantics must be observed; the historical free-plan cap is not a
permanent product guarantee. Done archival requires applicable standing authority,
not an inferred license to archive arbitrary work.

Executable follow-through: `session inspect --publication-required` compares a
fresh remote ref with actual local HEAD and fails on missing/unpublished evidence.
`session readiness` returns exact dependency integration receipts and pinned
artifact paths as a local transition proposal. Neither command publishes or
changes a remote issue. Session tests use a real disposable bare Git remote.
