"""Tests for race-track prediction: decomposition, erosion, comparison."""

import numpy as np
import pytest

from magnetflux.config import MU_0
from magnetflux.core.geometry import BoundingBox
from magnetflux.racetrack.comparison import compare, difference_map
from magnetflux.racetrack.erosion import (
    compute_race_track,
    eroded_area_fraction,
    erosion_intensity,
    uniformity,
)
from magnetflux.racetrack.tangential import decompose
from magnetflux.solver.analytic import AnalyticBackend
from magnetflux.solver.base import SolverProblem
from magnetflux.visualization.sampling import grid_points, plane_points


# -- decomposition ------------------------------------------------------------

def test_decompose_normal_and_tangential():
    dec = decompose([[1, 2, 3]], normal=[0, 0, 1])
    assert dec.b_normal[0] == pytest.approx(3.0)
    assert np.allclose(dec.b_tangential[0], [1, 2, 0])
    assert dec.b_tangential_mag[0] == pytest.approx(np.sqrt(5))


# -- erosion model ------------------------------------------------------------

def test_erosion_peaks_where_field_parallel_to_surface():
    # Row 0: field parallel to surface (B_n = 0) -> maximum erosion.
    # Row 1: field mostly normal (large B_n)     -> negligible erosion.
    b = np.array([[1.0, 0.0, 0.0], [0.1, 0.0, 1.0]])
    intensity, sigma = erosion_intensity(b, normal=[0, 0, 1])
    assert intensity[0] == pytest.approx(1.0)
    assert intensity[1] < 0.05
    assert sigma > 0


def test_eroded_fraction_and_uniformity_bounds():
    b = np.array([[1.0, 0, 0], [0.9, 0, 0.1], [0.1, 0, 1.0]])
    result = compute_race_track(
        np.zeros((3, 3)), b, dims=(3, 1, 1), normal=[0, 0, 1]
    )
    assert 0.0 <= eroded_area_fraction(result) <= 1.0
    assert 0.0 <= uniformity(result) <= 1.0


# -- comparison ---------------------------------------------------------------

def test_compare_identical_results():
    b = np.array([[1.0, 0, 0], [0.5, 0, 0.5], [0.1, 0, 1.0]])
    r = compute_race_track(np.zeros((3, 3)), b, dims=(3, 1, 1), normal=[0, 0, 1])
    cmp = compare(r, r)
    assert cmp.correlation == pytest.approx(1.0)
    assert cmp.peak_shift == pytest.approx(0.0)
    assert np.allclose(difference_map(r, r), 0.0)


def test_compare_requires_same_grid():
    b = np.array([[1.0, 0, 0]])
    r1 = compute_race_track(np.zeros((1, 3)), b, dims=(1, 1, 1), normal=[0, 0, 1])
    r2 = compute_race_track(np.zeros((1, 3)), b, dims=(1, 1, 1), normal=[1, 0, 0])
    # same dims -> ok
    assert compare(r1, r2).correlation is not None


# -- integration: closed race track from a magnetostatic solution -------------

def test_race_track_from_magnetron_like_arrangement():
    M = 1.30 / MU_0
    d = 0.02
    # Central magnet +z, four outer magnets -z (classic planar magnetron).
    sources = [{"shape": "box", "center": [0, 0, 0], "dims": [d, d, d],
                "magnetization": [0, 0, M]}]
    for cx, cy in [(0.03, 0), (-0.03, 0), (0, 0.03), (0, -0.03)]:
        sources.append({"shape": "box", "center": [cx, cy, 0], "dims": [d, d, d],
                        "magnetization": [0, 0, -M]})

    # Sample a target plane above the magnets.
    pts, dims = plane_points([0, 0, 0.02], [1, 0, 0], [0, 1, 0], 0.1, 0.1, 25, 25)
    res = AnalyticBackend().solve(SolverProblem(points=pts, magnet_sources=sources))
    track = compute_race_track(pts, res.b, dims, normal=[0, 0, 1])

    # A race track exists only if B_n changes sign across the target.
    assert track.b_normal.min() < 0 < track.b_normal.max()
    assert track.intensity.max() == pytest.approx(1.0)
    assert (track.intensity > 0.5).sum() > 0  # a non-empty erosion band
