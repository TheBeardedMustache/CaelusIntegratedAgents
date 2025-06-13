# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['desktop_app/app.py'],
    pathex=[],
    binaries=[
        ('/lib/x86_64-linux-gnu/libEGL.so.1', 'lib'),
        ('/lib/x86_64-linux-gnu/libxkbcommon-x11.so.0', 'lib'),
    ],
    datas=[
        ('desktop_app/resources/icons', 'icons'),
        ('desktop_app/resources/logging.yaml', '.'),
        ('.env', '.'),
    ],
    hiddenimports=['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CaelusIntegratedAgents',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
