"""Distinct display colours for components (Milestone: Selection UX).

Generates visually distinct RGB colours so each imported body/component is
shown in its own colour instead of a uniform grey. Uses golden-ratio hue
spacing for good separation at any count. Pure stdlib, so it is unit-testable
and usable from the core model without a GUI dependency.
"""

from __future__ import annotations

import colorsys

_GOLDEN_RATIO_CONJUGATE = 0.618033988749895
_HUE_START = 0.11  # start away from pure red
_SATURATION = 0.55
_VALUE = 0.90


def color_for_index(index: int) -> tuple[float, float, float]:
    """Deterministic distinct RGB colour (each channel in ``[0, 1]``) for ``index``."""
    hue = (_HUE_START + index * _GOLDEN_RATIO_CONJUGATE) % 1.0
    return colorsys.hsv_to_rgb(hue, _SATURATION, _VALUE)


def distinct_colors(n: int) -> list[tuple[float, float, float]]:
    """Return ``n`` visually distinct RGB colours."""
    return [color_for_index(i) for i in range(n)]
