# MagnetFlux Studio

A professional desktop CAE application for **magnetostatic analysis of magnetron
cathodes**, with a feature set comparable to the magnetostatics portion of
COMSOL: CAD import, material assignment, permanent-magnet definition, automatic
air-domain generation, meshing, an FEM magnetostatic solver, magnetic-flux
visualization, race-track (erosion) prediction, and optimization.

> Status: under active milestone-driven development. See
> [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and the milestone tracker below.

## Key design decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| FEM backend | **scikit-fem** (pure Python) | Packages cleanly into a native Windows `.exe`; no compiled-lib blocker |
| Solver formulation | **Magnetic vector potential A** (Nedelec edge elements) | Correct for closed flux loops through nonlinear steel pole plates |
| Units | **SI internally** (m, T, A/m) | Conversions confined to CAD import & UI; avoids the mm/m error class |
| Dependencies | Heavy libs (Qt, pythonOCC, Gmsh, PyVista) are **optional imports** | Numerical core stays importable & unit-testable headless |

## Architecture

```
magnetflux/
  core/           domain model: geometry, model tree, units, project (.mfx), jobs
  cad/            STEP / IGES / STL import (pythonOCC)
  materials/      magnet grades, nonlinear soft-iron B-H, magnetization
  solver/         analytic + scikit-fem A-formulation backends, air domain, mesh
  visualization/  contours, streamlines, glyphs, slices, probes, export
  racetrack/      tangential-field erosion model, heatmap, PDF report
  optimization/   spacing / pole-arrangement optimizers, utilization estimator
  ui/             PySide6 desktop GUI (optional)
```

GUI, solver, CAD, visualization and export are strictly separated — GUI and
solver logic never mix (see `CLAUDE.md`).

## Installation

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .            # numerical core (numpy, scipy)
pip install -e .[all]       # full app: GUI, CAD, FEM, reporting, dev tools
```

pythonOCC (`pythonocc-core`) is installed via conda-forge; see
`docs/ARCHITECTURE.md` for platform notes.

## Running

```bash
magnetflux            # launches the desktop GUI (requires the 'gui' extras)
```

## Development

```bash
pip install -e .[dev]
pytest                # numerical core is fully testable without GUI/FEM libs
```

## Milestones

- [x] **M0** Architecture foundations — units, project schema, logging, jobs, solver interfaces, CI
- [x] **M1** Foundation & 3D viewer — STEP/IGES/STL import, model tree, camera
- [x] **M2** Materials & magnetization — grades, nonlinear iron, direction editor
- [ ] **M3** Magnetostatic solver — air domain, mesh, analytic + scikit-fem A-formulation
- [ ] **M4** Visualization — contours, streamlines, glyphs, slices, probes; PNG/CSV/VTK export
- [ ] **M5** Race-track prediction — erosion model, heatmap, PDF report
- [ ] **M6** Optimization & release — spacing/pole optimizers, Windows installer
