[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$AvevaDesignDirectory = $env:AVEVA_DESIGN_EXE,
    [string]$UserDataDirectory = 'D:\AVEVA\USERDATA',
    [switch]$Rebuild,
    [switch]$PrepareOnly
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($AvevaDesignDirectory)) {
    $AvevaDesignDirectory = 'D:\AVEVA\Everything3D3.1'
}

$designRoot = (Resolve-Path -LiteralPath $AvevaDesignDirectory).Path
$monitorExe = Join-Path $designRoot 'mon.exe'
$launchInit = Join-Path $designRoot 'launch.init'
if (-not (Test-Path -LiteralPath $monitorExe)) {
    throw "E3D monitor executable not found: $monitorExe"
}
if (-not (Test-Path -LiteralPath $launchInit)) {
    throw "E3D launch.init not found: $launchInit"
}
$workingDirectory = (Resolve-Path -LiteralPath $UserDataDirectory).Path

$moduleRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$repositoryRoot = (Resolve-Path -LiteralPath (Join-Path $moduleRoot '..\..')).Path
$runtimeRoot = Join-Path $PSScriptRoot 'runtime'
$sessionRoot = Join-Path $runtimeRoot 'sessions'
$buildScript = Join-Path $moduleRoot 'addin\build.ps1'
$prepareScript = Join-Path $PSScriptRoot 'prepare_deployment.ps1'

$builtAddin = Join-Path $moduleRoot 'addin\bin\E3DLiveBridge.Addin.dll'
if ($Rebuild -or -not (Test-Path -LiteralPath $builtAddin)) {
    & $buildScript -AvevaDesignExe $designRoot
}
& $prepareScript -AvevaDesignExe $designRoot -OutputDirectory $runtimeRoot
New-Item -ItemType Directory -Path $sessionRoot -Force | Out-Null

Write-Output "Experiment configuration is ready under $runtimeRoot"
if ($PrepareOnly) {
    exit 0
}

if ($PSCmdlet.ShouldProcess($monitorExe, 'Start isolated interactive E3D monitor')) {
    $previousAddinsPath = $env:CAF_ADDINS_PATH
    $previousSessionRoot = $env:E3D_LIVE_SESSION_ROOT
    try {
        $env:CAF_ADDINS_PATH = $runtimeRoot
        $env:E3D_LIVE_SESSION_ROOT = $sessionRoot

        # E3D is intentionally visible because the operator must interact with it.
        $monitorProcess = Start-Process `
            -FilePath $monitorExe `
            -ArgumentList @('PROD', 'E3D', 'init', "`"$launchInit`"") `
            -WorkingDirectory $workingDirectory `
            -PassThru `
            -WindowStyle Normal
    }
    finally {
        $env:CAF_ADDINS_PATH = $previousAddinsPath
        $env:E3D_LIVE_SESSION_ROOT = $previousSessionRoot
    }

    $receipt = [ordered]@{
        launcher_process_id = $monitorProcess.Id
        started_utc = [DateTime]::UtcNow.ToString('o')
        executable = $monitorExe
        arguments = "PROD E3D init `"$launchInit`""
        working_directory = $workingDirectory
        addins_path = $runtimeRoot
        session_root = $sessionRoot
        repository_root = $repositoryRoot
    }
    $receiptPath = Join-Path $runtimeRoot 'target-e3d-process.json'
    $receipt | ConvertTo-Json | Set-Content -LiteralPath $receiptPath -Encoding UTF8

    Write-Output "Started isolated E3D monitor PID $($monitorProcess.Id)."
    Write-Output "Launch receipt: $receiptPath"
    Write-Output 'Log in and open Design, then list des.exe processes to obtain the target PID.'
}
