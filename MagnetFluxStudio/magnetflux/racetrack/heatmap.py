"""Race-track heatmap rendering (Milestone 5).

Turns a :class:`RaceTrackResult` into a 2D erosion-intensity image. The array
form is dependency-free; PNG rendering uses matplotlib (optional ``report``
extras) and overlays the predicted race-track (``B_n = 0``) locus.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from magnetflux.racetrack.erosion import RaceTrackResult


def is_matplotlib_available() -> bool:
    try:
        import matplotlib  # noqa: F401
        return True
    except ImportError:
        return False


def heatmap_array(result: RaceTrackResult) -> np.ndarray:
    """Return the ``(nu, nv)`` normalised erosion-intensity grid."""
    return result.intensity_grid()


def save_heatmap_png(
    result: RaceTrackResult, path: str | Path, title: str = "Predicted race track"
) -> Path:
    """Render the erosion heatmap (with the B_n=0 race-track contour) to PNG.

    Raises:
        RuntimeError: If matplotlib is not installed.
    """
    if not is_matplotlib_available():
        raise RuntimeError("PNG heatmap requires matplotlib (install .[report])")

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    nu, nv, _ = result.dims
    intensity = result.intensity_grid()
    b_n = result.b_normal.reshape(nu, nv)

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(intensity.T, origin="lower", cmap="inferno", aspect="equal")
    # Race-track locus = zero-crossing of the normal component.
    ax.contour(b_n.T, levels=[0.0], colors="cyan", linewidths=1.0)
    ax.set_title(title)
    ax.set_xlabel("u")
    ax.set_ylabel("v")
    fig.colorbar(im, ax=ax, label="Erosion intensity (norm.)")
    fig.tight_layout()
    path = Path(path)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
