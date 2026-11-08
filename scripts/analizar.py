"""Análisis preregistrado de P1 (preregistro §5) y exploratorio E4. Lee results/pasada/ y escribe results/analisis.json.

Uso: python scripts/analizar.py [carpeta_de_transcripciones]
"""
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from psicofonias import analisis, audio, texto  # noqa: E402

SEMILLA_PERM = 20261111
N_PERM = 10000
FAMILIA = {"base": "whisper", "small": "whisper", "medium": "whisper", "vosk": "vosk"}


def cargar(carpeta, etapa, ia):
    ruta = carpeta / f"{etapa}__{ia}.jsonl"
    if not ruta.exists():
        return None
    return {r["id"]: r for r in (json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip())}


def main():
    carpeta = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "results/pasada"
    rng = np.random.default_rng(SEMILLA_PERM)
    ias = [ia for ia in FAMILIA if cargar(carpeta, "ruido", ia)]
    ruido = {ia: cargar(carpeta, "ruido", ia) for ia in ias}
    res = {"ias": ias, "H1": {}, "H2": {}, "H3": {}, "V0": {}, "controles": {}, "E4": {}}

    # V0: WER por IA y relación señal/ruido
    for ia in ias:
        v0 = cargar(carpeta, "v0", ia) or {}
        por_snr = {}
        for r in v0.values():
            por_snr.setdefault(r["snr"], []).append(texto.wer(r["ref"], r["texto"]))
        res["V0"][ia] = {str(k): round(float(np.mean(v)), 4) for k, v in sorted(por_snr.items(), reverse=True)}

    # H1
    for ia in ias:
        for tipo in audio.TIPOS:
            filas = [r for r in ruido[ia].values() if r["tipo"] == tipo]
            k = sum(texto.no_vacia(r["texto"]) for r in filas)
            lo, hi = analisis.wilson(k, len(filas))
            res["H1"][f"{ia}/{tipo}"] = {"n": len(filas), "no_vacias": k, "frac": k / len(filas), "ic95": [lo, hi]}
    res["H1_afirmacion"] = any(v["ic95"][0] > 0.05 for v in res["H1"].values())

    # H2: todas las parejas x tipo de ruido; Holm sobre todas las evaluables
    claves, ps = [], []
    for a, b in combinations(ias, 2):
        for tipo in audio.TIPOS:
            ids = sorted(i for i, r in ruido[a].items() if r["tipo"] == tipo)
            out = analisis.h2_permutaciones([ruido[a][i]["texto"] for i in ids], [ruido[b][i]["texto"] for i in ids], N_PERM, rng)
            out["familia"] = "entre_hermanos" if FAMILIA[a] == FAMILIA[b] else "entre_familias"
            res["H2"][f"{a}-{b}/{tipo}"] = out
            claves.append(f"{a}-{b}/{tipo}")
            ps.append(out["p"])
    for k, pa in zip(claves, analisis.holm(ps)):
        res["H2"][k]["p_holm"] = pa
        res["H2"][k]["positivo"] = bool(pa < 0.01) if not np.isnan(pa) else None
    # Referencia: el mismo parecido con voz real (controles)
    ctrl = {ia: cargar(carpeta, "controles", ia) for ia in ias}
    for a, b in combinations(ias, 2):
        if ctrl[a] and ctrl[b]:
            js = [texto.jaccard(ctrl[a][i]["texto"], ctrl[b][i]["texto"]) for i in sorted(ctrl[a])]
            js = [j for j in js if not np.isnan(j)]
            res["controles"][f"{a}-{b}"] = {"J_media": float(np.mean(js)) if js else None, "n": len(js)}

    # H3: medium, psicofonía frente a neutra, en los mismos fragmentos
    neu, psi, sin = cargar(carpeta, "h3_neutra", "medium"), cargar(carpeta, "h3_psico", "medium"), ruido.get("medium")
    if neu and psi:
        ids = sorted(set(neu) & set(psi))
        nv = (np.array([texto.no_vacia(psi[i]["texto"]) for i in ids]), np.array([texto.no_vacia(neu[i]["texto"]) for i in ids]))
        lx = (np.array([texto.contiene_lexico(psi[i]["texto"]) for i in ids]), np.array([texto.contiene_lexico(neu[i]["texto"]) for i in ids]))
        r_nv, r_lx = analisis.mcnemar_unilateral(*nv), analisis.mcnemar_unilateral(*lx)
        p_h = analisis.holm([r_nv["p"], r_lx["p"]])
        res["H3"] = {
            "n": len(ids),
            "no_vacia": {**r_nv, "frac_psico": float(nv[0].mean()), "frac_neutra": float(nv[1].mean()), "p_holm": p_h[0]},
            "lexico": {**r_lx, "frac_psico": float(lx[0].mean()), "frac_neutra": float(lx[1].mean()), "p_holm": p_h[1]},
            "positivo": bool(min(p_h) < 0.01),
        }
        if sin:
            res["H3"]["sin_instruccion_descriptivo"] = {
                "frac_no_vacia": float(np.mean([texto.no_vacia(sin[i]["texto"]) for i in ids])),
                "frac_lexico": float(np.mean([texto.contiene_lexico(sin[i]["texto"]) for i in ids])),
            }

    # E4 (exploratorio): las 20 frases más repetidas en el ruido, por IA
    for ia in ias:
        c = Counter(" ".join(texto.tokens(r["texto"])) for r in ruido[ia].values() if texto.no_vacia(r["texto"]))
        res["E4"][ia] = c.most_common(20)

    salida = RAIZ / "results/analisis.json"
    salida.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("H1_afirmacion",)}, ensure_ascii=False))
    print("Escrito", salida)


if __name__ == "__main__":
    main()
