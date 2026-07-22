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

from magnetflux.cad.importer import SUPPORTED_EXTENSIONS, import_cad_named
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
from magnetflux.ui.model_builder import ModelBuilder
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

        from magnetflux.physics.boundary import PhysicsSettings

        self._physics = PhysicsSettings()

        self.setWindowTitle("MagnetFlux Studio")
        self.resize(1360, 860)

        # Central area: a stacked widget switching between the home dashboard
        # and the 3D workspace, COMSOL-style.
        from PySide6.QtWidgets import QStackedWidget

        from magnetflux.ui.dashboard import HomeDashboard
        from magnetflux.visualization.field_viz import FieldVisualizer

        self._stack = QStackedWidget(self)
        self.setCentralWidget(self._stack)

        self._dashboard = HomeDashboard(self)
        self._dashboard.new_project.connect(self._dashboard_new)
        self._dashboard.open_project.connect(self._dashboard_open)
        self._dashboard.import_cad.connect(self._dashboard_import)
        self._dashboard.open_material_library.connect(self._enter_workspace)
        self._stack.addWidget(self._dashboard)

        self._viewport = Viewport(self)
        self._stack.addWidget(self._viewport)
        self._field_viz = FieldVisualizer(self._viewport)
        self._viewport.body_picked.connect(self._on_body_selected)
        self._viewport.point_picked.connect(self._on_point_picked)

        # Docks.
        self._model_builder = ModelBuilder(self)
        self._model_builder.node_activated.connect(self._on_node_activated)
        self._builder_dock = self._add_dock(
            "Model Builder", self._model_builder, Qt.LeftDockWidgetArea
        )

        self._tree_widget = ModelTreeWidget(self)
        self._tree_widget.visibility_changed.connect(self._viewport.set_body_visible)
        self._tree_widget.body_selected.connect(self._on_body_selected)
        self._tree_dock = self._add_dock(
            "Geometry", self._tree_widget, Qt.LeftDockWidgetArea
        )

        self._property_panel = PropertyPanel(self._material_db, self._assignments, self)
        self._property_panel.assignment_changed.connect(self._on_assignment_changed)
        self._prop_dock = self._add_dock(
            "Properties", self._property_panel, Qt.RightDockWidgetArea
        )

        from magnetflux.ui.results_panel import ResultsPanel

        self._results_panel = ResultsPanel(self)
        self._results_panel.evaluate_requested.connect(self._evaluate_expression)
        self._results_dock = self._add_dock(
            "Results", self._results_panel, Qt.RightDockWidgetArea
        )

        self._log_panel = LogPanel(self)
        self._log_dock = self._add_dock("Log", self._log_panel, Qt.BottomDockWidgetArea)

        self._build_menus()
        self._build_ribbon()
        self._show_dashboard()
        self.statusBar().showMessage("Ready")

    # -- construction helpers -------------------------------------------- #

    def _add_dock(self, title: str, widget, area):
        dock = QDockWidget(title, self)
        dock.setWidget(widget)
        self.addDockWidget(area, dock)
        return dock

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

        analyze_menu = self.menuBar().addMenu("&Analyze")
        analyze_menu.addAction("Predict Race Track...", self._predict_race_track)
        analyze_menu.addAction("PDF Report...", self._generate_report)

        opt_menu = self.menuBar().addMenu("&Optimize")
        opt_menu.addAction("Magnet Spacing Study...", self._optimize_spacing)
        opt_menu.addAction("Pole Count Study...", self._optimize_poles)

        # Field-quantity selector toolbar.
        toolbar = self.addToolBar("Field")
        self._quantity_combo = QComboBox()
        for q in available_quantities():
            self._quantity_combo.addItem(q.value, q)
        self._quantity_combo.setCurrentText(FieldQuantity.BMAG.value)
        toolbar.addWidget(self._quantity_combo)

    def _build_ribbon(self) -> None:
        from magnetflux.ui.ribbon import RibbonBar

        ribbon = RibbonBar(self)

        home = ribbon.add_tab("Home")
        g = home.add_group("Project")
        g.add_button("New", self._new_project)
        g.add_button("Open", self._open_project_dialog)
        g.add_button("Save", self._save_project_dialog)
        g = home.add_group("View")
        g.add_button("Home", self._show_dashboard)
        g.add_button("Dark Mode", self._toggle_theme)

        geo = ribbon.add_tab("Geometry")
        g = geo.add_group("Import")
        g.add_button("Import CAD", self._import_cad_dialog)
        g = geo.add_group("Selection")
        g.add_button("Domain", lambda: self._set_selection_mode("domain"))
        g.add_button("Boundary", lambda: self._set_selection_mode("boundary"))
        g.add_button("Edge", lambda: self._set_selection_mode("edge"))
        g.add_button("Point", lambda: self._set_selection_mode("point"))
        g = geo.add_group("Visibility")
        g.add_button("Show All", lambda: self._set_all_visible(True))
        g.add_button("Hide All", lambda: self._set_all_visible(False))
        g = geo.add_group("Modify")
        g.add_button("Polar Array", self._polar_array)
        g.add_button("Mirror", self._mirror_body)
        g = geo.add_group("Camera")
        g.add_button("Fit", self._viewport.fit_view)
        g.add_button("Isometric", lambda: self._viewport.set_view("iso"))

        mat = ribbon.add_tab("Materials")
        g = mat.add_group("Materials")
        g.add_button("New Material", self._new_material)

        physics = ribbon.add_tab("Physics")
        g = physics.add_group("Magnetostatics")
        g.add_button("Boundary Conditions", self._edit_physics)

        mesh = ribbon.add_tab("Mesh")
        g = mesh.add_group("Mesh")
        g.add_button("Statistics", self._mesh_statistics)

        study = ribbon.add_tab("Study")
        g = study.add_group("Solve")
        g.add_button("Solve Field", self._solve_field)
        g = study.add_group("Magnetron")
        g.add_button("Race Track", self._predict_race_track)
        g.add_button("Race PDF", self._generate_report)
        g.add_button("Full Report", self._full_report)
        g = study.add_group("Parametric")
        g.add_button("Sweep", self._parametric_sweep)

        assistant = ribbon.add_tab("Assistant")
        g = assistant.add_group("Recommend")
        g.add_button("Magnet", self._recommend_magnet)
        g.add_button("Solver", self._recommend_solver)
        g = assistant.add_group("Check")
        g.add_button("Diagnose Setup", self._diagnose_setup)

        optimize = ribbon.add_tab("Optimize")
        g = optimize.add_group("Design")
        g.add_button("Optimize", self._design_optimize)
        g = optimize.add_group("Quick")
        g.add_button("Spacing", self._optimize_spacing)
        g.add_button("Poles", self._optimize_poles)

        results = ribbon.add_tab("Results")
        g = results.add_group("Plots")
        g.add_button("Slice", lambda: self._display("slice"))
        g.add_button("Contours", lambda: self._display("contours"))
        g.add_button("Glyphs", lambda: self._display("glyphs"))
        g.add_button("Streamlines", lambda: self._display("streamlines"))
        g = results.add_group("Analysis")
        g.add_button("Statistics", self._show_statistics)
        g = results.add_group("Export")
        g.add_button("PNG", self._export_png)
        g.add_button("CSV", self._export_csv)
        g.add_button("VTK", self._export_vtk)

        self._ribbon_toolbar = self.addToolBar("Ribbon")
        self.addToolBarBreak()
        self._ribbon_toolbar.addWidget(ribbon)
        self._ribbon_toolbar.setMovable(False)

    def _new_material(self) -> None:
        self._property_panel._create_material()  # noqa: SLF001

    def _edit_physics(self) -> None:
        from magnetflux.ui.physics_dialog import PhysicsDialog

        dlg = PhysicsDialog(self._physics, self)
        if dlg.exec():
            self._physics = dlg.settings()
            self.statusBar().showMessage(
                f"Boundary condition: {self._physics.outer_boundary.value}"
            )

    def _mesh_statistics(self) -> None:
        from magnetflux.mesh import generate_mesh, mesh_statistics
        from magnetflux.solver.air_domain import generate_air_domain

        bbox = self._project.model_tree.bounding_box()
        if bbox is None:
            QMessageBox.information(self, "Mesh", "Import a model first.")
            return
        domain = generate_air_domain(bbox, self._config.default_air_padding)
        self.statusBar().showMessage("Meshing air domain...")
        mesh = generate_mesh(domain, mesh_size=domain.diagonal / 20.0)
        stats = mesh_statistics(mesh.points, mesh.tets)
        lines = "\n".join(
            f"{k}: {v:.4g}" if isinstance(v, float) else f"{k}: {v}"
            for k, v in stats.as_dict().items()
        )
        QMessageBox.information(self, "Mesh Statistics", lines)
        self.statusBar().showMessage("Mesh statistics computed")

    def _parametric_sweep(self) -> None:
        from magnetflux.ui.parametric_dialog import ParametricDialog

        ParametricDialog(parent=self).exec()

    def _design_optimize(self) -> None:
        from magnetflux.ui.optimize_dialog import OptimizeDialog

        OptimizeDialog(parent=self).exec()

    # -- design assistant ------------------------------------------------- #

    def _recommend_magnet(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from magnetflux.assistant.recommend import recommend_magnet

        temp, ok = QInputDialog.getDouble(self, "Recommend Magnet",
                                          "Operating temperature (C):", 20.0, -50, 500)
        if not ok:
            return
        rec = recommend_magnet(self._material_db, operating_temp=temp,
                               prefer="performance")
        alts = ", ".join(rec.alternatives) if rec.alternatives else "-"
        QMessageBox.information(
            self, "Recommended Magnet",
            f"Best: {rec.choice}\n\n{rec.rationale}\n\nAlternatives: {alts}",
        )

    def _recommend_solver(self) -> None:
        from magnetflux.assistant.recommend import recommend_solver
        from magnetflux.materials.material import MaterialType

        has_iron = any(
            self._material_db.has(a.material_id)
            and self._material_db.get(a.material_id).mtype is MaterialType.SOFT_MAGNETIC
            for _, a in self._assignments.items()
        )
        rec = recommend_solver(has_iron, len(self._project.model_tree))
        QMessageBox.information(self, "Recommended Solver",
                                f"Backend: {rec.choice}\n\n{rec.rationale}")

    def _diagnose_setup(self) -> None:
        from magnetflux.assistant.recommend import diagnose_setup

        issues = diagnose_setup(self._project.model_tree, self._material_db,
                                self._assignments)
        if not issues:
            QMessageBox.information(self, "Diagnose Setup",
                                    "No issues found - the model looks ready to solve.")
        else:
            QMessageBox.warning(self, "Diagnose Setup",
                                "\n".join(f"- {i}" for i in issues))

    def _full_report(self) -> None:
        """Assemble and render the comprehensive engineering PDF report."""
        from pathlib import Path as _Path

        from magnetflux.report.assemble import build_full_report
        from magnetflux.report.pdf import render_pdf
        from magnetflux.results.statistics import field_statistics
        from magnetflux.visualization.quantities import FieldQuantity, scalar_values

        # Components + materials.
        bodies = []
        for body in self._project.model_tree:
            a = self._assignments.get(body.id)
            mat_id = a.material_id if a else "-"
            br = 0.0
            direction = "-"
            if a and self._material_db.has(a.material_id):
                br = a.effective_remanence(self._material_db.get(a.material_id))
                if a.magnetization:
                    direction = str(tuple(round(v, 2) for v in a.magnetization.direction))
            bodies.append({"name": body.name, "material": mat_id,
                           "br": br, "direction": direction})

        # Field statistics per quantity.
        quantity_stats = {}
        if self._last_field is not None:
            for q in (FieldQuantity.BMAG, FieldQuantity.BZ, FieldQuantity.HMAG,
                      FieldQuantity.ENERGY):
                stats = field_statistics(scalar_values(self._last_field.result, q))
                quantity_stats[f"{q.value} [{q.unit}]"] = stats.as_dict()

        # Race track (best-effort) + heatmap image.
        racetrack_metrics: dict[str, str] = {}
        heatmap_path = None
        track = self._compute_race_track()
        if track is not None:
            from magnetflux.racetrack.erosion import eroded_area_fraction, uniformity
            from magnetflux.racetrack.heatmap import save_heatmap_png

            racetrack_metrics = {
                "Peak |B_t|": f"{track.b_tangential_mag.max() * 1e3:.1f} mT",
                "Uniformity": f"{uniformity(track):.2f}",
                "Eroded area fraction": f"{eroded_area_fraction(track):.2f}",
            }

        path, _ = QFileDialog.getSaveFileName(self, "Full Report", "", "PDF (*.pdf)")
        if not path:
            return
        if track is not None:
            heatmap_path = str(_Path(path).with_suffix(".png"))
            save_heatmap_png(track, heatmap_path, "Predicted race track")

        model = build_full_report(
            project_name=self._project.name or "Untitled",
            bodies=bodies,
            solver_info={"backend": self._solver.backend.name,
                         "components": len(bodies)},
            quantity_stats=quantity_stats,
            racetrack_metrics=racetrack_metrics,
            conclusions=[
                "Magnetostatic analysis completed with MagnetFlux Studio.",
                f"{len(bodies)} component(s) analysed.",
            ],
            heatmap_path=heatmap_path,
        )
        try:
            render_pdf(model, path)
        except Exception as exc:  # noqa: BLE001 - surfaced to user
            QMessageBox.critical(self, "Report failed", str(exc))
            return
        self.statusBar().showMessage(f"Saved {_Path(path).name}")

    # -- workspace / dashboard switching ---------------------------------- #

    def _workspace_docks(self):
        return (self._builder_dock, self._tree_dock, self._prop_dock,
                self._results_dock, self._log_dock)

    # -- results post-processing ------------------------------------------ #

    def _field_variables(self) -> dict:
        """Named arrays for custom expressions over the last solved field."""
        res = self._last_field.result
        import numpy as np

        pts = res.points
        h = res.h
        return {
            "Bx": res.bx, "By": res.by, "Bz": res.bz, "Bmag": res.b_magnitude,
            "Hx": h[:, 0], "Hy": h[:, 1], "Hz": h[:, 2],
            "Hmag": np.linalg.norm(h, axis=1),
            "x": pts[:, 0], "y": pts[:, 1], "z": pts[:, 2],
        }

    def _show_statistics(self) -> None:
        from magnetflux.results.statistics import field_statistics
        from magnetflux.visualization.quantities import scalar_values

        if self._last_field is None:
            QMessageBox.information(self, "Results", "Solve the field first.")
            return
        q = self._current_quantity()
        stats = field_statistics(scalar_values(self._last_field.result, q))
        self._results_panel.set_title(f"Statistics — {q.value} [{q.unit}]")
        self._results_panel.set_statistics(stats.as_dict())
        self._results_dock.raise_()

    def _evaluate_expression(self, expression: str) -> None:
        from magnetflux.results.expressions import evaluate_expression
        from magnetflux.results.statistics import field_statistics

        if self._last_field is None:
            QMessageBox.information(self, "Results", "Solve the field first.")
            return
        try:
            values = evaluate_expression(expression, self._field_variables())
        except Exception as exc:  # noqa: BLE001 - surfaced to user
            QMessageBox.warning(self, "Expression error", str(exc))
            return
        self._results_panel.set_title(f"Statistics — {expression}")
        self._results_panel.set_statistics(field_statistics(values).as_dict())

    def _show_dashboard(self) -> None:
        self._stack.setCurrentWidget(self._dashboard)
        for dock in self._workspace_docks():
            dock.hide()
        self._ribbon_toolbar.hide()

    def _enter_workspace(self) -> None:
        self._stack.setCurrentWidget(self._viewport)
        for dock in self._workspace_docks():
            dock.show()
        self._ribbon_toolbar.show()

    def _dashboard_new(self) -> None:
        self._new_project()
        self._enter_workspace()

    def _dashboard_open(self) -> None:
        self._enter_workspace()
        self._open_project_dialog()

    def _dashboard_import(self) -> None:
        self._enter_workspace()
        self._import_cad_dialog()

    def _toggle_theme(self) -> None:
        from PySide6.QtWidgets import QApplication

        from magnetflux.ui.theme import Theme, stylesheet

        self._dark = not getattr(self, "_dark", False)
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(stylesheet(Theme.DARK if self._dark else Theme.LIGHT))

    def _on_node_activated(self, key: str) -> None:
        """Map a Model Builder node to an action/dock."""
        if key == "geometry":
            self._tree_dock.raise_()
        elif key == "materials" or key.startswith("material"):
            self._prop_dock.raise_()
        elif key == "study":
            self._solve_field()
        elif key == "results.racetrack":
            self._predict_race_track()
        elif key == "export":
            self._export_csv()
        elif key.startswith("body."):
            try:
                self._on_body_selected(int(key.split(".", 1)[1]))
            except ValueError:
                pass

    # -- actions ---------------------------------------------------------- #

    def _new_project(self) -> None:
        self._project = Project()
        self._assignments = AssignmentTable()
        self._material_db = MaterialDatabase()
        self._refresh_views()
        self.statusBar().showMessage("New project")

    def _on_body_selected(self, body_id: int) -> None:
        self._selected_body_id = body_id
        self._property_panel.show_body(body_id)
        self._viewport.highlight_body(body_id)

    def _on_point_picked(self, point) -> None:
        x, y, z = point
        self.statusBar().showMessage(
            f"Picked point: ({x * 1000:.2f}, {y * 1000:.2f}, {z * 1000:.2f}) mm"
        )

    def _set_selection_mode(self, mode: str) -> None:
        self._viewport.set_selection_mode(mode)
        self.statusBar().showMessage(f"Selection mode: {mode}")

    def _set_all_visible(self, visible: bool) -> None:
        self._tree_widget.set_all_visible(visible)
        self.statusBar().showMessage("Show all" if visible else "Hide all")

    def _polar_array(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from magnetflux.geometry.pattern import polar_array

        body = self._selected_body()
        if body is None:
            return
        count, ok = QInputDialog.getInt(self, "Polar Array", "Number of copies:",
                                        6, 2, 64)
        if not ok:
            return
        copies = polar_array(body.mesh, axis=[0, 0, 1], center=[0, 0, 0], count=count)
        for i, mesh in enumerate(copies[1:], start=2):
            self._project.model_tree.add_body(mesh, name=f"{body.name} ({i})")
        self._refresh_views()
        self.statusBar().showMessage(f"Polar array: {count} copies")

    def _mirror_body(self) -> None:
        from magnetflux.geometry.transform import mirror_mesh

        body = self._selected_body()
        if body is None:
            return
        mirrored = mirror_mesh(body.mesh, plane_normal=[1, 0, 0])
        self._project.model_tree.add_body(mirrored, name=f"{body.name} (mirror)")
        self._refresh_views()
        self.statusBar().showMessage("Mirrored body added")

    def _selected_body(self):
        bid = getattr(self, "_selected_body_id", None)
        if bid is None:
            QMessageBox.information(self, "Geometry", "Select a body first.")
            return None
        try:
            return self._project.model_tree.get(bid)
        except KeyError:
            return None

    def _on_assignment_changed(self, body_id: int, assignment) -> None:
        # Keep the model tree's material_id in sync for colouring/queries.
        self._project.model_tree.assign_material(body_id, assignment.material_id)

    # -- solve & visualize ------------------------------------------------ #

    def _current_quantity(self) -> FieldQuantity:
        # Qt may return the str value for a str-enum; coerce back to the enum.
        return FieldQuantity(self._quantity_combo.currentData())

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

        try:
            Job(work, on_done=done, on_error=failed).run_sync()
        except Exception:  # noqa: BLE001 - already reported via on_error
            pass

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

    # -- race-track analysis ---------------------------------------------- #

    def _compute_race_track(self):
        """Solve on a target plane above the model and predict the race track."""
        from magnetflux.racetrack.erosion import compute_race_track
        from magnetflux.visualization.sampling import plane_points

        bbox = self._project.model_tree.bounding_box()
        if bbox is None:
            QMessageBox.information(self, "Race Track", "Import a model first.")
            return None
        size = bbox.size
        z_target = bbox.max_corner[2] + 0.1 * max(size[0], size[1])
        origin = [bbox.center[0], bbox.center[1], z_target]
        pts, dims = plane_points(origin, [1, 0, 0], [0, 1, 0],
                                 1.5 * size[0], 1.5 * size[1], 60, 60)
        problem = self._solver.build_problem(
            self._project.model_tree, self._material_db, self._assignments, pts
        )
        if not problem.magnet_sources:
            QMessageBox.information(self, "Race Track", "Assign magnet materials first.")
            return None
        result = self._solver.solve(problem)
        return compute_race_track(pts, result.b, dims, normal=[0, 0, 1])

    def _predict_race_track(self) -> None:
        from magnetflux.racetrack.heatmap import save_heatmap_png

        track = self._compute_race_track()
        if track is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Race-Track Heatmap", "", "PNG (*.png)"
        )
        if path:
            save_heatmap_png(track, path, "Predicted race track")
            self.statusBar().showMessage(f"Saved {Path(path).name}")

    def _generate_report(self) -> None:
        from magnetflux.racetrack.erosion import eroded_area_fraction, uniformity
        from magnetflux.racetrack.heatmap import save_heatmap_png
        from magnetflux.racetrack.report import ReportData, generate_pdf_report

        track = self._compute_race_track()
        if track is None:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "PDF (*.pdf)")
        if not path:
            return
        png = str(Path(path).with_suffix(".png"))
        save_heatmap_png(track, png, "Predicted race track")
        magnets = [
            f"{b.name}: {self._assignments.get(b.id).material_id}"
            for b in self._project.model_tree
            if self._assignments.get(b.id) is not None
        ]
        data = ReportData(
            project_name=self._project.name,
            metrics={
                "Peak |B_t|": f"{track.b_tangential_mag.max() * 1000:.1f} mT",
                "Uniformity": f"{uniformity(track):.2f}",
                "Eroded area fraction": f"{eroded_area_fraction(track):.2f}",
            },
            magnets=magnets,
            heatmap_png=png,
        )
        generate_pdf_report(data, path)
        self.statusBar().showMessage(f"Saved {Path(path).name}")

    # -- optimization ----------------------------------------------------- #

    def _optimize_spacing(self) -> None:
        from magnetflux.optimization.layout import ParametricLayout
        from magnetflux.optimization.optimize import optimize_spacing

        layout = ParametricLayout()
        self.statusBar().showMessage("Optimizing magnet spacing...")
        result = optimize_spacing(layout, bounds=(0.02, 0.08))
        QMessageBox.information(
            self, "Spacing Study",
            f"Best ring radius: {result.best_value * 1000:.1f} mm\n"
            f"Target utilisation: {result.best_score:.3f}\n"
            f"({len(result.history)} evaluations)",
        )
        self.statusBar().showMessage("Spacing study complete")

    def _optimize_poles(self) -> None:
        from magnetflux.optimization.layout import ParametricLayout
        from magnetflux.optimization.optimize import optimize_pole_arrangement

        layout = ParametricLayout()
        self.statusBar().showMessage("Optimizing pole count...")
        result = optimize_pole_arrangement(layout, ring_counts=[3, 4, 6, 8, 12])
        QMessageBox.information(
            self, "Pole Count Study",
            f"Best ring magnet count: {int(result.best_value)}\n"
            f"Target utilisation: {result.best_score:.3f}",
        )
        self.statusBar().showMessage("Pole count study complete")

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
            named = import_cad_named(path, source_unit=LengthUnit.MILLIMETER)
            progress.report(0.9, "Building bodies")
            return named

        def done(named) -> None:
            stem = path.stem
            for i, (comp_name, mesh) in enumerate(named):
                # Prefer the component/part name from the assembly; fall back to
                # the file stem (single solid) or an indexed name.
                if comp_name:
                    name = comp_name
                elif len(named) == 1:
                    name = stem
                else:
                    name = f"{stem} [{i + 1}]"
                self._project.model_tree.add_body(
                    mesh, name=name, source_file=str(path)
                )
            self._refresh_views()
            self.statusBar().showMessage(
                f"Imported {path.name}: {len(named)} component(s)"
            )

        def failed(exc: BaseException) -> None:
            log.error("Import failed: %s", exc)
            QMessageBox.critical(self, "Import failed", str(exc))
            self.statusBar().showMessage("Import failed")

        self._import_job = Job(work, on_done=done, on_error=failed)
        # Run synchronously for a small file; large assemblies could use start().
        # The error is surfaced by `failed`; swallow the re-raise so the global
        # crash handler doesn't also pop an "Unexpected error" dialog.
        try:
            self._import_job.run_sync()
        except Exception:  # noqa: BLE001 - already reported via on_error
            pass

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
        self._model_builder.refresh(self._project.model_tree)
        self._viewport.render_tree(self._project.model_tree)

    def closeEvent(self, event) -> None:  # noqa: N802 (Qt override)
        self._log_panel.detach()
        super().closeEvent(event)
