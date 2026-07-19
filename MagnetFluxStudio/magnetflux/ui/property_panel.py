"""Property panel: material assignment and magnetization editor (Milestone 2+).

Shown for the currently selected body. The user picks a material (or defines a
new one), sets the **remanent flux density Br**, and gives a **direction vector
that points to the magnet's North pole** -- e.g. ``(1, 0, 0)`` orients North
along +X. Emits an ``assignment_changed`` signal the main window persists.
Contains no physics itself.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from magnetflux.materials.database import Assignment, AssignmentTable, MaterialDatabase
from magnetflux.materials.magnetization import MagnetizationSpec
from magnetflux.materials.material import MaterialType


class PropertyPanel(QWidget):
    """Editor for the selected body's material, Br and North direction."""

    assignment_changed = Signal(int, object)  # (body_id, Assignment)

    def __init__(self, db: MaterialDatabase, table: AssignmentTable, parent=None) -> None:
        super().__init__(parent)
        self._db = db
        self._table = table
        self._body_id: int | None = None

        layout = QVBoxLayout(self)

        # --- Material selection + custom material creation ---------------- #
        mat_row = QWidget()
        mat_hbox = QHBoxLayout(mat_row)
        mat_hbox.setContentsMargins(0, 0, 0, 0)
        self._material_combo = QComboBox()
        self._material_combo.currentIndexChanged.connect(self._on_material_changed)
        new_btn = QPushButton("New...")
        new_btn.setToolTip("Define a custom material")
        new_btn.clicked.connect(self._create_material)
        mat_hbox.addWidget(self._material_combo, 1)
        mat_hbox.addWidget(new_btn)

        form = QFormLayout()
        form.addRow("Material", mat_row)
        self._info = QLabel("-")
        self._info.setWordWrap(True)
        form.addRow("", self._info)
        layout.addLayout(form)

        # --- Magnetization: Br + North direction -------------------------- #
        self._mag_group = QGroupBox("Magnetization")
        mag_form = QFormLayout(self._mag_group)

        self._br = QDoubleSpinBox()
        self._br.setRange(0.0, 3.0)
        self._br.setDecimals(3)
        self._br.setSingleStep(0.05)
        self._br.setSuffix(" T")
        self._br.valueChanged.connect(self._emit_change)
        mag_form.addRow("Remanent flux density Br", self._br)

        self._dir = [self._make_spin() for _ in range(3)]
        dir_widget = QWidget()
        dir_hbox = QHBoxLayout(dir_widget)
        dir_hbox.setContentsMargins(0, 0, 0, 0)
        for label, spin in zip(("X", "Y", "Z"), self._dir):
            dir_hbox.addWidget(QLabel(label))
            dir_hbox.addWidget(spin)
        mag_form.addRow("North direction", dir_widget)
        mag_form.addRow("", QLabel("Vector pointing to the magnet's North pole,\n"
                                   "e.g. (1, 0, 0) = North along +X."))

        layout.addWidget(self._mag_group)
        layout.addStretch(1)

        self._reload_materials()
        self.setEnabled(False)

    # -- widget helpers --------------------------------------------------- #

    def _make_spin(self) -> QDoubleSpinBox:
        s = QDoubleSpinBox()
        s.setRange(-1.0, 1.0)
        s.setDecimals(3)
        s.setSingleStep(0.1)
        s.valueChanged.connect(self._emit_change)
        return s

    def _reload_materials(self) -> None:
        self._material_combo.blockSignals(True)
        self._material_combo.clear()
        for m in self._db.all():
            self._material_combo.addItem(f"{m.name} ({m.id})", m.id)
        self._material_combo.blockSignals(False)

    # -- context / population --------------------------------------------- #

    def set_context(self, db: MaterialDatabase, table: AssignmentTable) -> None:
        """Point the panel at a new database/assignment table (open/new project)."""
        self._db = db
        self._table = table
        self._body_id = None
        self._reload_materials()
        self.setEnabled(False)

    def show_body(self, body_id: int) -> None:
        """Load the assignment for ``body_id`` into the widgets."""
        self._body_id = body_id
        self.setEnabled(True)
        self.blockSignals(True)
        a = self._table.get(body_id)
        if a is not None and self._db.has(a.material_id):
            idx = self._material_combo.findData(a.material_id)
            if idx >= 0:
                self._material_combo.setCurrentIndex(idx)
            mat = self._db.get(a.material_id)
            self._br.setValue(a.effective_remanence(mat))
            spec = a.magnetization or MagnetizationSpec.north((0, 0, 1))
            for s, v in zip(self._dir, spec.direction):
                s.setValue(float(v))
        else:
            self._apply_material_defaults()
        self.blockSignals(False)
        self._update_info()

    def _apply_material_defaults(self) -> None:
        """Seed Br and direction from the selected material."""
        mid = self._material_combo.currentData()
        if mid and self._db.has(mid):
            self._br.setValue(self._db.get(mid).remanence_br)
        if all(s.value() == 0.0 for s in self._dir):
            self._dir[2].setValue(1.0)  # default North along +Z

    def _on_material_changed(self, *_args) -> None:
        self.blockSignals(True)
        self._apply_material_defaults()
        self.blockSignals(False)
        self._update_info()
        self._emit_change()

    def _update_info(self) -> None:
        mid = self._material_combo.currentData()
        if not mid or not self._db.has(mid):
            self._info.setText("-")
            return
        m = self._db.get(mid)
        if m.is_nonlinear:
            self._info.setText(f"{m.mtype.value} — nonlinear B-H")
        else:
            self._info.setText(f"{m.mtype.value} — mu_r = {m.mu_r:.2f}")

    # -- change emission -------------------------------------------------- #

    def _create_material(self) -> None:
        from magnetflux.ui.material_dialog import MaterialDialog

        dlg = MaterialDialog(self)
        if dlg.exec():
            material = dlg.material()
            self._db.add(material)
            self._reload_materials()
            idx = self._material_combo.findData(material.id)
            if idx >= 0:
                self._material_combo.setCurrentIndex(idx)

    def _emit_change(self, *_args) -> None:
        if self._body_id is None:
            return
        mid = self._material_combo.currentData()
        if not mid:
            return
        direction = tuple(s.value() for s in self._dir)
        if all(component == 0.0 for component in direction):
            direction = (0.0, 0.0, 1.0)  # avoid a zero magnetization vector
        assignment = Assignment(
            material_id=mid,
            magnetization=MagnetizationSpec.north(direction),
            remanence_override=self._br.value(),
        )
        self._table._by_body[self._body_id] = assignment  # noqa: SLF001
        self.assignment_changed.emit(self._body_id, assignment)
