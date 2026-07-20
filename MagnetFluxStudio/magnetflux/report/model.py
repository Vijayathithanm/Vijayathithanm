"""Report data model (Milestone: Report Generator).

Backend-agnostic description of an engineering report: an ordered list of
sections, each with paragraphs, an optional table and an optional image. The
PDF renderer consumes this, so report *content* is assembled and unit-tested
without any PDF dependency.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ReportSection:
    """One section of a report.

    Attributes:
        title: Section heading.
        paragraphs: Body text paragraphs.
        table_headers: Optional column headers.
        table_rows: Optional rows (each a list of cell strings).
        image_path: Optional path to an image to embed after the text.
    """

    title: str
    paragraphs: list[str] = field(default_factory=list)
    table_headers: list[str] | None = None
    table_rows: list[list[str]] | None = None
    image_path: str | None = None

    @property
    def has_table(self) -> bool:
        return bool(self.table_headers and self.table_rows)


@dataclass(slots=True)
class ReportModel:
    """A complete report: title, subtitle and ordered sections."""

    title: str
    subtitle: str
    sections: list[ReportSection] = field(default_factory=list)
