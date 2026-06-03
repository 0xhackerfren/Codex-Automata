# Product Testing

This document defines how Codex Automata projects verify the assembled product by deploying AI agents that operate the application as real users would. Product testing is a verification layer that runs on the working product, not on individual modules. It tests what users experience, not what code does.

For module-level molds (unit, integration, contract tests), see the test molding phase in `PLAYBOOK.md`. For the overall pipeline, see `workflow.md` in this directory. For terminology, see `glossary.md` in this directory.

## Why Product Testing Exists

The existing mold pipeline verifies that each module satisfies its specification. Unit tests confirm individual behavior. Integration tests confirm that modules compose. Contract tests confirm that boundaries hold. All of these run against code, not against the product a user actually touches.

A system can pass every unit test, every integration test, and every contract test while still being unusable. The signup flow might require twelve clicks when three would suffice. The error message might be technically correct but incomprehensible to the target audience. The navigation might be logical to the developer who built it but opaque to a first-time user. The mobile layout might render correctly but be impossible to operate with a thumb.

These are not code defects. They are product defects. They live in the gap between "the code works" and "the product works for the people who use it." Traditional E2E testing addresses this partially by scripting user journeys: click this button, type this text, assert this element appears. But scripted E2E tests are brittle. They break when the UI changes. They test a predetermined path, not whether a user can actually find and follow that path. They measure "does the path work" but not "is the path discoverable, efficient, and humane."

Agentic product testing closes this gap. Instead of scripting steps, you give an AI agent a user profile and an objective. The agent navigates the application the way a real user would: reading labels, clicking buttons, filling forms, making mistakes, recovering from errors. If the agent cannot accomplish the objective, the product has a usability defect. If the agent accomplishes it but requires excessive effort, the product has a friction defect. The agent's journey becomes measurable evidence of product quality.

This is a capability that exists only in the agentic era. No previous testing methodology could instruct a test to "figure out how to sign up" and measure whether the experience was any good. Codex Automata treats it as a first-class verification layer.

## Core Concepts

### User Profiles

A user profile defines who the simulated user is. It is not a persona document for marketing. It is a test fixture that constrains agent behavior to simulate a specific class of user.

A user profile includes:

- **Name and role.** A label for reference (e.g., "First-time visitor," "Power user," "Accessibility-dependent user").
- **Technical literacy.** How comfortable is this user with software? Do they scan for patterns or read every label? Do they know keyboard shortcuts or rely entirely on visible UI?
- **Domain knowledge.** How much does this user understand about the problem domain? A financial analyst using a trading platform has different expectations than a retail investor.
- **Goals.** What is this user trying to accomplish in general terms? Goals shape how the agent prioritizes actions and evaluates progress.
- **Constraints.** What limitations does this user operate under? Screen reader dependency, mobile-only access, slow network, limited session time, non-native language.
- **Behavioral tendencies.** Does this user read instructions or skip them? Do they explore or follow the most obvious path? Do they recover gracefully from errors or abandon the task?

Profiles are derived from the specification's user-facing sections. If the specification defines target users, each user class should have a corresponding test profile. Use `templates/user-profile-template.md` in the harness.

### Test Objectives

A test objective defines what the agent must accomplish, stated as a goal, not a script. The distinction is fundamental.

**Scripted (traditional E2E):** Navigate to /signup. Fill in email field. Fill in password field. Click "Create Account." Assert redirect to /dashboard.

**Objective-based (product test):** As a first-time visitor, create an account and reach the main dashboard.

The scripted version tests one hardcoded path. The objective version tests whether the product enables a user to accomplish the goal by whatever path they discover. If the signup button is buried under three menus and the agent cannot find it, that is a product defect even though the signup endpoint works perfectly.

Objectives trace to specification sections the same way unit test cases do. Every user-facing behavior in the specification should have a product test objective that verifies a real user can actually exercise that behavior.

### UX Budgets

A UX budget defines quantitative thresholds for acceptable user experience during a product test. Budgets transform subjective "this feels clunky" assessments into falsifiable metrics.

- **Click budget.** Maximum number of interactions (clicks, taps, keystrokes) to accomplish the objective. If the agent requires more, the journey has excessive friction.
- **Navigation depth.** Maximum number of page transitions or view changes. Deep navigation suggests poor information architecture.
- **Backtracking count.** Number of times the agent navigates backward or returns to a previous state. Backtracking indicates confusion, misleading labels, or dead ends.
- **Error encounters.** Number of user-facing error states triggered during the journey. Frequent errors suggest poor input guidance or unclear form design.
- **Time budget.** Wall-clock time for the agent to complete the objective (normalized for agent execution speed). Exceptionally long journeys indicate friction even when click counts are acceptable.
- **Abandonment.** Whether the agent gives up before completing the objective. Abandonment is a critical failure.

