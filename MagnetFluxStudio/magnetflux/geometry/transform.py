"""Rigid/affine transforms on triangle meshes (Milestone: Geometry).

4x4 homogeneous transforms (translate, rotate, scale, mirror) and their
application to a :class:`TriangleMesh`. Orientation-reversing transforms
(mirror, negative scale) flip the triangle winding so outward normals -- and
the computed volume -- stay consistent.
"""

from __future__ import annotations

import numpy as np

from magnetflux.core.geometry import TriangleMesh


def translation(offset) -> np.ndarray:
    m = np.eye(4)
    m[:3, 3] = np.asarray(offset, dtype=float).reshape(3)
    return m


def rotation(axis, angle: float) -> np.ndarray:
    """Rotation by ``angle`` [rad] about ``axis`` (Rodrigues)."""
    a = np.asarray(axis, dtype=float).reshape(3)
    a = a / np.linalg.norm(a)
    c, s = np.cos(angle), np.sin(angle)
    x, y, z = a
    r = np.array([
        [c + x * x * (1 - c), x * y * (1 - c) - z * s, x * z * (1 - c) + y * s],
        [y * x * (1 - c) + z * s, c + y * y * (1 - c), y * z * (1 - c) - x * s],
        [z * x * (1 - c) - y * s, z * y * (1 - c) + x * s, c + z * z * (1 - c)],
    ])
    m = np.eye(4)
    m[:3, :3] = r
    return m


def scaling(factor) -> np.ndarray:
    f = np.asarray(factor, dtype=float)
    diag = np.ones(3) * f if f.ndim == 0 else f.reshape(3)
    m = np.eye(4)
    m[:3, :3] = np.diag(diag)
    return m


def mirror(plane_normal, point=(0.0, 0.0, 0.0)) -> np.ndarray:
    """Reflection across the plane through ``point`` with ``plane_normal``."""
    n = np.asarray(plane_normal, dtype=float).reshape(3)
    n = n / np.linalg.norm(n)
    p = np.asarray(point, dtype=float).reshape(3)
    house = np.eye(3) - 2.0 * np.outer(n, n)
    m = np.eye(4)
    m[:3, :3] = house
    m[:3, 3] = 2.0 * np.dot(p, n) * n
    return m


def about_center(matrix: np.ndarray, center) -> np.ndarray:
    """Wrap ``matrix`` so it acts about ``center`` instead of the origin."""
    c = np.asarray(center, dtype=float).reshape(3)
    return translation(c) @ matrix @ translation(-c)


def apply_transform(mesh: TriangleMesh, matrix: np.ndarray) -> TriangleMesh:
    """Apply a 4x4 transform to ``mesh``, fixing winding for reflections."""
    matrix = np.asarray(matrix, dtype=float)
    v = np.column_stack([mesh.vertices, np.ones(len(mesh.vertices))])
    new_v = (v @ matrix.T)[:, :3]
    faces = mesh.faces.copy()
    if np.linalg.det(matrix[:3, :3]) < 0:  # orientation reversed -> flip winding
        faces = faces[:, ::-1]
    return TriangleMesh(new_v, faces)


# -- convenience --------------------------------------------------------------

def translate(mesh: TriangleMesh, offset) -> TriangleMesh:
    return apply_transform(mesh, translation(offset))


def rotate(mesh: TriangleMesh, axis, angle: float, center=(0, 0, 0)) -> TriangleMesh:
    return apply_transform(mesh, about_center(rotation(axis, angle), center))


def scale(mesh: TriangleMesh, factor, center=(0, 0, 0)) -> TriangleMesh:
    return apply_transform(mesh, about_center(scaling(factor), center))


def mirror_mesh(mesh: TriangleMesh, plane_normal, point=(0, 0, 0)) -> TriangleMesh:
    return apply_transform(mesh, mirror(plane_normal, point))
