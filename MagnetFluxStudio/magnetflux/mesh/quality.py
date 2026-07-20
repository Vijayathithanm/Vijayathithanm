"""Tetrahedral element quality and mesh statistics (Milestone: Mesh Engine).

Pure-NumPy quality metrics so mesh assessment is unit-testable without a mesher.
Uses the **mean-ratio** quality ``eta = 12 (3V)^(2/3) / sum(edge_i^2)`` which is
1 for a regular tetrahedron and approaches 0 for slivers.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

_EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def tetra_volumes(points: np.ndarray, tets: np.ndarray) -> np.ndarray:
    """Signed-magnitude volume of each tetrahedron [m^3]."""
    p = np.asarray(points, dtype=float)
    t = np.asarray(tets, dtype=np.int64).reshape(-1, 4)
    a, b, c, d = p[t[:, 0]], p[t[:, 1]], p[t[:, 2]], p[t[:, 3]]
    return np.abs(np.einsum("ij,ij->i", b - a, np.cross(c - a, d - a))) / 6.0


def tetra_quality(points: np.ndarray, tets: np.ndarray) -> np.ndarray:
    """Mean-ratio quality in ``(0, 1]`` per tetrahedron (1 = regular)."""
    p = np.asarray(points, dtype=float)
    t = np.asarray(tets, dtype=np.int64).reshape(-1, 4)
    vol = tetra_volumes(p, t)
    edge_sq = np.zeros(len(t))
    for i, j in _EDGES:
        diff = p[t[:, i]] - p[t[:, j]]
        edge_sq += np.einsum("ij,ij->i", diff, diff)
    with np.errstate(divide="ignore", invalid="ignore"):
        q = 12.0 * np.cbrt((3.0 * vol) ** 2) / edge_sq
    return np.clip(np.nan_to_num(q, nan=0.0), 0.0, 1.0)


@dataclass(slots=True)
class MeshStatistics:
    """Summary of a tetrahedral mesh."""

    n_nodes: int
    n_elements: int
    min_quality: float
    mean_quality: float
    max_quality: float
    min_volume: float
    total_volume: float

    def as_dict(self) -> dict[str, float]:
        return {
            "nodes": self.n_nodes,
            "elements": self.n_elements,
            "min quality": self.min_quality,
            "mean quality": self.mean_quality,
            "max quality": self.max_quality,
            "min volume": self.min_volume,
            "total volume": self.total_volume,
        }


def mesh_statistics(points: np.ndarray, tets: np.ndarray) -> MeshStatistics:
    """Compute node/element counts, quality and volume statistics."""
    tets = np.asarray(tets, dtype=np.int64).reshape(-1, 4)
    vol = tetra_volumes(points, tets)
    q = tetra_quality(points, tets)
    return MeshStatistics(
        n_nodes=int(np.asarray(points).reshape(-1, 3).shape[0]),
        n_elements=int(len(tets)),
        min_quality=float(q.min()) if q.size else 0.0,
        mean_quality=float(q.mean()) if q.size else 0.0,
        max_quality=float(q.max()) if q.size else 0.0,
        min_volume=float(vol.min()) if vol.size else 0.0,
        total_volume=float(vol.sum()),
    )
