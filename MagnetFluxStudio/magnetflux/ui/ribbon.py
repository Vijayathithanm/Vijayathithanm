"""Ribbon toolbar (COMSOL-style), Milestone: UI.

A ``QTabWidget`` of ribbon tabs (Home, Geometry, Materials, Physics, Mesh,
Study, Results), each holding grouped large tool buttons. Actions are wired by
the main window; this widget only builds the layout.
"""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class _RibbonGroup(QFrame):
    """A titled group of buttons within a ribbon tab."""

    def __init__(self, title: str, parent=None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 4, 6, 4)
        self._buttons = QHBoxLayout()
        outer.addLayout(self._buttons)
        caption = QLabel(title)
        caption.setAlignment(Qt.AlignHCenter)
        caption.setStyleSheet("color: #8a94a6; font-size: 8pt;")
        outer.addWidget(caption)

    def add_button(self, text: str, on_click: Callable[[], None]) -> QPushButton:
        btn = QPushButton(text)
        btn.setMinimumSize(QSize(84, 52))
        btn.clicked.connect(on_click)
        self._buttons.addWidget(btn)
        return btn


class RibbonTab(QWidget):
    """A single ribbon tab holding one or more groups."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._row = QHBoxLayout(self)
        self._row.setContentsMargins(6, 6, 6, 6)
        self._row.setAlignment(Qt.AlignLeft)

    def add_group(self, title: str) -> _RibbonGroup:
        group = _RibbonGroup(title, self)
        self._row.addWidget(group)
        return group


class RibbonBar(QTabWidget):
    """The ribbon: a set of named :class:`RibbonTab` pages."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMaximumHeight(120)

    def add_tab(self, name: str) -> RibbonTab:
        tab = RibbonTab(self)
        self.addTab(tab, name)
        return tab
