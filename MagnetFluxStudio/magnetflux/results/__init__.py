"""Results post-processing: statistics, cut lines/planes, custom expressions."""

from magnetflux.results.expressions import evaluate_expression
from magnetflux.results.probes import CutLine, cut_line, cut_plane
from magnetflux.results.statistics import (
    FieldStatistics,
    field_statistics,
    volume_integral,
)

__all__ = [
    "field_statistics",
    "FieldStatistics",
    "volume_integral",
    "evaluate_expression",
    "cut_line",
    "cut_plane",
    "CutLine",
]
