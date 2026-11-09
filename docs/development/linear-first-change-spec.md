# Linear-first delivery change specification

Status: implementation contract for this repository change. No external issue is claimed.

## Intent and scope

Make scarce frontier sessions produce durable, executable Linear work while
approved economical or local agents implement bounded tasks between sessions.
Keep the twelve principles and existing pipeline phases. Add a delivery cadence,
not a replacement methodology or automatic model dispatcher.

Linear owns scope, priorities, dependencies, issue acceptance and status. Git owns
versioned specifications, ADRs, SDK contracts, tests and implementation evidence.
Issues link exact contract revisions. Conflicts block affected work until reconciled.

Ship portable instructions, an issue template, session prompts, a project brief,
and a queue template in every adoption profile. Support offline drafts without
pretending they are synchronized. Supersede only conflicting authority/routing
statements in the older proposal; its unimplemented coordinator stays proposed.

## CLI safety contract

- Init preflights all selected top-level destinations. Any existing destination,
  including a symlink, fails before writing. Existing unrelated source is preserved.
  Users rehearse and merge adoption changes from a separate directory.
- Both shell initializers delegate to the Python implementation to avoid drift;
  they retain their documented profile arguments. Hidden Cursor/GitHub content ships.
- Verify fails when either required enforcement script is missing or cannot run.
  It remains a structural check, not proof of application acceptance.
- Python CI chooses one runner; installation or test failures cannot fall through
  to a different runner or a successful echo. Unknown stacks fail visibly.
- Updating an existing project stages a complete upstream candidate in a new,
  separate directory. It never overwrites customized rules, hooks or CI in place.
  Users review and merge the staged diff. Profile/agent selection stays explicit.

## Verification molds

Use stdlib unittest with disposable targets. Cover all profile/agent pairs,
portable delivery files, hidden directories, collision no-write behavior, unrelated
source preservation, staged updates preserving customized files, missing and
failing gates, and Python CI runner failure propagation. Exercise Bash init on
Linux. Add CI for Python tests on Linux and Windows. Do not claim Windows shell
execution unless observed. No SDK interface is needed for these CLI internals.

## Rollout

Review this change as one upstream PR. Do not initialize or update any consumer
harness or SDK. Automated dispatch, synchronization, provider approval storage and
native Linear template installation remain separate integration work.
