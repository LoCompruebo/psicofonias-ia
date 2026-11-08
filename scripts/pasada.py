"""Pasada de P1 (preregistro §4). Se puede cortar y reanudar: cada transcripción se guarda al momento.

Etapas, en este orden:
  v0         : 50 frases x 6 relaciones señal/ruido x 4 IAs (el «oído»). Si medium tiene WER > 15 % a +20 dB, se para.
  controles  : 50 frases a +10 dB x 4 IAs.
  ruido      : 900 fragmentos de ruido x 4 IAs, sin instrucción.
  h3_neutra  : 900 fragmentos x Whisper medium con la instrucción neutra.
  h3_psico   : 900 fragmentos x Whisper medium con la instrucción de psicofonía.

Uso:
  python -u scripts/pasada.py            -> la pasada real (solo después de congelar)
  python -u scripts/pasada.py --prueba   -> prueba de fontanería SIN RUIDO: 3 frases limpias en lugar de cada audio,
                                            a results/prueba_fontaneria/ (no cuenta para nada)
"""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from psicofonias import audio, texto, transcribir  # noqa: E402
from psicofonias.runtime import prioridad_baja  # noqa: E402

N_POR_TIPO = 300
SNRS_V0 = (20, 10, 0, -5, -10, -20)
SNR_CONTROLES = 10
INSTRUCCION = {
    "h3_neutra": "Grabación de ruido de fondo en una habitación.",
    "h3_psico": "Psicofonía grabada en una casa abandonada. Las voces de los espíritus dicen:",
}
IAS = (*transcribir.MODELOS_WHISPER, "vosk")


def frases():
    return [f.strip() for f in (RAIZ / "data/frases_control.txt").read_text(encoding="utf-8").splitlines() if f.strip()]


def voz(i):
    return audio.leer_wav(RAIZ / f"data/generado/voz/frase_{i:02d}.wav")


def cuantizar(x):
    """Lo que recibe la IA es exactamente lo que habría en un WAV de 16 bits."""
    q = audio.a_int16(x)
    return q.astype(np.float64) / 32767, hashlib.sha256(q.tobytes()).hexdigest()


def audios(etapa, prueba):
    """Genera (id, audio, extra) de cada etapa, de forma determinista."""
    if prueba:
        for i in range(3):
            x, h = cuantizar(np.concatenate([np.zeros(audio.SR), voz(i), np.zeros(audio.SR)]))
            yield f"prueba_{i}", x, {"sha256": h, "ref": frases()[i]}
        return
    fr = frases()
    if etapa == "v0":
        for k, snr in enumerate(SNRS_V0):
            for i in range(50):
                fondo = audio.ruido("blanco", audio.rng_para(audio.SEMILLA_V0, k, i))
                x, h = cuantizar(audio.limitar_pico(audio.mezclar(voz(i), fondo, snr)))
                yield f"v0_{snr:+d}_{i:02d}", x, {"sha256": h, "ref": fr[i], "snr": snr}
    elif etapa == "controles":
        for i in range(50):
            fondo = audio.ruido("blanco", audio.rng_para(audio.SEMILLA_CONTROLES, 0, i))
            x, h = cuantizar(audio.limitar_pico(audio.mezclar(voz(i), fondo, SNR_CONTROLES)))
            yield f"control_{i:02d}", x, {"sha256": h, "ref": fr[i]}
    else:
        for tipo in audio.TIPOS:
            for i in range(N_POR_TIPO):
                x, h = cuantizar(audio.fragmento_principal(tipo, i))
                yield f"{tipo}_{i:03d}", x, {"sha256": h, "tipo": tipo}


def hechos(ruta):
    if not ruta.exists():
        return set()
    return {json.loads(l)["id"] for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip()}


def correr(etapa, ia, salida, prueba):
    ruta = salida / f"{etapa}__{ia}.jsonl"
    ya = hechos(ruta)
    total = (3 if prueba else {"v0": 300, "controles": 50}.get(etapa, 3 * N_POR_TIPO))
    if len(ya) >= total:
        print(f"[{etapa} / {ia}] ya hecho ({len(ya)})", flush=True)
        return
    if ia == "vosk":
        m = transcribir.cargar_vosk()
        f = lambda x: transcribir.vosk_transcribir(m, x)  # noqa: E731
    else:
        m = transcribir.cargar_whisper(ia)
        ins = INSTRUCCION.get(etapa)
        f = lambda x: transcribir.whisper(m, x, initial_prompt=ins)  # noqa: E731
    t0, n = time.time(), 0
    with ruta.open("a", encoding="utf-8") as fh:
        for ident, x, extra in audios(etapa, prueba):
            if ident in ya:
                continue
            t1 = time.time()
            txt = f(x)
            fh.write(json.dumps({"id": ident, "texto": txt, "seg": round(time.time() - t1, 3), **extra}, ensure_ascii=False) + "\n")
            fh.flush()
            n += 1
            if n % 50 == 0:
                print(f"[{etapa} / {ia}] {len(ya) + n}/{total}  ({time.time() - t0:.0f} s)", flush=True)
    print(f"[{etapa} / {ia}] terminado: {len(ya) + n}/{total} en {time.time() - t0:.0f} s", flush=True)
    del m


def criterio_v0(salida):
    """WER medio de medium a +20 dB <= 15 %."""
    filas = [json.loads(l) for l in (salida / "v0__medium.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    w = [texto.wer(r["ref"], r["texto"]) for r in filas if r["snr"] == 20]
    return float(np.mean(w))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prueba", action="store_true")
    a = ap.parse_args()
    prioridad_baja()
    if a.prueba:
        salida = RAIZ / "results/prueba_fontaneria"
        salida.mkdir(parents=True, exist_ok=True)
        for etapa in ("controles", "h3_psico"):
            for ia in (IAS if etapa == "controles" else ("medium",)):
                correr(etapa, ia, salida, True)
        return
    if not (RAIZ / "results/CONGELADO.txt").exists():
        raise SystemExit("No hay results/CONGELADO.txt: la pasada real solo se lanza con el preregistro congelado.")
    salida = RAIZ / "results/pasada"
    salida.mkdir(parents=True, exist_ok=True)
    for ia in IAS:
        correr("v0", ia, salida, False)
    w = criterio_v0(salida)
    print(f"V0: WER de medium a +20 dB = {w:.3f} (criterio <= 0,15)", flush=True)
    if w > 0.15:
        raise SystemExit("V0 SUSPENDE: el montaje está roto. Se para (preregistro §6).")
    for etapa in ("controles", "ruido"):
        for ia in IAS:
            correr(etapa, ia, salida, False)
    for etapa in ("h3_neutra", "h3_psico"):
        correr(etapa, "medium", salida, False)
    print("PASADA COMPLETA", flush=True)


if __name__ == "__main__":
    main()
