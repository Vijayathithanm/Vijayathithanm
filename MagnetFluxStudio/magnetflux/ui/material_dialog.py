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
    QFileDialog,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
)

from magnetflux.materials.material import BHCurve, Material, MaterialType


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

        self._bh_curve: BHCurve | None = None
        self._bh_button = QPushButton("Load B-H from CSV...")
        self._bh_button.setToolTip("Import a nonlinear B-H curve (H,B columns)")
        self._bh_button.clicked.connect(self._load_bh_csv)

        form.addRow("ID", self._id)
        form.addRow("Name", self._name)
        form.addRow("Type", self._type)
        form.addRow("Remanent flux density Br", self._br)
        form.addRow("Relative permeability mu_r", self._mu_r)
        form.addRow("B-H curve", self._bh_button)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _load_bh_csv(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Load B-H curve", "", "CSV (*.csv)"
        )
        if not path:
            return
        try:
            self._bh_curve = BHCurve.from_csv(path)
        except Exception as exc:  # noqa: BLE001 - surfaced to user
            QMessageBox.warning(self, "B-H curve", f"Could not load curve:\n{exc}")
            return
        self._bh_button.setText(f"B-H loaded ({self._bh_curve.b.size} points)")

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
            bh_curve=self._bh_curve,
        )
