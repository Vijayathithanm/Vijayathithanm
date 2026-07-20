"""Mesh engine: tetrahedral generation and element-quality statistics."""

from magnetflux.mesh.generate import generate_mesh, structured_tet_mesh
from magnetflux.mesh.quality import (
    MeshStatistics,
    mesh_statistics,
    tetra_quality,
    tetra_volumes,
)

__all__ = [
    "generate_mesh",
    "structured_tet_mesh",
    "tetra_quality",
    "tetra_volumes",
    "mesh_statistics",
    "MeshStatistics",
]
