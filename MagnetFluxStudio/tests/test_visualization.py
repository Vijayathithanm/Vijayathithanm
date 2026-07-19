"""Tests for the visualization core: quantities, sampling, probe, export."""

import numpy as np
import pytest

from magnetflux.config import MU_0
from magnetflux.core.geometry import BoundingBox
from magnetflux.solver.analytic import AnalyticBackend
from magnetflux.solver.base import FieldResult, SolverProblem
from magnetflux.visualization.export import export_csv, export_vtk
from magnetflux.visualization.probe import GridProbe, SolverProbe
from magnetflux.visualization.quantities import (
    FieldQuantity,
    available_quantities,
    scalar_values,
)
from magnetflux.visualization.sampling import (
    StructuredField,
    grid_points,
    line_points,
    plane_points,
)

_SRC = {"shape": "box", "center": [0, 0, 0], "dims": [0.01, 0.01, 0.01],
        "magnetization": [0, 0, 1.0 / MU_0]}


def _result_on(points):
    return AnalyticBackend().solve(SolverProblem(points=points, magnet_sources=[_SRC]))


# -- quantities ---------------------------------------------------------------

def test_scalar_values_and_units():
    res = FieldResult(np.array([[0, 0, 0.03]]), np.array([[3.0, 0.0, 4.0]]))
    assert scalar_values(res, FieldQuantity.BMAG)[0] == pytest.approx(5.0)
    assert scalar_values(res, FieldQuantity.BZ)[0] == pytest.approx(4.0)
    assert FieldQuantity.BMAG.unit == "T"
    assert FieldQuantity.HMAG.unit == "A/m"
    assert len(available_quantities()) == 6


# -- sampling -----------------------------------------------------------------

def test_grid_points_dims_and_count():
    bb = BoundingBox([0, 0, 0], [1, 1, 1])
    pts, dims = grid_points(bb, 3, 4, 5)
    assert dims == (3, 4, 5)
    assert pts.shape == (60, 3)


def test_plane_points_lie_on_plane():
    pts, dims = plane_points([0, 0, 0.01], [1, 0, 0], [0, 1, 0], 0.02, 0.02, 5, 5)
    assert dims == (5, 5, 1)
    assert np.allclose(pts[:, 2], 0.01)  # plane at z = 0.01


def test_line_points_endpoints():
    pts = line_points([0, 0, 0], [0, 0, 0.1], 11)
    assert pts.shape == (11, 3)
    assert np.allclose(pts[0], [0, 0, 0])
    assert np.allclose(pts[-1], [0, 0, 0.1])


# -- probe --------------------------------------------------------------------

def test_solver_probe_matches_direct_solve():
    probe = SolverProbe(AnalyticBackend(), [_SRC])
    b = probe.at([0, 0, 0.03])
    ref = _result_on(np.array([[0, 0, 0.03]])).b[0]
    assert np.allclose(b, ref)


def test_grid_probe_interpolates():
    bb = BoundingBox([-0.03, -0.03, 0.02], [0.03, 0.03, 0.05])
    pts, dims = grid_points(bb, 6, 6, 6)
    field = StructuredField(pts, _result_on(pts), dims)
    probe = GridProbe(field, bb.min_corner, bb.max_corner)
    # At a grid node the interpolant reproduces the sampled value.
    node = pts[0]
    assert np.allclose(probe.at(node)[0], field.result.b[0], rtol=1e-6)


# -- export -------------------------------------------------------------------

def test_export_csv(tmp_path):
    res = _result_on(np.array([[0, 0, 0.03], [0, 0, 0.04]]))
    path = export_csv(tmp_path / "field.csv", res)
    text = path.read_text().splitlines()
    assert text[0] == "x,y,z,Bx,By,Bz,|B|"
    assert len(text) == 3  # header + 2 rows


def test_export_vtk_structured(tmp_path):
    bb = BoundingBox([-0.02, -0.02, 0.02], [0.02, 0.02, 0.05])
    pts, dims = grid_points(bb, 4, 4, 4)
    res = _result_on(pts)
    path = export_vtk(tmp_path / "field.vtk", res, dims=dims)
    text = path.read_text()
    assert "DATASET STRUCTURED_GRID" in text
    assert "DIMENSIONS 4 4 4" in text
    assert "VECTORS B float" in text
    assert "POINTS 64 float" in text


def test_export_vtk_polydata_point_cloud(tmp_path):
    res = _result_on(np.array([[0, 0, 0.03], [0, 0, 0.04], [0, 0, 0.05]]))
    path = export_vtk(tmp_path / "cloud.vtk", res)
    text = path.read_text()
    assert "DATASET POLYDATA" in text
    assert "VERTICES 3 6" in text
