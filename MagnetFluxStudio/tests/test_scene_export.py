"""Tests for scene export: OBJ writer and turntable camera path."""

import numpy as np
import pytest

from magnetflux.core.geometry import TriangleMesh
from magnetflux.core.model_tree import ModelTree
from magnetflux.visualization.scene_export import export_obj, turntable_azimuths


def _tri(z: float = 0.0) -> TriangleMesh:
    return TriangleMesh(
        np.array([[0, 0, z], [1, 0, z], [0, 1, z]], dtype=float),
        np.array([[0, 1, 2]]),
    )


def test_export_obj_two_bodies(tmp_path):
    tree = ModelTree()
    tree.add_body(_tri(0.0), name="Part A")
    tree.add_body(_tri(1.0), name="Part B")
    path = export_obj(tree, tmp_path / "scene.obj")
    text = path.read_text()

    assert text.count("g ") == 2                 # one group per body
    assert "g Part_A" in text and "g Part_B" in text
    assert text.count("\nv ") == 6               # 3 vertices per body
    # Second body's faces must reference offset (1-based) indices 4,5,6.
    assert "f 4 5 6" in text


def test_obj_face_indices_are_one_based(tmp_path):
    tree = ModelTree()
    tree.add_body(_tri(), name="Solo")
    text = export_obj(tree, tmp_path / "s.obj").read_text()
    assert "f 1 2 3" in text


def test_turntable_azimuths():
    az = turntable_azimuths(4)
    assert np.allclose(az, [0, 90, 180, 270])
    assert len(turntable_azimuths(72)) == 72


def test_turntable_rejects_zero():
    with pytest.raises(ValueError):
        turntable_azimuths(0)
