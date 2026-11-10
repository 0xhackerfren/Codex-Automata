# vNext delivery and validation record

Baseline: `28e36509c2632c4f9a77fc0fb9a41e9715116735` (28 Linux tests).
Release contract: CLI 0.6.0 / methodology 1.0 / schema v1.
Implementation branch: `feat/automata-vnext`. Pin the reviewed PR head's exact SHA;
the final response identifies the verified revision after publication.

## Substantive improvements

- Installation ownership and execution context are separated: namespaced managed
  assets/schemas, configurable monorepo paths, manifest, preserved consumer files,
  staged updates/migration, explicit grants and capability decisions.
- Offline engineering has exact operator-approved plans, deterministic risk floors,
  ordered phase outputs, real command receipts, protected contract/test deltas,
  reviewer-token attestations and current-head completion evidence.
- Small-model contexts have exact byte ceilings, pinned source excerpts, compact
  phase/output/tool contracts and durable supplied-context provenance.
- Recovery preserves attempts and failures across restart, release/reclaim and
  phase rewind; definition changes block active work rather than silently mutating it.
- Capability qualification and a repeatable three-arm evaluator are implemented.
  Local session evidence and child-readiness proposals require actual Git receipts.
- Retrospective amendments include two-layer molds, real fixture validation,
  authorization supersession, review policy, quota-aware closure, safe bootstrap,
  per-agent journals, gate tiers/determinism and a reusable domain spec template.

See the before/after gap assessment, adversarial audit, retrospective adoption
matrix and SWARM_INTEGRATION_HANDOFF.md for concrete evidence and residual limits.

## Observed validation

| Check | Actual result |
| --- | --- |
| `PYTHONPATH=cli python -m unittest discover -s cli/tests -q` | 73 tests pass on Linux |
| Built wheel, installed to isolated target, reran same suite against installed package | 73 tests pass |
| `PYTHONPATH=/tmp/automata-final-installed python examples/standalone_workflow_demo.py` | completed-local; six phases, six actual commands; checkpoint resumed; self-review labeled; no deployment/external service |
| Demo bounded context | maximum 3,114 bytes, budget 16,000 bytes |
| `npx markdownlint-cli2@0.20.0 --config .markdownlint.yaml '**/*.md'` | zero errors |
| Lychee 0.24.2 offline local-link check, external HTTP excluded | zero local-link errors |
| `git diff --check` and Python syntax parse | pass |
| Both workflow YAML files parsed | pass |
| Benchmark oracle regression | 8 tasks × 3 arms; 24 broken baselines rejected and 24 known solutions accepted, plus scope/budget/telemetry negatives |

Fixture oracle outcomes are evaluator tests, not model success rates. No live LLM
was run. Live-model performance, statistically meaningful effectiveness and
candidate-test-quality scoring remain pending. No next consumer campaign or
independent security review was performed here. Hosted CI results must be read
from the delivered PR; local Linux validation alone does not prove Windows passes.

## Migration and remaining weaknesses

Default `init` is intentionally migrated to the isolated layout; use explicit
`--layout legacy` for old root-copy behavior. Existing job/journal v1 remains.
Workflow jobs cannot use legacy supplied observations to bypass executor evidence.
Consumer-owned configuration survives update staging. Legacy rule ownership must
be reviewed before removing old always-on integrations; nothing is auto-deleted.

The actual runtime must isolate authority/database/processes, intercept tools,
review command meaning/impact declarations, provide genuine reviewer independence,
manage process trees, preserve cross-ID failure lineage and authenticate remote
adapters. Checkpoint exports cannot replace lost controller authority. The small
benchmark tests instruction treatments, not the entire process, until the external
live-agent study is run. No production readiness or unattended release is asserted.

## Hosted CI follow-up

The first published matrix passed both Linux versions and documentation checks,
but exposed Windows repository-path casing differences in authorization identity.
Repository grants now normalize absolute identity, Windows permission prefixes
compare without case sensitivity, and nonportable trailing-dot/space and Git
metadata aliases are rejected. Three additional regression tests cover normalized
identity, permission aliases and legacy-dependency evidence laundering. Workflow
dependencies now require executor-backed completion, while legacy v1 behavior
remains explicitly observation-only. The delivered PR head is rerun in the full
matrix; consult its current checks for final hosted status.
