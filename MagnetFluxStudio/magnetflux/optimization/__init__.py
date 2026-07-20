"""Optimization layer: parametric layout, objectives, and global optimizers."""

from magnetflux.optimization.algorithms import (
    OPTIMIZERS,
    OptimizeOutcome,
    bayesian_optimization,
    genetic_algorithm,
    particle_swarm,
)
from magnetflux.optimization.design_objectives import (
    Objective,
    magnet_cost,
    magnet_weight,
    objective_value,
)
from magnetflux.optimization.design_space import DesignSpace, DesignVariable
from magnetflux.optimization.layout import ParametricLayout
from magnetflux.optimization.objectives import (
    LayoutEvaluation,
    evaluate_layout,
    target_utilization,
)
from magnetflux.optimization.optimize import (
    OptimizationResult,
    optimize_pole_arrangement,
    optimize_spacing,
)
from magnetflux.optimization.runner import (
    DesignOptimizationResult,
    optimize_design,
)

__all__ = [
    "ParametricLayout",
    "evaluate_layout",
    "LayoutEvaluation",
    "target_utilization",
    "optimize_spacing",
    "optimize_pole_arrangement",
    "OptimizationResult",
    # global optimizers
    "genetic_algorithm",
    "particle_swarm",
    "bayesian_optimization",
    "OPTIMIZERS",
    "OptimizeOutcome",
    # design optimization
    "DesignSpace",
    "DesignVariable",
    "Objective",
    "objective_value",
    "magnet_weight",
    "magnet_cost",
    "optimize_design",
    "DesignOptimizationResult",
]
