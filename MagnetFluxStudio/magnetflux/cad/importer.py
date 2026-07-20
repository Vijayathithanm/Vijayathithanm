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

    One :class:`TriangleMesh` per solid (STL returns a single mesh), in metres.
    Use :func:`import_cad_named` to also get per-component names.
    """
    return [mesh for _name, mesh in import_cad_named(path, source_unit)]


def import_cad_named(
    path: str | Path,
    source_unit: LengthUnit = LengthUnit.MILLIMETER,
) -> list[tuple[str | None, TriangleMesh]]:
    """Import a CAD file, returning ``(component_name, mesh)`` pairs (metres).

    STEP/IGES assemblies keep each solid's component name so materials can be
    assigned per part in a single import. STL yields a single unnamed solid.

    Raises:
        UnsupportedFormatError: For an unrecognised extension.
        FileNotFoundError: If the file does not exist.
        RuntimeError: If STEP/IGES import needs a CAD kernel that isn't present.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    ext = path.suffix.lower()
    scale = source_unit.to_meter

    named: list[tuple[str | None, TriangleMesh]]
    if ext in STL_EXTENSIONS:
        from magnetflux.cad.stl import read_stl

        named = [(None, read_stl(path))]
    elif ext in STEP_EXTENSIONS or ext in IGES_EXTENSIONS:
        from magnetflux.cad.occ_import import is_occ_available, read_iges, read_step

        if is_occ_available():
            # pythonOCC gives the highest-fidelity B-rep import when present.
            meshes = read_step(path) if ext in STEP_EXTENSIONS else read_iges(path)
            named = [(None, m) for m in meshes]
        else:
            # Fall back to Gmsh, which ships pip wheels and works in the packaged app.
            from magnetflux.cad.gmsh_import import is_gmsh_available, read_cad_gmsh_named

            if not is_gmsh_available():
                raise RuntimeError(
                    "STEP/IGES import requires Gmsh or pythonOCC. Install with "
                    "'pip install gmsh', or import an STL instead."
                )
            named = read_cad_gmsh_named(path)
    else:
        raise UnsupportedFormatError(
            f"unsupported CAD format '{ext}'; supported: "
            f"{sorted(SUPPORTED_EXTENSIONS)}"
        )

    if scale != 1.0:
        named = [(name, m.scaled(scale)) for name, m in named]
    log.info("Imported %s: %d solid(s), unit=%s", path.name, len(named), source_unit.value)
    return named
