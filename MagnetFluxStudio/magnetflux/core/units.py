"""Unit conversion helpers and the project-wide unit policy.

MagnetFlux Studio stores **everything in SI internally** (metres, tesla,
amperes/metre). This module provides the conversions used at the two places
units cross the boundary:

* CAD import -- STEP/IGES/STL geometry is usually authored in millimetres.
* UI / reports -- users think in millimetres and millitesla.

Keeping conversions in one place prevents the classic 10^9 magnetostatics
error (mm treated as m).
"""

from __future__ import annotations

from enum import Enum

import numpy as np


class LengthUnit(str, Enum):
    """Supported length units for import and display."""

    METER = "m"
    MILLIMETER = "mm"
    CENTIMETER = "cm"
    INCH = "in"

    @property
    def to_meter(self) -> float:
        """Multiplicative factor converting *this* unit to metres."""
        return {
            LengthUnit.METER: 1.0,
            LengthUnit.MILLIMETER: 1.0e-3,
            LengthUnit.CENTIMETER: 1.0e-2,
            LengthUnit.INCH: 0.0254,
        }[self]


def to_meters(value: np.ndarray | float, unit: LengthUnit) -> np.ndarray | float:
    """Convert a length (scalar or array) from ``unit`` to metres."""
    factor = unit.to_meter
    if isinstance(value, np.ndarray):
        return value * factor
    return float(value) * factor


def from_meters(value: np.ndarray | float, unit: LengthUnit) -> np.ndarray | float:
    """Convert a length in metres to ``unit``."""
    factor = unit.to_meter
    if isinstance(value, np.ndarray):
        return value / factor
    return float(value) / factor


# Magnetic flux density -------------------------------------------------------

def tesla_to_millitesla(value: np.ndarray | float) -> np.ndarray | float:
    """Convert tesla to millitesla."""
    return value * 1.0e3


def millitesla_to_tesla(value: np.ndarray | float) -> np.ndarray | float:
    """Convert millitesla to tesla."""
    return value * 1.0e-3


def gauss_to_tesla(value: np.ndarray | float) -> np.ndarray | float:
    """Convert gauss to tesla (1 T = 10^4 G)."""
    return value * 1.0e-4
