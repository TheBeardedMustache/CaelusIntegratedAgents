param ()
$ErrorActionPreference = "Stop"

function Ensure-Venv {
    if (-not (Test-Path ".venv")) {
        python -m venv .venv
    }
    if ($env:OS -eq "Windows_NT") {
        . .venv\Scripts\Activate.ps1
    } else {
        . .venv/bin/activate
    }
}

Ensure-Venv
pip install -q --upgrade pyinstaller pyside6

pyinstaller --noconfirm desktop_app/resources/installer.spec

$sha = (git rev-parse --short HEAD).Trim()
mkdir -Force releases | Out-Null
Move-Item dist\CaelusIntegratedAgents.exe "releases\CaelusIntegratedAgents-$sha.exe" -Force
Write-Host "`e[32mSUCCESS:`e[0m releases\CaelusIntegratedAgents-$sha.exe"

