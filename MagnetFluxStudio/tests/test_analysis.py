"""Tests for the analysis layer: field metrics and magnetron quantities."""

import numpy as np
import pytest

from magnetflux.analysis.magnetron import (
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
from magnetflux.config import MU_0


# -- metrics ------------------------------------------------------------------

def test_energy_density_and_total():
    b = np.array([[0, 0, 1.0], [0, 0, 2.0]])
    ed = magnetic_energy_density(b)
    assert ed[0] == pytest.approx(1.0 / (2 * MU_0))
    assert ed[1] == pytest.approx(4.0 / (2 * MU_0))
    assert total_magnetic_energy(b, cell_volume=2.0) == pytest.approx(ed.sum() * 2.0)


def test_field_uniformity():
    assert field_uniformity([1.0, 1.0, 1.0]) == pytest.approx(1.0)
    assert field_uniformity([1.0, 3.0]) < 1.0


def test_gradient_magnitude_linear_field():
    # |B| = 2x on a 1D-ish grid -> gradient magnitude = 2 everywhere.
    x = np.linspace(0, 1, 6)
    grid = (2.0 * x).reshape(6, 1, 1)
    g = gradient_magnitude(grid, spacing=(x[1] - x[0], 1.0, 1.0))
    assert np.allclose(g, 2.0)


def test_mirror_ratio():
    assert mirror_ratio([1.0, 2.0, 4.0]) == pytest.approx(4.0)
    assert mirror_ratio([0.0, 0.0]) == 0.0


def test_lorentz_force_density():
    f = lorentz_force_density([[0, 0, 1.0]], [[1.0, 0, 0]])
    assert np.allclose(f[0], [0, 1, 0])  # (0,0,1) x (1,0,0) = (0,1,0)


def test_maxwell_stress_tension_along_normal():
    # Uniform B normal to a unit-area patch -> tension |B|^2/(2 mu0) along +z.
    b = np.array([[0, 0, 1.0]])
    force = maxwell_stress_force(b, normals=[[0, 0, 1.0]], areas=[1.0])
    assert np.allclose(force[:2], 0.0)
    assert force[2] == pytest.approx(1.0 / (2 * MU_0))


def test_flux_through_surface():
    b = np.array([[0, 0, 0.5], [0, 0, 0.5]])
    phi = flux_through_surface(b, normals=[[0, 0, 1], [0, 0, 1]], areas=[2.0, 2.0])
    assert phi == pytest.approx(2.0)  # 0.5*2 + 0.5*2


# -- magnetron ----------------------------------------------------------------

def test_pole_balance_and_classification():
    assert pole_balance(1.0, 1.0) == pytest.approx(1.0)
    assert pole_balance(1.0, 0.0) == pytest.approx(0.0)
    assert classify_magnetron(pole_balance(1.0, 1.0)) is MagnetronType.BALANCED
    assert classify_magnetron(pole_balance(1.0, 0.2)) is MagnetronType.UNBALANCED


def test_working_distance():
    heights = np.array([0.0, 0.01, 0.02, 0.03])
    b_mag = np.array([0.5, 0.3, 0.15, 0.05])
    assert working_distance(heights, b_mag, threshold=0.2) == pytest.approx(0.01)
    assert working_distance(heights, b_mag, threshold=1.0) == 0.0


def test_leakage_fraction():
    useful = np.array([[0, 0, 1.0]])
    leak = np.array([[0, 0, 1.0]])
    assert leakage_fraction(useful, leak) == pytest.approx(0.5)
    assert leakage_fraction(useful, np.zeros((1, 3))) == pytest.approx(0.0)


def test_flux_concentration():
    over = np.array([[0, 0, 0.4]])
    ref = np.array([[0, 0, 0.1], [0, 0, 0.1]])
    assert flux_concentration(over, ref) == pytest.approx(4.0)


def test_electron_confinement_zone():
    # Point 0: field parallel to surface (strong B_t) -> confined.
    # Point 1: field normal to surface -> not confined.
    b = np.array([[0.1, 0.0, 0.0], [0.0, 0.0, 0.1]])
    zone = electron_confinement_zone(b, normal=[0, 0, 1],
                                     b_tangential_threshold=0.05)
    assert zone.mask.tolist() == [True, False]
    assert zone.fraction == pytest.approx(0.5)
    assert zone.parallelism[0] == pytest.approx(1.0)
