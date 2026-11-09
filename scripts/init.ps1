<#
.SYNOPSIS
Initialize a fresh project using the canonical Python CLI. Requires Python 3.10+.
#>
param(
    [Parameter(Mandatory = $true)][string]$TargetPath,
    [ValidateSet('Essential', 'Standard', 'Complete')][string]$Profile = 'Standard'
)
$ErrorActionPreference = 'Stop'
$CliDir = Join-Path (Split-Path -Parent $PSScriptRoot) 'cli'
$PreviousPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $CliDir + [IO.Path]::PathSeparator + $PreviousPythonPath
    python -m codex_automata.cli init $TargetPath --profile $Profile.ToLowerInvariant()
    exit $LASTEXITCODE
} finally {
    $env:PYTHONPATH = $PreviousPythonPath
}
