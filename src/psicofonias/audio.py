"""Ruido, mezcla y ficheros WAV (preregistro §2). Todo determinista a partir de semillas."""
from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

SR = 16000
DURACION = 10.0
N = int(SR * DURACION)
RMS_OBJETIVO = 10 ** (-20 / 20)  # -20 dBFS de media cuadrática
TIPOS = ("blanco", "rosa", "marron")
EXPONENTE = {"blanco": 0.0, "rosa": 1.0, "marron": 2.0}  # densidad espectral ~ 1/f^exponente

# Semillas base (preregistro §2 y §6). Cada fragmento usa SeedSequence([base, tipo, índice]).
SEMILLA_PRINCIPAL = 20261105
SEMILLA_CONTROLES = 20261106
SEMILLA_V0 = 20261107


def rng_para(base: int, *claves: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([base, *claves]))


def ruido(tipo: str, rng: np.random.Generator, n: int = N) -> np.ndarray:
    """Ruido gaussiano con espectro 1/f^a, sin media y a -20 dBFS RMS. Devuelve float64."""
    x = rng.standard_normal(n)
    a = EXPONENTE[tipo]
    if a:
        X = np.fft.rfft(x)
        f = np.fft.rfftfreq(n, 1 / SR)
        f[0] = f[1]
        X *= f ** (-a / 2)
        x = np.fft.irfft(X, n)
    x -= x.mean()
    x *= RMS_OBJETIVO / np.sqrt(np.mean(x**2))
    return x


def fragmento_principal(tipo: str, indice: int) -> np.ndarray:
    return ruido(tipo, rng_para(SEMILLA_PRINCIPAL, TIPOS.index(tipo), indice))


def mezclar(voz: np.ndarray, ruido_fondo: np.ndarray, snr_db: float, inicio: float = 1.0) -> np.ndarray:
    """Pone la voz en el ruido a partir de `inicio` segundos. El ruido no cambia de nivel; la voz se escala
    para que su potencia (en su propio tramo) quede `snr_db` dB por encima de la del ruido en ese tramo."""
    i0 = int(inicio * SR)
    if i0 + len(voz) > len(ruido_fondo):
        raise ValueError("la voz no cabe en el fragmento")
    tramo = ruido_fondo[i0 : i0 + len(voz)]
    p_voz = np.mean(voz.astype(np.float64) ** 2)
    p_ruido = np.mean(tramo**2)
    g = np.sqrt(p_ruido * 10 ** (snr_db / 10) / p_voz)
    y = ruido_fondo.copy()
    y[i0 : i0 + len(voz)] += g * voz
    return y


def limitar_pico(y: np.ndarray, pico: float = 0.9) -> np.ndarray:
    """Si la mezcla pasa de `pico`, se baja entera (voz y ruido a la vez) hasta `pico`, como haría el control
    automático de nivel de una grabadora. No cambia la relación señal/ruido."""
    m = np.max(np.abs(y))
    return y * (pico / m) if m > pico else y


def a_int16(x: np.ndarray) -> np.ndarray:
    pico = np.max(np.abs(x))
    if pico >= 1.0:
        raise ValueError(f"saturación: pico {pico:.3f}")
    return np.round(x * 32767).astype(np.int16)


def guardar_wav(ruta: Path, x: np.ndarray) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(ruta), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(a_int16(x).tobytes())


def leer_wav(ruta: Path) -> np.ndarray:
    with wave.open(str(ruta), "rb") as w:
        if w.getframerate() != SR or w.getnchannels() != 1 or w.getsampwidth() != 2:
            raise ValueError(f"{ruta}: se espera 16 kHz, mono, 16 bits")
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32767
