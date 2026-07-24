"""Tests for per-body opacity (transparency) and its persistence."""

import numpy as np
import pytest

from magnetflux.core.geometry import TriangleMesh
from magnetflux.core.model_tree import ModelTree
from magnetflux.core.project import Project


def _tri() -> TriangleMesh:
    return TriangleMesh(
        np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float),
        np.array([[0, 1, 2]]),
    )


def test_default_opacity_is_solid():
    tree = ModelTree()
    body = tree.add_body(_tri())
    assert body.opacity == 1.0


def test_set_opacity_clamped():
    tree = ModelTree()
    body = tree.add_body(_tri())
    tree.set_opacity(body.id, 0.25)
    assert body.opacity == pytest.approx(0.25)
    tree.set_opacity(body.id, 5.0)   # clamped to 1
    assert body.opacity == 1.0
    tree.set_opacity(body.id, -1.0)  # clamped to 0
    assert body.opacity == 0.0


def test_opacity_persists_in_project(tmp_path):
    tree = ModelTree()
    casing = tree.add_body(_tri(), name="Casing")
    tree.set_opacity(casing.id, 0.25)
    path = Project(name="Assembly", model_tree=tree).save(tmp_path / "a.mfx")

    loaded = Project.load(path)
    assert loaded.model_tree.bodies[0].opacity == pytest.approx(0.25)
