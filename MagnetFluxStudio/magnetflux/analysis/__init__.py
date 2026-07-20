"""Analysis layer: field-derived quantities and magnetron-specific metrics.

Pure-NumPy post-processing of a magnetostatic solution for magnetron cathode
design. Split into generic field metrics (:mod:`~magnetflux.analysis.metrics`)
and magnetron-specific analysis (:mod:`~magnetflux.analysis.magnetron`).
"""

from magnetflux.analysis.magnetron import (
    ConfinementZone,
    MagnetronType,
    classify_magnetron,
    electron_confinement_zone,
    flux_concentration,
    leakage_fraction,
    pole_balance,
    working_distance,
)
from magnetflux.analysis.metrics import (
    field_uniformity,
    flux_through_surface,
    gradient_magnitude,
    lorentz_force_density,
    magnetic_energy_density,
    maxwell_stress_force,
    mirror_ratio,
    total_magnetic_energy,
)

__all__ = [
    # metrics
    "magnetic_energy_density",
    "total_magnetic_energy",
    "field_uniformity",
    "gradient_magnitude",
    "mirror_ratio",
    "lorentz_force_density",
    "maxwell_stress_force",
    "flux_through_surface",
    # magnetron
    "pole_balance",
    "classify_magnetron",
    "MagnetronType",
    "working_distance",
    "leakage_fraction",
    "flux_concentration",
    "electron_confinement_zone",
    "ConfinementZone",
]
