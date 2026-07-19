"""Tangential / normal field decomposition on a target surface (Milestone 5).

Magnetron erosion is governed by the field's orientation relative to the target
surface. This module splits the flux density into the component normal to the
surface (``B_n``) and the component tangential to it (``B_t``); the race-track
model builds on these.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class FieldDecomposition:
    """Normal / tangential split of B on a surface.

    Attributes:
        b_normal: ``(N,)`` signed normal component ``B . n`` [T].
        b_tangential: ``(N, 3)`` tangential vector ``B - (B.n) n`` [T].
        b_tangential_mag: ``(N,)`` tangential magnitude ``|B_t|`` [T].
    """

    b_normal: np.ndarray
    b_tangential: np.ndarray
    b_tangential_mag: np.ndarray


def decompose(b: np.ndarray, normal: np.ndarray) -> FieldDecomposition:
    """Split ``(N, 3)`` flux density into normal and tangential parts.

    Args:
        b: Flux density vectors [T].
        normal: Target surface unit normal (any non-zero vector; normalised).
    """
    b = np.asarray(b, dtype=float).reshape(-1, 3)
    n = np.asarray(normal, dtype=float).reshape(3)
    n = n / np.linalg.norm(n)
    b_n = b @ n
    b_t_vec = b - b_n[:, None] * n
    b_t_mag = np.linalg.norm(b_t_vec, axis=1)
    return FieldDecomposition(b_n, b_t_vec, b_t_mag)
