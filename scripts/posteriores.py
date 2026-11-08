"""Pasos posteriores al análisis (no congelados; escritos el 08-11 tras ver results/analisis.json).

1. E5: puntúa con Brier la apuesta sellada de Claude (results/apuesta_claude.md) frente a results/analisis.json.
   Los sucesos se leen tal como se definieron en la apuesta; no se reinterpretan.
2. E1: prepara el material con la regla fijada en el preregistro §9 (semilla 20261108): 30 transcripciones no vacías
   de Whisper medium sin instrucción, y 30 cadenas de palabras al azar del mismo largo sacadas de las frases de control.
   Solo prepara; la interpretación y la puntuación a ciegas van aparte.

Escribe results/e5_puntuacion.json y results/e1_material.json.
"""
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from psicofonias import texto  # noqa: E402

an = json.loads((RAIZ / "results/analisis.json").read_text(encoding="utf-8"))
h1 = an["H1"]
lim = lambda k: h1[k]["ic95"][0] > 0.05  # noqa: E731
h2 = an["H2"]
top3 = {ia: [f for f, _ in an["E4"][ia][:3]] for ia in ("base", "small", "medium")}
subtitulo = lambda f: ("subtitulos" in f) or ("gracias por ver" in f)  # noqa: E731

sucesos = [
    ("H1 se cumple", 0.75, an["H1_afirmacion"]),
    ("Algún Whisper cumple H1", 0.70, any(lim(k) for k in h1 if not k.startswith("vosk"))),
    ("Vosk cumple H1", 0.55, any(lim(k) for k in h1 if k.startswith("vosk"))),
    ("H2 positiva entre hermanos", 0.35, any(v.get("positivo") is True for v in h2.values() if v["familia"] == "entre_hermanos")),
    ("H2 positiva entre familias", 0.10, any(v.get("positivo") is True for v in h2.values() if v["familia"] == "entre_familias")),
    ("H3 positiva", 0.70, an["H3"]["positivo"]),
    ("H3 léxico p_Holm < 0,01", 0.40, an["H3"]["lexico"]["p_holm"] < 0.01),
    ("E4: subtítulos o «gracias por ver» en el top 3 de algún Whisper", 0.50, any(subtitulo(f) for fs in top3.values() for f in fs)),
    ("V0: medium < 50 % de WER a 0 dB", 0.70, an["V0"]["medium"]["0"] < 0.5),
]
filas = [{"suceso": s, "p": p, "ocurre": bool(r), "brier": round((p - float(r)) ** 2, 4)} for s, p, r in sucesos]
media = float(np.mean([f["brier"] for f in filas]))
e5 = {"filas": filas, "brier_medio": round(media, 4), "referencia_moneda_0_5": 0.25, "top3": top3}
(RAIZ / "results/e5_puntuacion.json").write_text(json.dumps(e5, indent=1, ensure_ascii=False), encoding="utf-8")
for f in filas:
    print(f)
print("Brier medio", round(media, 4), "(moneda al aire: 0,25)")

# E1: material
rng = np.random.default_rng(20261108)
filas_m = [json.loads(l) for l in (RAIZ / "results/pasada/ruido__medium.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
no_vacias = sorted((r for r in filas_m if texto.no_vacia(r["texto"])), key=lambda r: r["id"])
elegidas = [no_vacias[i] for i in sorted(rng.choice(len(no_vacias), 30, replace=False))]
palabras = [w for f in (RAIZ / "data/frases_control.txt").read_text(encoding="utf-8").split("\n") for w in f.strip().rstrip(".").split() if w]
azar = []
for r in elegidas:
    n = len(r["texto"].split())
    azar.append(" ".join(rng.choice(palabras, n, replace=True)))
e1 = {"ruido": [{"id": r["id"], "texto": r["texto"]} for r in elegidas], "azar": [{"id": f"azar_{k:02d}", "texto": t} for k, t in enumerate(azar)]}
(RAIZ / "results/e1_material.json").write_text(json.dumps(e1, indent=1, ensure_ascii=False), encoding="utf-8")
print("E1:", [r["texto"] for r in elegidas])
print("E1 azar:", azar[:5])
