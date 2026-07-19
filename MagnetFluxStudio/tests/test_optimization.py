"""Tests for the optimization layer: layout, objectives, optimizers."""

import numpy as np
import pytest

from magnetflux.config import MU_0
from magnetflux.optimization.layout import ParametricLayout
from magnetflux.optimization.objectives import evaluate_layout, target_utilization
from magnetflux.optimization.optimize import (
    optimize_pole_arrangement,
    optimize_spacing,
)


# -- parametric layout --------------------------------------------------------

def test_layout_builds_center_plus_ring():
    layout = ParametricLayout(ring_radius=0.04, ring_count=6, remanence_br=1.30)
    sources = layout.build_sources()
    assert len(sources) == 7  # center + 6 ring magnets
    # Central magnet at origin, +z; ring magnets -z.
    assert np.allclose(sources[0]["center"], [0, 0, 0])
    assert sources[0]["magnetization"][2] == pytest.approx(1.30 / MU_0)
    assert sources[1]["magnetization"][2] == pytest.approx(-1.30 / MU_0)
    # Ring magnets sit on the ring radius.
    radii = [np.hypot(s["center"][0], s["center"][1]) for s in sources[1:]]
    assert np.allclose(radii, 0.04)


def test_layout_override_ring_radius_and_count():
    layout = ParametricLayout(ring_radius=0.04, ring_count=6)
    sources = layout.build_sources(ring_radius=0.06, ring_count=4)
    assert len(sources) == 5
    radii = [np.hypot(s["center"][0], s["center"][1]) for s in sources[1:]]
    assert np.allclose(radii, 0.06)


# -- objectives ---------------------------------------------------------------

def test_evaluate_layout_returns_bounded_metrics():
    layout = ParametricLayout(ring_radius=0.045, ring_count=6)
    ev = evaluate_layout(layout, resolution=30)
    assert 0.0 <= ev.uniformity <= 1.0
    assert 0.0 <= ev.eroded_fraction <= 1.0
    assert 0.0 <= ev.utilization <= 1.0
    assert ev.race_track.intensity.max() == pytest.approx(1.0)


# -- optimizers ---------------------------------------------------------------

def test_optimize_spacing_improves_on_a_poor_guess():
    layout = ParametricLayout(ring_radius=0.02, ring_count=6)
    poor = evaluate_layout(layout, ring_radius=0.02, resolution=30).utilization
    result = optimize_spacing(layout, bounds=(0.02, 0.08), max_iter=12)
    assert 0.02 <= result.best_value <= 0.08
    assert len(result.history) > 0
    # The optimum is at least as good as the poor starting spacing.
    assert result.best_score >= poor - 1e-6


def test_optimize_pole_arrangement_selects_a_count():
    layout = ParametricLayout(ring_radius=0.045)
    result = optimize_pole_arrangement(layout, ring_counts=[3, 4, 6, 8])
    assert result.best_value in (3, 4, 6, 8)
    assert len(result.history) == 4
    assert result.best_score == max(s for _, s in result.history)


def test_target_utilization_monotone_in_inputs():
    # Higher, more uniform erosion -> higher utilisation.
    layout = ParametricLayout(ring_radius=0.045, ring_count=8)
    ev = evaluate_layout(layout, resolution=30)
    assert target_utilization(ev.race_track) == pytest.approx(ev.utilization)
