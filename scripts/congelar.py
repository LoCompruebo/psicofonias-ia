"""Congela P1: escribe results/CONGELADO.txt con las huellas SHA-256 del plan, el código, las frases, las voces,
el modelo de Vosk y la apuesta de Claude, más las versiones de las librerías. Se ejecuta una sola vez."""
import hashlib
import sys
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "results/CONGELADO.txt"

if DESTINO.exists():
    raise SystemExit("Ya está congelado: no se sobrescribe.")

ficheros = [
    "docs/01_preregistro.md",
    "data/frases_control.txt",
    "results/apuesta_claude.md",
    "results/v1.json",
    "data/raw/vosk_small_es_0.42/SHA256SUMS",
    *sorted(str(p.relative_to(RAIZ)).replace("\\", "/") for p in (RAIZ / "src/psicofonias").glob("*.py")),
    *sorted(str(p.relative_to(RAIZ)).replace("\\", "/") for p in (RAIZ / "scripts").glob("*.py")),
    "scripts/sintetizar_frases.ps1",
    "tests/test_basico.py",
    *sorted(str(p.relative_to(RAIZ)).replace("\\", "/") for p in (RAIZ / "data/generado/voz").glob("*.wav")),
]
lineas = [f"# P1 congelado el {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}", ""]
for f in ficheros:
    lineas.append(f"{hashlib.sha256((RAIZ / f).read_bytes()).hexdigest()}  {f}")
lineas.append("")
lineas.append("# Pesos de Whisper (caché de Hugging Face del usuario)")
cache = Path.home() / ".cache/huggingface/hub"
for tam in ("base", "small", "medium"):
    for p in sorted((cache / f"models--Systran--faster-whisper-{tam}").glob("snapshots/*/model.bin")):
        h = hashlib.sha256()
        with p.open("rb") as fh:
            for bloque in iter(lambda: fh.read(1 << 24), b""):
                h.update(bloque)
        lineas.append(f"{h.hexdigest()}  whisper-{tam}/{p.parent.name}/model.bin")
lineas.append("")
lineas.append("# Versiones")
lineas.append(f"python {sys.version.split()[0]}")
for paquete in ("faster-whisper", "ctranslate2", "numpy", "scipy", "vosk", "nvidia-cublas-cu12", "nvidia-cudnn-cu12"):
    lineas.append(f"{paquete} {version(paquete)}")
DESTINO.write_text("\n".join(lineas) + "\n", encoding="utf-8")
print("\n".join(lineas))
