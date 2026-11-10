# Local delivery control plane v1

Status: implementation specification. Scope: local, provider-neutral enforcement;
no credentials, remote writes, model execution, merges or releases.

## Contracts

A version-1 JSON job packet has an ID, repository identity, integration branch,
base SHA, phase, explicit risk, intent, bounded write paths, acceptance criteria, dependency IDs,
versioned specification references, approved-model policy ID and attempt limit.
Casting additionally requires contract and mold references. References are local
files at the assigned Git revision, not fabricated paths. Research may omit
contracts/molds. No field is executed as a shell command.

A consumer-owned version-1 policy lists eligible model IDs, capability tiers,
approved job phases, data classifications and deterministic preference order.
Routing fails closed on unknown schema, blocked dependencies, stale Git revision,
policy mismatch, unavailable/ineligible models, exhausted attempts or unresolved
environment/design failures. Stronger models inherit persistent attempts. Routing
is a recommendation, not dispatch authority.

SQLite persists immutable packet digests, one active writer per repository,
checkpoints, attempts, dependency completion and operation journal entries.
BEGIN IMMEDIATE serializes mutations across processes. Claims cannot be stolen
by age. Release requires the original owner and claim token; abandonment requires
an explicit checkpoint and verified process termination outside this tool.
An active job cannot be silently replaced by edited issue text. Retry records
survive reopen and prevent caller-supplied attempt resets.

Evidence validation binds checks and independent review to the actual current
Git head and packet digest. It rejects failed/missing/duplicate checks, stale
heads, unresolved findings, self-review, absent integration evidence and incorrect
merge ancestry. It validates supplied observations, not their provider authenticity;
only trusted adapters may use observations for unattended decisions. This v1
never performs merge or declares deployment. Dependency completion is permitted
only after evidence passes and a recorded claim is released by its owner.

Journal operations use stable IDs and canonical payload digests. Identical replay
returns existing state; changed payload under the same ID fails. Pending or
uncertain operations must reconcile against matching entity revision and current
remote observation before acknowledgement. No remote action is executed here.

## Acceptance / negative molds

Use disposable real Git repositories and SQLite files. Exercise unknown schema,
phase-specific references, untracked/missing files, stale base, unapproved model,
blocked dependency, environment failure, exhausted persistent budget, concurrent
claimers, token mismatch, packet edits, stale review/check SHA, duplicate checks,
self-review, missing integration ancestry, valid completion, duplicate operation,
changed-payload replay and uncertain-result reconciliation. Include CLI JSON errors
and process restart. Existing CLI regression checks must continue passing.

## Safety and portability

No inferred provider approval, arbitrary command execution or automatic retry of
uncertain external effects. Keep state outside committed artifacts. SQLite state
coordinates only processes sharing that same local database; separate hosts need
a coordinator service. Validate the repository root and refs using Git commands
with argument arrays, no shell interpolation. Store packets/evidence without
secrets. No SDK ABI change to consumer applications is needed.

## Trust decisions and v1 boundaries

The operator controls the approval inventory, identities, required checks and
observations. Job data cannot select shell commands. The database records local
observations and rejects inconsistent transitions, not cryptographic attestations.
A route is not permission to dispatch; a claim is not provider approval. Claim
acquisition and route validation are separate mandatory coordinator steps.
The CLI creates new databases with owner-only POSIX permissions and rejects
unknown database schema versions. State must remain outside model write scope.
Existing insecure permissions and remote-host coordination require deployment
controls. Revision and packet replacement is explicit re-planning, not mutation
of an active assignment; cross-ID retry lineage remains operator-enforced.

## Observed package validation

Built the wheel with the declared Hatchling backend, installed it into an isolated
local target, and ran all 28 tests against the installed package successfully.
The installed `job --help` exposes validation, routing, claims, completion,
checkpoints, release, attempt recording and prerequisite resolution. This is local
package evidence, not a claim about GitHub-hosted CI or remote provider integration.
