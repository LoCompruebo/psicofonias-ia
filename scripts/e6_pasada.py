"""Pasada única de E6 (docs/03_e6_plan.md §2). Reanudable. Solo se lanza con results/e6_CONGELADO.txt.
Escribe results/e6/{ia}.jsonl con la transcripción de cada grabación (las IAs nunca ven la frase del autor)."""
import json
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from psicofonias import audio, e6, transcribir  # noqa: E402
from psicofonias.runtime import prioridad_baja  # noqa: E402

if not (RAIZ / "results/e6_CONGELADO.txt").exists():
    raise SystemExit("Falta results/e6_CONGELADO.txt: E6 solo se pasa con el plan congelado.")
prioridad_baja()
salida = RAIZ / "results/e6"
salida.mkdir(parents=True, exist_ok=True)
filas = [f for f in e6.lista() if f["wav"].exists()]
print(len(filas), "grabaciones legibles", flush=True)

for ia in (*transcribir.MODELOS_WHISPER, "vosk"):
    ruta = salida / f"{ia}.jsonl"
    hechos = {json.loads(l)["n"] for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip()} if ruta.exists() else set()
    if ia == "vosk":
        import vosk

        vosk.SetLogLevel(-1)
        modelos = {l: vosk.Model(str(p)) for l, p in e6.RUTAS_VOSK.items()}
        f_t = lambda x, l: transcribir.vosk_transcribir(modelos[l], x)  # noqa: E731
    else:
        m = transcribir.cargar_whisper(ia)
        f_t = lambda x, l: e6.whisper(m, x, l)  # noqa: E731
    t0 = time.time()
    with ruta.open("a", encoding="utf-8") as fh:
        for k, f in enumerate(filas):
            if f["n"] in hechos:
                continue
            x = audio.leer_wav(f["wav"])
            t1 = time.time()
            txt = f_t(x, f["idioma"])
            fh.write(json.dumps({"n": f["n"], "idioma": f["idioma"], "texto": txt, "seg": round(time.time() - t1, 3)}, ensure_ascii=False) + "\n")
            fh.flush()
    print(f"[{ia}] terminado en {time.time() - t0:.0f} s", flush=True)
print("E6 COMPLETA", flush=True)
