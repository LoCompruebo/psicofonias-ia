# Preregistro P1: ¿oye voces una IA en el ruido? (v1.0, CONGELADO)

- **Estado:** **v1.0, CONGELADO el 05-11-2026** con el visto bueno del usuario («Sí, congela y lanza»). Huellas en `results/CONGELADO.txt`. Cualquier cambio desde ahora va a §13 como desviación. (Texto de la v0.2:) Ninguna IA de transcripción ha procesado todavía ningún ruido. Solo se han pasado por ellas, para medir la velocidad, las frases de control limpias, sin ruido (§7). Los cambios desde la v0.1 están en §11. Se congela cuando estén las respuestas a §10 y el código haya aprobado la validación con datos inventados (§6, partes V1 y V2). Las huellas irán en `results/CONGELADO.txt`.
- **Autor de las decisiones:** el asistente, como jefe de proyecto. La idea es del asistente (tabla única, 04-11) y la elección, del usuario («Psicofonías», 05-11).

## 0. Por qué esta prueba (el hueco)

| Trabajo | Qué hizo | Qué deja libre |
|---|---|---|
| Raudive y otros (años 70) | Grabaron «voces» en ruido de radio y cinta [NV en detalle] | Nunca hubo un control ciego |
| Williams y Blagrove (PLOS ONE, 2022) [V*] | 61 personas. Avisar de que son «voces de fantasmas» hace oír más voces. En las psicofonías, **solo un 13 % coincide en lo que dicen, frente al 95 % con voz real** (The Conversation) [V*] | Las máquinas |
| Alucinaciones de Whisper (Cornell 2024; arXiv 2501.11378, 2025) [V*] | Whisper inventa frases en el silencio y en sonidos sin voz | Nadie lo ha unido a las psicofonías, ni ha medido el acuerdo entre IAs ni el efecto de la sugestión |

**Lo nuevo:**
1. Medir cuántas «voces» oyen varias IAs en un ruido puro que sabemos con certeza que no tiene voz, porque lo fabricamos nosotros.
2. Medir si **coinciden entre ellas** en lo que oyen, que es el mismo dato del estudio con personas.
3. Medir si **sugestionar a la IA** le hace oír más voces y más «fantasmales».

## 1. Preguntas e hipótesis

- **H1, las voces en el ruido:** ¿qué fracción de los fragmentos de ruido puro producen una transcripción no vacía?
  - Es una medida descriptiva, con su intervalo del 95 %.
  - **Afirmación preregistrada:** «la IA oye voces en el ruido» si, para al menos un modelo y un tipo de ruido, el límite inferior del intervalo supera el 5 %.
- **H2, ¿coinciden las IAs?:** para cada pareja de modelos, ¿se parecen más las transcripciones de un **mismo** fragmento de ruido que las de fragmentos **distintos**?
  - El parecido se mide con la J de Jaccard sobre palabras, en §5.
  - **Positivo** si p < 0,01 (una cola, permutaciones).
  - **Lectura:** si es positivo, el ruido «empuja» a las IAs hacia las mismas palabras, y eso pediría una explicación. Si es nulo, cada IA oye lo suyo, como les pasa a las personas con las psicofonías.
- **H3, la sugestión:** con Whisper medium y los mismos fragmentos, ¿aumentan las transcripciones no vacías y las palabras del léxico «fantasmal» (§5) con la instrucción de psicofonía, frente a la neutra?
  - Prueba de McNemar con los mismos fragmentos, una cola.
  - **Positivo** si p < 0,01 en cualquiera de las dos medidas, corregido por haber probado dos (Holm).

## 2. Audios (todos nuestros; no se descarga ningún audio)

- **Ruido**, en `data/generado/`, a 16 kHz, mono, 10 s por fragmento y normalizado a −20 dBFS de media cuadrática:
  - **blanco:** gaussiano;
  - **rosa:** 1/f;
  - **marrón:** 1/f², parecido al rumor grave de una habitación.
  - **N = 300 fragmentos por tipo** (900 en total). Antes eran 200: se cambió por la potencia, ver §11.
  - **Semillas:** cada fragmento usa `SeedSequence([20261105, tipo, índice])`. Así, los tres tipos no comparten el mismo azar.
