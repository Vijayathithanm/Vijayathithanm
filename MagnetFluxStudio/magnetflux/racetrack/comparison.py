"""Compare two race-track predictions (Milestone 5 comparison view).

Given two :class:`RaceTrackResult` objects sampled on the same grid (e.g. two
magnet designs, or predicted vs. a reference), compute quantitative differences
the comparison view and report present side by side.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from magnetflux.racetrack.erosion import (
    RaceTrackResult,
    eroded_area_fraction,
    uniformity,
)


@dataclass(slots=True)
class RaceTrackComparison:
    """Quantitative comparison between two race-track predictions."""

    correlation: float          # Pearson correlation of intensity maps
    peak_shift: float           # |B_t| peak difference [T]
    uniformity_a: float
    uniformity_b: float
    eroded_fraction_a: float
    eroded_fraction_b: float

    @property
    def difference_map(self) -> np.ndarray | None:  # pragma: no cover - set below
        return getattr(self, "_diff", None)


def compare(a: RaceTrackResult, b: RaceTrackResult) -> RaceTrackComparison:
    """Compare two predictions defined on identical grids."""
    if a.dims != b.dims:
        raise ValueError("race-track results must share the same grid dimensions")
    ia, ib = a.intensity, b.intensity
    if ia.std() == 0 or ib.std() == 0:
        corr = 0.0
    else:
        corr = float(np.corrcoef(ia, ib)[0, 1])
    return RaceTrackComparison(
        correlation=corr,
        peak_shift=float(a.b_tangential_mag.max() - b.b_tangential_mag.max()),
        uniformity_a=uniformity(a),
        uniformity_b=uniformity(b),
        eroded_fraction_a=eroded_area_fraction(a),
        eroded_fraction_b=eroded_area_fraction(b),
    )


def difference_map(a: RaceTrackResult, b: RaceTrackResult) -> np.ndarray:
    """Return the ``(nu, nv)`` intensity difference ``a - b``."""
    if a.dims != b.dims:
        raise ValueError("race-track results must share the same grid dimensions")
    return a.intensity_grid() - b.intensity_grid()
