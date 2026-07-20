"""Parametric study layer: sweep design parameters and compare designs."""

from magnetflux.study.parametric import (
    PARAMETERS,
    ParametricStudy,
    StudyResult,
    apply_parameters,
    best,
)

__all__ = [
    "ParametricStudy",
    "StudyResult",
    "apply_parameters",
    "best",
    "PARAMETERS",
]
