# E6: apuesta de Claude antes de la pasada (sellada)

- **Escrita el 08-11-2026**, antes de que ninguna IA escuche ninguna grabación de E6.
- **Lo que he visto:** solo los títulos, las descripciones y las frases de los autores. No he oído nada, porque no puedo oír.
- **No es independiente:** la escribe quien diseñó la prueba.
- **Se puntúa con Brier.** Los sucesos usan las medidas de `docs/03_e6_plan.md` §3, sobre las 101 grabaciones legibles.

| # | Suceso | Probabilidad |
|---|---|---|
| 1 | (a) Whisper medium escribe algo en ≥ 80 % de las grabaciones | 0,85 |
| 2 | (a) Vosk escribe algo en ≥ 50 % | 0,60 |
| 3 | (b) small–medium coinciden más en la misma grabación que barajadas (p_Holm < 0,01) | 0,85 |
| 4 | (c) Whisper medium escribe la frase del autor más que la de otra grabación (p_Holm < 0,01) | 0,65 |
| 5 | (c) alguna de las 4 IAs sale con p_Holm < 0,01 | 0,75 |
| 6 | (c) Vosk sale con p_Holm < 0,01 | 0,35 |
| 7 | (c) medium acierta (cobertura ≥ 0,5) en ≥ 21 grabaciones (≥ 20 %) | 0,35 |
| 8 | Alguna IA acierta en ≥ 30 grabaciones (`alguna_acierta` ≥ 30) | 0,40 |
| 9 | En las 5 en español, alguna IA acierta en ≥ 2 | 0,30 |

**Razonamiento, en breve:**
- Son grabaciones elegidas por sus autores como las «más claras». Algunas serán voces reales: los propios investigadores, gente cerca o una radio colada. Por eso espero que Whisper acierte bastante más que por azar.
- La mayoría serán susurros cortos. Por eso no espero que acierte en más de 1 de cada 5.
- Vosk oye peor.
