# Session start and recovery

1. Obtain effective DEVELOP, OPERATE or MAINTAIN_METHODOLOGY context from the
   trusted controller. Missing context denies tool changes. OPERATE loads only
   application policy/tools, never development phases by installation alone.
2. Read dated authorization grants and explicit supersession; identify task,
   actor, policy version, allowed capabilities and write scope. Agents request
   transitions; only operator/controller authority issues grants.
3. In fresh checkouts, operator bootstrap occurs outside blocked agent tools:
   `context bootstrap`, `context authorize`, then `context select`. Never weaken
   an operational hook to let an agent grant itself development privileges.
4. Check the evidence surface when remote publication is required: configured
   remote, remote refs, local head and observed remote head. An unpushed head is
   pending publication, not delivered. Offline tasks explicitly record N/A.
5. Read current dynamic tool schemas before first use. For each server, record
   observed payload/parameter quirks in the project runbook. Do not generalize
   one connector's names across all integrations.
6. Restore per-agent/task checkpoint and authoritative attempts. After interrupted
   writes, re-read target files and inspect Git before any replay. Unknown remote
   effects require journal reconciliation. Never reset attempts by model change.
7. Confirm adoption review policy, task profile, acceptance-to-check mapping and
   required T0/T1/T2 host evidence before starting. Static/fixture checks must
   pass independently of behavioral red molds.

Hook selftest uses synthetic events and returns allow/deny without performing
operations. MCP payload: `tool_name: MCP:<exact-tool>`, separate
`mcp_server_name`; file tools use `input.path` or `input.filePath`. Verify the
actual host schema before adoption. Unknown tools deny with an actionable operator
bootstrap remedy. Re-read effective context per tool call. Tool adapters, not
prompts, enforce privileges; unrestricted shells bypass a prompt-only policy.

Executable evidence checks: `session inspect --project .` records local-only N/A;
add `--publication-required --branch BRANCH` to require a fresh remote ref matching
local HEAD. Failure blocks publication claims, not already authorized offline work.
`session readiness --packet child.json --state /secure/control.sqlite` derives a
local Ready proposal from actual upstream integration receipts and artifact pins;
it performs no Linear transition.
