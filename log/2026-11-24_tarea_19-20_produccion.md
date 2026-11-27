# 2026-11-24, sesión automática de producción (#19 y #20)

Resultado: **2 videos programados** en YouTube Shorts + TikTok (sin etiquetas de IA, 12 hashtags).

| # | Tema | Publicación | Planner |
|---|---|---|---|
| 19 | El volante | 2026-12-03 10:00 (America/Chihuahua) | https://app.metricool.com/planner/calendar?blogId=8320706&openWithPostUuid=331891390907238092 |
| 20 | La ventana | 2026-12-03 16:00 (America/Chihuahua) | https://app.metricool.com/planner/calendar?blogId=8320706&openWithPostUuid=3424986257030794206 |

## Detalles
- Voces nuevas con ElevenLabs (eleven_v3, Chuck Miller, 1 generación cada una, ~3,190 créditos en total); descarga con curl funcionó. Duraciones: 109.2 s y 104.4 s (algo más largas que el objetivo de 1:30 porque los guiones tienen muchas pausas).
- Alineación de subtítulos: faster-whisper (small) con marcas por palabra, ajustadas a los silencios de silencedetect.
- #19 animación: vista desde el asiento trasero de un auto de noche; conductor fantasma que desaparece en "Nadie te quitó el volante", volante que se enciende cálido, letreros en la carretera ("ESTUDIA ESTO", "QUÉDATE AQUÍ", "DI QUE SÍ", "← ? →"), frenón con sacudida, niebla al perderse, el copiloto se pasa al volante y amanece en la carretera.
- #20 animación: casa en la tormenta con una persona afuera y otra detrás de la ventana con taza; zooms a cada una, relámpagos en "pérdida, deuda, diagnóstico, puerta", camino de luz de la ventana hacia quien está afuera, tres luces en los vidrios (persona, rutina, pregunta); luego vista desde adentro hacia la ventana, la lluvia se calma y amanece.
- Loudnorm -14 LUFS. Ojo: a 7M el render de 114 s pesa ~103 MB (más que el límite de 100 MB de GitHub); se re-codificó con libx264 a 5.6M (~80 MB). Conviene bajar el bitrate en PIPELINE.md para videos de más de 100 s.
- Ojo: el render de hyperframes se cancela ("render_cancelled_parent_exited") si se lanza con setsid/nohup; lanzarlo con `( ... ) &` normal sí funciona.
- Videos quitados del repo después de programar; temas agregados a usados en kit/GUIA.md.
