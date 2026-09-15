$ErrorActionPreference = 'Stop'

$processes = @(Get-Process -Name 'des' -ErrorAction SilentlyContinue |
    Sort-Object StartTime)

if ($processes.Count -eq 0) {
    Write-Output 'No running AVEVA E3D Design (des.exe) process was found.'
    exit 0
}

$processes |
    Select-Object Id, StartTime, MainWindowTitle, Path |
    Format-Table -AutoSize
