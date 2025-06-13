# Build the Caelus Integrated Agents executable

$venvPath = '.venv'
if (!(Test-Path $venvPath)) {
    python -m venv $venvPath
}

& (Join-Path $venvPath 'Scripts/Activate.ps1')

function Ensure-Package($Name) {
    if (-not (pip show $Name > $null 2>&1)) {
        pip install $Name
    }
}

Ensure-Package 'pyinstaller'
Ensure-Package 'PySide6'

pyinstaller 'desktop_app/resources/installer.spec'

$sha = (git rev-parse --short HEAD).Trim()
$releaseDir = 'releases'
if (!(Test-Path $releaseDir)) { New-Item -ItemType Directory -Path $releaseDir | Out-Null }

$builtExe = 'dist/CaelusIntegratedAgents.exe'
$destExe = Join-Path $releaseDir "CaelusIntegratedAgents-$sha.exe"
Move-Item $builtExe $destExe -Force

Write-Host "SUCCESS: built $destExe" -ForegroundColor Green
