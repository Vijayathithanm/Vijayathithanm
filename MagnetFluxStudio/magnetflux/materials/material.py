"""Material model: permanent magnets, soft-magnetic (nonlinear) and air.

The solver (Milestone 3) consumes two things from a material:

* a **reluctivity** ``nu = H/B = 1/(mu_0 mu_r)`` -- constant for linear
  materials, a function of ``|B|`` for saturating steel (nonlinear B-H); and
* a **remanent magnetization** ``M = Br / mu_0`` [A/m] for permanent magnets,
  with optional temperature correction.

Keeping this physics in the material layer keeps the solver backend-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import numpy as np

from magnetflux.config import MU_0


class MaterialType(str, Enum):
    """Broad magnetic classification of a material."""

    AIR = "air"
    PERMANENT_MAGNET = "permanent_magnet"
    SOFT_MAGNETIC = "soft_magnetic"
    NON_MAGNETIC = "non_magnetic"  # e.g. copper, aluminium, stainless


@dataclass(slots=True)
class BHCurve:
    """A single-valued B-H magnetisation curve for soft-magnetic materials.

    Attributes:
        h: Monotonic magnetic field strength samples [A/m], starting at 0.
        b: Corresponding flux density samples [T], starting at 0.
    """

    h: np.ndarray
    b: np.ndarray

    def __post_init__(self) -> None:
        h = np.asarray(self.h, dtype=float).ravel()
        b = np.asarray(self.b, dtype=float).ravel()
        if h.shape != b.shape or h.size < 2:
            raise ValueError("h and b must be equal-length arrays of length >= 2")
        if np.any(np.diff(b) <= 0) or np.any(np.diff(h) < 0):
            raise ValueError("b must be strictly increasing and h non-decreasing")
        self.h = h
        self.b = b

    def h_of_b(self, b_mag: np.ndarray | float) -> np.ndarray | float:
        """Interpolate H for a given ``|B|`` (linear extrapolation past the top)."""
        b_mag = np.asarray(b_mag, dtype=float)
        return np.interp(b_mag, self.b, self.h, left=self.h[0])

    def reluctivity(self, b_mag: np.ndarray | float) -> np.ndarray | float:
        """Reluctivity ``nu = H/B`` at ``|B|``; near B=0 use the initial slope."""
        b_mag = np.asarray(b_mag, dtype=float)
        # Initial (small-signal) reluctivity from the first curve segment.
        nu0 = self.h[1] / self.b[1]
        with np.errstate(divide="ignore", invalid="ignore"):
            nu = np.where(b_mag > 1e-9, self.h_of_b(b_mag) / b_mag, nu0)
        return nu

    def initial_mu_r(self) -> float:
        """Initial relative permeability (first curve segment)."""
        return float(self.b[1] / (MU_0 * self.h[1]))


@dataclass(slots=True)
class Material:
    """A magnetic material definition.

    Attributes:
        id: Stable identifier (e.g. ``"N42"``).
        name: Human-readable name.
        mtype: Magnetic classification.
        mu_r: Relative permeability for linear materials (recoil permeability
            for permanent magnets).
        remanence_br: Remanent flux density Br [T] (permanent magnets).
        coercivity_hc: Coercivity Hc [A/m] (informational).
        temp_coeff_br: Reversible temperature coefficient of Br [%/degC].
        bh_curve: Nonlinear B-H curve (soft-magnetic materials).
        density: Mass density [kg/m^3] (informational / mass estimates).
        description: Free-form notes.
    """

    id: str
    name: str
    mtype: MaterialType
    mu_r: float = 1.0
    remanence_br: float = 0.0
    coercivity_hc: float = 0.0
    temp_coeff_br: float = 0.0
    bh_curve: BHCurve | None = None
    density: float = 0.0
    description: str = ""

    # -- physics ---------------------------------------------------------- #

    def br_at(self, temperature_c: float = 20.0) -> float:
        """Remanence at ``temperature_c`` using the reversible temp coefficient."""
        return self.remanence_br * (1.0 + self.temp_coeff_br / 100.0 * (temperature_c - 20.0))

    def magnetization_magnitude(self, temperature_c: float = 20.0) -> float:
        """Remanent magnetisation magnitude ``|M| = Br/mu_0`` [A/m]."""
        return self.br_at(temperature_c) / MU_0

    def reluctivity(self, b_mag: np.ndarray | float = 0.0) -> np.ndarray | float:
        """Reluctivity ``nu`` [m/H]. Uses the B-H curve if present, else linear."""
        if self.bh_curve is not None:
            return self.bh_curve.reluctivity(b_mag)
        mu_r = max(self.mu_r, 1e-6)
        value = 1.0 / (MU_0 * mu_r)
        return np.full_like(np.asarray(b_mag, dtype=float), value) if np.ndim(b_mag) else value

    @property
    def is_nonlinear(self) -> bool:
        return self.bh_curve is not None

    @property
    def is_magnet(self) -> bool:
        return self.mtype is MaterialType.PERMANENT_MAGNET and self.remanence_br > 0.0
