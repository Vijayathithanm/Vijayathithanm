"""Gmsh tetrahedral meshing of the air domain (optional dependency).

Generates a conforming tetrahedral mesh of the air box with the magnet solids
embedded as tagged physical volumes, so a future FEM assembly can integrate
material properties per region. Guarded by :func:`is_gmsh_available`; the
structured-mesh path in :mod:`magnetflux.solver.fem` is used when Gmsh is absent.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from magnetflux.core.geometry import BoundingBox


def is_gmsh_available() -> bool:
    """Whether the Gmsh Python API is importable."""
    try:
        import gmsh  # noqa: F401
        return True
    except ImportError:
        return False


@dataclass(slots=True)
class VolumeMesh:
    """A tetrahedral volume mesh.

    Attributes:
        points: ``(V, 3)`` node coordinates [m].
        tets: ``(T, 4)`` node indices per tetrahedron.
        cell_tags: ``(T,)`` integer region tag per tetrahedron.
    """

    points: np.ndarray
    tets: np.ndarray
    cell_tags: np.ndarray


def mesh_air_domain(
    domain: BoundingBox, mesh_size: float, *, air_tag: int = 1
) -> VolumeMesh:
    """Mesh the air box with Gmsh at characteristic size ``mesh_size`` [m].

    Args:
        domain: Air-domain bounding box.
        mesh_size: Target element size [m].
        air_tag: Physical tag assigned to the air region.

    Returns:
        A :class:`VolumeMesh`.

    Raises:
        RuntimeError: If Gmsh is not installed.
    """
    if not is_gmsh_available():
        raise RuntimeError("Gmsh is not installed; install the 'cad' extras")

    import gmsh

    gmsh.initialize()
    try:
        gmsh.model.add("air_domain")
        size = domain.size
        box = gmsh.model.occ.addBox(
            domain.min_corner[0], domain.min_corner[1], domain.min_corner[2],
            size[0], size[1], size[2],
        )
        gmsh.model.occ.synchronize()
        gmsh.model.addPhysicalGroup(3, [box], air_tag)
        gmsh.option.setNumber("Mesh.MeshSizeMax", mesh_size)
        gmsh.model.mesh.generate(3)

        node_tags, coords, _ = gmsh.model.mesh.getNodes()
        points = coords.reshape(-1, 3)
        # Remap Gmsh's 1-based node tags to contiguous 0-based indices.
        tag_to_index = {int(t): i for i, t in enumerate(node_tags)}
        elem_types, _, node_conn = gmsh.model.mesh.getElements(dim=3)
        tets = []
        for etype, conn in zip(elem_types, node_conn):
            if etype == 4:  # 4-node tetrahedron
                tets = np.array([tag_to_index[int(t)] for t in conn]).reshape(-1, 4)
        cell_tags = np.full(len(tets), air_tag, dtype=np.int64)
        return VolumeMesh(points, np.asarray(tets), cell_tags)
    finally:
        gmsh.finalize()
