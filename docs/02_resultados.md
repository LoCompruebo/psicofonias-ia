# Resultados de P1: ¿oye voces una IA en el ruido?

- **Pasada real:** la única, del 05-11-2026 (19:23) al 07-11-2026 (21:54). Hubo una interrupción y se reanudó (§6).
- **Análisis:** `scripts/analizar.py`, congelado, ejecutado el 08-11-2026 → `results/analisis.json`.
- **Comprobación previa:** las 68 huellas de ficheros de `results/CONGELADO.txt` coinciden con los ficheros actuales. Ninguna transcripción está repetida ni falta (900 por IA y etapa).
- Lo preregistrado (§1–§4) va separado de lo exploratorio (§5).

## Veredicto en una frase

Las IAs grandes **sí «oyen» voces en un ruido que sabemos vacío**, casi siempre. Pero lo que oyen no sale del ruido: son las frases finales de los vídeos de YouTube con los que aprendieron («Suscríbete», «Gracias por ver el vídeo»). Y cuando se les sugiere que es una psicofonía, empiezan a hablar de muerte, Dios y espíritus.

## 1. V0, el examen del oído (preregistrado): APRUEBA

Es el WER, la fracción de palabras falladas. Por encima del 100 % significa que la IA escribe más palabras de las que se dijeron.

| IA | +20 dB | +10 dB | 0 dB | −5 dB | −10 dB | −20 dB |
|---|---|---|---|---|---|---|
| Whisper base | 3,4 % | 10,4 % | 39,6 % | 82,1 % | 110,7 % | 100 % |
| Whisper small | 1,0 % | 2,4 % | 17,9 % | 46,9 % | 103,5 % | 99,8 % |
| Whisper medium | 0,4 % | 1,1 % | 9,9 % | 33,7 % | 86,5 % | 99,6 % |
| Vosk | 3,2 % | 7,5 % | 27,1 % | 81,8 % | 100 % | 100 % |

El criterio era que medium tuviera un WER ≤ 15 % a +20 dB. Tiene un 0,4 %. El montaje funciona.

## 2. H1, las voces en el ruido (preregistrado): POSITIVA

Fragmentos de ruido puro (10 s cada uno) con una transcripción no vacía, de 300 por tipo, con el intervalo de Wilson al 95 %:

| IA | Blanco | Rosa | Marrón |
|---|---|---|---|
| Whisper base | 1 (0,1–1,9 %) | 2 (0,2–2,4 %) | 1 (0,1–1,9 %) |
| Whisper small | **300 (98,7–100 %)** | **300 (98,7–100 %)** | 7 (1,1–4,7 %) |
| Whisper medium | **300 (98,7–100 %)** | **299 (98,1–99,9 %)** | **300 (98,7–100 %)** |
| Vosk | 0 (0–1,3 %) | 0 (0–1,3 %) | 0 (0–1,3 %) |

- **Se cumple la afirmación preregistrada** («la IA oye voces en el ruido»). Lo hace en cinco de las doce combinaciones de IA y ruido, con el límite inferior muy por encima del 5 %.
- **Cada IA se comporta a su manera:**
  - **Vosk**, la IA de otra familia, no escribe nada nunca.
  - **Whisper base** casi nunca escribe nada. En 18 fragmentos escribió solo «y y y y…», que no cuenta porque las palabras de una letra se descartan (§5 del preregistro).
  - **Small** escribe algo en el ruido blanco y el rosa, pero calla en el marrón (el ruido más grave).
  - **Medium** escribe algo en prácticamente todos.

## 3. H2, ¿coinciden las IAs? (preregistrado): NEGATIVA o NO EVALUABLE

- **Entre familias (Whisper con Vosk): no evaluable.** Vosk no escribe nada, así que no hay parejas que comparar (regla §11.4 del preregistro).
- **Entre hermanos:**
  - Las parejas con base no son evaluables (de 0 a 2 parejas no vacías).
  - La única evaluable es **small–medium**, y **sale negativa en los tres ruidos**:

| Ruido | Parejas | J observada | J con fragmentos barajados (media) | p_Holm |
|---|---|---|---|---|
| Blanco | 300 | 0,892 | 0,893 | 1,0 |
| Rosa | 299 | 0,111 | 0,106 | 0,85 |
| Marrón | 7 | 0,149 | — | 1,0 |

- **Lectura:** en el ruido blanco, small y medium coinciden muchísimo (J = 0,89), pero coinciden **igual de bien con fragmentos barajados**. No es que el ruido concreto les dicte las mismas palabras: es que las dos dicen casi siempre lo mismo («Suscríbete») sea cual sea el fragmento.
- **Referencia:** con voz real (controles a +10 dB), las parejas coinciden con J de entre 0,78 y 0,95.
- El ruido **no empuja** a dos IAs hacia el mismo mensaje. Es lo mismo que pasa con las personas: cada una oye lo suyo.

