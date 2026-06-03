# Multi-Agent Orchestration

This document covers how to run multiple AI agents simultaneously under Codex Automata. Multi-agent work is coordination through artifacts—specifications, frozen SDK interfaces, interface contracts, and context state—not through agent-to-agent chat.

For bounded context definitions and decomposition, see [architecture.md](architecture.md). For session handoff and who-is-working-on-what tracking, see [context-persistence.md](context-persistence.md).

## Why Multi-Agent Orchestration Matters

As of 2026, industry surveys report that a majority of developers use three or more AI tools simultaneously. Methodology vendors have responded: BMAD offers Party Mode for collaborative agent sessions; hatch3r emphasizes parallel delegation with dependency-aware orchestration. Running multiple agents is standard practice.

Uncoordinated multi-agent work breaks codebases quickly. Typical failures include:

- **Merge conflicts** from two agents editing the same files
- **Duplicated implementations** of the same building block under different names
- **Semantic contradictions** where two agents choose incompatible patterns for the same boundary
- **SDK drift** when one agent extends interfaces while another assumes the old surface

Codex Automata does not treat multi-agent work as an optional advanced topic. It provides a principled framework that uses the existing methodology—bounded contexts, interface contracts, frozen SDK, specifications, block registry, context state—as the **coordination protocol**.

## The Codex Automata Answer: SDK as Coordination Surface

Agents do not coordinate by talking to each other. They coordinate by implementing against **shared, frozen interfaces**.

The SDK constraint surface is the coordination protocol:

- Agent A implements bounded context **Orders** against `IOrderRepository` and `IPaymentGateway` as defined in the SDK.
- Agent B implements bounded context **Payments** against the same interface definitions from the read-only SDK reference.
- Neither agent needs the other’s implementation files, conversation history, or informal agreements.

When two agents work on **different** bounded contexts, the **interface contracts** between those contexts are the only point of contact. Contracts are written in Phase 1–2, reflected in the SDK in Phase 3, and frozen before casting. No direct agent-to-agent communication is needed or desired; it creates untraceable decisions.

If coordination requires changing an interface, **stop all agents** on that boundary, obtain human approval, update the specification and SDK through the normal pipeline, then resume with a single updated contract version.

## When to Use Multiple Agents

Use parallel agents when work partitions cleanly along methodology boundaries.

### Parallel bounded context implementation

Each agent owns one bounded context. All agents read the same frozen SDK and interface contracts. Integration happens through contract tests and sequential merges, not shared file edits.

### Pipeline parallelism

Different modules at different phases simultaneously—for example, one agent writes specifications for module B while another derives tests for module A after A’s spec is approved. Respect phase dependencies: do not cast code for B before B’s spec and SDK exist.

### Coder and reviewer pairs

One agent casts implementation; another performs review against specification, SDK, and test plan. The reviewer does not edit implementation in the same session; it reports findings for the caster or a human to address.

### Parallel product testing

Different user profiles exercise different journeys at the same time against a shared build. Product test objectives are independent; results aggregate into a single product test report.

## Isolation Patterns

Isolation prevents conflicts and semantic drift.

### Git worktree per agent

Give each agent its own working directory (git worktree or separate clone) following the project's declared branch strategy (Pipeline as First Citizen, Principle 12; R16). Agents do not share uncommitted working tree state. Each worktree runs its own test suite before proposing merge.

### One bounded context per agent

An agent’s write scope is limited to files belonging to a single bounded context (as defined in architecture and context state). Cross-context changes require escalation and sequential assignment, not parallel edits.

### Shared SDK as read-only reference

All agents read the same SDK version from the integration branch. Agents do not modify SDK interfaces without human approval and a coordinated pipeline pause. SDK changes are serialized through the normal Phase 3 process.

### Sequential merges

Never merge two agent branches in parallel. Merge one PR at a time into the integration branch following the merge policy declared in the architecture (Pipeline as First Citizen, Principle 12). After each merge, other agents **pull/rebase** and run tests before continuing. Parallel merges multiply conflict resolution cost and hide contract violations.

## Coordination Through Artifacts

| Artifact | Coordination role |
|----------|-------------------|
| **Specifications** | Define what each bounded context does; authoritative when merge conflicts imply semantic disagreement |
| **Interface contracts** | Define how contexts interact; both sides must honor before merge |
| **SDK (frozen)** | Shared constraint surface; version all agents implement against |
| **Block registry** | Prevents duplicate building blocks across agents |
| **Context state** | Tracks active phase, which agent owns which context, checkpoint, blockers |
| **Agent tasks** | Scoped session work with explicit spec section and test mapping |
| **Test plans** | Molds per context; failing contract tests block integration merge |

