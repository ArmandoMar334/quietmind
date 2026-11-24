import os, shutil, json, sys
KIT = os.path.dirname(os.path.abspath(__file__))
P = os.path.abspath(sys.argv[1])  # carpeta del proyecto
SCENES = os.path.abspath(sys.argv[2])  # archivo scenes_*.py
TOTAL_ARG = float(sys.argv[3])  # duración total en segundos
NAME = sys.argv[4] if len(sys.argv) > 4 else "quiet-mind"
W, H = 1080, 1920
TOTAL = TOTAL_ARG
os.makedirs(P + "/compositions", exist_ok=True)

for f in ["hyperframes.json", "package.json"]:
    if not os.path.exists(P + "/" + f): shutil.copy(KIT + "/" + f, P + "/" + f)
json.dump({"id": NAME, "name": NAME, "createdAt": "2026-11-14T06:45:00.000Z"}, open(P + "/meta.json", "w"))

CSS = """
#root { position: absolute; inset: 0; overflow: hidden; color: #fff; }
.cv { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
.kick { position: absolute; left: 0; width: 1080px; text-align: center; font-family: Inter, sans-serif; font-size: 30px; font-weight: 700; letter-spacing: 0.34em; color: rgba(255,255,255,0.78); }
.title { position: absolute; left: 40px; width: 1000px; text-align: center; font-family: 'EB Garamond', serif; font-style: italic; font-weight: 400; line-height: 1.0; color: #f4efe6; text-shadow: 0 0 30px rgba(0,0,0,0.8), 0 0 40px rgba(255,220,180,0.2); }
.word { position: absolute; white-space: nowrap; font-family: 'EB Garamond', serif; font-style: italic; color: #f4efe6; text-shadow: 0 0 22px rgba(0,0,0,0.95), 0 0 8px rgba(0,0,0,0.9); }
"""

