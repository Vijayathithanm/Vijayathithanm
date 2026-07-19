# PyInstaller spec for MagnetFlux Studio (Milestone 6).
#
# Build a one-folder Windows application:
#     pyinstaller packaging/magnetflux.spec
#
# Because every runtime dependency is pure-Python or ships Windows wheels
# (scikit-fem, PySide6, PyVista, VTK, matplotlib, reportlab), no native
# toolchain is required -- this is why scikit-fem was chosen over FEniCSx.

# -*- mode: python ; coding: utf-8 -*-
import os

from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_dynamic_libs,
    collect_submodules,
)

# Resolve paths relative to this spec file so the build works from any CWD.
project_root = os.path.dirname(SPECPATH)
entry_script = os.path.join(project_root, "magnetflux", "__main__.py")
icon_path = os.path.join(project_root, "resources", "magnetflux.ico")
icon = icon_path if os.path.exists(icon_path) else None  # optional icon

block_cipher = None

hiddenimports = (
    collect_submodules("skfem")
    + collect_submodules("pyvista")
    + collect_submodules("pyvistaqt")
    + collect_submodules("vtkmodules")
    + collect_submodules("scipy")
)

datas = collect_data_files("pyvista") + collect_data_files("vtkmodules")

# Gmsh is a single module that loads a bundled shared library via ctypes; its
# binary must be collected explicitly so STEP/IGES import works in the freeze.
hiddenimports += ["gmsh"]
binaries = collect_dynamic_libs("gmsh")

a = Analysis(
    [entry_script],
    pathex=[project_root],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MagnetFluxStudio",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=icon,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="MagnetFluxStudio",
)
