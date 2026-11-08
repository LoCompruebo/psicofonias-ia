# Resultados de E6: psicofonías reales, a ciegas (exploratorio)

- **Plan:** `03_e6_plan.md`, congelado el 08-11-2026 a las 01:32Z (`results/e6_CONGELADO.txt`, 115 huellas, apuesta incluida).
- **Pasada única:** el 08-11, 6 minutos (`results/e6_pasada.log`).
- **Análisis:** `scripts/e6_analizar.py` → `results/e6_analisis.json`, con todas las transcripciones grabación a grabación.
- **Material:** 101 grabaciones legibles de 102 (la 024 no se puede leer): 5 en español y 96 en inglés.

## Veredicto en una frase

Las IAs escriben la frase que dice el autor **muy pocas veces**: Whisper medium, en 10 de 101. Eso es más que por casualidad (lo esperado sería 1), pero casi todos esos aciertos son palabras claras y corrientes («Hello», «Hey», «Hola») o frases de los propios investigadores. En las demás grabaciones, la IA escribe otra cosa, nada, o lo mismo que en el ruido puro: «Thanks for watching».

## (a) ¿Escriben algo?

| IA | Con texto | IC95 |
|---|---|---|
| Whisper base | 58 (57 %) | 48–67 % |
| Whisper small | 62 (61 %) | 52–70 % |
| Whisper medium | 76 (75 %) | 66–83 % |
| Vosk (es/en) | 31 (31 %) | 23–40 % |

## (b) ¿Coinciden entre ellas?

- **Todas las parejas** coinciden más en la misma grabación que con las grabaciones barajadas (p_Holm = 0,0006 en las seis).
- Valores de J:
  - small–medium, 0,50;
  - entre Whisper, de 0,32 a 0,39;
  - Whisper con Vosk, de 0,17 a 0,19.
- **Comparación:**
  - en el ruido puro de P1, el barajado daba lo mismo;
  - con voz clara de P1, la J estaba entre 0,78 y 0,95.
- **Lectura:** en estas grabaciones hay sonido con forma de voz, mucho menos claro que una voz normal. Era lo esperado, porque muchas llevan la voz de los investigadores (plan §4).

## (c) ¿Escriben la frase del autor? (la medida clave)

| IA | Aciertos (cobertura ≥ 0,5) | Esperados por casualidad | Cobertura media (frente a la nula) | p_Holm |
|---|---|---|---|---|
| Whisper base | 8 | 1,5 | 0,096 (0,024) | 0,0004 |
| Whisper small | 10 | 1,2 | 0,108 (0,024) | 0,0004 |
| Whisper medium | 10 | 1,0 | 0,095 (0,019) | 0,0004 |
| Vosk | 3 | 0,6 | 0,033 (0,009) | 0,003 |

- **Positivo en las cuatro IAs:** aciertan más que con la frase de otra grabación.
- **Pero el tamaño es pequeño:**
  - alguna IA acierta en 12 grabaciones de 101 (12 %);
  - las cuatro a la vez, en 3.
  - En el 88 % de las grabaciones, ninguna IA escribe lo que dice el autor.
- **Las 12 grabaciones con algún acierto**, mirando las transcripciones. Esta clasificación es **a posteriori**: no estaba en el plan.

| Grabación | Frase del autor | Lo que escriben (medium) | Lectura a posteriori |
|---|---|---|---|
| 005 (es) | «Hola» | «hola hola hola…» (las 4 IAs) | Voz clara repetida |
| 065 | «Hey» | «Hey!» (3 IAs) | Palabra clara |
| 089 | «Hello» | «Hello!» (3 IAs) | Palabra clara |
| 067 | «Please» | «Please.» (2 IAs) | Palabra clara |
| 057 | «We just want to talk» | «We're a couple of nice guys. We just want to talk to you.» (4 IAs) | Parece la frase de un investigador |
| 092 | «No» | «…he wants to leave? He said no.» | Un investigador cuenta la respuesta |
| 069 | «Good» | «…are you good, are you bad?» | La pregunta del investigador |
| 078 | «I'm here» | «…is there anybody in here» | Solo coincide «here» |
| 084 | «You should get» | «You should care.» | Parecido parcial |
| 083 | «I'll return» | «…I'll call you in a minute.» | Parcial, dudoso |
| 100 | «Wait» | small: «It's over there, wait.» | Solo una IA |
| 102 | «Watch» | base: «Watch me.» | Solo una IA |

- **Por grupo de autores**, aciertos de medium:
  - MSSPI, 2 de 57;
  - Todd_Bates, 4 de 13;
  - Soulwriter, 1 de 8;
  - southlandghosthunter, 0 de 6;
  - otros, 3 de 17.
- **El grupo más grande (MSSPI, 57 grabaciones de cementerios y casas) casi nunca coincide** con lo que dice su autor.

## En español (5 grabaciones)

| Frase del autor | base | small | medium | Vosk |
|---|---|---|---|---|
| «Ahí viene» | «No, no, no…» | «¡Suscríbete!» | «Subtítulos por la comunidad de Amara.org» | (nada) |
| «A este lo mato» | (nada) | «¡Suscríbete!» | (nada) | (nada) |
| «Tú lo tienes que descubrir» | «No, no, no…» | «¡Suscríbete!» | «Gracias por ver el video.» | (nada) |
| «Apártate» | (nada) | (nada) | «¡Gracias por ver!» | (nada) |
| «Hola» | «Hola, hola…» | «hola-hola…» | «hola hola…» | «hola hola…» |

En 4 de 5, las IAs reaccionan **exactamente igual que ante el ruido puro de P1**.

## Exploratorio a posteriori: las frases de cierre de vídeo

- Whisper medium escribe «Thanks for watching», «Thank you», «Gracias por ver» o «Suscríbete» en **37 de las 101 grabaciones**. Small lo hace en 12, base en 6 y Vosk en ninguna.
- La cuenta es aproximada: incluye algún «thank you» que podría haberse dicho de verdad.
- **Lectura:** para la IA, más de un tercio de estas psicofonías son indistinguibles del silencio o del ruido.

## La apuesta de Claude (sellada antes)

- **Brier medio: 0,232.** Una moneda al aire da 0,25: apenas mejor que el azar.
- **Fallos:** creyó que medium escribiría algo en ≥ 80 % (fue el 75 %), que Vosk lo haría en ≥ 50 % (fue el 31 %) y que habría más aciertos (≥ 21 de medium; fueron 10).
- **Acierto:** que (b) y (c) saldrían positivas.
- Detalle en `results/e6_apuesta_puntuacion.json`.

## Qué significa y qué no

- **Sí:**
  - en la mayoría de estas psicofonías, una máquina sin expectativas **no oye la frase que oyó su autor**;
  - cuando la oye, casi siempre es una palabra corriente y clara, o algo que dicen los propios investigadores;
  - una voz humana real en la grabación es la explicación más sencilla, y no dice de dónde viene (plan §4).
- **No:**
  - no demuestra que no haya nada;
  - una IA de transcripción entrenada con voz normal puede fallar con susurros débiles que un oído humano atento sí capta;
  - la muestra está dominada por un solo grupo de Misisipi;
  - las grabaciones de Freesound son previas en MP3.
- **Desviaciones:** ninguna en la pasada. La clasificación de las 12 grabaciones con acierto y la cuenta de las frases de cierre se hicieron después de ver los datos: son a posteriori.
