"""Report generator: assemble a report model and render it to PDF."""

from magnetflux.report.assemble import build_full_report
from magnetflux.report.model import ReportModel, ReportSection
from magnetflux.report.pdf import is_reportlab_available, render_pdf

__all__ = [
    "ReportModel",
    "ReportSection",
    "build_full_report",
    "render_pdf",
    "is_reportlab_available",
]
