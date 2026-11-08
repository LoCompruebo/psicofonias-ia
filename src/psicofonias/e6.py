"""E6: psicofonías reales (docs/03_e6_plan.md). Módulo nuevo; no toca el código congelado de P1."""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

from .texto import tokens

RAIZ = Path(__file__).resolve().parents[2]
LISTA = RAIZ / "data/e6_candidatas.csv"
AUDIO = RAIZ / "data/generado/e6_16k"
RUTAS_VOSK = {
    "es": RAIZ / "data/raw/vosk_small_es_0.42/vosk-model-small-es-0.42",
    "en": RAIZ / "data/raw/vosk_small_en_0.15/vosk-model-small-en-us-0.15",
}


def lista() -> list[dict]:
    with LISTA.open(encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh, delimiter="|"))
    for f in filas:
        f["n"] = int(f["n"])
        f["wav"] = AUDIO / f"{f['n']:03d}.wav"
    return filas


def grupo(f: dict) -> str:
    """Grupo de autores, para el sesgo (§1 del plan). Lo fija la URL y el identificador, no el contenido."""
    if f["fuente"] == "freesound":
        autor = f["url"].split("/previews/")[1]
        if "_112484-" in autor:
            return "Todd_Bates"
        if "_2436611-" in autor:
            return "Soulwriter"
        if "_4811789-" in autor:
            return "southlandghosthunter"
        return "otros"
    if 6 <= f["n"] <= 49 or 52 <= f["n"] <= 65:
        return "MSSPI"
    return "otros"


def whisper(modelo, x: np.ndarray, idioma: str) -> str:
    """Como en P1 (ajustes por defecto, sin instrucción), pero con el idioma de la grabación."""
    segmentos, _ = modelo.transcribe(x.astype(np.float32), language=idioma)
    return " ".join(s.text.strip() for s in segmentos).strip()


def cobertura(frase: str, transcripcion: str | None) -> float:
    """Fracción de las palabras (únicas) de la frase del autor que aparecen en la transcripción."""
    tf = set(tokens(frase))
    if not tf:
        return float("nan")
    return len(tf & set(tokens(transcripcion))) / len(tf)


def prueba_cobertura(frases: list[str], textos: list[str], idiomas: list[str], n_perm: int, rng) -> dict:
    """Cobertura media de la frase propia frente a la de otra grabación del mismo idioma (barajado).
    p = (1 + #(barajado >= observado)) / (n_perm + 1), una cola."""
    n = len(frases)
    C = np.array([[cobertura(frases[j], textos[i]) for j in range(n)] for i in range(n)])
    obs = float(np.nanmean(np.diag(C)))
    aciertos = int(np.sum(np.diag(C) >= 0.5))
    grupos = {}
    for i, l in enumerate(idiomas):
        grupos.setdefault(l, []).append(i)
    mayores = 0
    nulos = np.empty(n_perm)
    aciertos_nulos = np.empty(n_perm)
    for k in range(n_perm):
        perm = np.arange(n)
        for idx in grupos.values():
            perm[idx] = rng.permutation(idx)
        vals = C[np.arange(n), perm]
        v = float(np.nanmean(vals))
        nulos[k] = v
        aciertos_nulos[k] = np.sum(vals >= 0.5)
        mayores += v >= obs - 1e-12
    return {
        "n": n,
        "cobertura_media": obs,
        "cobertura_nula_media": float(nulos.mean()),
        "aciertos_0_5": aciertos,
        "aciertos_nulos_esperados": float(aciertos_nulos.mean()),
        "p": (1 + mayores) / (n_perm + 1),
    }


def jaccard_frase(frase: str, transcripcion: str | None) -> float:
    a, b = set(tokens(frase)), set(tokens(transcripcion))
    if not a or not b:
        return 0.0 if a else math.nan
    return len(a & b) / len(a | b)
