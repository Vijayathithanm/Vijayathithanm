"""Materials layer: magnet grades, nonlinear soft-iron, magnetization."""

from magnetflux.materials.database import (
    Assignment,
    AssignmentTable,
    MaterialDatabase,
    materials_from_section,
    materials_to_section,
)
from magnetflux.materials.grades import BUILTIN_MATERIALS, MAGNET_GRADES
from magnetflux.materials.magnetization import MagnetizationMode, MagnetizationSpec
from magnetflux.materials.material import BHCurve, Material, MaterialType

__all__ = [
    "Material",
    "MaterialType",
    "BHCurve",
    "MaterialDatabase",
    "Assignment",
    "AssignmentTable",
    "MagnetizationSpec",
    "MagnetizationMode",
    "BUILTIN_MATERIALS",
    "MAGNET_GRADES",
    "materials_to_section",
    "materials_from_section",
]
