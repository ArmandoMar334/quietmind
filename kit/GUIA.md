# Quiet Mind: guía para hacer cada video

Canal faceless de motivación y crecimiento personal en español (TikTok @quiet_mind__, Instagram, YouTube). Dueño: Armando.

## 1. Guion
- Español, en segunda persona o como parábola, de 1:10 a 1:30 de duración (unas 230 a 280 palabras).
- Etiquetas de ElevenLabs v3 al inicio de cada línea: [calm], [softly], [thoughtful], [serious], [confident], [exhales], [pause], [long pause].
- Cierre con una frase corta y citable.
- **Nunca repetir un tema.** Temas ya usados:
  el momento perfecto, la incomodidad, las promesas, el ruido, el niño que fuiste, el fondo, la mochila, las grietas de oro (kintsugi), la cadena (el elefante), carta de tu yo del futuro, nadie va a venir, no todos van a subir contigo, cómo te hablas, dos versiones de ti, no vas tarde, lo que un día pediste, cuando no tengas ganas, esto también va a pasar, nadie te está mirando, suelta lo que no controlas, antes de que termine el año, el tren, a las 3 de la mañana, solo el 1%, ¿a dónde se va tu tiempo?, nadie sabe lo que cargas, la flor del concreto, las máscaras, no es el final del libro, el faro (no te apagues), cuando aprendiste a caminar, ellos también tuvieron tu edad, el bonsái.
  Temas autorizados pendientes: ver `temas.md` en la raíz del repo.
  Rechazados por Armando (no usar): los días que nadie ve, cuatro mil semanas, el pescador, el hacha.
- Agrega cada tema nuevo a esta lista.

## 2. Voz (ElevenLabs)
- Voz: Chuck Miller - Deep, Raspy, American, voice_id `HIGUfNOdjuWQwwapnTRW`.
- Modelo eleven_v3, stability 50, similarity 70–75. Genera solo una variación.
- Créditos: plan Starter de 30,389 caracteres al mes, que se renuevan alrededor del día 16. Revisa el saldo antes de generar.
- Descarga el mp3 como `assets/voz.mp3` del proyecto.

## 3. Animación (HyperFrames)
- Estilo cinematográfico, vertical 1080×1920:
  - Mundo oscuro con horizonte, neblina, polvo y grano.
  - Figuras en silueta con contorno de luz (`C.person`).
  - Arco de luz de frío a cálido (amanecer al final).
  - Títulos en EB Garamond itálica (clase `.title`, top unos 230px) y kickers en Inter espaciada (`.kick`).
  - Subtítulos palabra por palabra en Inter, en la franja de 1140 a 1320 px. Nada importante debajo de los subtítulos.
- **Cada video debe tener una animación nueva y distinta** (escenario, metáfora visual y movimientos de cámara propios). Los archivos de `ejemplos/` muestran el patrón.
- Pasos:
  1. Crea la carpeta del proyecto, por ejemplo `proyecto/`, con `assets/`.
  2. Copia `assets/cine.js` y `assets/gsap.min.js` del kit, y pon `assets/voz.mp3`.
  3. Arma la música larga con ffmpeg: `ffmpeg -i musica.mp3 -i musica.mp3 -filter_complex "[0][1]acrossfade=d=5,atrim=0:DURACION+10" proyecto/assets/musica_larga.mp3`.
  4. Alinea el texto con la voz: `ffmpeg -i voz.mp3 -af silencedetect=noise=-38dB:d=0.3 -f null -` y asigna cada segmento hablado (el primero empieza en 0) a una frase del guion. Los `[exhales]` aparecen como segmentos de unos 0.3 s.
  5. Escribe `scenes_TEMA.py`. Define `S` con una escena `(id, 0.0, TOTAL, 0.0, markup, STAGE_js, timeline_js)` y la lista `CUES` con (inicio, fin, texto). El dibujo va en canvas con la variable `t` (segundos absolutos) y ayudantes de `C` (cine.js): glow, cone, sun, rays, fog, dust, person, mixc, rgba, ease, prog, rng.
  6. `python3 gen.py proyecto scenes_TEMA.py DURACION nombre`. La duración es la del audio más unos 3 a 4 s.
  7. `cd proyecto && npx hyperframes lint`, y luego `npx hyperframes snapshot --at 2,10,...` para revisar los cuadros: que nada se encime con los subtítulos ni con los títulos. Corrige.
  8. Render: `HYPERFRAMES_BROWSER_PATH=/usr/bin/google-chrome npx hyperframes render --fps 24 --video-bitrate 7M --max-bitrate 8M -o renders/raw.mp4`.
  9. Audio final: `ffmpeg -i renders/raw.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k renders/NOMBRE.mp4`.
- Reglas del contrato de HyperFrames: nada de `tl.set` ni tweens de letterSpacing (usa `gsap.set` o `fromTo`). El dibujo debe ser determinista (usa `C.rng(seed)`, nunca Math.random).

## 4. Entrega
- Deja el mp4 final en la carpeta de Descargas de Armando.
- Publicación con Metricool (brand blogId `8320706`, zona horaria America/Chihuahua, YouTube ya conectado):
  - YouTube Short + TikTok en el mismo post, con título, descripción y hashtags (#motivacion #crecimientopersonal #shorts), madeForKids false. Nunca pongas etiquetas de IA (isAiGeneratedContent ni isAigc), decisión de Armando.
  - Metricool necesita el video en una URL pública. Súbelo al repo público de GitHub `ArmandoMar334/quietmind` en `videos/NOMBRE.mp4` (git push; menos de 100 MB) y usa `https://raw.githubusercontent.com/ArmandoMar334/quietmind/main/videos/NOMBRE.mp4`. Los releases de GitHub están bloqueados para Claude; no los uses.
  - **Nunca publiques ni programes en público sin el "sí" explícito de Armando para ese video.**
