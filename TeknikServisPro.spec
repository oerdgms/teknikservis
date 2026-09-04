# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

project_root = Path(SPECPATH)
app_root = project_root / "app"

a = Analysis(
    [str(app_root / "desktop_launcher.py")],
    pathex=[str(app_root)],
    binaries=[],
    datas=[
        (str(app_root / "index.html"), "."),
        (str(app_root / "portal.html"), "."),
        (str(app_root / "db.json"), "."),
        (str(app_root / "assets" / "TeknikServisPro.ico"), "assets"),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="TeknikServisPro",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=str(app_root / "assets" / "TeknikServisPro.ico"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="TeknikServisPro",
)
