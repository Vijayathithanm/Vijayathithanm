"""Material database and per-body assignment table (Milestone 2).

:class:`MaterialDatabase` holds the built-in library plus any user-defined
materials. :class:`AssignmentTable` records, per body, which material is applied
together with its magnetisation direction and operating temperature. Both
serialise into the project's ``materials`` section so assignments persist.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from magnetflux.materials.grades import BUILTIN_MATERIALS
from magnetflux.materials.magnetization import MagnetizationSpec
from magnetflux.materials.material import BHCurve, Material, MaterialType


class MaterialDatabase:
    """The library of available materials (built-in + user-defined)."""

    def __init__(self) -> None:
        self._materials: dict[str, Material] = dict(BUILTIN_MATERIALS)
        self._custom_ids: set[str] = set()

    def get(self, material_id: str) -> Material:
        return self._materials[material_id]

    def has(self, material_id: str) -> bool:
        return material_id in self._materials

    def all(self) -> list[Material]:
        return list(self._materials.values())

    def magnets(self) -> list[Material]:
        return [m for m in self._materials.values() if m.is_magnet]

    def by_type(self, mtype: MaterialType) -> list[Material]:
        return [m for m in self._materials.values() if m.mtype is mtype]

    def add(self, material: Material) -> None:
        """Add or overwrite a user-defined material."""
        self._materials[material.id] = material
        self._custom_ids.add(material.id)

    def remove(self, material_id: str) -> None:
        if material_id in self._custom_ids:
            self._materials.pop(material_id, None)
            self._custom_ids.discard(material_id)

    # -- serialization (custom materials only) ---------------------------- #

    def to_dict(self) -> dict:
        out = {}
        for mid in self._custom_ids:
            m = self._materials[mid]
            out[mid] = {
                "name": m.name,
                "mtype": m.mtype.value,
                "mu_r": m.mu_r,
                "remanence_br": m.remanence_br,
                "coercivity_hc": m.coercivity_hc,
                "temp_coeff_br": m.temp_coeff_br,
                "density": m.density,
                "description": m.description,
                "bh_curve": (
                    {"h": m.bh_curve.h.tolist(), "b": m.bh_curve.b.tolist()}
                    if m.bh_curve else None
                ),
            }
        return out

    def load_custom(self, data: dict) -> None:
        for mid, d in data.items():
            curve = d.get("bh_curve")
            bh = BHCurve(np.asarray(curve["h"]), np.asarray(curve["b"])) if curve else None
            self.add(Material(
                id=mid, name=d["name"], mtype=MaterialType(d["mtype"]),
                mu_r=d.get("mu_r", 1.0), remanence_br=d.get("remanence_br", 0.0),
                coercivity_hc=d.get("coercivity_hc", 0.0),
                temp_coeff_br=d.get("temp_coeff_br", 0.0),
                bh_curve=bh, density=d.get("density", 0.0),
                description=d.get("description", ""),
            ))


@dataclass(slots=True)
class Assignment:
    """A material assignment for one body.

    Attributes:
        material_id: Id into a :class:`MaterialDatabase`.
        magnetization: Direction spec (permanent magnets); ``None`` otherwise.
        temperature_c: Operating temperature [degC] for Br(T) correction.
    """

    material_id: str
    magnetization: MagnetizationSpec | None = None
    temperature_c: float = 20.0

    def to_dict(self) -> dict:
        return {
            "material_id": self.material_id,
            "magnetization": self.magnetization.to_dict() if self.magnetization else None,
            "temperature_c": self.temperature_c,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Assignment":
        mag = data.get("magnetization")
        return cls(
            material_id=data["material_id"],
            magnetization=MagnetizationSpec.from_dict(mag) if mag else None,
            temperature_c=data.get("temperature_c", 20.0),
        )


class AssignmentTable:
    """Maps body id -> :class:`Assignment`."""

    def __init__(self) -> None:
        self._by_body: dict[int, Assignment] = {}

    def assign(
        self,
        body_id: int,
        material_id: str,
        magnetization: MagnetizationSpec | None = None,
        temperature_c: float = 20.0,
    ) -> Assignment:
        a = Assignment(material_id, magnetization, temperature_c)
        self._by_body[body_id] = a
        return a

    def get(self, body_id: int) -> Assignment | None:
        return self._by_body.get(body_id)

    def clear(self, body_id: int) -> None:
        self._by_body.pop(body_id, None)

    def items(self):
        return self._by_body.items()

    def magnetization_vector(
        self, body_id: int, db: MaterialDatabase, points: np.ndarray
    ) -> np.ndarray | None:
        """Magnetisation vector field ``M`` [A/m] at ``points`` for a magnet body.

        Returns ``None`` if the body is unassigned or not a permanent magnet.
        """
        a = self._by_body.get(body_id)
        if a is None or not db.has(a.material_id):
            return None
        mat = db.get(a.material_id)
        if not mat.is_magnet or a.magnetization is None:
            return None
        magnitude = mat.magnetization_magnitude(a.temperature_c)
        directions = a.magnetization.direction_at(points)
        return magnitude * directions

    # -- serialization ---------------------------------------------------- #

    def to_dict(self) -> dict:
        return {str(bid): a.to_dict() for bid, a in self._by_body.items()}

    def load(self, data: dict) -> None:
        for bid, d in data.items():
            self._by_body[int(bid)] = Assignment.from_dict(d)


def materials_to_section(db: MaterialDatabase, table: AssignmentTable) -> dict:
    """Serialise custom materials and assignments into a project section."""
    return {"custom_materials": db.to_dict(), "assignments": table.to_dict()}


def materials_from_section(
    section: dict,
) -> tuple[MaterialDatabase, AssignmentTable]:
    """Rebuild a database + assignment table from a project ``materials`` section."""
    db = MaterialDatabase()
    db.load_custom(section.get("custom_materials", {}))
    table = AssignmentTable()
    table.load(section.get("assignments", {}))
    return db, table
