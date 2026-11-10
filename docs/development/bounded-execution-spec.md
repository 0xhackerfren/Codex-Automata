# Bounded workflow command execution

Workflow verification currently redirects arbitrary output to a temporary file.
This limits retained excerpts but permits disk exhaustion and leaves descendants
running after timeout. This change applies to `workflow run` only.

## Contract

1. Each approved check may set `output_limit_bytes` from 1 to 16,777,216.
   Omission means 1,048,576 bytes. The exact plan approval covers the setting.
2. Read merged stdout/stderr through a bounded pipe queue; do not spool output to
   disk. Retain at most 8,192 excerpt bytes and hash/count at most the output limit.
   Exactly the limit is allowed. A further byte fails with `output-limit` even if
   the child exits zero or the caller expected a failing behavioral mold.
3. Timeout includes pipe draining. Timeout and overflow terminate the process and
   consume a durable environment failure attempt. Successful output receipts keep
   their existing hash/count semantics; overflow receipts describe only the
   captured prefix, never claim a complete transcript.
4. POSIX checks start a fresh session. Kill the process group on timeout, overflow,
   interruption and direct-child completion, including children holding the pipe.
   Windows terminates the direct child; full tree containment remains external.
   Deliberately detached POSIX descendants and arbitrary file writes also require
   external containment. This is resource control, not an OS sandbox.
5. Preserve current-head, ownership, schema and attempt gates. A spawn failure
   returns a failure receipt. Readers use bounded queues and cannot block cleanup.

## Validation molds

Exercise exact-limit success, merged stderr, zero-exit overflow, continuous
output, silent timeout, invalid limits and spawn failure. On POSIX, exercise a
grandchild that would write a marker after timeout and after parent completion.
Verify an overflow persists as a failed attempt and cannot satisfy phase gates.
Run the complete CLI suite and standalone workflow demonstration.

## Observed validation

- 80 tests pass on Linux from source and again from the built, separately
  installed 0.6.1 wheel. Seven new tests cover this contract, including durable
  failure evidence and process-group cleanup with real descendants.
- Standalone demo completes six phases and six commands, resumes its checkpoint
  and reports zero failed attempts. Context remains within its 16,000-byte budget.
- Markdown lint passes across 128 files; `git diff --check` passes.
- Hosted Windows/Python matrix results belong to the PR checks, not this local
  Linux validation. This was a single-agent review.

## Repository reconciliation

Baseline main is `687c71eb2574a86db775c62a6de22d11acf78a25`, the merge of PR #6.
At inspection, all four non-main branches were ancestors of main:
`docs/per-10-operating-model`, `feat/automata-vnext`, `sdk-block-registry` and
`three-new-principles`. Remote deletion was blocked pending explicit user
authorization; no branch was removed. The implementation is committed locally;
automatic approval review also blocked public push pending explicit authorization.
No remote implementation branch or PR was created in this continuation.
