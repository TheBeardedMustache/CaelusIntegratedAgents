# Build the Caelus Integrated Agents executable

# Ensure virtual environment exists
$venvPath = ".venv"
if (!(Test-Path $venvPath)) {
    python -m venv $venvPath
}

# Activate the virtual environment
$activateScript = Join-Path $venvPath "Scripts/Activate.ps1"
& $activateScript

# Install dependencies if missing
function Ensure-Package {
    param([string]$Name)
    if (-not (pip show $Name > $null 2>&1)) {
        pip install $Name
    }
}

Ensure-Package "pyinstaller"
Ensure-Package "PySide6"

# Run PyInstaller with the provided spec file
pyinstaller "desktop_app/resources/installer.spec"

# Move the executable to the releases directory with git short SHA
$shortSha = (git rev-parse --short HEAD).Trim()
$releaseDir = "releases"
if (!(Test-Path $releaseDir)) { New-Item -ItemType Directory -Path $releaseDir | Out-Null }
$builtExe = Join-Path "dist/CaelusIntegratedAgents" "CaelusIntegratedAgents.exe"
$destExe = Join-Path $releaseDir "CaelusIntegratedAgents-$shortSha.exe"
Move-Item $builtExe $destExe -Force

# Print success message
Write-Host "Executable built at $destExe" -ForegroundColor Green

