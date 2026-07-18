"""Tests for STL reading/writing and the CAD import dispatcher."""

import numpy as np
import pytest

from magnetflux.cad.importer import UnsupportedFormatError, import_cad
from magnetflux.cad.stl import read_stl, write_binary_stl
from magnetflux.core.geometry import TriangleMesh
from magnetflux.core.units import LengthUnit


def _tetra() -> TriangleMesh:
    v = np.array(
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float
    )
    f = np.array([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]])
    return TriangleMesh(v, f)


ASCII_STL = """solid tri
facet normal 0 0 1
 outer loop
  vertex 0 0 0
  vertex 1 0 0
  vertex 0 1 0
 endloop
endfacet
endsolid tri
"""


def test_binary_stl_roundtrip(tmp_path):
    mesh = _tetra()
    path = write_binary_stl(tmp_path / "t.stl", mesh)
    loaded = read_stl(path)
    assert loaded.n_faces == 4
    assert loaded.n_vertices == 4  # dedup collapses shared corners
    assert loaded.surface_area() == pytest.approx(mesh.surface_area(), rel=1e-5)


def test_ascii_stl_read(tmp_path):
    path = tmp_path / "a.stl"
    path.write_text(ASCII_STL)
    mesh = read_stl(path)
    assert mesh.n_faces == 1
    assert mesh.n_vertices == 3
    assert mesh.surface_area() == pytest.approx(0.5)


def test_import_cad_scales_mm_to_m(tmp_path):
    # A 1000 mm triangle should become 1 m after import.
    mesh = TriangleMesh(
        np.array([[0, 0, 0], [1000, 0, 0], [0, 1000, 0]], dtype=float),
        np.array([[0, 1, 2]]),
    )
    path = write_binary_stl(tmp_path / "big.stl", mesh)
    meshes = import_cad(path, source_unit=LengthUnit.MILLIMETER)
    assert len(meshes) == 1
    bb = meshes[0].bounding_box()
    assert np.allclose(bb.size, [1.0, 1.0, 0.0], atol=1e-6)


def test_import_cad_meter_unit_no_scaling(tmp_path):
    path = write_binary_stl(tmp_path / "m.stl", _tetra())
    meshes = import_cad(path, source_unit=LengthUnit.METER)
    assert meshes[0].surface_area() == pytest.approx(_tetra().surface_area())


def test_import_cad_unsupported_extension(tmp_path):
    p = tmp_path / "model.xyz"
    p.write_text("nope")
    with pytest.raises(UnsupportedFormatError):
        import_cad(p)


def test_import_cad_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        import_cad(tmp_path / "absent.stl")
