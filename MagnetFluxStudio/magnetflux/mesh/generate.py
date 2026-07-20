"""Tetrahedral mesh generation (Milestone: Mesh Engine).

A dependency-free **structured** tet mesher (each grid cell split into 6
tetrahedra) plus an optional **Gmsh** path for conforming unstructured meshes.
Both yield a :class:`VolumeMesh` (points + tets) shared with the solver.
"""

from __future__ import annotations

import numpy as np

from magnetflux.core.geometry import BoundingBox
from magnetflux.solver.meshing import VolumeMesh, is_gmsh_available, mesh_air_domain

# Six-tetrahedron decomposition of a hex cell (all sharing the 0-6 diagonal).
_HEX_TETS = (
    (0, 1, 2, 6), (0, 2, 3, 6), (0, 3, 7, 6),
    (0, 7, 4, 6), (0, 4, 5, 6), (0, 5, 1, 6),
)


def structured_tet_mesh(domain: BoundingBox, nx: int, ny: int, nz: int) -> VolumeMesh:
    """Structured tetrahedral mesh of ``domain`` with ``nx x ny x nz`` cells."""
    xs = np.linspace(domain.min_corner[0], domain.max_corner[0], nx + 1)
    ys = np.linspace(domain.min_corner[1], domain.max_corner[1], ny + 1)
    zs = np.linspace(domain.min_corner[2], domain.max_corner[2], nz + 1)
    xx, yy, zz = np.meshgrid(xs, ys, zs, indexing="ij")
    points = np.column_stack([xx.ravel(), yy.ravel(), zz.ravel()])

    def nid(i, j, k):
        return (i * (ny + 1) + j) * (nz + 1) + k

    tets: list[list[int]] = []
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                corners = [
                    nid(i, j, k), nid(i + 1, j, k), nid(i + 1, j + 1, k),
                    nid(i, j + 1, k), nid(i, j, k + 1), nid(i + 1, j, k + 1),
                    nid(i + 1, j + 1, k + 1), nid(i, j + 1, k + 1),
                ]
                for t in _HEX_TETS:
                    tets.append([corners[c] for c in t])

    return VolumeMesh(points, np.asarray(tets, dtype=np.int64),
                      np.ones(len(tets), dtype=np.int64))


def generate_mesh(
    domain: BoundingBox, mesh_size: float, backend: str = "structured"
) -> VolumeMesh:
    """Generate a tet mesh of ``domain``.

    Args:
        domain: Bounding box to mesh.
        mesh_size: Target element size [m] (used by both backends).
        backend: ``"structured"`` (default, dependency-free) or ``"gmsh"``.
    """
    if backend == "gmsh":
        if not is_gmsh_available():
            raise RuntimeError("Gmsh backend requested but Gmsh is not installed")
        return mesh_air_domain(domain, mesh_size)
    if backend != "structured":
        raise ValueError(f"unknown mesh backend '{backend}'")
    size = domain.size
    n = [max(1, int(round(s / mesh_size))) for s in size]
    return structured_tet_mesh(domain, n[0], n[1], n[2])