Budgets are defined per objective and per profile. A power user completing a routine task should have tighter budgets than a first-time user performing initial setup. Budgets are set by humans during specification, informed by domain norms and product standards.

### Experience Signals

Beyond pass/fail and budget compliance, product tests capture qualitative signals that inform product decisions:

- **Path taken.** The sequence of pages, actions, and decisions the agent made. Compare across profiles to identify whether different user types navigate differently.
- **Hesitation points.** Where did the agent pause, re-read, or explore before acting? These indicate UI elements that are not self-evident.
- **Dead ends.** Pages or states where the agent could not find a way forward and had to backtrack. Dead ends are navigation defects.
- **Error recovery.** When the agent triggered an error, how did it recover? Did the error message guide it toward the correct action, or did it have to experiment?
- **Discovery path.** How did the agent find the feature it needed? Through navigation menus, search, help documentation, or trial and error? Discovery paths reveal information architecture quality.

These signals are not pass/fail gates. They are diagnostic data that feeds back into specification and design decisions.

## How Product Testing Fits the Pipeline

Product testing runs after the code is assembled and before (or during) deployment verification. It occupies the space between "the code works" and "the product ships."

```text
Code Casting --> Review --> Product Testing --> Deployment and Observation
                                  |
                                  v
                          Feedback to Spec / UX
```

### Relationship to Existing Phases

**Phase 4 (Test Molding)** produces module-level molds: unit, integration, contract tests. These run against code. Product test objectives are defined alongside module molds in the test plan but are not executable until the product is assembled.

**Phase 6 (Review)** verifies that castings match the specification. Product testing extends this verification to the assembled product's user experience.

**Phase 7 (Deployment and Observation)** includes smoke tests and monitoring. Product tests can serve as pre-deployment smoke tests (does the critical user journey still work?) and post-deployment verification (does the journey work in production?).

Product testing does not replace any existing phase. It adds a verification layer that no existing phase covers: the experience of operating the assembled product as a user.

### Relationship to Assembly Pressure

Assembly Pressure (Principle 11) and Product Testing are complementary but distinct. Assembly Pressure is an incremental feedback loop during development: after each cast increment, the running system is exercised under realistic conditions to catch integration failures early. Product Testing is a formal verification gate that runs the full suite of user profiles, objectives, and UX budgets against the assembled product before deployment. Pipeline as First Citizen (Principle 12) provides the delivery infrastructure that makes both repeatable: product tests are pipeline stages designed at architecture time, not ad hoc manual runs.

Assembly Pressure asks "does the assembly hold together?" Product Testing asks "is the assembled product good to use?" Assembly Pressure may run a subset of product test objectives as smoke tests after each cast increment, but it does not replace the full Product Testing pass. Think of Assembly Pressure as continuous integration for the user experience, and Product Testing as the acceptance gate.

### When Product Tests Run

**Pre-merge (CI gate).** Critical journey objectives (signup, core workflow, payment) run as quality gates on integration branches, configured as pipeline stages per Pipeline as First Citizen (Principle 12). These are the product equivalent of unit test gates.

**Staging environment.** Full product test suites run against staging after deployment. This catches experience regressions that module-level tests cannot detect.

**Production (canary).** A subset of product tests run against production canaries during progressive rollout. If a journey breaks in production, the canary fails before full rollout.

**Scheduled (regression).** Product test suites run on a schedule against the live product to detect experience degradation from data growth, configuration drift, or third-party changes.

## Defining Product Tests

Product tests are defined in a product test template (`templates/product-test-template.md` in the harness). Each test specifies:

1. **The user profile** that the agent will adopt (reference to a user profile document).
2. **The objective** the agent must accomplish, stated as a goal.
3. **Preconditions** for the test (clean account, seeded data, specific environment state).
4. **Success criteria** that define completion (what state must the product be in when the objective is met?).
5. **UX budgets** for the journey (click budget, navigation depth, backtracking, time).
6. **Specification traceability** linking the objective to spec section(s).

### Writing Good Objectives

**Good objectives** are goal-oriented and user-centric:

- "As a new user, create an account and see a personalized dashboard."
- "As a returning user, find and re-order a previous purchase."
- "As an admin, invite a new team member and verify they can access the shared workspace."
- "As a screen-reader user, navigate from the homepage to the pricing page and identify the enterprise tier."

**Bad objectives** are implementation-aware or scripted:

- "Click the signup button in the top-right corner." (Tests a specific UI location, not a user goal.)
- "Navigate to /api/users and POST a new user." (Tests an API, not a user experience.)
- "Fill in the form fields in order." (Prescribes a path instead of an outcome.)

### Setting UX Budgets

Budgets should be grounded in product standards and competitive benchmarks, not arbitrary numbers. Consider:

