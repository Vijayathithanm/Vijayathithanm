"""Tests for the model tree and versioned .mfx project round-trip."""

import numpy as np
import pytest

from magnetflux.core.geometry import TriangleMesh
from magnetflux.core.model_tree import ModelTree
from magnetflux.core.project import Project
from magnetflux.core.units import LengthUnit


def _tri() -> TriangleMesh:
    return TriangleMesh(
        np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float),
        np.array([[0, 1, 2]]),
    )


def test_model_tree_add_and_ids():
    tree = ModelTree()
    a = tree.add_body(_tri(), name="Magnet")
    b = tree.add_body(_tri())
    assert a.id != b.id
    assert len(tree) == 2
    assert tree.get(a.id).name == "Magnet"
    assert tree.get(b.id).name == f"Body {b.id}"


def test_model_tree_state_mutations():
    tree = ModelTree()
    body = tree.add_body(_tri())
    tree.set_visible(body.id, False)
    tree.set_color(body.id, (2.0, -1.0, 0.5))  # clamped to [0,1]
    tree.assign_material(body.id, "N42")
    assert body.visible is False
    assert body.color == (1.0, 0.0, 0.5)
    assert body.material_id == "N42"


def test_project_roundtrip(tmp_path):
    tree = ModelTree()
    body = tree.add_body(_tri(), name="Ring", source_file="ring.step")
    body.material_id = "N52"
    body.visible = False
    proj = Project(
        name="Cathode A",
        model_tree=tree,
        display_length_unit=LengthUnit.MILLIMETER,
        sections={"solver": {"mesh_size": 0.002}},
    )
    path = proj.save(tmp_path / "cathode.mfx")
    loaded = Project.load(path)

    assert loaded.name == "Cathode A"
    assert loaded.display_length_unit == LengthUnit.MILLIMETER
    assert loaded.sections["solver"]["mesh_size"] == pytest.approx(0.002)
    assert len(loaded.model_tree) == 1
    lb = loaded.model_tree.bodies[0]
    assert lb.name == "Ring"
    assert lb.material_id == "N52"
    assert lb.visible is False
    assert np.allclose(lb.mesh.vertices, body.mesh.vertices)


def test_project_rejects_future_schema(tmp_path):
    proj = Project(name="x")
    path = proj.save(tmp_path / "x.mfx")
    # Rewrite manifest with a bumped schema version.
    import json
    import zipfile

    with zipfile.ZipFile(path) as zf:
        data = {n: zf.read(n) for n in zf.namelist()}
    manifest = json.loads(data["manifest.json"])
    manifest["schema_version"] = 999
    data["manifest.json"] = json.dumps(manifest).encode()
    with zipfile.ZipFile(path, "w") as zf:
        for n, b in data.items():
            zf.writestr(n, b)

    with pytest.raises(ValueError):
        Project.load(path)
