"""Application-wide configuration and physical constants.

No third-party dependencies here so it can be imported from any layer without
pulling in NumPy, Qt or a solver backend.

Unit policy (see :mod:`magnetflux.core.units`): **all internal data is SI**
(metres, tesla, amperes). Conversions to/from display units (mm, mT) happen
only at the CAD-import boundary and in the UI.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------- #
# Physical constants (SI)
# --------------------------------------------------------------------------- #

#: Permeability of free space [H/m].
MU_0: float = 4.0e-7 * math.pi

#: Relative permeability of vacuum / air.
MU_R_AIR: float = 1.0

# --------------------------------------------------------------------------- #
# Application metadata
# --------------------------------------------------------------------------- #

APP_NAME: str = "MagnetFlux Studio"
APP_ORG: str = "MagnetFlux"
PROJECT_FILE_EXTENSION: str = ".mfx"
PROJECT_FILE_VERSION: int = 1


@dataclass(slots=True)
class AppConfig:
    """Runtime configuration for a MagnetFlux Studio session.

    Attributes:
        log_level: Logging level name (e.g. ``"INFO"``, ``"DEBUG"``).
        log_dir: Directory where rotating log files are written.
        default_air_padding: Air-domain padding as a multiple of the model
            bounding-box half-extent (solver, Milestone 3).
        default_mesh_size: Default characteristic mesh element size [m].
    """

    log_level: str = "INFO"
    log_dir: Path = field(default_factory=lambda: Path.home() / ".magnetflux" / "logs")
    default_air_padding: float = 2.0
    default_mesh_size: float = 2.0e-3

    def ensure_dirs(self) -> None:
        """Create configuration directories if they do not yet exist."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
