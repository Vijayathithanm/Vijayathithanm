"""Tests for the mesh engine: structured generation, quality, statistics."""

import numpy as np
import pytest

from magnetflux.core.geometry import BoundingBox
from magnetflux.mesh.generate import generate_mesh, structured_tet_mesh
from magnetflux.mesh.quality import mesh_statistics, tetra_quality, tetra_volumes


def test_structured_mesh_counts_and_volume():
    box = BoundingBox([0, 0, 0], [1, 1, 1])
    mesh = structured_tet_mesh(box, 1, 1, 1)
    assert mesh.tets.shape == (6, 4)          # 6 tets per hex cell
    assert mesh.points.shape == (8, 3)        # 2x2x2 nodes
    # The six tets tile the cube exactly.
    assert tetra_volumes(mesh.points, mesh.tets).sum() == pytest.approx(1.0)


def test_structured_mesh_multicell_volume():
    box = BoundingBox([0, 0, 0], [2, 1, 1])
    mesh = structured_tet_mesh(box, 2, 1, 1)
    assert mesh.tets.shape[0] == 6 * 2
    assert tetra_volumes(mesh.points, mesh.tets).sum() == pytest.approx(2.0)


def test_regular_tetrahedron_quality_is_one():
    # A regular tetrahedron has mean-ratio quality 1.
    pts = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], dtype=float)
    tets = np.array([[0, 1, 2, 3]])
    assert tetra_quality(pts, tets)[0] == pytest.approx(1.0, abs=1e-9)


def test_sliver_tetrahedron_has_low_quality():
    # Nearly coplanar (sliver) tetrahedron -> quality near 0.
    pts = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0.4, 0.4, 1e-4]], dtype=float)
    tets = np.array([[0, 1, 2, 3]])
    assert tetra_quality(pts, tets)[0] < 0.05


def test_mesh_statistics():
    box = BoundingBox([0, 0, 0], [1, 1, 1])
    mesh = structured_tet_mesh(box, 2, 2, 2)
    stats = mesh_statistics(mesh.points, mesh.tets)
    assert stats.n_elements == 6 * 8
    assert stats.total_volume == pytest.approx(1.0)
    assert 0.0 < stats.min_quality <= 1.0
    assert stats.min_quality <= stats.mean_quality + 1e-9
    assert stats.mean_quality <= stats.max_quality + 1e-9
    assert stats.max_quality <= 1.0


def test_generate_mesh_structured_respects_size():
    box = BoundingBox([0, 0, 0], [1, 1, 1])
    mesh = generate_mesh(box, mesh_size=0.5, backend="structured")
    # ~2 cells per axis -> 8 hexes -> 48 tets.
    assert mesh.tets.shape[0] == 6 * 8


def test_generate_mesh_rejects_unknown_backend():
    with pytest.raises(ValueError):
        generate_mesh(BoundingBox([0, 0, 0], [1, 1, 1]), 0.5, backend="bogus")
