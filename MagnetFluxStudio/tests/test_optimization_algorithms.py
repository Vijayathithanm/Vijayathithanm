"""Tests for the global optimizers, design space, objectives and runner."""

import numpy as np
import pytest

from magnetflux.optimization.algorithms import (
    bayesian_optimization,
    genetic_algorithm,
    particle_swarm,
)
from magnetflux.optimization.design_objectives import (
    Objective,
    magnet_weight,
    objective_value,
)
from magnetflux.optimization.design_space import DesignSpace, DesignVariable
from magnetflux.optimization.layout import ParametricLayout
from magnetflux.optimization.objectives import evaluate_layout
from magnetflux.optimization.runner import optimize_design


def _quadratic(x: np.ndarray) -> float:
    # Maximum (0) at x = 0.5 in every dimension.
    return -float(np.sum((np.asarray(x) - 0.5) ** 2))


@pytest.mark.parametrize("optimizer", [genetic_algorithm, particle_swarm])
def test_evolutionary_optimizers_find_optimum(optimizer):
    out = optimizer(_quadratic, n_vars=2, seed=1)
    assert out.best_value > -0.02          # close to the maximum of 0
    assert np.allclose(out.best_x, 0.5, atol=0.15)
    assert out.history[-1] >= out.history[0]  # monotonic best-so-far


def test_bayesian_optimizer_improves():
    out = bayesian_optimization(_quadratic, n_vars=2, n_init=6, iterations=20, seed=1)
    assert out.best_value > -0.05
    assert out.history[-1] >= out.history[0]


# -- design space -------------------------------------------------------------

def test_design_variable_decode_bounds():
    var = DesignVariable("ring_radius", 0.03, 0.07)
    assert var.decode(0.0) == pytest.approx(0.03)
    assert var.decode(1.0) == pytest.approx(0.07)
    assert var.decode(0.5) == pytest.approx(0.05)


def test_design_variable_validation():
    with pytest.raises(ValueError):
        DesignVariable("bogus", 0, 1)
    with pytest.raises(ValueError):
        DesignVariable("ring_radius", 1.0, 1.0)


def test_design_space_make_layout():
    space = DesignSpace([DesignVariable("ring_radius", 0.03, 0.07)])
    layout = space.make_layout(ParametricLayout(), np.array([1.0]))
    assert layout.ring_radius == pytest.approx(0.07)


# -- objectives ---------------------------------------------------------------

def test_objective_value_min_weight_is_negative_weight():
    layout = ParametricLayout()
    val = objective_value(Objective.MIN_WEIGHT, layout, evaluate_layout(layout, resolution=20))
    assert val == pytest.approx(-magnet_weight(layout))


def test_magnet_weight_scales_with_count():
    small = ParametricLayout(ring_count=4)
    big = ParametricLayout(ring_count=8)
    assert magnet_weight(big) > magnet_weight(small)


# -- runner -------------------------------------------------------------------

def test_optimize_design_runs_and_bounds_result():
    space = DesignSpace([DesignVariable("ring_radius", 0.03, 0.07)])
    result = optimize_design(
        ParametricLayout(ring_count=6), space, Objective.MAX_UTILIZATION,
        algorithm="ga", resolution=20, pop_size=8, generations=4,
    )
    assert 0.03 <= result.best_layout.ring_radius <= 0.07
    assert result.algorithm == "ga"
    assert len(result.history) > 0
