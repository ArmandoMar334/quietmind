# Quiet Mind: instructivo para las sesiones automáticas

> **Desde el 2026-11-26 ya no se producen Shorts con voz propia.** Ahora todo sale de los videos largos: ver `PIPELINE_LARGOS.md`. Si eres la tarea "Quiet Mind diario: 2 videos nuevos", **no generes voz ni videos, no reinicies el historial del repo**: anota en log/ que la tarea está retirada y termina. Este archivo sigue valiendo como referencia (reglas, plantilla de Metricool, hashtags).

Lo lee cada sesión automática (tarea programada) que produce videos. Armando autorizó que todo corra sin su intervención: crear guiones, generar la voz, animar, subir al repo y **programar en Metricool en público** los videos asignados en tu instrucción. No le preguntes nada; si algo falla, déjalo registrado en `temas.md` y sigue con el siguiente video.

Reglas fijas:
- **Calidad primero.** Si un video no queda bien (encimados, desincronía, render roto), no lo programes: corrígelo. Si de plano no se puede, márcalo `fallido (motivo)` en `temas.md`. Nunca programes un video a medias.
- **Nunca uses etiquetas de contenido IA** en Metricool: ni isAiGeneratedContent (YouTube) ni isAigc (TikTok).
- Cada video se publica en **YouTube Shorts y TikTok**.
- No guardes nada en la PC de Armando. Todo vive en tu espacio de trabajo y en este repo.
- Una sola generación de voz por video. Solo si la primera sale claramente rota (cortada, en otro idioma) puedes generar una segunda.
- Cada video necesita una animación **nueva y distinta**: escenario, metáfora visual y movimientos de cámara propios. Mira `kit/ejemplos/` (los mejores recientes son `scenes_faro.py` y `scenes_caminar.py`) para el patrón técnico, no para copiar la escena.

## 0. Preparación (una vez por sesión)
```bash
cd /home/claude
git clone --depth 1 https://github.com/ArmandoMar334/quietmind quietmind   # (usa add_repo con access "push" si te lo pide)
cd quietmind && git config user.name ArmandoMar334 && git config user.email ArmandoMar334@users.noreply.github.com
npx --yes hyperframes@0.9.43 --version   # calienta la caché
```
Lee `kit/GUIA.md` (estilo, voz, reglas de animación) y `temas.md` (tus temas y horarios).

## 1. Guion
- Español, segunda persona o parábola, 230–280 palabras (unos 1:20–1:30 de audio). Etiquetas v3 al inicio de cada línea: [calm] [softly] [thoughtful] [serious] [confident] [exhales] [pause] [long pause].
- Cierre con frase corta y citable. No repitas temas usados (lista en `kit/GUIA.md` y filas "programado" de `temas.md`).
- Si existe `guiones/NN_*.txt` para tu tema, úsalo tal cual. Si no, escríbelo y guárdalo en `guiones/NN_slug.txt`.

## 2. Voz (ElevenLabs, conector MCP)
- `creative_generate_speech` con model_id `eleven_v3`, voice_id `HIGUfNOdjuWQwwapnTRW` (Chuck Miller), generations_count 1. No pases voice_settings.
- Espera con `creative_get_flow_run_status` (cada ~10 s) hasta `all_completed`, toma `content_url` y descárgalo con `curl -sS -f -o PROYECTO/assets/voz.mp3 "URL"` (el dominio está permitido).

