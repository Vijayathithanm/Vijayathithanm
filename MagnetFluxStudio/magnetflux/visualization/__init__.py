"""Visualization & export layer: quantities, sampling, probes, export.

The core (quantities, sampling, probes, CSV/VTK export) depends only on
NumPy/SciPy. The PyVista renderer (:mod:`magnetflux.visualization.field_viz`)
and PNG export require the GUI extras and are imported lazily.
"""

from magnetflux.visualization.export import export_csv, export_vtk
from magnetflux.visualization.probe import GridProbe, SolverProbe
from magnetflux.visualization.quantities import (
    FieldQuantity,
    available_quantities,
    scalar_values,
)
from magnetflux.visualization.sampling import (
    StructuredField,
    grid_points,
    line_points,
    plane_points,
)

__all__ = [
    "FieldQuantity",
    "scalar_values",
    "available_quantities",
    "StructuredField",
    "grid_points",
    "plane_points",
    "line_points",
    "SolverProbe",
    "GridProbe",
    "export_csv",
    "export_vtk",
]