- **Controles de voz real:** 50 frases neutras en español, escritas en el anexo A antes de generar nada y leídas con la voz sintética «Microsoft Helena Desktop» de Windows (SAPI).
  - Se mezclan con ruido blanco nuevo (`SeedSequence([20261106, 0, índice])`) a +10 dB de relación señal/ruido. La voz empieza en el segundo 1 de un fragmento de 10 s.
  - Si la mezcla pasa de 0,9 de pico, se baja entera, voz y ruido a la vez, hasta 0,9 (`limitar_pico`), como haría una grabadora. Esto no cambia la relación señal/ruido.
  - Dan el parecido que hay «cuando de verdad hay voz».
- **Opcional (exploratorio E2):** grabaciones del usuario en una habitación vacía con el móvil. Solo si el usuario quiere, y nunca en la pasada principal.

## 3. Modelos y ajustes (fijos)

- **Whisper base, small y medium** (faster-whisper 1.2.1, pesos de Systran ya en el ordenador).
  - GPU, con `compute_type="int8_float16"` en los tres para que quepan en 6 GB y se traten igual.
  - **Ajustes por defecto de la librería**, como los usaría cualquiera: haz de 5, temperaturas 0,0 a 1,0, sin filtro de voz (VAD), `condition_on_previous_text=True` y umbrales por defecto.
  - **Idioma forzado:** `language="es"`, porque las psicofonías que se cuentan en España son en español. Con detección automática, solo exploratorio (E3).
- **Vosk, modelo pequeño en español 0.42** (39,8 MB, Apache 2.0 [V]), **descargado el 05-11** con permiso (`data/raw/vosk_small_es_0.42/`, SHA-256 en su PROVENANCE). Funciona con `vosk==0.3.45` en CPU (un proceso), a 16 kHz y con los ajustes por defecto (`KaldiRecognizer`, resultado final de cada fragmento). Es de otra familia (Kaldi, no transformer).
- **Las semillas, los modelos y las versiones** se escriben en `results/CONGELADO.txt`.

## 4. Procedimiento

1. Generar los audios (§2) y guardar sus SHA-256.
2. **V0, el oído de las IAs** (§6): voz sintética mezclada con ruido a varias relaciones señal/ruido.
3. **Pasada principal**, una sola: cada modelo transcribe los 900 fragmentos de ruido y los 50 controles. Para H3, Whisper medium transcribe además los 900 fragmentos con las dos instrucciones. Whisper va en la GPU; Vosk, en la CPU, con un solo proceso.
4. Análisis fijado en §5. Las transcripciones se guardan en bruto, sin limpiar, en `results/`.

## 5. Medidas y pruebas

- **Normalización del texto:**
  - minúsculas, sin tildes ni signos;
  - se separa por espacios;
  - solo cuentan los tokens de letras con 2 o más caracteres.
  - Una transcripción es **«no vacía»** si le queda al menos uno.
- **H1:** fracción de fragmentos no vacíos por modelo y tipo de ruido, con el intervalo de Wilson al 95 %.
- **H2:**
  - Para cada pareja de modelos y tipo de ruido, el estadístico es la J media de Jaccard (conjuntos de tokens) en los fragmentos en los que **las dos** transcripciones son no vacías.
  - **Nulo:** se barajan los fragmentos del segundo modelo dentro del mismo tipo de ruido, con 10.000 permutaciones. p = (1 + número de veces que el barajado ≥ el observado) / 10.001.
  - **Familias de pruebas:**
    - entre hermanos: base–small, base–medium y small–medium;
    - entre familias: cada Whisper con Vosk, si se aprueba.
    - Se corrige por todas las parejas y tipos de ruido (Holm).
  - **Referencia:** la misma J en los 50 controles de voz.
