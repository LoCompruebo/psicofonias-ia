"""Las IAs de transcripción (preregistro §3). Ajustes por defecto de cada librería, idioma español."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .audio import SR

RUTA_VOSK = Path(__file__).resolve().parents[2] / "data/raw/vosk_small_es_0.42/vosk-model-small-es-0.42"
MODELOS_WHISPER = ("base", "small", "medium")


def _dlls_nvidia() -> None:
    """Las librerías de CUDA (cuBLAS, cuDNN) están instaladas como paquetes de pip, pero Windows no las busca ahí."""
    import os
    import site

    for base in site.getsitepackages():
        raiz = Path(base) / "nvidia"
        if raiz.is_dir():
            for b in raiz.glob("*/bin"):
                os.add_dll_directory(str(b))
                os.environ["PATH"] = str(b) + os.pathsep + os.environ.get("PATH", "")


def cargar_whisper(tamano: str, dispositivo: str = "cuda", hilos: int = 4):
    if dispositivo == "cuda":
        _dlls_nvidia()
    from faster_whisper import WhisperModel

    # local_files_only: nunca descarga nada; usa los pesos ya guardados.
    if dispositivo == "cuda":
        return WhisperModel(tamano, device="cuda", compute_type="int8_float16", local_files_only=True)
    return WhisperModel(tamano, device="cpu", compute_type="int8", cpu_threads=hilos, local_files_only=True)


def whisper(modelo, x: np.ndarray, initial_prompt: str | None = None) -> str:
    segmentos, _info = modelo.transcribe(x.astype(np.float32), language="es", initial_prompt=initial_prompt)
    return " ".join(s.text.strip() for s in segmentos).strip()


def cargar_vosk():
    import vosk

    vosk.SetLogLevel(-1)
    return vosk.Model(str(RUTA_VOSK))


def vosk_transcribir(modelo, x: np.ndarray) -> str:
    import vosk

    rec = vosk.KaldiRecognizer(modelo, SR)
    datos = np.round(np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()
    textos = []
    paso = 8000  # 4000 muestras de 16 bits
    for i in range(0, len(datos), paso):
        if rec.AcceptWaveform(datos[i : i + paso]):
            textos.append(json.loads(rec.Result()).get("text", ""))
    textos.append(json.loads(rec.FinalResult()).get("text", ""))
    return " ".join(t for t in textos if t).strip()
