"""Tests for the solver orchestration service and backend selection."""

import numpy as np
import pytest

from magnetflux.config import MU_0
from magnetflux.core.geometry import TriangleMesh
from magnetflux.core.model_tree import ModelTree
from magnetflux.materials.database import AssignmentTable, MaterialDatabase
from magnetflux.materials.magnetization import MagnetizationMode, MagnetizationSpec
from magnetflux.solver.analytic import AnalyticBackend
from magnetflux.solver.service import BackendKind, SolverService, select_backend


def test_select_backend_kinds():
    assert select_backend(BackendKind.ANALYTIC).name == "analytic-charge"


def _magnet_project():
    tree = ModelTree()
    mesh = TriangleMesh(
        np.array([[-0.01, -0.01, -0.01], [0.01, 0.01, 0.01], [0.01, -0.01, 0.0]]),
        np.array([[0, 1, 2]]),
    )
    body = tree.add_body(mesh)
    db = MaterialDatabase()
    table = AssignmentTable()
    table.assign(body.id, "N42",
                 MagnetizationSpec(mode=MagnetizationMode.AXIAL, axis=(0, 0, 1)))
    return tree, db, table


def test_service_build_and_solve_analytic():
    tree, db, table = _magnet_project()
    service = SolverService(backend=AnalyticBackend())
    points = np.array([[0, 0, 0.05]])
    problem = service.build_problem(tree, db, table, points)
    assert len(problem.magnet_sources) == 1
    result = service.solve(problem)
    assert result.bz[0] > 0
    assert result.b_magnitude[0] > 0
