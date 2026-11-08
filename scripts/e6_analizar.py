"""Análisis de E6 (docs/03_e6_plan.md §3). Lee results/e6/*.jsonl y escribe results/e6_analisis.json."""
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from psicofonias import analisis, e6, texto  # noqa: E402

IAS = ("base", "small", "medium", "vosk")
filas = {f["n"]: f for f in e6.lista()}
tr = {}
for ia in IAS:
    ruta = (Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "results/e6") / f"{ia}.jsonl"
    tr[ia] = {r["n"]: r["texto"] for r in (json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip())}
ns = sorted(set.intersection(*(set(t) for t in tr.values())))
res = {"n": len(ns), "excluidas": sorted(set(filas) - set(ns)), "a": {}, "b": {}, "c": {}, "c_por_grupo": {}, "por_grabacion": []}

# (a) no vacías
for ia in IAS:
    k = sum(texto.no_vacia(tr[ia][n]) for n in ns)
    res["a"][ia] = {"no_vacias": k, "frac": k / len(ns), "ic95": analisis.wilson(k, len(ns))}

# (b) acuerdo entre IAs, con barajado
rng = np.random.default_rng(20261112)
for a, b in combinations(IAS, 2):
    res["b"][f"{a}-{b}"] = analisis.h2_permutaciones([tr[a][n] for n in ns], [tr[b][n] for n in ns], 10000, rng)
pb = analisis.holm([v["p"] for v in res["b"].values()])
for k, p in zip(res["b"], pb):
    res["b"][k]["p_holm"] = p

# (c) cobertura de la frase del autor, frente a la de otra grabación del mismo idioma
rng = np.random.default_rng(20261113)
frases = [filas[n]["frase_del_autor"] for n in ns]
idiomas = [filas[n]["idioma"] for n in ns]
for ia in IAS:
    res["c"][ia] = e6.prueba_cobertura(frases, [tr[ia][n] for n in ns], idiomas, 10000, rng)
    res["c"][ia]["jaccard_0_5"] = int(sum((e6.jaccard_frase(frases[i], tr[ia][n]) or 0) >= 0.5 for i, n in enumerate(ns)))
pc = analisis.holm([res["c"][ia]["p"] for ia in IAS])
for ia, p in zip(IAS, pc):
    res["c"][ia]["p_holm"] = p
# por grupo (descriptivo): aciertos de cobertura >= 0,5
for g in sorted({e6.grupo(filas[n]) for n in ns}):
    idx = [n for n in ns if e6.grupo(filas[n]) == g]
    res["c_por_grupo"][g] = {"n": len(idx), **{ia: sum(e6.cobertura(filas[n]["frase_del_autor"], tr[ia][n]) >= 0.5 for n in idx) for ia in IAS}}
# alguna IA acierta / todas aciertan
cov = {ia: {n: e6.cobertura(filas[n]["frase_del_autor"], tr[ia][n]) for n in ns} for ia in IAS}
res["alguna_acierta"] = sum(any(cov[ia][n] >= 0.5 for ia in IAS) for n in ns)
res["todas_aciertan"] = sum(all(cov[ia][n] >= 0.5 for ia in IAS) for n in ns)
for n in ns:
    res["por_grabacion"].append({"n": n, "frase": filas[n]["frase_del_autor"], "grupo": e6.grupo(filas[n]),
                                 **{ia: tr[ia][n] for ia in IAS}, **{f"cob_{ia}": round(cov[ia][n], 2) for ia in IAS}})
res["frases_mas_repetidas"] = {ia: Counter(" ".join(texto.tokens(tr[ia][n])) for n in ns if texto.no_vacia(tr[ia][n])).most_common(10) for ia in IAS}
(RAIZ / "results/e6_analisis.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
print(json.dumps({k: res[k] for k in ("n", "excluidas", "a", "c", "c_por_grupo", "alguna_acierta", "todas_aciertan")}, indent=1, ensure_ascii=False, default=float))
