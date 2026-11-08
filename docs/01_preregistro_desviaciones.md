# Desviaciones de P1 (después de congelar)

El preregistro `01_preregistro.md` se conserva **exactamente como se congeló** (su huella coincide con `results/CONGELADO.txt`). Las desviaciones posteriores se apuntan aquí, en un fichero aparte, para no romper esa huella.

> Nota (08-11-2026): estas desviaciones se escribieron primero dentro del §13 del propio preregistro, lo que cambiaba su huella. Se detectó al preparar la publicación. Se restauró el texto congelado byte a byte (la huella vuelve a coincidir) y el contenido se movió aquí sin cambios.

1. **08-11-2026, interrupción:** la pasada se cortó en h3_psico/medium, hacia el fragmento 735, por saturación del ordenador. El 07-11 a las 21:43 se reanudó con el mismo código, que es reanudable por diseño, y se completó. Los audios son deterministas y no hay transcripciones repetidas ni ausentes. Detalle en `02_resultados.md` §6.
2. **08-11-2026, E1 no se ejecuta como estaba fijado.** Las 30 transcripciones elegidas con la semilla 20261108 son todas «Suscríbete» o «Gracias por ver el vídeo». No hay mensaje que interpretar, y además haría falta una segunda instancia de Claude, que el proyecto no permite sin el visto bueno del usuario. Cualquier versión con otro material será exploratoria a posteriori.
3. **08-11-2026, código posterior:** `scripts/posteriores.py` (la puntuación de E5 y el material de E1) se escribió después de ver `results/analisis.json`. No está congelado. Lee los sucesos tal como se definieron en la apuesta.
