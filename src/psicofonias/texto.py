"""Normalización de transcripciones y medidas de texto (preregistro §5)."""
from __future__ import annotations

import re
import unicodedata

# Léxico «fantasmal» de H3, fijado en el preregistro §5 (ya normalizado: sin tildes).
LEXICO_FANTASMAL = frozenset(
    "muerte muerto muertos ayuda ayudame socorro vete fuera alma almas dios diablo demonio "
    "infierno sangre frio miedo oscuridad auxilio perdon matar mataron tumba cielo".split()
)
# Palabras de la instrucción de psicofonía: no cuentan para el léxico (no se premia copiar la instrucción).
PALABRAS_INSTRUCCION = frozenset("psicofonia grabada casa abandonada voces espiritus dicen".split())

_NO_LETRA = re.compile(r"[^a-z]+")


def _sin_tildes(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def tokens(s: str | None) -> list[str]:
    """Minúsculas, sin tildes ni signos; solo tokens de letras con 2 o más caracteres."""
    if not s:
        return []
    s = _NO_LETRA.sub(" ", _sin_tildes(s.lower()))
    return [t for t in s.split() if len(t) >= 2]


def no_vacia(s: str | None) -> bool:
    return len(tokens(s)) > 0


def jaccard(a: str | None, b: str | None) -> float:
    """J de Jaccard sobre conjuntos de tokens. Solo definida si las dos son no vacías (si no, NaN)."""
    ta, tb = set(tokens(a)), set(tokens(b))
    if not ta or not tb:
        return float("nan")
    return len(ta & tb) / len(ta | tb)


def contiene_lexico(s: str | None) -> bool:
    return any(t in LEXICO_FANTASMAL and t not in PALABRAS_INSTRUCCION for t in tokens(s))


_UNIDADES = "cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciseis diecisiete dieciocho diecinueve veinte veintiuno veintidos veintitres veinticuatro veinticinco veintiseis veintisiete veintiocho veintinueve".split()
_DECENAS = {30: "treinta", 40: "cuarenta", 50: "cincuenta", 60: "sesenta", 70: "setenta", 80: "ochenta", 90: "noventa"}


def _numero(n: int) -> list[str]:
    if n < 30:
        return [_UNIDADES[n]]
    d, u = divmod(n, 10)
    return [_DECENAS[d * 10]] + (["y", _UNIDADES[u]] if u else [])


def tokens_wer(s: str | None) -> list[str]:
    """Como tokens(), pero las cifras de 0 a 99 se escriben en palabras («8» -> «ocho»). Solo para el WER de V0:
    Whisper escribe cifras y Vosk palabras, y la referencia está en palabras."""
    if not s:
        return []
    s = re.sub(r"\d+", lambda m: " " + " ".join(_numero(int(m.group()))) + " " if int(m.group()) < 100 else " ", s)
    return tokens(s)


def wer(referencia: str, hipotesis: str | None) -> float:
    """Tasa de error de palabras: distancia de edición entre listas de tokens / largo de la referencia."""
    r, h = tokens_wer(referencia), tokens_wer(hipotesis)
    if not r:
        raise ValueError("referencia vacía")
    prev = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        cur = [i] + [0] * len(h)
        for j, hw in enumerate(h, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (rw != hw))
        prev = cur
    return prev[-1] / len(r)
