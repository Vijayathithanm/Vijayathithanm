"""Geometry operations: transforms, mirror, pattern arrays and booleans."""

from magnetflux.geometry.boolean import boolean
from magnetflux.geometry.boolean import is_available as booleans_available
from magnetflux.geometry.pattern import linear_array, polar_array
from magnetflux.geometry.transform import (
    apply_transform,
    mirror_mesh,
    rotate,
    scale,
    translate,
)

__all__ = [
    "translate",
    "rotate",
    "scale",
    "mirror_mesh",
    "apply_transform",
    "linear_array",
    "polar_array",
    "boolean",
    "booleans_available",
]
