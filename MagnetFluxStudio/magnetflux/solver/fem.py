"""scikit-fem magnetostatic backend: vector potential A, Coulomb gauge.

Solves the linear magnetostatic problem for permanent magnets in air using the
**magnetic vector potential A**. In the Coulomb gauge with constant
permeability ``mu_0`` the three Cartesian components decouple into vector
Poisson equations whose source is the magnetisation curl:

    laplacian(A_i) = -mu_0 (curl M)_i .

Integrating the source by parts gives a load that uses ``M`` directly (its
surface-current ``M x n`` appears naturally at the magnet boundary):

    integral( grad(A_i) . grad(v) ) = mu_0 integral( M . (grad(v) x e_i) ) .

This uses ordinary nodal (P1) elements -- no edge elements or explicit gauging
-- which keeps it robust and Windows-packageable, while remaining a genuine
vector-potential A formulation. ``B = curl A`` is recovered per element.

The outer boundary uses the magnetic-insulation condition ``A = 0`` (far field).
A structured tetrahedral air domain is generated internally; the optional Gmsh
mesher (:mod:`magnetflux.solver.meshing`) can supply conforming meshes later.
"""

from __future__ import annotations

import numpy as np

from magnetflux.config import MU_0
from magnetflux.core.geometry import BoundingBox
from magnetflux.solver.air_domain import generate_air_domain
from magnetflux.solver.base import FieldResult, SolverBackend, SolverProblem


def is_skfem_available() -> bool:
    """Whether scikit-fem is importable."""
    try:
        import skfem  # noqa: F401
        return True
    except ImportError:
        return False


class ScikitFemBackend(SolverBackend):
    """Vector-potential (Coulomb-gauge) FEM solver on a structured tet mesh."""

    name = "scikit-fem-A"

    def __init__(self, resolution: int = 24) -> None:
        """Args: resolution -- cells per axis of the structured air domain."""
        self._resolution = resolution

    def is_available(self) -> bool:
        return is_skfem_available()

    def _build_mesh(self, domain: BoundingBox):
        import skfem

        n = self._resolution
        xs = np.linspace(domain.min_corner[0], domain.max_corner[0], n + 1)
        ys = np.linspace(domain.min_corner[1], domain.max_corner[1], n + 1)
        zs = np.linspace(domain.min_corner[2], domain.max_corner[2], n + 1)
        return skfem.MeshTet.init_tensor(xs, ys, zs)

    def solve(self, problem: SolverProblem, progress=None) -> FieldResult:
        import skfem
        from skfem import Basis, ElementTetP1, LinearForm
        from skfem.models.poisson import laplace
        from scipy.spatial import cKDTree

        if not problem.magnet_sources:
            return FieldResult(problem.points, np.zeros_like(problem.points),
                               metadata={"backend": self.name, "empty": True})

        # Air domain from the magnets' combined extent.
        boxes = [
            BoundingBox(np.asarray(s["center"]) - np.asarray(s["dims"]) / 2,
                        np.asarray(s["center"]) + np.asarray(s["dims"]) / 2)
            for s in problem.magnet_sources
        ]
        domain = generate_air_domain(BoundingBox.union(boxes), problem.air_padding)
        if progress:
            progress.report(0.1, "meshing air domain")
        mesh = self._build_mesh(domain)

        basis = Basis(mesh, ElementTetP1())
        centroids = mesh.p[:, mesh.t].mean(axis=1).T          # (n_elem, 3)
        sources = problem.magnet_sources

        def m_at(x: np.ndarray) -> np.ndarray:
            """Piecewise-constant M [A/m] at quadrature coords ``x`` (3, nqp, nelem)."""
            m = np.zeros_like(x)
            for src in sources:
                c = np.asarray(src["center"], dtype=float).reshape(3, 1, 1)
                half = (np.asarray(src["dims"], dtype=float) / 2).reshape(3, 1, 1)
                mvec = np.asarray(src["magnetization"], dtype=float).reshape(3, 1, 1)
                inside = np.all(np.abs(x - c) <= half, axis=0)   # (nqp, nelem)
                m += mvec * inside[None, :, :]
            return m

        # Load forms: mu0 * M . (grad v x e_i)  (see module docstring).
        @LinearForm
        def load_x(v, w):
            m = m_at(w.x)
            return MU_0 * (m[1] * v.grad[2] - m[2] * v.grad[1])

        @LinearForm
        def load_y(v, w):
            m = m_at(w.x)
            return MU_0 * (-m[0] * v.grad[2] + m[2] * v.grad[0])

        @LinearForm
        def load_z(v, w):
            m = m_at(w.x)
            return MU_0 * (m[0] * v.grad[1] - m[1] * v.grad[0])

        if progress:
            progress.report(0.4, "assembling system")
        K = laplace.assemble(basis)
        loads = [load_x.assemble(basis),
                 load_y.assemble(basis),
                 load_z.assemble(basis)]

        boundary = basis.get_dofs()  # all outer-boundary DOFs (A = 0)
        a_components = []
        for i, b in enumerate(loads):
            A_i = skfem.solve(*skfem.condense(K, b, D=boundary))
            a_components.append(A_i)
            if progress:
                progress.report(0.5 + 0.15 * (i + 1), f"solved component {i + 1}/3")

        # B = curl A, evaluated per element from P1 nodal gradients.
        b_field = self._curl_per_element(basis, a_components)

        # Sample element-constant B at the requested points via nearest centroid.
        tree = cKDTree(centroids)
        _, idx = tree.query(problem.points)
        b_at_points = b_field[idx]
        if progress:
            progress.report(1.0, "done")
        return FieldResult(
            problem.points, b_at_points,
            metadata={"backend": self.name, "n_dofs": basis.N,
                      "n_elements": mesh.t.shape[1]},
        )

    @staticmethod
    def _curl_per_element(basis, a_components: list[np.ndarray]) -> np.ndarray:
        """Return ``(n_elem, 3)`` B = curl A from nodal P1 components."""
        # Gradient of each component at the (single) P1 quadrature point.
        grads = []
        for A_i in a_components:
            gi = basis.interpolate(A_i).grad          # (3, n_elem, nqp)
            grads.append(gi.mean(axis=2))             # (3, n_elem)
        gAx, gAy, gAz = grads                          # each (3, n_elem)
        bx = gAz[1] - gAy[2]
        by = gAx[2] - gAz[0]
        bz = gAy[0] - gAx[1]
        return np.column_stack([bx, by, bz])
