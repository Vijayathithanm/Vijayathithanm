"""Parametric magnet layout for optimization (Milestone 6).

Optimizing magnet spacing or pole arrangement requires a geometry that can be
*rebuilt* from design variables -- imported B-rep CAD is static. This module
provides a parametric planar-magnetron layout (a central magnet plus a
concentric ring of magnets) whose spacing, ring count and polarities are the
design variables, and which emits solver ``magnet_sources`` on demand.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from magnetflux.config import MU_0


@dataclass(slots=True)
class ParametricLayout:
    """A concentric planar-magnetron magnet layout.

    Attributes:
        magnet_dims: Full side lengths (lx, ly, lz) of each magnet [m].
        remanence_br: Magnet remanence Br [T] (sets |M| = Br/mu_0).
        ring_radius: Radius of the outer magnet ring [m] (spacing variable).
        ring_count: Number of magnets in the outer ring.
        center_polarity: +/-1 sign of the central magnet's axial magnetisation.
        ring_polarity: +/-1 sign of the ring magnets' axial magnetisation.
    """

    magnet_dims: tuple[float, float, float] = (0.02, 0.02, 0.01)
    remanence_br: float = 1.30
    ring_radius: float = 0.04
    ring_count: int = 6
    center_polarity: int = +1
    ring_polarity: int = -1

    @property
    def magnetization(self) -> float:
        """Magnetisation magnitude ``|M| = Br/mu_0`` [A/m]."""
        return self.remanence_br / MU_0

    def build_sources(
        self, ring_radius: float | None = None, ring_count: int | None = None
    ) -> list[dict]:
        """Return solver source descriptors for the (optionally overridden) layout."""
        R = self.ring_radius if ring_radius is None else ring_radius
        n = self.ring_count if ring_count is None else ring_count
        M = self.magnetization
        dims = list(self.magnet_dims)

        sources = [{
            "shape": "box", "center": [0.0, 0.0, 0.0], "dims": dims,
            "magnetization": [0.0, 0.0, self.center_polarity * M],
        }]
        for k in range(n):
            angle = 2 * np.pi * k / n
            sources.append({
                "shape": "box",
                "center": [R * np.cos(angle), R * np.sin(angle), 0.0],
                "dims": dims,
                "magnetization": [0.0, 0.0, self.ring_polarity * M],
            })
        return sources

    def target_plane_extent(self, ring_radius: float | None = None) -> float:
        """Suggested half-width of the target plane for the current spacing [m]."""
        R = self.ring_radius if ring_radius is None else ring_radius
        return 1.5 * (R + max(self.magnet_dims[:2]))
