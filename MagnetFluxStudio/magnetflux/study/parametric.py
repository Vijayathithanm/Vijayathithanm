"""Parametric study engine (Milestone: Parametric Study).

Sweeps design parameters of a :class:`ParametricLayout` -- magnet width /
thickness, ring radius (pole gap), magnet count, remanence -- solves each
configuration and tabulates the resulting magnetron metrics so designs can be
compared automatically.
"""

from __future__ import annotations

import dataclasses
import itertools
from collections.abc import Callable
from dataclasses import dataclass, field

from magnetflux.optimization.layout import ParametricLayout
from magnetflux.optimization.objectives import LayoutEvaluation, evaluate_layout

#: Parameter name -> function returning a modified layout with that value set.
_SETTERS: dict[str, Callable[[ParametricLayout, float], ParametricLayout]] = {
    "ring_radius": lambda lay, v: dataclasses.replace(lay, ring_radius=float(v)),
    "ring_count": lambda lay, v: dataclasses.replace(lay, ring_count=int(v)),
    "remanence_br": lambda lay, v: dataclasses.replace(lay, remanence_br=float(v)),
    "magnet_width": lambda lay, v: dataclasses.replace(
        lay, magnet_dims=(float(v), float(v), lay.magnet_dims[2])
    ),
    "magnet_thickness": lambda lay, v: dataclasses.replace(
        lay, magnet_dims=(lay.magnet_dims[0], lay.magnet_dims[1], float(v))
    ),
}

PARAMETERS = tuple(_SETTERS)


def apply_parameters(layout: ParametricLayout, values: dict[str, float]) -> ParametricLayout:
    """Return a copy of ``layout`` with the given parameter ``values`` applied."""
    for name, value in values.items():
        if name not in _SETTERS:
            raise ValueError(f"unknown parameter '{name}'; valid: {PARAMETERS}")
        layout = _SETTERS[name](layout, value)
    return layout


@dataclass(slots=True)
class StudyResult:
    """One configuration's parameters and resulting metrics."""

    parameters: dict[str, float]
    metrics: dict[str, float]


def _metrics(ev: LayoutEvaluation) -> dict[str, float]:
    return {
        "uniformity": ev.uniformity,
        "eroded_fraction": ev.eroded_fraction,
        "utilization": ev.utilization,
        "peak_Bt_mT": float(ev.race_track.b_tangential_mag.max() * 1e3),
    }


class ParametricStudy:
    """Runs parameter sweeps over a base :class:`ParametricLayout`."""

    def __init__(self, base_layout: ParametricLayout, resolution: int = 30) -> None:
        self._base = base_layout
        self._resolution = resolution

    def _evaluate(self, values: dict[str, float]) -> StudyResult:
        layout = apply_parameters(self._base, values)
        ev = evaluate_layout(layout, resolution=self._resolution)
        return StudyResult(parameters=dict(values), metrics=_metrics(ev))

    def sweep(self, parameter: str, values) -> list[StudyResult]:
        """One-parameter sweep over ``values``."""
        if parameter not in _SETTERS:
            raise ValueError(f"unknown parameter '{parameter}'; valid: {PARAMETERS}")
        return [self._evaluate({parameter: v}) for v in values]

    def grid(self, parameter_values: dict[str, list]) -> list[StudyResult]:
        """Full-factorial sweep over every combination of ``parameter_values``."""
        names = list(parameter_values)
        results: list[StudyResult] = []
        for combo in itertools.product(*(parameter_values[n] for n in names)):
            results.append(self._evaluate(dict(zip(names, combo))))
        return results


def best(results: list[StudyResult], metric: str, maximize: bool = True) -> StudyResult:
    """Return the run with the best value of ``metric``."""
    if not results:
        raise ValueError("no results to compare")
    key = lambda r: r.metrics[metric]  # noqa: E731
    return max(results, key=key) if maximize else min(results, key=key)
