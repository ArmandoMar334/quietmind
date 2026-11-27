S = []

STAGE = """
      const T = t;
      const keys = (K, T) => { if (T <= K[0][0]) return K[0][1]; for (let i = 1; i < K.length; i++) if (T <= K[i][0]) { const k = (T - K[i-1][0]) / (K[i][0] - K[i-1][0]); return C.lerp(K[i-1][1], K[i][1], C.ease(k)); } return K[K.length-1][1]; };
      const P = (a, b) => C.ease(C.prog(T, a, b));
      const FLY = 1110, COLD = [170, 188, 225], WARMC = [255, 196, 136];
      const txt = (s, x, y, size, col, a, o) => { if (a <= 0.01) return; o = o || {}; ctx.save(); ctx.globalAlpha = a; ctx.font = (o.italic ? "italic " : "") + (o.w || "") + " " + size + "px " + (o.italic ? "'EB Garamond', Georgia, serif" : "Inter, sans-serif"); ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.shadowColor = "rgba(0,0,0,0.9)"; ctx.shadowBlur = 16; ctx.fillStyle = col; ctx.fillText(s, x, y); ctx.restore(); };
      // ---------- masks ----------
      const mask = (x, y, r, kind, a, rot) => { if (a <= 0.01) return; ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.rotate(rot || 0);
        const gold = kind === "social"; const base = gold ? "rgba(255,214,120,0.97)" : "rgba(238,236,232,0.97)";
        if (gold) C.glow(ctx, 0, 0, r * 3, [255, 200, 110], 0.45);
        ctx.fillStyle = base; ctx.beginPath(); ctx.ellipse(0, 0, r * 0.82, r, 0, 0, 6.283); ctx.fill();
        ctx.fillStyle = "#151318"; ctx.strokeStyle = "#151318"; ctx.lineWidth = r * 0.08; ctx.lineCap = "round";
        if (kind === "work") { ctx.beginPath(); ctx.ellipse(-r * 0.3, -r * 0.18, r * 0.14, r * 0.08, 0, 0, 6.283); ctx.ellipse(r * 0.3, -r * 0.18, r * 0.14, r * 0.08, 0, 0, 6.283); ctx.fill(); ctx.beginPath(); ctx.moveTo(-r * 0.25, r * 0.38); ctx.quadraticCurveTo(0, r * 0.46, r * 0.25, r * 0.38); ctx.stroke(); ctx.beginPath(); ctx.moveTo(-r * 0.45, -r * 0.38); ctx.lineTo(-r * 0.15, -r * 0.34); ctx.moveTo(r * 0.45, -r * 0.38); ctx.lineTo(r * 0.15, -r * 0.34); ctx.stroke(); }
        if (kind === "family") { [-1, 1].forEach((d) => { ctx.beginPath(); ctx.arc(d * r * 0.3, -r * 0.16, r * 0.13, Math.PI * 0.1, Math.PI * 0.9); ctx.stroke(); }); ctx.beginPath(); ctx.arc(0, r * 0.22, r * 0.22, 0.3, Math.PI - 0.3); ctx.stroke(); }
        if (kind === "friends" || gold) { [-1, 1].forEach((d) => { ctx.beginPath(); ctx.arc(d * r * 0.3, -r * 0.12, r * 0.13, Math.PI * 1.1, Math.PI * 1.9); ctx.stroke(); }); ctx.beginPath(); ctx.moveTo(-r * 0.4, r * 0.2); ctx.quadraticCurveTo(0, r * 0.75, r * 0.4, r * 0.2); ctx.closePath(); ctx.fill(); }
        if (gold) { for (let i = 0; i < 4; i++) { const q = T * 2 + i * 1.6; ctx.fillStyle = "rgba(255,250,220,0.9)"; ctx.beginPath(); ctx.arc(Math.cos(q) * r * 1.3, Math.sin(q) * r * 1.3, 3, 0, 6.283); ctx.fill(); } }
        ctx.restore(); };
      // ---------- state ----------
      const night = P(27.6, 28.6) * (1 - P(65, 72) * 0.6);
      const settings = [P(5.6, 6.3) * (1 - P(10.5, 11.0)), P(10.5, 11.0) * (1 - P(16.8, 17.3)), P(16.8, 17.3) * (1 - P(23.6, 24.4))];
      const phoneA = P(24.0, 24.6) * (1 - P(27.6, 28.3));
      const mirrorA = (1 - P(5.4, 6.0)) + P(27.8, 28.8) * (1 - P(41.0, 42.0));
      const friendA = P(52.6, 53.8);
      const warm = Math.max(P(56.0, 58) * 0.6, P(66.9, 74));
      const X = 440, H = 380, HX = X, HY = FLY - 0.92 * H, MR = 44;
      const CZ = keys([[0,1.06],[5.6,1.0],[24,1.0],[24.6,1.05],[27.6,1.05],[28.6,1.0],[41,1.0],[50.5,1.08],[51.6,1.0],[78,1.06]], T);
      ctx.save(); ctx.translate(540, 900); ctx.scale(CZ, CZ); ctx.translate(-540, -900);
      // background
      { const g = ctx.createLinearGradient(0, 0, 0, 1920); g.addColorStop(0, C.rgba(C.mixc(C.mixc([30, 28, 34], [8, 9, 16], night), [40, 28, 26], warm), 1)); g.addColorStop(1, "#000"); ctx.fillStyle = g; ctx.fillRect(-200, -200, 1480, 2400); }
      // settings
      if (settings[0] > 0.01) { ctx.save(); ctx.globalAlpha = settings[0]; for (let i = 0; i < 3; i++) { const x = 140 + i * 330; ctx.fillStyle = "#0b0b0e"; ctx.fillRect(x - 100, FLY - 150, 200, 14); ctx.fillRect(x - 90, FLY - 136, 10, 136); ctx.fillRect(x + 80, FLY - 136, 10, 136); ctx.fillStyle = "rgba(150,180,240,0.8)"; ctx.fillRect(x - 40, FLY - 250, 80, 56); C.glow(ctx, x, FLY - 222, 120, [140, 170, 240], 0.35); if (i !== 1) C.person(ctx, x + 60, FLY, 300, { fill: "#08080b", rim: COLD, rimA: 0.3 }); } ctx.restore(); }
      if (settings[1] > 0.01) { ctx.save(); ctx.globalAlpha = settings[1]; C.glow(ctx, 640, 640, 420, WARMC, 0.3); ctx.fillStyle = "#0b0b0e"; ctx.fillRect(637, 420, 6, 180); ctx.beginPath(); ctx.moveTo(590, 600); ctx.lineTo(690, 600); ctx.lineTo(660, 560); ctx.lineTo(620, 560); ctx.fill(); ctx.fillRect(560, FLY - 170, 400, 16); ctx.fillRect(580, FLY - 154, 12, 154); ctx.fillRect(930, FLY - 154, 12, 154);
        [[680, 290], [800, 260], [910, 300]].forEach(([x, h]) => C.person(ctx, x, FLY, h, { fill: "#08080b", rim: WARMC, rimA: 0.35 })); ctx.restore(); }
      if (settings[2] > 0.01) { ctx.save(); ctx.globalAlpha = settings[2]; [[160, 340], [700, 350], [830, 330], [960, 345]].forEach(([x, h], i) => { C.person(ctx, x, FLY, h, { fill: "#08080b", rim: [230, 200, 255], rimA: 0.35 }); ctx.fillStyle = "rgba(255,210,140,0.7)"; ctx.fillRect(x + 24, FLY - h * 0.55, 10, 22); }); C.glow(ctx, 540, 700, 600, [200, 150, 255], 0.12); ctx.restore(); }
      // mirror and reflection
      if (mirrorA > 0.01) { ctx.save(); ctx.globalAlpha = Math.min(1, mirrorA); const mx = 640, my = 500, mw = 300, mh = 600;
        ctx.fillStyle = C.rgba(C.mixc([40, 44, 58], [70, 56, 50], warm), 1); ctx.fillRect(mx, my, mw, mh); ctx.save(); ctx.beginPath(); ctx.rect(mx, my, mw, mh); ctx.clip();
        const g = ctx.createLinearGradient(mx, my, mx + mw, my + mh); g.addColorStop(0, "rgba(255,255,255,0.10)"); g.addColorStop(1, "rgba(255,255,255,0.02)"); ctx.fillStyle = g; ctx.fillRect(mx, my, mw, mh);
        const fog = P(35.2, 39.0) * (1 - P(70.4, 72.4)); const clear = P(70.6, 73.0);
        ctx.globalAlpha = Math.min(1, mirrorA) * (0.55 + 0.45 * clear) * (1 - 0.8 * fog); C.person(ctx, 790, FLY - 10, H * 0.85, { fill: "#09090c", rim: C.mixc(COLD, WARMC, clear), rimA: 0.4 + 0.5 * clear });
        if (clear > 0.01) C.glow(ctx, 790, FLY - 170, 160, WARMC, 0.35 * clear);
        if (fog > 0.01) { ctx.globalAlpha = Math.min(1, mirrorA) * fog; for (let i = 0; i < 10; i++) C.glow(ctx, mx + 40 + (i * 53) % 240, my + 60 + (i * 97) % 500, 120, [180, 185, 200], 0.25); }
        ctx.restore(); ctx.strokeStyle = "#0c0b0d"; ctx.lineWidth = 16; ctx.strokeRect(mx, my, mw, mh); ctx.restore(); }
      // floor
      { const g = ctx.createLinearGradient(0, FLY, 0, 1900); g.addColorStop(0, C.rgba(C.mixc([24, 22, 26], [44, 32, 26], warm), 1)); g.addColorStop(1, "#000"); ctx.fillStyle = g; ctx.fillRect(-200, FLY, 1480, 900); }
      // the friend who stays
      if (friendA > 0.01) { const fx = keys([[52.6,1000],[54.4,880],[67,880],[69.5,640]], T); ctx.save(); ctx.globalAlpha = friendA; C.person(ctx, fx, FLY, 350, { fill: "#060507", rim: WARMC, rimA: 0.75, walk: (T > 52.6 && T < 54.4) || (T > 67 && T < 69.5) ? T * 6 : null }); ctx.restore(); C.glow(ctx, fx, FLY - 180, 220, WARMC, 0.25 * friendA); }
      // you
      { const rim = C.mixc(COLD, WARMC, warm); const inner = P(56.0, 57.5);
        C.person(ctx, X, FLY, H, { fill: "#040405", rim, rimA: 0.8 });
        if (inner > 0.01) C.glow(ctx, X, FLY - H * 0.6, 120 + 160 * warm, WARMC, 0.45 * inner);
        // blurred face when masks are off at night
        const blur = P(31.7, 33.5) * (1 - P(56, 57.5)); if (blur > 0.01) { for (let i = 0; i < 5; i++) C.glow(ctx, HX + Math.sin(T + i) * 6, HY + Math.cos(T * 1.3 + i) * 6, 40, [120, 120, 140], 0.25 * blur); } }
      // masks on the face, by moment
      const onFace = [["work", 5.76, 10.6], ["family", 10.78, 16.9], ["friends", 17.09, 24.0], ["social", 24.3, 29.65]];
      onFace.forEach(([k, a0, a1]) => { const a = P(a0, a0 + 0.4) * (1 - P(a1, a1 + 0.3)); mask(HX, HY, MR, k, a, 0); });
      // the pile on the table / floor after removing them at night
      const pile = [["social", 29.9], ["friends", 30.4], ["family", 30.9], ["work", 31.4]];
      const shield = P(43.8, 45.0) * (1 - P(49.6, 51.0)); const cage = P(45.5, 48.5);
      const fall = P(65.4, 67.0);
      pile.forEach(([k, t0], i) => { const off = P(t0, t0 + 0.7); if (off <= 0.01) return; const removed = i === 0 ? P(56.0, 56.7) : 0;
        let x = C.lerp(HX, 180 + i * 70, off), y = C.lerp(HY, FLY - 30, off) - Math.sin(off * 3.14) * 80; let rot = off * (i % 2 ? 1.2 : -1.2);
        // orbit as shields, then close into a wall
        if (shield > 0.01 || cage > 0.01) { const q = T * 0.8 + i * 1.57, rr = C.lerp(220, 120, cage); const ox = HX + Math.cos(q) * rr, oy = FLY - H * 0.55 + Math.sin(q) * rr * 0.7; const k2 = Math.max(shield, Math.min(1, cage)) * (1 - P(51.0, 52.0)); x = C.lerp(x, ox, k2); y = C.lerp(y, oy, k2); rot = C.lerp(rot, 0, k2); }
        const gone = Math.max(fall, i === 0 ? P(56.0, 57.0) : 0); y += fall * 40; const a = 1 - Math.max(gone * 0.9, P(51.0, 52.0) * 0.4);
        mask(x, y, MR * (1 + 0.8 * cage * (1 - P(51, 52))), k, a * (1 - P(70, 72)), rot); });
      // cage lines
      if (cage > 0.01) { const a = cage * (1 - P(51.0, 52.0)); ctx.save(); ctx.strokeStyle = "rgba(220,220,230," + 0.25 * a + ")"; ctx.lineWidth = 3; ctx.beginPath(); ctx.ellipse(HX, FLY - H * 0.55, 140, 220, 0, 0, 6.283); ctx.stroke(); ctx.restore(); }
      if (phoneA > 0.01) { ctx.save(); ctx.globalAlpha = phoneA; ctx.strokeStyle = "rgba(230,232,245,0.85)"; ctx.lineWidth = 8; ctx.beginPath(); ctx.roundRect(HX - 230, HY - 160, 460, 900, 50); ctx.stroke(); ctx.fillStyle = "rgba(230,232,245,0.85)"; ctx.beginPath(); ctx.roundRect(HX - 50, HY - 140, 100, 18, 9); ctx.fill();
        for (let i = 0; i < 12; i++) { const ph = ((T - 24) * 0.5 + i / 12) % 1; const x = HX + 120 + Math.sin(i * 2.1 + T) * 40, y = HY + 600 - ph * 700; const s = 14 * Math.sin(ph * 3.14); ctx.fillStyle = "rgba(255,90,110," + Math.sin(ph * 3.14) + ")"; ctx.beginPath(); ctx.moveTo(x, y + s); ctx.bezierCurveTo(x - s * 1.6, y - s * 0.2, x - s * 0.8, y - s * 1.4, x, y - s * 0.5); ctx.bezierCurveTo(x + s * 0.8, y - s * 1.4, x + s * 1.6, y - s * 0.2, x, y + s); ctx.fill(); }
        ctx.restore(); }
      // words to the one you trust
      const bub = (s, x, y, a) => { if (a <= 0.01) return; ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "rgba(255,244,228,0.95)"; ctx.font = "600 34px Inter, sans-serif"; const w = ctx.measureText(s).width + 50; ctx.beginPath(); ctx.roundRect(x - w / 2, y - 38, w, 76, 30); ctx.fill(); ctx.beginPath(); ctx.moveTo(x - 30, y + 36); ctx.lineTo(x - 50, y + 64); ctx.lineTo(x, y + 36); ctx.fill(); ctx.restore(); txt(s, x, y, 34, "#2a1a14", a, { w: 600 }); };
      bub("No estoy bien.", 560, 560, P(59.4, 59.9) * (1 - P(62.0, 62.4)));
      bub("Esto me gusta.", 560, 560, P(62.4, 62.9) * (1 - P(64.9, 65.4)));
      ctx.restore();
      C.dust(ctx, T, { n: 50, alpha: 0.2 + 0.3 * warm, seed: 4, warm: warm, speed: 0.2 });
"""

