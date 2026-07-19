"""Analytic magnetostatic backend: magnetic surface-charge superposition.

A uniformly magnetised body carries no volume magnetic charge (``rho_m =
-div M = 0``) and a surface charge ``sigma_m = M . n``. The field outside the
body is then the Coulomb-like superposition

    H(p) = 1/(4 pi) * sum_k q_k (p - r_k) / |p - r_k|^3 ,   B = mu_0 H ,

where ``q_k = sigma_m dA_k`` are discretised surface charges. This is exact in
the fine-discretisation limit, needs no mesh, and reproduces the closed-form
on-axis field of a cylinder -- making it both a production solver for
permanent-magnet-in-air problems (the magnetron case) and the validation
benchmark for the FEM backend.

Field points are assumed to lie outside the magnet volume (where ``B = mu_0 H``);
this is exactly the race-track evaluation region above the target.
"""

from __future__ import annotations

import numpy as np

from magnetflux.config import MU_0
from magnetflux.solver.base import FieldResult, SolverBackend, SolverProblem

_FOUR_PI = 4.0 * np.pi


def closed_form_cylinder_axial_bz(
    z: np.ndarray | float, radius: float, length: float, magnetization: float
) -> np.ndarray | float:
    """On-axis axial flux density of a uniformly axially magnetised cylinder.

    Closed-form benchmark (SI):

        Bz(z) = mu_0 M / 2 * [ (z+L/2)/sqrt(R^2+(z+L/2)^2)
                               - (z-L/2)/sqrt(R^2+(z-L/2)^2) ]

    Args:
        z: Axial coordinate(s) measured from the cylinder centre [m].
        radius: Cylinder radius R [m].
        length: Cylinder length L [m].
        magnetization: Magnetisation magnitude M [A/m].
    """
    z = np.asarray(z, dtype=float)
    zp = z + length / 2.0
    zm = z - length / 2.0
    term = zp / np.sqrt(radius**2 + zp**2) - zm / np.sqrt(radius**2 + zm**2)
    return MU_0 * magnetization / 2.0 * term


