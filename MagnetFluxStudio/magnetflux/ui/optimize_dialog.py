"""Design-optimization dialog (Milestone: Optimization).

The user chooses an objective (max B, max uniformity, min weight, ...), an
algorithm (genetic / particle-swarm / Bayesian) and the ring-radius bounds; the
optimizer searches the design space and reports the best design found.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from magnetflux.optimization.algorithms import OPTIMIZERS
from magnetflux.optimization.design_objectives import Objective
from magnetflux.optimization.design_space import DesignSpace, DesignVariable
from magnetflux.optimization.layout import ParametricLayout
from magnetflux.optimization.runner import optimize_design


class OptimizeDialog(QDialog):
    """Configure and run a design optimization over the ring radius."""

    def __init__(self, base_layout: ParametricLayout | None = None, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Design Optimization")
        self._base = base_layout or ParametricLayout()

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self._objective = QComboBox()
        for obj in Objective:
            self._objective.addItem(obj.value, obj)
        self._algorithm = QComboBox()
        self._algorithm.addItems(list(OPTIMIZERS))

        self._low = self._spin(0.03)
        self._high = self._spin(0.07)

        form.addRow("Objective", self._objective)
        form.addRow("Algorithm", self._algorithm)
        form.addRow("Ring radius min [m]", self._low)
        form.addRow("Ring radius max [m]", self._high)
        layout.addLayout(form)

        run_row = QHBoxLayout()
        run_btn = QPushButton("Optimize")
        run_btn.clicked.connect(self._run)
        run_row.addStretch(1)
        run_row.addWidget(run_btn)
        layout.addLayout(run_row)

        self._result = QLabel("Configure and click Optimize.")
        self._result.setWordWrap(True)
        layout.addWidget(self._result)

    def _spin(self, value: float) -> QDoubleSpinBox:
        s = QDoubleSpinBox()
        s.setRange(0.001, 1.0)
        s.setDecimals(4)
        s.setSingleStep(0.005)
        s.setValue(value)
        return s

    def _run(self) -> None:
        self._result.setText("Optimizing...")
        space = DesignSpace([DesignVariable("ring_radius", self._low.value(),
                                            self._high.value())])
        result = optimize_design(
            self._base, space, self._objective.currentData(),
            algorithm=self._algorithm.currentText(), resolution=20,
            pop_size=10, generations=6,
        ) if self._algorithm.currentText() == "ga" else optimize_design(
            self._base, space, self._objective.currentData(),
            algorithm=self._algorithm.currentText(), resolution=20,
        )
        radius = result.best_parameters.get("ring_radius", 0.0)
        self._result.setText(
            f"Best objective: {result.best_value:.4g}\n"
            f"Ring radius: {radius * 1000:.1f} mm\n"
            f"Algorithm: {result.algorithm}, evaluations: {len(result.history)}"
        )
