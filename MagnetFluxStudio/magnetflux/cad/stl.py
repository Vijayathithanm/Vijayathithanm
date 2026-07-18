"""Pure-NumPy STL reader (ASCII and binary).

STL needs no CAD kernel, so this reader is dependency-free and fully unit
tested. STEP/IGES import lives in :mod:`magnetflux.cad.occ_import` and requires
pythonOCC. All readers return a :class:`~magnetflux.core.geometry.TriangleMesh`
in the file's native units; unit scaling to metres is applied by
:mod:`magnetflux.cad.importer`.
"""

from __future__ import annotations

import struct
from pathlib import Path

import numpy as np

from magnetflux.core.geometry import TriangleMesh


def _is_binary_stl(path: Path) -> bool:
    """Heuristically decide whether an STL file is binary.

    A binary STL declares its triangle count at byte 80; the file size must then
    equal ``84 + 50 * n``. ASCII files rarely satisfy this, so it is a reliable
    discriminator even when the header text starts with ``solid``.
    """
    size = path.stat().st_size
    if size < 84:
        return False
    with path.open("rb") as fh:
        fh.seek(80)
        (n_tri,) = struct.unpack("<I", fh.read(4))
    return size == 84 + n_tri * 50


def _dedup_vertices(tri_vertices: np.ndarray) -> TriangleMesh:
    """Collapse ``(F, 3, 3)`` per-triangle vertices into an indexed mesh."""
    flat = tri_vertices.reshape(-1, 3)
    unique, inverse = np.unique(flat, axis=0, return_inverse=True)
    faces = inverse.reshape(-1, 3)
    return TriangleMesh(unique, faces)


def read_binary_stl(path: Path) -> TriangleMesh:
    """Read a binary STL file into a :class:`TriangleMesh`."""
    with path.open("rb") as fh:
        fh.seek(80)
        (n_tri,) = struct.unpack("<I", fh.read(4))
        # Each record: 12 floats (normal + 3 verts) then a 2-byte attribute.
        dtype = np.dtype(
            [("normal", "<3f4"), ("verts", "<3,3f4"), ("attr", "<u2")]
        )
        data = np.frombuffer(fh.read(n_tri * 50), dtype=dtype, count=n_tri)
    return _dedup_vertices(data["verts"].astype(float))


def read_ascii_stl(path: Path) -> TriangleMesh:
    """Read an ASCII STL file into a :class:`TriangleMesh`."""
    coords: list[tuple[float, float, float]] = []
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            parts = line.split()
            if parts and parts[0] == "vertex":
                coords.append((float(parts[1]), float(parts[2]), float(parts[3])))
    if len(coords) % 3 != 0:
        raise ValueError("ASCII STL has a vertex count not divisible by 3")
    tri_vertices = np.asarray(coords, dtype=float).reshape(-1, 3, 3)
    return _dedup_vertices(tri_vertices)


def read_stl(path: str | Path) -> TriangleMesh:
    """Read an STL file (auto-detecting ASCII vs binary)."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    if _is_binary_stl(path):
        return read_binary_stl(path)
    return read_ascii_stl(path)


def write_binary_stl(path: str | Path, mesh: TriangleMesh) -> Path:
    """Write a :class:`TriangleMesh` to a binary STL (used by tests/exports)."""
    path = Path(path)
    tris = mesh.vertices[mesh.faces]  # (F, 3, 3)
    ab = tris[:, 1] - tris[:, 0]
    ac = tris[:, 2] - tris[:, 0]
    normals = np.cross(ab, ac)
    norms = np.linalg.norm(normals, axis=1, keepdims=True)
    normals = np.divide(normals, norms, out=np.zeros_like(normals), where=norms > 0)
    with path.open("wb") as fh:
        fh.write(b"\x00" * 80)
        fh.write(struct.pack("<I", len(mesh.faces)))
        for i in range(len(mesh.faces)):
            fh.write(struct.pack("<3f", *normals[i].astype(np.float32)))
            for v in tris[i]:
                fh.write(struct.pack("<3f", *v.astype(np.float32)))
            fh.write(struct.pack("<H", 0))
    return path
