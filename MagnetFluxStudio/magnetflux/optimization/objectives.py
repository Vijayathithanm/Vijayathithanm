"""Objective evaluation and target-utilization estimator (Milestone 6).

Evaluates a :class:`ParametricLayout` by solving the field on a target plane and
scoring the resulting race track. The default figure of merit is a
target-utilization estimate that rewards a wide, uniform erosion band (which is
what maximises how much target material is consumed before the groove wears
through).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from magnetflux.optimization.layout import ParametricLayout
from magnetflux.racetrack.erosion import (
    RaceTrackResult,
    compute_race_track,
    eroded_area_fraction,
    uniformity,
)
from magnetflux.solver.analytic import AnalyticBackend
from magnetflux.solver.base import SolverBackend, SolverProblem
from magnetflux.visualization.sampling import plane_points


@dataclass(slots=True)
class LayoutEvaluation:
    """Result of scoring one layout."""

    race_track: RaceTrackResult
    uniformity: float
    eroded_fraction: float
    utilization: float


def target_utilization(result: RaceTrackResult) -> float:
    """Estimate target utilisation in ``[0, 1]``.

    Combines how much of the target is eroded (a wider band uses more of the
    target) with how uniform that band is (an even groove wears through later):
    ``utilization = sqrt(eroded_fraction * uniformity)``.
    """
    ef = eroded_area_fraction(result, threshold=0.3)
    un = uniformity(result)
    return float(np.sqrt(max(ef, 0.0) * max(un, 0.0)))


def evaluate_layout(
    layout: ParametricLayout,
    ring_radius: float | None = None,
    ring_count: int | None = None,
    backend: SolverBackend | None = None,
    plane_z: float = 0.02,
    resolution: int = 40,
) -> LayoutEvaluation:
    """Solve and score a layout on its target plane."""
    backend = backend or AnalyticBackend()
    sources = layout.build_sources(ring_radius, ring_count)
    half = layout.target_plane_extent(ring_radius)
    pts, dims = plane_points(
        [0.0, 0.0, plane_z], [1, 0, 0], [0, 1, 0],
        2 * half, 2 * half, resolution, resolution,
    )
    result = backend.solve(SolverProblem(points=pts, magnet_sources=sources))
    track = compute_race_track(pts, result.b, dims, normal=[0, 0, 1])
    return LayoutEvaluation(
        race_track=track,
        uniformity=uniformity(track),
        eroded_fraction=eroded_area_fraction(track),
        utilization=target_utilization(track),
    )
