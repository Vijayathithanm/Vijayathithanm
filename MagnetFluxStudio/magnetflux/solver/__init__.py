"""Magnetostatic solver layer.

Defines the backend-agnostic solver interfaces (:mod:`magnetflux.solver.base`)
so the rest of the application depends on abstractions, not a concrete FEM
library. Concrete backends (analytic superposition, scikit-fem A-formulation)
are added in Milestone 3.
"""

from magnetflux.solver.base import (
    FieldResult,
    SolverBackend,
    SolverProblem,
)

__all__ = ["FieldResult", "SolverBackend", "SolverProblem"]
