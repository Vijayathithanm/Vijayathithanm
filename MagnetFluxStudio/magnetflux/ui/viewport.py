"""3D viewport widget backed by PyVista's Qt interactor (Milestone 1).

Wraps a :class:`pyvistaqt.QtInteractor` and renders the project's bodies as
surface meshes with per-body colour and visibility. Camera controls (rotate,
pan, zoom, fit) are delegated to the underlying VTK interactor. This module is
imported only when the GUI runs, so PyVista/Qt are optional at package level.
"""

from __future__ import annotations

import numpy as np

from PySide6.QtCore import Signal
from pyvistaqt import QtInteractor  # noqa: E402  (optional GUI dependency)

from magnetflux.core.model_tree import Body, ModelTree


def _to_polydata(body: Body):
    """Convert a body's TriangleMesh to a PyVista PolyData surface."""
    import pyvista as pv

    faces = body.mesh.faces
    # PyVista face array format: [n0, i0, i1, i2, n1, ...] with n=3 per triangle.
    padded = np.hstack(
        [np.full((len(faces), 1), 3, dtype=np.int64), faces]
    ).ravel()
    return pv.PolyData(body.mesh.vertices, padded)


class Viewport(QtInteractor):
    """Interactive 3D view of the model tree."""

    body_picked = Signal(int)     # body id clicked in the scene (domain selection)
    point_picked = Signal(object)  # (x, y, z) for boundary/edge/point modes

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.set_background("white")
        self.add_axes()
        self._actors: dict[int, object] = {}
        self._selection_mode = "domain"
        self._selected_id: int | None = None

    def render_tree(self, tree: ModelTree) -> None:
        """Replace the scene with the bodies in ``tree``."""
        self.clear()
        self._actors.clear()
        for body in tree:
            self.add_body(body)
        if not tree.is_empty():
            self.reset_camera()

    def add_body(self, body: Body) -> None:
        """Add or replace a single body's actor."""
        if body.id in self._actors:
            self.remove_actor(self._actors[body.id])
        actor = self.add_mesh(
            _to_polydata(body),
            color=body.color,
            show_edges=False,
            smooth_shading=True,
            name=f"body_{body.id}",
        )
        actor.SetVisibility(body.visible)
        self._actors[body.id] = actor

    def set_body_visible(self, body_id: int, visible: bool) -> None:
        actor = self._actors.get(body_id)
        if actor is not None:
            actor.SetVisibility(visible)
            self.render()

    # -- selection -------------------------------------------------------- #

    def set_selection_mode(self, mode: str) -> None:
        """Set the selection mode: 'domain', 'boundary', 'edge' or 'point'."""
        self._selection_mode = mode
        self._enable_picking()

    def _enable_picking(self) -> None:
        """Enable click picking appropriate to the current selection mode."""
        try:
            if self._selection_mode == "domain":
                self.enable_mesh_picking(
                    self._on_domain_pick, use_actor=True, show=False,
                    show_message=False, left_clicking=True,
                )
            else:
                self.enable_point_picking(
                    self._on_point_pick, show_message=False, left_clicking=True,
                )
        except Exception:  # pragma: no cover - picking unavailable in some backends
            pass

    def _on_domain_pick(self, actor) -> None:
        for body_id, a in self._actors.items():
            if a is actor:
                self.highlight_body(body_id)
                self.body_picked.emit(body_id)
                return

    def _on_point_pick(self, point) -> None:
        if point is not None:
            self.point_picked.emit(tuple(float(c) for c in point))

    def highlight_body(self, body_id: int) -> None:
        """Outline the selected body and un-highlight the rest."""
        self._selected_id = body_id
        for bid, actor in self._actors.items():
            prop = actor.GetProperty()
            prop.SetEdgeVisibility(bid == body_id)
            prop.SetLineWidth(3 if bid == body_id else 1)
        self.render()

    def fit_view(self) -> None:
        """Frame all visible geometry (camera 'fit to screen')."""
        self.reset_camera()
        self.render()

    def set_view(self, axis: str) -> None:
        """Snap the camera to a standard view (``'xy'``, ``'xz'``, ``'yz'``)."""
        {"xy": self.view_xy, "xz": self.view_xz, "yz": self.view_yz}.get(
            axis, self.view_isometric
        )()