- **H3:**
  - **Tres condiciones de instrucción inicial** (`initial_prompt`):
    - ninguna;
    - neutra: «Grabación de ruido de fondo en una habitación.»;
    - psicofonía: «Psicofonía grabada en una casa abandonada. Las voces de los espíritus dicen:».
  - **Medida 1:** no vacía (sí o no).
  - **Medida 2:** contiene alguna palabra del **léxico fantasmal**, fijado aquí: muerte, muerto, muertos, ayuda, ayudame, socorro, vete, fuera, alma, almas, dios, diablo, demonio, infierno, sangre, frio, miedo, oscuridad, auxilio, perdon, matar, mataron, tumba, cielo.
    - Las palabras de la propia instrucción (psicofonia, grabada, casa, abandonada, voces, espiritus, dicen) **no cuentan**: así no se puntúa a la IA por copiar la instrucción.
  - **Comparación preregistrada:** psicofonía frente a neutra, con McNemar exacto de una cola. La condición sin instrucción es descriptiva.

## 6. Validación antes de la pasada real

- **V1, el análisis con transcripciones inventadas** (sin audio ni IA):
  - **Código:** `scripts/validar_v1.py`; resultado en `results/v1.json`.
  - **H2:** 500 repeticiones por escenario, con N fragmentos por tipo y 10.000 permutaciones.
    - **Nulo:** cada «modelo» transcribe por su cuenta, sin relación con el otro. Hay tres escenarios: pocas transcripciones no vacías (5 %), muchas (30 %), y muchas con el 90 % sacado de una bolsa común de 20 «alucinaciones típicas» con pesos de Zipf, que es el caso difícil.
    - **Efecto escondido:** en el 10 % de los fragmentos, los dos «modelos» escriben la misma frase.
    - **Criterios:** falsas alarmas (p < 0,01) ≤ 2 % y detección ≥ 90 %, en los tres escenarios. Una prueba «no evaluable» (menos de 5 parejas no vacías) cuenta como «no alarma».
  - **H3:** McNemar con 3·N fragmentos y umbral 0,005, el más exigente de Holm con 2 pruebas.
    - **Nulo:** la misma probabilidad con las dos instrucciones, que varía por fragmento según una Beta(2, 5).
    - **Efecto:** +10 puntos en «no vacía» y +5 puntos en el léxico, sobre una base del 3 %.
    - **Criterios:** falsas alarmas ≤ 2 % y detección ≥ 90 % en cada medida.
- **V2, comprobación del programa:** los tests unitarios de la normalización, del Jaccard y del barajado.
- **V0, el oído** (se ejecuta como paso 2 de §4, después de congelar):
  - Las 50 frases mezcladas con ruido blanco **de otras semillas** (`SeedSequence([20261107, nivel, índice])`) a +20, +10, 0, −5, −10 y −20 dB, con la voz desde el segundo 1 y `limitar_pico`.
  - Se mide el error de palabras (WER) de cada modelo.
  - **Criterio:** WER de medium ≤ 15 % a +20 dB. Si no se cumple, el montaje está roto: se para y se corrige como desviación.
  - Además, da el **«límite de oído»**: la relación señal/ruido a la que el WER pasa del 50 %.
  - Nada de V0 sirve para cambiar los ajustes de §3.

## 7. Coste

- Prepararlo cuesta cuota de Claude: el código y esta revisión.
- Calcular es trabajo de la GPU, sin cuota.
- La velocidad real se medirá con voz sintética **sin ruido** antes de congelar, para decidir N con datos. **Estimación:** de 1 a 3 horas de GPU en total [NV]. Se pedirá permiso antes de lanzarlo.

## 8. Lectura y límites

- **Esto no prueba que las psicofonías sean falsas.** Muestra si una máquina, sin creencias, «oye» voces en un ruido que sabemos vacío, y si esas voces se parecen entre máquinas.
- **Las IAs aprendieron de subtítulos humanos.** Si salen frases típicas de subtítulos («gracias por ver el vídeo», «subtítulos de la comunidad…»), es una pista de dónde salen esas «voces». Se cuenta como hallazgo **exploratorio** (E4: las 20 frases más repetidas).
- **Ruido sintético:** el ruido de una grabadora real es distinto, y por eso existe E2.
- **Vosk** es un modelo pequeño (WER del 16 % en Common Voice): oye peor que Whisper medium, y eso pesa al comparar acuerdos entre familias.

## 9. Exploratorio (no cambia el veredicto; cada regla, fijada aquí)