- Industry norms for the task type (e.g., e-commerce checkout averages 4-6 steps).
- Accessibility standards (WCAG requires that all functionality be operable through a keyboard interface).
- Your own product's stated experience goals from the specification.
- Progressive tightening: start with generous budgets, measure baselines, then tighten as the product matures.

A budget that no real user could meet is useless. A budget so generous it never fails is also useless. Calibrate using initial agent runs as baseline data, then set budgets as quality commitments.

## Agent Behavior During Product Tests

The agent operating a product test is not the same as the agent writing code. It operates under a different set of constraints:

- **The agent uses the product through its user interface.** Browser tools, screen readers, mobile emulators, or API clients depending on the profile. It does not access internal code, databases, or admin tools unless the profile explicitly grants that access.
- **The agent follows the user profile's behavioral model.** A "cautious first-time user" reads labels and explores tentatively. A "power user" looks for shortcuts and keyboard navigation. The profile constrains the agent's strategy.
- **The agent does not use knowledge of the implementation.** It knows what the user profile would know: what is visible on screen, what the product's help documentation says, what a reasonable person in that role would expect. It does not know internal routes, hidden features, or implementation details.
- **The agent records its journey.** Every action, observation, hesitation, error, and recovery is logged. The journey log is the test artifact, equivalent to a test report for module-level molds.
- **The agent reports honestly.** If it cannot accomplish the objective, it reports exactly where it got stuck, what it tried, and why it believes the product blocked it. This report is diagnostic data for the specification and design team.

## Metrics and Quality Gates

### Gate Metrics (Pass/Fail)

- **Objective completion.** Did the agent accomplish the stated goal? Binary pass/fail.
- **Budget compliance.** Did the journey stay within all UX budgets? A budget violation is a gate failure.
- **Critical error absence.** Did the agent encounter any critical errors (crashes, data loss, security failures) during the journey?

### Diagnostic Metrics (Informational)

- **Click count.** Total interactions to complete the objective.
- **Navigation depth.** Page transitions or view changes.
- **Backtracking rate.** Backward navigations as a fraction of total navigations.
- **Time to completion.** Normalized wall-clock time.
- **Error encounter rate.** User-facing errors per journey.
- **Confusion index.** A composite of hesitation points, re-reads, and exploratory actions that did not advance the objective. Higher values indicate less intuitive UX.
- **Path variance.** When multiple profiles complete the same objective, how different are their paths? High variance may indicate that the product's navigation model is inconsistent.

### Tracking Over Time

Product test metrics tracked over releases reveal experience trends:

- **Friction creep.** Click counts or navigation depth increasing over time for the same objective.
- **Accessibility regression.** Constrained profiles (screen reader, keyboard-only) failing objectives that unconstrained profiles complete.
- **Onboarding degradation.** First-time user profiles taking longer or backtracking more as features accumulate.

These trends feed back to specification and architecture. If onboarding friction is climbing, the specification should address it. If accessibility is regressing, the molds should encode accessibility requirements more sharply.

## Relationship to Other Test Types

Product testing does not replace existing test types. It covers a distinct layer:

| Test type | What it verifies | Runs against | When |
|-----------|------------------|-------------|------|
| Unit tests | Individual module behavior | Code | Before casting (red state) and after |
| Integration tests | Module composition | Assembled modules | After casting |
| Contract tests | Boundary compliance | Interface boundaries | After casting, in CI |
| Product tests | User experience quality | Running application | After assembly, in staging/production |

Product tests depend on all other test types passing first. If unit tests fail, there is no product to test. Product tests are the outermost ring of verification.

## Feedback to Specification

Product test results are a primary input to specification revision. When a product test reveals a UX defect:

1. **Diagnose.** Is the defect in the specification (the spec said to build it this way), the implementation (the code does not match the spec), or the design (the spec needs to change)?
2. **Route.** Specification defects go back to Phase 2. Implementation defects go back to Phase 5. Design defects require human judgment about whether and how to revise the specification.
3. **Update budgets.** If a journey consistently uses fewer interactions than its budget, tighten the budget to lock in the improvement. If a justified design change increases interactions, update the budget with rationale.

Product test feedback is the primary mechanism by which user experience quality enters the specification-first pipeline. Without it, specifications define what the system does but not whether it is good to use.

## Companion Documents

- `workflow.md` in this directory for end-to-end pipeline context.
- `principles.md` in this directory for foundational principles product testing enforces.
- `recovery.md` in this directory for handling gaps discovered through product testing.
- `kanban.md` in this directory for flow and WIP management.
- `PLAYBOOK.md` in the harness for phase-by-phase execution guidance.
- `templates/product-test-template.md` in the harness for defining product test scenarios.
- `templates/user-profile-template.md` in the harness for defining test user profiles.
