"""Global optimizers: genetic algorithm, particle swarm, Bayesian (Milestone: Optimization).

All optimizers maximise a ``fitness(x) -> float`` over the unit hypercube
``x in [0, 1]^n`` (the design space maps that to physical parameters). Pure
NumPy/SciPy so they bundle into the Windows executable with no extra deps.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

import numpy as np

Fitness = Callable[[np.ndarray], float]


@dataclass(slots=True)
class OptimizeOutcome:
    """Result of an optimizer run.

    Attributes:
        best_x: Best design vector found, in ``[0, 1]^n``.
        best_value: Fitness at ``best_x`` (higher is better).
        history: Best-so-far fitness after each iteration/generation.
    """

    best_x: np.ndarray
    best_value: float
    history: list[float] = field(default_factory=list)


def _evaluate_pop(fitness: Fitness, pop: np.ndarray) -> np.ndarray:
    return np.array([fitness(x) for x in pop], dtype=float)


def genetic_algorithm(
    fitness: Fitness, n_vars: int, pop_size: int = 24, generations: int = 30,
    mutation: float = 0.15, seed: int = 0,
) -> OptimizeOutcome:
    """Maximise ``fitness`` with a real-coded GA (tournament + blend + elitism)."""
    rng = np.random.default_rng(seed)
    pop = rng.random((pop_size, n_vars))
    fit = _evaluate_pop(fitness, pop)
    history = [float(fit.max())]

    for _ in range(generations):
        # Tournament selection.
        a, b = rng.integers(0, pop_size, pop_size), rng.integers(0, pop_size, pop_size)
        winners = np.where(fit[a] >= fit[b], a, b)
        parents = pop[winners]
        # Blend crossover with a shuffled partner.
        partner = parents[rng.permutation(pop_size)]
        alpha = rng.random((pop_size, n_vars))
        children = alpha * parents + (1 - alpha) * partner
        # Gaussian mutation.
        mask = rng.random((pop_size, n_vars)) < mutation
        children = np.clip(children + mask * rng.normal(0, 0.1, children.shape), 0, 1)
        cfit = _evaluate_pop(fitness, children)
        # Elitism: keep the best pop_size of parents + children.
        merged = np.vstack([pop, children])
        merged_fit = np.concatenate([fit, cfit])
        keep = np.argsort(merged_fit)[::-1][:pop_size]
        pop, fit = merged[keep], merged_fit[keep]
        history.append(float(fit.max()))

    best = int(np.argmax(fit))
    return OptimizeOutcome(pop[best], float(fit[best]), history)


def particle_swarm(
    fitness: Fitness, n_vars: int, n_particles: int = 24, iterations: int = 30,
    inertia: float = 0.7, c1: float = 1.5, c2: float = 1.5, seed: int = 0,
) -> OptimizeOutcome:
    """Maximise ``fitness`` with particle-swarm optimization."""
    rng = np.random.default_rng(seed)
    x = rng.random((n_particles, n_vars))
    v = rng.normal(0, 0.1, (n_particles, n_vars))
    pbest = x.copy()
    pfit = _evaluate_pop(fitness, x)
    g_idx = int(np.argmax(pfit))
    g, gfit = pbest[g_idx].copy(), float(pfit[g_idx])
    history = [gfit]

    for _ in range(iterations):
        r1, r2 = rng.random((n_particles, n_vars)), rng.random((n_particles, n_vars))
        v = inertia * v + c1 * r1 * (pbest - x) + c2 * r2 * (g - x)
        x = np.clip(x + v, 0, 1)
        f = _evaluate_pop(fitness, x)
        improved = f > pfit
        pbest[improved], pfit[improved] = x[improved], f[improved]
        if pfit.max() > gfit:
            g_idx = int(np.argmax(pfit))
            g, gfit = pbest[g_idx].copy(), float(pfit[g_idx])
        history.append(gfit)

    return OptimizeOutcome(g, gfit, history)


def bayesian_optimization(
    fitness: Fitness, n_vars: int, n_init: int = 8, iterations: int = 20,
    length: float = 0.2, noise: float = 1e-6, n_candidates: int = 256, seed: int = 0,
) -> OptimizeOutcome:
    """Maximise ``fitness`` with GP surrogate + expected-improvement acquisition."""
    from scipy.linalg import cho_factor, cho_solve
    from scipy.stats import norm

    rng = np.random.default_rng(seed)

    def rbf(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        d2 = np.sum(a**2, 1)[:, None] + np.sum(b**2, 1)[None, :] - 2 * a @ b.T
        return np.exp(-0.5 * np.maximum(d2, 0) / length**2)

    x = rng.random((n_init, n_vars))
    y = _evaluate_pop(fitness, x)
    history = [float(y.max())]

    for _ in range(iterations):
        mean = y.mean()
        chol = cho_factor(rbf(x, x) + noise * np.eye(len(x)), lower=True)
        alpha = cho_solve(chol, y - mean)
        cand = rng.random((n_candidates, n_vars))
        ks = rbf(cand, x)
        mu = mean + ks @ alpha
        var = 1.0 - np.einsum("ij,ij->i", ks, cho_solve(chol, ks.T).T)
        sigma = np.sqrt(np.clip(var, 1e-12, None))
        best = y.max()
        z = (mu - best) / sigma
        ei = (mu - best) * norm.cdf(z) + sigma * norm.pdf(z)
        nxt = cand[int(np.argmax(ei))]
        x = np.vstack([x, nxt])
        y = np.append(y, fitness(nxt))
        history.append(float(y.max()))

    best_i = int(np.argmax(y))
    return OptimizeOutcome(x[best_i], float(y[best_i]), history)


#: Registry of optimizers by short name.
OPTIMIZERS = {
    "ga": genetic_algorithm,
    "pso": particle_swarm,
    "bayesian": bayesian_optimization,
}
