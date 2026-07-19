# MagnetFlux Studio — Architecture

This document records the structural decisions that keep the application
maintainable, testable and scalable. It is the developer-facing companion to
`README.md`.

## Layering

Dependencies flow **downward only**. A layer may import from layers above it in
this list but never the reverse:

```
ui  ->  visualization / racetrack / optimization  ->  solver  ->  materials  ->  cad  ->  core
```

* **core** — pure NumPy/Python domain model. No Qt, no FEM, no CAD kernel.
  Contains geometry primitives, the model tree, unit policy, the versioned
  `.mfx` project container, and the background job runner.
* **cad** — CAD import (STEP/IGES/STL) via pythonOCC, producing `TriangleMesh`.
* **materials** — magnet grades, nonlinear soft-iron B-H curves, magnetization.
* **solver** — backend-agnostic interfaces plus concrete backends.
* **visualization / racetrack / optimization** — consume solver results.
* **ui** — PySide6 desktop shell; the only layer that talks to the user.

The rule from `CLAUDE.md` — *never mix GUI and solver logic* — is enforced by
this layering: the solver layer has no import of `magnetflux.ui`.

## Optional dependencies

Heavy or platform-specific libraries (PySide6, pythonOCC, Gmsh, scikit-fem,
PyVista, reportlab) are imported **lazily inside the functions that need them**.
This keeps `import magnetflux` cheap and lets the numerical core run and be
unit-tested in a headless CI environment with only NumPy and SciPy.

## Units

All internal data is **SI** (metres, tesla, amperes/metre). The two boundaries
that convert are:

1. **CAD import** — STEP/IGES/STL are typically in millimetres; the importer
   scales to metres immediately (`magnetflux.core.units`).
2. **UI / reports** — display in mm / mT.

## Solver strategy

`solver.base.SolverBackend` is the abstraction the rest of the app depends on.
Two backends implement it:

* **AnalyticBackend** — surface-charge / dipole superposition. No mesh, always
  available, closed-form. Used to validate the FEM backend and to unblock
  visualization/race-track development before FEM is complete.
* **ScikitFemBackend** — magnetic **vector potential A** formulation,
  `curl(nu curl A) = curl(nu mu0 M) + J`, discretised with lowest-order
  **Nedelec (edge) elements** on Gmsh tetrahedra. Outer boundary uses magnetic
  insulation (`n x A = 0`). Gauging via tree–cotree / small `div A` penalty.
  Nonlinear steel handled by Newton iteration on `nu(|B|)`.

Choosing the vector-potential formulation (over a scalar potential) is what
makes closed flux loops through saturating pole plates — the magnetron case —
physically correct.

### Validation

The analytic on-axis field of a uniformly magnetised cylinder is the primary
regression benchmark for the FEM backend (Milestone 3), with a numerical
tolerance enforced in the test suite.

## Concurrency

`core.jobs` provides a Qt-independent, cancellable job runner with progress
reporting. Meshing, solving and optimization run on worker threads so the GUI
stays responsive; the UI layer adapts `Job` callbacks to Qt signals.

## Project file (`.mfx`)

A ZIP archive with a versioned `manifest.json` and per-body mesh arrays. The
manifest carries a free-form `sections` map that later milestones extend
(materials, solver settings, cached results) without changing the container
code. Loading refuses schema versions newer than the running build.

## Packaging (Milestone 6)

Because every runtime dependency is pure-Python or ships Windows wheels
(scikit-fem, PySide6, PyVista, Gmsh), the app builds into a native Windows
executable with **PyInstaller**, wrapped by an **Inno Setup** installer.
