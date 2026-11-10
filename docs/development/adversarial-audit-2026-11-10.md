# Adversarial review: vNext local enforcement

Single-agent implementation review, not independent security certification.
Reproduce with `PYTHONPATH=cli python -m unittest discover -s cli/tests -v`.
Tests use real disposable Git repositories, SQLite state and subprocess checks.

| Finding / attack | Reproduction mold | Disposition |
| --- | --- | --- |
| Agent changes plan to a no-op check | test_agent_cannot_replace_operator_approved_plan | Exact plan digest requires separate operator authority |
| Coder names an existing reviewer and fabricates approval | test_independent_review_for_standard_and_protected_delta | Exact artifact requires reviewer-token attestation |
| Legacy observation-only completion bypasses new gates | test_fabrication_missing_artifacts_skipped_phase_and_legacy_bypass | Workflow jobs rejected by legacy completion |
| Implementation lands before specification | test_implementation_before_specification_is_rejected | Early phase changes restricted to configured artifact categories |
| Fake/stale artifact, wrong phase or missing output | test_output_size_and_stale_blob_rejected; test_fabrication_missing_artifacts_skipped_phase_and_legacy_bypass | Version, identity, head, pin and ordered-transition gates |
| Review expires or code changes after checks | test_expired_review_rejected; test_stale_checks_review_and_protected_tests_rejected | Current-head executions, pins and review lifetime enforced |
| Scope creep or inconvenient test weakened | test_pinned_mold_drift_and_scope_changes; test_stale_checks_review_and_protected_tests_rejected | Actual Git diff and protected existing artifacts checked |
| Prompt injection requests policy rewrite | test_repository_prompt_injection_is_data_and_cannot_grant_policy_write | Excerpts labeled data; controller denies policy writes |
| Oversized packet/output | test_context_overflow_and_unknown_versions; test_output_size_and_stale_blob_rejected | Exact UTF-8 context/output budgets, no silent truncation |
| Reset retry budget on restart/model change | test_failure_consumes_budget_across_restart; existing control tests | Unexpected failures consume persistent attempts |
| Corrupt checkpoint/partial implementation | test_context_determinism_budget_and_resume_corruption; test_release_reclaim_keeps_partial_code_and_retry_history | Compare authoritative history; reclaim and rewind preserve state |
| Operational prompt escalates to development | test_operation_does_not_inherit_development | Grant token required, effective capability intersection |
| Stale authorization remains active | test_authority_and_supersession_observable | Superseded selected grants and token reuse denied |
| Maintenance locks itself after first authorized policy edit | test_maintenance_can_repair_multiple_assets_without_unlocking_development | Only maintenance tolerates in-progress asset changes; development stays blocked |
| Interrupted install leaves adapter behind | test_install_failure_after_adapter_creation_rolls_back | Staged namespace and created routing adapter removed on failure |
| Windows casing aliases reject legitimate grants or bypass permission prefixes | test_repository_alias_is_normalized_and_relative_identity_rejected; test_windows_permission_prefixes_do_not_depend_on_case | Canonical absolute repository identity, case-aware Windows permission comparisons and portable paths |
| Observation-only legacy completion launders a workflow dependency | test_legacy_dependency_observations_do_not_qualify_for_verified_workflow | Workflow dependencies require local-executor-backed completion |
| New methodology silently changes active phases | test_methodology_change_blocks_active_work_without_resetting_history | Definition/schema/CLI fingerprint mismatch blocks continuation |
| Shared claim launches overlapping commands or controller dies before receipt | test_running_intent_blocks_overlap_and_state_transitions; test_process_crash_retains_intent_and_requires_operator_reconciliation | Durable intent, repository lock and operator-only reconciliation |
| Reconciliation reuses an older green receipt or accepts a late result | test_reconciliation_cannot_reuse_older_passing_receipt; test_reconciled_run_rejects_late_receipt | Latest run identity must match the receipt; reconciliation consumes an attempt |
| Unapproved/unqualified/unknown model | test_unapproved_unknown_unavailable_and_security_fail_closed | Capability thresholds, approval and explicit availability fail closed |
| Benchmark accepts unauthorized patch or confuses fixtures with model results | benchmark tests | Hidden trusted oracles, scope validation, pending live results |

## Remaining boundaries

- OS/process isolation is external. An agent with arbitrary shell or database
  writes can bypass controller gates; a selftest is not interception.
- Approved commands can be semantically weak or malicious. Exit zero proves a
  command ran successfully, not sufficient coverage. Artifact prose and intended
  red reasons still require review. Test quality is not empirically scored yet.
- Reviewer tokens authenticate a controller-issued identity, not cognitive
  diversity. Operators must issue them to a genuinely separate review process.
- CLI 0.6.1 follow-up bounds captured command output and kills POSIX process
  groups on timeout, overflow and direct-child completion. Windows descendants,
  detached POSIX descendants and arbitrary disk writes still require host
  containment. See [execution contract](bounded-execution-spec.md).
- Cross-ID retry lineage, multi-host synchronization, provider attestations and
  authenticated Linear/GitHub writes remain adapter/operator responsibilities.
- Checkpoint relocation needs reviewed replan plus trusted DB restoration; exports
  cannot reconstruct lost authority. Unknown external side effects are not replayed.
- The small eight-task benchmark is not statistical evidence of improved local
  model engineering outcomes; live-model paired trials remain pending.
- Legacy root integrations must be explicitly removed/merged during migration;
  preserving them automatically is safer for files but can preserve old prompts.

These limitations are exposed in the runtime handoff and do not authorize silent
unattended merging, deployment or privilege escalation.
