"""Bridge: build solver magnet sources from the model + material assignments.

Turns the CAD bodies plus their material assignments (Milestone 2) into the
backend-agnostic ``magnet_sources`` list a :class:`SolverProblem` needs. Each
magnet body becomes a source descriptor with its centre, magnetisation vector
[A/m] and inferred dimensions. Geometry is inferred from the body's bounding
box (treated as a box by default); users can refine the shape later.
"""

from __future__ import annotations

import numpy as np

from magnetflux.core.model_tree import ModelTree
from magnetflux.materials.database import AssignmentTable, MaterialDatabase


def build_magnet_sources(
    tree: ModelTree, db: MaterialDatabase, assignments: AssignmentTable
) -> list[dict]:
    """Return solver source descriptors for every permanent-magnet body.

    Args:
        tree: The model tree of CAD bodies.
        db: Material database (for remanence / magnetisation magnitude).
        assignments: Per-body material + magnetisation assignments.

    Returns:
        A list of ``{"shape", "center", "dims", "axis", "magnetization"}``
        dicts (SI units); non-magnet bodies are skipped.
    """
    sources: list[dict] = []
    for body in tree:
        a = assignments.get(body.id)
        if a is None or not db.has(a.material_id):
            continue
        mat = db.get(a.material_id)
        if not mat.is_magnet or a.magnetization is None:
            continue

        bbox = body.bounding_box()
        center = bbox.center
        magnitude = mat.magnetization_magnitude(a.temperature_c)
        # Uniform-direction magnetisation at the body centre (radial magnets use
        # the FEM backend; the charge model handles uniform/axial/diametric).
        direction = a.magnetization.direction_at(center[None, :])[0]
        sources.append(
            {
                "shape": "box",
                "center": center,
                "dims": bbox.size,
                "axis": a.magnetization.axis,
                "magnetization": magnitude * direction,
                "material_id": a.material_id,
            }
        )
    return sources
