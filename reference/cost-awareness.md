# Cost-Aware Development

This document defines how Codex Automata teams monitor, estimate, and control the token and compute cost of agent-assisted development. Cost awareness is not optional for production adoption: it determines whether the methodology scales or stalls after the first sprint.

For iteration attempt budgets, see [iteration.md](iteration.md). For profile scope and ceremony, see [adoption-profiles.md](adoption-profiles.md). For agent operating constraints, see `harness/agent/AGENT_RULES.md`. For parallel work economics, see [multi-agent.md](multi-agent.md).

## Why Cost Matters

Industry surveys consistently report that a large majority of AI-assisted projects fail to scale past pilots. **Inability to monitor and control costs** ranks among the top blockers—not lack of model capability.

Running multiple agents across a full Codex Automata pipeline consumes significant tokens: specifications, SDK design, test molding, casting, review, and product testing each load context into the model. Without cost awareness, teams fall into two failure modes:

- **Overspend** — Running frontier models for every task, loading entire repositories into context, and running marathon sessions that accumulate useless chat history.
- **Underspend** — Avoiding agents entirely out of cost fear, losing the quality gates and traceability the methodology provides.

Codex Automata is designed to make **informed** cost decisions: bounded contexts, SDK constraint surfaces, checkpoint re-dispatch, and profile tiers each reduce waste while preserving quality.

## Token Budget Estimation by Phase

Estimates below are **rough orders of magnitude** for a typical module. Actual cost varies with codebase size, spec length, number of iteration attempts, and model pricing. Use these for planning and retrospectives, not invoicing.

| Phase | Typical Context | Estimated Tokens | Model Tier |
|-------|----------------|-----------------|------------|
| 0: Intake | Project description, constraints | 5–15K | Standard |
| 1: Architecture | Existing codebase context, design docs | 20–50K | Frontier |
| 2: Specification | Domain knowledge, existing specs | 10–30K | Standard |
| 3: SDK Design | Spec + architecture + existing SDK | 15–40K | Standard |
| 4: Test Molding | Spec + SDK interfaces | 10–30K | Standard |
| 5: Code Casting | Spec + SDK + tests + existing code | 50–150K | Frontier |
| 6: Review | All artifacts for the module | 30–80K | Standard |
| 6b: Product Testing | App context + user profiles | 20–50K per journey | Standard |
| 7: Deployment | Checklist + environment config | 5–15K | Standard |

**Casting (Phase 5)** is usually the most expensive phase per module because it combines spec, SDK, tests, and implementation context. **Architecture (Phase 1)** is the highest reasoning load per session. Plan frontier model budget accordingly.

Multiply by module count and iteration attempts for project-level estimates. A three-attempt inner loop on casting can approach **3×** the Phase 5 row before escalation.

## Cost-Aware Task Decomposition

The methodology's **bounded-context** model naturally controls costs:

- Each **agent task** is scoped to one context, limiting what must fit in the context window.
- The **SDK constraint surface** means agents read interfaces and types—not every implementation file in the repository.
- **Interface contracts** define boundaries; agents do not need other modules' internals to cast or test their module.

Decomposition is a cost strategy: ten small tasks with fresh checkpoints are often cheaper than one task that loads the entire monolith and chat history.

## Model Tiering

Not every phase needs the most expensive model.

**Phases that benefit from frontier models**

- Architecture (complex reasoning, trade-off analysis)
- Code casting (implementation requires deep understanding of spec, tests, and existing code)
- Complex **recovery** when gaps span multiple artifacts and require synthesis

**Phases that work well with standard models**

- Specification writing (structured output from templates)
- Test molding (pattern application against spec and SDK)
- Review (checklist verification against artifacts)
- Context state updates (structured edits to `context-state.md`)

**Phases that work with small / economical models**

- Linting and formatting
- Simple context state field updates
- Commit message lint, spec section cross-reference checks (when scripted)

**Escalation pattern:** Start with the smallest viable model (local-first). Escalate only when a task fails acceptance criteria after bounded attempts. See [iteration.md](iteration.md) for attempt budgets and when escalation means human handoff, not a fourth model call.

## How Local-First Connects to Cost

The **local-first** principle (R12 in `AGENT_RULES.md`) is inherently cost-conscious:

- **Smaller context windows** mean fewer tokens per request.
- **Modular tasks** mean shorter sessions and less accumulated noise.
- **Structured prompts and templates** mean less wasted generation re-explaining format.
- **Artifact pipeline** means the next session reads files, not a 200K-token chat transcript.

The methodology's architecture is cost-optimized by design when teams follow checkpoint discipline and SDK boundaries.

## Cost Optimization Patterns

| Pattern | What it does |
|---------|----------------|
| **Semantic caching** | Cache spec and SDK reads across tasks in the same session; avoid re-uploading unchanged sections |
| **Context pruning** | Include only the relevant spec section and module SDK—not the full spec or full repo |
| **Checkpoint-based re-dispatch** | Use `context-state.md` to start fresh sessions instead of accumulating conversation context |
| **Attempt budgets** | The iteration protocol's **3-attempt** inner-loop limit implicitly caps per-problem spending |
| **Parallel bounded contexts** | Multiple cheaper agents on separate modules are often cheaper than one expensive long session on everything |

Avoid "just one more message" loops that duplicate artifact content already on disk.

## Monitoring Recommendations

Track these metrics at team or project level (tooling varies by provider):

| Metric | Why it matters |
|--------|----------------|
| **Tokens per phase per module** | Identifies expensive phases (often casting) |
| **Tokens per iteration attempt** | Identifies problematic areas that consume retries |
| **Cost per bounded context** | Surfaces modules disproportionately expensive to build |
| **Model tier per phase** | Detects frontier overuse where standard would suffice |

Review metrics at **retrospectives** and profile upgrades. If Complete profile product testing dominates cost, prioritize critical user journeys first.

## Profile Cost Context

Estimated **agent cost per module** (illustrative USD ranges; highly variable):

| Profile | Relative cost | Typical range per module | Notes |
|---------|-----------------|--------------------------|-------|
| **Essential** | Low | $0.50–$5 | 3–5 phases active; standard model sufficient for most tasks |
| **Standard** | Moderate | $2–$15 | Full pipeline; mix of standard and frontier models |
| **Complete** | Higher | $5–$30 | Full pipeline plus product testing and design identity; product testing adds **$1–$5 per user journey** |

See [adoption-profiles.md](adoption-profiles.md) for capability trade-offs, not only cost.

## Anti-Patterns

- **Frontier-by-default** — Using the largest model for test molding and context updates.
- **Whole-repo context** — Pasting implementation from unrelated bounded contexts.
- **Chat as memory** — Long threads instead of checkpoint re-dispatch.
- **Unbounded iteration** — More than three attempts without human escalation.
- **Complete profile on every spike** — Match profile to risk; upgrade at phase boundaries.

## Companion Documents

- [iteration.md](iteration.md) — Inner-loop attempt budget, token budget guidance, cost dimension on retries
- [adoption-profiles.md](adoption-profiles.md) — Essential, Standard, Complete scope and estimated cost
- [multi-agent.md](multi-agent.md) — Parallel agents and merge cost trade-offs
- [context-persistence.md](context-persistence.md) — Checkpoint re-dispatch and session handoff
- [principles.md](principles.md) — Local-first (Principle 8)
- `harness/agent/AGENT_RULES.md` — R12 and cost-conscious core principle
- `harness/PLAYBOOK.md` — Phase boundaries for planning token load
