"""Tests for the Gmsh-based STEP/IGES importer (skipped if Gmsh unavailable)."""

import numpy as np
import pytest

from magnetflux.cad.gmsh_import import is_gmsh_available, read_cad_gmsh
from magnetflux.cad.importer import import_cad
from magnetflux.core.units import LengthUnit

pytestmark = pytest.mark.skipif(
    not is_gmsh_available(), reason="gmsh not importable in this environment"
)


def _make_step_box(path, lx=10.0, ly=20.0, lz=30.0):
    """Write a STEP box (mm) using Gmsh, for round-trip import testing."""
    import gmsh

    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add("box")
        gmsh.model.occ.addBox(0, 0, 0, lx, ly, lz)
        gmsh.model.occ.synchronize()
        gmsh.write(str(path))
    finally:
        gmsh.finalize()


def test_gmsh_reads_step_box(tmp_path):
    step = tmp_path / "box.step"
    _make_step_box(step)
    meshes = read_cad_gmsh(step)
    assert len(meshes) == 1
    bb = meshes[0].bounding_box()
    # Box is 10x20x30 mm in native units (import_cad applies unit scaling).
    assert np.allclose(bb.size, [10, 20, 30], atol=0.5)
    assert meshes[0].n_faces > 0


def test_import_cad_step_scales_to_meters(tmp_path):
    step = tmp_path / "box.step"
    _make_step_box(step)
    meshes = import_cad(step, source_unit=LengthUnit.MILLIMETER)
    assert len(meshes) == 1
    bb = meshes[0].bounding_box()
    # 10x20x30 mm -> metres.
    assert np.allclose(bb.size, [0.010, 0.020, 0.030], atol=5e-4)
