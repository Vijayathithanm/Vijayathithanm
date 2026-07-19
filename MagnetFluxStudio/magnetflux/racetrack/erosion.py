"""Erosion-intensity model and race-track computation (Milestone 5).

Physical basis: in a planar magnetron the plasma (and therefore sputter
erosion) concentrates where the magnetic field is **parallel to the target**,
i.e. where the normal component ``B_n`` passes through zero while the tangential
component ``|B_t|`` is strong. This is the ``E x B`` electron trap that forms the
closed "race track" groove.

The erosion intensity is modelled as

    I(x) = |B_t(x)| * exp( -(B_n(x) / sigma)^2 ) ,

normalised to ``[0, 1]``. The Gaussian in ``B_n`` peaks on the ``B_n = 0`` locus
(field parallel to the surface); ``sigma`` sets how sharply erosion is confined
to that locus. This reproduces the characteristic closed-loop race track.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from magnetflux.racetrack.tangential import decompose


@dataclass(slots=True)
class RaceTrackResult:
    """Race-track prediction on a planar target surface.

    Attributes:
        points: ``(N, 3)`` target-plane sample coordinates [m].
        dims: ``(nu, nv, 1)`` grid dimensions of the plane.
        intensity: ``(N,)`` normalised erosion intensity in ``[0, 1]``.
        b_normal: ``(N,)`` normal component ``B_n`` [T].
        b_tangential_mag: ``(N,)`` tangential magnitude ``|B_t|`` [T].
        sigma: The ``B_n`` scale used in the model [T].
    """

    points: np.ndarray
    dims: tuple[int, int, int]
    intensity: np.ndarray
    b_normal: np.ndarray
    b_tangential_mag: np.ndarray
    sigma: float

    def intensity_grid(self) -> np.ndarray:
        """Erosion intensity reshaped to the plane's ``(nu, nv)`` grid."""
        nu, nv, _ = self.dims
        return self.intensity.reshape(nu, nv)


def erosion_intensity(
    b: np.ndarray, normal: np.ndarray, sigma: float | None = None
) -> tuple[np.ndarray, float]:
    """Return normalised erosion intensity and the ``sigma`` used.

    Args:
        b: ``(N, 3)`` flux density on the target surface [T].
        normal: Target surface normal.
        sigma: ``B_n`` scale [T]. Defaults to one third of the peak ``|B_n|``,
            which confines erosion to a narrow band around ``B_n = 0``.
    """
    dec = decompose(b, normal)
    if sigma is None:
        peak = float(np.max(np.abs(dec.b_normal)))
        sigma = max(peak / 3.0, 1e-9)
    raw = dec.b_tangential_mag * np.exp(-((dec.b_normal / sigma) ** 2))
    peak = float(raw.max())
    intensity = raw / peak if peak > 0 else raw
    return intensity, sigma


def compute_race_track(
    points: np.ndarray,
    b: np.ndarray,
    dims: tuple[int, int, int],
    normal: np.ndarray,
    sigma: float | None = None,
) -> RaceTrackResult:
    """Compute a :class:`RaceTrackResult` from a field sampled on a target plane."""
    dec = decompose(b, normal)
    intensity, sigma_used = erosion_intensity(b, normal, sigma)
    return RaceTrackResult(
        points=np.asarray(points, dtype=float).reshape(-1, 3),
        dims=dims,
        intensity=intensity,
        b_normal=dec.b_normal,
        b_tangential_mag=dec.b_tangential_mag,
        sigma=sigma_used,
    )


def eroded_area_fraction(result: RaceTrackResult, threshold: float = 0.5) -> float:
    """Fraction of the target where intensity exceeds ``threshold`` (0..1)."""
    return float(np.mean(result.intensity >= threshold))


def uniformity(result: RaceTrackResult) -> float:
    """Erosion uniformity in ``[0, 1]`` (``1 - std/mean`` over the eroded band).

    Computed over cells above 10% intensity so background zeros don't dominate.
    A higher value means a more even race track (better target utilisation).
    """
    band = result.intensity[result.intensity > 0.1]
    if band.size == 0 or band.mean() == 0:
        return 0.0
    return float(max(0.0, 1.0 - band.std() / band.mean()))