## 4. H3, la sugestión (preregistrado): POSITIVA

Whisper medium con los mismos 900 fragmentos, comparando la instrucción de psicofonía con la neutra (McNemar de una cola, Holm con 2 pruebas):

| Medida | Sin instrucción (descriptivo) | Neutra | Psicofonía | Cambios a favor y en contra de la psicofonía | p_Holm |
|---|---|---|---|---|---|
| Transcripción no vacía | 99,9 % | 70,7 % | **78,2 %** | 103 frente a 35 | 6·10⁻⁹ |
| Contiene léxico fantasmal | 0 % | 0 % | **1,2 % (11)** | 11 frente a 0 | 0,0005 |

- **Las dos medidas salen positivas.** Con la instrucción de psicofonía, la IA escribe en más fragmentos y, en 11, aparecen palabras como muerte, Dios, diablo, cielo, frío o «fuera». Con la instrucción neutra no aparece **ninguna**.
- **Ejemplos literales** (Whisper medium, ruido puro, instrucción de psicofonía):
  - rosa_236: «¡Dios mío!»
  - rosa_105: «¡Fuera de los espíritus!»
  - rosa_243: «Chocó la vida por el diablo.»
  - rosa_078: «¿Qué es eso? Ese es el frío.»
  - rosa_227: «Los espíritus dicen que la vida es una muerte, una muerte de una persona que sufrirá la muerte.»
  - blanco_090: «¡Sin el amor de Dios!»
- **Matiz importante:** varias salidas copian o continúan la instrucción («Las voces de los espíritus dicen que…»). Las palabras de la instrucción no cuentan para el léxico, pero la IA continúa la frase que se le ha empezado. Ese es justo el mecanismo de la sugestión: el contexto rellena el hueco.
- **Hallazgo no previsto (descriptivo):** cualquier instrucción, incluso la neutra, hace que medium **calle más** (del 99,9 % al 71 %). Sin instrucción tiende a cerrar como un vídeo de YouTube. Con la instrucción neutra calla sobre todo en el ruido marrón (36 de 300). Con la de psicofonía «oye» algo en 116 de 300 fragmentos marrones.

## 5. Exploratorio

### E4, de dónde salen las «voces» (regla en el preregistro §8 y §9)

Las frases más repetidas en el ruido puro, sin instrucción:

| IA | Frases más repetidas (de 900 fragmentos) |
|---|---|
| Medium | «Gracias por ver el vídeo» 358, «Suscríbete» 303, «Suscríbete al canal» 224, «Suscríbete, dale like» 7, «Subtítulos por la comunidad de Amara.org» 2 |
| Small | «Suscríbete» 516, «Subtítulos por la comunidad de Amara.org» 59, «Subtítulos realizados por la comunidad de Amara.org» 27, más un caso de «Este es el canal de subtítulos en español de la Iglesia de Jesucristo…» |
| Base | Solo 4 salidas no vacías («No, no, no…»). |
| Vosk | Ninguna. |

- **Medium dice solo 10 frases distintas en 900 fragmentos**, más uno en blanco (corregido el 08-11: antes ponía 11 porque contaba el vacío). Las «voces» no salen del ruido: son el final típico de los vídeos subtitulados con los que aprendió Whisper.
- Es la explicación más sencilla de su «psicofonía»: ante el silencio, rellena con lo que más veces vio al final de un audio.
- **Con la instrucción de psicofonía**, el repertorio sube de 11 a 266 frases distintas. Aparecen «No te preocupes, no te preocupes» (42 veces), «Apúntenme» (11) y «Buenos días».

### E5, la apuesta de Claude (sellada antes de la pasada)

| # | Suceso | Probabilidad | ¿Ocurrió? | Brier |
|---|---|---|---|---|
| 1 | Se cumple H1 | 0,75 | Sí | 0,063 |
| 2 | Algún Whisper cumple H1 | 0,70 | Sí | 0,090 |
| 3 | Vosk cumple H1 | 0,55 | **No** | 0,303 |
| 4 | H2 positiva entre hermanos | 0,35 | No | 0,123 |
| 5 | H2 positiva entre familias | 0,10 | No (no evaluable) | 0,010 |
| 6 | Se cumple H3 | 0,70 | Sí | 0,090 |
| 7 | H3 léxico con p_Holm < 0,01 | 0,40 | Sí | 0,360 |
| 8 | Subtítulos o «gracias por ver» en el top 3 de algún Whisper | 0,50 | Sí | 0,250 |
| 9 | Medium por debajo del 50 % de WER a 0 dB | 0,70 | Sí | 0,090 |

