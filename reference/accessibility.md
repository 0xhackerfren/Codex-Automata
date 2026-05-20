# Accessibility

This document defines how Codex Automata treats accessibility as a first-class specification constraint that flows through the entire pipeline: specification, SDK design, test molding, code casting, review, and product testing.

For terminology, see [glossary.md](glossary.md). For adoption profile requirements, see [adoption-profiles.md](adoption-profiles.md). For the overall pipeline, see [workflow.md](workflow.md).

## Why Accessibility Belongs in the Specification

Accessibility is not a testing afterthought or a nice-to-have feature. It is a specification constraint. When a specification defines user-facing behavior, the specification should also define what accessibility standards that behavior must meet. Treating accessibility as "something QA checks later" is the same anti-pattern as treating tests as "something we add after coding."

In Codex Automata, accessibility enters at the specification level and flows through the entire pipeline:

- **Specification** — WCAG success criteria cited per user-facing behavior
- **SDK** — Design tokens include accessible values (contrast-validated colors, touch-target sizes, focus styles)
- **Tests** — Accessibility molds constrain casting before implementation
- **Casting** — Implementation honors accessibility constraints from spec, design identity, and molds
- **Review** — Accessibility verified against spec and design identity commitments
- **Product testing** — Accessibility-constrained profiles test real-user experience, not only technical compliance

## WCAG as a Specification Constraint

The [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/standards-guidelines/wcag/) define four principles: **Perceivable**, **Operable**, **Understandable**, and **Robust**. For each user-facing behavior in the specification, cite the relevant WCAG success criteria. This makes accessibility requirements explicit and testable, not implicit and subjective.

### Target Levels

| Level | Role in Codex Automata |
|-------|------------------------|
| **WCAG 2.2 Level A** | Minimum for any user-facing product |
| **WCAG 2.2 Level AA** | Recommended standard; required by most regulations and compliance frameworks |
| **WCAG 2.2 Level AAA** | Aspirational for products where accessibility is a core differentiator |

Declare the target level in the design identity and reference it in the specification for each user-facing module.

## Accessibility in the Design Identity

The design identity is the aesthetic and structural contract for user-facing work. Accessibility commitments belong there alongside typography, color, and motion. Use `harness/templates/design-identity-template.md` and complete the **Accessibility Commitments** section during Phase 1 (Architecture).

Design identity accessibility commitments include:

- **Target WCAG level** — A, AA, or AAA
- **Minimum contrast ratios** — Text/background pairings validated against the design token palette (document in the WCAG Contrast Validation table)
- **Keyboard navigation** — All interactive elements reachable and operable via keyboard; visible focus; logical tab order; no focus traps
- **Screen reader support** — Semantic HTML first; ARIA only when native semantics are insufficient; meaningful alt text; labeled form inputs
- **Motion sensitivity** — Respect `prefers-reduced-motion`; no autoplay animations without controls
- **Focus management** — Visible focus indicators; logical tab order; Escape exits modals and dropdowns
- **Touch targets** — Minimum sizes for mobile (44×44 CSS pixels per WCAG 2.5.5 Target Size)

These commitments feed into SDK design tokens and test molds.

## Accessibility in Test Molding

Accessibility tests are molds. They constrain the casting just like functional tests.

- **Automated accessibility testing** (axe-core, pa11y, Lighthouse) runs in CI alongside unit tests
- **Every user-facing component** has accessibility checks: color contrast, keyboard operability, screen reader labels
- **Accessibility tests are in red state before casting**, just like functional tests
- **Accessibility regressions are quality gate failures**, not warnings

Document accessibility checks in the test plan using the **Accessibility Tests** section in `harness/templates/test-plan-template.md`. Map each check to a WCAG criterion, tool, scope, and priority (Must / Should).

## Accessibility in Product Testing

At least one product test user profile should include accessibility constraints. These profiles test whether the product is genuinely usable under accessibility constraints, not just technically compliant.

Recommended accessibility-constrained profiles:

| Profile | Constraints | What it validates |
|---------|-------------|-------------------|
| **Screen reader user** | Navigates entirely via screen reader; no visual scanning | Semantic structure, labels, landmarks, announcements |
| **Keyboard-only user** | No mouse or touch; Tab and Enter only | Reachability, operability, focus order, no traps |
| **Low vision user** | Browser zoom at 200%; relies on contrast | Contrast, reflow, text scaling |
| **Reduced motion user** | `prefers-reduced-motion` enabled | Animation alternatives, no essential motion-only cues |

Define profiles with `harness/templates/user-profile-template.md`. See the example accessibility profile at the end of that template.

For experiential verification methodology, see [product-testing.md](product-testing.md).

## Accessibility as a Quality Gate

Requirements vary by adoption profile (see [adoption-profiles.md](adoption-profiles.md)):

| Profile | Accessibility expectation |
|---------|---------------------------|
| **Complete** | Accessibility tests must pass for all user-facing modules. At least one accessibility-constrained product test profile must be defined. |
| **Standard** | Accessibility tests recommended for user-facing modules. |
| **Essential** | Accessibility is the developer's judgment call. |

At Complete profile, failing accessibility molds or product tests blocks the quality gate the same way functional test failures do.

## Common Accessibility Anti-Patterns to Avoid

- **Color as the only indicator** — Use icons or labels alongside color
- **Missing alt text or decorative-only alt on informative images** — Informative images need meaningful `alt`; decorative images use `alt=""`
- **Focus traps** — Modals and dropdowns that capture keyboard focus without Escape to exit
- **ARIA overuse** — Semantic HTML first; ARIA only when native semantics are insufficient
- **"Click here" or "Learn more" link text** — Links should describe their destination
- **Inaccessible forms** — Missing labels, no error descriptions, no input hints
- **Auto-playing media without controls** — Provide pause/stop and respect user preferences
- **Time-limited interactions without extensions** — Offer extensions or alternatives where timeouts are required

## Companion Documents

| Document | Path |
|----------|------|
| Design identity template | `harness/templates/design-identity-template.md` |
| User profile template | `harness/templates/user-profile-template.md` |
| Test plan template | `harness/templates/test-plan-template.md` |
| Product testing reference | [product-testing.md](product-testing.md) |
| Code casting rules (Cursor) | `harness/.cursor/rules/code-casting.mdc` |
