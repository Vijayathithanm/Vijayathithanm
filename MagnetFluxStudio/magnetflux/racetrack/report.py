"""PDF report generation for a race-track analysis (Milestone 5).

Assembles a one-page summary -- project metadata, magnet/material summary, key
field metrics and the predicted race-track heatmap -- into a PDF. Uses reportlab
(optional ``report`` extras); guarded by :func:`is_reportlab_available`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


def is_reportlab_available() -> bool:
    try:
        import reportlab  # noqa: F401
        return True
    except ImportError:
        return False


@dataclass(slots=True)
class ReportData:
    """Content for a race-track report.

    Attributes:
        project_name: Project title.
        metrics: Ordered ``label -> value`` rows (peak |B|, uniformity, ...).
        magnets: Human-readable magnet/material summary lines.
        heatmap_png: Optional path to a rendered heatmap image to embed.
    """

    project_name: str
    metrics: dict[str, str] = field(default_factory=dict)
    magnets: list[str] = field(default_factory=list)
    heatmap_png: str | None = None


def generate_pdf_report(data: ReportData, path: str | Path) -> Path:
    """Write a PDF report to ``path``.

    Raises:
        RuntimeError: If reportlab is not installed.
    """
    if not is_reportlab_available():
        raise RuntimeError("PDF report requires reportlab (install .[report])")

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas

    path = Path(path)
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    y = height - 25 * mm

    c.setFont("Helvetica-Bold", 18)
    c.drawString(20 * mm, y, "MagnetFlux Studio — Race-Track Report")
    y -= 10 * mm
    c.setFont("Helvetica", 12)
    c.drawString(20 * mm, y, f"Project: {data.project_name}")
    y -= 12 * mm

    c.setFont("Helvetica-Bold", 13)
    c.drawString(20 * mm, y, "Field metrics")
    y -= 7 * mm
    c.setFont("Helvetica", 11)
    for label, value in data.metrics.items():
        c.drawString(25 * mm, y, f"{label}: {value}")
        y -= 6 * mm

    y -= 4 * mm
    c.setFont("Helvetica-Bold", 13)
    c.drawString(20 * mm, y, "Magnets & materials")
    y -= 7 * mm
    c.setFont("Helvetica", 11)
    for line in data.magnets:
        c.drawString(25 * mm, y, line)
        y -= 6 * mm

    if data.heatmap_png and Path(data.heatmap_png).exists():
        img_h = 90 * mm
        c.drawImage(data.heatmap_png, 20 * mm, max(20 * mm, y - img_h),
                    width=110 * mm, height=img_h, preserveAspectRatio=True)

    c.showPage()
    c.save()
    return path
