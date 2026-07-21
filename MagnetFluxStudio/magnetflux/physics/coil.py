"""Current-carrying coil sources via the Biot-Savart law (Milestone: Physics).

Computes the magnetic field of circular current loops and solenoids by
discretising the conductor and summing Biot-Savart contributions:

    B(p) = mu_0 I / (4 pi) * integral( dl x r_hat / |r|^2 ).

Validated against the closed-form on-axis field of a circular loop,
``Bz(z) = mu_0 I R^2 / (2 (R^2 + z^2)^{3/2})``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from magnetflux.config import MU_0

_FOUR_PI = 4.0 * np.pi


def _orthonormal_frame(axis: np.ndarray):
    a = np.asarray(axis, dtype=float).reshape(3)
    a = a / np.linalg.norm(a)
    ref = np.array([1.0, 0.0, 0.0]) if abs(a[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    e1 = ref - np.dot(ref, a) * a
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(a, e1)
    return e1, e2, a


def loop_axial_field(z: np.ndarray | float, radius: float, current: float) -> np.ndarray | float:
    """Closed-form on-axis flux density of a circular current loop [T]."""
    z = np.asarray(z, dtype=float)
    return MU_0 * current * radius**2 / (2.0 * (radius**2 + z**2) ** 1.5)


def circular_loop_field(
    points: np.ndarray, center, axis, radius: float, current: float, segments: int = 180
) -> np.ndarray:
    """Biot-Savart field [T] of a circular current loop at ``points`` (N, 3)."""
    pts = np.asarray(points, dtype=float).reshape(-1, 3)
    center = np.asarray(center, dtype=float).reshape(3)
    e1, e2, _ = _orthonormal_frame(axis)

    theta = np.linspace(0.0, 2.0 * np.pi, segments, endpoint=False)
    dtheta = 2.0 * np.pi / segments
    # Source points on the loop and tangent (dl) vectors.
    src = center + radius * (np.cos(theta)[:, None] * e1 + np.sin(theta)[:, None] * e2)
    dl = radius * dtheta * (-np.sin(theta)[:, None] * e1 + np.cos(theta)[:, None] * e2)

    b = np.zeros_like(pts)
    coeff = MU_0 * current / _FOUR_PI
    for start in range(0, segments, 60):
        s = src[start:start + 60]
        d = dl[start:start + 60]
        r = pts[:, None, :] - s[None, :, :]          # (N, S, 3)
        dist = np.linalg.norm(r, axis=2)             # (N, S)
        inv3 = np.where(dist > 1e-12, dist**-3, 0.0)
        cross = np.cross(d[None, :, :], r)           # dl x r  -> (N, S, 3)
        b += coeff * np.einsum("ns,nsk->nk", inv3, cross)
    return b


@dataclass(slots=True)
class CoilSource:
    """A coil source descriptor.

    Attributes:
        center: Coil centre [m].
        axis: Coil axis (current circulates in the plane normal to it).
        radius: Coil radius [m].
        current: Current per turn [A].
        turns: Number of turns (>=1); a solenoid if ``length`` > 0.
        length: Axial length [m] over which the turns are distributed.
    """

    center: tuple[float, float, float] = (0.0, 0.0, 0.0)
    axis: tuple[float, float, float] = (0.0, 0.0, 1.0)
    radius: float = 0.02
    current: float = 1.0
    turns: int = 1
    length: float = 0.0

    def field(self, points: np.ndarray) -> np.ndarray:
        """Total Biot-Savart field [T] of this coil at ``points``."""
        _, _, a = _orthonormal_frame(self.axis)
        center = np.asarray(self.center, dtype=float).reshape(3)
        if self.turns <= 1 or self.length <= 0:
            return circular_loop_field(points, center, self.axis, self.radius, self.current)
        # Solenoid: stack ``turns`` loops evenly along the axis.
        offsets = np.linspace(-self.length / 2, self.length / 2, self.turns)
        total = np.zeros((np.asarray(points).reshape(-1, 3).shape[0], 3))
        for off in offsets:
            total += circular_loop_field(points, center + off * a, self.axis,
                                         self.radius, self.current)
        return total