TT = "opacity: 0, y: 24, filter: \"blur(14px)\" }, { opacity: 1, y: 0, filter: \"blur(0px)\", duration: 0.8, ease: \"power3.out\" }"
titles = [
    ("CADA MAÑANA", "kick", 0.2, 3.0, ""),
    ("la más brillante<br>de todas.", "title", 25.6, 28.0, "font-size:100px; color:#ffe2bf"),
    ("se te olvidó<br>quién eras tú.", "title", 39.08, 41.6, "font-size:100px"),
    ("Ni siquiera tú.", "title", 49.77, 51.4, "font-size:110px"),
    ("Quítate una.", "title", 56.03, 59.2, "font-size:118px; color:#ffe2bf"),
    ("Te conocieron<br>a ti.", "title", 73.36, None, "font-size:120px; color:#fff1de"),
]
markup, js = "", '    gsap.set(".hbt", { opacity: 0 });\n'
for i, (txt, cls, a, b, sty) in enumerate(titles):
    top = 300 if cls == "kick" else 230
    markup += f'    <div id="mk-t{i}" class="{cls} hbt" style="top:{top}px; {sty}">{txt}</div>\n'
    if cls == "kick":
        js += f'    tl.fromTo("#mk-t{i}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {a});\n'
    else:
        js += f'    tl.fromTo("#mk-t{i}", {{ {TT}, {a});\n'
    if b: js += f'    tl.to("#mk-t{i}", {{ opacity: 0, filter: "blur(10px)", duration: 0.4 }}, {b});\n'

