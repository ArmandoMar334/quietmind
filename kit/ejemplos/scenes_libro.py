S = []

STAGE = """
      const T = t;
      const keys = (K, T) => { if (T <= K[0][0]) return K[0][1]; for (let i = 1; i < K.length; i++) if (T <= K[i][0]) { const k = (T - K[i-1][0]) / (K[i][0] - K[i-1][0]); return C.lerp(K[i-1][1], K[i][1], C.ease(k)); } return K[K.length-1][1]; };
      const P = (a, b) => C.ease(C.prog(T, a, b));
      const COLD = [170, 188, 225], WARMC = [255, 196, 136], INK = [16, 14, 18];
      const txt = (s, x, y, size, col, a, o) => { if (a <= 0.01) return; o = o || {}; ctx.save(); ctx.globalAlpha = a; ctx.font = (o.italic ? "italic " : "") + (o.w || "") + " " + size + "px " + (o.italic ? "'EB Garamond', Georgia, serif" : "Inter, sans-serif"); ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.shadowColor = "rgba(0,0,0,0.9)"; ctx.shadowBlur = 16; ctx.fillStyle = col; ctx.fillText(s, x, y); ctx.restore(); };
      const L0 = 60, MID = 540, R1 = 1020, TOP = 420, BOT = 1080, PW = 480;
      // ---------- state ----------
      const open = P(0.6, 3.2);
      const dark = P(5.9, 14) * (1 - P(38.8, 40.5) * 0.7 * (1 - P(41.3, 42.7)));
      const blank = P(47.9, 49.2);
      const warm = Math.max(P(38.8, 41) * 0.5 * (1 - P(42.7, 43.5)), P(50.2, 52) * 0.5, P(64.2, 72));
      const CZ = keys([[0,1.05],[5,1.0],[22.4,1.0],[25,0.6],[29,0.6],[30.8,0.92],[41.3,0.92],[42.7,1.0],[64,1.0],[76,1.06]], T);
      // background
      { const g = ctx.createRadialGradient(540, 760, 50, 540, 760, 1200); g.addColorStop(0, C.rgba(C.mixc([26, 24, 32], [70, 46, 36], warm), 1)); g.addColorStop(1, "#030304"); ctx.fillStyle = g; ctx.fillRect(0, 0, 1080, 1920); }
      ctx.save(); ctx.translate(540, 760); ctx.scale(CZ, CZ); ctx.translate(-540, -760);
      // future pages stack (right) and past pages (left)
      { const st = 18; for (let i = st; i > 0; i--) { ctx.fillStyle = C.rgba(C.mixc([150, 140, 125], [60, 56, 52], dark * 0.6), 1); ctx.fillRect(R1 - 6 + i * 3, TOP + 6 + i * 2.2, 6, BOT - TOP); } for (let i = 6; i > 0; i--) { ctx.fillStyle = "rgba(120,112,100,1)"; ctx.fillRect(L0 - i * 3, TOP + 6 + i * 2.2, 6, BOT - TOP); } }
      C.glow(ctx, 540, 760, 700, C.mixc([200, 190, 170], WARMC, warm), 0.12 + 0.25 * open * (1 - dark * 0.7) + 0.2 * warm);
      // pages
      const pageCol = (side) => { const b = side === 1 ? blank : 0; return C.mixc(C.mixc([228, 218, 196], [70, 66, 64], dark * (1 - b)), [255, 246, 226], b); };
      const page = (x0, side, a) => { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.rgba(pageCol(side), 1); ctx.beginPath(); ctx.moveTo(x0, TOP + 10); ctx.quadraticCurveTo(x0 + PW / 2, TOP - 14, x0 + PW, TOP + 10 * (side === 0 ? 0 : 1)); ctx.lineTo(x0 + PW, BOT); ctx.quadraticCurveTo(x0 + PW / 2, BOT - 18, x0, BOT); ctx.closePath(); ctx.fill(); ctx.restore(); };
      // closed book opening
      if (open < 1) { const w = PW * (1 - open); ctx.fillStyle = "#3a1f18"; ctx.fillRect(MID, TOP - 10, PW + 10, BOT - TOP + 20); ctx.save(); ctx.globalAlpha = 1; ctx.fillStyle = "#4a281e"; ctx.fillRect(MID - w, TOP - 10, w, BOT - TOP + 20); ctx.restore(); }
      if (open > 0.02) { page(L0 + PW * (1 - open), 0, open); page(MID, 1, 1); }
      // gutter
      { const g = ctx.createLinearGradient(MID - 40, 0, MID + 40, 0); g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(0.5, "rgba(0,0,0,0.35)"); g.addColorStop(1, "rgba(0,0,0,0)"); ctx.fillStyle = g; ctx.fillRect(MID - 40, TOP, 80, BOT - TOP); }
      // text lines on pages (texture)
      { const a = open * (1 - P(29, 30.8)) * 1 + P(41.3, 42.7); ctx.fillStyle = C.rgba(INK, 0.12 * a); for (let side = 0; side < 2; side++) { if (side === 1 && blank > 0.5) continue; for (let i = 0; i < 18; i++) { const y = TOP + 60 + i * 30, x0 = side ? MID + 50 : L0 + 50; ctx.fillRect(x0, y, 380 - ((i * 37) % 90), 5); } } }
      // ink rain and blots
      { const r = C.rng(5); for (let i = 0; i < 26; i++) { const t0 = 6 + r() * 12, x = L0 + 40 + r() * 900, y = TOP + 60 + r() * 560, rr = 14 + r() * 36; const k = C.clamp((T - t0) / 0.6); if (k <= 0) continue;
          const onRight = x > MID; const vis = (onRight ? 1 - blank : 1) * (1 - P(29.0, 30.8)) + P(41.3, 42.7) * (onRight ? 1 - blank : 1);
          if (k < 1) { ctx.fillStyle = C.rgba(INK, 0.9 * vis); ctx.beginPath(); ctx.ellipse(x, C.lerp(TOP - 300, y, k), 5, 12, 0, 0, 6.283); ctx.fill(); }
          else { ctx.fillStyle = C.rgba(INK, 0.85 * vis); ctx.beginPath(); for (let j = 0; j < 10; j++) { const q = j / 10 * 6.283, d = rr * (0.8 + 0.3 * Math.sin(j * 2.3 + i)); ctx.lineTo(x + Math.cos(q) * d, y + Math.sin(q) * d * 0.8); } ctx.closePath(); ctx.fill(); } } }
      // ---------- the story flipping ----------
      const flipA = P(30.6, 31.0) * (1 - P(41.0, 41.4));
      const story = (kind, x0, a, light) => { if (a <= 0.01) return; ctx.save(); ctx.globalAlpha = a; const cx = x0 + PW / 2, cy = 820; ctx.fillStyle = C.rgba(INK, 0.9); ctx.strokeStyle = C.rgba(INK, 0.9); ctx.lineWidth = 6;
        if (light > 0.01) { C.glow(ctx, cx, cy - 200, 200, WARMC, 0.6 * light); ctx.fillStyle = C.rgba([255, 200, 120], light); ctx.beginPath(); ctx.arc(cx, cy - 200, 46, 0, 6.283); ctx.fill(); ctx.fillStyle = C.rgba(INK, 0.9); }
        if (kind === 0) { ctx.save(); ctx.translate(cx + 60, cy + 150); ctx.rotate(-Math.PI / 2); C.person(ctx, 0, 0, 150, { fill: C.rgba(INK, 0.9) }); ctx.restore(); ctx.save(); ctx.translate(cx - 80, cy + 150); ctx.rotate(-0.7); ctx.fillRect(-4, -110, 8, 110); ctx.restore(); }
        if (kind === 1) { ctx.beginPath(); ctx.arc(cx - 50, cy - 40, 50, 0, 6.283); ctx.arc(cx + 20, cy - 60, 64, 0, 6.283); ctx.arc(cx + 90, cy - 30, 44, 0, 6.283); ctx.fill(); ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx - 30, cy + 70); ctx.lineTo(cx + 6, cy + 76); ctx.lineTo(cx - 24, cy + 160); ctx.stroke(); }
        if (kind === 2) { ctx.save(); ctx.translate(cx, cy + 90); ctx.rotate(0.4); ctx.beginPath(); ctx.moveTo(-90, -20); ctx.lineTo(90, -20); ctx.lineTo(60, 20); ctx.lineTo(-60, 20); ctx.closePath(); ctx.fill(); ctx.fillRect(-4, -130, 8, 110); ctx.beginPath(); ctx.moveTo(4, -126); ctx.lineTo(60, -40); ctx.lineTo(4, -40); ctx.fill(); ctx.restore(); ctx.beginPath(); for (let x = x0 + 30; x < x0 + PW - 30; x += 10) ctx.lineTo(x, cy + 150 + Math.sin(x * 0.05 + T * 3) * 12); ctx.stroke(); }
        ctx.restore(); };
      if (flipA > 0.01) { const tt = C.clamp(T - 30.8, 0, 7.5), i = Math.min(5, Math.floor(tt / 1.25)), k = (tt / 1.25) % 1; const light = P(38.8, 40.0);
        story(i % 3, L0, flipA, light); story((i + 1) % 3, MID, flipA, light);
        // the turning page
        if (T < 38.4) { const ang = k * Math.PI, w = PW * Math.cos(ang); ctx.save(); ctx.globalAlpha = flipA; ctx.fillStyle = C.rgba(C.mixc(pageCol(1), [0, 0, 0], 0.25 * Math.sin(ang)), 1); ctx.fillRect(MID + Math.min(0, w), TOP + 4, Math.abs(w), BOT - TOP - 4); ctx.restore(); } }
      // the page turning to a blank one
      { const k = C.clamp((T - 46.7) / 1.2); if (k > 0 && k < 1) { const w = PW * Math.cos(k * Math.PI); ctx.fillStyle = C.rgba(C.mixc([70, 66, 64], [0, 0, 0], 0.3 * Math.sin(k * 3.14)), 1); ctx.fillRect(MID + Math.min(0, w), TOP + 4, Math.abs(w), BOT - TOP - 4); } }
      if (blank > 0.01) C.glow(ctx, MID + PW / 2, 760, 420, [255, 240, 210], 0.35 * blank);
      // lines you write
      const LINES = [55.9, 57.55, 58.88, 60.43, 61.86];
      LINES.forEach((t0, i) => { const k = P(t0, t0 + 0.9); if (k <= 0.01) return; const y = 1000 - i * 80; ctx.save(); ctx.strokeStyle = C.rgba(WARMC, 0.95); ctx.lineWidth = 5; ctx.lineCap = "round"; ctx.shadowColor = "rgba(255,180,110,0.9)"; ctx.shadowBlur = 14; ctx.beginPath(); for (let j = 0; j <= 40 * k; j++) { const x = MID + 60 + j * 9; ctx.lineTo(x, y + Math.sin(j * 0.5 + i) * 6); } ctx.stroke(); ctx.restore(); });
      // the next pages filling with dawn
      { const d = P(64.2, 70); if (d > 0.01) { ctx.save(); ctx.beginPath(); ctx.rect(MID + 10, TOP + 10, PW - 20, 520); ctx.clip(); const g = ctx.createLinearGradient(0, TOP, 0, TOP + 520); g.addColorStop(0, C.rgba([120, 90, 140], 0.7 * d)); g.addColorStop(1, C.rgba([255, 170, 110], 0.85 * d)); ctx.fillStyle = g; ctx.fillRect(MID, TOP, PW, 520); C.sun(ctx, MID + PW / 2, TOP + 520 - 60 * d, 60, d, null); C.rays(ctx, MID + PW / 2, TOP + 470, T, 0.5 * d, 9, 600); ctx.restore(); } }
      // ---------- figure on the page ----------
      { const onPage = P(5.9, 6.8) * (1 - P(22.4, 24)) + P(42.7, 43.6);
        const X = keys([[0,760],[42,760],[44.6,720],[46,740],[64,740],[72,860]], T); const rub = T > 44.0 && T < 46.0 ? Math.sin(T * 12) * 6 : 0;
        const blur = P(19.7, 21.0) * (1 - P(42.7, 43.5));
        if (onPage > 0.01) { const rim = C.mixc(COLD, WARMC, warm); ctx.save(); ctx.globalAlpha = onPage * (1 - 0.4 * blur); C.person(ctx, X + rub, BOT - 20, 180, { fill: "#0a090c", rim, rimA: 0.75, walk: (T > 6.8 && T < 13) || (T > 64.2 && T < 72) ? T * 6 : null }); ctx.restore();
          if (blur > 0.01) C.glow(ctx, X, BOT - 120, 70, [40, 38, 44], 0.6 * blur);
          // the one you lost, running like ink
          const lost = P(6.5, 7.5) * (1 - P(16.5, 18.6)) * (1 - P(22.4, 24)); if (lost > 0.01 || (T > 16.5 && T < 19)) { const dr = P(16.5, 18.6); ctx.save(); ctx.globalAlpha = Math.max(lost, (1 - dr) * 0.9) * (T < 22.4 ? 1 : 0); C.person(ctx, 640, BOT - 20 + dr * 20, 170 * (1 - 0.3 * dr), { fill: "#0a090c", rim: COLD, rimA: 0.5 }); ctx.restore(); if (dr > 0.01 && dr < 1) { ctx.fillStyle = C.rgba(INK, 0.6 * (1 - dr)); for (let j = 0; j < 6; j++) ctx.fillRect(620 + j * 8, BOT - 150, 4, 60 + dr * 100 * (1 + (j % 3))); } }
          // the pen of light
          const pen = P(50.2, 50.9); if (pen > 0.01) { const s = 180 / 180; ctx.save(); ctx.translate(X + 24, BOT - 20 - 128); ctx.rotate(-0.6); ctx.strokeStyle = C.rgba(WARMC, pen); ctx.lineWidth = 6; ctx.lineCap = "round"; ctx.shadowColor = "rgba(255,190,120,1)"; ctx.shadowBlur = 16; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, -60); ctx.stroke(); ctx.restore(); }
          if (warm > 0.3) C.glow(ctx, X, BOT - 110, 200, WARMC, 0.25 * warm); } }
      ctx.restore();
      C.dust(ctx, T, { n: 50, alpha: 0.2 + 0.3 * warm, seed: 4, warm: warm, speed: 0.2 });
"""

