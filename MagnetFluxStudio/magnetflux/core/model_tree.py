"""Model tree: the hierarchy of CAD bodies in a project.

A :class:`Body` is a single solid (one region of the future FEM domain). The
:class:`ModelTree` owns the ordered collection of bodies and provides the
display/state a viewport and property panel need: visibility, colour, naming.
Material assignment (Milestone 2) is referenced by id, not embedded here, to
keep the CAD and material layers decoupled.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from magnetflux.core.geometry import BoundingBox, TriangleMesh
from magnetflux.core.palette import color_for_index


@dataclass(slots=True)
class Body:
    """A single CAD solid within the model tree.

    Attributes:
        id: Stable unique identifier (assigned by :class:`ModelTree`).
        name: Human-readable display name.
        mesh: Triangulated surface of the solid [m].
        visible: Whether the body is shown in the viewport.
        color: RGB display colour, each channel in ``[0, 1]``.
        material_id: Id of the assigned material (Milestone 2), or ``None``.
        source_file: Originating CAD file, for provenance.
    """

    id: int
    name: str
    mesh: TriangleMesh
    visible: bool = True
    color: tuple[float, float, float] = (0.7, 0.7, 0.75)
    material_id: str | None = None
    source_file: str | None = None

    def bounding_box(self) -> BoundingBox:
        return self.mesh.bounding_box()


class ModelTree:
    """Ordered collection of :class:`Body` objects with stable ids."""

    def __init__(self) -> None:
        self._bodies: dict[int, Body] = {}
        self._next_id: int = 1

    # -- population ------------------------------------------------------- #

    def add_body(
        self,
        mesh: TriangleMesh,
        name: str | None = None,
        *,
        source_file: str | None = None,
    ) -> Body:
        """Create and register a new body from ``mesh``.

        Each body is given a distinct display colour (by insertion order) so
        imported assembly components are visually differentiated.
        """
        body_id = self._next_id
        self._next_id += 1
        body = Body(
            id=body_id,
            name=name or f"Body {body_id}",
            mesh=mesh,
            color=color_for_index(len(self._bodies)),
            source_file=source_file,
        )
        self._bodies[body_id] = body
        return body

    def remove_body(self, body_id: int) -> None:
        """Remove a body by id (no-op if absent)."""
        self._bodies.pop(body_id, None)

    # -- access ----------------------------------------------------------- #

    def get(self, body_id: int) -> Body:
        return self._bodies[body_id]

    @property
    def bodies(self) -> list[Body]:
        """Bodies in insertion order."""
        return list(self._bodies.values())

    def __len__(self) -> int:
        return len(self._bodies)

    def __iter__(self):
        return iter(self._bodies.values())

    def is_empty(self) -> bool:
        return not self._bodies

    # -- queries ---------------------------------------------------------- #

    def bounding_box(self) -> BoundingBox | None:
        """Union bounding box of all bodies, or ``None`` if empty."""
        if not self._bodies:
            return None
        return BoundingBox.union([b.bounding_box() for b in self._bodies.values()])

    def rename(self, body_id: int, name: str) -> None:
        self._bodies[body_id].name = name

    def set_visible(self, body_id: int, visible: bool) -> None:
        self._bodies[body_id].visible = visible

    def set_color(self, body_id: int, color: tuple[float, float, float]) -> None:
        rgb = np.clip(np.asarray(color, dtype=float), 0.0, 1.0)
        self._bodies[body_id].color = (float(rgb[0]), float(rgb[1]), float(rgb[2]))

    def assign_material(self, body_id: int, material_id: str | None) -> None:
        self._bodies[body_id].material_id = material_id
