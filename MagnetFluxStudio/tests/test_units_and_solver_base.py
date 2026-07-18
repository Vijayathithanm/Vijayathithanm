"""Tests for unit conversions and the solver-base data structures."""

import numpy as np
import pytest

from magnetflux.config import MU_0
from magnetflux.core.units import LengthUnit, from_meters, gauss_to_tesla, to_meters
from magnetflux.solver.base import FieldResult, SolverProblem


def test_length_unit_conversions():
    assert to_meters(1000.0, LengthUnit.MILLIMETER) == pytest.approx(1.0)
    assert to_meters(1.0, LengthUnit.INCH) == pytest.approx(0.0254)
    assert from_meters(1.0, LengthUnit.MILLIMETER) == pytest.approx(1000.0)
    arr = to_meters(np.array([1.0, 2.0]), LengthUnit.CENTIMETER)
    assert np.allclose(arr, [0.01, 0.02])


def test_gauss_to_tesla():
    assert gauss_to_tesla(10000.0) == pytest.approx(1.0)


def test_field_result_derived_quantities():
    pts = np.array([[0, 0, 0], [1, 0, 0]], dtype=float)
    b = np.array([[0.0, 0.0, 1.0], [3.0, 4.0, 0.0]])
    res = FieldResult(pts, b)
    assert np.allclose(res.b_magnitude, [1.0, 5.0])
    assert np.allclose(res.bz, [1.0, 0.0])
    assert np.allclose(res.h, b / MU_0)
    assert res.energy_density()[0] == pytest.approx(1.0 / (2 * MU_0))


def test_field_result_length_mismatch():
    with pytest.raises(ValueError):
        FieldResult(np.zeros((2, 3)), np.zeros((3, 3)))


def test_solver_problem_reshapes_points():
    prob = SolverProblem(points=[0, 0, 0, 1, 1, 1])
    assert prob.points.shape == (2, 3)