The block registry is especially important for multi-agent work. Before starting SDK or casting work, agents check the registry for existing building blocks. Duplicate abstractions across agents are a coordination failure.

## Practical Scaling Guidance

Start small and scale only when merge and review discipline stay green.

**Start with two agents:** one caster, one reviewer (or one context implementer, one spec/test deriver on adjacent modules). Verify the workflow—worktrees, PRs, sequential merge, context state updates—before adding parallelism.

**Scale to one agent per bounded context** for larger systems. Each agent owns exactly one context’s files for writing. Read access to specs and SDK is global; write access is partitioned.

**Maximum recommended:** one agent per bounded context **plus** one reviewer (or integration coordinator). Beyond that, coordination cost typically grows faster than throughput.

Research and field experience suggest **two to four parallel implementers** is the practical ceiling before coordination overhead dominates. More agents require stronger human integration ownership, not more automation.

## Anti-Patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Two agents editing the **same file** | Guaranteed merge conflicts and contradictory logic |
| Agents without **bounded context isolation** | Semantic contradictions invisible until integration |
| Agents **modifying SDK interfaces** without human approval | Breaks all other agents mid-flight |
| **Unbounded parallelism** | Coordination cost exceeds development cost |
| Agents coordinating through **chat** instead of artifacts | Untraceable decisions; no spec or contract trail |
| **Parallel merges** | Conflict storms and contract test skew |
| Duplicate building blocks | Registry bypass; incompatible types at boundaries |

## Merge Protocol

Follow this sequence for every agent completion. The merge protocol operationalizes Pipeline as First Citizen (Principle 12) and branch strategy (R16) for multi-agent work. Do not shortcut human review on contract-touching or security-sensitive work.

1. **Complete work in worktree.** All assigned tests pass; linters and quality gates clear for that agent’s scope.
2. **Open a PR** against the integration branch (not directly to main unless that is your single integration line). PR description references spec sections and bounded context.
3. **Human review** (or review agent assists with findings; human approves merge for contract and security changes).
4. **Merge sequentially.** One PR at a time. No parallel merges to integration.
5. **Other agents pull** integration branch, resolve ripple effects, re-run contract tests.
6. **If conflicts arise, specification is authoritative.** If spec is ambiguous, halt and escalate to human; do not “pick one agent’s version.”

After merge, update context state: Recently Completed, Checkpoint for waiting agents, and block registry if new blocks landed.

## Context State for Multi-Agent Work

Extend context state Current Work to make ownership explicit:

- Which bounded context each active agent owns
- Which agent tasks are in flight (task IDs)
- Integration branch name and last merged PR
- Blockers on shared contracts or SDK freeze windows

Session History should note agent identity (human or tool label) and context owned, so the next session does not duplicate work.

## Relationship to Profiles

**Essential** projects rarely run multiple implementers; quick-change and single-agent flow dominate. Multi-agent guidance still applies if two tools touch the repo—use spec traceability and avoid parallel edits.

**Standard** and **Complete** profiles assume architecture decomposition and interface contracts—the prerequisites for safe multi-agent partitioning. Complete adds product testing parallelism and stricter release gates.

## Companion Documents

- [principles.md](principles.md) — Pipeline as First Citizen (Principle 12) governs branch strategy and merge policy for multi-agent work
- [architecture.md](architecture.md) — Bounded contexts, decomposition, interface boundaries, and pipeline design
- [context-persistence.md](context-persistence.md) — Context state, checkpoint, and session handoff for parallel work
- [PLAYBOOK.md](../harness/PLAYBOOK.md) — Phase dependencies when pipeline parallelism is used
- [AGENT_RULES.md](../harness/agent/AGENT_RULES.md) — Agent halt conditions, contract freeze, gap reporting, and branch strategy (R16-R18)
- [adoption-profiles.md](adoption-profiles.md) — Profile capabilities for architecture and contracts
- [kanban.md](kanban.md) — WIP limits and flow when multiple agents pull work
- [iteration.md](iteration.md) — Inner and outer loops when agents retry after failed gates
- [recovery.md](recovery.md) — When parallel work discovers spec, mold, or contract gaps
- [quick-change.md](quick-change.md) — Single-agent shortcut; not a substitute for multi-context coordination
