"""Tests for results post-processing: statistics, expressions, cut line."""

import numpy as np
import pytest

from magnetflux.config import MU_0
from magnetflux.results.expressions import evaluate_expression
from magnetflux.results.probes import cut_line
from magnetflux.results.statistics import field_statistics, volume_integral
from magnetflux.solver.analytic import AnalyticBackend
from magnetflux.solver.base import SolverProblem
from magnetflux.visualization.sampling import StructuredField, grid_points
from magnetflux.core.geometry import BoundingBox


# -- statistics ---------------------------------------------------------------

def test_field_statistics():
    s = field_statistics([1.0, 2.0, 3.0])
    assert s.minimum == 1.0 and s.maximum == 3.0
    assert s.mean == pytest.approx(2.0)
    assert s.rms == pytest.approx(np.sqrt((1 + 4 + 9) / 3))
    assert set(s.as_dict()) == {"min", "max", "mean", "rms", "std"}


def test_volume_integral():
    assert volume_integral([1.0, 2.0, 3.0], cell_volume=2.0) == pytest.approx(12.0)


# -- custom expressions -------------------------------------------------------

def test_expression_bmag_matches_norm():
    vars_ = {"Bx": np.array([3.0]), "By": np.array([4.0]), "Bz": np.array([0.0])}
    out = evaluate_expression("sqrt(Bx^2 + By^2 + Bz^2)", vars_)
    assert out[0] == pytest.approx(5.0)


def test_expression_uses_constants():
    out = evaluate_expression("Bz / mu0", {"Bz": np.array([MU_0])})
    assert out[0] == pytest.approx(1.0)


def test_expression_rejects_unknown_variable():
    with pytest.raises(ValueError):
        evaluate_expression("Bx + Qq", {"Bx": np.array([1.0])})


def test_expression_rejects_malicious_code():
    with pytest.raises(ValueError):
        evaluate_expression("__import__('os').system('echo hi')", {})
    with pytest.raises(ValueError):
        evaluate_expression("Bx.__class__", {"Bx": np.array([1.0])})


# -- cut line -----------------------------------------------------------------

def _field_on(bb: BoundingBox) -> StructuredField:
    src = {"shape": "box", "center": [0, 0, 0], "dims": [0.01, 0.01, 0.01],
           "magnetization": [0, 0, 1.0 / MU_0]}
    pts, dims = grid_points(bb, 8, 8, 8)
    res = AnalyticBackend().solve(SolverProblem(points=pts, magnet_sources=[src]))
    return StructuredField(pts, res, dims)


def test_cut_line_endpoints_and_decay():
    bb = BoundingBox([-0.03, -0.03, 0.02], [0.03, 0.03, 0.06])
    field = _field_on(bb)
    line = cut_line(field, p0=[0, 0, 0.02], p1=[0, 0, 0.06], n=20)
    assert line.points.shape == (20, 3)
    assert line.arc_length[0] == pytest.approx(0.0)
    assert line.arc_length[-1] == pytest.approx(0.04, rel=1e-6)
    # Field weakens with height above the magnet.
    assert line.b_magnitude[0] > line.b_magnitude[-1]
