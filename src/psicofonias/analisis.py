"""Pruebas estadísticas de H1, H2 y H3 (preregistro §5)."""
from __future__ import annotations

import math

import numpy as np
from scipy.stats import binom

from .texto import tokens

MIN_PAREJAS_H2 = 5  # por debajo, la prueba H2 de esa pareja y ese ruido «no es evaluable»


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - m, c + m)


def matriz_jaccard(a: list[str], b: list[str]) -> np.ndarray:
    """M[i, j] = Jaccard(a_i, b_j); NaN si alguna es vacía."""
    sa = [set(tokens(x)) for x in a]
    sb = [set(tokens(x)) for x in b]
    M = np.full((len(a), len(b)), np.nan)
    for i, ta in enumerate(sa):
        if not ta:
            continue
        for j, tb in enumerate(sb):
            if tb:
                M[i, j] = len(ta & tb) / len(ta | tb)
    return M


def h2_permutaciones(a: list[str], b: list[str], n_perm: int, rng: np.random.Generator) -> dict:
    """J media en los fragmentos con las dos transcripciones no vacías, frente al barajado de b.
    p = (1 + #(J_barajado >= J_obs)) / (n_perm + 1). Si hay < MIN_PAREJAS_H2 parejas, no evaluable."""
    if len(a) != len(b):
        raise ValueError("listas de distinto largo")
    M = matriz_jaccard(a, b)
    diag = np.diag(M)
    validas = ~np.isnan(diag)
    n_pares = int(validas.sum())
    if n_pares < MIN_PAREJAS_H2:
        return {"evaluable": False, "n_pares": n_pares, "J_obs": float("nan"), "p": float("nan")}
    j_obs = float(diag[validas].mean())
    n = len(a)
    filas = np.arange(n)
    mayores = 0
    lote = 1000
    for ini in range(0, n_perm, lote):
        k = min(lote, n_perm - ini)
        perms = np.argsort(rng.random((k, n)), axis=1)
        vals = M[filas[None, :], perms]
        cuenta = np.sum(~np.isnan(vals), axis=1)
        suma = np.nansum(vals, axis=1)
        medias = np.where(cuenta > 0, suma / np.maximum(cuenta, 1), -np.inf)
        mayores += int(np.sum(medias >= j_obs - 1e-12))
    return {"evaluable": True, "n_pares": n_pares, "J_obs": j_obs, "p": (1 + mayores) / (n_perm + 1)}


def mcnemar_unilateral(si_tratamiento: np.ndarray, si_control: np.ndarray) -> dict:
    """McNemar exacto de una cola: ¿más «sí» con el tratamiento que con el control, en los mismos fragmentos?"""
    t = np.asarray(si_tratamiento, bool)
    c = np.asarray(si_control, bool)
    b = int(np.sum(t & ~c))
    cc = int(np.sum(~t & c))
    n = b + cc
    p = 1.0 if n == 0 else float(binom.sf(b - 1, n, 0.5))
    return {"b": b, "c": cc, "p": p}


def holm(pvals: list[float]) -> list[float]:
    """p ajustados de Holm (los NaN, que son pruebas no evaluables, no cuentan y se devuelven como NaN)."""
    idx = [i for i, p in enumerate(pvals) if not math.isnan(p)]
    m = len(idx)
    orden = sorted(idx, key=lambda i: pvals[i])
    ajust = [float("nan")] * len(pvals)
    acumulado = 0.0
    for r, i in enumerate(orden):
        acumulado = max(acumulado, min(1.0, (m - r) * pvals[i]))
        ajust[i] = acumulado
    return ajust
