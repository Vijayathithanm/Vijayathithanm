"""Derived electromagnetic quantities from a magnetostatic solution.

Pure NumPy functions computing the field-derived quantities a magnetron
designer needs from a solved B field: energy, gradient, uniformity, the
magnetic-mirror ratio, Lorentz force density, and the Maxwell-stress force /
flux through a surface. All SI units (metres, tesla, A/m, newtons).
"""

from __future__ import annotations

import numpy as np

from magnetflux.config import MU_0


def magnetic_energy_density(b: np.ndarray) -> np.ndarray:
    """Energy density ``|B|^2 / (2 mu_0)`` [J/m^3] at each point."""
    b = np.asarray(b, dtype=float).reshape(-1, 3)
    return np.einsum("ij,ij->i", b, b) / (2.0 * MU_0)


def total_magnetic_energy(b: np.ndarray, cell_volume: np.ndarray | float) -> float:
    """Total magnetic energy [J] = integral of energy density over the volume."""
    return float(np.sum(magnetic_energy_density(b) * cell_volume))


def field_uniformity(values: np.ndarray) -> float:
    """Field uniformity in ``[0, 1]`` (``1 - std/mean``); 1 = perfectly uniform."""
    v = np.asarray(values, dtype=float).ravel()
    mean = v.mean()
    if mean == 0:
        return 0.0
    return float(max(0.0, 1.0 - v.std() / abs(mean)))


def gradient_magnitude(scalar_grid: np.ndarray, spacing: tuple[float, ...]) -> np.ndarray:
    """Magnitude of the gradient of a scalar field on a structured grid.

    Args:
        scalar_grid: e.g. ``|B|`` reshaped to the grid ``(nx, ny, nz)``.
        spacing: physical spacing along each axis [m].
    """
    arr = np.asarray(scalar_grid, dtype=float)
    # Only differentiate axes with more than one sample (skip singleton dims,
    # e.g. a slice plane of shape (nu, nv, 1)).
    axes = tuple(ax for ax in range(arr.ndim) if arr.shape[ax] > 1)
    if not axes:
        return np.zeros_like(arr)
    sp = [spacing[ax] for ax in axes]
    grads = np.gradient(arr, *sp, axis=axes)
    if not isinstance(grads, list):
        grads = [grads]
    return np.sqrt(np.sum([g**2 for g in grads], axis=0))


def mirror_ratio(b_mag_along_line: np.ndarray) -> float:
    """Magnetic mirror ratio ``B_max / B_min`` along a field line / axis.

    Governs magnetic-mirror electron confinement: a higher ratio traps a wider
    range of electron pitch angles.
    """
    v = np.asarray(b_mag_along_line, dtype=float).ravel()
    v = v[v > 0]
    if v.size == 0:
        return 0.0
    return float(v.max() / v.min())


def lorentz_force_density(current_density: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Lorentz force density ``J x B`` [N/m^3] at each point."""
    j = np.asarray(current_density, dtype=float).reshape(-1, 3)
    field = np.asarray(b, dtype=float).reshape(-1, 3)
    return np.cross(j, field)


def maxwell_stress_force(
    b: np.ndarray, normals: np.ndarray, areas: np.ndarray
) -> np.ndarray:
    """Net force [N] on a closed surface via the Maxwell stress tensor.

    Traction ``t = (1/mu_0)[(B.n) B - 1/2 |B|^2 n]`` integrated over the
    surface. For a field normal to the surface this reduces to a tension
    ``|B|^2 / (2 mu_0)`` along the normal.
    """
    field = np.asarray(b, dtype=float).reshape(-1, 3)
    n = np.asarray(normals, dtype=float).reshape(-1, 3)
    a = np.asarray(areas, dtype=float).ravel()
    bn = np.einsum("ij,ij->i", field, n)
    b2 = np.einsum("ij,ij->i", field, field)
    traction = (bn[:, None] * field - 0.5 * b2[:, None] * n) / MU_0
    return (traction * a[:, None]).sum(axis=0)


def flux_through_surface(
    b: np.ndarray, normals: np.ndarray, areas: np.ndarray
) -> float:
    """Magnetic flux [Wb] through a surface = integral of ``B.n dA``."""
    field = np.asarray(b, dtype=float).reshape(-1, 3)
    n = np.asarray(normals, dtype=float).reshape(-1, 3)
    a = np.asarray(areas, dtype=float).ravel()
    return float(np.sum(np.einsum("ij,ij->i", field, n) * a))
