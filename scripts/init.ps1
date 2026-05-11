<#
.SYNOPSIS
    Initialize a new project with the Codex Automata harness.

.DESCRIPTION
    Copies the contents of the harness/ directory into the target project path.
    The target directory is created if it does not exist.

.PARAMETER TargetPath
    The path to the project directory where the harness will be installed.

.EXAMPLE
    .\init.ps1 -TargetPath D:\projects\my-new-app
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$TargetPath
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$HarnessDir = Join-Path (Split-Path -Parent $ScriptDir) "harness"

if (-not (Test-Path $HarnessDir)) {
    Write-Error "Harness directory not found at $HarnessDir"
    exit 1
}

if (-not (Test-Path $TargetPath)) {
    New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
}

Get-ChildItem -Path $HarnessDir -Force | Copy-Item -Destination $TargetPath -Recurse -Force

Write-Host ""
Write-Host "Codex Automata harness initialized at: $TargetPath"
Write-Host ""
Write-Host "Your project now contains:"
Write-Host "  AGENTS.md        Root agent instructions"
Write-Host "  PLAYBOOK.md      Phase-by-phase methodology guide"
Write-Host "  .cursor/         Cursor IDE rules, skills, subagents, hooks"
Write-Host "  .github/         PR template, issue templates, CI workflow"
Write-Host "  agent/           Detailed agent operating rules"
Write-Host "  templates/       Specification, test, task, and review templates"
Write-Host "  docs/            Project documentation (empty, ready for specs)"
Write-Host "  tests/           Test plans and test code (empty)"
Write-Host "  tasks/           Agent task definitions (empty)"
Write-Host "  review/          Human review records (empty)"
Write-Host "  src/             Source code (empty)"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Open the project in Cursor IDE"
Write-Host "  2. Read PLAYBOOK.md for the phase-by-phase guide"
Write-Host "  3. Copy templates/project-intake-template.md to docs/intake.md"
Write-Host "  4. Or use /project-intake in Cursor chat to get started"
Write-Host ""
