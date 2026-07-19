"""Magnetostatic solver layer.

Defines the backend-agnostic solver interfaces (:mod:`magnetflux.solver.base`)
so the rest of the application depends on abstractions, not a concrete FEM
library. Concrete backends (analytic superposition, scikit-fem A-formulation)
are added in Milestone 3.
"""

from magnetflux.solver.air_domain import generate_air_domain
from magnetflux.solver.analytic import (
    AnalyticBackend,
    closed_form_cylinder_axial_bz,
)
from magnetflux.solver.base import (
    FieldResult,
    SolverBackend,
    SolverProblem,
)
from magnetflux.solver.fem import ScikitFemBackend, is_skfem_available
from magnetflux.solver.service import BackendKind, SolverService, select_backend
from magnetflux.solver.sources import build_magnet_sources

__all__ = [
    "FieldResult",
    "SolverBackend",
    "SolverProblem",
    "AnalyticBackend",
    "ScikitFemBackend",
    "is_skfem_available",
    "closed_form_cylinder_axial_bz",
    "generate_air_domain",
    "build_magnet_sources",
    "SolverService",
    "BackendKind",
    "select_backend",
]
