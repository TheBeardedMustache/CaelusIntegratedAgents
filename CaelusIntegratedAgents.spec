# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for the Caelus desktop app.
This version collects binaries only if they exist on the build host so the
build works on Windows, macOS and Linux.
"""
from pathlib import Path
from PyInstaller.utils.hooks import collect_dynamic_libs
import sys

block_cipher = None


def _safe_collect(package, dest):
    """Collect binaries from *package* but only keep those that exist."""
    out = []
    for src, _ in collect_dynamic_libs(package, dest):
        if Path(src).is_file():
            out.append((src, dest))
    return out


binaries = _safe_collect("PySide6", "PySide6")

if sys.platform.startswith("win"):
    dll_name = f"python{sys.version_info.major}{sys.version_info.minor}.dll"
    candidates = [
        Path(sys.executable).with_name(dll_name),
        Path(sys.base_prefix) / dll_name,
        Path(sys.executable).parent.parent / dll_name,
    ]
    for dll_path in candidates:
        if dll_path.is_file():
            binaries.insert(0, (str(dll_path), "."))
            break

project_root = Path(__file__).resolve().parent if "__file__" in globals() else Path(sys.argv[0]).resolve().parent

a = Analysis(
    ["desktop_app/main.py"],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=[
        ("desktop_app/resources/icons", "icons"),
        ("desktop_app/resources/logging.yaml", "."),
        # Include UI definition for QUiLoader in frozen builds
        ("desktop_app/ui/main_window.ui", "desktop_app/ui"),
    ],
    hiddenimports=[],
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
