"""Application theming: light and dark Qt stylesheets (Milestone: UI).

A single :func:`stylesheet` returns the QSS for a theme so the whole app can be
switched between a professional light theme and a dark mode. Kept as pure
strings (no Qt import) so theme selection is unit-testable.
"""

from __future__ import annotations

from enum import Enum

#: MagnetFlux accent colour (magnetic blue).
ACCENT = "#2f6fdb"

_LIGHT = f"""
* {{ font-family: "Segoe UI", "Helvetica Neue", Arial; font-size: 10pt; }}
QMainWindow, QWidget {{ background: #f4f6f9; color: #1c1f24; }}
QMenuBar, QToolBar {{ background: #ffffff; border-bottom: 1px solid #d7dce3; }}
QTreeWidget, QPlainTextEdit, QComboBox, QDoubleSpinBox, QLineEdit {{
    background: #ffffff; color: #1c1f24; border: 1px solid #cfd6df; border-radius: 4px;
}}
QDockWidget::title {{ background: #eef1f5; padding: 6px; font-weight: 600; }}
QPushButton {{
    background: {ACCENT}; color: white; border: none; border-radius: 5px;
    padding: 6px 14px; font-weight: 600;
}}
QPushButton:hover {{ background: #245bc0; }}
QPushButton:disabled {{ background: #b9c2d0; }}
QTabBar::tab {{ padding: 8px 16px; background: #e7ebf1; border-top-left-radius: 5px;
    border-top-right-radius: 5px; }}
QTabBar::tab:selected {{ background: #ffffff; color: {ACCENT}; font-weight: 700; }}
"""

_DARK = f"""
* {{ font-family: "Segoe UI", "Helvetica Neue", Arial; font-size: 10pt; }}
QMainWindow, QWidget {{ background: #1e2229; color: #e6e9ef; }}
QMenuBar, QToolBar {{ background: #262b33; border-bottom: 1px solid #10131a; }}
QTreeWidget, QPlainTextEdit, QComboBox, QDoubleSpinBox, QLineEdit {{
    background: #2a2f38; color: #e6e9ef; border: 1px solid #3a414d; border-radius: 4px;
}}
QDockWidget::title {{ background: #262b33; padding: 6px; font-weight: 600; }}
QPushButton {{
    background: {ACCENT}; color: white; border: none; border-radius: 5px;
    padding: 6px 14px; font-weight: 600;
}}
QPushButton:hover {{ background: #3f82ef; }}
QPushButton:disabled {{ background: #3a414d; color: #7b828e; }}
QTabBar::tab {{ padding: 8px 16px; background: #262b33; color: #b8bfca;
    border-top-left-radius: 5px; border-top-right-radius: 5px; }}
QTabBar::tab:selected {{ background: #2a2f38; color: #6fa8ff; font-weight: 700; }}
"""


class Theme(str, Enum):
    LIGHT = "light"
    DARK = "dark"


def stylesheet(theme: Theme) -> str:
    """Return the QSS stylesheet string for ``theme``."""
    theme = Theme(theme)
    return _DARK if theme is Theme.DARK else _LIGHT
