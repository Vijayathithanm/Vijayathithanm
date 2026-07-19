"""Magnetization direction specification and evaluation (Milestone 2).

A magnet's magnetisation direction is defined per body. The default convention
is a per-body local frame with presets suited to magnetron ring magnets:

* ``UNIFORM``   -- a single global direction vector.
* ``AXIAL``     -- along a reference axis (e.g. a cylinder's axis).
* ``RADIAL``    -- pointing outward from a reference axis (cylindrical ring).
* ``DIAMETRIC`` -- uniform, perpendicular to the axis (diametric ring magnet).

:meth:`MagnetizationSpec.direction_at` returns unit vectors at arbitrary
points, so the solver can build a spatially varying magnetisation for radial
magnets, not just a constant.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import numpy as np


class MagnetizationMode(str, Enum):
    UNIFORM = "uniform"
    AXIAL = "axial"
    RADIAL = "radial"
    DIAMETRIC = "diametric"


def _unit(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float).reshape(3)
    n = np.linalg.norm(v)
    if n == 0:
        raise ValueError("direction/axis vector must be non-zero")
    return v / n


@dataclass(slots=True)
class MagnetizationSpec:
    """Direction of magnetisation for a permanent-magnet body.

    Attributes:
        mode: One of :class:`MagnetizationMode`.
        direction: Reference direction (UNIFORM / DIAMETRIC), any non-zero vec.
        axis: Reference axis (AXIAL / RADIAL / DIAMETRIC).
        origin: Point on the axis (RADIAL), in metres.
    """

    mode: MagnetizationMode = MagnetizationMode.AXIAL
    direction: tuple[float, float, float] = (0.0, 0.0, 1.0)
    axis: tuple[float, float, float] = (0.0, 0.0, 1.0)
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0)

    def direction_at(self, points: np.ndarray) -> np.ndarray:
        """Return ``(N, 3)`` unit magnetisation directions at ``points`` [m]."""
        pts = np.asarray(points, dtype=float).reshape(-1, 3)
        n = len(pts)

        if self.mode is MagnetizationMode.UNIFORM:
            return np.tile(_unit(self.direction), (n, 1))

        if self.mode is MagnetizationMode.AXIAL:
            return np.tile(_unit(self.axis), (n, 1))

        if self.mode is MagnetizationMode.DIAMETRIC:
            # Component of `direction` perpendicular to the axis.
            ax = _unit(self.axis)
            d = np.asarray(self.direction, dtype=float).reshape(3)
            perp = d - np.dot(d, ax) * ax
            return np.tile(_unit(perp), (n, 1))

        # RADIAL: outward from the axis line through `origin`.
        ax = _unit(self.axis)
        origin = np.asarray(self.origin, dtype=float).reshape(3)
        rel = pts - origin
        axial_comp = (rel @ ax)[:, None] * ax
        radial = rel - axial_comp
        norms = np.linalg.norm(radial, axis=1, keepdims=True)
        # On the axis (norm 0) the radial direction is undefined; use `direction`.
        fallback = _unit(self.direction)
        out = np.divide(radial, norms, out=np.tile(fallback, (n, 1)),
                        where=norms > 1e-12)
        return out

    # -- serialization ---------------------------------------------------- #

    def to_dict(self) -> dict:
        return {
            "mode": self.mode.value,
            "direction": list(self.direction),
            "axis": list(self.axis),
            "origin": list(self.origin),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MagnetizationSpec":
        return cls(
            mode=MagnetizationMode(data.get("mode", "axial")),
            direction=tuple(data.get("direction", (0.0, 0.0, 1.0))),
            axis=tuple(data.get("axis", (0.0, 0.0, 1.0))),
            origin=tuple(data.get("origin", (0.0, 0.0, 0.0))),
        )
