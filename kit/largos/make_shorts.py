#!/usr/bin/env python3
"""Corta Shorts verticales (1080x1920) desde el video largo horizontal de Quiet Mind.

Uso:
  python3 make_shorts.py PROYECTO VIDEO_LARGO.mp4 SALIDA_DIR CAPS [--label "Texto"]
  --offset N: segundos del largo donde empieza VIDEO (si es un trozo); por defecto 0
  CAPS: capítulos a cortar, ej. "1,2,3,4,5,6"

Requiere en PROYECTO: timing.json (chapters con start/dur) y assets/c{i}.mp3 (voz de cada capítulo),
assets/musica_larga.mp3. El video largo debe tener títulos y subtítulos dentro del cuadro central
(x 420–1500), que es lo que se recorta.
Cada Short: cuadro central 1080x1080 sin escalar, fondo del mismo video desenfocado,
"QUIET MIND" arriba y "Video completo en el canal" al final.
"""
import json, os, subprocess, sys

proj, src, out, caps = sys.argv[1], sys.argv[2], sys.argv[3], [int(x) for x in sys.argv[4].split(',')]
off = float(sys.argv[sys.argv.index('--offset') + 1]) if '--offset' in sys.argv else 0.0
label = sys.argv[sys.argv.index('--label') + 1] if '--label' in sys.argv else 'Video completo en el canal'
T = json.load(open(os.path.join(proj, 'timing.json')))
CH, TOTAL = T['chapters'], T['total']
os.makedirs(out, exist_ok=True)
FB = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
FM = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:]); sys.exit(1)

for i in caps:
    ch = CH[i]
    s = ch['start']
    e = (s + ch['dur'] + 0.9) if i + 1 < len(CH) else TOTAL - 0.05
    d = round(e - s, 3)
    voice = os.path.join(proj, 'assets', f'c{i}.mp3')
    music = os.path.join(proj, 'assets', 'musica_larga.mp3')
    tmp = os.path.join(out, f'short_c{i}.tmp.mp4')
    dst = os.path.join(out, f'short_c{i}.mp4')
    endt = max(0, d - 4.5)
    vf = (
        f"[0:v]trim=start={s - off}:duration={d},setpts=PTS-STARTPTS,split=2[a][b];"
        f"[a]crop=326:580:797:300,scale=270:480,boxblur=10:2,scale=1080:1920,eq=brightness=-0.10:saturation=0.9[bg];"
        f"[b]crop=1080:1080:420:0[fg];"
        f"[bg][fg]overlay=0:420,"
        f"drawbox=x=0:y=410:w=1080:h=10:color=black@0.25:t=fill,drawbox=x=0:y=1500:w=1080:h=10:color=black@0.25:t=fill,"
        f"drawtext=fontfile={FB}:text='Q U I E T   M I N D':fontsize=30:fontcolor=white@0.80:x=(w-tw)/2:y=300,"
        f"drawtext=fontfile={FM}:text='{label}':fontsize=40:fontcolor=white:x=(w-tw)/2:y=1600:"
        f"alpha='if(lt(t,{endt}),0,min(1,(t-{endt})/0.6))':shadowcolor=black@0.8:shadowx=0:shadowy=2,"
        f"fade=t=in:st=0:d=0.4,fade=t=out:st={d - 0.8}:d=0.8,format=yuv420p[v];"
        f"[1:a]aresample=48000,apad,atrim=0:{d}[vo];"
        f"[2:a]atrim=start={s}:duration={d},asetpts=PTS-STARTPTS,volume=0.2,afade=t=in:d=0.6,afade=t=out:st={d - 1.5}:d=1.5[mu];"
        f"[vo][mu]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[au]"
    )
    run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-i', voice, '-i', music, '-filter_complex', vf,
         '-map', '[v]', '-map', '[au]', '-r', '24', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(d), tmp])
    os.replace(tmp, dst)
    print(dst, d)
