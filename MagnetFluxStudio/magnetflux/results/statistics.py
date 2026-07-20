"""Scalar statistics over a sampled field (Milestone: Results).

Min / max / mean / RMS / std of any field quantity, plus a volume integral,
for the results panel's numeric summary.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class FieldStatistics:
    """Summary statistics of a scalar field quantity."""

    minimum: float
    maximum: float
    mean: float
    rms: float
    std: float

    def as_dict(self) -> dict[str, float]:
        return {
            "min": self.minimum,
            "max": self.maximum,
            "mean": self.mean,
            "rms": self.rms,
            "std": self.std,
        }


def field_statistics(values: np.ndarray) -> FieldStatistics:
    """Compute summary statistics of ``values``."""
    v = np.asarray(values, dtype=float).ravel()
    if v.size == 0:
        return FieldStatistics(0.0, 0.0, 0.0, 0.0, 0.0)
    return FieldStatistics(
        minimum=float(v.min()),
        maximum=float(v.max()),
        mean=float(v.mean()),
        rms=float(np.sqrt(np.mean(v**2))),
        std=float(v.std()),
    )


def volume_integral(values: np.ndarray, cell_volume: np.ndarray | float) -> float:
    """Integral of ``values`` over the volume ``sum(values * cell_volume)``."""
    return float(np.sum(np.asarray(values, dtype=float).ravel() * cell_volume))
