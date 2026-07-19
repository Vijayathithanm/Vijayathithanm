"""Selectable field quantities derived from a solved field (Milestone 4).

The visualization and export layers let the user choose which scalar to colour
by (``|B|``, a component, ``|H|``, energy density). Centralising the mapping
keeps contours, slices, probes and exports consistent.
"""

from __future__ import annotations

from enum import Enum

import numpy as np

from magnetflux.solver.base import FieldResult


class FieldQuantity(str, Enum):
    """A scalar quantity that can be visualised or exported."""

    BX = "Bx"
    BY = "By"
    BZ = "Bz"
    BMAG = "|B|"
    HMAG = "|H|"
    ENERGY = "energy_density"

    @property
    def unit(self) -> str:
        return {
            FieldQuantity.BX: "T",
            FieldQuantity.BY: "T",
            FieldQuantity.BZ: "T",
            FieldQuantity.BMAG: "T",
            FieldQuantity.HMAG: "A/m",
            FieldQuantity.ENERGY: "J/m^3",
        }[self]


def scalar_values(result: FieldResult, quantity: FieldQuantity) -> np.ndarray:
    """Return the ``(N,)`` scalar array for ``quantity`` from ``result``."""
    return {
        FieldQuantity.BX: result.bx,
        FieldQuantity.BY: result.by,
        FieldQuantity.BZ: result.bz,
        FieldQuantity.BMAG: result.b_magnitude,
        FieldQuantity.HMAG: np.linalg.norm(result.h, axis=1),
        FieldQuantity.ENERGY: result.energy_density(),
    }[quantity]


def available_quantities() -> list[FieldQuantity]:
    """All selectable field quantities."""
    return list(FieldQuantity)
