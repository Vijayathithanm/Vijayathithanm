"""COMSOL-style Model Builder navigation tree (Milestone: UI).

A fixed hierarchy -- Model > Geometry / Materials / Physics (Magnetostatics) /
Mesh / Study / Results / Export -- that mirrors the engineering workflow. Body
and material nodes are populated dynamically. Emits ``node_activated`` with a
stable node key the main window maps to an action or dock.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from magnetflux.core.model_tree import ModelTree

_KEY = 0x0100  # Qt.UserRole


class ModelBuilder(QTreeWidget):
    """Navigation tree following the magnetostatics workflow."""

    node_activated = Signal(str)  # node key, e.g. "geometry", "study"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setHeaderLabels(["Model Builder"])
        self.itemActivated.connect(self._on_activated)
        self.itemClicked.connect(self._on_activated)
        self._build()

    def _node(self, parent, label: str, key: str) -> QTreeWidgetItem:
        item = QTreeWidgetItem(parent, [label])
        item.setData(0, _KEY, key)
        return item

    def _build(self) -> None:
        self.clear()
        root = self._node(self, "MagnetFlux Model", "model")
        self._geometry = self._node(root, "Geometry", "geometry")
        self._materials = self._node(root, "Materials", "materials")
        physics = self._node(root, "Physics: Magnetostatics", "physics")
        self._node(physics, "Permanent Magnets", "physics.magnets")
        self._node(physics, "Magnetic Insulation", "physics.insulation")
        self._node(physics, "Symmetry", "physics.symmetry")
        self._node(root, "Mesh", "mesh")
        self._node(root, "Study: Stationary", "study")
        results = self._node(root, "Results", "results")
        self._node(results, "Flux Density (B)", "results.b")
        self._node(results, "Race Track", "results.racetrack")
        self._node(root, "Export", "export")
        self.expandAll()

    def refresh(self, tree: ModelTree) -> None:
        """Repopulate the Geometry and Materials nodes from the model tree."""
        for parent in (self._geometry, self._materials):
            parent.takeChildren()
        for body in tree:
            self._node(self._geometry, body.name, f"body.{body.id}")
            if body.material_id:
                self._node(self._materials, f"{body.name}: {body.material_id}",
                           f"material.{body.id}")

    def _on_activated(self, item: QTreeWidgetItem, _column: int = 0) -> None:
        key = item.data(0, _KEY)
        if key:
            self.node_activated.emit(str(key))
