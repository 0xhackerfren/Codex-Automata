# Qualification and evaluation v1

## Capability eligibility

`model eligible --inventory inventory.json --request requirements.json` filters
operator-provided model profiles using approval, data classification, phase,
execution location, availability, context capacity, RAM, measured sample count,
structured-output/tool reliability, coding acceptance, regressions, measurement
age and security eligibility. Unknown metrics fail relevant thresholds. It emits
eligibility only, never schedules compute or infers unused credits. Inspect the
bundled `model.schema.json`; request fields are documented by
`qualification.eligible`. Existing v1 two-tier routing remains compatible but
is coarse; new runtimes should use capability eligibility before claiming work.

Profiles include identity/version/provider, local/external, approval, availability,
context limit in bytes, structured output/tool/coding rates, failure/regression
rates, sample counts, security sample count/eligibility, measured throughput
(nullable), RAM/accelerator requirements and measurement provenance digest/date.
These are trusted inventory observations, not authenticated model certifications.
All unit-test profiles are explicitly synthetic fixtures. None qualifies a real
model. Prefer the cheapest qualified approved local candidate; ambiguous/high-risk
work needs separately demonstrated capability. No name grants permission.

## Reproducible three-arm evaluation

```bash
codex-automata benchmark corpus
codex-automata benchmark prepare --task bounded-bug --arm bare --output /eval/bug-bare --budget 16000
codex-automata benchmark prepare --task bounded-bug --arm concise --output /eval/bug-concise --budget 16000
codex-automata benchmark prepare --task bounded-bug --arm automata --output /eval/bug-automata --budget 16000
# Run the same approved external coding agent/model against each context.json.
# It edits only that run's candidate/ directory under the same time/token/tool cap.
codex-automata benchmark evaluate --output /eval/bug-automata --telemetry /eval/telemetry.json
```

Corpus categories: trivial, bounded bug, feature, refactor, API, multiple modules,
security fix and intentionally ambiguous task. Every arm has identical starting
files, task, allowed paths, evaluator and context ceiling. Only instructions vary:
bare task, concise conventional rules, or bounded Automata phase guidance. Prepare
fails if the treatment exceeds the equal budget. Gold solutions validate evaluator
behavior only; never supply them to the coding agent. Held-out acceptance and
regression subprocesses run outside the candidate tree, so deleting candidate
tests cannot turn acceptance green. Unexpected file changes fail acceptance.

This first harness measures the **instruction treatment**, not a full causal
comparison of every controller gate. For a full-process experiment, separately
apply actual workflow plans/grants and collect their receipts in the Automata arm;
report that additional treatment and overhead explicitly. The tiny synthetic
corpus is a smoke suite, not a statistically adequate engineering benchmark.

Live-model path: an external approved local-agent driver reads `context.json`,
uses its existing inference/tool loop to edit `candidate/`, and emits telemetry
conforming to `benchmark.schema.json`. This repository intentionally does not
implement inference serving or a second agent runtime. Pin model identity/version,
sampling settings, hardware, corpus digest and runtime driver revision; randomize
arm order, reset candidate directories, and use repeated paired trials. Keep
context/time/token/attempt/tool/human budgets equal. Never change or expose evaluator
oracles during a run. Use a disposable sandbox: candidate Python executes real code.
The evaluator is a correctness tool, not protection from malicious candidate code.

Outputs include observed correctness, acceptance/regression results, unauthorized
changes, exact context bytes and evaluation wall time. Telemetry supplies model
version, attempts, tokens (nullable when unmeasured), agent wall time and human
interventions. First-pass acceptance stays null without telemetry. Telemetry is
labeled driver-supplied, not authenticated. Test quality is explicitly **not scored**:
add independent test review/mutation testing before claiming that metric. Passing
oracle scenarios is bounded specification compliance, not proof of full correctness.

Actual deterministic verification: 8 tasks × 3 arms, each initial broken baseline
rejected and each known solution accepted. Those 48 evaluator outcomes plus scope,
telemetry and budget negatives are regression tests of this harness. Live model
measurements remain pending. Do not use fixture acceptance rates as model results
or claim the methodology improves outcomes until the live paired study is run.
