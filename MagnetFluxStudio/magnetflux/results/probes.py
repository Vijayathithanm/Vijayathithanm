"""Cut-line and cut-plane extraction from a sampled field (Milestone: Results).

Interpolates a solved :class:`StructuredField` along a line or over a plane so
the user can plot ``|B|`` versus position (cut line) or extract a field slice
without re-solving.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from magnetflux.core.geometry import BoundingBox
from magnetflux.visualization.probe import GridProbe
from magnetflux.visualization.sampling import StructuredField, line_points, plane_points


@dataclass(slots=True)
class CutLine:
    """Field sampled along a straight probe line.

    Attributes:
        points: ``(n, 3)`` sample coordinates [m].
        arc_length: ``(n,)`` distance from the start [m].
        b: ``(n, 3)`` interpolated flux density [T].
    """

    points: np.ndarray
    arc_length: np.ndarray
    b: np.ndarray

    @property
    def b_magnitude(self) -> np.ndarray:
        return np.linalg.norm(self.b, axis=1)


def _bounds(field: StructuredField) -> BoundingBox:
    return BoundingBox.from_points(field.points)


def cut_line(field: StructuredField, p0, p1, n: int = 60) -> CutLine:
    """Interpolate the field along the segment ``p0 -> p1`` (``n`` samples)."""
    bb = _bounds(field)
    probe = GridProbe(field, bb.min_corner, bb.max_corner)
    pts = line_points(p0, p1, n)
    b = probe.at(pts)
    s = np.linalg.norm(pts - np.asarray(p0, dtype=float).reshape(3), axis=1)
    return CutLine(points=pts, arc_length=s, b=b)


def cut_plane(
    field: StructuredField, origin, u_dir, v_dir, u_len, v_len, nu=40, nv=40
) -> StructuredField:
    """Interpolate the field over a rectangular plane, as a new StructuredField."""
    from magnetflux.solver.base import FieldResult

    bb = _bounds(field)
    probe = GridProbe(field, bb.min_corner, bb.max_corner)
    pts, dims = plane_points(origin, u_dir, v_dir, u_len, v_len, nu, nv)
    b = probe.at(pts)
    return StructuredField(pts, FieldResult(pts, b), dims)
