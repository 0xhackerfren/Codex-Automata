# Context Persistence

This document defines how Codex Automata projects maintain agent context across sessions. Context persistence is a first-class mechanism, not an afterthought. Without it, agents suffer context rot: the progressive loss of accumulated decisions, trade-offs, and progress that degrades effectiveness over time.

## Why Context Persistence Matters

Agents start fresh each session. They have no memory of prior conversations, partial implementations, rejected alternatives, or informal agreements made during review. Without structured state, they re-read everything, make redundant decisions, or worse, contradict previous decisions.

Context rot is the name for this degradation. It compounds across sessions:

- An agent re-decomposes architecture that was already decided in Phase 1.
- Two sessions implement incompatible patterns because neither knew the other had chosen an approach.
- Open questions from three sessions ago resurface as if they were new.
- Progress on bounded contexts is invisible; the next agent starts Phase 4 work on a module still missing its SDK.

Structured context persistence gives every session a fast, reliable answer to "where are we?" so agents spend context budget on "what do we do next?" instead of reconstructing history.

## The Context State File

Each project maintains a `context-state.md` file as the single source of truth for project status. Initialize it by copying `harness/templates/context-state-template.md` into the project root or `docs/` (pick one location per project and record it in Key File Locations).

**Session start:** The context state file is the first file an agent reads. It orients the session: active phase, current work, open decisions, checkpoint.

**Session end:** The context state file is the last file an agent updates. It hands off to the next session through the Checkpoint section and Session History.

The context state file is living documentation. It is updated frequently and kept current. Stale context state is worse than no context state because it misleads agents into confident wrong assumptions.

## Update Protocol

### When to Update

- **Mandatory:** At session end, before marking work complete or closing an agent task.
- **Recommended:** After significant milestones (phase transition, bounded context completion, gap filed, recovery unit closed, major review feedback incorporated).

### How to Update

Updates are mostly additive with selective in-place edits:

1. **Session History:** Append a new row for the session just completed. Do not delete history; trim only if the table grows unwieldy (keep the most recent 10-15 sessions).
2. **Current Work:** Update In Progress, Blocked, and Recently Completed in place. Move finished items from In Progress to Recently Completed with a date.
3. **Active Phase and bounded context table:** Update when phase or station work changes.
4. **Open Decisions:** Add new decisions; remove or resolve when humans decide. Note resolution in Session History.
5. **Known Gaps:** Add when gaps are discovered; link to gap assessments; remove or mark recovered when recovery closes.
6. **Checkpoint:** Always rewrite to reflect the exact resume point for the next session. This section must never be left stale.

### Checkpoint Discipline

The Checkpoint section is the handoff contract between sessions:

- **Resume from:** The precise location (phase, module, spec section, task ID).
- **Prerequisites met:** What the next session can assume without re-verification.
- **Next action:** The single first step the next session should take.

If an agent can only update one section, update Checkpoint.

## Context Health Checks

Run these checks at session start and during human reviews:

| Check | Condition | Action |
|-------|-----------|--------|
| Staleness | Context state not updated in more than 3 sessions | Flag for human review. Verify Checkpoint and Current Work before proceeding. |
| Phase drift | Active Phase does not match actual work | Reconcile with human before proceeding. Update Active Phase or redirect work. |
| Stale decisions | Open Decisions unchanged for more than 2 sessions | Escalate to human. Work blocked on these decisions should stay in Blocked, not proceed by assumption. |
| Missing file | No `context-state.md` exists | Create from template before any other work. Populate from available artifacts. |

Agents should surface health check failures in their session report rather than silently continuing with stale state.

## Relationship to Other Artifacts

Context state is a navigation layer, not a replacement for authoritative artifacts:

| Artifact | Answers | Context state role |
|----------|---------|-------------------|
| Specification | What are we building? | Points to spec paths; summarizes scope, not behavior |
| Architecture docs | Why these boundaries? | Lists key decisions; links for rationale |
| SDK | What building blocks exist? | Summarizes surface; links to registry |
| Test plans | What must pass? | Tracks mold status per context |
| Agent tasks | What is this session's scope? | Links active tasks to current work |
| Gap assessments | What debt exists? | Lists known gaps with links |

Context state answers **where are we?** Specifications answer **what are we building?** Do not duplicate specification content in context state. Summarize and link.

## Companion Documents

- [PLAYBOOK.md](../harness/PLAYBOOK.md) — Phase workflow and context persistence responsibilities
- [AGENT_RULES.md](../harness/agent/AGENT_RULES.md) — Agent protocol including context state read/update steps
- [workflow.md](workflow.md) — End-to-end methodology overview
- [context-state-template.md](../harness/templates/context-state-template.md) — Template for initializing `context-state.md`
- [recovery.md](recovery.md) — Gap recovery protocol; Known Gaps in context state link here