S.append(("mk", 0.0, 78.0, 0.0, markup, STAGE, js))

CUES = [(0.00,4.28,"Cada mañana… antes de salir… te pones una máscara."),(5.76,6.88,"Una para el trabajo."),(7.64,10.20,"Siempre capaz. Siempre de buen humor."),
(10.78,12.11,"Otra para tu familia."),(12.64,16.52,"La del que no tiene problemas. La del que no preocupa a nadie."),(17.09,18.40,"Otra para tus amigos."),
(18.79,21.19,"La del gracioso. La del fuerte."),(21.68,23.25,"La del que siempre está bien."),(24.30,27.38,"Y en redes… la más brillante de todas."),
(28.34,31.25,"Y por la noche… cuando por fin te las quitas…"),(31.74,34.12,"a veces ya no reconoces la cara que queda."),
(35.24,38.52,"Porque pasaste tanto tiempo siendo lo que otros esperaban…"),(39.08,40.70,"que se te olvidó quién eras tú."),
(41.77,44.95,"Las máscaras no son malas. A veces nos protegen."),(45.48,49.20,"Pero si nunca te las quitas… nadie va a conocerte de verdad."),
(49.77,50.48,"Ni siquiera tú."),(51.57,55.49,"Prueba algo. Con una sola persona. Alguien de confianza."),(56.03,58.97,"Quítate una. Di cómo te sientes en realidad."),
(59.44,61.94,"Di «no estoy bien» si no lo estás."),(62.33,64.86,"Di «esto me gusta» aunque parezca raro."),(65.36,66.51,"Vas a descubrir algo."),
(66.95,70.47,"Que las personas correctas… no se van cuando ven tu cara real."),(71.02,74.68,"Se quedan. Porque por fin… te conocieron a ti.")]
