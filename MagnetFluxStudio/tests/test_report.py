"""Tests for the report generator: content assembly + PDF rendering."""

import pytest

from magnetflux.report.assemble import build_full_report, geometry_section
from magnetflux.report.pdf import is_reportlab_available, render_pdf


def _sample_report():
    return build_full_report(
        project_name="Cathode A",
        bodies=[{"name": "Inner Magnet", "material": "N42", "br": 1.30,
                 "direction": "(0, 0, 1)"}],
        solver_info={"backend": "analytic-charge", "air_padding": 2.0},
        quantity_stats={"|B|": {"min": 0.0, "max": 0.5, "mean": 0.2, "rms": 0.25}},
        racetrack_metrics={"Pole balance": "0.92", "Working distance": "12 mm"},
        conclusions=["Balanced design.", "Race track is closed."],
    )


def test_geometry_section_table():
    sec = geometry_section([{"name": "M1", "material": "N52", "br": 1.44,
                             "direction": "(1,0,0)"}])
    assert sec.has_table
    assert sec.table_rows[0][0] == "M1"
    assert "N52" in sec.table_rows[0]


def test_build_full_report_sections():
    model = build_full_report(
        "P", [], {}, {}, {}, [],
    )
    titles = [s.title for s in model.sections]
    assert titles[0].startswith("1.")
    assert any("Race-Track" in t for t in titles)
    assert any("Conclusions" in t for t in titles)
    assert len(model.sections) == 6


def test_full_report_has_content():
    model = _sample_report()
    assert model.subtitle == "Cathode A"
    geom = next(s for s in model.sections if "Geometry" in s.title)
    assert geom.table_rows[0][0] == "Inner Magnet"


@pytest.mark.skipif(not is_reportlab_available(), reason="reportlab not installed")
def test_render_pdf(tmp_path):
    path = render_pdf(_sample_report(), tmp_path / "report.pdf")
    assert path.exists()
    assert path.read_bytes()[:4] == b"%PDF"
    assert path.stat().st_size > 1000