TT = "opacity: 0, y: 24, filter: \"blur(14px)\" }, { opacity: 1, y: 0, filter: \"blur(0px)\", duration: 0.8, ease: \"power3.out\" }"
titles = [
    ("Un mal capítulo<br>no es el libro entero.", "title", 23.99, 27.6, "font-size:84px"),
    ("ahí empieza<br>lo bueno.", "title", 38.81, 42.3, "font-size:108px; color:#ffe2bf"),
    ("La pluma sigue<br>en tu mano.", "title", 50.24, 53.0, "font-size:100px; color:#ffe2bf"),
    ("Solo una línea.", "title", 55.9, 59.6, "font-size:110px; color:#ffe2bf"),
    ("Es el comienzo de<br>la mejor parte.", "title", 69.65, None, "font-size:96px; color:#fff1de"),
]
markup, js = "", '    gsap.set(".hbt", { opacity: 0 });\n'
for i, (txt, cls, a, b, sty) in enumerate(titles):
    markup += f'    <div id="lb-t{i}" class="{cls} hbt" style="top:160px; {sty}">{txt}</div>\n'
    js += f'    tl.fromTo("#lb-t{i}", {{ {TT}, {a});\n'
    if b: js += f'    tl.to("#lb-t{i}", {{ opacity: 0, filter: "blur(10px)", duration: 0.4 }}, {b});\n'

