"""PDF rendering of a :class:`ReportModel` (Report Generator).

Uses reportlab's Platypus for a professional multi-section layout (title,
headings, paragraphs, tables, embedded plots). Optional dependency, guarded by
:func:`is_reportlab_available`.
"""

from __future__ import annotations

from pathlib import Path

from magnetflux.report.model import ReportModel


def is_reportlab_available() -> bool:
    try:
        import reportlab  # noqa: F401
        return True
    except ImportError:
        return False


def render_pdf(model: ReportModel, path: str | Path) -> Path:
    """Render ``model`` to a PDF at ``path``.

    Raises:
        RuntimeError: If reportlab is not installed.
    """
    if not is_reportlab_available():
        raise RuntimeError("PDF report requires reportlab (install .[report])")

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        Image,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    path = Path(path)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(model.title, styles["Title"]),
        Paragraph(model.subtitle, styles["Heading2"]),
        Spacer(1, 8 * mm),
    ]

    table_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f6fdb")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c0c8d4")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#eef2f8")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ])

    for section in model.sections:
        story.append(Paragraph(section.title, styles["Heading2"]))
        for para in section.paragraphs:
            story.append(Paragraph(para, styles["BodyText"]))
        if section.has_table:
            data = [section.table_headers, *section.table_rows]
            table = Table(data, hAlign="LEFT")
            table.setStyle(table_style)
            story.append(Spacer(1, 3 * mm))
            story.append(table)
        if section.image_path and Path(section.image_path).exists():
            story.append(Spacer(1, 3 * mm))
            story.append(Image(section.image_path, width=120 * mm, height=95 * mm,
                               kind="proportional"))
        story.append(Spacer(1, 6 * mm))

    SimpleDocTemplate(str(path), pagesize=A4).build(story)
    return path
