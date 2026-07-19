"""Magnet spacing and pole-arrangement optimizers (Milestone 6).

Both optimizers maximise the target-utilisation estimate over a
:class:`ParametricLayout`:

* :func:`optimize_spacing` -- continuous 1-D search over the ring radius using
  SciPy's bounded scalar minimiser.
* :func:`optimize_pole_arrangement` -- discrete search over ring magnet counts.

The fast analytic backend makes the many evaluations tractable; a progress
handle allows cancellation from the GUI.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from magnetflux.optimization.layout import ParametricLayout
from magnetflux.optimization.objectives import evaluate_layout
from magnetflux.solver.base import SolverBackend


@dataclass(slots=True)
class OptimizationResult:
    """Outcome of an optimizer run.

    Attributes:
        best_value: The winning design variable (radius [m] or ring count).
        best_score: Target-utilisation score at the optimum.
        history: ``(value, score)`` pairs evaluated, in order.
    """

    best_value: float
    best_score: float
    history: list[tuple[float, float]] = field(default_factory=list)


def optimize_spacing(
    layout: ParametricLayout,
    bounds: tuple[float, float],
    backend: SolverBackend | None = None,
    progress=None,
    max_iter: int = 25,
) -> OptimizationResult:
    """Find the ring radius maximising target utilisation within ``bounds``."""
    from scipy.optimize import minimize_scalar

    history: list[tuple[float, float]] = []

    def neg_score(radius: float) -> float:
        score = evaluate_layout(layout, ring_radius=float(radius), backend=backend).utilization
        history.append((float(radius), score))
        if progress is not None:
            frac = min(1.0, len(history) / max_iter)
            progress.report(frac, f"radius={radius * 1000:.1f} mm score={score:.3f}")
        return -score

    # Sample the endpoints too: bounded Brent can miss optima at the bounds.
    neg_score(bounds[0])
    neg_score(bounds[1])
    minimize_scalar(
        neg_score, bounds=bounds, method="bounded",
        options={"maxiter": max_iter, "xatol": (bounds[1] - bounds[0]) * 1e-3},
    )
    best_value, best_score = max(history, key=lambda vs: vs[1])
    return OptimizationResult(
        best_value=float(best_value), best_score=float(best_score), history=history
    )


def optimize_pole_arrangement(
    layout: ParametricLayout,
    ring_counts: list[int],
    backend: SolverBackend | None = None,
    progress=None,
) -> OptimizationResult:
    """Pick the outer-ring magnet count maximising target utilisation."""
    history: list[tuple[float, float]] = []
    best_value = ring_counts[0]
    best_score = -1.0
    for i, n in enumerate(ring_counts):
        score = evaluate_layout(layout, ring_count=n, backend=backend).utilization
        history.append((float(n), score))
        if score > best_score:
            best_score, best_value = score, n
        if progress is not None:
            progress.report((i + 1) / len(ring_counts), f"ring_count={n} score={score:.3f}")
    return OptimizationResult(
        best_value=float(best_value), best_score=best_score, history=history
    )
