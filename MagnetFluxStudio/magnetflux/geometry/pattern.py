"""Linear and polar pattern arrays (Milestone: Geometry).

Replicate a mesh into a linear row or a circular (polar) array -- the latter is
how magnetron ring-magnet layouts are built. Returns one mesh per instance
(the original included).
"""

from __future__ import annotations

import numpy as np

from magnetflux.core.geometry import TriangleMesh
from magnetflux.geometry.transform import rotate, translate


def linear_array(
    mesh: TriangleMesh, direction, spacing: float, count: int
) -> list[TriangleMesh]:
    """``count`` copies of ``mesh`` spaced ``spacing`` apart along ``direction``."""
    if count < 1:
        raise ValueError("count must be >= 1")
    d = np.asarray(direction, dtype=float).reshape(3)
    d = d / np.linalg.norm(d)
    return [translate(mesh, k * spacing * d) for k in range(count)]


def polar_array(
    mesh: TriangleMesh, axis, center, count: int, total_angle: float = 2 * np.pi
) -> list[TriangleMesh]:
    """``count`` copies of ``mesh`` rotated evenly about ``axis`` through ``center``.

    A full ``2*pi`` array places ``count`` copies at ``360/count`` spacing.
    """
    if count < 1:
        raise ValueError("count must be >= 1")
    full = abs(total_angle - 2 * np.pi) < 1e-9
    step = total_angle / count if full else total_angle / max(count - 1, 1)
    return [rotate(mesh, axis, k * step, center) for k in range(count)]
