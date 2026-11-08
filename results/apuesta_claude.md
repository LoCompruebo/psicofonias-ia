# E5, «la IA apuesta»: predicción de Claude antes de la pasada real

- **Escrita el 05-11-2026**, antes de congelar el preregistro y sin que ninguna IA haya procesado ningún ruido de este proyecto. Lo único visto: las frases de control limpias (velocidad y WER) y la prueba de fontanería con 3 frases limpias rodeadas de silencio.
- **No es independiente:** la escribe la misma IA que diseñó la prueba, y sabe por la literatura que Whisper inventa frases en el silencio y el ruido.
- **Se sella** con su SHA-256 en `results/CONGELADO.txt`.
- **Se puntúa con Brier:** (p − r)², donde r = 1 si ocurre y 0 si no.

| # | Suceso (definido en el preregistro) | Probabilidad |
|---|---|---|
| 1 | **H1:** se cumple la afirmación preregistrada (algún modelo con algún tipo de ruido tiene el límite inferior del IC95 > 5 %) | 0,75 |
| 2 | Algún modelo **Whisper**, por sí solo, cumple la condición de H1 | 0,70 |
| 3 | **Vosk** cumple, por sí solo, la condición de H1 | 0,55 |
| 4 | **H2:** al menos una pareja **entre hermanos** (Whisper–Whisper) sale positiva tras Holm | 0,35 |
| 5 | **H2:** al menos una pareja **entre familias** (Whisper–Vosk) sale positiva tras Holm | 0,10 |
| 6 | **H3:** sale positiva (cualquiera de las dos medidas, tras Holm) | 0,70 |
| 7 | **H3, léxico** por separado: p_Holm < 0,01 | 0,40 |
| 8 | **E4:** entre las 3 frases más repetidas de algún Whisper hay una de tipo «subtítulos» o «gracias por ver» | 0,50 |
| 9 | **V0:** Whisper medium sigue por debajo del 50 % de WER a 0 dB | 0,70 |

**Razonamiento, en breve:**
- Whisper alucina con el ruido, pero faster-whisper descarta por defecto los tramos con mucha probabilidad de «no voz» y poca confianza. Eso puede dejar en blanco la mayoría de los fragmentos de ruido puro. Por eso la 1 no pasa de 0,75.
- La instrucción de psicofonía empuja al decodificador a continuar el texto: espero más salidas no vacías. Más palabras fantasmales es menos seguro.
- Que dos IAs coincidan **en el mismo fragmento** más allá de las frases comunes exigiría que el ruido concreto las guíe, y no lo espero.
