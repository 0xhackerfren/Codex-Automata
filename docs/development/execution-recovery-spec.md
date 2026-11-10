# Durable command intent and interruption recovery

## Problem and contract

A workflow command previously started before its receipt existed in SQLite.
Two invocations sharing a claim could execute together, and a controller crash
left no durable indication that a command might have produced side effects.

1. Commit a command intent before launching. Record run ID, repository, task,
   phase, approved check, Git head, owner and start time; never expose claim tokens.
2. Permit one running command per canonical repository in the shared controller
   database. Reject another command, phase advance, rewind, claim release and
   manual attempt/resolution changes while its outcome remains unresolved.
3. Receipt insertion, failure accounting and command completion are atomic.
   A missing receipt leaves the intent running across restarts. There is no
   automatic expiry, replay or inference that the command stopped.
4. Operator-only reconciliation requires authority, the exact run ID, nonempty
   investigation evidence and an explicit assertion that the command and its
   descendants have stopped. It records an environment failure attempt once and
   never fabricates a passing receipt. Normal failure resolution is still needed
   before retry; exhausted attempts remain exhausted.
5. Expose run history in checkpoints and `workflow runs`. Reject late receipts
   after reconciliation. The operator must stop the original process before
   reconciliation; this controller cannot prove host isolation or remote effects.

## Validation

Reject overlapping runners before the second launch. Exercise real controller
process exit after intent commit, restart with retained intent, blocked replay,
invalid authority/evidence, exact-once reconciliation, persistent attempt count,
and normal receipt completion. Keep existing workflow/demo compatibility and
current-head checks. Multi-host locks and separate databases remain out of scope.

## Observed validation and delivery

- 84 CLI tests pass on Linux from source and again from a separately installed
  0.6.1 wheel. The new regressions cover overlap, real controller-process exit,
  restart/reconciliation, persistent attempts, late receipts and stale green reuse.
- Standalone demo completes six phases and six actual commands with zero failed
  attempts, resumes its checkpoint and stays within its context budget.
- Markdown lint passes across 129 files; whitespace checks pass.
- Hosted Windows/Linux Python 3.10/3.13 results must be read at the current PR
  head. Earlier-head results do not establish validation of later changes.
- Delivery: [PR #7](https://github.com/0xhackerfren/Codex-Automata/pull/7), pending
  review/integration. Linear tracking could not be created because the workspace
  rejected the write at its free issue limit; this contract remains the durable
  local work specification. No remote issue ID is claimed.

Single-agent implementation review. No live-model effectiveness claim, automatic
replay, merge, deployment or OS isolation is implied.
