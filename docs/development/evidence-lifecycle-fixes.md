# Execution evidence, artifact lifecycle and reviewer freshness

## Contract

This change closes the three reproduced findings at PR #7 head
`3544283ba9df4ee7d03b3cf6e5b5e1347c134b15`.

1. Workflow checks execute in a fresh temporary snapshot materialized from the
   exact commit's regular Git blobs, without checkout/export filters, ignored
   files, inherited Python import paths or Git metadata. Bound snapshot size to
   64 MiB per blob and 256 MiB total. Reject symlinks and submodules explicitly.
   Each command gets a separate snapshot and a minimal process environment.
   Hash tracked snapshot files again after execution. Verify the original
   worktree before/after and at transitions using file contents; reject hidden
   index flags. Allow Git-declared text newline normalization only. Arbitrary
   clean filters are unsupported. These checks do not implement an OS sandbox,
   pin installed dependencies or prevent transient/external side effects.
   The exact plan may explicitly select `verified-worktree` for tools needing
   Git metadata or ignored dependencies. That mode retains physical tracked-file
   checks and index-flag rejection, but does not exclude ignored files. Receipts
   distinguish both modes; there is no automatic fallback.
2. Exact-plan `planned_outputs` declares phase-owned future spec/SDK/mold paths.
   They must belong to the job references, write scope and required lifecycle.
   Legacy job APIs still require existing versioned references. Workflow approval,
   start, recovery and context generation understand planned paths. Missing
   outputs appear as planned context, never fabricated source. The owning phase
   must create and pin them before advancement. Earlier provisional outputs may
   evolve only through their owning phase. Later changes require rewind; existing
   protected files still require approved-change scope and independent review.
3. Store reviewer attestation issuance time and workflow recovery generation.
   Enforce age from reviewer issuance both at review acceptance and downstream
   gates. Do not reset the clock when a coder submits an artifact. Rewind
   invalidates older attestations, including exact-artifact replay. Re-attestation
   with the separate reviewer token may renew approval. Reject missing legacy
   timestamps and future-dated timestamps. Retain review maximum-age gates.

## Verification

Regressions must reject the hidden-dirty-worktree and expired-attestation
reproductions. Exercise a complete workflow creating a new SDK and behavioral
mold, authorized spec revision, post-freeze drift, rewind/review replay and
renewal, ignored-source exclusion, environment stripping and snapshot mutation.
Run source and installed-wheel suites, standalone demo, documentation checks and
the Windows/Linux Python matrix. CLI 0.6.2 changes the policy fingerprint; active
jobs require the original pinned release or reviewed migration.

## Observed validation and delivery

- 102 tests pass on Linux from source and again from the built, separately
  installed 0.6.2 wheel. Eighteen new regressions cover the reproduced findings,
  full new-SDK/new-mold authoring, authorized amendments, downstream freezes,
  reviewer expiry/renewal/rewind, physical byte and mode changes, ignored-source
  exclusion, environment stripping and explicit compatibility-mode approval.
- Source and installed-wheel standalone demos complete six phases and six actual
  commands with zero failed attempts and checkpoint resume; context stays within
  16,000 bytes. Markdown lint and whitespace checks pass.
- Hosted Windows/Linux Python 3.10/3.13 results must be read at the current head
  of [PR #7](https://github.com/0xhackerfren/Codex-Automata/pull/7). POSIX symlink
  and mode checks are explicitly skipped on Windows.
- Linear synchronization remains unavailable at the workspace issue limit. This
  versioned contract is the durable local work specification; no issue ID or
  completed review/integration is fabricated.

Single-agent implementation review. No live-model efficacy, unattended release,
OS containment, dependency attestation or general hermetic execution is claimed.
