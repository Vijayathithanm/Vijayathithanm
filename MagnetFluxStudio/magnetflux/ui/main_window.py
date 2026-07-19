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
    QComboBox,
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
from magnetflux.materials.database import AssignmentTable, MaterialDatabase
from magnetflux.materials.database import materials_from_section, materials_to_section
from magnetflux.solver.service import SolverService
from magnetflux.visualization.export import export_csv, export_vtk
from magnetflux.visualization.quantities import FieldQuantity, available_quantities
from magnetflux.visualization.sampling import StructuredField, grid_points
from magnetflux.ui.log_panel import LogPanel
from magnetflux.ui.model_tree_widget import ModelTreeWidget
from magnetflux.ui.property_panel import PropertyPanel
from magnetflux.ui.viewport import Viewport

log = get_logger("ui.main_window")


class MainWindow(QMainWindow):
    """Top-level window hosting the 3D viewport and docks."""

    def __init__(self, config: AppConfig) -> None:
        super().__init__()
        self._config = config
        self._project = Project()
        self._import_job: Job | None = None
        self._material_db = MaterialDatabase()
        self._assignments = AssignmentTable()
        self._solver = SolverService()
        self._last_field: StructuredField | None = None

        self.setWindowTitle("MagnetFlux Studio")
        self.resize(1280, 800)

        self._viewport = Viewport(self)
        self.setCentralWidget(self._viewport)

        from magnetflux.visualization.field_viz import FieldVisualizer

        self._field_viz = FieldVisualizer(self._viewport)

        self._tree_widget = ModelTreeWidget(self)
        self._tree_widget.visibility_changed.connect(self._viewport.set_body_visible)
        self._tree_widget.body_selected.connect(self._on_body_selected)
        self._add_dock("Model Tree", self._tree_widget, Qt.LeftDockWidgetArea)

        self._property_panel = PropertyPanel(self._material_db, self._assignments, self)
        self._property_panel.assignment_changed.connect(self._on_assignment_changed)
        self._add_dock("Properties", self._property_panel, Qt.RightDockWidgetArea)

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

        solve_menu = self.menuBar().addMenu("&Solve")
        solve_menu.addAction("Solve Field", self._solve_field)

        display_menu = self.menuBar().addMenu("&Display")
        display_menu.addAction("Slice", lambda: self._display("slice"))
        display_menu.addAction("Contours", lambda: self._display("contours"))
        display_menu.addAction("Vector Glyphs", lambda: self._display("glyphs"))
        display_menu.addAction("Streamlines", lambda: self._display("streamlines"))
        display_menu.addSeparator()
        display_menu.addAction("Export PNG...", self._export_png)
        display_menu.addAction("Export CSV...", self._export_csv)
        display_menu.addAction("Export VTK...", self._export_vtk)

        # Field-quantity selector toolbar.
        toolbar = self.addToolBar("Field")
        self._quantity_combo = QComboBox()
        for q in available_quantities():
            self._quantity_combo.addItem(q.value, q)
        self._quantity_combo.setCurrentText(FieldQuantity.BMAG.value)
        toolbar.addWidget(self._quantity_combo)

    # -- actions ---------------------------------------------------------- #

    def _new_project(self) -> None:
        self._project = Project()
        self._assignments = AssignmentTable()
        self._material_db = MaterialDatabase()
        self._refresh_views()
        self.statusBar().showMessage("New project")

    def _on_body_selected(self, body_id: int) -> None:
        self._property_panel.show_body(body_id)

    def _on_assignment_changed(self, body_id: int, assignment) -> None:
        # Keep the model tree's material_id in sync for colouring/queries.
        self._project.model_tree.assign_material(body_id, assignment.material_id)

    # -- solve & visualize ------------------------------------------------ #

    def _current_quantity(self) -> FieldQuantity:
        return self._quantity_combo.currentData()

    def _solve_field(self) -> None:
        bbox = self._project.model_tree.bounding_box()
        if bbox is None:
            QMessageBox.information(self, "Solve", "Import a model first.")
            return
        region = bbox.padded(1.5)
        points, dims = grid_points(region, 24, 24, 24)
        self.statusBar().showMessage("Solving field...")

        def work(progress):
            problem = self._solver.build_problem(
                self._project.model_tree, self._material_db,
                self._assignments, points,
            )
            if not problem.magnet_sources:
                raise ValueError("No permanent-magnet bodies assigned.")
            return self._solver.solve(problem, progress=progress)

        def done(result) -> None:
            self._last_field = StructuredField(points, result, dims)
            self._display("slice")
            self.statusBar().showMessage(
                f"Solved: {result.metadata.get('backend', '')}"
            )

        def failed(exc: BaseException) -> None:
            log.error("Solve failed: %s", exc)
            QMessageBox.critical(self, "Solve failed", str(exc))
            self.statusBar().showMessage("Solve failed")

        Job(work, on_done=done, on_error=failed).run_sync()

    def _display(self, kind: str) -> None:
        if self._last_field is None:
            QMessageBox.information(self, "Display", "Solve the field first.")
            return
        q = self._current_quantity()
        self._field_viz.clear()
        {
            "slice": lambda: self._field_viz.show_slice(self._last_field, q),
            "contours": lambda: self._field_viz.show_contours(self._last_field, q),
            "glyphs": lambda: self._field_viz.show_glyphs(self._last_field, q),
            "streamlines": lambda: self._field_viz.show_streamlines(self._last_field, q),
        }[kind]()
        self._viewport.render()

    def _export_png(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Export PNG", "", "PNG (*.png)")
        if path:
            self._field_viz.export_png(path)
            self.statusBar().showMessage(f"Saved {Path(path).name}")

    def _export_csv(self) -> None:
        if self._last_field is None:
            QMessageBox.information(self, "Export", "Solve the field first.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV (*.csv)")
        if path:
            export_csv(path, self._last_field.result)
            self.statusBar().showMessage(f"Saved {Path(path).name}")

    def _export_vtk(self) -> None:
        if self._last_field is None:
            QMessageBox.information(self, "Export", "Solve the field first.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export VTK", "", "VTK (*.vtk)")
        if path:
            export_vtk(path, self._last_field.result, dims=self._last_field.dims)
            self.statusBar().showMessage(f"Saved {Path(path).name}")

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
            section = self._project.sections.get("materials")
            if section:
                self._material_db, self._assignments = materials_from_section(section)
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
        self._project.sections["materials"] = materials_to_section(
            self._material_db, self._assignments
        )
        try:
            self._project.save(path)
        except Exception as exc:  # noqa: BLE001 - surfaced to user
            QMessageBox.critical(self, "Save failed", str(exc))
            return
        self.statusBar().showMessage(f"Saved {Path(path).name}")

    # -- view refresh ----------------------------------------------------- #

    def _refresh_views(self) -> None:
        self._property_panel.set_context(self._material_db, self._assignments)
        self._tree_widget.set_model_tree(self._project.model_tree)
        self._viewport.render_tree(self._project.model_tree)

    def closeEvent(self, event) -> None:  # noqa: N802 (Qt override)
        self._log_panel.detach()
        super().closeEvent(event)
