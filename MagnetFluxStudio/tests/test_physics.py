"""Tests for the physics layer: coils (Biot-Savart) and boundary conditions."""

import numpy as np
import pytest

from magnetflux.config import MU_0
from magnetflux.physics.boundary import (
    BoundaryCondition,
    PhysicsSettings,
    mirror_magnet_sources,
)
from magnetflux.physics.coil import CoilSource, circular_loop_field, loop_axial_field
from magnetflux.solver.analytic import AnalyticBackend
from magnetflux.solver.base import SolverProblem


# -- coil Biot-Savart ---------------------------------------------------------

def test_loop_field_matches_closed_form_on_axis():
    R, I = 0.05, 100.0
    z = np.array([0.0, 0.02, 0.05, 0.1])
    pts = np.column_stack([np.zeros_like(z), np.zeros_like(z), z])
    b = circular_loop_field(pts, [0, 0, 0], [0, 0, 1], R, I, segments=240)
    exact = loop_axial_field(z, R, I)
    assert np.allclose(b[:, 2], exact, rtol=1e-3)
    assert np.allclose(b[:, :2], 0.0, atol=1e-9)  # transverse vanishes on axis


def test_loop_center_field():
    R, I = 0.05, 100.0
    b = circular_loop_field([[0, 0, 0]], [0, 0, 0], [0, 0, 1], R, I)
    # At the centre, Bz = mu0 I / (2R).
    assert b[0, 2] == pytest.approx(MU_0 * I / (2 * R), rel=1e-3)


def test_solenoid_stronger_than_single_loop_at_center():
    loop = CoilSource(radius=0.05, current=100.0, turns=1)
    solenoid = CoilSource(radius=0.05, current=100.0, turns=20, length=0.1)
    b_loop = loop.field([[0, 0, 0]])[0, 2]
    b_sol = solenoid.field([[0, 0, 0]])[0, 2]
    assert b_sol > b_loop


def test_coil_integrated_into_solver_problem():
    coil = CoilSource(radius=0.05, current=100.0)
    prob = SolverProblem(points=[[0, 0, 0]], magnet_sources=[], coils=[coil])
    res = AnalyticBackend().solve(prob)
    assert res.metadata["n_coils"] == 1
    assert res.bz[0] == pytest.approx(MU_0 * 100.0 / (2 * 0.05), rel=1e-3)


# -- boundary conditions ------------------------------------------------------

def test_physics_settings_roundtrip():
    s = PhysicsSettings(outer_boundary=BoundaryCondition.SYMMETRY,
                        symmetry_plane_normal=(1, 0, 0))
    s2 = PhysicsSettings.from_dict(s.to_dict())
    assert s2.outer_boundary is BoundaryCondition.SYMMETRY
    assert s2.symmetry_plane_normal == (1, 0, 0)


def test_mirror_sources_reflect_position():
    src = {"shape": "box", "center": [0, 0, 0.05], "dims": [0.01, 0.01, 0.01],
           "magnetization": [0, 0, 1.0]}
    images = mirror_magnet_sources([src], plane_point=[0, 0, 0], plane_normal=[0, 0, 1])
    assert len(images) == 1
    # Position reflects to z = -0.05.
    assert np.allclose(images[0]["center"], [0, 0, -0.05])


def test_symmetry_plane_makes_field_symmetric():
    # A magnet plus its mirror image gives a field symmetric about the plane.
    M = 1.0 / MU_0
    src = {"shape": "box", "center": [0, 0, 0.03], "dims": [0.01, 0.01, 0.01],
           "magnetization": [0, 0, M]}
    images = mirror_magnet_sources([src], [0, 0, 0], [0, 0, 1])
    backend = AnalyticBackend()
    above = backend.solve(SolverProblem(points=[[0.02, 0, 0.05]],
                                        magnet_sources=[src, *images]))
    below = backend.solve(SolverProblem(points=[[0.02, 0, -0.05]],
                                        magnet_sources=[src, *images]))
    # |B| is mirror-symmetric across the plane.
    assert above.b_magnitude[0] == pytest.approx(below.b_magnitude[0], rel=1e-6)
