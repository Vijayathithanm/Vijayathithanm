"""Tests for the materials layer: grades, B-H curves, magnetization, database."""

import numpy as np
import pytest

from magnetflux.config import MU_0
from magnetflux.materials.database import AssignmentTable, MaterialDatabase
from magnetflux.materials.grades import BUILTIN_MATERIALS, MAGNET_GRADES
from magnetflux.materials.magnetization import MagnetizationMode, MagnetizationSpec
from magnetflux.materials.material import BHCurve, Material, MaterialType


# -- grade library ------------------------------------------------------------

def test_required_grades_present():
    for g in MAGNET_GRADES:
        assert g in BUILTIN_MATERIALS
    assert BUILTIN_MATERIALS["N52"].remanence_br > BUILTIN_MATERIALS["N35"].remanence_br


def test_magnetization_magnitude_matches_br_over_mu0():
    n42 = BUILTIN_MATERIALS["N42"]
    assert n42.magnetization_magnitude() == pytest.approx(1.30 / MU_0)


def test_temperature_reduces_ndfeb_remanence():
    n42 = BUILTIN_MATERIALS["N42"]
    hot = n42.br_at(100.0)
    assert hot < n42.remanence_br
    # -0.12 %/K over 80 K -> ~ -9.6 %
    assert hot == pytest.approx(1.30 * (1 - 0.0012 * 80), rel=1e-6)


# -- B-H curve ----------------------------------------------------------------

def test_bh_curve_reluctivity_and_mu_r():
    steel = BUILTIN_MATERIALS["STEEL_1010"]
    assert steel.is_nonlinear
    nu_low = steel.reluctivity(0.2)
    nu_high = steel.reluctivity(1.9)
    # Reluctivity rises steeply as the steel saturates.
    assert nu_high > nu_low
    assert steel.bh_curve.initial_mu_r() > 100


def test_linear_material_reluctivity():
    air = BUILTIN_MATERIALS["AIR"]
    assert air.reluctivity(0.0) == pytest.approx(1.0 / MU_0)


def test_bh_curve_validation():
    with pytest.raises(ValueError):
        BHCurve([0, 1], [0, 0])  # b not strictly increasing


# -- magnetization direction --------------------------------------------------

def test_uniform_direction():
    spec = MagnetizationSpec(mode=MagnetizationMode.UNIFORM, direction=(0, 0, 2))
    d = spec.direction_at([[1, 2, 3], [4, 5, 6]])
    assert np.allclose(d, [[0, 0, 1], [0, 0, 1]])


def test_axial_direction():
    spec = MagnetizationSpec(mode=MagnetizationMode.AXIAL, axis=(3, 0, 0))
    d = spec.direction_at([[0, 0, 0]])
    assert np.allclose(d, [[1, 0, 0]])


def test_radial_direction_points_outward():
    spec = MagnetizationSpec(
        mode=MagnetizationMode.RADIAL, axis=(0, 0, 1), origin=(0, 0, 0)
    )
    pts = np.array([[1, 0, 0.5], [0, 2, -1]], dtype=float)
    d = spec.direction_at(pts)
    assert np.allclose(d[0], [1, 0, 0])
    assert np.allclose(d[1], [0, 1, 0])
    assert np.allclose(np.linalg.norm(d, axis=1), 1.0)


def test_diametric_is_perpendicular_to_axis():
    spec = MagnetizationSpec(
        mode=MagnetizationMode.DIAMETRIC, axis=(0, 0, 1), direction=(1, 0, 1)
    )
    d = spec.direction_at([[0, 0, 0]])
    assert np.allclose(d, [[1, 0, 0]])


# -- database & assignments ---------------------------------------------------

def test_database_custom_material_roundtrip():
    db = MaterialDatabase()
    custom = Material("MYMAG", "Custom", MaterialType.PERMANENT_MAGNET,
                      mu_r=1.05, remanence_br=1.25)
    db.add(custom)
    assert db.has("MYMAG")
    dumped = db.to_dict()
    assert "MYMAG" in dumped and "N42" not in dumped  # only custom serialised

    db2 = MaterialDatabase()
    db2.load_custom(dumped)
    assert db2.get("MYMAG").remanence_br == pytest.approx(1.25)


def test_assignment_table_magnetization_vector():
    db = MaterialDatabase()
    table = AssignmentTable()
    spec = MagnetizationSpec(mode=MagnetizationMode.AXIAL, axis=(0, 0, 1))
    table.assign(body_id=1, material_id="N42", magnetization=spec)
    m = table.magnetization_vector(1, db, np.array([[0, 0, 0]]))
    assert m is not None
    assert np.allclose(m[0], [0, 0, 1.30 / MU_0])


def test_assignment_vector_none_for_non_magnet():
    db = MaterialDatabase()
    table = AssignmentTable()
    table.assign(2, "STEEL_1010")
    assert table.magnetization_vector(2, db, np.array([[0, 0, 0]])) is None


def test_north_direction_sets_magnetization_along_axis():
    # north((1,0,0)) => magnet's North along +X.
    db = MaterialDatabase()
    table = AssignmentTable()
    table.assign(1, "N42", MagnetizationSpec.north((1, 0, 0)))
    m = table.magnetization_vector(1, db, np.array([[0, 0, 0]]))
    assert np.allclose(m[0], [1.30 / MU_0, 0, 0])


def test_remanence_override_takes_precedence():
    db = MaterialDatabase()
    table = AssignmentTable()
    # Override N42 (Br=1.30) with a user-defined Br=0.5 T along +Z.
    table.assign(1, "N42", MagnetizationSpec.north((0, 0, 1)), remanence_override=0.5)
    m = table.magnetization_vector(1, db, np.array([[0, 0, 0]]))
    assert np.allclose(m[0], [0, 0, 0.5 / MU_0])


def test_remanence_override_works_on_any_material():
    # A user can turn any material into a magnet by giving it a Br + direction.
    db = MaterialDatabase()
    table = AssignmentTable()
    table.assign(1, "STEEL_1010", MagnetizationSpec.north((0, 1, 0)),
                 remanence_override=1.0)
    m = table.magnetization_vector(1, db, np.array([[0, 0, 0]]))
    assert np.allclose(m[0], [0, 1.0 / MU_0, 0])


def test_assignment_table_serialization_roundtrip():
    table = AssignmentTable()
    table.assign(1, "N52",
                 MagnetizationSpec(mode=MagnetizationMode.RADIAL, axis=(0, 0, 1)),
                 temperature_c=60.0)
    dumped = table.to_dict()
    table2 = AssignmentTable()
    table2.load(dumped)
    a = table2.get(1)
    assert a.material_id == "N52"
    assert a.temperature_c == pytest.approx(60.0)
    assert a.magnetization.mode is MagnetizationMode.RADIAL
