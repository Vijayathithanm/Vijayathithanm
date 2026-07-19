# Building & Packaging MagnetFlux Studio

## Prerequisites

- Python 3.11 or 3.12 (64-bit)
- Windows 10/11 for the packaged desktop build

## Development install

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -e .[all]
```

`.[all]` pulls in the GUI (PySide6, PyVista, VTK), the FEM backend
(scikit-fem), reporting (reportlab, matplotlib) and dev tools (pytest).
pythonOCC (`pythonocc-core`) is installed separately via conda-forge if you
need STEP/IGES import:

```bash
conda install -c conda-forge pythonocc-core
```

## Running the tests

```bash
pytest
```

The numerical core (units, geometry, materials, solver, race-track,
optimization) is fully testable without the GUI. FEM and rendering tests run
when scikit-fem / matplotlib / reportlab are installed and skip otherwise.

## Building the Windows executable

The choice of a pure-Python FEM backend (scikit-fem) means the whole app
packages with **PyInstaller** — no native FEM toolchain, no WSL/Docker.

```bash
pip install pyinstaller
pyinstaller packaging/magnetflux.spec
```

This produces a one-folder application in `dist/MagnetFluxStudio/` with
`MagnetFluxStudio.exe`.

## Building the installer

With [Inno Setup](https://jrsoftware.org/isinfo.php) installed:

```bash
iscc packaging/installer.iss
```

The signed-ready installer `MagnetFluxStudio-<version>-setup.exe` is written to
the `Output` folder.

## Continuous integration

`.github/workflows/magnetflux-ci.yml` runs the test suite (core + FEM +
rendering) on Python 3.11 and 3.12 for every change under `MagnetFluxStudio/`.
