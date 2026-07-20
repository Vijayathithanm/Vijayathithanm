"""Assemble a :class:`ReportModel` from simulation data (Report Generator).

Pure data assembly (no PDF dependency) so report content is unit-testable.
Each ``*_section`` builds one section; :func:`build_full_report` composes the
standard engineering report a magnetron designer expects.
"""

from __future__ import annotations

from datetime import date

from magnetflux.report.model import ReportModel, ReportSection


def project_section(project_name: str, when: str | None = None) -> ReportSection:
    return ReportSection(
        title="1. Project Details",
        paragraphs=[
            f"Project: {project_name}",
            f"Date: {when or date.today().isoformat()}",
            "Analysis: Magnetostatic (permanent-magnet magnetron cathode).",
            "Tool: MagnetFlux Studio.",
        ],
    )


def geometry_section(bodies: list[dict]) -> ReportSection:
    rows = [[b.get("name", "?"), b.get("material", "-"),
             f"{b.get('br', 0.0):.3f}", b.get("direction", "-")] for b in bodies]
    return ReportSection(
        title="2. Geometry & Materials",
        paragraphs=[f"The model contains {len(bodies)} component(s)."],
        table_headers=["Component", "Material", "Br [T]", "North direction"],
        table_rows=rows or [["(none)", "-", "-", "-"]],
    )


def solver_section(solver_info: dict) -> ReportSection:
    rows = [[k, str(v)] for k, v in solver_info.items()]
    return ReportSection(
        title="3. Solver Settings",
        paragraphs=["Magnetostatic solve of B = curl A on the air domain."],
        table_headers=["Setting", "Value"],
        table_rows=rows or [["backend", "analytic"]],
    )


def results_section(quantity_stats: dict[str, dict[str, float]]) -> ReportSection:
    rows = []
    for name, stats in quantity_stats.items():
        rows.append([
            name,
            f"{stats.get('min', 0):.4g}", f"{stats.get('max', 0):.4g}",
            f"{stats.get('mean', 0):.4g}", f"{stats.get('rms', 0):.4g}",
        ])
    return ReportSection(
        title="4. Results — Field Statistics",
        paragraphs=["Summary statistics of the computed magnetic field."],
        table_headers=["Quantity", "min", "max", "mean", "rms"],
        table_rows=rows or [["|B|", "-", "-", "-", "-"]],
    )


def racetrack_section(metrics: dict[str, str], image_path: str | None = None) -> ReportSection:
    return ReportSection(
        title="5. Race-Track Prediction",
        paragraphs=["Predicted erosion race track and magnetron balance metrics."],
        table_headers=["Metric", "Value"],
        table_rows=[[k, v] for k, v in metrics.items()] or [["-", "-"]],
        image_path=image_path,
    )


def conclusions_section(points: list[str]) -> ReportSection:
    return ReportSection(
        title="6. Conclusions",
        paragraphs=points or ["Analysis complete."],
    )


def build_full_report(
    project_name: str,
    bodies: list[dict],
    solver_info: dict,
    quantity_stats: dict[str, dict[str, float]],
    racetrack_metrics: dict[str, str],
    conclusions: list[str],
    heatmap_path: str | None = None,
) -> ReportModel:
    """Compose the standard multi-section engineering report."""
    return ReportModel(
        title="Magnetron Cathode — Magnetic Analysis Report",
        subtitle=project_name,
        sections=[
            project_section(project_name),
            geometry_section(bodies),
            solver_section(solver_info),
            results_section(quantity_stats),
            racetrack_section(racetrack_metrics, heatmap_path),
            conclusions_section(conclusions),
        ],
    )
