"""Materials persist through a .mfx project round-trip via the sections map."""

import numpy as np
import pytest

from magnetflux.core.geometry import TriangleMesh
from magnetflux.core.model_tree import ModelTree
from magnetflux.core.project import Project
from magnetflux.materials import (
    MagnetizationMode,
    MagnetizationSpec,
    Material,
    MaterialDatabase,
    MaterialType,
    AssignmentTable,
    materials_from_section,
    materials_to_section,
)


def _tri() -> TriangleMesh:
    return TriangleMesh(
        np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float),
        np.array([[0, 1, 2]]),
    )


def test_materials_survive_project_save_load(tmp_path):
    tree = ModelTree()
    body = tree.add_body(_tri(), name="Ring")

    db = MaterialDatabase()
    db.add(Material("SPECIAL", "Special", MaterialType.PERMANENT_MAGNET,
                    remanence_br=1.4))
    table = AssignmentTable()
    table.assign(body.id, "SPECIAL",
                 MagnetizationSpec(mode=MagnetizationMode.RADIAL, axis=(0, 0, 1)),
                 temperature_c=45.0)

    proj = Project(name="Cathode", model_tree=tree)
    proj.sections["materials"] = materials_to_section(db, table)
    path = proj.save(tmp_path / "c.mfx")

    loaded = Project.load(path)
    db2, table2 = materials_from_section(loaded.sections["materials"])
    assert db2.get("SPECIAL").remanence_br == pytest.approx(1.4)
    a = table2.get(body.id)
    assert a.material_id == "SPECIAL"
    assert a.temperature_c == pytest.approx(45.0)
    assert a.magnetization.mode is MagnetizationMode.RADIAL