- **E1, Claude intérprete:**
  - Se eligen al azar (semilla 20261108) 30 transcripciones no vacías de ruido de Whisper medium sin instrucción.
  - Para cada una, Claude recibe: «Eres investigador de psicofonías. Esta es la transcripción de una grabación. ¿Qué mensaje transmite y de quién podría ser?».
  - Otra instancia de Claude, a ciegas, puntúa de 1 a 5 lo convincente de cada interpretación. Las mezcla con 30 interpretaciones de **cadenas de palabras al azar** del mismo largo, sacadas de los controles de voz.
  - **Medida:** diferencia de medias. **Pregunta:** ¿construye la IA tanto «significado» desde el ruido como desde palabras al azar?
- **E2:** las grabaciones del usuario, si las hay.
- **E3:** la detección automática de idioma.
- **E4:** las 20 frases más repetidas en el ruido, por modelo.
- **E6, psicofonías reales, a ciegas** (pregunta del usuario, 05-11; se puede ascender a hipótesis H4 si antes de congelar se reúnen al menos 20 grabaciones con licencia clara):
  - **Fuentes, por orden:**
    1. grabaciones con licencia libre (Creative Commons o dominio público), por ejemplo en Freesound o en Internet Archive [NV: falta ver qué hay];
    2. las famosas, solo si se pueden conseguir de forma legal. **No se descarga de YouTube**, porque sus condiciones lo prohíben. Ningún audio ajeno se publica en el vídeo; como mucho, un fragmento corto citado con su autor.
  - Cada grabación se apunta con la frase que dice contener su autor, **pero las IAs no la ven** (sin instrucción inicial, igual que en H1).
  - **Medidas:**
    - (a) si las IAs escriben algo;
    - (b) si coinciden entre ellas (la J de H2), comparado con el ruido puro y con los controles de voz;
    - (c) si alguna escribe la frase que dice su autor, con un parecido de Jaccard ≥ 0,5.
  - **Lectura fijada antes:**
    - Si las IAs coinciden entre sí bastante más que en el ruido puro, en esa grabación hay algo con forma de voz. Eso **no dice de dónde viene**: puede ser una persona cerca, una emisora de radio o un montaje.
    - Si no coinciden, o no escriben la frase del autor, encaja con la pareidolia.
  - Se descarga solo con permiso del usuario, con nombre, origen, tamaño y licencia, y cada grabación lleva su `PROVENANCE.md`.
- **E5, «la IA apuesta»:** antes de la pasada real, Claude escribe su predicción de H1, H2 y H3 con probabilidades. Se sella con SHA-256 y se puntúa con Brier.

## 10. Pendiente antes de congelar

1. ~~Permiso para descargar Vosk~~: **hecho el 05-11** (modelo de 39,8 MB y paquete `vosk` 0.3.45).
2. Escribir el anexo A (las 50 frases), los generadores de ruido, el análisis y los tests.
3. Pasar V1 y V2.
4. Medir la velocidad con voz sintética sin ruido.
5. ~~Revisar la potencia de H3~~: hecho. El intento 1 de V1 la vio corta con 200 por tipo y se subió a 300 (§11).

## Anexo A: las 50 frases de control

Se escribirán antes de generar ningún audio, con estas reglas:
- frases neutras de la vida diaria, de 6 a 12 palabras;
- sin ninguna palabra del léxico fantasmal.

## 11. Cambios del borrador v0.1 a la v0.2 (antes de congelar; no son desviaciones)

