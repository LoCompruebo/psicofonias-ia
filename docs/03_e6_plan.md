# E6: psicofonías reales, a ciegas (plan v1.0; se congela antes de que ninguna IA escuche nada)

**Estado:** exploratorio. Lo pidió el usuario (05-11) y lo encargó el 08-11 («Sí, búscalas»). El preregistro P1 ya estaba congelado, así que E6 no puede ser una hipótesis principal: es exploratorio, con sus reglas fijadas aquí antes de procesar ningún audio.

## 1. Material (`data/e6_candidatas.csv`)

- **Búsqueda del 08-11-2026:** Freesound (EVP, psicofonía, «electronic voice phenomenon», «spirit box») e Internet Archive (las mismas palabras, solo audio y solo con licencia).
- **Reglas de selección**, fijadas antes de escuchar nada:
  1. licencia Creative Commons, CC0 o dominio público declarada en la ficha;
  2. el autor dice qué frase contiene, en el título, la descripción o el nombre del fichero;
  3. una sola grabación por fichero (se quitan los duplicados);
  4. fuera las versiones en bucle, las invertidas y los montajes que el propio autor declara fabricados;
  5. fuera los programas de radio y los pódcast.
- **Resultado: 102 grabaciones**, 5 en español y 97 en inglés, de 0,5 a 23,5 s y 19,2 MB en total.
  - Internet Archive: 72 ficheros originales, 16,8 MB.
  - Freesound: 30 «previas» de alta calidad (MP3 a 128 kbps), 2,4 MB. Se usan las previas porque el original exige una cuenta, y no se crean cuentas.
- **Sesgo conocido:** 58 de las 102 son de un mismo grupo de Misisipi (MSSPI), 13 de Todd_Bates, 8 de Soulwriter y 6 de southlandghosthunter (grupos fijados en `src/psicofonias/e6.py`, `grupo()`). Se informará también por grupo.
- **Derechos:**
  - Solo se analizan. Ningún audio ajeno se publica en el vídeo, como mucho se describe (decisión del 05-11).
  - Varias licencias son «sin obras derivadas» o «no comercial»: analizar no es publicar, pero por eso mismo no se reproducen.
  - Cada fichero llevará su autor, licencia y URL en `data/raw/e6/PROVENANCE.md`.

## 2. Procedimiento

- **Formato:** cada audio se convierte a 16 kHz mono (ffmpeg, ya instalado). No se normaliza ni se filtra.
- **IAs:**
  - Whisper base, small y medium, con los ajustes de P1, **sin instrucción inicial** y con el idioma fijado al de la lista (en o es).
  - Vosk, con el modelo del idioma: el español que ya tenemos y, si el usuario permite descargarlo, el inglés pequeño (`vosk-model-small-en-us-0.15`, unos 40 MB, Apache 2.0). Sin él, Vosk solo escucha las 5 en español.
- **Pasada única.** Cuesta unos minutos de GPU.
- **Las IAs no ven nunca la frase del autor.**

## 3. Medidas

- **(a) ¿Escribe algo?:** la fracción de grabaciones con una transcripción no vacía, por IA.
- **(b) ¿Coinciden las IAs?:** la J de Jaccard por parejas (como en H2), comparada con:
  - el ruido puro de P1;
  - los controles de voz de P1;
  - la misma J con las grabaciones barajadas (10.000 permutaciones, semilla 20261112).
- **(c) ¿Escriben la frase del autor?** (la medida clave)
  - **Cobertura:** la fracción de palabras de la frase del autor que aparecen en la transcripción, normalizadas como en P1.
  - **«Acierto»** si la cobertura es ≥ 0,5. También se da la J ≥ 0,5 del preregistro §9.
  - **Nulo:** la misma cobertura, pero con la frase de **otra** grabación (10.000 barajados, semilla 20261113). Así se descuentan los aciertos por palabras comunes («you», «me», «get»).
  - **p de una cola** por IA, con Holm sobre las IAs evaluadas.

## 4. Lectura (fijada antes)

- **Las grabaciones llevan también la voz de los investigadores** (la pregunta antes de la «respuesta»). Por eso (a) y (b) saldrán altas aunque la «voz del más allá» no exista. La medida que decide es (c).
- **Si las IAs escriben la frase del autor bastante más que la frase de otra grabación**, en esas grabaciones hay algo con forma de esa voz. Eso **no dice de dónde viene**: puede ser una persona cerca, una radio («spirit box») o un montaje.
- **Si no**, encaja con la pareidolia: el autor oyó lo que esperaba, y una máquina sin expectativas no lo oye.
- Se informa:
  - por grupo de autores;
  - por tipo de grabación: grabadora o «spirit box», cuando la ficha lo dice.

## 5. Apuesta de Claude

`results/e6_apuesta_claude.md`, sellada con SHA-256 en `results/e6_CONGELADO.txt` antes de la pasada.

## 6. Hecho antes de congelar (08-11)

- **Descargas** (con permiso del usuario: «Sí, las dos cosas»):
  - las 102 grabaciones, en `data/raw/e6/audio/NNN.ext`, con sus huellas en `data/raw/e6/SHA256SUMS_audio`;
  - Vosk inglés, en `data/raw/vosk_small_en_0.15/` (41.205.931 bytes, que coincide con el tamaño publicado).
- **Conversión a 16 kHz mono** (`data/generado/e6_16k/`):
  - salen 101 de 102;
  - **la 024 («Fred», 648 bytes) no se puede leer**: su cabecera no dice cuántos canales tiene y ffmpeg la rechaza. Se excluye, con la regla «si no se puede leer, fuera», fijada antes de transcribir nada.
- **Validación de (c) con transcripciones inventadas** (`scripts/e6_validar.py`, `results/e6_validacion.json`; 300 repeticiones):
  - falsas alarmas: 0 %;
  - detección de un efecto plantado en el 15 % de las grabaciones: 96 %.
  - **Aprueba** (criterios: ≤ 2 % y ≥ 90 %).
- **Prueba de fontanería del análisis** con transcripciones falsas, fuera de `results/`. Funciona.
- **Código:** `src/psicofonias/e6.py`, `scripts/e6_pasada.py` y `scripts/e6_analizar.py`.
