"""CAD import layer: STEP / IGES / STL -> TriangleMesh (scaled to metres)."""

from magnetflux.cad.importer import (
    SUPPORTED_EXTENSIONS,
    UnsupportedFormatError,
    import_cad,
    import_cad_named,
)
from magnetflux.cad.stl import read_stl, write_binary_stl

__all__ = [
    "import_cad",
    "import_cad_named",
    "read_stl",
    "write_binary_stl",
    "SUPPORTED_EXTENSIONS",
    "UnsupportedFormatError",
]
