"""Backend-agnostic magnetostatic solver interfaces (Milestone 0).

The application depends on these abstractions, never on a concrete FEM library.
Two backends implement :class:`SolverBackend` (Milestone 3):

* an **analytic** surface-charge / dipole superposition solver (no mesh,
  always available, used as the validation benchmark), and
* a **scikit-fem** solver using the magnetic **vector potential A**
  formulation with Nedelec edge elements.

Both return a :class:`FieldResult` sampling B (and derived quantities) at a
set of evaluation points, so the visualization layer is backend-independent.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np

from magnetflux.config import MU_0


@dataclass(slots=True)
class SolverProblem:
    """Definition of a magnetostatic problem, independent of the backend.

    Attributes:
        points: ``(N, 3)`` evaluation points [m] where the field is wanted.
        magnet_sources: List of magnet source descriptors. Each is a dict with
            keys understood by the backends, e.g. ``{"center", "magnetization",
            "dims", "shape"}`` (SI units; magnetization in A/m).
        air_padding: Air-domain padding factor (FEM backends).
        mesh_size: Characteristic element size [m] (FEM backends).
    """

    points: np.ndarray
    magnet_sources: list[dict] = field(default_factory=list)
    coils: list = field(default_factory=list)  # CoilSource objects (current sources)
    air_padding: float = 2.0
    mesh_size: float = 2.0e-3

    def __post_init__(self) -> None:
        self.points = np.asarray(self.points, dtype=float).reshape(-1, 3)


@dataclass(slots=True)
class FieldResult:
    """Magnetic field sampled at evaluation points.

    Attributes:
        points: ``(N, 3)`` evaluation points [m].
        b: ``(N, 3)`` magnetic flux density vectors [T].
        metadata: Free-form backend metadata (solver name, dof count, residual).
    """

    points: np.ndarray
    b: np.ndarray
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.points = np.asarray(self.points, dtype=float).reshape(-1, 3)
        self.b = np.asarray(self.b, dtype=float).reshape(-1, 3)
        if len(self.points) != len(self.b):
            raise ValueError("points and b must have the same length")

    @property
    def bx(self) -> np.ndarray:
        return self.b[:, 0]

    @property
    def by(self) -> np.ndarray:
        return self.b[:, 1]

    @property
    def bz(self) -> np.ndarray:
        return self.b[:, 2]

    @property
    def b_magnitude(self) -> np.ndarray:
        """``|B|`` at each point [T]."""
        return np.linalg.norm(self.b, axis=1)

    @property
    def h(self) -> np.ndarray:
        """Magnetic field H in free space (B/mu_0) [A/m].

        Valid in the air region; inside magnetic materials the backend should
        override this via metadata.
        """
        return self.b / MU_0

    def energy_density(self) -> np.ndarray:
        """Magnetic energy density ``|B|^2 / (2 mu_0)`` [J/m^3] (air)."""
        return self.b_magnitude**2 / (2.0 * MU_0)


class SolverBackend(ABC):
    """Interface every magnetostatic backend must implement."""

    #: Human-readable backend name.
    name: str = "abstract"

    @abstractmethod
    def is_available(self) -> bool:
        """Whether this backend's dependencies are importable."""

    @abstractmethod
    def solve(self, problem: SolverProblem, progress=None) -> FieldResult:
        """Solve ``problem`` and return the sampled field.

        Args:
            problem: The magnetostatic problem definition.
            progress: Optional :class:`~magnetflux.core.jobs.ProgressHandle`
                for progress reporting and cooperative cancellation.
        """
