# ¿Oye voces una IA en el ruido? (psicofonías)

Materiales del vídeo de **Lo Compruebo** «Le di ruido a una IA y oyó psicofonías»: el plan sellado, el código, los resultados y las fuentes.

## Qué se hizo

1. **P1, preregistrado** (`docs/01_preregistro.md`, congelado el 05-11-2026).
   - **Material:** 900 trozos de 10 s de ruido fabricado por ordenador (blanco, rosa y marrón).
   - **Máquinas:** cuatro IAs de transcripción: Whisper base, small y medium (faster-whisper), y Vosk.
   - **Preguntas:**
     - H1: ¿escriben algo?
     - H2: ¿coinciden en el mismo trozo?
     - H3: ¿cambia lo que escriben si se les dice antes que es una psicofonía?
   - **Resultados:** `docs/02_resultados.md`.
2. **E6, exploratorio** (`docs/03_e6_plan.md`, congelado el 08-11-2026).
   - **Material:** 101 psicofonías reales con licencia libre, escuchadas sin conocer la frase que dice su autor.
   - **Resultados:** `docs/04_e6_resultados.md`.

## Cómo comprobar que nada cambió después de congelar

- `results/CONGELADO.txt` y `results/e6_CONGELADO.txt` guardan la huella SHA-256 de cada fichero en el momento de congelar.
- **Con cualquier herramienta de SHA-256** (`sha256sum` o `certutil -hashfile <fichero> SHA256`), compara las huellas de los ficheros incluidos aquí con esas listas.
- **Las predicciones de la IA**, selladas antes de cada pasada, son `results/apuesta_claude.md` y `results/e6_apuesta_claude.md`. Sus huellas están dentro de esas listas.

## Qué NO se incluye, y por qué

- **El audio de terceros:**
  - de las psicofonías reales solo hay enlaces, autores y licencias (`SOURCES.md` y `atribuciones_e6.csv`), más las huellas del audio original (`data/raw/e6/SHA256SUMS_audio`) para poder verificarlo tras descargarlo de su fuente;
  - las transcripciones automáticas de esas grabaciones sí están (`results/e6/`, `results/e6_analisis.json`), porque son el resultado del análisis.
- **Los modelos de reconocimiento** (Vosk y Whisper): se descargan de sus fuentes oficiales. La procedencia y las huellas están en `data/raw/*/`.
- **Las voces sintéticas** de las 50 frases de control: se regeneran con `scripts/sintetizar_frases.ps1`, que usa la voz «Helena» de Windows. Sus huellas están en `results/CONGELADO.txt`.
- **El ruido** no hace falta guardarlo: se regenera bit a bit con las semillas de `src/psicofonias/audio.py`. Los cinco trozos exportados para el vídeo están en `video/clips/` (en el montaje final suenan cuatro: `rosa_105` se quedó fuera), con su huella comprobada contra la pasada real (`scripts/exportar_clips_video.py`).

## Avisos de lectura

- **Lo que esto no demuestra:** que las psicofonías sean falsas. Enseña un mecanismo: una máquina rellena el silencio con lo que aprendió y se deja sugestionar.
- **Desviaciones y comprobaciones a posteriori:** están en `docs/01_preregistro_desviaciones.md` (aparte, para no romper la huella del plan congelado) y en `docs/02_resultados.md` §6 y §8, incluidas dos correcciones de cifras hechas el 08-11.
- **Entorno:** Python 3.12, faster-whisper 1.2.1, ctranslate2 4.8.2 y vosk 0.3.45. Las versiones exactas están en `results/CONGELADO.txt`.

## Licencias

- **Código** (`src/`, `scripts/`, `tests/`): MIT (`LICENSE`).
- **Documentos, resultados y los cinco clips de ruido** (`docs/`, `results/`, `video/clips/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es), citando «Lo Compruebo».
- **Las psicofonías de terceros** no están aquí y conservan su licencia original: cada una se enlaza en `SOURCES.md` con su autor y su licencia.

## El vídeo

«Puse a prueba a una IA con psicofonías y oyó voces»: https://youtu.be/dVDfw9QwUsE (público desde el sábado 14-11-2026 a las 18:00, hora de España).
