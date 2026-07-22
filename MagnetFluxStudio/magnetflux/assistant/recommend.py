"""Design-assistant recommenders and diagnostics (Milestone: Assistant).

Rule-based (expert-system) recommenders -- not machine learning -- that suggest
a magnet grade, mesh resolution and solver backend from the design intent, and
flag common setup problems. Deterministic and unit-testable.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from magnetflux.materials.database import AssignmentTable, MaterialDatabase
from magnetflux.materials.material import Material, MaterialType
from magnetflux.core.model_tree import ModelTree


@dataclass(slots=True)
class Recommendation:
    """A single recommendation with rationale and ranked alternatives."""

    choice: str
    rationale: str
    alternatives: list[str] = field(default_factory=list)


# Rough relative cost per unit remanence, by magnet family (for the cost pref).
_FAMILY_COST = {"NDFEB": 3.0, "SMCO": 8.0, "ALNICO": 4.0, "FERRITE": 1.0}


def _family(material: Material) -> str:
    name = material.id.upper()
    if name.startswith("N"):
        return "NDFEB"
    if name.startswith("SMCO"):
        return "SMCO"
    if name.startswith("ALNICO"):
        return "ALNICO"
    if name.startswith("FERRITE"):
        return "FERRITE"
    return "OTHER"


def recommend_magnet(
    db: MaterialDatabase,
    target_br: float | None = None,
    operating_temp: float | None = None,
    prefer: str = "performance",
) -> Recommendation:
    """Recommend a magnet grade.

    Args:
        db: Material database to choose from.
        target_br: Minimum required remanence Br [T], if any.
        operating_temp: Operating temperature [degC]; grades whose max
            operating temperature is below this are excluded.
        prefer: ``"performance"`` (rank by Br) or ``"cost"`` (rank by a
            Br-per-cost proxy).
    """
    candidates = [m for m in db.magnets()]
    if operating_temp is not None:
        candidates = [m for m in candidates
                      if m.max_operating_temp == 0 or m.max_operating_temp >= operating_temp]
    if target_br is not None:
        candidates = [m for m in candidates if m.remanence_br >= target_br]
    if not candidates:
        return Recommendation("(none)", "No magnet grade meets the requirements; "
                              "relax the temperature or Br target.")

    if prefer == "cost":
        candidates.sort(key=lambda m: _FAMILY_COST.get(_family(m), 5.0) / m.remanence_br)
        why = "lowest cost per unit remanence meeting the constraints"
    else:
        candidates.sort(key=lambda m: m.remanence_br, reverse=True)
        why = "highest remanence meeting the constraints"

    best = candidates[0]
    return Recommendation(
        choice=best.id,
        rationale=f"{best.name} (Br={best.remanence_br:.2f} T, "
                  f"Tmax={best.max_operating_temp:.0f} C) - {why}.",
        alternatives=[m.id for m in candidates[1:4]],
    )


def recommend_mesh(model_diagonal: float, accuracy: str = "normal") -> Recommendation:
    """Recommend a mesh element size [m] from the model size and accuracy."""
    divisions = {"coarse": 15, "normal": 30, "fine": 60}.get(accuracy, 30)
    size = model_diagonal / divisions
    return Recommendation(
        choice=f"{size * 1000:.2f} mm",
        rationale=f"~{divisions} elements across the model diagonal "
                  f"({model_diagonal * 1000:.1f} mm) for '{accuracy}' accuracy.",
    )


def recommend_solver(has_soft_iron: bool, n_bodies: int) -> Recommendation:
    """Recommend a solver backend from the problem characteristics."""
    if has_soft_iron:
        return Recommendation(
            "fem", "Nonlinear soft-magnetic (steel) parts are present; the "
            "scikit-fem A-formulation captures saturation and flux through iron.",
            alternatives=["analytic"],
        )
    return Recommendation(
        "analytic", "Permanent magnets in air only; the analytic charge model "
        "is exact and fast (no meshing needed).",
        alternatives=["fem"],
    )


def diagnose_setup(
    tree: ModelTree, db: MaterialDatabase, assignments: AssignmentTable
) -> list[str]:
    """Return a list of setup warnings (empty if the model looks ready)."""
    issues: list[str] = []
    if tree.is_empty():
        issues.append("No geometry imported.")
        return issues

    n_magnets = 0
    for body in tree:
        a = assignments.get(body.id)
        if a is None:
            issues.append(f"'{body.name}' has no material assigned.")
            continue
        if not db.has(a.material_id):
            issues.append(f"'{body.name}' references unknown material "
                          f"'{a.material_id}'.")
            continue
        mat = db.get(a.material_id)
        if mat.is_magnet:
            n_magnets += 1
            br = a.effective_remanence(mat)
            if br <= 0:
                issues.append(f"'{body.name}' is a magnet with zero remanence.")
            if (mat.max_operating_temp and a.temperature_c > mat.max_operating_temp):
                issues.append(
                    f"'{body.name}' at {a.temperature_c:.0f} C exceeds "
                    f"{mat.name}'s max operating temp ({mat.max_operating_temp:.0f} C)."
                )
    if n_magnets == 0:
        issues.append("No permanent-magnet body assigned; the field will be zero.")
    return issues
