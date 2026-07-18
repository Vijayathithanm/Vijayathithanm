"""Versioned MagnetFlux project file (``.mfx``).

An ``.mfx`` file is a ZIP archive containing:

* ``manifest.json`` -- schema version, app version, units, body metadata,
  material assignments, and a free-form ``sections`` mapping that later
  milestones (materials, solver settings, results) extend without changing
  this module.
* ``meshes/body_<id>.npz`` -- ``vertices`` and ``faces`` arrays per body.

Defining the container in Milestone 0 means every later layer serialises into
one place, and old files keep loading as the schema version advances.
"""

from __future__ import annotations

import io
import json
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from magnetflux.config import PROJECT_FILE_VERSION
from magnetflux.core.geometry import TriangleMesh
from magnetflux.core.model_tree import Body, ModelTree
from magnetflux.core.units import LengthUnit


@dataclass(slots=True)
class Project:
    """In-memory representation of a MagnetFlux project.

    Attributes:
        name: Project display name.
        model_tree: The CAD bodies.
        display_length_unit: Preferred display unit (data stays SI internally).
        sections: Free-form named sections for later milestones (materials,
            solver config, results). Values must be JSON-serialisable.
    """

    name: str = "Untitled"
    model_tree: ModelTree = field(default_factory=ModelTree)
    display_length_unit: LengthUnit = LengthUnit.MILLIMETER
    sections: dict = field(default_factory=dict)

    # -- serialization ---------------------------------------------------- #

    def save(self, path: str | Path) -> Path:
        """Write the project to ``path`` as a ``.mfx`` archive."""
        path = Path(path)
        manifest = {
            "schema_version": PROJECT_FILE_VERSION,
            "name": self.name,
            "display_length_unit": self.display_length_unit.value,
            "bodies": [
                {
                    "id": b.id,
                    "name": b.name,
                    "visible": b.visible,
                    "color": list(b.color),
                    "material_id": b.material_id,
                    "source_file": b.source_file,
                }
                for b in self.model_tree
            ],
            "sections": self.sections,
        }
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("manifest.json", json.dumps(manifest, indent=2))
            for b in self.model_tree:
                buf = io.BytesIO()
                np.savez_compressed(
                    buf, vertices=b.mesh.vertices, faces=b.mesh.faces
                )
                zf.writestr(f"meshes/body_{b.id}.npz", buf.getvalue())
        return path

    @classmethod
    def load(cls, path: str | Path) -> "Project":
        """Load a project from a ``.mfx`` archive.

        Raises:
            ValueError: If the schema version is newer than this build supports.
        """
        path = Path(path)
        with zipfile.ZipFile(path, "r") as zf:
            manifest = json.loads(zf.read("manifest.json"))
            version = int(manifest.get("schema_version", 0))
            if version > PROJECT_FILE_VERSION:
                raise ValueError(
                    f"project schema version {version} is newer than supported "
                    f"version {PROJECT_FILE_VERSION}; please update MagnetFlux Studio"
                )
            tree = ModelTree()
            for entry in manifest.get("bodies", []):
                with zf.open(f"meshes/body_{entry['id']}.npz") as fh:
                    data = np.load(io.BytesIO(fh.read()))
                    mesh = TriangleMesh(data["vertices"], data["faces"])
                body = tree.add_body(
                    mesh, name=entry["name"], source_file=entry.get("source_file")
                )
                # Restore persisted state (id is reassigned by the tree; remap).
                body.visible = entry.get("visible", True)
                body.color = tuple(entry.get("color", (0.7, 0.7, 0.75)))
                body.material_id = entry.get("material_id")

            unit = LengthUnit(manifest.get("display_length_unit", "mm"))
            return cls(
                name=manifest.get("name", "Untitled"),
                model_tree=tree,
                display_length_unit=unit,
                sections=manifest.get("sections", {}),
            )
