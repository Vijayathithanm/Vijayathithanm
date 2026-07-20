"""Safe custom-expression evaluator over field variables (Milestone: Results).

Lets users type expressions like ``sqrt(Bx^2 + By^2 + Bz^2)`` or
``Bz / mu0`` and evaluate them elementwise over the sampled field. Only
arithmetic, a whitelist of NumPy functions, the provided variables and a few
constants are allowed -- no attribute access, indexing, imports or builtins --
so arbitrary code cannot run.
"""

from __future__ import annotations

import ast

import numpy as np

from magnetflux.config import MU_0

_ALLOWED_FUNCS = {
    "sqrt": np.sqrt, "abs": np.abs, "exp": np.exp, "log": np.log,
    "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "minimum": np.minimum, "maximum": np.maximum, "where": np.where,
    "sign": np.sign,
}
_CONSTANTS = {"pi": float(np.pi), "mu0": MU_0}

_ALLOWED_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Call, ast.Name, ast.Load,
    ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
    ast.USub, ast.UAdd,
)


def _validate(node: ast.AST) -> None:
    for child in ast.walk(node):
        if not isinstance(child, _ALLOWED_NODES):
            raise ValueError(f"disallowed expression element: {type(child).__name__}")
        if isinstance(child, ast.Call):
            if not isinstance(child.func, ast.Name) or child.func.id not in _ALLOWED_FUNCS:
                raise ValueError("only whitelisted functions may be called")


def evaluate_expression(expression: str, variables: dict[str, np.ndarray]) -> np.ndarray:
    """Evaluate ``expression`` elementwise over ``variables``.

    Args:
        expression: e.g. ``"sqrt(Bx^2 + By^2 + Bz^2)"`` (``^`` means power).
        variables: name -> array (e.g. ``{"Bx":..., "By":..., "Bz":...}``).

    Raises:
        ValueError: If the expression uses a disallowed construct or unknown name.
    """
    # Engineers write ``^`` for exponentiation; map to Python's ``**`` before
    # parsing so operator precedence is correct.
    tree = ast.parse(expression.replace("^", "**"), mode="eval")
    _validate(tree)

    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    scope = {**_CONSTANTS, **variables}
    unknown = names - set(scope) - set(_ALLOWED_FUNCS)
    if unknown:
        raise ValueError(f"unknown variable(s): {sorted(unknown)}")

    code = compile(tree, "<expression>", "eval")
    result = eval(code, {"__builtins__": {}}, {**_ALLOWED_FUNCS, **scope})  # noqa: S307
    return np.asarray(result, dtype=float)
