"""Tests for the magnetostatic solver: air domain, analytic + FEM backends.

The analytic backend is validated tightly against the closed-form on-axis field
of a uniformly magnetised cylinder. The scikit-fem A-formulation backend is
validated against the analytic backend to first-order (P1) accuracy.
"""

import numpy as np
import pytest

from magnetflux.config import MU_0
from magnetflux.core.geometry import BoundingBox
from magnetflux.core.model_tree import ModelTree
from magnetflux.core.geometry import TriangleMesh
from magnetflux.materials.database import AssignmentTable, MaterialDatabase
from magnetflux.materials.magnetization import MagnetizationMode, MagnetizationSpec
from magnetflux.solver.air_domain import generate_air_domain
from magnetflux.solver.analytic import (
    AnalyticBackend,
    closed_form_cylinder_axial_bz,
)
from magnetflux.solver.base import SolverProblem
from magnetflux.solver.fem import ScikitFemBackend, is_skfem_available
from magnetflux.solver.sources import build_magnet_sources


# -- air domain ---------------------------------------------------------------

def test_air_domain_padding():
    model = BoundingBox([-1, -1, -1], [1, 1, 1])
    air = generate_air_domain(model, padding=2.0)
    assert np.allclose(air.size, [6, 6, 6])
    assert np.allclose(air.center, model.center)


# -- analytic backend vs closed form ------------------------------------------

def test_analytic_cylinder_matches_closed_form():
    R, L = 0.01, 0.02
    M = 1.30 / MU_0  # N42-class remanence
    z = np.array([0.02, 0.03, 0.05])  # points outside the magnet (z > L/2)
    pts = np.column_stack([np.zeros_like(z), np.zeros_like(z), z])
    src = {"shape": "cylinder", "center": [0, 0, 0], "axis": [0, 0, 1],
           "dims": [R, L], "magnetization": [0, 0, M]}
    res = AnalyticBackend().solve(SolverProblem(points=pts, magnet_sources=[src]))
    exact = closed_form_cylinder_axial_bz(z, R, L, M)
    assert np.allclose(res.bz, exact, rtol=0.01)
    # Transverse components vanish on axis.
    assert np.allclose(res.bx, 0.0, atol=1e-6)
    assert np.allclose(res.by, 0.0, atol=1e-6)


def test_analytic_field_decays_with_distance():
    M = 1.0 / MU_0
    src = {"shape": "box", "center": [0, 0, 0], "dims": [0.01, 0.01, 0.01],
           "magnetization": [0, 0, M]}
    z = np.array([0.02, 0.04, 0.08])
    pts = np.column_stack([np.zeros_like(z), np.zeros_like(z), z])
    res = AnalyticBackend().solve(SolverProblem(points=pts, magnet_sources=[src]))
    b = res.b_magnitude
    assert b[0] > b[1] > b[2]  # monotonic decay
    # Far field of a small magnet is dipole-like (~1/r^3): doubling r ~ /8.
    assert b[1] / b[2] == pytest.approx(8.0, rel=0.3)


def test_field_result_components():
    M = 1.0 / MU_0
    src = {"shape": "box", "center": [0, 0, 0], "dims": [0.01, 0.01, 0.01],
           "magnetization": [0, 0, M]}
    pts = np.array([[0, 0, 0.02]])
    res = AnalyticBackend().solve(SolverProblem(points=pts, magnet_sources=[src]))
    assert res.bz[0] > 0
    assert res.b_magnitude[0] == pytest.approx(abs(res.bz[0]), rel=1e-6)


# -- source bridge ------------------------------------------------------------

def test_build_magnet_sources_from_model():
    tree = ModelTree()
    mesh = TriangleMesh(
        np.array([[-0.01, -0.01, -0.01], [0.01, 0.01, 0.01], [0.01, -0.01, 0.0]]),
        np.array([[0, 1, 2]]),
    )
    body = tree.add_body(mesh, name="Magnet")
    db = MaterialDatabase()
    table = AssignmentTable()
    table.assign(body.id, "N42",
                 MagnetizationSpec(mode=MagnetizationMode.AXIAL, axis=(0, 0, 1)))
    sources = build_magnet_sources(tree, db, table)
    assert len(sources) == 1
    m = sources[0]["magnetization"]
    assert np.allclose(m[:2], 0.0)
    assert m[2] == pytest.approx(1.30 / MU_0, rel=1e-6)


def test_build_magnet_sources_skips_non_magnet():
    tree = ModelTree()
    mesh = TriangleMesh(
        np.array([[0, 0, 0], [0.01, 0, 0], [0, 0.01, 0]]), np.array([[0, 1, 2]])
    )
    body = tree.add_body(mesh)
    db = MaterialDatabase()
    table = AssignmentTable()
    table.assign(body.id, "STEEL_1010")  # soft iron, not a magnet source
    assert build_magnet_sources(tree, db, table) == []


# -- FEM backend --------------------------------------------------------------

@pytest.mark.skipif(not is_skfem_available(), reason="scikit-fem not installed")
def test_fem_matches_analytic_first_order():
    Br = 1.30
    M = Br / MU_0
    L = 0.02
    src = {"shape": "box", "center": [0, 0, 0], "dims": [L, L, L],
           "magnetization": [0, 0, M]}
    z = np.array([0.015, 0.02])  # just outside the magnet top face (z > L/2)
    pts = np.column_stack([np.zeros_like(z), np.zeros_like(z), z])
    prob = SolverProblem(points=pts, magnet_sources=[src], air_padding=3.0)

    fem = ScikitFemBackend(resolution=18).solve(prob)
    ana = AnalyticBackend().solve(prob)

    assert fem.metadata["n_dofs"] > 0
    # Correct sign and first-order agreement with the analytic reference.
    assert np.all(fem.bz > 0)
    rel_err = np.abs(fem.bz - ana.bz) / np.abs(ana.bz)
    assert np.all(rel_err < 0.25)


@pytest.mark.skipif(not is_skfem_available(), reason="scikit-fem not installed")
def test_fem_empty_sources_returns_zero_field():
    pts = np.array([[0, 0, 0.02]])
    res = ScikitFemBackend().solve(SolverProblem(points=pts, magnet_sources=[]))
    assert np.allclose(res.b, 0.0)
