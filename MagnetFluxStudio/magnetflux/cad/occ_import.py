"""STEP / IGES import via pythonOCC (optional dependency).

pythonOCC (``OCP`` / ``OCC``) reads B-rep CAD and we tessellate each solid into
a :class:`~magnetflux.core.geometry.TriangleMesh`. Multi-solid assemblies yield
one mesh per solid so the model tree can list them separately.

The import is guarded by :func:`is_occ_available`; the rest of the app degrades
gracefully (STL still works) when pythonOCC is not installed.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from magnetflux.core.geometry import TriangleMesh


def is_occ_available() -> bool:
    """Whether pythonOCC is importable in this environment."""
    try:
        import OCC.Core.STEPControl  # noqa: F401
        return True
    except ImportError:
        return False


def _shape_to_meshes(shape, lin_deflection: float = 0.5) -> list[TriangleMesh]:
    """Tessellate every solid in an OCC shape into triangle meshes."""
    from OCC.Core.BRep import BRep_Tool
    from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
    from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_SOLID
    from OCC.Core.TopExp import TopExp_Explorer
    from OCC.Core.TopLoc import TopLoc_Location
    from OCC.Core.TopoDS import topods

    meshes: list[TriangleMesh] = []
    solid_exp = TopExp_Explorer(shape, TopAbs_SOLID)
    solids = []
    while solid_exp.More():
        solids.append(solid_exp.Current())
        solid_exp.Next()
    # Fall back to treating the whole shape as one body if no solids are found.
    targets = solids if solids else [shape]

    for solid in targets:
        BRepMesh_IncrementalMesh(solid, lin_deflection)
        verts: list[list[float]] = []
        faces: list[list[int]] = []
        face_exp = TopExp_Explorer(solid, TopAbs_FACE)
        while face_exp.More():
            face = topods.Face(face_exp.Current())
            loc = TopLoc_Location()
            tri = BRep_Tool.Triangulation(face, loc)
            if tri is not None:
                trsf = loc.Transformation()
                base = len(verts)
                for i in range(1, tri.NbNodes() + 1):
                    p = tri.Node(i).Transformed(trsf)
                    verts.append([p.X(), p.Y(), p.Z()])
                for i in range(1, tri.NbTriangles() + 1):
                    a, b, c = tri.Triangle(i).Get()
                    faces.append([base + a - 1, base + b - 1, base + c - 1])
            face_exp.Next()
        if verts and faces:
            meshes.append(TriangleMesh(np.asarray(verts), np.asarray(faces)))
    return meshes


def read_step(path: str | Path) -> list[TriangleMesh]:
    """Read a STEP file, returning one mesh per solid."""
    from OCC.Core.IFSelect import IFSelect_RetDone
    from OCC.Core.STEPControl import STEPControl_Reader

    reader = STEPControl_Reader()
    if reader.ReadFile(str(path)) != IFSelect_RetDone:
        raise ValueError(f"failed to read STEP file: {path}")
    reader.TransferRoots()
    return _shape_to_meshes(reader.OneShape())


def read_iges(path: str | Path) -> list[TriangleMesh]:
    """Read an IGES file, returning one mesh per solid."""
    from OCC.Core.IFSelect import IFSelect_RetDone
    from OCC.Core.IGESControl import IGESControl_Reader

    reader = IGESControl_Reader()
    if reader.ReadFile(str(path)) != IFSelect_RetDone:
        raise ValueError(f"failed to read IGES file: {path}")
    reader.TransferRoots()
    return _shape_to_meshes(reader.OneShape())
