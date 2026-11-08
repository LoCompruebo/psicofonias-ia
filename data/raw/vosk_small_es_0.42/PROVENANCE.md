# Procedencia: Vosk, modelo pequeño en español 0.42

- **Qué es:** el modelo de reconocimiento de voz en español de Vosk (Kaldi, una familia distinta de Whisper). Es la segunda IA de H2 (`docs/01_preregistro.md` §3).
- **URL:** https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
- **Página del catálogo:** https://alphacephei.com/vosk/models [V]. Da 39 MB, licencia **Apache 2.0** y un WER del 16,02 en Common Voice.
- **Descargado:** 2026-11-05T17:48:06Z con `curl`, HTTP 200, **39.817.833 bytes**.
- **SHA-256 del zip:** `09b239888f633ef2f0b4e09736e3d9936acfd810bc65d53fad45261762c6511f`
- **Extraído** con `extraer_zip.py` (`python -I`), que comprueba que ninguna ruta se salga de la carpeta. Son 14 ficheros, todos de datos (pesos, grafos y configuración), sin código ejecutable. Sus huellas están en `SHA256SUMS`.
- **README del modelo:** «Copyright 2022-2050 AC Technologies LLC», con sus tablas de WER. La licencia la da el catálogo.
- **Autorizado por el usuario** el 05-11-2026 («Sí, descárgalo»).

## Programa instalado (no está en esta carpeta)

- **Paquetes:** `vosk==0.3.45` (rueda `vosk-0.3.45-py3-none-win_amd64.whl`, de PyPI) y su dependencia `srt==3.5.3` (MIT).
- **Dónde:** en el Python del sistema (Windows, Python 3.12).
- **Tamaño:** unos 53 MB en disco, porque incluye `libvosk.dll` y las librerías de C++.
- **Licencia:** el proyecto vosk-api es Apache 2.0 [V*]; el campo de licencia del paquete viene vacío («UNKNOWN»).
- **Prueba de carga** (05-11): el modelo carga en 0,6 s y crea el reconocedor a 16 kHz. **No se le ha pasado ningún audio.**
