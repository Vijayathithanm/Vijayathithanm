"""Parametric sweep dialog with an automatic comparison table (Milestone: Study).

The user picks a design parameter and a start/stop/steps range; the study runs
each configuration through the solver + magnetron analysis and shows a
comparison table, highlighting the best design by target utilisation.
"""

from __future__ import annotations

import numpy as np
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from magnetflux.optimization.layout import ParametricLayout
from magnetflux.study.parametric import PARAMETERS, ParametricStudy, best

_METRICS = ("uniformity", "eroded_fraction", "utilization", "peak_Bt_mT")


class ParametricDialog(QDialog):
    """Configure and run a single-parameter sweep, then compare results."""

    def __init__(self, base_layout: ParametricLayout | None = None, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Parametric Study")
        self.resize(560, 420)
        self._base = base_layout or ParametricLayout()

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self._param = QComboBox()
        self._param.addItems(PARAMETERS)
        self._start = self._spin(0.02)
        self._stop = self._spin(0.08)
        self._steps = QSpinBox()
        self._steps.setRange(2, 25)
        self._steps.setValue(5)

        form.addRow("Parameter", self._param)
        form.addRow("Start", self._start)
        form.addRow("Stop", self._stop)
        form.addRow("Steps", self._steps)
        layout.addLayout(form)

        run_row = QHBoxLayout()
        run_btn = QPushButton("Run Sweep")
        run_btn.clicked.connect(self._run)
        run_row.addStretch(1)
        run_row.addWidget(run_btn)
        layout.addLayout(run_row)

        self._table = QTableWidget()
        self._table.setColumnCount(1 + len(_METRICS))
        self._table.setHorizontalHeaderLabels(["value", *_METRICS])
        layout.addWidget(self._table)

    def _spin(self, value: float) -> QDoubleSpinBox:
        s = QDoubleSpinBox()
        s.setRange(0.0, 1000.0)
        s.setDecimals(4)
        s.setSingleStep(0.01)
        s.setValue(value)
        return s

    def _run(self) -> None:
        param = self._param.currentText()
        values = np.linspace(self._start.value(), self._stop.value(),
                             self._steps.value())
        if param == "ring_count":
            values = np.unique(np.round(values).astype(int))
        study = ParametricStudy(self._base, resolution=26)
        results = study.sweep(param, list(values))
        top = best(results, "utilization")

        self._table.setRowCount(len(results))
        for row, r in enumerate(results):
            value = next(iter(r.parameters.values()))
            self._table.setItem(row, 0, QTableWidgetItem(f"{value:g}"))
            for col, metric in enumerate(_METRICS, start=1):
                item = QTableWidgetItem(f"{r.metrics[metric]:.4g}")
                if r is top:
                    item.setBackground(QColor("#c9e7c9"))
                self._table.setItem(row, col, item)
        self._table.resizeColumnsToContents()
