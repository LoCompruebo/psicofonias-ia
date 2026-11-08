# Procedencia: E6, psicofonías reales con licencia libre

- **Qué es:** 102 grabaciones que sus autores presentan como psicofonías (EVP), cada una con la frase que dicen oír.
- **Lista completa:** `data/e6_candidatas.csv`, con fuente, identificador, fichero, frase, idioma, licencia, tamaño, duración y URL. El fichero local es `audio/NNN.ext`, donde NNN es la columna `n`.
- **Fuentes:**
  - **Internet Archive** (72): los ficheros originales, de `https://archive.org/download/<id>/<fichero>`. La licencia es la del campo `licenseurl` de cada ficha.
  - **Freesound** (30): las previas públicas de alta calidad (`https://cdn.freesound.org/previews/...-hq.mp3`, MP3 a 128 kbps). El original exige una cuenta, y no se crean cuentas. La licencia es la de la ficha de cada sonido.
- **Descargado:** 2026-11-08, hacia las 01:25 UTC, con `curl` (HTTP 200 en los 102). 19 MB en total.
- **Huellas:** `SHA256SUMS_audio`.
- **Licencias:** CC BY, BY-NC, BY-NC-SA, BY-NC-ND, BY-ND, Sampling+ 1.0, CC0 y dominio público.
  - **Uso:** solo análisis. No se publica ni se reproduce ningún audio, y como mucho se describe.
  - Si se cita una grabación, va con su autor, su licencia y su URL.
- **Autorizado por el usuario** el 08-11-2026 («Sí, las dos cosas»).
- **Avisos:**
  - la 024 (`fred.wav`, 648 bytes) no se puede leer;
  - las grabaciones no son de confianza: solo se leen como audio con ffmpeg, y nunca se ejecuta nada de ellas.
