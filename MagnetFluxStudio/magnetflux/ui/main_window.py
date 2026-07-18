"""Main application window (Milestone 1).

Assembles the viewport, model-tree dock and log dock, and wires the File menu
(import CAD, open/save project). CAD import runs on a background job so the UI
stays responsive. This class holds a :class:`Project` but contains no numerical
or solver logic -- it only orchestrates domain-layer calls.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QFileDialog,
    QMainWindow,
    QMessageBox,
)

from magnetflux.cad.importer import SUPPORTED_EXTENSIONS, import_cad
from magnetflux.config import PROJECT_FILE_EXTENSION, AppConfig
from magnetflux.core.jobs import Job
from magnetflux.core.project import Project
from magnetflux.core.units import LengthUnit
from magnetflux.logging_setup import get_logger
from magnetflux.ui.log_panel import LogPanel
from magnetflux.ui.model_tree_widget import ModelTreeWidget
from magnetflux.ui.viewport import Viewport

log = get_logger("ui.main_window")


class MainWindow(QMainWindow):
    """Top-level window hosting the 3D viewport and docks."""

    def __init__(self, config: AppConfig) -> None:
        super().__init__()
        self._config = config
        self._project = Project()
        self._import_job: Job | None = None

        self.setWindowTitle("MagnetFlux Studio")
        self.resize(1280, 800)

        self._viewport = Viewport(self)
        self.setCentralWidget(self._viewport)

        self._tree_widget = ModelTreeWidget(self)
        self._tree_widget.visibility_changed.connect(self._viewport.set_body_visible)
        self._add_dock("Model Tree", self._tree_widget, Qt.LeftDockWidgetArea)

        self._log_panel = LogPanel(self)
        self._add_dock("Log", self._log_panel, Qt.BottomDockWidgetArea)

        self._build_menus()
        self.statusBar().showMessage("Ready")

    # -- construction helpers -------------------------------------------- #

    def _add_dock(self, title: str, widget, area) -> None:
        dock = QDockWidget(title, self)
        dock.setWidget(widget)
        self.addDockWidget(area, dock)

    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction("&New Project", self._new_project)
        file_menu.addAction("&Import CAD...", self._import_cad_dialog)
        file_menu.addSeparator()
        file_menu.addAction("&Open Project...", self._open_project_dialog)
        file_menu.addAction("&Save Project...", self._save_project_dialog)
        file_menu.addSeparator()
        file_menu.addAction("E&xit", self.close)

        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction("Fit", self._viewport.fit_view)
        view_menu.addAction("Isometric", lambda: self._viewport.set_view("iso"))
        view_menu.addAction("Top (XY)", lambda: self._viewport.set_view("xy"))
        view_menu.addAction("Front (XZ)", lambda: self._viewport.set_view("xz"))
        view_menu.addAction("Right (YZ)", lambda: self._viewport.set_view("yz"))

    # -- actions ---------------------------------------------------------- #

    def _new_project(self) -> None:
        self._project = Project()
        self._refresh_views()
        self.statusBar().showMessage("New project")

    def _import_cad_dialog(self) -> None:
        patterns = " ".join(f"*{e}" for e in sorted(SUPPORTED_EXTENSIONS))
        path, _ = QFileDialog.getOpenFileName(
            self, "Import CAD", "", f"CAD files ({patterns})"
        )
        if path:
            self._import_cad(Path(path))

    def _import_cad(self, path: Path) -> None:
        self.statusBar().showMessage(f"Importing {path.name}...")

        def work(progress):
            progress.report(0.1, f"Reading {path.name}")
            meshes = import_cad(path, source_unit=LengthUnit.MILLIMETER)
            progress.report(0.9, "Building bodies")
            return meshes

        def done(meshes) -> None:
            stem = path.stem
            for i, mesh in enumerate(meshes):
                name = stem if len(meshes) == 1 else f"{stem} [{i + 1}]"
                self._project.model_tree.add_body(
                    mesh, name=name, source_file=str(path)
                )
            self._refresh_views()
            self.statusBar().showMessage(
                f"Imported {path.name}: {len(meshes)} solid(s)"
            )

        def failed(exc: BaseException) -> None:
            log.error("Import failed: %s", exc)
            QMessageBox.critical(self, "Import failed", str(exc))
            self.statusBar().showMessage("Import failed")

        self._import_job = Job(
            work, on_done=done, on_error=failed
        )
        # Run synchronously for a small file; large assemblies could use start().
        self._import_job.run_sync()

    def _open_project_dialog(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", f"MagnetFlux (*{PROJECT_FILE_EXTENSION})"
        )
        if not path:
            return
        try:
            self._project = Project.load(path)
        except Exception as exc:  # noqa: BLE001 - surfaced to user
            QMessageBox.critical(self, "Open failed", str(exc))
            return
        self._refresh_views()
        self.statusBar().showMessage(f"Opened {Path(path).name}")

    def _save_project_dialog(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Project", "", f"MagnetFlux (*{PROJECT_FILE_EXTENSION})"
        )
        if not path:
            return
        if not path.endswith(PROJECT_FILE_EXTENSION):
            path += PROJECT_FILE_EXTENSION
        try:
            self._project.save(path)
        except Exception as exc:  # noqa: BLE001 - surfaced to user
            QMessageBox.critical(self, "Save failed", str(exc))
            return
        self.statusBar().showMessage(f"Saved {Path(path).name}")

    # -- view refresh ----------------------------------------------------- #

    def _refresh_views(self) -> None:
        self._tree_widget.set_model_tree(self._project.model_tree)
        self._viewport.render_tree(self._project.model_tree)

    def closeEvent(self, event) -> None:  # noqa: N802 (Qt override)
        self._log_panel.detach()
        super().closeEvent(event)
