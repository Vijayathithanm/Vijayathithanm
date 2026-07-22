"""Tests for the design-assistant recommenders and diagnostics."""

import numpy as np

from magnetflux.assistant.recommend import (
    diagnose_setup,
    recommend_magnet,
    recommend_mesh,
    recommend_solver,
)
from magnetflux.core.geometry import TriangleMesh
from magnetflux.core.model_tree import ModelTree
from magnetflux.materials.database import AssignmentTable, MaterialDatabase
from magnetflux.materials.magnetization import MagnetizationSpec


def _tri() -> TriangleMesh:
    return TriangleMesh(
        np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float),
        np.array([[0, 1, 2]]),
    )


# -- magnet recommendation ----------------------------------------------------

def test_recommend_magnet_high_temperature_excludes_ndfeb():
    db = MaterialDatabase()
    rec = recommend_magnet(db, operating_temp=200.0)
    # NdFeB N-grades top out ~60-80 C, so a 200 C requirement must pick SmCo /
    # Alnico / ferrite, never an N-grade.
    assert not rec.choice.startswith("N3") and not rec.choice.startswith("N5")
    assert rec.choice in {"SMCO_28", "SMCO_32", "ALNICO_5", "ALNICO_8",
                          "FERRITE_Y30", "FERRITE_Y35"}


def test_recommend_magnet_performance_picks_highest_br():
    db = MaterialDatabase()
    rec = recommend_magnet(db, prefer="performance")
    assert rec.choice == "N52"  # highest Br in the library


def test_recommend_magnet_target_br_filters():
    db = MaterialDatabase()
    rec = recommend_magnet(db, target_br=1.42)
    assert db.get(rec.choice).remanence_br >= 1.42


def test_recommend_magnet_none_when_impossible():
    db = MaterialDatabase()
    rec = recommend_magnet(db, target_br=5.0)  # no real magnet reaches 5 T
    assert rec.choice == "(none)"


# -- mesh / solver ------------------------------------------------------------

def test_recommend_mesh_scales_with_accuracy():
    coarse = recommend_mesh(0.1, "coarse")
    fine = recommend_mesh(0.1, "fine")
    # Finer accuracy -> smaller element size.
    coarse_mm = float(coarse.choice.split()[0])
    fine_mm = float(fine.choice.split()[0])
    assert fine_mm < coarse_mm


def test_recommend_solver_soft_iron_uses_fem():
    assert recommend_solver(has_soft_iron=True, n_bodies=3).choice == "fem"
    assert recommend_solver(has_soft_iron=False, n_bodies=1).choice == "analytic"


# -- diagnostics --------------------------------------------------------------

def test_diagnose_empty_model():
    issues = diagnose_setup(ModelTree(), MaterialDatabase(), AssignmentTable())
    assert any("No geometry" in i for i in issues)


def test_diagnose_unassigned_and_no_magnet():
    tree = ModelTree()
    tree.add_body(_tri(), name="Part")
    issues = diagnose_setup(tree, MaterialDatabase(), AssignmentTable())
    assert any("no material assigned" in i for i in issues)
    assert any("No permanent-magnet" in i for i in issues)


def test_diagnose_clean_setup_has_no_issues():
    tree = ModelTree()
    body = tree.add_body(_tri(), name="Magnet")
    db = MaterialDatabase()
    table = AssignmentTable()
    table.assign(body.id, "N42", MagnetizationSpec.north((0, 0, 1)))
    issues = diagnose_setup(tree, db, table)
    assert issues == []