- **Brier medio: 0,153.** Una moneda al aire (0,5 en todo) daría 0,25 y adivinarlo todo daría 0. Claude acertó la dirección en 6 de los 9 sucesos, falló 2 (Vosk y el léxico) y dejó 1 al 50 % (E4). Corregido el 08-11: antes ponía «8 de 9».
- **Su gran fallo:** creyó que Vosk también «oiría» voces, y Vosk no dice nada nunca. Además, infravaloró cuánto alucina medium: apostó que el filtro de «no voz» dejaría muchos fragmentos en blanco, y no dejó casi ninguno.
- Recuerda que la apuesta no es independiente: la escribió la misma IA que diseñó la prueba (`results/apuesta_claude.md`).

### E1, Claude intérprete: no se ejecuta tal como estaba fijado

- La regla fijada saca al azar 30 transcripciones de medium sin instrucción (semilla 20261108; `results/e1_material.json`). Salen 15 «¡SUSCRÍBETE!», 10 «¡Gracias por ver el vídeo!» y 5 «¡Suscríbete al canal!». Las cadenas al azar del mismo largo tienen de 1 a 4 palabras.
- Con ese material, la prueba no puede medir nada: no hay «mensaje» que interpretar. Ese ya es un resultado: **el ruido, por sí solo, no da a la IA material para una psicofonía**.
- Además, la regla pedía una segunda instancia de Claude que puntuara a ciegas, y el proyecto prohíbe usar subagentes sin permiso.
- Se deja como desviación (§6). Si se hace una versión a posteriori con las transcripciones con sugestión, irá marcada como exploratoria.

## 6. Desviaciones y avisos

1. **Interrupción y reanudación:**
   - Qué pasó: la pasada se cortó en h3_psico/medium, hacia el fragmento 735 de 900, por saturación del ordenador.
   - Cómo se reanudó: la cola automática de la sesión de Simulación la reanudó el 07-11 a las 21:43, con el mismo código congelado, y la pasada siguió donde iba.
   - Efecto: los audios son deterministas y cada transcripción se guarda por separado, así que solo afecta al tiempo. Durante la saturación, la mediana subió a 5,8 s por fragmento, frente a 1 s en la etapa de ruido.
   - Límite: Whisper puede reintentar con muestreo aleatorio cuando duda, así que la salida exacta de un fragmento no está garantizada al repetir. Eso añade ruido, pero no sesgo.
2. **E1 no se ejecuta como estaba fijado** (§5). Es material degenerado y necesitaría una segunda instancia de Claude.
3. **`scripts/posteriores.py`** (E5 y el material de E1) se escribió después de ver `analisis.json`. Solo lee los sucesos tal como se definieron en la apuesta; no está congelado.

## 7. Qué significa y qué no

- **Sí significa:**
  - una IA de transcripción moderna, ante ruido sin ninguna voz, escribe frases casi siempre;
  - esas frases no las «dicta» el ruido: dos IAs no coinciden más en el mismo fragmento que en fragmentos barajados;
  - salen de su entrenamiento (finales de vídeos de YouTube);
  - basta con decirle «esto es una psicofonía» para que aparezcan la muerte, Dios y los espíritus.
- **No significa** que las psicofonías humanas sean falsas. Esto es una máquina con ruido sintético. Lo que muestra es un mecanismo, rellenar con lo esperado, que encaja con la explicación de la pareidolia.
- **Límites:**
  - es ruido sintético, no el de una grabadora real (de ahí E2 y E6);
  - es una sola instrucción de sugestión;
  - el léxico fantasmal es una lista fija y cuenta solo palabras, no el sentido.

## 8. Corrección de una cita del preregistro (08-11-2026)

El preregistro (§0, congelado, no se toca) citaba a Williams y Blagrove (2022) [V*] a través de una fuente secundaria: «avisar de que son voces de fantasmas hace oír más voces» y «un 13 % de coincidencia frente al 95 %». **Comprobado en el artículo original [V]:**
- **La coincidencia máxima media entre personas** fue del 11,8 % con las psicofonías, el 10,7 % con la voz estropeada y el 89,0 % con la voz normal (tabla 2).
- **9 de 984 respuestas (0,91 %)** coincidieron con la interpretación de los cazafantasmas originales.
- **La sugestión:** el grupo avisado («voces de fantasmas») **no** oyó más voces que el no avisado. Solo oyó más voces en las psicofonías que en la voz estropeada, mientras que el no avisado no mostró esa diferencia. Los autores lo llaman una réplica **parcial**.
- **Consecuencia:** nuestro H3, la sugestión en una máquina, no «copia» un efecto firme en personas. Lo prueba en una máquina, donde sí sale con claridad. Esto no cambia ningún resultado de P1.
