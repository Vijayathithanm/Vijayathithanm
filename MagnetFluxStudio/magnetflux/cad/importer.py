"""CAD import dispatcher: format detection and unit scaling.

Loads STEP / IGES / STL into :class:`~magnetflux.core.geometry.TriangleMesh`
objects and applies the source-unit -> metre conversion in one place, so no
downstream layer ever sees millimetres.
"""

from __future__ import annotations

from pathlib import Path

from magnetflux.core.geometry import TriangleMesh
from magnetflux.core.units import LengthUnit
from magnetflux.logging_setup import get_logger

log = get_logger("cad.importer")

STEP_EXTENSIONS = {".step", ".stp"}
IGES_EXTENSIONS = {".iges", ".igs"}
STL_EXTENSIONS = {".stl"}
SUPPORTED_EXTENSIONS = STEP_EXTENSIONS | IGES_EXTENSIONS | STL_EXTENSIONS


class UnsupportedFormatError(ValueError):
    """Raised for a file extension MagnetFlux Studio cannot import."""


def import_cad(
    path: str | Path,
    source_unit: LengthUnit = LengthUnit.MILLIMETER,
) -> list[TriangleMesh]:
    """Import a CAD file, returning meshes scaled to metres.

    Args:
        path: File to import (``.step/.stp``, ``.iges/.igs`` or ``.stl``).
        source_unit: Unit the CAD file is authored in (CAD is usually mm).

    Returns:
        One :class:`TriangleMesh` per solid (STL returns a single mesh),
        with vertices in metres.

    Raises:
        UnsupportedFormatError: For an unrecognised extension.
        FileNotFoundError: If the file does not exist.
        RuntimeError: If STEP/IGES import is requested without pythonOCC.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    ext = path.suffix.lower()
    scale = source_unit.to_meter

    if ext in STL_EXTENSIONS:
        from magnetflux.cad.stl import read_stl

        meshes = [read_stl(path)]
    elif ext in STEP_EXTENSIONS or ext in IGES_EXTENSIONS:
        from magnetflux.cad.occ_import import is_occ_available, read_iges, read_step

        if is_occ_available():
            # pythonOCC gives the highest-fidelity B-rep import when present.
            meshes = read_step(path) if ext in STEP_EXTENSIONS else read_iges(path)
        else:
            # Fall back to Gmsh, which ships pip wheels and works in the packaged app.
            from magnetflux.cad.gmsh_import import is_gmsh_available, read_cad_gmsh

            if not is_gmsh_available():
                raise RuntimeError(
                    "STEP/IGES import requires Gmsh or pythonOCC. Install with "
                    "'pip install gmsh', or import an STL instead."
                )
            meshes = read_cad_gmsh(path)
    else:
        raise UnsupportedFormatError(
            f"unsupported CAD format '{ext}'; supported: "
            f"{sorted(SUPPORTED_EXTENSIONS)}"
        )

    scaled = [m.scaled(scale) for m in meshes] if scale != 1.0 else meshes
    log.info("Imported %s: %d solid(s), unit=%s", path.name, len(scaled), source_unit.value)
    return scaled
