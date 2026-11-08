"""Mide la velocidad de cada IA con las frases de control LIMPIAS (sin ruido ni silencio añadido).
Permitido antes de congelar: no se pasa ningún ruido por ninguna IA. Además da el WER con voz limpia,
que comprueba que el montaje funciona. Salida: results/velocidad.json
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from psicofonias import audio, texto, transcribir  # noqa: E402
from psicofonias.runtime import prioridad_baja  # noqa: E402

N = 20


def main():
    prioridad_baja()
    frases = [f.strip() for f in (RAIZ / "data/frases_control.txt").read_text(encoding="utf-8").splitlines() if f.strip()]
    voces = [audio.leer_wav(RAIZ / f"data/generado/voz/frase_{i:02d}.wav") for i in range(N)]
    res = {}
    for nombre in (*transcribir.MODELOS_WHISPER, "vosk"):
        t0 = time.time()
        if nombre == "vosk":
            m = transcribir.cargar_vosk()
            f = lambda x: transcribir.vosk_transcribir(m, x)  # noqa: E731
        else:
            m = transcribir.cargar_whisper(nombre)
            f = lambda x: transcribir.whisper(m, x)  # noqa: E731
        carga = time.time() - t0
        f(voces[0])  # calentamiento
        t1 = time.time()
        hip = [f(x) for x in voces]
        dt = (time.time() - t1) / N
        wers = [texto.wer(frases[i], hip[i]) for i in range(N)]
        res[nombre] = {"carga_s": round(carga, 1), "s_por_frase": round(dt, 3), "wer_medio": round(float(np.mean(wers)), 4),
                       "ejemplos": [{"ref": frases[i], "hip": hip[i]} for i in range(3)]}
        print(nombre, {k: v for k, v in res[nombre].items() if k != "ejemplos"}, flush=True)
        del m
    (RAIZ / "results/velocidad.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
