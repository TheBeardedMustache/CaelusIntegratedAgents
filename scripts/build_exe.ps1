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

pip install -q --upgrade -r requirements.txt


pip install -q --upgrade pyinstaller pyside6

pyinstaller --noconfirm desktop_app/resources/installer.spec
pip uninstall -y PyQt5 PyQt5-sip PyQt5-Qt5 2>$null
pip install -q --upgrade pyinstaller pyside6
pyinstaller `
  --onefile --windowed `
  --add-data "desktop_app/resources/icons;icons" `
  --add-data "desktop_app/resources/logging.yaml;." `
  --hidden-import PySide6.QtCore `
  --hidden-import PySide6.QtGui `
  --hidden-import PySide6.QtWidgets `
  desktop_app/main.py


$sha = (git rev-parse --short HEAD).Trim()
mkdir -Force releases | Out-Null
Move-Item dist\CaelusIntegratedAgents.exe "releases\CaelusIntegratedAgents-$sha.exe" -Force
Write-Host "`e[32mSUCCESS:`e[0m releases\CaelusIntegratedAgents-$sha.exe"