def _orthonormal_frame(axis: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return an orthonormal frame (e1, e2, axis_hat) with axis_hat along axis."""
    a = axis / np.linalg.norm(axis)
    ref = np.array([1.0, 0.0, 0.0]) if abs(a[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    e1 = ref - np.dot(ref, a) * a
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(a, e1)
    return e1, e2, a


def _box_charges(
    center: np.ndarray, dims: np.ndarray, m: np.ndarray, n: int
) -> tuple[np.ndarray, np.ndarray]:
    """Discretised surface charges (positions, q) for a uniformly magnetised box.

    ``dims`` are full side lengths (lx, ly, lz); the box is axis-aligned.
    """
    positions: list[np.ndarray] = []
    charges: list[np.ndarray] = []
    half = dims / 2.0
    # Each of the 3 axes contributes two faces with normals +/- e_axis.
    for ax in range(3):
        sigma = m[ax]  # M . n where n = +e_ax on the +face
        if abs(sigma) < 1e-12:
            continue
        u, v = [k for k in range(3) if k != ax]
        us = (np.arange(n) + 0.5) / n * dims[u] - half[u]
        vs = (np.arange(n) + 0.5) / n * dims[v] - half[v]
        uu, vv = np.meshgrid(us, vs, indexing="ij")
        dA = (dims[u] / n) * (dims[v] / n)
        for sign in (+1.0, -1.0):
            pts = np.zeros((uu.size, 3))
            pts[:, u] = uu.ravel()
            pts[:, v] = vv.ravel()
            pts[:, ax] = sign * half[ax]
            positions.append(pts + center)
            charges.append(np.full(uu.size, sign * sigma * dA))
    if not positions:
        return np.zeros((0, 3)), np.zeros(0)
    return np.vstack(positions), np.concatenate(charges)


def _cylinder_charges(
    center: np.ndarray, axis: np.ndarray, radius: float, length: float,
    m: np.ndarray, nr: int, nt: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Surface charges for a uniformly magnetised cylinder (end caps + lateral)."""
    e1, e2, a = _orthonormal_frame(np.asarray(axis, dtype=float))
    m_axial = float(np.dot(m, a))
    positions: list[np.ndarray] = []
    charges: list[np.ndarray] = []

    # End caps: sigma = +/- M_axial, discretised on a polar grid (annular rings).
    if abs(m_axial) > 1e-12:
        r_edges = np.linspace(0.0, radius, nr + 1)
        r_mid = 0.5 * (r_edges[:-1] + r_edges[1:])
        ring_area = np.pi * (r_edges[1:] ** 2 - r_edges[:-1] ** 2) / nt
        thetas = (np.arange(nt) + 0.5) / nt * 2 * np.pi
        for sign in (+1.0, -1.0):
            for ri, rm in enumerate(r_mid):
                pts = (
                    center
                    + sign * (length / 2.0) * a
                    + rm * (np.cos(thetas)[:, None] * e1 + np.sin(thetas)[:, None] * e2)
                )
                positions.append(pts)
                charges.append(np.full(nt, sign * m_axial * ring_area[ri]))

    # Lateral surface: sigma = M . n_radial (nonzero for transverse magnetisation).
    m_perp = m - m_axial * a
    if np.linalg.norm(m_perp) > 1e-12:
        nz = max(nr, 4)
        zs = (np.arange(nz) + 0.5) / nz * length - length / 2.0
        thetas = (np.arange(nt) + 0.5) / nt * 2 * np.pi
        dA = (length / nz) * (2 * np.pi * radius / nt)
        for z in zs:
            n_rad = np.cos(thetas)[:, None] * e1 + np.sin(thetas)[:, None] * e2
            pts = center + z * a + radius * n_rad
            sigma = n_rad @ m_perp
            positions.append(pts)
            charges.append(sigma * dA)

    if not positions:
        return np.zeros((0, 3)), np.zeros(0)
    return np.vstack(positions), np.concatenate(charges)


class AnalyticBackend(SolverBackend):
    """Surface-charge superposition solver (no mesh required)."""

    name = "analytic-charge"

    def __init__(self, box_res: int = 24, cyl_nr: int = 24, cyl_nt: int = 64) -> None:
        self._box_res = box_res
        self._cyl_nr = cyl_nr
        self._cyl_nt = cyl_nt

    def is_available(self) -> bool:
        return True  # depends only on NumPy

    def _charges_for(self, source: dict) -> tuple[np.ndarray, np.ndarray]:
        center = np.asarray(source["center"], dtype=float).reshape(3)
        m = np.asarray(source["magnetization"], dtype=float).reshape(3)
        shape = source.get("shape", "box")
        if shape == "cylinder":
            return _cylinder_charges(
                center, np.asarray(source["axis"], dtype=float),
                float(source["dims"][0]), float(source["dims"][1]),
                m, self._cyl_nr, self._cyl_nt,
            )
        return _box_charges(center, np.asarray(source["dims"], dtype=float),
                            m, self._box_res)

    def solve(self, problem: SolverProblem, progress=None) -> FieldResult:
        pts = problem.points
        h = np.zeros_like(pts)
        n_src = max(len(problem.magnet_sources), 1)
        for i, source in enumerate(problem.magnet_sources):
            positions, q = self._charges_for(source)
            if len(q):
                # Vectorised Coulomb sum, chunked over charges to bound memory.
                for start in range(0, len(q), 2000):
                    pc = positions[start:start + 2000]
                    qc = q[start:start + 2000]
                    diff = pts[:, None, :] - pc[None, :, :]      # (N, C, 3)
                    dist = np.linalg.norm(diff, axis=2)          # (N, C)
                    inv = np.where(dist > 1e-12, dist**-3, 0.0)
                    weight = qc[None, :] * inv                   # (N, C)
                    h += np.einsum("nc,nck->nk", weight, diff) / _FOUR_PI
            if progress is not None:
                progress.report((i + 1) / n_src, f"magnet {i + 1}/{n_src}")
        b = MU_0 * h
        return FieldResult(pts, b, metadata={"backend": self.name,
                                             "n_sources": len(problem.magnet_sources)})