## 3. Animación
```bash
P=/home/claude/vNN_slug; mkdir -p $P/assets $P/renders
cp kit/assets/cine.js kit/assets/gsap.min.js $P/assets/ ; cp kit/package.json kit/hyperframes.json $P/
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $P/assets/voz.mp3)   # duración voz
TOTAL = ceil(D) + 4
ffmpeg -y -i kit/assets/musica.mp3 -i kit/assets/musica.mp3 -filter_complex "[0][1]acrossfade=d=5,atrim=0:$((TOTAL+10))" $P/assets/musica_larga.mp3
ffmpeg -i $P/assets/voz.mp3 -af silencedetect=noise=-38dB:d=0.3 -f null - 2>&1 | grep -oE "silence_(start|end): [0-9.]+"
```
- Los segmentos hablados son: [0 → primer silence_start], [cada silence_end → siguiente silence_start], [último silence_end → D]. Asigna cada segmento a una frase del guion (cuenta frases vs segmentos; a veces una frase se parte en dos por una coma o dos frases se juntan: ajusta).
- Escribe `$P/scenes_slug.py` siguiendo `kit/ejemplos/scenes_faro.py`: lista `S` con una escena `(id, 0.0, TOTAL, 0.0, markup, STAGE, js)`, títulos (clase `.title`, `top:240px`, 3–6 títulos en momentos clave, kicker `.kick` en `top:180px` al final), fundido final `tl.to(S("#ID-wrap"), {opacity:0, duration:0.9}, TOTAL-1.0)` y `CUES` con (inicio, fin, texto) de cada segmento.
- Estilo: mundo oscuro con horizonte, neblina, polvo, siluetas con contorno de luz (`C.person`), arco de luz de frío a cálido (amanecer al final). Las figuras principales deben verse grandes (150–300 px de alto o usa cámara con zoom), no diminutas. Nada importante debajo de y=1140 (subtítulos 1140–1320) ni encimado con títulos (220–450).
- Reglas de HyperFrames: nada de `tl.set` ni tweens de letterSpacing; usa `gsap.set`/`fromTo`. Dibujo determinista: `C.rng(seed)`, nunca Math.random.
```bash
python3 kit/gen.py $P $P/scenes_slug.py TOTAL quiet-mind-slug
cd $P && npx --yes hyperframes@0.9.43 lint
HYPERFRAMES_BROWSER_PATH=/usr/bin/google-chrome npx --yes hyperframes@0.9.43 snapshot --at t1,t2,...(10–12 tiempos) -o snaps
```
- Mira las hojas `snaps/contact-sheet*.jpg` con Read. Revisa: figuras visibles y grandes, metáfora clara, títulos sin encimarse, subtítulos legibles, amanecer al final. Corrige y repite hasta que esté bien.
```bash
HYPERFRAMES_BROWSER_PATH=/usr/bin/google-chrome npx --yes hyperframes@0.9.43 render --fps 24 --video-bitrate 7M --max-bitrate 8M -o renders/raw.mp4   # timeout 600000
ffmpeg -y -i renders/raw.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k renders/quietmind_slug.mp4
```
- Verifica el final: duración correcta, saca 4–5 cuadros con ffmpeg y míralos.
- Tip de tiempo: mientras corre el render (en segundo plano dentro del mismo turno), escribe el guion y genera la voz del siguiente video.

## 4. Publicar
```bash
cd /home/claude/quietmind && git pull -q --rebase
mkdir -p videos && cp $P/renders/quietmind_slug.mp4 videos/ && git add videos guiones && git commit -qm "Add slug" && git push   # si el push falla por cambios remotos: git pull --rebase y reintenta (hasta 3 veces)
curl -sS -L -o /dev/null -w "%{http_code} %{size_download}\n" https://raw.githubusercontent.com/ArmandoMar334/quietmind/main/videos/quietmind_slug.mp4   # debe dar 200 y el tamaño del archivo
```
Metricool (`createScheduledPost`), blogId `8320706`, date en ISO con `-06:00`, info:
```json
{"autoPublish": true, "descendants": [], "draft": false, "firstCommentText": "", "hasNotReadNotes": false,
 "media": ["https://raw.githubusercontent.com/ArmandoMar334/quietmind/main/videos/quietmind_slug.mp4"], "mediaAltText": [],
 "providers": [{"network": "youtube"}, {"network": "tiktok"}],
 "publicationDate": {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "America/Chihuahua"},
 "shortener": false, "smartLinkData": {"ids": []},
 "text": "Descripción de 1–2 frases.\n\n#motivacion #crecimientopersonal #shorts #reflexion #frasesmotivadoras #desarrollopersonal #superacionpersonal #mentalidad #parati #fyp #TAG_DEL_TEMA1 #TAG_DEL_TEMA2",
 "youtubeData": {"title": "Frase gancho + emoji | Tema", "type": "short", "privacy": "public", "tags": ["motivacion", "crecimiento personal", "shorts"], "madeForKids": false},
 "tiktokData": {"title": "Frase gancho + emoji", "privacyOption": "PUBLIC_TO_EVERYONE", "disableComment": false, "disableDuet": false, "disableStitch": false, "autoAddMusic": false}}
```
- Hashtags: entre 10 y 12, nunca más de 15 (YouTube ignora todos si pasan de 15). Siempre los 10 fijos de arriba + 1 o 2 del tema en español, sin acentos ni espacios (ej. #elfaro #nuncaterindas). En youtubeData.tags agrega también 3–4 palabras clave del tema.
- Cada video va a **YouTube Shorts y TikTok** en el mismo post. En TikTok no envíes isAigc (ni ninguna etiqueta de IA). Para TikTok usa en `text` la misma descripción con hashtags; si Metricool rechaza el post por TikTok, prográmalo solo en YouTube y anota el error en log/.
- La respuesta debe traer `media` en `static.metricool.com` (Metricool ya copió el video). Si la fecha ya pasó, usa el siguiente horario libre (10:00 o 16:00) y anótalo.
- Después de programar: quita tu video del repo (`git rm videos/quietmind_slug.mp4`), actualiza tu fila de `temas.md` a `programado (plannerUrl)`, agrega el tema a la lista de usados en `kit/GUIA.md`, commit y push (con `pull --rebase` si hace falta).

## 5. Cierre
Deja en `log/AAAA-MM-DD_tarea.md` un resumen corto: temas hechos, horarios, enlaces del planner y cualquier problema.
