"""STEP / IGES import via Gmsh (pip-installable, bundleable fallback).

pythonOCC gives the best B-rep import but is conda-only and cannot be frozen
into a Windows executable. Gmsh ships pip wheels (with its OpenCASCADE kernel
bundled), so it works in the packaged app. This module reads STEP/IGES with
Gmsh, tessellates each solid, and returns one
:class:`~magnetflux.core.geometry.TriangleMesh` per volume.

Vertices are in the file's native units; :mod:`magnetflux.cad.importer` applies
the unit -> metre scaling, exactly as for the STL and pythonOCC paths.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from magnetflux.core.geometry import TriangleMesh


def is_gmsh_available() -> bool:
    """Whether the Gmsh Python API is importable."""
    try:
        import gmsh  # noqa: F401
        return True
    except (ImportError, OSError):
        # OSError: shared library present but a system dependency is missing.
        return False


def _volume_mesh(gmsh, node_coords: dict[int, tuple], volume_tag: int) -> TriangleMesh | None:
    """Build a TriangleMesh for one volume from its boundary surface triangles."""
    surfaces = gmsh.model.getBoundary([(3, volume_tag)], oriented=False, recursive=False)
    local: dict[int, int] = {}
    verts: list[tuple] = []
    faces: list[list[int]] = []

    def index_of(tag: int) -> int:
        idx = local.get(tag)
        if idx is None:
            idx = len(verts)
            local[tag] = idx
            verts.append(node_coords[tag])
        return idx

    for _dim, stag in surfaces:
        etypes, _etags, enodes = gmsh.model.mesh.getElements(2, abs(stag))
        for etype, conn in zip(etypes, enodes):
            if etype == 2:  # 3-node triangle
                tri = np.asarray(conn, dtype=np.int64).reshape(-1, 3)
                for a, b, c in tri:
                    faces.append([index_of(int(a)), index_of(int(b)), index_of(int(c))])
    if not verts or not faces:
        return None
    return TriangleMesh(np.asarray(verts, dtype=float), np.asarray(faces, dtype=np.int64))


def _clean_component_name(raw: str) -> str | None:
    """Extract a usable component name from a Gmsh/STEP entity name.

    STEP assembly names may be nested ("Assembly/Bracket") or empty; return the
    last path component, or ``None`` if there is no meaningful name.
    """
    if not raw:
        return None
    name = raw.replace("\\", "/").split("/")[-1].strip()
    return name or None


def read_cad_gmsh(path: str | Path) -> list[TriangleMesh]:
    """Read a STEP/IGES file with Gmsh, returning one mesh per solid."""
    return [mesh for _name, mesh in read_cad_gmsh_named(path)]


def read_cad_gmsh_named(path: str | Path) -> list[tuple[str | None, TriangleMesh]]:
    """Read a STEP/IGES file, returning ``(component_name, mesh)`` per solid.

    The component name comes from the STEP product/part name of each solid, so
    an imported assembly lists its parts by name and materials can be assigned
    per component in a single import.

    Raises:
        RuntimeError: If Gmsh cannot be loaded.
    """
    if not is_gmsh_available():
        raise RuntimeError("Gmsh is not available for STEP/IGES import")

    import gmsh

    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add("import")
        gmsh.model.occ.importShapes(str(path))
        gmsh.model.occ.synchronize()

        # Size the surface tessellation from the overall bounding box.
        xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.getBoundingBox(-1, -1)
        diag = float(np.linalg.norm([xmax - xmin, ymax - ymin, zmax - zmin]))
        if diag > 0:
            gmsh.option.setNumber("Mesh.MeshSizeMax", diag / 40.0)
            gmsh.option.setNumber("Mesh.MeshSizeMin", diag / 400.0)
        gmsh.model.mesh.generate(2)

        node_tags, coords, _ = gmsh.model.mesh.getNodes()
        coords = np.asarray(coords, dtype=float).reshape(-1, 3)
        node_coords = {int(t): tuple(coords[i]) for i, t in enumerate(node_tags)}

        meshes: list[tuple[str | None, TriangleMesh]] = []
        for _dim, vtag in gmsh.model.getEntities(3):
            mesh = _volume_mesh(gmsh, node_coords, vtag)
            if mesh is not None:
                name = _clean_component_name(gmsh.model.getEntityName(3, vtag))
                meshes.append((name, mesh))

        # IGES/surface models may have no solids: fall back to all surfaces.
        if not meshes:
            local: dict[int, int] = {}
            verts: list[tuple] = []
            faces: list[list[int]] = []
            etypes, _etags, enodes = gmsh.model.mesh.getElements(2)
            for etype, conn in zip(etypes, enodes):
                if etype == 2:
                    tri = np.asarray(conn, dtype=np.int64).reshape(-1, 3)
                    for a, b, c in tri:
                        row = []
                        for tag in (int(a), int(b), int(c)):
                            idx = local.get(tag)
                            if idx is None:
                                idx = len(verts)
                                local[tag] = idx
                                verts.append(node_coords[tag])
                            row.append(idx)
                        faces.append(row)
            if verts and faces:
                meshes.append((None, TriangleMesh(np.asarray(verts, float),
                                                  np.asarray(faces, np.int64))))
        return meshes
    finally:
        gmsh.finalize()
