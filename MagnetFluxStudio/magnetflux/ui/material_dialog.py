"""Dialog for defining a user-editable custom material (Milestone 2+).

Lets the user create their own material with any name, type, remanent flux
density and relative permeability, which is then added to the database and
selectable like the built-in grades.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
)

from magnetflux.materials.material import Material, MaterialType


class MaterialDialog(QDialog):
    """Create a custom :class:`Material` from user input."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("New Material")
        form = QFormLayout(self)

        self._id = QLineEdit()
        self._id.setPlaceholderText("e.g. MY_MAGNET")
        self._name = QLineEdit()
        self._name.setPlaceholderText("e.g. Custom NdFeB")

        self._type = QComboBox()
        for t in MaterialType:
            self._type.addItem(t.value.replace("_", " ").title(), t)
        self._type.setCurrentText("Permanent Magnet")

        self._br = QDoubleSpinBox()
        self._br.setRange(0.0, 3.0)
        self._br.setDecimals(3)
        self._br.setSingleStep(0.05)
        self._br.setValue(1.30)
        self._br.setSuffix(" T")

        self._mu_r = QDoubleSpinBox()
        self._mu_r.setRange(1.0, 100000.0)
        self._mu_r.setDecimals(3)
        self._mu_r.setValue(1.05)

        form.addRow("ID", self._id)
        form.addRow("Name", self._name)
        form.addRow("Type", self._type)
        form.addRow("Remanent flux density Br", self._br)
        form.addRow("Relative permeability mu_r", self._mu_r)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _on_accept(self) -> None:
        if not self._id.text().strip() or not self._name.text().strip():
            QMessageBox.warning(self, "New Material", "ID and Name are required.")
            return
        self.accept()

    def material(self) -> Material:
        """Return the :class:`Material` defined by the dialog fields."""
        mtype: MaterialType = self._type.currentData()
        return Material(
            id=self._id.text().strip(),
            name=self._name.text().strip(),
            mtype=mtype,
            mu_r=self._mu_r.value(),
            remanence_br=self._br.value() if mtype is MaterialType.PERMANENT_MAGNET else 0.0,
        )
