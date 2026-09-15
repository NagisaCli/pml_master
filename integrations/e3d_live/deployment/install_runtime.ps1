param(
    [string]$PythonCommand = 'python'
)

$ErrorActionPreference = 'Stop'

$moduleRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$runtimeRoot = Join-Path $PSScriptRoot 'runtime'
$venvRoot = Join-Path $runtimeRoot 'python'
$requirements = Join-Path $moduleRoot 'requirements.txt'

New-Item -ItemType Directory -Path $runtimeRoot -Force | Out-Null
if (-not (Test-Path -LiteralPath (Join-Path $venvRoot 'Scripts\python.exe'))) {
    & $PythonCommand -m venv $venvRoot
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to create the isolated Python runtime at $venvRoot."
    }
}

$runtimePython = Join-Path $venvRoot 'Scripts\python.exe'
& $runtimePython -m pip install --disable-pip-version-check --requirement $requirements
if ($LASTEXITCODE -ne 0) {
    throw 'Unable to install the pinned E3D live runtime dependencies.'
}

& $runtimePython -c "import openai; print('OpenAI SDK', openai.__version__)"
if ($LASTEXITCODE -ne 0) {
    throw 'The isolated OpenAI SDK import check failed.'
}

Write-Output "Isolated gateway runtime ready: $runtimePython"
