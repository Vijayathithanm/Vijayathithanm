"""Field probe tool (Milestone 4).

Two probing modes:

* :class:`SolverProbe` -- evaluate the field at arbitrary points by running the
  solver backend there (exact for the analytic backend; used for interactive
  point picks).
* :class:`GridProbe` -- interpolate a previously sampled structured field, for
  fast repeated queries without re-solving.
"""

from __future__ import annotations

import numpy as np

from magnetflux.solver.base import FieldResult, SolverBackend, SolverProblem
from magnetflux.visualization.sampling import StructuredField


class SolverProbe:
    """Probe that evaluates the field at query points via a solver backend."""

    def __init__(self, backend: SolverBackend, magnet_sources: list[dict]) -> None:
        self._backend = backend
        self._sources = magnet_sources

    def at(self, point: np.ndarray) -> np.ndarray:
        """Return the ``(3,)`` B vector [T] at a single ``point``."""
        pts = np.asarray(point, dtype=float).reshape(1, 3)
        res = self._backend.solve(SolverProblem(points=pts, magnet_sources=self._sources))
        return res.b[0]


class GridProbe:
    """Trilinear interpolation of a sampled structured field."""

    def __init__(self, field: StructuredField, bounds_min, bounds_max) -> None:
        from scipy.interpolate import RegularGridInterpolator

        nx, ny, nz = field.dims
        axes = [
            np.linspace(bounds_min[i], bounds_max[i], (nx, ny, nz)[i])
            for i in range(3)
        ]
        b = field.result.b.reshape(nx, ny, nz, 3)
        self._interp = RegularGridInterpolator(
            axes, b, bounds_error=False, fill_value=None
        )

    def at(self, points: np.ndarray) -> np.ndarray:
        """Interpolated ``(N, 3)`` B vectors at ``points``."""
        pts = np.asarray(points, dtype=float).reshape(-1, 3)
        return self._interp(pts)
