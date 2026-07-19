"""3D viewport widget backed by PyVista's Qt interactor (Milestone 1).

Wraps a :class:`pyvistaqt.QtInteractor` and renders the project's bodies as
surface meshes with per-body colour and visibility. Camera controls (rotate,
pan, zoom, fit) are delegated to the underlying VTK interactor. This module is
imported only when the GUI runs, so PyVista/Qt are optional at package level.
"""

from __future__ import annotations

import numpy as np

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

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.set_background("white")
        self.add_axes()
        self._actors: dict[int, object] = {}

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

    def fit_view(self) -> None:
        """Frame all visible geometry (camera 'fit to screen')."""
        self.reset_camera()
        self.render()

    def set_view(self, axis: str) -> None:
        """Snap the camera to a standard view (``'xy'``, ``'xz'``, ``'yz'``)."""
        {"xy": self.view_xy, "xz": self.view_xz, "yz": self.view_yz}.get(
            axis, self.view_isometric
        )()
