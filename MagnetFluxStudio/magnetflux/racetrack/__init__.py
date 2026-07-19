"""Race-track (erosion) prediction layer.

Core (tangential decomposition, erosion model, comparison, heatmap array) needs
only NumPy. PNG heatmaps (matplotlib) and PDF reports (reportlab) are optional.
"""

from magnetflux.racetrack.comparison import (
    RaceTrackComparison,
    compare,
    difference_map,
)
from magnetflux.racetrack.erosion import (
    RaceTrackResult,
    compute_race_track,
    eroded_area_fraction,
    erosion_intensity,
    uniformity,
)
from magnetflux.racetrack.tangential import FieldDecomposition, decompose

__all__ = [
    "decompose",
    "FieldDecomposition",
    "erosion_intensity",
    "compute_race_track",
    "RaceTrackResult",
    "eroded_area_fraction",
    "uniformity",
    "compare",
    "difference_map",
    "RaceTrackComparison",
]
