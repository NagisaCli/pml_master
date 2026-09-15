<#
.SYNOPSIS
    Syncs the local AVEVA E3D PML modeling skill to Antigravity's global skill library (~/.gemini/config/skills/e3d-pml).
.DESCRIPTION
    Updates SKILL.md, knowledge/, workflows/, equipment/, projects/, and helper scripts.
#>

$ErrorActionPreference = 'Stop'

$SourceRepo = $PSScriptRoot
$TargetDir = Join-Path $env:USERPROFILE ".gemini\config\skills\e3d-pml"

Write-Host "Syncing skill from: $SourceRepo" -ForegroundColor Cyan
Write-Host "Syncing skill to  : $TargetDir" -ForegroundColor Cyan

# 1. Ensure target directories
$subdirs = @("skill\knowledge", "skill\workflows", "skill\equipment", "skill\projects", "references", "scripts")
foreach ($d in $subdirs) {
    $p = Join-Path $TargetDir $d
    if (-not (Test-Path $p)) {
        New-Item -ItemType Directory -Path $p -Force | Out-Null
    }
}

# 2. Copy skill subfolders
$sections = @("knowledge", "workflows", "equipment", "projects")
foreach ($sec in $sections) {
    $src = Join-Path $SourceRepo "skill\$sec"
    $dst = Join-Path $TargetDir "skill\$sec"
    if (Test-Path $src) {
        Copy-Item -Path "$src\*" -Destination $dst -Recurse -Force
        Write-Host "  -> Synced skill\$sec" -ForegroundColor Green
    }
}

# 3. Copy knowledge to references/
$srcK = Join-Path $SourceRepo "skill\knowledge"
$dstR = Join-Path $TargetDir "references"
if (Test-Path $srcK) {
    Copy-Item -Path "$srcK\*" -Destination $dstR -Recurse -Force
    Write-Host "  -> Synced references\" -ForegroundColor Green
}

# 4. Generate SKILL.md with frontmatter
$frontmatter = @"
---
name: e3d-pml
description: >-
  AVEVA E3D PML1 macro generation and industrial equipment/piping modeling skill for pulp & paper plants.
  Use this skill whenever generating, reviewing, debugging, or validating AVEVA E3D PML macros,
  modeling equipment (pumps, tanks, vessels, chests, heat exchangers, nozzles), routing piping,
  positioning 3D primitives (CYLI, DISH, BOX, CONE, PYRAMID), or translating CAD/vendor drawings into E3D macros.
---

"@

$sourceSkillMd = Join-Path $SourceRepo "SKILL.md"
$content = Get-Content -LiteralPath $sourceSkillMd -Raw -Encoding UTF8
$targetSkillMd = Join-Path $TargetDir "SKILL.md"
Set-Content -LiteralPath $targetSkillMd -Value ($frontmatter + "`n" + $content) -Encoding UTF8
Write-Host "  -> Updated SKILL.md with frontmatter" -ForegroundColor Green

Write-Host "`nSkill e3d-pml successfully updated in global config!" -ForegroundColor Green
