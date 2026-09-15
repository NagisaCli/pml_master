param(
    [string]$AvevaDesignExe = $env:AVEVA_DESIGN_EXE
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($AvevaDesignExe)) {
    $AvevaDesignExe = 'D:\AVEVA\Everything3D3.1'
}

$addinDir = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$avevaDir = (Resolve-Path -LiteralPath $AvevaDesignExe).Path
$compiler = 'C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe'
$framework = 'C:\Windows\Microsoft.NET\Framework\v4.0.30319'
$outputDir = Join-Path $addinDir 'bin'
$outputDll = Join-Path $outputDir 'E3DLiveBridge.Addin.dll'

if (-not (Test-Path -LiteralPath $compiler)) {
    throw "C# compiler not found: $compiler"
}

$requiredAveva = @(
    'Aveva.ApplicationFramework.dll',
    'Aveva.ApplicationFramework.Presentation.dll',
    'Aveva.Core.Database.dll',
    'Aveva.Core.Geometry.dll',
    'Aveva.Core.Presentation.dll',
    'Aveva.Core.Utilities.dll'
)

foreach ($assembly in $requiredAveva) {
    $assemblyPath = Join-Path $avevaDir $assembly
    if (-not (Test-Path -LiteralPath $assemblyPath)) {
        throw "Required AVEVA assembly not found: $assemblyPath"
    }
}

New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

$references = @(
    (Join-Path $framework 'System.dll'),
    (Join-Path $framework 'System.Core.dll'),
    (Join-Path $framework 'System.Drawing.dll'),
    (Join-Path $framework 'System.Runtime.Serialization.dll'),
    (Join-Path $framework 'System.Windows.Forms.dll')
) + ($requiredAveva | ForEach-Object { Join-Path $avevaDir $_ })

$arguments = @(
    '/nologo',
    '/target:library',
    '/platform:x86',
    '/optimize+',
    '/warn:4',
    "/out:$outputDll"
)
$arguments += $references | ForEach-Object { "/reference:$_" }
$arguments += Get-ChildItem -LiteralPath $addinDir -File -Filter '*.cs' |
    Sort-Object Name |
    ForEach-Object { $_.FullName }

& $compiler $arguments
if ($LASTEXITCODE -ne 0) {
    throw "C# build failed with exit code $LASTEXITCODE"
}

$hash = Get-FileHash -LiteralPath $outputDll -Algorithm SHA256
Write-Output "Built $outputDll"
Write-Output "SHA256 $($hash.Hash)"
