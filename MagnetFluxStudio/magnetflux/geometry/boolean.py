"""Boolean solid operations via Gmsh OpenCASCADE (Milestone: Geometry).

Union / difference / intersection of box and cylinder primitives, meshed back
to a :class:`TriangleMesh`. Uses Gmsh's OCC kernel (pip-installable, bundled
into the app). Guarded by :func:`is_available`.
"""

from __future__ import annotations

import numpy as np

from magnetflux.core.geometry import TriangleMesh
from magnetflux.solver.meshing import is_gmsh_available as _gmsh_ok

is_available = _gmsh_ok


def _add_primitive(gmsh, prim: dict) -> tuple[int, int]:
    center = np.asarray(prim["center"], dtype=float).reshape(3)
    shape = prim.get("shape", "box")
    if shape == "box":
        dims = np.asarray(prim["dims"], dtype=float).reshape(3)
        corner = center - dims / 2.0
        tag = gmsh.model.occ.addBox(*corner, *dims)
    elif shape == "cylinder":
        axis = np.asarray(prim["axis"], dtype=float).reshape(3)
        axis = axis / np.linalg.norm(axis)
        length = float(prim["length"])
        base = center - axis * length / 2.0
        tag = gmsh.model.occ.addCylinder(*base, *(axis * length), float(prim["radius"]))
    else:
        raise ValueError(f"unsupported primitive shape '{shape}'")
    return (3, tag)


def _extract_surface(gmsh) -> TriangleMesh:
    node_tags, coords, _ = gmsh.model.mesh.getNodes()
    coords = np.asarray(coords, dtype=float).reshape(-1, 3)
    index = {int(t): i for i, t in enumerate(node_tags)}
    etypes, _etags, enodes = gmsh.model.mesh.getElements(2)
    faces = []
    for etype, conn in zip(etypes, enodes):
        if etype == 2:  # 3-node triangle
            for a, b, c in np.asarray(conn, dtype=np.int64).reshape(-1, 3):
                faces.append([index[int(a)], index[int(b)], index[int(c)]])
    return TriangleMesh(coords, np.asarray(faces, dtype=np.int64))


def boolean(op: str, objects: list[dict], tools: list[dict],
            mesh_size_factor: float = 20.0) -> TriangleMesh:
    """Apply a boolean ``op`` (``union``/``difference``/``intersection``).

    Args:
        op: One of ``"union"``, ``"difference"``, ``"intersection"``.
        objects: Primitive descriptors for the object solids.
        tools: Primitive descriptors for the tool solids.
        mesh_size_factor: Larger -> finer surface mesh (size = bbox diag / factor).

    Returns:
        The resulting solid as a surface :class:`TriangleMesh`.
    """
    if not is_available():
        raise RuntimeError("boolean operations require Gmsh")

    import gmsh

    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add("boolean")
        obj = [_add_primitive(gmsh, p) for p in objects]
        tool = [_add_primitive(gmsh, p) for p in tools]
        if op == "union":
            gmsh.model.occ.fuse(obj, tool)
        elif op == "difference":
            gmsh.model.occ.cut(obj, tool)
        elif op == "intersection":
            gmsh.model.occ.intersect(obj, tool)
        else:
            raise ValueError(f"unknown boolean op '{op}'")
        gmsh.model.occ.synchronize()

        xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.getBoundingBox(-1, -1)
        diag = float(np.linalg.norm([xmax - xmin, ymax - ymin, zmax - zmin]))
        if diag > 0:
            gmsh.option.setNumber("Mesh.MeshSizeMax", diag / mesh_size_factor)
        gmsh.model.mesh.generate(2)
        return _extract_surface(gmsh)
    finally:
        gmsh.finalize()
