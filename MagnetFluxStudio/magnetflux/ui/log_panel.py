"""Dockable log panel that mirrors the application log (Milestone 1).

Attaches a ``logging.Handler`` to the ``magnetflux`` logger and appends records
to a read-only text view, so users see import/solve progress and errors in-app.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QPlainTextEdit


class _QtLogBridge(QObject, logging.Handler):
    """Logging handler that forwards records to the Qt thread via a signal."""

    message = Signal(str)

    def __init__(self) -> None:
        QObject.__init__(self)
        logging.Handler.__init__(self)
        self.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s",
                              datefmt="%H:%M:%S")
        )

    def emit(self, record: logging.LogRecord) -> None:
        self.message.emit(self.format(record))


class LogPanel(QPlainTextEdit):
    """Read-only view of the application log."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setReadOnly(True)
        self.setMaximumBlockCount(5000)
        self._bridge = _QtLogBridge()
        self._bridge.message.connect(self.appendPlainText)
        logging.getLogger("magnetflux").addHandler(self._bridge)

    def detach(self) -> None:
        logging.getLogger("magnetflux").removeHandler(self._bridge)
