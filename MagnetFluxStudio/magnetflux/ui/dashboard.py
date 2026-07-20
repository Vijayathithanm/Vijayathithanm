"""Home dashboard landing page (COMSOL-style), Milestone: UI.

Shown on startup: quick actions (New, Open, Import CAD), recent projects,
templates, and status tiles (solver / license). Emits signals the main window
connects to; holds no project state.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from magnetflux.config import APP_NAME
from magnetflux import __version__


def _card(title: str) -> tuple[QFrame, QVBoxLayout]:
    frame = QFrame()
    frame.setFrameShape(QFrame.StyledPanel)
    lay = QVBoxLayout(frame)
    heading = QLabel(title)
    heading.setStyleSheet("font-size: 12pt; font-weight: 700;")
    lay.addWidget(heading)
    return frame, lay


class HomeDashboard(QWidget):
    """Startup landing page with quick actions and recent projects."""

    new_project = Signal()
    open_project = Signal()
    import_cad = Signal()
    open_recent = Signal(str)          # project path
    open_material_library = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        root = QVBoxLayout(self)

        header = QLabel(f"{APP_NAME}")
        header.setStyleSheet("font-size: 22pt; font-weight: 800;")
        subtitle = QLabel(f"Magnetron Cathode Magnetic Simulation  ·  v{__version__}")
        subtitle.setStyleSheet("color: #8a94a6;")
        root.addWidget(header)
        root.addWidget(subtitle)

        grid = QGridLayout()
        root.addLayout(grid, 1)

        # Quick actions.
        actions_card, actions_lay = _card("Start")
        for text, signal in (
            ("New Project", self.new_project),
            ("Open Project...", self.open_project),
            ("Import CAD...", self.import_cad),
            ("Material Library", self.open_material_library),
        ):
            btn = QPushButton(text)
            btn.clicked.connect(signal.emit)
            actions_lay.addWidget(btn)
        actions_lay.addStretch(1)
        grid.addWidget(actions_card, 0, 0)

        # Recent projects.
        recent_card, recent_lay = _card("Recent Projects")
        self._recent = QListWidget()
        self._recent.itemActivated.connect(
            lambda item: self.open_recent.emit(item.text())
        )
        recent_lay.addWidget(self._recent)
        grid.addWidget(recent_card, 0, 1)

        # Templates.
        tmpl_card, tmpl_lay = _card("Templates")
        for name in ("Planar Magnetron", "Circular Magnetron", "Balanced Magnetron"):
            lbl = QLabel(f"•  {name}")
            tmpl_lay.addWidget(lbl)
        tmpl_lay.addStretch(1)
        grid.addWidget(tmpl_card, 1, 0)

        # Status tiles.
        status_card, status_lay = _card("Status")
        status_row = QHBoxLayout()
        for label, value in (("Solver", "Ready"), ("License", "Community")):
            tile = QLabel(f"{label}\n{value}")
            tile.setAlignment(Qt.AlignCenter)
            tile.setStyleSheet(
                "background:#2f6fdb; color:white; border-radius:8px; padding:14px;"
                " font-weight:600;"
            )
            status_row.addWidget(tile)
        status_lay.addLayout(status_row)
        status_lay.addStretch(1)
        grid.addWidget(status_card, 1, 1)

    def set_recent_projects(self, paths: list[str]) -> None:
        self._recent.clear()
        self._recent.addItems(paths)
