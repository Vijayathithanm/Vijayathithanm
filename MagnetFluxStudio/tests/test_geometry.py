"""Tests for core geometry primitives."""

import numpy as np
import pytest

from magnetflux.core.geometry import BoundingBox, TriangleMesh


def _unit_cube_mesh() -> TriangleMesh:
    v = np.array(
        [
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
        ],
        dtype=float,
    )
    f = np.array(
        [
            [0, 1, 2], [0, 2, 3], [4, 5, 6], [4, 6, 7],
            [0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6],
            [1, 2, 6], [1, 6, 5], [0, 3, 7], [0, 7, 4],
        ]
    )
    return TriangleMesh(v, f)


def test_bounding_box_properties():
    bb = BoundingBox([0, 0, 0], [2, 4, 6])
    assert np.allclose(bb.center, [1, 2, 3])
    assert np.allclose(bb.size, [2, 4, 6])
    assert bb.diagonal == pytest.approx(np.sqrt(4 + 16 + 36))


def test_bounding_box_rejects_inverted():
    with pytest.raises(ValueError):
        BoundingBox([1, 0, 0], [0, 0, 0])


def test_bounding_box_padded_triples_size():
    bb = BoundingBox([-1, -1, -1], [1, 1, 1])
    padded = bb.padded(2.0)
    assert np.allclose(padded.size, [6, 6, 6])
    assert np.allclose(padded.center, bb.center)


def test_bounding_box_contains_and_union():
    bb = BoundingBox([0, 0, 0], [1, 1, 1])
    mask = bb.contains([[0.5, 0.5, 0.5], [2, 2, 2]])
    assert mask.tolist() == [True, False]
    u = BoundingBox.union([BoundingBox([0, 0, 0], [1, 1, 1]),
                           BoundingBox([2, 2, 2], [3, 3, 3])])
    assert np.allclose(u.min_corner, [0, 0, 0])
    assert np.allclose(u.max_corner, [3, 3, 3])


def test_mesh_area_and_bbox():
    mesh = _unit_cube_mesh()
    assert mesh.surface_area() == pytest.approx(6.0)
    bb = mesh.bounding_box()
    assert np.allclose(bb.size, [1, 1, 1])


def test_mesh_scaled_for_unit_conversion():
    mesh = _unit_cube_mesh().scaled(1e-3)  # mm -> m
    assert mesh.surface_area() == pytest.approx(6.0e-6)


def test_mesh_rejects_bad_face_index():
    with pytest.raises(ValueError):
        TriangleMesh(np.zeros((3, 3)), np.array([[0, 1, 5]]))
