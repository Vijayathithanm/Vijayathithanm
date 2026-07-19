"""Solver orchestration service (Milestone 3).

Selects a backend, builds the :class:`SolverProblem` from the project's model
tree and material assignments, and runs the solve. Keeps backend choice and
problem assembly out of both the GUI and the individual backends.
"""

from __future__ import annotations

from enum import Enum

import numpy as np

from magnetflux.core.model_tree import ModelTree
from magnetflux.materials.database import AssignmentTable, MaterialDatabase
from magnetflux.solver.analytic import AnalyticBackend
from magnetflux.solver.base import FieldResult, SolverBackend, SolverProblem
from magnetflux.solver.fem import ScikitFemBackend, is_skfem_available
from magnetflux.solver.sources import build_magnet_sources


class BackendKind(str, Enum):
    ANALYTIC = "analytic"
    FEM = "fem"
    AUTO = "auto"


def select_backend(kind: BackendKind = BackendKind.AUTO) -> SolverBackend:
    """Return a solver backend instance for ``kind``.

    ``AUTO`` prefers the FEM backend when scikit-fem is available (it captures
    soft-iron effects), otherwise falls back to the analytic backend.
    """
    if kind is BackendKind.ANALYTIC:
        return AnalyticBackend()
    if kind is BackendKind.FEM:
        return ScikitFemBackend()
    return ScikitFemBackend() if is_skfem_available() else AnalyticBackend()


class SolverService:
    """Builds and runs magnetostatic problems from project data."""

    def __init__(self, backend: SolverBackend | None = None) -> None:
        self._backend = backend or select_backend()

    @property
    def backend(self) -> SolverBackend:
        return self._backend

    def build_problem(
        self,
        tree: ModelTree,
        db: MaterialDatabase,
        assignments: AssignmentTable,
        points: np.ndarray,
        *,
        air_padding: float = 2.0,
        mesh_size: float = 2.0e-3,
    ) -> SolverProblem:
        """Assemble a :class:`SolverProblem` from project data + eval points."""
        sources = build_magnet_sources(tree, db, assignments)
        return SolverProblem(
            points=points,
            magnet_sources=sources,
            air_padding=air_padding,
            mesh_size=mesh_size,
        )

    def solve(self, problem: SolverProblem, progress=None) -> FieldResult:
        """Run the configured backend on ``problem``."""
        return self._backend.solve(problem, progress=progress)
