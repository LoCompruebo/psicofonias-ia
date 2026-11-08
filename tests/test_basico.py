"""V2: tests unitarios (preregistro §6). Se ejecuta como script: python tests/test_basico.py"""
import math
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from psicofonias import analisis, audio, texto  # noqa: E402

FALLOS = []


def comprobar(nombre, cond):
    print(("OK   " if cond else "FALLO") + "  " + nombre)
    if not cond:
        FALLOS.append(nombre)


# --- texto ---
comprobar("tokens: minúsculas, sin tildes ni signos", texto.tokens("¡Ayúdame, POR favor!") == ["ayudame", "por", "favor"])
comprobar("tokens: quita tokens de 1 letra y números", texto.tokens("y a 3 la casa 2x") == ["la", "casa"])
comprobar("no_vacia: solo signos es vacía", not texto.no_vacia(" ... ¿? ") and not texto.no_vacia(None))
comprobar("jaccard: iguales = 1", texto.jaccard("hola que tal", "Tal, qué hola") == 1.0)
comprobar("jaccard: 1 de 3", abs(texto.jaccard("hola mundo", "hola gente") - 1 / 3) < 1e-12)
comprobar("jaccard: vacía = NaN", math.isnan(texto.jaccard("", "hola")))
comprobar("lexico: detecta ayúdame", texto.contiene_lexico("Ayúdame por favor"))
comprobar("lexico: no cuenta palabras de la instrucción", not texto.contiene_lexico("las voces de la casa abandonada"))
comprobar("lexico: instrucción y léxico no se solapan", not (texto.LEXICO_FANTASMAL & texto.PALABRAS_INSTRUCCION))
comprobar("wer: perfecto = 0", texto.wer("el perro ladra", "El perro ladra.") == 0.0)
comprobar("wer: una sustitución de 3", abs(texto.wer("el perro ladra", "el gato ladra") - 1 / 3) < 1e-12)
comprobar("wer: hipótesis vacía = 1", texto.wer("el perro ladra", "") == 1.0)

# --- frases de control (anexo A) ---
frases = [f.strip() for f in (RAIZ / "data/frases_control.txt").read_text(encoding="utf-8").splitlines() if f.strip()]
comprobar("anexo A: 50 frases", len(frases) == 50)
comprobar("anexo A: de 6 a 12 palabras", all(6 <= len(texto.tokens(f)) <= 12 for f in frases))
comprobar("anexo A: ninguna con palabras del léxico", not any(texto.contiene_lexico(f) for f in frases))
comprobar("anexo A: sin repetidas", len(set(frases)) == 50)

# --- ruido ---
for tipo in audio.TIPOS:
    x = audio.fragmento_principal(tipo, 0)
    comprobar(f"ruido {tipo}: 10 s a 16 kHz", len(x) == 160000)
    comprobar(f"ruido {tipo}: -20 dBFS RMS", abs(20 * np.log10(np.sqrt(np.mean(x**2))) + 20) < 0.01)
    comprobar(f"ruido {tipo}: sin saturar", np.max(np.abs(x)) < 1.0)
    comprobar(f"ruido {tipo}: determinista", np.array_equal(x, audio.fragmento_principal(tipo, 0)))
    f = np.fft.rfftfreq(len(x), 1 / audio.SR)
    P = np.zeros(len(f))
    for k in range(20):  # promedio de 20 fragmentos para estimar la pendiente
        P += np.abs(np.fft.rfft(audio.fragmento_principal(tipo, k))) ** 2
    banda = (f > 50) & (f < 5000)
    pend = np.polyfit(np.log10(f[banda]), np.log10(P[banda]), 1)[0]
    comprobar(f"ruido {tipo}: pendiente espectral {pend:.2f} ~ -{audio.EXPONENTE[tipo]:.0f}", abs(pend + audio.EXPONENTE[tipo]) < 0.1)
a = audio.fragmento_principal("blanco", 0)
b = audio.fragmento_principal("rosa", 0)
comprobar("ruido: tipos distintos no comparten azar", abs(np.corrcoef(a, b)[0, 1]) < 0.05)

# --- mezcla ---
rng = np.random.default_rng(1)
voz = np.sin(2 * np.pi * 440 * np.arange(32000) / audio.SR) * 0.3
fondo = audio.ruido("blanco", rng)
for snr in (20, 0, -10):
    y = audio.mezclar(voz, fondo, snr)
    seg = slice(16000, 48000)
    p_v = np.mean((y[seg] - fondo[seg]) ** 2)
    p_n = np.mean(fondo[seg] ** 2)
    comprobar(f"mezcla: SNR {snr} dB", abs(10 * np.log10(p_v / p_n) - snr) < 0.01)
comprobar("mezcla: el ruido fuera del tramo no cambia", np.array_equal(audio.mezclar(voz, fondo, 0)[:16000], fondo[:16000]))

# --- análisis ---
comprobar("wilson: 0 de 100 empieza en 0", analisis.wilson(0, 100)[0] == 0.0)
lo, hi = analisis.wilson(50, 100)
comprobar("wilson: 50 de 100 ~ [0,40, 0,60]", abs(lo - 0.4038) < 1e-3 and abs(hi - 0.5962) < 1e-3)
r = analisis.mcnemar_unilateral(np.array([1] * 10 + [0] * 90), np.zeros(100))
comprobar("mcnemar: 10 a 0 da p = 0,5^10", abs(r["p"] - 0.5**10) < 1e-12)
comprobar("mcnemar: sin discordantes p = 1", analisis.mcnemar_unilateral(np.ones(5), np.ones(5))["p"] == 1.0)
comprobar("holm: ejemplo", np.allclose(analisis.holm([0.01, 0.04, float("nan"), 0.03]), [0.03, 0.06, float("nan"), 0.06], equal_nan=True))
iguales = ["hola mundo cruel"] * 3 + [f"palabra{i} otra{i}" for i in range(17)]
iguales = [f"frase unica numero {chr(97 + i)}{chr(98 + i)}" for i in range(20)]
r = analisis.h2_permutaciones(iguales, iguales, 2000, np.random.default_rng(2))
comprobar("h2: transcripciones idénticas dan p mínimo", r["evaluable"] and r["p"] < 0.001)
r = analisis.h2_permutaciones(["hola"] * 3 + [""] * 17, ["hola"] * 3 + [""] * 17, 100, np.random.default_rng(3))
comprobar("h2: menos de 5 parejas no es evaluable", not r["evaluable"])

print()
print("TODO BIEN" if not FALLOS else f"{len(FALLOS)} FALLOS: {FALLOS}")
sys.exit(1 if FALLOS else 0)
