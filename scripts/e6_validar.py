"""Validación de la medida (c) de E6 con transcripciones inventadas, antes de que ninguna IA escuche nada.

Escenarios (300 repeticiones cada uno, 2000 barajados, semilla 20261114):
  nulo     : cada transcripción es la frase de OTRA grabación del mismo idioma (o vacía con prob. 0,2).
             Imita IAs que escriben frases de verdad pero no la del autor. Criterio: falsas alarmas (p < 0,01) <= 2 %.
  plantado : como el nulo, pero en un 15 % de las grabaciones la transcripción contiene la frase propia.
             Criterio: detección (p < 0,01) >= 90 %.
Escribe results/e6_validacion.json.
"""
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from psicofonias import e6  # noqa: E402

L = e6.lista()
frases = [f["frase_del_autor"] for f in L]
idiomas = [f["idioma"] for f in L]
rng = np.random.default_rng(20261114)
N_REP, N_PERM = 300, 2000


def inventar(plantado: float):
    out = []
    for i, l in enumerate(idiomas):
        if rng.random() < 0.2:
            out.append("")
            continue
        otros = [j for j, m in enumerate(idiomas) if m == l and j != i]
        t = frases[rng.choice(otros)]
        if rng.random() < plantado:
            t = t + " " + frases[i]
        out.append(t)
    return out


res = {}
for nombre, plant in (("nulo", 0.0), ("plantado", 0.15)):
    ps = []
    for r in range(N_REP):
        ps.append(e6.prueba_cobertura(frases, inventar(plant), idiomas, N_PERM, rng)["p"])
        if (r + 1) % 50 == 0:
            print(nombre, r + 1, flush=True)
    ps = np.array(ps)
    res[nombre] = {"frac_p_menor_0_01": float(np.mean(ps < 0.01)), "p_mediana": float(np.median(ps))}
res["aprueba"] = res["nulo"]["frac_p_menor_0_01"] <= 0.02 and res["plantado"]["frac_p_menor_0_01"] >= 0.90
(RAIZ / "results/e6_validacion.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print(json.dumps(res, indent=1))
