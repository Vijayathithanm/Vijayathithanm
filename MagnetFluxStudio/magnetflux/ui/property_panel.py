"""Property panel: material assignment and magnetization editor (Milestone 2).

Shown for the currently selected body. Lets the user pick a material from the
database and, for permanent magnets, edit the magnetisation mode and reference
vectors. Emits an ``assignment_changed`` signal the main window persists into
the project; contains no physics itself.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from magnetflux.materials.database import Assignment, AssignmentTable, MaterialDatabase
from magnetflux.materials.magnetization import MagnetizationMode, MagnetizationSpec
from magnetflux.materials.material import MaterialType


class PropertyPanel(QWidget):
    """Editor for the selected body's material and magnetisation."""

    assignment_changed = Signal(int, object)  # (body_id, Assignment)

    def __init__(self, db: MaterialDatabase, table: AssignmentTable, parent=None) -> None:
        super().__init__(parent)
        self._db = db
        self._table = table
        self._body_id: int | None = None

        layout = QVBoxLayout(self)

        self._material_combo = QComboBox()
        for m in db.all():
            self._material_combo.addItem(f"{m.name} ({m.id})", m.id)
        self._material_combo.currentIndexChanged.connect(self._emit_change)

        mat_form = QFormLayout()
        mat_form.addRow("Material", self._material_combo)
        self._props_label = QLabel("-")
        self._props_label.setWordWrap(True)
        mat_form.addRow("Properties", self._props_label)
        layout.addLayout(mat_form)

        self._mag_group = QGroupBox("Magnetization")
        mag_form = QFormLayout(self._mag_group)
        self._mode_combo = QComboBox()
        for mode in MagnetizationMode:
            self._mode_combo.addItem(mode.value.title(), mode)
        self._mode_combo.currentIndexChanged.connect(self._emit_change)
        mag_form.addRow("Mode", self._mode_combo)

        self._dir = [self._spin() for _ in range(3)]
        self._axis = [self._spin() for _ in range(3)]
        mag_form.addRow("Direction", self._triple_row(self._dir))
        mag_form.addRow("Axis", self._triple_row(self._axis))

        self._temp = QDoubleSpinBox()
        self._temp.setRange(-273.0, 500.0)
        self._temp.setValue(20.0)
        self._temp.setSuffix(" °C")
        self._temp.valueChanged.connect(self._emit_change)
        mag_form.addRow("Temperature", self._temp)

        layout.addWidget(self._mag_group)
        layout.addStretch(1)
        self.setEnabled(False)

    # -- helpers ---------------------------------------------------------- #

    def _spin(self) -> QDoubleSpinBox:
        s = QDoubleSpinBox()
        s.setRange(-1e3, 1e3)
        s.setDecimals(3)
        s.valueChanged.connect(self._emit_change)
        return s

    def _triple_row(self, spins) -> QWidget:
        w = QWidget()
        lay = QFormLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        inner = QWidget()
        from PySide6.QtWidgets import QHBoxLayout

        hbox = QHBoxLayout(inner)
        hbox.setContentsMargins(0, 0, 0, 0)
        for s in spins:
            hbox.addWidget(s)
        lay.addRow(inner)
        return w

    # -- population ------------------------------------------------------- #

    def set_context(self, db: MaterialDatabase, table: AssignmentTable) -> None:
        """Point the panel at a new database/assignment table (open/new project)."""
        self._db = db
        self._table = table
        self._body_id = None
        self.blockSignals(True)
        self._material_combo.clear()
        for m in db.all():
            self._material_combo.addItem(f"{m.name} ({m.id})", m.id)
        self.blockSignals(False)
        self.setEnabled(False)

    def show_body(self, body_id: int) -> None:
        """Load the assignment for ``body_id`` into the widgets."""
        self._body_id = body_id
        self.setEnabled(True)
        a = self._table.get(body_id)
        self.blockSignals(True)
        if a is not None:
            idx = self._material_combo.findData(a.material_id)
            if idx >= 0:
                self._material_combo.setCurrentIndex(idx)
            self._temp.setValue(a.temperature_c)
            spec = a.magnetization or MagnetizationSpec()
            self._mode_combo.setCurrentIndex(
                self._mode_combo.findData(spec.mode)
            )
            for s, v in zip(self._dir, spec.direction):
                s.setValue(v)
            for s, v in zip(self._axis, spec.axis):
                s.setValue(v)
        self.blockSignals(False)
        self._update_props_label()

    def _update_props_label(self) -> None:
        mid = self._material_combo.currentData()
        if not mid or not self._db.has(mid):
            return
        m = self._db.get(mid)
        is_pm = m.mtype is MaterialType.PERMANENT_MAGNET
        self._mag_group.setEnabled(is_pm)
        if is_pm:
            self._props_label.setText(f"Br = {m.remanence_br:.2f} T, mu_r = {m.mu_r:.2f}")
        elif m.is_nonlinear:
            self._props_label.setText("Nonlinear soft-magnetic (B-H curve)")
        else:
            self._props_label.setText(f"mu_r = {m.mu_r:.2f}")

    def _emit_change(self, *_args) -> None:
        if self._body_id is None:
            return
        self._update_props_label()
        spec = MagnetizationSpec(
            mode=self._mode_combo.currentData(),
            direction=tuple(s.value() for s in self._dir),
            axis=tuple(s.value() for s in self._axis),
        )
        assignment = Assignment(
            material_id=self._material_combo.currentData(),
            magnetization=spec,
            temperature_c=self._temp.value(),
        )
        self._table._by_body[self._body_id] = assignment  # noqa: SLF001
        self.assignment_changed.emit(self._body_id, assignment)
