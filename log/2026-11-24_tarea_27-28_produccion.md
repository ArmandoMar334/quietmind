# 2026-11-24, sesión automática de producción (#27 y #28)

Resultado: **2 videos programados** en YouTube Shorts + TikTok (sin etiquetas de IA, 12 hashtags cada uno).

| # | Tema | Publicación | Duración | Planner |
|---|---|---|---|---|
| 27 | La mano extendida | 2026-12-07 10:00 (America/Chihuahua) | 1:40 | https://app.metricool.com/planner/calendar?blogId=8320706&openWithPostUuid=-5706600840890594974 |
| 28 | Los que se fueron | 2026-12-07 16:00 (America/Chihuahua) | 1:31 | https://app.metricool.com/planner/calendar?blogId=8320706&openWithPostUuid=2245652840370487514 |

## Detalles
- Voces nuevas con ElevenLabs (eleven_v3, Chuck Miller, 1 generación cada una: 1,579 + 1,389 créditos). Descarga directa con curl desde elevenlabsusercontent.com: OK.
- Alineación de subtítulos con transcripción local (faster-whisper small) además de silencedetect.
- #27 animación: caminante cargando piedras → cae a un pozo (corte transversal), intentos de trepar, figura arrodillada en la orilla con la mano extendida, cono de luz cálida, compañeros con faroles, huellas de manos en las paredes, hilo de luz que baja, sube y amanece en la orilla.
- #28 animación: mesa con lámpara bajo un árbol de otoño; las personas se desvanecen, puerta que se cierra de golpe, el árbol suelta sus hojas, siluetas que se alejan y se vuelven faroles, sillas llenas de fantasmas, una silla libre que se ilumina, una puerta nueva que se abre y alguien llega a sentarse; amanecer con flores.
- Videos: 86 MB y 78 MB (aviso de GitHub >50 MB, pero el push pasó). Metricool copió ambos a static.metricool.com; luego se quitaron del repo.
- Push: hubo choques con otras sesiones (cannot lock ref); se resolvieron con pull --rebase y reintento.
