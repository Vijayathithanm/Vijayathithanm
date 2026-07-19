"""Sampling helpers: structured grids, slice planes and probe lines (Milestone 4).

Streamlines, slice plots and surface contours all need the field sampled on a
structured layout rather than at scattered points. These helpers generate the
evaluation points (fed to a solver backend) and record the grid dimensions so
the result can be reshaped for visualization and structured VTK export.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from magnetflux.core.geometry import BoundingBox
from magnetflux.solver.base import FieldResult


@dataclass(slots=True)
class StructuredField:
    """A field sampled on a structured grid.

    Attributes:
        points: ``(N, 3)`` sample coordinates [m], C-ordered over ``dims``.
        result: The solved :class:`FieldResult` at ``points``.
        dims: ``(nx, ny, nz)`` grid dimensions (a slice has one dim == 1).
    """

    points: np.ndarray
    result: FieldResult
    dims: tuple[int, int, int]

    def reshape_scalar(self, values: np.ndarray) -> np.ndarray:
        """Reshape an ``(N,)`` scalar array to the grid ``dims``."""
        return np.asarray(values).reshape(self.dims)


def grid_points(bbox: BoundingBox, nx: int, ny: int, nz: int) -> tuple[np.ndarray, tuple[int, int, int]]:
    """Structured grid of points filling ``bbox``; returns (points, dims)."""
    xs = np.linspace(bbox.min_corner[0], bbox.max_corner[0], nx)
    ys = np.linspace(bbox.min_corner[1], bbox.max_corner[1], ny)
    zs = np.linspace(bbox.min_corner[2], bbox.max_corner[2], nz)
    xx, yy, zz = np.meshgrid(xs, ys, zs, indexing="ij")
    pts = np.column_stack([xx.ravel(), yy.ravel(), zz.ravel()])
    return pts, (nx, ny, nz)


def plane_points(
    origin: np.ndarray,
    u_dir: np.ndarray,
    v_dir: np.ndarray,
    u_len: float,
    v_len: float,
    nu: int,
    nv: int,
) -> tuple[np.ndarray, tuple[int, int, int]]:
    """Grid of points on a rectangular slice plane; returns (points, dims).

    The plane is centred on ``origin`` and spans ``+/- u_len/2`` along ``u_dir``
    and ``+/- v_len/2`` along ``v_dir``.
    """
    origin = np.asarray(origin, dtype=float).reshape(3)
    u = np.asarray(u_dir, dtype=float).reshape(3)
    v = np.asarray(v_dir, dtype=float).reshape(3)
    u = u / np.linalg.norm(u)
    v = v / np.linalg.norm(v)
    us = np.linspace(-u_len / 2, u_len / 2, nu)
    vs = np.linspace(-v_len / 2, v_len / 2, nv)
    uu, vv = np.meshgrid(us, vs, indexing="ij")
    pts = (
        origin
        + uu.ravel()[:, None] * u
        + vv.ravel()[:, None] * v
    )
    return pts, (nu, nv, 1)


def line_points(p0: np.ndarray, p1: np.ndarray, n: int) -> np.ndarray:
    """``n`` points along the segment from ``p0`` to ``p1`` (probe line)."""
    p0 = np.asarray(p0, dtype=float).reshape(3)
    p1 = np.asarray(p1, dtype=float).reshape(3)
    t = np.linspace(0.0, 1.0, n)[:, None]
    return p0 + t * (p1 - p0)
