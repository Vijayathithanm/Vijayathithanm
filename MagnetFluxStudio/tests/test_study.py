"""Tests for the parametric study engine."""

import numpy as np
import pytest

from magnetflux.optimization.layout import ParametricLayout
from magnetflux.study.parametric import (
    PARAMETERS,
    ParametricStudy,
    apply_parameters,
    best,
)


def test_apply_parameters_modifies_layout():
    base = ParametricLayout(ring_radius=0.04, ring_count=6)
    modified = apply_parameters(base, {"ring_radius": 0.06, "magnet_thickness": 0.02})
    assert modified.ring_radius == pytest.approx(0.06)
    assert modified.magnet_dims[2] == pytest.approx(0.02)
    # Base is unchanged (dataclasses.replace returns a copy).
    assert base.ring_radius == pytest.approx(0.04)


def test_apply_parameters_rejects_unknown():
    with pytest.raises(ValueError):
        apply_parameters(ParametricLayout(), {"nonsense": 1.0})


def test_sweep_returns_result_per_value():
    study = ParametricStudy(ParametricLayout(ring_count=6), resolution=24)
    results = study.sweep("ring_radius", [0.03, 0.05, 0.07])
    assert len(results) == 3
    for r in results:
        assert "ring_radius" in r.parameters
        for m in ("uniformity", "eroded_fraction", "utilization", "peak_Bt_mT"):
            assert m in r.metrics
        assert 0.0 <= r.metrics["utilization"] <= 1.0


def test_grid_is_full_factorial():
    study = ParametricStudy(ParametricLayout(), resolution=20)
    results = study.grid({"ring_radius": [0.04, 0.06], "ring_count": [4, 6]})
    assert len(results) == 4  # 2 x 2


def test_best_selects_max_metric():
    study = ParametricStudy(ParametricLayout(ring_count=6), resolution=24)
    results = study.sweep("ring_radius", [0.03, 0.05, 0.07])
    top = best(results, "utilization", maximize=True)
    assert top.metrics["utilization"] == max(r.metrics["utilization"] for r in results)


def test_parameter_names_exposed():
    assert "ring_radius" in PARAMETERS
    assert "magnet_thickness" in PARAMETERS
