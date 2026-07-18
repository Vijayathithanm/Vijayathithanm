"""Core domain data model for MagnetFlux Studio.

Pure-Python / NumPy data structures shared by every other layer. This layer
has no knowledge of Qt, PyVista, Gmsh or any solver backend.
"""

from magnetflux.core.geometry import BoundingBox, TriangleMesh
from magnetflux.core.model_tree import Body, ModelTree
from magnetflux.core.units import LengthUnit

__all__ = ["BoundingBox", "TriangleMesh", "Body", "ModelTree", "LengthUnit"]
