param(
    [Parameter(Mandatory = $true)]
    [int]$TargetE3dPid,

    [Parameter(Mandatory = $true)]
    [string]$ProjectCode,

    [Parameter(Mandatory = $true)]
    [string]$Mdb,

    [string]$Module = 'DESIGN',
    [int]$Port = 48731,

    [ValidateSet('controlled_write', 'read_only')]
    [string]$AccessMode = 'controlled_write',

    [ValidateSet('local', 'openai')]
    [string]$AssistantBackend = 'local',

    [string]$OpenAIModel = 'gpt-5.4-2026-03-05',
    [switch]$AllowExternalAI
)

$ErrorActionPreference = 'Stop'

if ($TargetE3dPid -le 0) {
    throw 'TargetE3dPid must be a positive process ID.'
}

$target = Get-Process -Id $TargetE3dPid -ErrorAction Stop
if (-not [string]::Equals($target.ProcessName, 'des', [StringComparison]::OrdinalIgnoreCase)) {
    throw "PID $TargetE3dPid is $($target.ProcessName), not AVEVA E3D Design (des.exe)."
}

$moduleRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$repositoryRoot = (Resolve-Path -LiteralPath (Join-Path $moduleRoot '..\..')).Path
$sessionRoot = Join-Path $PSScriptRoot 'runtime\sessions'
New-Item -ItemType Directory -Path $sessionRoot -Force | Out-Null
$runtimePython = Join-Path $PSScriptRoot 'runtime\python\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $runtimePython)) {
    $runtimePython = 'python'
}

if ($AssistantBackend -eq 'openai') {
    if (-not $AllowExternalAI) {
        throw 'The OpenAI backend requires -AllowExternalAI.'
    }
}

$gatewayArguments = @(
    '-m', 'integrations.e3d_live.gateway',
    '--target-e3d-pid', $TargetE3dPid,
    '--project-code', $ProjectCode,
    '--mdb', $Mdb,
    '--module', $Module,
    '--port', $Port,
    '--session-root', $sessionRoot,
    '--assistant-backend', $AssistantBackend,
    '--access-mode', $AccessMode,
    '--openai-model', $OpenAIModel
)
if ($AssistantBackend -eq 'openai') {
    $gatewayArguments += @(
        '--allow-external-ai'
    )
}

Push-Location $repositoryRoot
try {
    & $runtimePython $gatewayArguments
    if ($LASTEXITCODE -ne 0) {
        throw "E3D live gateway exited with code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}
