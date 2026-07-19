"""Optimization layer: parametric layout, objectives, spacing/pole optimizers."""

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

__all__ = [
    "ParametricLayout",
    "evaluate_layout",
    "LayoutEvaluation",
    "target_utilization",
    "optimize_spacing",
    "optimize_pole_arrangement",
    "OptimizationResult",
]
