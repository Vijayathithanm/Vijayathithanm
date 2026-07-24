"""Scene export: OBJ, interactive 3D-HTML and MP4 turntable (Milestone: Export).

The OBJ writer and the turntable camera path are dependency-free and testable.
The 3D-HTML and MP4 exporters render a live PyVista scene, so they need the GUI
extras and are imported lazily.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from magnetflux.core.model_tree import ModelTree


def export_obj(tree: ModelTree, path: str | Path) -> Path:
    """Write the model tree to a Wavefront OBJ (one group per body).

    OBJ is widely readable (web viewers, CAD, Blender). Faces are 1-indexed and
    offset per body; each body becomes a named group ``g <name>``.
    """
    path = Path(path)
    lines: list[str] = ["# MagnetFlux Studio scene export"]
    vertex_offset = 1  # OBJ indices are 1-based
    for body in tree:
        safe = body.name.replace(" ", "_")
        lines.append(f"g {safe}")
        for v in body.mesh.vertices:
            lines.append(f"v {v[0]:.6g} {v[1]:.6g} {v[2]:.6g}")
        for f in body.mesh.faces:
            a, b, c = (int(i) + vertex_offset for i in f)
            lines.append(f"f {a} {b} {c}")
        vertex_offset += body.mesh.n_vertices
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def turntable_azimuths(n_frames: int) -> np.ndarray:
    """Evenly spaced azimuth angles [deg] for a 360-degree turntable."""
    if n_frames < 1:
        raise ValueError("n_frames must be >= 1")
    return np.linspace(0.0, 360.0, n_frames, endpoint=False)


# -- rendering exporters (optional, need the GUI extras) --------------------- #

def export_html(plotter, path: str | Path) -> Path:
    """Export the current PyVista scene to a self-contained interactive HTML."""
    path = Path(path)
    plotter.export_html(str(path))
    return path


def export_turntable_mp4(plotter, path: str | Path, n_frames: int = 72,
                         framerate: int = 24) -> Path:
    """Render a 360-degree turntable MP4 of the current scene.

    Raises:
        RuntimeError: If the movie writer (imageio-ffmpeg) is unavailable.
    """
    path = Path(path)
    try:
        plotter.open_movie(str(path), framerate=framerate)
        for _ in range(n_frames):
            plotter.camera.azimuth += 360.0 / n_frames
            plotter.write_frame()
        plotter.close()
    except Exception as exc:  # pragma: no cover - depends on ffmpeg backend
        raise RuntimeError(f"MP4 export failed (needs imageio-ffmpeg): {exc}") from exc
    return path
