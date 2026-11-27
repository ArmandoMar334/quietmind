# 2026-11-24, sesión automática relanzada (#02 y #03)

Resultado: **nada programado**. No quedó ningún post a medias en Metricool.

## Qué pasó
- Probé la red al inicio: el proxy de salida sigue respondiendo `403 (CONNECT tunnel failed)` para `elevenlabsusercontent.com`, `storage.elevenlabsusercontent.com` y `api.elevenlabs.io`. El cambio de dominios permitidos todavía no aplica a las sesiones programadas.
- Las voces de #02 (flow YUK4xAOglYkbS3QCQyXD, nodo completado) y #03 (flow kMsgEN2FhXNwr95ugO7O) ya existen en ElevenLabs, pero no se pueden descargar desde aquí. **No se regeneró nada** (no gasté créditos) y no se intentó rodear el bloqueo.
- Sin el mp3 no hay alineación de subtítulos ni animación, así que #02 y #03 quedan `fallido` en temas.md y no se agregaron a la lista de usados de kit/GUIA.md.

## Para destrabar (cualquiera de las dos)
1. Revisa que `*.elevenlabsusercontent.com` y `api.elevenlabs.io` estén en los dominios permitidos de la red **del entorno de las tareas programadas** (no solo del chat) y que la tarea use ese entorno; luego relanza.
2. Más rápido: descarga los dos mp3 desde el historial de ElevenLabs (TTS OGechsA9ohausBadBYS3 y O2ycjVXeTCHiiBwEeg8q), súbelos al repo como `voces/02.mp3` y `voces/03.mp3` (raw.githubusercontent.com sí funciona) y regresa las filas a `pendiente`.
- #02 era para hoy 16:00; si se reintenta después, toca el siguiente horario libre.

## Corrida relanzada por Armando (06:42 UTC)
- Probé los dos enlaces firmados que venían en la corrida (vencen 09:00 UTC). Ambos fallaron: `403 Forbidden (agent proxy: no rule or network setting allows this host)` para `elevenlabsusercontent.com`. El permiso del dominio todavía no llega al entorno de las tareas programadas.
- Como se indicó, no se regeneró la voz. #02 y #03 quedan `fallido`; nada en Metricool.
- Opción más segura: sube los mp3 al repo como `voces/02.mp3` y `voces/03.mp3` (GitHub sí funciona desde aquí) y relanza. Los enlaces firmados vencen hoy a las 09:00 UTC.
