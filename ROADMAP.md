# Roadmap

This document sketches planned evolution of the Codex Automata methodology harness, templates, examples, tooling, and quality gates. Priorities may shift based on community feedback and real-world usage.

## Current

- **Version 0.1.0**: Baseline harness: specification doctrine, molds and casting metaphors across docs, bounded context guidance, agent task boundaries, interface contract discipline, Cursor integration (rules, skills, subagents, hooks), templates, examples, GitHub-oriented quality gate patterns.
- **Recovery protocol**: Formal process for closing gaps in specification, tests, or coverage after code exists. Includes gap classification taxonomy, severity-based triage, recovery sequence (audit, spec patch, mold patch, recast, re-review), kanban integration, gap assessment template, recurrence prevention, and health metrics. Wired into manifesto, playbook, agent rules, Cursor rules, and glossary.

## v0.2.0 (goals)

- Additional worked examples (for example REST API service, CLI tool) spanning specification, molds, casting, agent tasks, human review checkpoints, and flow documentation.
- Refined templates informed by reuse in real repositories.
- Community feedback folded into playbook and glossary alignment without silent interface contract churn.

## v0.3.0 (goals)

- Language-specific starter kits (Python, TypeScript, Go) with consistent molds and casting steps.
- Automated specification-to-test generation tooling where it respects frozen contracts and bounded context seams.
- A reusable CI/CD quality gate library (patterns or composable workflows) suited to methodology enforcement.

## v1.0.0 (goals)

- Stable methodology narrative and templates proven across multiple bounded contexts.
- Comprehensive example library showing diverse flows end to end.
- Tooling ecosystem (spec authoring helpers, molds, validators) interoperable with common stacks.
- Broader adoption and maintainer playbook for onboarding contributors and agent task operators.

## Future considerations

- IDE integration beyond Cursor where interface contracts and agent task models still map cleanly.
- Exploration of a formal specification language or constraint layer over natural-language specifications.
- Agent benchmarking framework tied to quality gates and human review baselines.

## Living document

This roadmap is not a commitment schedule. Version goals express direction: adjust scope only when specifications and human review signal a change in priority.
