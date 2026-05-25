<#
.SYNOPSIS
    Initialize a new project with the Codex Automata harness.

.DESCRIPTION
    Copies harness contents into the target project path. Use -Profile to control
    which templates and directories are installed (Essential, Standard, or Complete).
    Defaults to Standard when -Profile is omitted.

.PARAMETER TargetPath
    The path to the project directory where the harness will be installed.

.PARAMETER Profile
    Adoption profile: Essential, Standard, or Complete.

.EXAMPLE
    .\init.ps1 -TargetPath D:\projects\my-new-app

.EXAMPLE
    .\init.ps1 -TargetPath D:\projects\my-side-project -Profile Essential
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$TargetPath,
    [ValidateSet('Essential', 'Standard', 'Complete')]
    [string]$Profile = 'Standard'
)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$HarnessDir = Join-Path (Split-Path -Parent $ScriptDir) 'harness'
$TemplatesDir = Join-Path $HarnessDir 'templates'

if (-not (Test-Path $HarnessDir)) {
    Write-Error "Harness directory not found at $HarnessDir"
    exit 1
}

$EssentialTemplates = @(
    'spec-template.md',
    'test-plan-template.md',
    'agent-task-template.md'
)

$StandardTemplates = $EssentialTemplates + @(
    'interface-contract-template.md',
    'module-boundary-template.md',
    'architecture-decision-record.md',
    'context-state-template.md',
    'block-registry-template.md',
    'brownfield-audit-template.md',
    'human-review-template.md',
    'project-intake-template.md',
    'sdk-design-template.md',
    'deployment-checklist-template.md',
    'guardrail-config-template.md',
    'retrospective-template.md'
)

$CompleteExtraTemplates = @(
    'product-test-template.md',
    'user-profile-template.md',
    'design-identity-template.md',
    'gap-assessment-template.md',
    'security-audit-template.md',
    'incident-postmortem-template.md'
)

$ProfileTemplates = switch ($Profile) {
    'Essential' { $EssentialTemplates }
    'Standard'  { $StandardTemplates }
    'Complete'  { $StandardTemplates + $CompleteExtraTemplates }
}

$SkipDirs = if ($Profile -eq 'Essential') { @('sdk', 'review') } else { @() }

if (-not (Test-Path $TargetPath)) {
    New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
}

foreach ($item in Get-ChildItem -Path $HarnessDir -Force) {
    if ($item.Name -eq 'templates') { continue }
    if ($SkipDirs -contains $item.Name) { continue }
    Copy-Item -Path $item.FullName -Destination $TargetPath -Recurse -Force
}

$TargetTemplates = Join-Path $TargetPath 'templates'
New-Item -ItemType Directory -Path $TargetTemplates -Force | Out-Null

$AgentsTemplate = Join-Path $TemplatesDir 'AGENTS.md'
if (Test-Path $AgentsTemplate) {
    Copy-Item -Path $AgentsTemplate -Destination $TargetTemplates -Force
}

foreach ($name in $ProfileTemplates) {
    $src = Join-Path $TemplatesDir $name
    if (-not (Test-Path $src)) {
        Write-Error "Template not found: $src"
        exit 1
    }
    Copy-Item -Path $src -Destination $TargetTemplates -Force
}

if ($Profile -ne 'Essential') {
    foreach ($dir in @('sdk', 'review')) {
        $dest = Join-Path $TargetPath $dir
        if (-not (Test-Path $dest)) {
            New-Item -ItemType Directory -Path $dest -Force | Out-Null
        }
        $gitkeep = Join-Path $HarnessDir "$dir\.gitkeep"
        if (Test-Path $gitkeep) {
            Copy-Item -Path $gitkeep -Destination $dest -Force
        }
    }
}

# Copy enforcement scripts
$ScriptsSrc = Join-Path $HarnessDir 'scripts'
if (Test-Path $ScriptsSrc) {
    $ScriptsDest = Join-Path $TargetPath 'scripts'
    New-Item -ItemType Directory -Path $ScriptsDest -Force | Out-Null
    Copy-Item -Path (Join-Path $ScriptsSrc '*') -Destination $ScriptsDest -Force
}

# Patch hooks.json for Windows: replace .sh hook commands with .ps1 equivalents
$HooksJson = Join-Path $TargetPath '.cursor' 'hooks.json'
if (Test-Path $HooksJson) {
    $hooksContent = Get-Content $HooksJson -Raw
    $hooksContent = $hooksContent -replace '\.cursor/hooks/([^"]+)\.sh', '.cursor/hooks/$1.ps1'
    Set-Content -Path $HooksJson -Value $hooksContent -NoNewline
}

Write-Host ''
Write-Host "Codex Automata harness initialized at: $TargetPath"
Write-Host "Adoption profile: $Profile"
Write-Host ''
Write-Host 'Your project now contains:'
Write-Host '  AGENTS.md        Root agent instructions'
Write-Host '  PLAYBOOK.md      Phase-by-phase methodology guide'
Write-Host '  .cursor/         Cursor IDE rules, skills, subagents, hooks'
Write-Host '  .github/         PR template, issue templates, CI workflow'
Write-Host '  agent/           Detailed agent operating rules'
Write-Host "  templates/       $($ProfileTemplates.Count) profile template(s)"
Write-Host '  docs/            Project documentation (empty, ready for specs)'
Write-Host '  tests/           Test plans and test code (empty)'
Write-Host '  tasks/           Agent task definitions (empty)'
if ($Profile -ne 'Essential') {
    Write-Host '  review/          Human review records (empty)'
    Write-Host '  sdk/             SDK constraint surface (empty)'
}
Write-Host '  src/             Source code (empty)'
Write-Host '  scripts/         Enforcement scripts (divergence gate, spec check, commit lint)'
Write-Host ''
Write-Host 'Next steps:'
Write-Host '  1. Open the project in Cursor IDE'
Write-Host '  2. Read PLAYBOOK.md for the phase-by-phase guide'
Write-Host '  3. See reference/adoption-profiles.md for profile details'
if ($Profile -ne 'Essential') {
    Write-Host '  4. Copy templates/project-intake-template.md to docs/intake.md'
    Write-Host '  5. Or use /project-intake in Cursor chat to get started'
} else {
    Write-Host '  4. Create docs/intake.md with project name, goal, constraints, and Profile: Essential'
    Write-Host '  5. Or use /project-intake in Cursor chat to get started'
}
Write-Host ''
