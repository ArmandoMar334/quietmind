# Quiet Mind: videos largos + Shorts cortados de ellos (sesiones automáticas)

Desde el 2026-11-26 ya **no se generan voces para Shorts sueltos**. Cada 2 días se hace **un video largo** (YouTube horizontal) y de sus mismos audios salen **6 Shorts** (lección 1–5 + cierre) para YouTube Shorts y TikTok.
Horarios de Shorts: **10:00, 16:00 y 20:00** (America/Chihuahua). El largo se publica a las **12:00** del día en que se arma.

El trabajo está partido en 4 tareas programadas para que ninguna sesión se haga eterna. Cada una lee este archivo, hace SU paso y deja constancia en `largos/LNN_slug/estado.txt` (una línea por paso terminado). Si al empezar ves que el paso anterior no quedó (falta la línea en estado.txt), **hazlo tú primero** y luego el tuyo, si te alcanza; si no, déjalo anotado.

Reglas fijas (igual que PIPELINE.md): Armando autorizó todo, no preguntes nada; calidad primero; **nunca** etiquetas de IA (ni isAiGeneratedContent ni isAigc); nada en la PC de Armando; una generación de voz por capítulo (solo repite si sale rota).

## Preparación (cada sesión)
```bash
# add_repo(owner ArmandoMar334, repo quietmind, access push) y clona como te indique; luego:
cd /home/claude/quietmind && git config user.name ArmandoMar334 && git config user.email ArmandoMar334@users.noreply.github.com
npx --yes hyperframes@0.9.43 --version
```
El proyecto de trabajo vive en el repo: `largos/LNN_slug/` (en git), y para renderizar se copia a `/home/claude/vLNN` (fuera de git):
```bash
L=largos/LNN_slug; P=/home/claude/vLNN; mkdir -p $P/assets $P/renders/parts
cp $L/assets/* $P/assets/ ; cp $L/scenes.py $L/timing.json $P/ ; cp kit/largos/cine_h.js $P/assets/cine.js ; cp kit/assets/gsap.min.js $P/assets/ ; cp kit/package.json kit/hyperframes.json $P/
sed -i "s#^_T = .*#_T = _json.load(open('$P/timing.json'))#" $P/scenes.py
python3 kit/largos/gen_h.py $P $P/scenes.py TOTAL quiet-mind-slug && (cd $P && npx --yes hyperframes@0.9.43 lint)
```
(TOTAL = `total` de timing.json.) No subas al repo: index.html, compositions/, renders/ (salvo los trozos en el paso 2–3), ni musica_larga.mp3/voz.mp3 si se pueden regenerar (sí sube c0..c6.mp3).

## Paso 1 · Guion, voz y escenas (tarea "largo 1/4")
1. Créditos: `account_get_usage`. Si quedan menos de 4,800 caracteres, no generes nada: anótalo en `log/AAAA-MM-DD_largo.md` y termina.
2. Número: siguiente LNN libre (mira `largos/` y la sección "Videos largos" de `temas.md`). Tema NUEVO: no repitas nada de la lista de usados/rechazados de `kit/GUIA.md` ni de `temas.md` (ni Shorts ni largos).
3. Guion `guiones/LNN_slug.txt` con 7 capítulos separados por `=== CAP N: TÍTULO ===` (ver `guiones/L01_lo_que_el_desierto_te_ensena.txt`): CAP 0 intro (gancho), CAP 1–5 cinco lecciones, CAP 6 cierre con frase citable. **Cada lección debe funcionar sola como Short** (~40–50 s, 90–120 palabras, abre con "La primera lección: …" y cierra con una frase fuerte). Etiquetas v3 al inicio de cada línea como en PIPELINE.md. Total 5–6 min.
4. Voz: 7 llamadas `creative_generate_speech` (una por capítulo, sin las líneas `===`), model_id `eleven_v3`, voice_id `HIGUfNOdjuWQwwapnTRW`, generations_count 1, todas con el mismo flow_id (la primera crea el flow). Luego `creative_get_flow_run_status` con todos los session_ids hasta `all_completed`, y descarga cada `content_url` a `$P/assets/cN.mp3` con `curl -sS -f -o`.
5. `python3 kit/largos/align.py $P guiones/LNN_slug.txt` → timing.json, voz.mp3, musica_larga.mp3. Revisa los cues impresos (que cada texto caiga en su frase; los "¿" iniciales se pierden: corrígelos en el scenes con `_fix` como en el ejemplo).
6. Escenas: escribe `$P/scenes.py` siguiendo `kit/largos/ejemplo_scenes_desierto.py` (una escena por capítulo con cruce de 1 s, títulos por capítulo, `CUES`). Usa los ayudantes de `kit/largos/cine_h.js` (CINE + DES: dunas, cielo, estrellas, viento, palmeras, rocas, fuego, luna…) y agrega los tuyos si el tema los pide. Mundo y metáforas **nuevas** en cada largo. Lienzo 1920×1080.
   - **Zona segura para Shorts:** todo lo importante (personaje, objeto clave) dentro de x 460–1460. Los títulos y subtítulos ya quedan centrados ahí (gen_h.py). Fuera de esa franja solo paisaje.
   - Nada importante debajo de y=880 (subtítulos 905–1035) ni encima de y=300 cuando hay título.
