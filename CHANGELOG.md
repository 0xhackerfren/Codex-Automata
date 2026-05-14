# Changelog

All notable changes to this project are documented here.

Format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to semantic versioning concepts where versioning applies to the methodology harness and documented releases.

Types of changes: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**.

## [Unreleased]

### Added

- Recovery protocol (`reference/recovery.md`): formal process for closing gaps in specification, tests, or coverage after code already exists. Covers discovery triggers, gap classification (spec gap, mold gap, coverage erosion, contract gap), severity-based triage, the five-step recovery sequence (audit, spec patch, mold patch, recast, re-review), kanban integration, recurrence prevention, and health metrics.
- Gap assessment template (`harness/templates/gap-assessment-template.md`): structured template for documenting discovered gaps during recovery.
- Recovery acknowledgment in `MANIFESTO.md` Section VII (The Fracture Lines): recognizes that gaps are inevitable and defines recovery as the methodology applied in reverse.
- Recovery procedure in `harness/PLAYBOOK.md`: expanded Iteration and Feedback section with recovery sequence, exit criteria, human and agent responsibilities, and kanban treatment.
- Agent rules R11 (halt and report gaps) and R12 (recovery task behavior) in `harness/agent/AGENT_RULES.md`.
- Retroactive gap discovery failure mode in `reference/agent-operating-model.md`.
- Retroactive Gap Discovery section in `reference/workflow.md` feedback loops.
- Recovery terms added to `reference/glossary.md`: contract gap, coverage erosion, gap assessment, mold gap, recovery, spec gap.
- Recovery constraint and terminology added to `harness/.cursor/rules/codex-automata.mdc`.

## [0.1.0] - 2026-05-11

### Added

- Initial repository scaffold, manifesto, playbook, documentation, templates, example project, agent rules, Cursor IDE integration (rules, skills, subagents, hooks), and GitHub configuration.
