# Model routing and job contracts

This portable routing policy has local enforcement through `codex-automata job`
commands. The CLI recommends eligible routes; it does not dispatch models. A coordinator
or human applies it using the engagement's approved provider inventory. Never
infer available credit, tools, rates, permissions or model suitability from names.

## Job taxonomy

| Job | Inputs | Required output / exit gate | Default capability |
| --- | --- | --- | --- |
| Discover | Bounded question, repository revision, constraints | Evidence, unknowns, recommended decision; no invented certainty | Economical for mechanical inspection; frontier for ambiguous synthesis |
| Architect / specify | Goal, discovery, current contracts | Versioned decisions and dependency-ordered Ready issue packets | Frontier |
| Design SDK | Reviewed behavior spec, existing types | Reviewed contract delta, compatibility and dependent-work impact | Frontier for new boundaries; proven economical for fixed mechanical changes |
| Mold tests | Reviewed spec, frozen SDK | Independent positive/negative/invariant tests and traceability | Proven economical; frontier for subtle invariants or security-sensitive design |
| Cast implementation | Ready issue, pinned contracts, molds, relevant code | Bounded diff, acceptance evidence, PR/head SHA | Cheapest proven approved hosted/local model |
| Review / audit | Pinned diff, spec, contracts, test evidence | Findings with severity, reproduction and disposition | Risk-matched reviewer; frontier for cross-system/security ambiguity |
| Integrate / release | Reviewed heads, current CI, integration/release contract | Sequential integration, cross-boundary checks, rollback and release evidence | Deterministic tooling plus approved agent; required human decisions stay human |
| Reconcile | Issues, actual heads/checks, blockers and checkpoints | Repaired dependencies/specs, next queue, routing feedback | Frontier for semantic drift; economical for mechanical bookkeeping |

A Ready job is Ready for its own phase. A Ready specification task does not
license casting before contracts and molds exist. No job may approve its own
required independent review. Agents can assist upstream work; project approval
rules still determine which decisions require a human.

## Routing decision order

1. **Authority and data:** verify the approved provider/model, environment, tools,
   data restrictions and action scope. An unapproved provider is ineligible at
   every capability tier; stronger reasoning does not grant permission.
2. **Readiness:** missing requirements, conflicting contracts or open research
   return to planning. Do not pay a stronger coder to invent product decisions.
3. **Risk and complexity:** new architecture, cross-context contradictions,
   subtle security properties or semantic reconciliation go directly to an
   approved frontier/specialist session. Routine fixed-contract implementation
   starts economical/local if it has demonstrated competence for that job class.
4. **Availability:** choose among eligible available candidates. If none exists,
   checkpoint and queue the job. Do not guess reset times or silently change
   providers. A human may explicitly select an eligible different tier.
5. **Evidence:** validate outputs against the same acceptance gate at every tier.
   A frontier result has no exemption from tests, contracts or review.

## Failure classification and escalation

| Observed failure | Action |
| --- | --- |
| Missing dependency, runner, credentials or service | Repair/queue environment work; no capability escalation |
| Ambiguous acceptance or contradictory contract | Block affected work; architect/specify with evidence |
| Repeated incorrect implementation under clear contract | Escalate capability within approved inventory and remaining attempt budget |
| New SDK boundary or cross-context/security issue | Stop affected casting; route design/audit and required human decision |
| Credits exhausted, interrupted session or unavailable model | Preserve checkpoint and worktree; resume eligible work later |
| Review failure or commit changed after review | Repair and re-review the current head; no reuse of stale approval |

Three grounded attempts per failure cluster across sessions is the default total
budget, not three attempts per model. A stronger model inherits attempts and
checkpoint. Stop earlier when classification exposes a design or authority gap.
Budget reset requires a recorded clarification or repaired prerequisite and the
project's authorized decision maker; do not reset by renaming the job.

## Required job packet and routing record

Attach these fields to the Linear issue or a linked versioned task record:

- Real issue ID/URL (or UNSYNCHRONIZED DRAFT), job kind and current phase.
- Repository, integration branch, inspected/base SHA and linked spec/contract
  sections; selected issue revision/update timestamp when available.
- Outcome, exclusions, prerequisites, allowed write paths and ownership.
- Acceptance criteria, exact verification commands, evidence and review gate.
- Approved provider/model constraint reference; selected model and routing reason.
- Risk/complexity rationale and explicit non-applicable contract/mold fields.
- Attempt count, failure classification, next escalation destination and budget.
- Session/branch/worktree, checkpoint, output head SHA and pending service writes.

Do not record secrets or infer provider approval from past unrelated engagements.
Routing records support retrospective qualification: first-pass acceptance,
rework, integration defects, escalation causes, latency and measured cost. Never
lower acceptance criteria to qualify a cheaper model. Keep model IDs and limits
in consumer configuration; keep the job and evidence contracts provider-neutral.

## Measured capability path

CLI 0.6 additionally exposes `model eligible` using versioned capability profiles
and operator-supplied real availability/capacity. Unknown metrics cannot qualify a
model; commercial names imply no hierarchy. The existing v1 tier route remains a
compatibility interface. New runtime adapters should apply capability eligibility
and task risk before dispatch. The methodology recommends, the runtime schedules.
