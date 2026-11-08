"""V1: el análisis de H2 y H3 con transcripciones inventadas (preregistro §6). Sin audio ni IA.

H2:
  - nulo: cada «modelo» transcribe cada fragmento por su cuenta (sin relación con el otro). Criterio: falsas alarmas <= 2 % con p < 0,01.
  - efecto escondido: en el 10 % de los fragmentos los dos «modelos» escriben la misma frase. Criterio: detección >= 90 %.
  Escenarios del nulo: pocas transcripciones no vacías (5 %), muchas (30 %), y muchas con «alucinaciones típicas»
  dominantes (el 90 % de las frases sale de una bolsa común de 20, con pesos de Zipf), que es el caso difícil.
H3 (n = 3 x N_FRAG, McNemar, una cola, umbral 0,005 = el más exigente de Holm con 2 pruebas):
  - nulo: misma probabilidad con las dos instrucciones. Criterio: falsas alarmas <= 2 %.
  - efecto: +10 puntos de «no vacía» y +5 puntos de «léxico». Criterio: detección >= 90 % en cada una.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from psicofonias.analisis import h2_permutaciones, mcnemar_unilateral  # noqa: E402
from psicofonias.runtime import prioridad_baja  # noqa: E402

SEMILLA = 20261110  # intento 2 (el 1 usó 20261109; ver results/v1_intento1.log)
N_FRAG = 300  # intento 2: 300 por tipo (el intento 1 usó 200)
N_PERM = 10000
REPS = 500
SILABAS = [c + v for c in "bcdfglmnprstvz" for v in "aeiou"]


def vocabulario(rng, n=3000):
    return ["".join(rng.choice(SILABAS, size=rng.integers(2, 4))) for _ in range(n)]


def frase(rng, voc):
    return " ".join(rng.choice(voc, size=rng.integers(2, 7)))


def modelo_inventado(rng, voc, comunes, pesos, q, p_comun):
    """Una «transcripción» por fragmento: vacía con prob. 1-q; si no, una frase común (Zipf) o una al azar."""
    out = []
    for _ in range(N_FRAG):
        if rng.random() >= q:
            out.append("")
        elif rng.random() < p_comun:
            out.append(comunes[rng.choice(len(comunes), p=pesos)])
        else:
            out.append(frase(rng, voc))
    return out


def escenario_h2(rng, voc, q, p_comun, plantar):
    comunes = [frase(rng, voc) for _ in range(20)]
    w = 1 / np.arange(1, 21)
    pesos = w / w.sum()
    a = modelo_inventado(rng, voc, comunes, pesos, q, p_comun)
    b = modelo_inventado(rng, voc, comunes, pesos, q, p_comun)
    if plantar:
        for i in rng.choice(N_FRAG, size=int(0.10 * N_FRAG), replace=False):
            f = frase(rng, voc)
            a[i] = f
            b[i] = f
    return h2_permutaciones(a, b, N_PERM, rng)


def main():
    prioridad_baja()
    rng = np.random.default_rng(SEMILLA)
    voc = vocabulario(rng)
    res = {"semilla": SEMILLA, "reps": REPS, "n_perm": N_PERM, "h2": {}, "h3": {}}
    escenarios = [("q05_azar", 0.05, 0.0), ("q30_azar", 0.30, 0.0), ("q30_comunes90", 0.30, 0.9)]
    t0 = time.time()
    for nombre, q, pc in escenarios:
        for plantar in (False, True):
            ps, no_eval = [], 0
            for r in range(REPS):
                out = escenario_h2(rng, voc, q, pc, plantar)
                if out["evaluable"]:
                    ps.append(out["p"])
                else:
                    no_eval += 1
                if (r + 1) % 100 == 0:
                    print(f"  H2 {nombre} {'efecto' if plantar else 'nulo  '} {r + 1}/{REPS}  ({time.time() - t0:.0f} s)", flush=True)
            ps = np.array(ps)
            clave = f"{nombre}_{'efecto' if plantar else 'nulo'}"
            # Una prueba «no evaluable» (menos de 5 parejas) no da alarma: cuenta como no detección.
            res["h2"][clave] = {
                "evaluables": int(len(ps)),
                "no_evaluables": no_eval,
                "frac_p_menor_0_01": float(np.sum(ps < 0.01) / REPS),
            }
            print(clave, res["h2"][clave], flush=True)

    n = 3 * N_FRAG  # 900 en el intento 2
    for nombre, efecto_nv, efecto_lx in (("nulo", 0.0, 0.0), ("efecto", 0.10, 0.05)):
        det_nv, det_lx = [], []
        for _ in range(REPS):
            u = rng.beta(2, 5, n)  # propensión de cada fragmento a «sonar a voz» (media ~0,29)
            neutra_nv = rng.random(n) < u
            psico_nv = rng.random(n) < np.minimum(1, u + efecto_nv)
            base_lx = 0.03
            neutra_lx = neutra_nv & (rng.random(n) < base_lx / 0.29)
            psico_lx = psico_nv & (rng.random(n) < (base_lx + efecto_lx) / (0.29 + efecto_nv))
            det_nv.append(mcnemar_unilateral(psico_nv, neutra_nv)["p"] < 0.005)
            det_lx.append(mcnemar_unilateral(psico_lx, neutra_lx)["p"] < 0.005)
        res["h3"][nombre] = {"frac_no_vacia": float(np.mean(det_nv)), "frac_lexico": float(np.mean(det_lx))}
        print("H3", nombre, res["h3"][nombre], flush=True)

    h2 = res["h2"]
    crit = {
        "H2 falsas alarmas <= 2 % (los 3 escenarios)": all(h2[f"{e}_nulo"]["frac_p_menor_0_01"] <= 0.02 for e, _, _ in escenarios),
        "H2 detección >= 90 % (los 3 escenarios)": all(h2[f"{e}_efecto"]["frac_p_menor_0_01"] >= 0.90 for e, _, _ in escenarios),
        "H3 falsas alarmas <= 2 %": res["h3"]["nulo"]["frac_no_vacia"] <= 0.02 and res["h3"]["nulo"]["frac_lexico"] <= 0.02,
        "H3 detección >= 90 %": res["h3"]["efecto"]["frac_no_vacia"] >= 0.90 and res["h3"]["efecto"]["frac_lexico"] >= 0.90,
    }
    res["criterios"] = crit
    res["aprueba"] = all(crit.values())
    res["segundos"] = round(time.time() - t0)
    (RAIZ / "results").mkdir(exist_ok=True)
    (RAIZ / "results/v1.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    for k, v in crit.items():
        print(("APRUEBA " if v else "SUSPENDE") + "  " + k)
    print("V1:", "APRUEBA" if res["aprueba"] else "SUSPENDE", f"({res['segundos']} s)")


if __name__ == "__main__":
    main()
