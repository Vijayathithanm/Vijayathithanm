"""Model-tree dock widget (Milestone 1).

A ``QTreeWidget`` mirroring the project's :class:`ModelTree`: each body is a row
with a visibility checkbox and an editable name. Emits signals the main window
connects to the viewport, keeping GUI wiring out of the domain model.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from magnetflux.core.model_tree import ModelTree

_ID_ROLE = Qt.UserRole + 1


class ModelTreeWidget(QTreeWidget):
    """Tree view of bodies with visibility toggles and rename."""

    visibility_changed = Signal(int, bool)   # (body_id, visible)
    body_selected = Signal(int)              # body_id
    body_renamed = Signal(int, str)          # (body_id, new_name)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setHeaderLabels(["Body"])
        self.setColumnCount(1)
        self._tree: ModelTree | None = None
        self.itemChanged.connect(self._on_item_changed)
        self.itemClicked.connect(self._on_item_clicked)

    def set_model_tree(self, tree: ModelTree) -> None:
        """Rebuild the widget from ``tree``."""
        self._tree = tree
        self.blockSignals(True)
        self.clear()
        for body in tree:
            item = QTreeWidgetItem([body.name])
            item.setData(0, _ID_ROLE, body.id)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
            item.setCheckState(0, Qt.Checked if body.visible else Qt.Unchecked)
            self.addTopLevelItem(item)
        self.blockSignals(False)

    def _on_item_changed(self, item: QTreeWidgetItem, _column: int) -> None:
        body_id = item.data(0, _ID_ROLE)
        if body_id is None or self._tree is None:
            return
        visible = item.checkState(0) == Qt.Checked
        self._tree.set_visible(body_id, visible)
        self.visibility_changed.emit(body_id, visible)
        name = item.text(0)
        if name and name != self._tree.get(body_id).name:
            self._tree.rename(body_id, name)
            self.body_renamed.emit(body_id, name)

    def _on_item_clicked(self, item: QTreeWidgetItem, _column: int) -> None:
        body_id = item.data(0, _ID_ROLE)
        if body_id is not None:
            self.body_selected.emit(body_id)
