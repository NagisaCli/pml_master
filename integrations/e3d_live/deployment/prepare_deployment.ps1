param(
    [string]$AvevaDesignExe = $env:AVEVA_DESIGN_EXE,
    [string]$AddinDll = (Join-Path $PSScriptRoot '..\addin\bin\E3DLiveBridge.Addin.dll'),
    [string]$OutputDirectory = (Join-Path $PSScriptRoot 'runtime')
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($AvevaDesignExe)) {
    $AvevaDesignExe = 'D:\AVEVA\Everything3D3.1'
}

$avevaDir = (Resolve-Path -LiteralPath $AvevaDesignExe).Path
$addinPath = (Resolve-Path -LiteralPath $AddinDll).Path
$sourceConfig = Join-Path $avevaDir 'DesignAddins.xml'
if (-not (Test-Path -LiteralPath $sourceConfig)) {
    throw "Installed DesignAddins.xml not found: $sourceConfig"
}

$outputRoot = [IO.Path]::GetFullPath($OutputDirectory)
$moduleRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$modulePrefix = $moduleRoot.TrimEnd([IO.Path]::DirectorySeparatorChar) +
    [IO.Path]::DirectorySeparatorChar
if (-not $outputRoot.StartsWith($modulePrefix, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Deployment output must remain inside the isolated e3d_live module."
}

New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null
$targetConfig = Join-Path $outputRoot 'DesignAddins.xml'
$deployedDll = Join-Path $outputRoot ([IO.Path]::GetFileName($addinPath))
Copy-Item -LiteralPath $addinPath -Destination $deployedDll -Force
[xml]$document = Get-Content -Raw -LiteralPath $sourceConfig
$addinAssemblyName = [IO.Path]::GetFileNameWithoutExtension($addinPath)
$existing = @($document.ArrayOfString.string | ForEach-Object { [string]$_ })
if ($existing -notcontains $addinAssemblyName) {
    $node = $document.CreateElement('string')
    $node.InnerText = $addinAssemblyName
    [void]$document.ArrayOfString.AppendChild($node)
}

$settings = [Xml.XmlWriterSettings]::new()
$settings.Indent = $true
$settings.Encoding = [Text.UTF8Encoding]::new($false)
$writer = [Xml.XmlWriter]::Create($targetConfig, $settings)
try {
    $document.Save($writer)
}
finally {
    $writer.Dispose()
}

Write-Output "Prepared isolated add-in configuration: $targetConfig"
Write-Output "Deployed isolated add-in assembly: $deployedDll"
Write-Output "Set CAF_ADDINS_PATH=$outputRoot before starting E3D Design."
