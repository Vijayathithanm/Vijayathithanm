"""Boundary conditions and physics settings (Milestone: Physics).

The magnetostatics interface supports several boundary conditions. For the FEM
backend these select the outer-boundary treatment; for the analytic backend a
**symmetry** plane is realised by adding mirror-image sources.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import numpy as np


class BoundaryCondition(str, Enum):
    """Supported outer-boundary conditions for magnetostatics."""

    MAGNETIC_INSULATION = "magnetic_insulation"   # n x A = 0 (far field)
    SYMMETRY = "symmetry"                          # mirror plane
    PERIODIC = "periodic"                          # periodic array
    OPEN = "open"                                  # open / infinite element


@dataclass(slots=True)
class PhysicsSettings:
    """Physics configuration carried by a solve.

    Attributes:
        outer_boundary: Condition applied on the air-domain outer boundary.
        symmetry_plane_point: A point on the symmetry plane [m] (SYMMETRY).
        symmetry_plane_normal: The symmetry plane normal (SYMMETRY).
    """

    outer_boundary: BoundaryCondition = BoundaryCondition.MAGNETIC_INSULATION
    symmetry_plane_point: tuple[float, float, float] = (0.0, 0.0, 0.0)
    symmetry_plane_normal: tuple[float, float, float] = (0.0, 0.0, 1.0)

    def to_dict(self) -> dict:
        return {
            "outer_boundary": self.outer_boundary.value,
            "symmetry_plane_point": list(self.symmetry_plane_point),
            "symmetry_plane_normal": list(self.symmetry_plane_normal),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PhysicsSettings":
        return cls(
            outer_boundary=BoundaryCondition(data.get("outer_boundary",
                                                       "magnetic_insulation")),
            symmetry_plane_point=tuple(data.get("symmetry_plane_point", (0, 0, 0))),
            symmetry_plane_normal=tuple(data.get("symmetry_plane_normal", (0, 0, 1))),
        )


def mirror_magnet_sources(
    sources: list[dict], plane_point, plane_normal
) -> list[dict]:
    """Return image magnet sources reflected across a symmetry plane.

    A magnetic mirror plane reflects both position and the magnetisation vector
    (the tangential components flip so field lines meet the plane normally).
    """
    p0 = np.asarray(plane_point, dtype=float).reshape(3)
    n = np.asarray(plane_normal, dtype=float).reshape(3)
    n = n / np.linalg.norm(n)
    images: list[dict] = []
    for src in sources:
        center = np.asarray(src["center"], dtype=float).reshape(3)
        m = np.asarray(src["magnetization"], dtype=float).reshape(3)
        # Reflect the centre across the plane.
        center_img = center - 2.0 * np.dot(center - p0, n) * n
        # Mirror the magnetisation: flip the tangential part (image of a magnet).
        m_img = m - 2.0 * np.dot(m, n) * n
        image = dict(src)
        image["center"] = center_img
        image["magnetization"] = -m_img
        images.append(image)
    return images
