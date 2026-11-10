# vNext execution contract (methodology 1.0)

Status: implementation contract. Existing twelve principles and numbered phases
remain canonical. New local workflow phases are CLI aliases, not new doctrine.
No scheduler, daemon, inference server or remote synchronization is introduced.

## Requirements

1. Preserve job/journal v1 APIs. Reuse packet identity, claims, attempts and SQLite
   transactions. An opt-in workflow freezes an operator-owned execution plan;
   the legacy completion interface remains observation-only and is not upgraded
   into trusted execution by a version string.
2. Five task risk profiles are distinct from Essential/Standard/Complete adoption
   profiles. Path and declared-impact floors can raise risk, never lower it.
   Unknown semantic impact remains an operator responsibility. Security/policy/CI
   edits require critical rigor; API/persistence/concurrency require architectural.
3. Workflow transitions are ordered and transactional. Phase outputs reference
   committed regular files at exact Git blob revisions. Reject unknown versions,
   stale references, skipped phases and missing acceptance-to-check mappings.
4. Local verification runs only commands frozen in the trusted plan, using argv
   without shell interpolation. Store command, exit status, output digest, elapsed
   time, packet digest and clean Git head in the control database. Reject changed
   trees, failures, missing checks and agent-submitted substitutes at completion.
   Commands are executable authority; operators must review them. This is not an
   OS sandbox or proof that a command tests the right behavior.
5. Protect specification, SDK, molds, policy and test paths against silent changes.
   Explicit operator-authorized protected deltas remain possible and require
   independent review. Self-review is labeled and allowed only at low risk.
6. Context contains universal, task, phase, risk and selected source material in
   deterministic order. Use committed blobs, hashes and a strict UTF-8 byte budget;
   never silently truncate. Repository excerpts are untrusted data, not policy.
   A byte budget is exact; tokenizer-specific tokens are not inferred.
7. Checkpoints export portable, versioned state with phase, baseline/current head,
   artifacts, attempts, failures and remaining budget. Resume checks database
   identity and repository state. An export cannot replace the trusted database
   or reset retries. Unknown side effects still require journal reconciliation.
8. Model qualification uses measured capabilities, approval and availability;
   no commercial name implies competence. Return eligibility, never dispatch.
9. Benchmark three instruction arms against the same eight task categories with
   equal budgets, real subprocess checks and externally driven live-agent runs.
   Synthetic harness validation is never reported as model performance.

## Test molds

Use disposable Git repositories and control databases. Reject fabricated receipts,
failed commands, post-check commits, uncommitted edits, profile downgrades, missing
phase outputs, stale artifact blobs, protected edits, skipped phases, malformed
JSON, unsupported versions, context overflow, corrupt checkpoint and duplicate
completion. Exercise actual single-agent completion, restart and retries. Test
installed wheel and existing adoption combinations. Hosted Windows results must
be observed separately from local Linux results.
