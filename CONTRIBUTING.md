# Contributing to Codex Automata

Thank you for helping improve Codex Automata. This repository holds the methodology, templates, examples, and agent guidance for specification-first, SDK-constrained, test-molded workflows.

## How to Contribute

1. Fork this repository on GitHub.
2. Create a branch for your change. Use a clear name tied to the work (for example `docs/agent-rules-clarification` or `templates/add-go-starter`).
3. Open a pull request (PR) against the appropriate default branch. Describe what changed and why, and link related issues.

## Contribution Types

- **Methodology improvements**: clarifications or extensions to doctrine, playbook sections, bounded context boundaries, flow definitions, or quality gate expectations documented in specs and docs.
- **Template improvements**: updates to reusable project templates while preserving frozen interface contracts unless the specification is updated intentionally.
- **Documentation fixes**: typos, broken links, structural fixes, glossary alignment with specification and mold terminology.
- **Example additions**: new worked examples that demonstrate the full pipeline (specification, SDK, mold, casting, agent task boundaries, human review touchpoints).

## Style Guide

- Do not use emojis in contributed text.
- Do not use em dashes. Prefer commas, semicolons, colons, or parentheses for breaks and lists.
- Use crisp, precise, technical prose. Avoid hype or startup fluff.
- Use terminology consistently: research, specification, SDK, constraint surface, building block, local-first, mold, casting, bounded context, interface contract, quality gate, agent task, human review, flow.

## Pull Request Requirements

- Summarize **what changed** and **why** it aligns with Codex Automata doctrine.
- **Link to a relevant issue** when one exists so reviewers can trace scope.
- Follow existing conventions in file layout, heading style, cross-references (`docs/`, `agent/`, `templates/`).
- Prefer small, reviewable PRs scoped to one concern where practical.

## Repository Layout

- `harness/` is the canonical source for everything that gets copied into new projects: templates, agent rules, Cursor integration, GitHub configuration, and the playbook.
- `reference/` contains methodology documentation (principles, workflow, architecture patterns, glossary). Read-only reference material.
- `examples/` contains worked examples demonstrating the full pipeline.
- Root files (`MANIFESTO.md`, `README.md`, `LICENSE`, etc.) describe and govern the Codex Automata project itself.

## Scope of this repository

This is a **methodology harness** repository, not an application library. Contributions should improve the harness, templates, documentation, examples, or IDE integration paths. Functional product code belongs in repositories that consume these artifacts, unless an example expressly requires executable casting for illustration.

## Code of Conduct

All participants agree to uphold the expectations in [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Report concerns by opening a GitHub issue describing the incident and context, or via the escalation path described there.
