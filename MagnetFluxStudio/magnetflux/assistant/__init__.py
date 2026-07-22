"""Design-assistant layer: rule-based recommenders and setup diagnostics."""

from magnetflux.assistant.recommend import (
    Recommendation,
    diagnose_setup,
    recommend_magnet,
    recommend_mesh,
    recommend_solver,
)

__all__ = [
    "Recommendation",
    "recommend_magnet",
    "recommend_mesh",
    "recommend_solver",
    "diagnose_setup",
]
