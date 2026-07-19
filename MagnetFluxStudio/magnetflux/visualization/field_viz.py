"""PyVista field visualizer (Milestone 4).

Renders a solved structured field as surface contours, slice planes, vector
glyphs and streamlines, coloured by a selectable :class:`FieldQuantity`, and
exports the current scene to PNG. Consumes a
:class:`~magnetflux.visualization.sampling.StructuredField`; imported only when
the GUI runs (PyVista is an optional dependency).
"""

from __future__ import annotations

import numpy as np

from magnetflux.visualization.quantities import FieldQuantity, scalar_values
from magnetflux.visualization.sampling import StructuredField


def structured_field_to_pyvista(field: StructuredField, quantity: FieldQuantity):
    """Build a PyVista StructuredGrid from a sampled field with named arrays."""
    import pyvista as pv

    nx, ny, nz = field.dims
    pts = field.points.reshape(nx, ny, nz, 3)
    grid = pv.StructuredGrid()
    grid.dimensions = (nx, ny, nz)
    grid.points = field.points
    grid["B"] = field.result.b
    grid[quantity.value] = scalar_values(field.result, quantity)
    grid.set_active_scalars(quantity.value)
    grid.set_active_vectors("B")
    return grid


class FieldVisualizer:
    """Adds field visualization actors to a PyVista plotter."""

    def __init__(self, plotter) -> None:
        self._plotter = plotter
        self._actors: list = []

    def clear(self) -> None:
        for actor in self._actors:
            self._plotter.remove_actor(actor)
        self._actors.clear()

    def show_contours(self, field: StructuredField, quantity: FieldQuantity,
                      n_contours: int = 10) -> None:
        grid = structured_field_to_pyvista(field, quantity)
        contours = grid.contour(n_contours, scalars=quantity.value)
        self._actors.append(
            self._plotter.add_mesh(contours, cmap="viridis",
                                   scalar_bar_args={"title": f"{quantity.value} [{quantity.unit}]"})
        )

    def show_slice(self, field: StructuredField, quantity: FieldQuantity,
                   normal=(0, 0, 1)) -> None:
        grid = structured_field_to_pyvista(field, quantity)
        sliced = grid.slice(normal=normal)
        self._actors.append(
            self._plotter.add_mesh(sliced, cmap="viridis",
                                   scalar_bar_args={"title": f"{quantity.value} [{quantity.unit}]"})
        )

    def show_glyphs(self, field: StructuredField, quantity: FieldQuantity,
                    factor: float = 0.01) -> None:
        grid = structured_field_to_pyvista(field, quantity)
        glyphs = grid.glyph(orient="B", scale="B", factor=factor)
        self._actors.append(self._plotter.add_mesh(glyphs, cmap="viridis"))

    def show_streamlines(self, field: StructuredField, quantity: FieldQuantity,
                         n_points: int = 100) -> None:
        grid = structured_field_to_pyvista(field, quantity)
        streams = grid.streamlines(
            "B", n_points=n_points, source_radius=float(np.linalg.norm(
                field.points.max(axis=0) - field.points.min(axis=0)) / 4),
        )
        self._actors.append(
            self._plotter.add_mesh(streams.tube(radius=field_tube_radius(field)),
                                   cmap="viridis")
        )

    def export_png(self, path: str) -> None:
        """Save the current render window to a PNG file."""
        self._plotter.screenshot(path)


def field_tube_radius(field: StructuredField) -> float:
    """A reasonable streamline tube radius from the field extent."""
    extent = np.linalg.norm(field.points.max(axis=0) - field.points.min(axis=0))
    return float(extent) * 0.002