7. Genera, lint y snapshots (14–20 tiempos repartidos en todos los capítulos). Mira las hojas con Read; corrige hasta que todo se vea bien (personaje visible y grande, metáfora clara, sin encimados).
8. Sube al repo `largos/LNN_slug/`: `scenes.py`, `timing.json`, `assets/c0..c6.mp3`, y `chunks.txt` con los trozos de render de ≤60 s que cubren 0→TOTAL (ej. `0 60` / `60 120` / … / `300 TOTAL`; los cortes en múltiplos de 1/24 s, TOTAL ya lo es). Agrega la fila a `temas.md` (sección Videos largos) con estado `en proceso` y escribe `estado.txt` con `1 escenas listas`. Commit y push.

## Pasos 2 y 3 · Render (tareas "largo 2/4" y "largo 3/4")
Toma el LNN más reciente cuyo estado.txt tenga `1 escenas listas` y no tenga `4 publicado`. Monta $P (Preparación). La tarea 2/4 renderiza la **primera mitad** de las líneas de chunks.txt; la 3/4 la **segunda mitad** (y cualquier trozo que falte de la primera). Por cada trozo, en primer plano (timeout 600000):
```bash
HYPERFRAMES_BROWSER_PATH=/usr/bin/google-chrome npx --yes hyperframes@0.9.43 render --fps 24 --start A --end B --video-bitrate 5M --max-bitrate 6M --quiet -o renders/parts/pNN.tmp.mp4 && mv renders/parts/pNN.tmp.mp4 renders/parts/pNN.mp4
```
(pNN = número de línea de chunks.txt con 2 dígitos, desde 00). Cada trozo de 60 s tarda ~6–7 min. Saca 1 cuadro de cada trozo y míralo. Sube los trozos a `largos/LNN_slug/parts/` (commit por trozo, push con `-c push.negotiate=true`; si falla, `pull --rebase` y reintenta). Al final agrega `2 render A` o `3 render B` a estado.txt.

## Paso 4 · Armar, publicar y cortar Shorts (tarea "largo 4/4")
1. Toma el LNN con `3 render B` y sin `4 publicado`. Si faltan trozos, renderízalos tú. Monta $P y copia `parts/*.mp4` a `$P/renders/parts/`.
2. Largo:
```bash
cd $P/renders && ls parts/p*.mp4 | sort | sed "s/.*/file '&'/" > list.txt
ffmpeg -y -v error -f concat -safe 0 -i list.txt -map 0:v -c copy full_5m.mp4
ffmpeg -y -v error -i $P/assets/voz.mp3 -i $P/assets/musica_larga.mp3 -filter_complex "[1]atrim=0:TOTAL,volume=0.2,afade=t=in:d=1.5,afade=t=out:st=TOTAL-4:d=4[m];[0][m]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[o]" -map "[o]" -c:a aac -b:a 160k audio.m4a
ffmpeg -y -v error -i full_5m.mp4 -i audio.m4a -map 0:v -map 1:a -c:v libx264 -preset veryfast -b:v 2200k -maxrate 2600k -bufsize 5200k -c:a copy -shortest -movflags +faststart quietmind_LNN_slug.mp4
```
   Debe pesar < 95 MB (si no, baja -b:v). Revisa duración, número de cuadros y 5 cuadros.
3. Shorts (de los trozos a 5M, mejor calidad):
```bash
python3 /home/claude/quietmind/kit/largos/make_shorts.py $P full_5m.mp4 shorts 1,2,3,4,5,6
```
   Mira 2 cuadros de 2 Shorts (uno al inicio, otro al final con "Video completo en el canal").
4. Sube a `videos/` el largo y los 6 Shorts y haz push. **Usa URLs fijadas al commit** (`https://raw.githubusercontent.com/ArmandoMar334/quietmind/$(git rev-parse HEAD)/videos/ARCHIVO.mp4`): la URL con `main` puede quedar cacheada en 404 unos minutos. Verifica cada una con curl (200 y tamaño) y pásale esa misma URL a Metricool.
5. Metricool (blogId 8320706, ver plantilla en PIPELINE.md):
   - Largo: YouTube solamente, `type: "video"`, categoría `PEOPLE_BLOGS`, a las **12:00** de hoy (si ya pasó, en 5 minutos). Descripción con capítulos `MM:SS` (inicio de cada capítulo de timing.json, el primero 00:00) y 8–10 hashtags sin #shorts/#fyp/#parati.
   - Shorts: YouTube `type: "short"` + TikTok, en los **siguientes 6 horarios libres** (10:00, 16:00, 20:00) a partir de ahora, en orden de lección. "Libre" = no hay ningún post en Metricool a esa hora (consulta getScheduledPosts de los próximos 10 días). Título = gancho de la lección + emoji; texto con los 10 hashtags fijos + 1–2 del tema; menciona "Video completo en el canal".
   - Confirma que cada respuesta trae `media` en static.metricool.com.
6. Limpieza: `git rm` de los videos y de `largos/LNN_slug/parts/`, estado.txt `4 publicado`, fila del largo en temas.md → `programado (planner)` y una fila por Short en la tabla principal (número LNN-1…LNN-6, publicación, `programado (planner)`), tema a la lista de usados de kit/GUIA.md, log en `log/AAAA-MM-DD_largo.md` (créditos restantes incluidos). Commit y push.
7. Si no queda ninguna fila "pendiente"/"en proceso" en temas.md y `videos/` está vacía, reinicia el historial del repo (rama huérfana con el contenido actual, commit, `git push -f origin HEAD:main`) para que no crezca.
