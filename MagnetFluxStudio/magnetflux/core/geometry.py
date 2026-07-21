"""Geometry primitives: bounding boxes and triangle meshes.

Backend-agnostic containers. CAD importers (pythonOCC, STL readers) produce
:class:`TriangleMesh` instances; the viewport and solver consume them.
All coordinates are SI (metres).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class BoundingBox:
    """An axis-aligned bounding box in 3D.

    Attributes:
        min_corner: ``(3,)`` array with the minimum x, y, z coordinates.
        max_corner: ``(3,)`` array with the maximum x, y, z coordinates.
    """

    min_corner: np.ndarray
    max_corner: np.ndarray

    def __post_init__(self) -> None:
        mn = np.asarray(self.min_corner, dtype=float).reshape(3)
        mx = np.asarray(self.max_corner, dtype=float).reshape(3)
        if np.any(mx < mn):
            raise ValueError("max_corner must be component-wise >= min_corner")
        object.__setattr__(self, "min_corner", mn)
        object.__setattr__(self, "max_corner", mx)

    @property
    def center(self) -> np.ndarray:
        """Geometric centre of the box."""
        return 0.5 * (self.min_corner + self.max_corner)

    @property
    def size(self) -> np.ndarray:
        """Extent along each axis (``max - min``)."""
        return self.max_corner - self.min_corner

    @property
    def diagonal(self) -> float:
        """Length of the box's space diagonal."""
        return float(np.linalg.norm(self.size))

    def padded(self, factor: float) -> "BoundingBox":
        """Return a box grown symmetrically about its centre.

        Args:
            factor: Padding as a fraction of each half-extent. ``factor=2.0``
                triples the total size (model plus 2x on each side).
        """
        if factor < 0:
            raise ValueError("factor must be non-negative")
        half = 0.5 * self.size * (1.0 + factor)
        c = self.center
        return BoundingBox(c - half, c + half)

    def contains(self, points: np.ndarray) -> np.ndarray:
        """Boolean mask of which ``(N, 3)`` points lie inside the box."""
        pts = np.asarray(points, dtype=float).reshape(-1, 3)
        return np.all(pts >= self.min_corner, axis=1) & np.all(
            pts <= self.max_corner, axis=1
        )

    @classmethod
    def from_points(cls, points: np.ndarray) -> "BoundingBox":
        """Build the tightest box enclosing a set of ``(N, 3)`` points."""
        pts = np.asarray(points, dtype=float).reshape(-1, 3)
        if pts.size == 0:
            raise ValueError("cannot build a bounding box from zero points")
        return cls(pts.min(axis=0), pts.max(axis=0))

    @staticmethod
    def union(boxes: list["BoundingBox"]) -> "BoundingBox":
        """Smallest box enclosing every box in ``boxes``."""
        if not boxes:
            raise ValueError("cannot union an empty list of boxes")
        mn = np.min([b.min_corner for b in boxes], axis=0)
        mx = np.max([b.max_corner for b in boxes], axis=0)
        return BoundingBox(mn, mx)


@dataclass(slots=True)
class TriangleMesh:
    """A triangulated surface mesh.

    Attributes:
        vertices: ``(V, 3)`` float array of vertex coordinates [m].
        faces: ``(F, 3)`` int array of vertex indices (one row per triangle).
    """

    vertices: np.ndarray
    faces: np.ndarray

    def __post_init__(self) -> None:
        v = np.asarray(self.vertices, dtype=float).reshape(-1, 3)
        f = np.asarray(self.faces, dtype=np.int64).reshape(-1, 3)
        if f.size and (f.min() < 0 or f.max() >= len(v)):
            raise ValueError("face indices out of range for vertex array")
        self.vertices = v
        self.faces = f

    @property
    def n_vertices(self) -> int:
        return len(self.vertices)

    @property
    def n_faces(self) -> int:
        return len(self.faces)

    def bounding_box(self) -> BoundingBox:
        """Axis-aligned bounding box of the mesh vertices."""
        return BoundingBox.from_points(self.vertices)

    def centroid(self) -> np.ndarray:
        """Area-weighted centroid of the triangulated surface."""
        tris = self.vertices[self.faces]
        tri_centroids = tris.mean(axis=1)
        ab = tris[:, 1] - tris[:, 0]
        ac = tris[:, 2] - tris[:, 0]
        areas = 0.5 * np.linalg.norm(np.cross(ab, ac), axis=1)
        total = areas.sum()
        if total == 0:
            return self.vertices.mean(axis=0)
        return (tri_centroids * areas[:, None]).sum(axis=0) / total

    def surface_area(self) -> float:
        """Total surface area of the mesh [m^2]."""
        tris = self.vertices[self.faces]
        ab = tris[:, 1] - tris[:, 0]
        ac = tris[:, 2] - tris[:, 0]
        return float(0.5 * np.linalg.norm(np.cross(ab, ac), axis=1).sum())

    def volume(self) -> float:
        """Enclosed volume [m^3] via the divergence theorem (closed meshes).

        Sums the signed tetrahedron volumes of each face with the origin;
        returns the magnitude, so it is orientation-independent.
        """
        tris = self.vertices[self.faces]
        v0, v1, v2 = tris[:, 0], tris[:, 1], tris[:, 2]
        return float(abs(np.einsum("ij,ij->i", v0, np.cross(v1, v2)).sum()) / 6.0)

    def scaled(self, factor: float) -> "TriangleMesh":
        """Return a copy with vertices scaled by ``factor`` (unit conversion)."""
        return TriangleMesh(self.vertices * factor, self.faces.copy())

    def translated(self, offset: np.ndarray) -> "TriangleMesh":
        """Return a copy translated by ``offset`` ``(3,)``."""
        offset = np.asarray(offset, dtype=float).reshape(3)
        return TriangleMesh(self.vertices + offset, self.faces.copy())
