"""Named design objectives for optimization (Milestone: Optimization).

Turns a scored :class:`LayoutEvaluation` (and the layout itself) into a single
scalar the optimizers **maximise**. Minimisation goals (weight, cost, leakage)
are returned negated so every objective is "higher is better".
"""

from __future__ import annotations

from enum import Enum

from magnetflux.optimization.layout import ParametricLayout
from magnetflux.optimization.objectives import LayoutEvaluation


class Objective(str, Enum):
    MAX_B = "max_B"
    MAX_UNIFORMITY = "max_uniformity"
    MAX_UTILIZATION = "max_utilization"
    MIN_LEAKAGE = "min_leakage"
    MIN_WEIGHT = "min_weight"
    MIN_COST = "min_cost"


#: Relative cost per kg by magnet family (NdFeB dearest, ferrite cheapest).
_COST_PER_KG = {"ndfeb": 60.0, "smco": 200.0, "alnico": 40.0, "ferrite": 8.0}


def magnet_weight(layout: ParametricLayout, density: float = 7500.0) -> float:
    """Total magnet mass [kg]: one central + ``ring_count`` ring magnets."""
    volume = layout.magnet_dims[0] * layout.magnet_dims[1] * layout.magnet_dims[2]
    return volume * (layout.ring_count + 1) * density


def magnet_cost(layout: ParametricLayout, family: str = "ndfeb") -> float:
    """Relative magnet cost = mass x cost-per-kg for the magnet family."""
    return magnet_weight(layout) * _COST_PER_KG.get(family, 60.0)


def objective_value(
    objective: Objective, layout: ParametricLayout, evaluation: LayoutEvaluation
) -> float:
    """Return the scalar to maximise for ``objective`` (higher is better)."""
    objective = Objective(objective)
    if objective is Objective.MAX_B:
        return float(evaluation.race_track.b_tangential_mag.max())
    if objective is Objective.MAX_UNIFORMITY:
        return float(evaluation.uniformity)
    if objective is Objective.MAX_UTILIZATION:
        return float(evaluation.utilization)
    if objective is Objective.MIN_LEAKAGE:
        # More field usefully over the target (wider eroded band) = less leakage.
        return float(evaluation.eroded_fraction)
    if objective is Objective.MIN_WEIGHT:
        return -magnet_weight(layout)
    if objective is Objective.MIN_COST:
        return -magnet_cost(layout)
    raise ValueError(f"unknown objective {objective!r}")
