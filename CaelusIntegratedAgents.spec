# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for the Caelus desktop app.
This version collects binaries only if they exist on the build host so the
build works on Windows, macOS and Linux.
"""
from pathlib import Path
from PyInstaller.utils.hooks import collect_dynamic_libs

block_cipher = None


def _safe_collect(package, dest):
    """Collect binaries from *package* but only keep those that exist."""
    out = []
    for src, _ in collect_dynamic_libs(package, dest):
        if Path(src).is_file():
            out.append((src, dest))
    return out


binaries = _safe_collect("PySide6", "PySide6")

a = Analysis(
    ["desktop_app/main.py"],
    pathex=[],
    binaries=binaries,
    datas=[
        ("desktop_app/resources/icons", "icons"),
        ("desktop_app/resources/logging.yaml", "."),
    ],
    hiddenimports=["PySide6.QtCore", "PySide6.QtGui", "PySide6.QtWidgets"],
    hookspath=[],
    runtime_hooks=[],
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name="CaelusIntegratedAgents",
    console=False,
    icon=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="CaelusIntegratedAgents",
)
