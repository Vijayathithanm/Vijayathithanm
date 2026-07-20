"""Design space: map a normalized vector to magnet-layout parameters (Optimization).

A :class:`DesignSpace` is a list of bounded :class:`DesignVariable` s. It
decodes an optimizer's ``x in [0, 1]^n`` into physical parameter values and
builds the corresponding :class:`ParametricLayout`.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from magnetflux.optimization.layout import ParametricLayout
from magnetflux.study.parametric import PARAMETERS, apply_parameters


@dataclass(slots=True)
class DesignVariable:
    """A bounded design variable mapping to a layout parameter.

    Attributes:
        name: One of :data:`magnetflux.study.parametric.PARAMETERS`.
        low: Lower bound (physical units).
        high: Upper bound (physical units).
    """

    name: str
    low: float
    high: float

    def __post_init__(self) -> None:
        if self.name not in PARAMETERS:
            raise ValueError(f"unknown parameter '{self.name}'; valid: {PARAMETERS}")
        if self.high <= self.low:
            raise ValueError("high must exceed low")

    def decode(self, unit_value: float) -> float:
        """Map ``unit_value in [0, 1]`` to the physical range."""
        return self.low + float(np.clip(unit_value, 0.0, 1.0)) * (self.high - self.low)


class DesignSpace:
    """An ordered collection of design variables."""

    def __init__(self, variables: list[DesignVariable]) -> None:
        if not variables:
            raise ValueError("design space needs at least one variable")
        self._vars = variables

    @property
    def n_vars(self) -> int:
        return len(self._vars)

    def decode(self, x: np.ndarray) -> dict[str, float]:
        """Decode a normalized vector into ``{parameter: physical value}``."""
        x = np.asarray(x, dtype=float).ravel()
        return {v.name: v.decode(x[i]) for i, v in enumerate(self._vars)}

    def make_layout(self, base: ParametricLayout, x: np.ndarray) -> ParametricLayout:
        """Build a layout from ``base`` with the decoded design values applied."""
        return apply_parameters(base, self.decode(x))
