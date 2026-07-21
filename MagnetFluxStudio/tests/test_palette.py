"""Tests for the distinct-colour palette and auto-colouring of bodies."""

import numpy as np

from magnetflux.core.geometry import TriangleMesh
from magnetflux.core.model_tree import ModelTree
from magnetflux.core.palette import color_for_index, distinct_colors


def _tri() -> TriangleMesh:
    return TriangleMesh(
        np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float),
        np.array([[0, 1, 2]]),
    )


def test_colors_in_range():
    for c in distinct_colors(10):
        assert len(c) == 3
        assert all(0.0 <= ch <= 1.0 for ch in c)


def test_colors_are_distinct():
    cols = distinct_colors(8)
    assert len({tuple(round(x, 3) for x in c) for c in cols}) == 8


def test_color_for_index_deterministic():
    assert color_for_index(3) == color_for_index(3)


def test_bodies_get_distinct_colors_on_add():
    tree = ModelTree()
    a = tree.add_body(_tri())
    b = tree.add_body(_tri())
    c = tree.add_body(_tri())
    colors = {a.color, b.color, c.color}
    assert len(colors) == 3          # not all the same grey
    assert a.color == color_for_index(0)
    assert b.color == color_for_index(1)