S.append(("lb", 0.0, 76.0, 0.0, markup, STAGE, js))

CUES = [(0.00,4.26,"Si tu vida fuera un libro… ¿en qué capítulo estarías hoy?"),(5.88,7.31,"Tal vez en uno difícil."),(8.26,12.48,"De esos que dan ganas de cerrar el libro… y no volver a abrirlo."),
(13.48,15.68,"Un capítulo donde todo salió mal."),(16.52,18.84,"Donde perdiste algo… o a alguien."),(19.72,21.06,"Donde no te reconoces."),(22.46,23.33,"Pero escucha esto."),
(23.99,26.98,"Un mal capítulo… no es el libro entero."),(27.81,30.10,"Piensa en las historias que más te han marcado."),(30.80,34.58,"En todas… hay un momento donde el personaje lo pierde todo."),
(35.26,36.89,"Y nadie cierra el libro ahí."),(37.60,41.33,"Porque sabemos… que ahí es justo donde empieza lo bueno."),(42.73,46.09,"Las páginas que ya están escritas… no las puedes borrar."),
(46.70,49.59,"Pero la siguiente página… todavía está en blanco."),(50.24,52.09,"Y la pluma… sigue en tu mano."),(53.37,55.45,"No tienes que escribir un final feliz hoy."),
(55.90,59.82,"Solo una línea. Una decisión. Un paso pequeño."),(60.43,63.02,"Mañana otra. Y pasado otra."),(64.25,66.84,"Y un día… vas a releer este capítulo…"),
(67.20,69.17,"y vas a entender que no fue el final."),(69.65,72.91,"Fue el comienzo… de la mejor parte de tu historia.")]
