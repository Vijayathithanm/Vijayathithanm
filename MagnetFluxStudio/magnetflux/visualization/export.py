"""Field export: CSV and VTK (Milestone 4).

CSV and legacy-VTK writers are dependency-free (openable in Excel/ParaView).
PNG export of the rendered scene lives with the PyVista visualizer, which needs
the GUI extras. VTK is written as a ``STRUCTURED_GRID`` when grid dimensions are
supplied (so ParaView can slice/streamline it), otherwise as a ``POLYDATA``
point cloud.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from magnetflux.solver.base import FieldResult


def export_csv(path: str | Path, result: FieldResult) -> Path:
    """Write points and field components to CSV (x,y,z,Bx,By,Bz,|B|)."""
    path = Path(path)
    bmag = result.b_magnitude
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["x", "y", "z", "Bx", "By", "Bz", "|B|"])
        for p, b, mag in zip(result.points, result.b, bmag):
            writer.writerow([p[0], p[1], p[2], b[0], b[1], b[2], mag])
    return path


def _reorder_to_vtk(arr: np.ndarray, dims: tuple[int, int, int]) -> np.ndarray:
    """Reorder a C-ordered (nx,ny,nz,...) array to VTK's x-fastest ordering."""
    nx, ny, nz = dims
    shape = (nx, ny, nz) + arr.shape[1:]
    a = arr.reshape(shape)
    axes = (2, 1, 0) + tuple(range(3, a.ndim))
    return np.transpose(a, axes).reshape((nx * ny * nz,) + arr.shape[1:])


def export_vtk(
    path: str | Path,
    result: FieldResult,
    dims: tuple[int, int, int] | None = None,
) -> Path:
    """Write the field to a legacy ASCII VTK file.

    Args:
        path: Output path (``.vtk``).
        result: The solved field.
        dims: ``(nx, ny, nz)`` grid dimensions for a ``STRUCTURED_GRID`` export.
            If ``None`` (or a slice with a unit dim), a ``POLYDATA`` point cloud
            is written instead.
    """
    path = Path(path)
    pts = result.points
    b = result.b
    bmag = result.b_magnitude

    structured = dims is not None and all(d >= 1 for d in dims) and np.prod(dims) == len(pts)
    lines = ["# vtk DataFile Version 3.0", "MagnetFlux Studio field", "ASCII"]

    if structured:
        pts_o = _reorder_to_vtk(pts, dims)
        b_o = _reorder_to_vtk(b, dims)
        bmag_o = _reorder_to_vtk(bmag, dims)
        lines.append("DATASET STRUCTURED_GRID")
        lines.append(f"DIMENSIONS {dims[0]} {dims[1]} {dims[2]}")
        lines.append(f"POINTS {len(pts_o)} float")
        lines += [f"{p[0]} {p[1]} {p[2]}" for p in pts_o]
        lines.append(f"POINT_DATA {len(pts_o)}")
        lines.append("VECTORS B float")
        lines += [f"{v[0]} {v[1]} {v[2]}" for v in b_o]
        lines.append("SCALARS Bmag float 1")
        lines.append("LOOKUP_TABLE default")
        lines += [f"{m}" for m in bmag_o]
    else:
        n = len(pts)
        lines.append("DATASET POLYDATA")
        lines.append(f"POINTS {n} float")
        lines += [f"{p[0]} {p[1]} {p[2]}" for p in pts]
        lines.append(f"VERTICES {n} {2 * n}")
        lines += [f"1 {i}" for i in range(n)]
        lines.append(f"POINT_DATA {n}")
        lines.append("VECTORS B float")
        lines += [f"{v[0]} {v[1]} {v[2]}" for v in b]
        lines.append("SCALARS Bmag float 1")
        lines.append("LOOKUP_TABLE default")
        lines += [f"{m}" for m in bmag]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
