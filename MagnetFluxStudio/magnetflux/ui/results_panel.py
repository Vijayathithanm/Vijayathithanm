"""Results panel: statistics table + custom-expression evaluator (Milestone: Results).

Shows min/max/mean/RMS/std of the current field quantity and lets the user type
a custom expression (e.g. ``sqrt(Bx^2+By^2+Bz^2)``) to evaluate over the field.
Emits ``evaluate_requested`` with the expression string.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ResultsPanel(QWidget):
    """Numeric results: statistics + custom expression."""

    evaluate_requested = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self._title = QLabel("Statistics")
        self._title.setStyleSheet("font-weight: 700;")
        layout.addWidget(self._title)

        self._stats_form = QFormLayout()
        self._values: dict[str, QLabel] = {}
        for key in ("min", "max", "mean", "rms", "std"):
            lbl = QLabel("-")
            self._values[key] = lbl
            self._stats_form.addRow(key, lbl)
        layout.addLayout(self._stats_form)

        layout.addWidget(QLabel("Custom expression"))
        row = QHBoxLayout()
        self._expr = QLineEdit()
        self._expr.setPlaceholderText("sqrt(Bx^2 + By^2 + Bz^2)")
        self._expr.returnPressed.connect(self._emit)
        eval_btn = QPushButton("Evaluate")
        eval_btn.clicked.connect(self._emit)
        row.addWidget(self._expr, 1)
        row.addWidget(eval_btn)
        layout.addLayout(row)
        layout.addStretch(1)

    def _emit(self) -> None:
        text = self._expr.text().strip()
        if text:
            self.evaluate_requested.emit(text)

    def set_title(self, title: str) -> None:
        self._title.setText(title)

    def set_statistics(self, stats: dict[str, float]) -> None:
        for key, lbl in self._values.items():
            if key in stats:
                lbl.setText(f"{stats[key]:.4g}")
