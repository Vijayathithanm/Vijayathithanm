"""Boundary-conditions dialog for the magnetostatics physics (Milestone: Physics).

Lets the user choose the outer-boundary condition and, for a symmetry plane,
its normal. Returns a :class:`PhysicsSettings` the main window stores on the
project and passes to the solver.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QWidget,
    QHBoxLayout,
)

from magnetflux.physics.boundary import BoundaryCondition, PhysicsSettings


class PhysicsDialog(QDialog):
    """Edit the magnetostatics boundary conditions."""

    def __init__(self, settings: PhysicsSettings | None = None, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Physics — Boundary Conditions")
        settings = settings or PhysicsSettings()
        form = QFormLayout(self)

        self._bc = QComboBox()
        for bc in BoundaryCondition:
            self._bc.addItem(bc.value.replace("_", " ").title(), bc)
        idx = self._bc.findData(settings.outer_boundary)
        if idx >= 0:
            self._bc.setCurrentIndex(idx)
        form.addRow("Outer boundary", self._bc)

        self._normal = [self._spin(v) for v in settings.symmetry_plane_normal]
        row = QWidget()
        hbox = QHBoxLayout(row)
        hbox.setContentsMargins(0, 0, 0, 0)
        for s in self._normal:
            hbox.addWidget(s)
        form.addRow("Symmetry normal", row)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _spin(self, value: float) -> QDoubleSpinBox:
        s = QDoubleSpinBox()
        s.setRange(-1.0, 1.0)
        s.setDecimals(2)
        s.setSingleStep(1.0)
        s.setValue(value)
        return s

    def settings(self) -> PhysicsSettings:
        return PhysicsSettings(
            outer_boundary=self._bc.currentData(),
            symmetry_plane_normal=tuple(s.value() for s in self._normal),
        )
