"""Design-optimization runner (Milestone: Optimization).

Ties a :class:`DesignSpace`, a named :class:`Objective` and a global optimizer
(GA / PSO / Bayesian) together: it maximises the objective over the design
space and returns the best layout found.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from magnetflux.optimization.algorithms import OPTIMIZERS, OptimizeOutcome
from magnetflux.optimization.design_objectives import Objective, objective_value
from magnetflux.optimization.design_space import DesignSpace
from magnetflux.optimization.layout import ParametricLayout
from magnetflux.optimization.objectives import evaluate_layout


@dataclass(slots=True)
class DesignOptimizationResult:
    """Outcome of a design optimization."""

    best_layout: ParametricLayout
    best_value: float
    best_parameters: dict[str, float]
    history: list[float]
    algorithm: str


def optimize_design(
    base_layout: ParametricLayout,
    space: DesignSpace,
    objective: Objective,
    algorithm: str = "ga",
    resolution: int = 24,
    **algo_kwargs,
) -> DesignOptimizationResult:
    """Maximise ``objective`` over ``space`` using ``algorithm`` (ga/pso/bayesian)."""
    if algorithm not in OPTIMIZERS:
        raise ValueError(f"unknown algorithm '{algorithm}'; valid: {list(OPTIMIZERS)}")

    def fitness(x: np.ndarray) -> float:
        layout = space.make_layout(base_layout, x)
        ev = evaluate_layout(layout, resolution=resolution)
        return objective_value(objective, layout, ev)

    outcome: OptimizeOutcome = OPTIMIZERS[algorithm](fitness, space.n_vars, **algo_kwargs)
    best_params = space.decode(outcome.best_x)
    return DesignOptimizationResult(
        best_layout=space.make_layout(base_layout, outcome.best_x),
        best_value=outcome.best_value,
        best_parameters=best_params,
        history=outcome.history,
        algorithm=algorithm,
    )
