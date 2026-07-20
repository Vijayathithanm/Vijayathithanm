"""Tests for component-name handling on assembly import + CSV B-H import."""

import numpy as np
import pytest

from magnetflux.cad.gmsh_import import _clean_component_name, is_gmsh_available
from magnetflux.cad.importer import import_cad_named
from magnetflux.cad.stl import write_binary_stl
from magnetflux.core.geometry import TriangleMesh
from magnetflux.materials.material import BHCurve


def _tri() -> TriangleMesh:
    return TriangleMesh(
        np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float),
        np.array([[0, 1, 2]]),
    )


def test_clean_component_name():
    assert _clean_component_name("Bracket") == "Bracket"
    assert _clean_component_name("Assembly/Inner Magnet") == "Inner Magnet"
    assert _clean_component_name("Asm\\Pole Plate") == "Pole Plate"
    assert _clean_component_name("") is None
    assert _clean_component_name("   ") is None


def test_import_cad_named_stl_has_no_component_name(tmp_path):
    path = write_binary_stl(tmp_path / "part.stl", _tri())
    named = import_cad_named(path)
    assert len(named) == 1
    name, mesh = named[0]
    assert name is None                       # STL carries no component name
    assert mesh.n_faces == 1


@pytest.mark.skipif(not is_gmsh_available(), reason="gmsh not importable")
def test_import_cad_named_step_returns_pairs(tmp_path):
    import gmsh

    step = tmp_path / "asm.step"
    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add("asm")
        gmsh.model.occ.addBox(0, 0, 0, 10, 10, 10)
        gmsh.model.occ.addBox(20, 0, 0, 10, 10, 10)
        gmsh.model.occ.synchronize()
        gmsh.write(str(step))
    finally:
        gmsh.finalize()

    named = import_cad_named(step)
    assert len(named) == 2  # two solids -> two components
    for name, mesh in named:
        assert name is None or isinstance(name, str)
        assert mesh.n_faces > 0


def test_bh_curve_from_csv(tmp_path):
    csv = tmp_path / "bh.csv"
    csv.write_text("H,B\n0,0\n100,0.2\n400,1.0\n3000,1.5\n")
    curve = BHCurve.from_csv(csv)
    assert curve.b[0] == 0.0 and curve.h[0] == 0.0
    assert curve.b[-1] == pytest.approx(1.5)
    # Reluctivity rises as it saturates.
    assert curve.reluctivity(1.5) > curve.reluctivity(0.2)