def scene(cid, dur, markup, draw, js_extra):
    return f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
    <div id="{cid}-wrap" style="position:absolute; inset:0;">
    <canvas id="{cid}-cv" class="cv" width="{W}" height="{H}"></canvas>
{markup}
    </div>
  </div>
  <script>
    (function () {{
    const tl = gsap.timeline({{ paused: true }});
    const S = (sel) => document.querySelector('[data-composition-id="{cid}"] ' + sel);
    const C = window.CINE, DUR = {dur};
    const ctx = S("#{cid}-cv").getContext("2d");
    const st = {{ t: 0 }};
    function draw() {{
      const t = st.t;
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.filter = "none"; ctx.globalAlpha = 1; ctx.globalCompositeOperation = "source-over";
      ctx.fillStyle = "#000"; ctx.fillRect(0, 0, C.W, C.H);
      ctx.save();
{draw}
      ctx.restore();
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      C.vignette(ctx, 0.8);

    }}
    draw();
    tl.to(st, {{ t: DUR, duration: DUR, ease: "none", onUpdate: draw }}, 0);
    if (FADE_IN > 0.01) tl.fromTo(S("#{cid}-wrap"), {{ opacity: 0 }}, {{ opacity: 1, duration: FADE_IN, ease: "none" }}, 0);
{js_extra}
    window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
"""

def fades(js, fin, fout):
    return js.replace("FADE_IN", str(fin)).replace("FADE_OUT", str(fout))

exec(open(SCENES).read())

hosts = []
for zi, (cid, st, du, fin, markup, draw, extra) in enumerate(S):
    html = fades(scene(cid, du, markup, draw, extra), fin, 0)
    open(f"{P}/compositions/{cid}.html", "w").write(html)
    hosts.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{st}" data-duration="{du}" data-track-index="{1 + zi % 2}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{1 + zi}"></div>')

# ---------------- grain ----------------
grain = f"""<template>
  <style>#root {{ position: absolute; inset: 0; pointer-events: none; }} #gr-cv {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}</style>
  <div id="root" data-composition-id="grain" data-width="{W}" data-height="{H}">
    <canvas id="gr-cv" width="540" height="960"></canvas>
  </div>
  <script>
    (function () {{
    const tl = gsap.timeline({{ paused: true }});
    const C = window.CINE;
    const cv = document.querySelector('[data-composition-id="grain"] #gr-cv'), ctx = cv.getContext("2d");
    const tile = document.createElement("canvas"); tile.width = tile.height = 192;
    const tc = tile.getContext("2d"), img = tc.createImageData(192, 192), r = C.rng(99);
    for (let i = 0; i < img.data.length; i += 4) {{ const v = Math.floor(r() * 255); img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255; }}
    tc.putImageData(img, 0, 0);
    const pat = ctx.createPattern(tile, "repeat");
    const st = {{ t: 0 }};
    function draw() {{
      const f = Math.floor(st.t * 24), rr = C.rng(f * 7919 + 13);
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, 540, 960);
      ctx.globalAlpha = 0.07; ctx.translate(-Math.floor(rr() * 192), -Math.floor(rr() * 192));
      ctx.fillStyle = pat; ctx.fillRect(0, 0, 540 + 192, 960 + 192);
    }}
    draw();
    tl.to(st, {{ t: {TOTAL}, duration: {TOTAL}, ease: "none", onUpdate: draw }}, 0);
    window.__timelines["grain"] = tl;
    }})();
  </script>
</template>
"""
open(P + "/compositions/grain.html", "w").write(grain)

# ---------------- captions ----------------
cm, cj = [], []
for i, (a, b, t) in enumerate(CUES):
    s = max(0.0, a - 0.08)
    nxt = CUES[i + 1][0] - 0.1 if i + 1 < len(CUES) else TOTAL
    e = TOTAL if i + 1 == len(CUES) else min(b + 0.4, nxt)
    words = " ".join(f'<span class="w">{w}</span>' for w in t.split())
    cm.append(f'    <div id="cap{i}" class="clip cap" data-start="{s:.2f}" data-duration="{e - s:.2f}"><div id="cap{i}-in" class="capin">{words}</div></div>')
    n = len(t.split())
    cj.append(f'    tl.fromTo("#cap{i}-in .w", {{ opacity: {1 if i == 0 else 0.25} }}, {{ opacity: 1, duration: 0.12, stagger: {max(0.05, (b - a) / n):.3f}, ease: "none" }}, {a:.2f});')
CAPCSS = """
#root { position: absolute; inset: 0; }
.cap { position: absolute; left: 90px; width: 900px; top: 1140px; height: 180px; display: flex; align-items: flex-start; justify-content: center; }
.capin { text-align: center; font-family: Inter, sans-serif; font-size: 48px; font-weight: 700; line-height: 1.22; color: #fff; text-shadow: 0 2px 16px rgba(0,0,0,0.9), 0 0 4px rgba(0,0,0,0.8); }
"""
open(P + "/compositions/caps.html", "w").write(f"""<template>
  <style>{CAPCSS}</style>
  <div id="root" data-composition-id="caps" data-width="{W}" data-height="{H}">
{chr(10).join(cm)}
  </div>
  <script>
    (function () {{
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(cj)}
    window.__timelines["caps"] = tl;
    }})();
  </script>
</template>
""")

open(P + "/index.html", "w").write(f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/gsap.min.js"></script>
    <script src="assets/cine.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ width: 100%; height: 100%; position: relative; background: #000; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{chr(10).join(hosts)}
      <div id="grain" data-composition-id="grain" data-composition-src="compositions/grain.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:20"></div>
      <div id="caps" data-composition-id="caps" data-composition-src="compositions/caps.html" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:30"></div>
      <audio id="voz" class="clip" src="assets/voz.mp3" data-start="0" data-track-index="5" data-volume="1"></audio>
      <audio id="musica" class="clip" src="assets/musica_larga.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="6" data-volume="0.2" data-fade-in="1" data-fade-out="3"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")
print("ok")
