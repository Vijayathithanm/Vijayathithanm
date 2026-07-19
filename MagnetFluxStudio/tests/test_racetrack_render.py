"""Guarded tests for optional heatmap (matplotlib) and report (reportlab)."""

import numpy as np
import pytest

from magnetflux.racetrack.erosion import compute_race_track
from magnetflux.racetrack.heatmap import is_matplotlib_available, save_heatmap_png
from magnetflux.racetrack.report import (
    ReportData,
    generate_pdf_report,
    is_reportlab_available,
)


def _track():
    # 10x10 plane with a sign-changing normal component -> a race track.
    nu = nv = 10
    xs = np.linspace(-1, 1, nu)
    ys = np.linspace(-1, 1, nv)
    xx, yy = np.meshgrid(xs, ys, indexing="ij")
    r = np.sqrt(xx**2 + yy**2).ravel()
    b = np.zeros((nu * nv, 3))
    b[:, 0] = np.maximum(0, 1 - np.abs(r - 0.5))  # tangential band at r=0.5
    b[:, 2] = (r - 0.5)                            # normal crosses zero at r=0.5
    pts = np.column_stack([xx.ravel(), yy.ravel(), np.zeros(nu * nv)])
    return compute_race_track(pts, b, (nu, nv, 1), normal=[0, 0, 1])


@pytest.mark.skipif(not is_matplotlib_available(), reason="matplotlib not installed")
def test_save_heatmap_png(tmp_path):
    path = save_heatmap_png(_track(), tmp_path / "hm.png")
    assert path.exists() and path.stat().st_size > 0


@pytest.mark.skipif(not is_reportlab_available(), reason="reportlab not installed")
def test_generate_pdf_report(tmp_path):
    data = ReportData(
        project_name="Test",
        metrics={"Peak |B_t|": "129 mT", "Uniformity": "0.48"},
        magnets=["Center: N42"],
    )
    path = generate_pdf_report(data, tmp_path / "r.pdf")
    assert path.exists() and path.read_bytes()[:4] == b"%PDF"
