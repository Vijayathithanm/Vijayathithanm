"""Tests for geometry operations: transforms, arrays, booleans, volume."""

import numpy as np
import pytest

from magnetflux.core.geometry import TriangleMesh
from magnetflux.geometry.boolean import boolean
from magnetflux.geometry.boolean import is_available as booleans_available
from magnetflux.geometry.pattern import linear_array, polar_array
from magnetflux.geometry.transform import mirror_mesh, rotate, scale, translate


def _unit_cube() -> TriangleMesh:
    v = np.array([
        [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
    ], dtype=float)
    f = np.array([
        [0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7],
        [0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6],
        [1, 2, 6], [1, 6, 5], [0, 4, 7], [0, 7, 3],
    ])
    return TriangleMesh(v, f)


# -- transforms ---------------------------------------------------------------

def test_translate_moves_bounding_box():
    m = translate(_unit_cube(), [10, 0, 0])
    assert np.allclose(m.bounding_box().min_corner, [10, 0, 0])


def test_rotate_preserves_volume():
    cube = _unit_cube()
    rotated = rotate(cube, [0, 0, 1], np.pi / 4, center=[0.5, 0.5, 0.5])
    assert rotated.volume() == pytest.approx(cube.volume(), rel=1e-9)


def test_scale_scales_volume():
    scaled = scale(_unit_cube(), 2.0)
    assert scaled.volume() == pytest.approx(8.0, rel=1e-9)


def test_mirror_preserves_volume_sign():
    mirrored = mirror_mesh(_unit_cube(), [1, 0, 0])
    # Winding is flipped so the volume stays positive and equal.
    assert mirrored.volume() == pytest.approx(1.0, rel=1e-9)


# -- arrays -------------------------------------------------------------------

def test_linear_array_positions():
    parts = linear_array(_unit_cube(), [1, 0, 0], spacing=2.0, count=3)
    assert len(parts) == 3
    centres = [p.bounding_box().center[0] for p in parts]
    assert np.allclose(centres, [0.5, 2.5, 4.5])


def test_polar_array_count_and_radius():
    cube = translate(_unit_cube(), [0.04, 0, 0])  # off-axis so it forms a ring
    parts = polar_array(cube, axis=[0, 0, 1], center=[0, 0, 0], count=6)
    assert len(parts) == 6
    radii = [np.hypot(*p.bounding_box().center[:2]) for p in parts]
    assert np.allclose(radii, radii[0], rtol=1e-6)  # all on the same ring


# -- booleans -----------------------------------------------------------------

@pytest.mark.skipif(not booleans_available(), reason="gmsh not available")
def test_boolean_union_volume():
    a = {"shape": "box", "center": [0, 0, 0], "dims": [1, 1, 1]}
    b = {"shape": "box", "center": [0.5, 0, 0], "dims": [1, 1, 1]}
    result = boolean("union", [a], [b])
    # Two unit boxes overlapping by half -> union volume 1.5.
    assert result.volume() == pytest.approx(1.5, rel=0.02)


@pytest.mark.skipif(not booleans_available(), reason="gmsh not available")
def test_boolean_difference_volume():
    a = {"shape": "box", "center": [0, 0, 0], "dims": [1, 1, 1]}
    b = {"shape": "box", "center": [0.5, 0, 0], "dims": [1, 1, 1]}
    result = boolean("difference", [a], [b])
    assert result.volume() == pytest.approx(0.5, rel=0.02)


@pytest.mark.skipif(not booleans_available(), reason="gmsh not available")
def test_boolean_intersection_volume():
    a = {"shape": "box", "center": [0, 0, 0], "dims": [1, 1, 1]}
    b = {"shape": "box", "center": [0.5, 0, 0], "dims": [1, 1, 1]}
    result = boolean("intersection", [a], [b])
    assert result.volume() == pytest.approx(0.5, rel=0.02)
