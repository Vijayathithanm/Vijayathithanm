"""Air-domain generation for the FEM solver (Milestone 3).

The magnetostatic FEM problem is posed on the magnets/iron *plus* a surrounding
air region truncated at an outer boundary. This module builds that air box from
the model's bounding box and a padding factor, and exposes the far-field
boundary used for the magnetic-insulation condition.
"""

from __future__ import annotations

from magnetflux.core.geometry import BoundingBox


def generate_air_domain(model_bbox: BoundingBox, padding: float = 2.0) -> BoundingBox:
    """Return the air-domain bounding box enclosing the model.

    Args:
        model_bbox: Bounding box of all solids [m].
        padding: Air padding as a multiple of each half-extent. ``padding=2.0``
            makes the air box three times the model size in every direction,
            keeping the truncation boundary far enough that the magnetic-
            insulation BC error is small.

    Returns:
        The padded air-domain :class:`BoundingBox`.
    """
    if padding < 0:
        raise ValueError("padding must be non-negative")
    return model_bbox.padded(padding)
