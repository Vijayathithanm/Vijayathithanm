"""Regression tests: str-enum values (as Qt combo boxes yield) are coerced.

Qt stores a ``str``-subclass enum as a plain string in combo-box item data, so
``currentData()`` returns e.g. ``"Bx"`` instead of ``FieldQuantity.BX``. The
consuming code must tolerate that (previously crashed with
``'str' object has no attribute 'value'``).
"""

import numpy as np
import pytest

from magnetflux.materials.magnetization import MagnetizationMode, MagnetizationSpec
from magnetflux.solver.base import FieldResult
from magnetflux.visualization.quantities import FieldQuantity, scalar_values


def test_scalar_values_accepts_string_quantity():
    res = FieldResult(np.array([[0, 0, 0.03]]), np.array([[3.0, 0.0, 4.0]]))
    from_str = scalar_values(res, "|B|")
    from_enum = scalar_values(res, FieldQuantity.BMAG)
    assert from_str[0] == pytest.approx(5.0)
    assert np.allclose(from_str, from_enum)


def test_magnetization_spec_coerces_string_mode():
    spec = MagnetizationSpec(mode="radial", axis=(0, 0, 1))
    assert spec.mode is MagnetizationMode.RADIAL
    # direction_at relies on `is` comparisons that only work once coerced.
    d = spec.direction_at([[1.0, 0.0, 0.5]])
    assert np.allclose(d[0], [1, 0, 0])
    # to_dict uses .value, which fails on a raw string.
    assert spec.to_dict()["mode"] == "radial"


def test_magnetization_spec_uniform_string_mode():
    spec = MagnetizationSpec(mode="uniform", direction=(0, 0, 2))
    assert spec.mode is MagnetizationMode.UNIFORM
    assert np.allclose(spec.direction_at([[9, 9, 9]])[0], [0, 0, 1])
