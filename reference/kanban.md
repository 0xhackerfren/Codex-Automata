# Kanban for Agentic Development

Kanban maps Codex Automata to continuous flow: specifications authorize work, molds fix the acceptance shape, agents perform code casting within interface contracts, humans perform review against intent, CI/CD implements quality gates, deployment completes the loop under observation.

The method invests in visible work in process (WIP), pull based movement, explicit policies, and bottleneck diagnosis rather than rituals tuned to individuals who tire or seek coordination comfort.

## Why Scrum Does Not Fit This Model

Scrum optimizes a human team's cadence through time boxed commitments, estimation, forecasting, and synchronizing ceremonies. Agents scale differently: they do not fatigue, they benefit weakly from standups framed around social blockers, and they rarely produce trustworthy story point forecasts when molds already define correctness.

Throughput also splits across stations. Parallel agents can inflate casting completions while specification or review stays human bound. Scrum's sprint abstraction hides those station specific queues behind a single burndown metaphor.

Prefer kanban's core moves: visualize the flow of agent tasks between stations, constrain WIP to shorten feedback latency, expose aging work, negotiate explicit policies ("definition of ready" per station), and improve using operational metrics tied to molds and deployments.

Codex Automata may still schedule lightweight planning rhythms; kanban rejects sprint commitment theater as the primary throttle.

## Stations

Codex Automata aligns boards and telemetry to five canonical stations:

1. **Spec Writing.** Humans author falsifiable specifications and interface contracts inside bounded contexts. This station establishes vocabulary downstream artifacts must reuse without drift.

2. **Test Molding.** Humans and agents derive executable molds and fixtures strictly from specification language. Incomplete molding upstream creates downstream false positives about readiness.

3. **Code Casting.** Agents write implementation constrained by molds and frozen contracts for each slicing window. Humans handle escalations around ambiguity and integration merges rather than supervising every keystroke unless policy demands spot checks.

4. **Review.** Humans compare casting to specification and systemic risk posture. Review amplifies diligence; automated quality gates still block merges mechanically.

5. **Deployment.** Progressive release plus verification plus operational observation with explicit rollback posture. Automation may execute most commands; the station remains real because rollout risk concentrates blast radius.

Optionally subdivide Deployment into gated substages (`Build + gates`, staging, progressive production, observation). Keep naming tethered across teams: specification, molds, casting, human review, quality gates, rollout.

## WIP Limits (Guidelines)

Calibrate limits to team size and risk posture; adjust using cycle time and queue age signals.

| Station | Guideline limit | Purpose |
|---------|-----------------|--------|
| Spec Writing | 2 to 3 items | Preserve depth and reduce contradictory partially drafted specs that leak ambiguity into molds |
| Test Molding | 3 to 5 items | Allow parallel derivation while keeping deterministic fixtures tractable |
| Code Casting | Unlimited | Computational throughput lacks a physiological ceiling at this station |
| Human Review | 2 to 3 items | Protect thorough comparison against specification creep and checklist fatigue |
| Deployment | 1 to 2 items | Limit concurrent rollout experiments that correlate failures during attribution |

Treat "unlimited" casting pragmatically when merge thrash spikes: institute soft concurrency caps tied to branches or reviewer batch size rather than pretending integration risk stays flat as branch count climbs.

## Pull Based Scheduling

Stations downstream pull only when spare capacity meets explicit readiness rules. Test molding pulls specs once writers mark them coherent enough for fixture investment. Casting pulls molded items once contracts stabilize for the slicing window merges expect. Review pulls completed casting batches once local molds and branch policy prerequisites pass. Deployment pulls merges that cleared centralized quality gates plus human approvals where required.

Block push behavior that floods partially groomed cards into molding or casting to "keep agents busy"; idle agents should signal starvation upstream specifications or contracts deserve attention sooner.

Codify readiness at each boundary: molding ready, casting ready, review ready, deployment ready plus rollback rehearsals when policy demands them.

## Bottleneck Diagnosis

Queues visualize systemic starvation, not anecdotes about effort.

When specifications age in Spec Writing relative to molding demand, throughput is bounded by human specification work even if agents later idle sporadically at casting.

Casting buildup ahead of Review usually signals insufficient reviewer capacity, overloaded review scopes, fuzzy exit criteria for review cards, or low trust in molds that forces exhaustive manual archaeology.

Test molding buildup often signals unresolved specification ambiguity, flaky environments, reluctant contract freezes, or missing scaffolding shared across bounded contexts.

Deployment buildup often reflects environment scarcity, conservative policy after incidents, or weak progressive delivery primitives that discourage smaller safer promotions.

Elevate recurring bottlenecks into architecture or specification work when tactical staffing cannot explain the pattern.

Track rework distinctly: bounced review tickets, reopened specification sections, regenerated molds, duplicated casting attempts. Rework dominates aging when molds or specs oscillate faster than integrations absorb.

## Metrics

Operational metrics reinforce flow hygiene:

**Cycle Time.** Interval from clarified intake or refined backlog readiness through observable production effect (choose one definition per program and stay consistent).

**Throughput.** Completed items exiting Review or Deployment per interval aligned to organizational policy on what counts as done.

**WIP Age.** Elapsed time in each station; highlights stale casting branches, orphaned molds, drifting contracts, stalled reviews.

Augment flow metrics with quality signals: deployment failure rate, defect escapes, review rejection rate, mold flakiness, merge conflict frequency, contract test breakage correlated with parallel casting lanes.

Cumulative flow diagrams expose queue growth early.

Codex Automata favors these measures over story point velocity, which mis scales when agents multiply casting throughput without matching specification or review investment.

## Board Setup Instructions

Lay out columns left to right that mirror stations. Optional swim lanes group cards by bounded context or service area.

`Backlog (clarified intake) → Spec Writing → Test Molding → Code Casting → Review → Deployment → Done (observed)`

Post policies above each column: definition of ready, definition of done, escalation paths, linked ADR requirements, security review triggers, progressive delivery rules.

Tag risk class to drive mandatory reviewer pairing, deployment strategy, and kill switch expectations.

Maintain a visible blocked column with reason codes so systemic impediments surface outside chat scrollback.

## Connection to Toyota Production System and Continuous Flow

Toyota Production System themes translate directly: limit inventory (WIP), make abnormalities visible (aging cards), stop the line on defects (failing quality gates block merges), standardize work through specifications and molds, improve continuously with metrics grounded retrospectives, and respect humans by spending their attention on irreplaceable judgment while automating mechanical repetition.

Continuous flow here means small increments move across stations without batching purely for planning theater. Agents enable frequent casting batches; humans batch review only as far as WIP limits and risk policy allow, harmonizing machine scale with governance.
