"""Exporta, para el montaje del vídeo, los trozos de ruido de P1 que salen en el guion (docs/guion_video.md).
Regenera cada trozo con su semilla y comprueba que su huella coincide bit a bit con la que se usó en la pasada real.
No transcribe nada: las transcripciones son las guardadas de la pasada única. Escribe video/clips/*.wav y video/clips/clips.json.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from psicofonias import audio  # noqa: E402

CLIPS = ["rosa_236", "rosa_243", "rosa_105", "rosa_003", "blanco_001"]
salida = RAIZ / "video/clips"
salida.mkdir(parents=True, exist_ok=True)


def cargar(etapa, ia):
    ruta = RAIZ / f"results/pasada/{etapa}__{ia}.jsonl"
    return {r["id"]: r for r in (json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip())}


t = {(e, ia): cargar(e, ia) for e, ia in [("ruido", "base"), ("ruido", "small"), ("ruido", "medium"), ("ruido", "vosk"), ("h3_neutra", "medium"), ("h3_psico", "medium")]}
info = {}
for c in CLIPS:
    tipo, i = c.split("_")
    x = audio.fragmento_principal(tipo, int(i))
    q = audio.a_int16(x)
    h = hashlib.sha256(q.tobytes()).hexdigest()
    esperado = t[("ruido", "medium")][c]["sha256"]
    if h != esperado:
        raise SystemExit(f"{c}: la huella no coincide con la pasada real")
    audio.guardar_wav(salida / f"{c}.wav", x)
    info[c] = {"sha256_audio": h, **{f"{e}/{ia}": t[(e, ia)][c]["texto"] for (e, ia) in t}}
(salida / "clips.json").write_text(json.dumps(info, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps(info, indent=1, ensure_ascii=False))
