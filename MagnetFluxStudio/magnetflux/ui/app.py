"""GUI bootstrap (Milestone 1).

Creates the ``QApplication``, shows the main window, and connects the crash
handler to a message dialog. Kept separate from :mod:`magnetflux.__main__` so
the entry point never imports Qt unless the GUI is actually launched.
"""

from __future__ import annotations

import sys

from magnetflux.config import APP_NAME, APP_ORG, AppConfig


def run_app(config: AppConfig | None = None) -> int:
    """Launch the desktop application and run the Qt event loop."""
    from PySide6.QtWidgets import QApplication, QMessageBox

    from magnetflux.logging_setup import install_crash_handler
    from magnetflux.ui.main_window import MainWindow

    config = config or AppConfig()

    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_ORG)

    window = MainWindow(config)

    def show_crash(text: str) -> None:
        QMessageBox.critical(window, "Unexpected error", text)

    install_crash_handler(on_crash=show_crash)

    window.show()
    return app.exec()
