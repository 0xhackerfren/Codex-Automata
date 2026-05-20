# Adoption Profiles

Codex Automata is designed to be adopted incrementally. Not every project needs every artifact, and not every team is ready for the full methodology on day one. Adoption profiles define which components of the harness are active for a given project, enabling teams to start small and scale up as they see value.

## Why Profiles Exist

The full Codex Automata pipeline includes ten principles, eight phases, dozens of templates, agent rules, quality gates, and specialized workflows like recovery and product testing. For a solo developer building a side project, this is overwhelming. For a regulated enterprise building a payments platform, it may not be enough.

Profiles solve this by defining three tiers of adoption. Each profile specifies which phases run, which templates are required, which rules are enforced, and which quality gates apply. Projects declare their profile at intake (Phase 0) and can upgrade at any phase boundary.

## Profile Definitions

### Essential

**For:** Solo developers, prototypes, hackathons, small projects, teams trying the methodology for the first time.

**Philosophy:** Get the core loop right. Specification, tests, code. Everything else is optional but available.

**Active phases:**
- Phase 0: Intake (simplified: project name, goal, constraints)
- Phase 2: Specification Writing
- Phase 4: Test Molding
- Phase 5: Code Casting
- Phase 6: Review (self-review checklist)

**Skipped phases:**
- Phase 1: Architecture (implicit for small scope)
- Phase 3: SDK Design (no separate SDK; types live alongside code)
- Phase 6b: Product Testing (optional manual verification)
- Phase 7: Deployment (out of scope for the methodology at this tier)

**Required templates (3):**
- `spec-template.md`
- `test-plan-template.md`
- `agent-task-template.md`

**Active rules (4):**
- R1 (spec before code)
- R4 (do not bypass tests)
- R8 (surface ambiguity)
- R10 (every task maps to spec and test)

**Quality gates:**
- All tests pass
- Specification exists for every module

**Accessibility:** Developer's judgment call. No required accessibility molds or product test profiles.

**What you skip:** SDK constraint surface, bounded context decomposition, interface contracts, kanban flow management, product testing, design identity, recovery protocol, context persistence.

**When to upgrade:** When the project grows beyond a single bounded context, when multiple agents or developers work on it simultaneously, or when you need interface contracts between modules.

**Brownfield adoption:** Start here. Apply to a single high-risk module. Spec + tests + code only. See [brownfield-onboarding.md](brownfield-onboarding.md).

**Estimated agent cost per module:** Low. 3-5 phases active, standard model sufficient for most tasks. Typical: $0.50-$5 per module depending on complexity.

---

### Standard

**For:** Teams of 2-10, production applications, projects with defined architecture, most professional work.

**Philosophy:** Full pipeline minus the heaviest verification layers. All principles active. SDK constraint surface enforced.

**Active phases:**
- Phase 0: Intake (full)
- Phase 1: Architecture and Decomposition
- Phase 2: Specification Writing
- Phase 3: SDK Design
- Phase 4: Test Molding
- Phase 5: Code Casting
- Phase 6: Review (full human review)
- Phase 7: Deployment and Observation

**Skipped phases:**
- Phase 6b: Product Testing (recommended but not required)

**Required templates (all standard):**
- `spec-template.md`
- `test-plan-template.md`
- `agent-task-template.md`
- `interface-contract-template.md`
- `architecture-decision-record.md`
- `module-boundary-template.md`
- `context-state-template.md`
- `block-registry-template.md`

**Active rules:** R1-R13, R14, R15

**Quality gates:**
- All tests pass
- Specification exists for every module
- SDK interfaces cover all public module boundaries
- Interface contracts verified
- Context state file is current

**Accessibility:** Accessibility tests recommended for user-facing modules. See [accessibility.md](accessibility.md).

**What you skip:** Product testing (Phase 6b), design identity (unless the project has user-facing surfaces), progressive UX budgets.

**When to upgrade:** When you ship user-facing products where experience quality matters, when regulatory or compliance requirements demand full traceability, or when product testing would catch defects that code-level testing misses.

**Brownfield adoption:** Upgrade when 3+ modules are onboarded and you need SDK interfaces and contracts between them. See [brownfield-onboarding.md](brownfield-onboarding.md).

**Estimated agent cost per module:** Moderate. Full pipeline, mix of standard and frontier models. Typical: $2-$15 per module.

---

### Complete

**For:** Enterprise teams, regulated industries, products where UX quality is a competitive differentiator, teams that want maximum coverage.

**Philosophy:** Everything. Every principle, every phase, every quality gate. Full traceability from research through deployment.

**Active phases:** All (Phase 0 through Phase 7, including Phase 6b)

**Required templates:** All templates in the harness, including:
- All Standard templates
- `product-test-template.md`
- `user-profile-template.md`
- `design-identity-template.md`
- `gap-assessment-template.md`

**Active rules:** All (R1-R15)

**Quality gates:**
- All Standard gates
- Product test objectives pass for all critical user journeys
- UX budgets met for all defined profiles
- Accessibility tests pass for all user-facing modules; at least one accessibility-constrained product test profile defined. See [accessibility.md](accessibility.md).
- Design identity compliance verified (no slop fingerprints)
- Divergence gates pass
- Recovery protocol active for all discovered gaps
- Context state updated at every phase boundary

**What you get:** Full methodology coverage. Every gap is caught. Every decision is traceable. Every user journey is verified. The cost is higher ceremony per change, justified by the value of what you are building.

**Brownfield adoption:** Upgrade when the full system is onboarded and you want product testing, design identity, and full quality gates. See [brownfield-onboarding.md](brownfield-onboarding.md).

**Estimated agent cost per module:** Higher. Full pipeline plus product testing and design identity verification. Typical: $5-$30 per module. Product testing adds $1-$5 per user journey.

## Declaring a Profile

Profile is declared during Phase 0 (Intake). Add a `Profile` field to the intake document:

| Field | Value |
|-------|-------|
| Profile | Essential / Standard / Complete |

The profile determines which phases the PLAYBOOK activates, which templates the init script copies, and which rules agents enforce.

## Upgrading Profiles

Profiles can be upgraded at any phase boundary. To upgrade:

1. Update the intake document's Profile field.
2. Create any newly required artifacts (e.g., upgrading from Essential to Standard requires adding SDK interfaces and interface contracts for existing modules).
3. Run the recovery protocol for any gaps the upgrade reveals (existing code without SDK interfaces is an SDK gap).
4. Update the context state file to reflect the new profile.

Downgrades are not recommended. Removing artifacts that exist creates orphaned documentation. If a profile is too heavy, reduce scope within the profile rather than downgrading.

## Profile Comparison Matrix

| Capability | Essential | Standard | Complete |
|-----------|-----------|----------|----------|
| Specification | Required | Required | Required |
| SDK constraint surface | Skip | Required | Required |
| Test molding | Required | Required | Required |
| Interface contracts | Skip | Required | Required |
| Architecture decomposition | Skip | Required | Required |
| Human review | Self-review | Full review | Full review |
| Product testing | Skip | Optional | Required |
| Design identity | Skip | If user-facing | Required for user-facing |
| Recovery protocol | Skip | Active | Active |
| Context persistence | Skip | Required | Required |
| Kanban flow | Skip | Recommended | Required |
| Quality gates | Basic (2) | Standard (5) | Full (7+) |
| Templates | 3 | 7+ | All |
| Active rules | 4 | All | All |
