"""Magnetron-specific analysis derived from a magnetostatic solution.

Higher-level quantities a magnetron cathode designer reports: pole balance,
working distance, leakage flux, flux concentration, the electron-confinement
zone and a balanced/unbalanced classification. Builds on
:mod:`magnetflux.analysis.metrics` and the race-track model.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from magnetflux.racetrack.tangential import decompose


def pole_balance(flux_inner: float, flux_outer: float) -> float:
    """Pole balance in ``[0, 1]``: ``1 - |Fi-Fo| / (|Fi|+|Fo|)``.

    1.0 means the inner and outer poles carry equal flux (a *balanced*
    magnetron); lower values indicate an unbalanced design.
    """
    denom = abs(flux_inner) + abs(flux_outer)
    if denom == 0:
        return 0.0
    return float(1.0 - abs(abs(flux_inner) - abs(flux_outer)) / denom)


class MagnetronType(str, Enum):
    BALANCED = "balanced"
    UNBALANCED = "unbalanced"


def classify_magnetron(balance: float, threshold: float = 0.85) -> MagnetronType:
    """Classify as balanced/unbalanced from the pole-balance value."""
    return MagnetronType.BALANCED if balance >= threshold else MagnetronType.UNBALANCED


def working_distance(
    heights: np.ndarray, b_mag_on_axis: np.ndarray, threshold: float
) -> float:
    """Greatest height [m] above the target where ``|B|`` still exceeds ``threshold``.

    Approximates how far from the target the trapping field remains effective.
    """
    heights = np.asarray(heights, dtype=float).ravel()
    b_mag = np.asarray(b_mag_on_axis, dtype=float).ravel()
    ok = heights[b_mag >= threshold]
    return float(ok.max()) if ok.size else 0.0


def leakage_fraction(b_useful: np.ndarray, b_leak: np.ndarray) -> float:
    """Leakage-flux fraction in ``[0, 1]``.

    Ratio of field energy that escapes to the back / sides (``b_leak``) versus
    the total (useful over-target field + leakage).
    """
    from magnetflux.analysis.metrics import magnetic_energy_density

    e_use = float(magnetic_energy_density(b_useful).sum())
    e_leak = float(magnetic_energy_density(b_leak).sum())
    total = e_use + e_leak
    return float(e_leak / total) if total > 0 else 0.0


def flux_concentration(b_over_target: np.ndarray, b_reference: np.ndarray) -> float:
    """Flux concentration factor = peak |B| over target / reference |B|."""
    bt = np.linalg.norm(np.asarray(b_over_target, dtype=float).reshape(-1, 3), axis=1)
    br = np.linalg.norm(np.asarray(b_reference, dtype=float).reshape(-1, 3), axis=1)
    ref = br.mean()
    return float(bt.max() / ref) if ref > 0 else 0.0


@dataclass(slots=True)
class ConfinementZone:
    """Electron-confinement / trap zone on the target surface.

    Attributes:
        mask: Boolean ``(N,)`` -- points inside the confinement zone.
        fraction: Fraction of sampled points inside the zone.
        parallelism: ``(N,)`` ``|B_t| / |B|`` (1 = field parallel to surface).
    """

    mask: np.ndarray
    fraction: float
    parallelism: np.ndarray


def electron_confinement_zone(
    b: np.ndarray,
    normal: np.ndarray,
    b_tangential_threshold: float,
    parallel_tolerance: float = 0.9,
) -> ConfinementZone:
    """Locate the electron trap: field nearly parallel to the target and strong.

    Electrons are trapped where the magnetic field is parallel to the target
    (small normal component) and the tangential field is strong enough to close
    the ``E x B`` drift loop.

    Args:
        b: ``(N, 3)`` flux density on the target surface [T].
        normal: Target surface normal.
        b_tangential_threshold: Minimum ``|B_t|`` [T] for confinement.
        parallel_tolerance: Minimum ``|B_t|/|B|`` (closeness to parallel).
    """
    dec = decompose(b, normal)
    b_total = np.linalg.norm(np.asarray(b, dtype=float).reshape(-1, 3), axis=1)
    parallelism = np.divide(
        dec.b_tangential_mag, b_total,
        out=np.zeros_like(b_total), where=b_total > 0,
    )
    mask = (parallelism >= parallel_tolerance) & (
        dec.b_tangential_mag >= b_tangential_threshold
    )
    return ConfinementZone(
        mask=mask,
        fraction=float(np.mean(mask)) if mask.size else 0.0,
        parallelism=parallelism,
    )