1. **Semillas:** antes eran «base + índice», igual en los tres tipos de ruido, de modo que el ruido rosa y el marrón habrían sido versiones filtradas del **mismo** ruido blanco. Ahora cada fragmento usa `SeedSequence([base, tipo, índice])`. Un test lo comprueba (correlación < 0,05).
2. **Límite de pico en las mezclas:** con la voz a +20 dB sobre un ruido de −20 dBFS, la mezcla saturaba. Ahora se baja entera hasta 0,9 de pico (`limitar_pico`), sin cambiar la relación señal/ruido.
3. **N de 200 a 300 por tipo (900 fragmentos).** El intento 1 de V1 (semilla 20261109, `results/v1_intento1.log`) aprobó H2: falsas alarmas del 0 %, el 1,2 % y el 0,2 %, y detección del 100 % en los tres escenarios. Aprobó también las falsas alarmas de H3 (0,2 %). Pero **la detección del léxico en H3 se quedó en el 89 %, por debajo del 90 % exigido**, con n = 600. Además, ese intento no tenía en cuenta las pruebas «no evaluables» (con un 5 % de no vacías, ninguna repetición era evaluable) y se paró con un error al calcular los criterios. Se corrigió la regla (no evaluable = no alarma) y se repitió V1 **con una semilla nueva** (20261110) y N = 300.
4. **Regla nueva:** H2 con menos de 5 parejas no vacías en una pareja de modelos y un tipo de ruido es **«no evaluable»** y se informa así, sin p.
5. **Librerías de la GPU:** cuBLAS y cuDNN ya estaban instaladas como paquetes de pip (`nvidia-cublas-cu12` 12.9.2.10, `nvidia-cudnn-cu12` 9.27.0.42 y `nvidia-cuda-nvrtc-cu12` 12.9.86), pero Windows no las encontraba. `transcribir._dlls_nvidia()` añade sus carpetas. No se ha descargado nada.
6. **Velocidad medida** con las 20 primeras frases de control **limpias** (`results/velocidad.json`), en segundos por frase de unos 3,5 s:
   - base, 0,28 (GPU), con WER del 5,9 %;
   - small, 0,54 (GPU), con WER del 2,9 %;
   - medium, 1,13 (GPU), con WER del 3,0 %;
   - Vosk, 0,94 (CPU), con WER del 2,4 %.

   En CPU, medium tardaba 11,2 s, por eso se usa la GPU. **Estimación de la pasada completa** (900 fragmentos de 10 s, multiplicando por 3 por los reintentos de temperatura en el ruido): **de 3 a 4 horas**, casi todo de GPU.

## 12. Código que se congela

- `src/psicofonias/`:
  - `texto.py`: normalización, Jaccard, léxico y WER (con las cifras de 0 a 99 pasadas a palabras, solo para el WER);
  - `audio.py`: ruido, mezcla, `limitar_pico` y WAV;
  - `analisis.py`: Wilson, H2 por permutaciones, McNemar y Holm;
  - `transcribir.py`: Whisper en la GPU (int8_float16, `local_files_only`) y Vosk;
  - `runtime.py`: prioridad baja.
- `scripts/`:
  - `pasada.py`: las etapas v0, controles, ruido, h3_neutra y h3_psico, reanudable. Se niega a correr sin `CONGELADO.txt`.
  - `analizar.py`: el análisis de §5, con la semilla de permutaciones 20261111, y E4.
  - `validar_v1.py`, `medir_velocidad.py`, `sintetizar_frases.ps1` y `congelar.py`.
- `tests/test_basico.py`: V2.
- **Pruebas hechas sin ruido:**
  - `pasada.py --prueba`: 3 frases limpias con 1 s de silencio a cada lado, en `results/prueba_fontaneria/`;
  - `analizar.py`, sobre transcripciones inventadas: funciona de principio a fin.

**Nota sobre la prueba de fontanería:** usó silencio (ceros), no ruido. En esas 3 frases ninguna IA añadió nada en el silencio. Se deja escrito porque es lo único «sin voz» que han visto las IAs antes de congelar.

**Resultado de V1, intento 2** (semilla 20261110, N = 300 por tipo, 500 repeticiones, 13 minutos; `results/v1.json`): **APRUEBA**.
- **H2, falsas alarmas:** 0 % (pocas transcripciones no vacías: ninguna repetición evaluable, así que tampoco hay alarmas), 0,8 % (azar) y 1,0 % (alucinaciones comunes). **Detección:** 100 % en los tres escenarios.
- **H3, falsas alarmas:** 0,2 % (no vacía) y 0,6 % (léxico). **Detección:** 98,8 % y 98,0 %.
- **Límite que se deja escrito:** con un 5 % de no vacías por modelo, H2 casi nunca será evaluable. Si en la pasada real hay muy pocas «voces», H2 quedará «no evaluable», y así se contará.


## 13. Desviaciones (después de congelar)

Ninguna por ahora.
