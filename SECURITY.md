# Security Policy

Codex Automata is a methodology and template repository: documentation, specifications, molds, workflows, and configuration for agent-assisted development. It is **not** a deployable runtime or application library.

## Supported versions

| Version | Supported          |
|---------|---------------------|
| 0.1.x   | Supported            |

Older or unreleased branches are not formally supported unless explicitly marked.

## Reporting a vulnerability

If you believe you have identified a security-relevant concern:

1. **Preferred for general cases**: open a **private** GitHub security advisory if the repository enables it; otherwise open a GitHub issue with a clear summary and reproduction context. Do **not** include exploit code in public issues if it could harm others without consent.
2. **Sensitive disclosures**: email the maintainers if your issue must not appear in public (for example, credentials exposure or supply-chain details). Use a subject line that indicates security (for example `[SECURITY] Codex Automata`). If no dedicated security email is listed in the repository profile or organization docs, open a minimally descriptive public issue requesting a private channel.

Include affected paths (for example workflows under `.github/`), reproduction steps if applicable, and impact you assess.

## What "security surface" means here

This repo does **not** ship executable product code intended for production runtimes under normal use. Typical concerns include:

- **CI/CD workflow integrity**: GitHub Actions definitions, pinned actions, secrets usage patterns, fork PR workflow behavior.
- **Supply chain**: dependencies declared for tooling or CI; third-party action versions; submodule or scripted fetch behavior if present.

If you report outdated actions or insecure patterns in workflows, cite the workflow file path and suggested remediation when possible.

## Response expectations

Maintainers aim to acknowledge reports in a reasonable timeframe. Severity and fix timeline depend on impact and reproducibility. This repository's risk profile is bounded by docs and harness assets; escalation paths match that scope.
