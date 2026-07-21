"""Physics layer: coil (current) sources and boundary conditions."""

from magnetflux.physics.boundary import (
    BoundaryCondition,
    PhysicsSettings,
    mirror_magnet_sources,
)
from magnetflux.physics.coil import (
    CoilSource,
    circular_loop_field,
    loop_axial_field,
)

__all__ = [
    "CoilSource",
    "circular_loop_field",
    "loop_axial_field",
    "BoundaryCondition",
    "PhysicsSettings",
    "mirror_magnet_sources",
]
