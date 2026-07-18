"""MagnetFlux Studio.

A professional desktop magnetostatic simulation tool for magnetron cathodes.

Layered architecture (see ``CLAUDE.md`` -- GUI, solver, CAD, visualization and
export must never mix):

* :mod:`magnetflux.core`          -- domain data model, units, project, jobs
* :mod:`magnetflux.cad`           -- CAD import (STEP / IGES / STL)
* :mod:`magnetflux.materials`     -- material & magnetization definitions
* :mod:`magnetflux.solver`        -- magnetostatic field computation
* :mod:`magnetflux.visualization` -- field visualization & export
* :mod:`magnetflux.racetrack`     -- erosion / race-track prediction
* :mod:`magnetflux.optimization`  -- magnet layout optimization
* :mod:`magnetflux.ui`            -- PySide6 desktop GUI (optional import)

Heavy, platform-specific dependencies (PySide6, pythonOCC, Gmsh, scikit-fem,
PyVista) are imported lazily so the numerical core remains importable and
unit-testable with only NumPy and SciPy installed.
"""

__version__ = "0.1.0"
__all__ = ["__version__"]
