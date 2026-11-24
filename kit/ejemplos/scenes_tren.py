S = []

STAGE = """
      const T = t;
      const keys = (K, T) => { if (T <= K[0][0]) return K[0][1]; for (let i = 1; i < K.length; i++) if (T <= K[i][0]) { const k = (T - K[i-1][0]) / (K[i][0] - K[i-1][0]); return C.lerp(K[i-1][1], K[i][1], C.ease(k)); } return K[K.length-1][1]; };
      const P = (a, b) => C.ease(C.prog(T, a, b));
      const FLY = 1110, BENCH = 1045, COLD = [180, 196, 230], WARMC = [255, 196, 136];
      const txt = (s, x, y, size, col, a, o) => { if (a <= 0.01) return; o = o || {}; ctx.save(); ctx.globalAlpha = a; ctx.font = (o.italic ? "italic " : "") + (o.w || "") + " " + size + "px " + (o.italic ? "'EB Garamond', Georgia, serif" : "Inter, sans-serif"); ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.shadowColor = "rgba(0,0,0,0.9)"; ctx.shadowBlur = 16; ctx.fillStyle = col; ctx.fillText(s, x, y); ctx.restore(); };
      // ---------- motion ----------
      const STOPS = [[10.3, 19.6], [20.2, 31.9], [61.4, 65.2]];
      const speed = (tt) => { let v = tt > 37.6 && tt < 52.5 ? 620 : 320; STOPS.forEach(([a, b]) => { const k = Math.min(C.clamp((tt - a) / 0.9), C.clamp((b - tt) / 0.9)); v *= 1 - C.ease(k); }); return v; };
      const integ = (tt) => { let x = 0; for (let s = 0; s < tt; s += 0.05) x += speed(s) * 0.05; return x; };
      const X = integ(T);
      const stopX = STOPS.map(([a, b]) => integ((a + b) / 2));
      const dawn = P(64.5, 74);
      const biome = keys([[0,0],[40,0],[41.5,1],[43.8,1],[45.2,2],[47.5,2],[49,0]], T); // 0 fields, 1 snow, 2 city
      // ---------- landscape (screen space, scrolled) ----------
      const land = (ox, scale) => {
        const g = ctx.createLinearGradient(0, 520, 0, 900); g.addColorStop(0, C.rgba(C.mixc([8, 10, 22], [70, 60, 100], dawn), 1)); g.addColorStop(1, C.rgba(C.mixc(C.mixc([26, 30, 52], [70, 80, 100], biome === 1 ? 1 : 0), [255, 170, 110], dawn), 1));
        ctx.fillStyle = g; ctx.fillRect(0, 0, 1080, 1920);
        if (dawn > 0.01) C.sun(ctx, 760, C.lerp(900, 700, dawn), 50, dawn, null);
        { const r = C.rng(3); for (let i = 0; i < 60; i++) { const x = ((r() * 1400 - ox * 0.02) % 1400 + 1400) % 1400 - 160; ctx.fillStyle = "rgba(225,232,255," + 0.5 * (1 - dawn) * r() + ")"; ctx.beginPath(); ctx.arc(x, 540 + r() * 200, 0.6 + r() * 1.4, 0, 6.283); ctx.fill(); } }
        // far hills
        const hills = (par, base, amp, col, seed) => { ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(0, 1000); for (let x = 0; x <= 1080; x += 20) { const w = x + ox * par; ctx.lineTo(x, base - amp * (0.5 + 0.5 * Math.sin(w * 0.004 + seed)) - amp * 0.4 * Math.sin(w * 0.011 + seed * 2)); } ctx.lineTo(1080, 1000); ctx.fill(); };
        const snow = biome > 0.5 && biome < 1.5 ? 1 : 0;
        hills(0.1, 800, 90, C.rgba(C.mixc(C.mixc([16, 18, 30], [140, 150, 175], snow), [60, 40, 50], dawn), 1), 1);
        if (biome > 1.5) { const r = C.rng(9); for (let i = 0; i < 40; i++) { const x = ((i * 70 - ox * 0.35) % 2800 + 2800) % 2800 - 200, h = 60 + ((i * 37) % 9) * 22; ctx.fillStyle = "#0d0f18"; ctx.fillRect(x, 860 - h, 56, h); for (let k = 0; k < 6; k++) if ((i * 7 + k * 3) % 5 < 2) { ctx.fillStyle = "rgba(255,210,150,0.8)"; ctx.fillRect(x + 8 + (k % 2) * 24, 860 - h + 12 + Math.floor(k / 2) * 22, 10, 10); } } }
        hills(0.3, 860, 50, C.rgba(C.mixc(C.mixc([10, 11, 18], [90, 100, 125], snow), [40, 26, 30], dawn), 1), 4);
        if (snow) { const r = C.rng(5); for (let i = 0; i < 60; i++) { const x = (r() * 1080 + T * 40) % 1080, y = (r() * 400 + T * 90) % 400 + 520; ctx.fillStyle = "rgba(240,245,255,0.7)"; ctx.fillRect(x, y, 3, 3); } }
        // near poles
        for (let i = 0; i < 30; i++) { const x = ((i * 260 - ox) % 7800 + 7800) % 7800 - 100; if (x > -40 && x < 1120) { ctx.fillStyle = "#050507"; ctx.fillRect(x, 560, 10, 340); } }
        // stations
        stopX.forEach((sx, i) => { const x = sx + 540 - ox; if (x < -900 || x > 2000) return; ctx.fillStyle = "#0b0a0c"; ctx.fillRect(x - 700, 820, 1400, 80); ctx.fillStyle = "#0b0a0c"; ctx.fillRect(x - 700, 560, 1400, 26);
          for (let k = -2; k <= 2; k++) { const lx = x + k * 300; ctx.fillStyle = "#08080a"; ctx.fillRect(lx - 4, 586, 8, 240); C.glow(ctx, lx, 610, 160, [255, 200, 130], 0.55); ctx.fillStyle = "rgba(255,230,180,0.95)"; ctx.beginPath(); ctx.arc(lx, 610, 9, 0, 6.283); ctx.fill(); }
          ctx.fillStyle = "rgba(255,210,150,0.15)"; ctx.fillRect(x - 700, 818, 1400, 3); });
      };
      // ---------- people ----------
      const frontSit = (x, h, rim, rimA, a, light) => { if (a <= 0.01) return; const s = h / 180; ctx.save(); ctx.globalAlpha = a; ctx.translate(x, BENCH);
        const path = () => { ctx.beginPath(); ctx.arc(0, -150 * s, 17 * s, 0, 6.283); ctx.roundRect(-26 * s, -128 * s, 52 * s, 112 * s, [18 * s, 18 * s, 6 * s, 6 * s]); ctx.roundRect(-24 * s, -20 * s, 20 * s, (FLY - BENCH) + 20 * s, 6 * s); ctx.roundRect(4 * s, -20 * s, 20 * s, (FLY - BENCH) + 20 * s, 6 * s); ctx.roundRect(-34 * s, -116 * s, 12 * s, 84 * s, 6 * s); ctx.roundRect(22 * s, -116 * s, 12 * s, 84 * s, 6 * s); };
        ctx.save(); ctx.shadowColor = C.rgba(rim, rimA); ctx.shadowBlur = 20; ctx.fillStyle = C.rgba(rim, rimA); path(); ctx.fill(); ctx.restore(); ctx.fillStyle = "#050405"; ctx.save(); ctx.scale(0.965, 0.985); path(); ctx.fill(); ctx.restore();
        if (light > 0.01) { C.glow(ctx, 0, -95 * s, 40 * s, WARMC, 0.7 * light); ctx.fillStyle = "rgba(255,236,206," + light + ")"; ctx.beginPath(); ctx.arc(0, -95 * s, 4 * s, 0, 6.283); ctx.fill(); }
        ctx.restore(); };
      const walker = (x, h, rim, a, walking) => { if (a <= 0.01) return; ctx.save(); ctx.globalAlpha = a; C.person(ctx, x, FLY, h, { fill: "#050405", rim, rimA: 0.75, walk: walking ? T * 7 : null }); ctx.restore(); };
      // passenger: seat x, board time (null = from start), leave time, mode
      const PASS = [
        { x: 400, h: 230, on: null, off: null, mode: "stay", rim: WARMC },          // parent
        { x: 680, h: 236, on: null, off: 29.84, mode: "fade", rim: WARMC },          // parent who fades
        { x: 810, h: 205, on: 13.66, off: 24.62, mode: "wave", rim: [255, 214, 170] }, // school friend
        { x: 270, h: 212, on: 15.28, off: 26.41, mode: "walk", rim: [255, 180, 170] }, // first love
        { x: 940, h: 222, on: 16.62, off: null, mode: "stay", rim: [255, 220, 170] },  // the one who taught you
        { x: 680, h: 214, on: 62.4, off: null, mode: "stay", rim: [255, 214, 170] },  // the new one
      ];
      const DOOR = 1130;
      // ---------- camera ----------
      const ext = 1 - P(3.0, 4.2);
      const CZ = keys([[0,1],[4,1.0],[32.8,1.0],[33.6,1.3],[36.6,1.3],[37.6,1.0],[53,1.0],[54,1.12],[57.4,1.12],[58.4,1.0],[76,1.05]], T);
      const CXc = keys([[0,540],[32.8,540],[33.6,700],[36.6,700],[37.6,540]], T);
      // ===== exterior opening =====
      if (ext > 0.01) { ctx.save(); ctx.globalAlpha = ext; land(X * 0.5, 1);
        ctx.fillStyle = "#0a0a0d"; ctx.fillRect(0, 1060, 1080, 900); ctx.fillStyle = "rgba(180,170,170,0.25)"; ctx.fillRect(0, 1060, 1080, 3);
        const cx = 380 - T * 200; for (let c = 0; c < 4; c++) { const x0 = cx + c * 560; ctx.fillStyle = "#08080b"; ctx.beginPath(); ctx.roundRect(x0, 860, 540, 190, 14); ctx.fill();
          for (let w = 0; w < 5; w++) { const wx = x0 + 30 + w * 100; ctx.fillStyle = "rgba(255,206,140,0.85)"; ctx.fillRect(wx, 890, 70, 60); C.glow(ctx, wx + 35, 920, 70, WARMC, 0.35); ctx.fillStyle = "#08080b"; ctx.beginPath(); ctx.arc(wx + 35, 930, 10, 0, 6.283); ctx.fill(); ctx.fillRect(wx + 24, 938, 22, 20); }
          ctx.fillStyle = "#050507"; [0.2, 0.8].forEach((f) => { ctx.beginPath(); ctx.arc(x0 + 540 * f, 1052, 22, 0, 6.283); ctx.fill(); }); }
        for (let i = 0; i < 10; i++) { const k = ((T * 0.6 + i * 0.1) % 1); C.glow(ctx, cx + 40 + k * 200, 840 - k * 300, 60 + k * 90, [190, 190, 200], 0.18 * (1 - k)); }
        ctx.restore(); }
      // ===== interior =====
      if (ext < 0.99) {
        ctx.save(); ctx.globalAlpha = 1 - ext; ctx.translate(540, 870); ctx.scale(CZ, CZ); ctx.translate(-CXc, -900);
        // windows with the world passing
        ctx.save(); ctx.beginPath(); [[50, 330], [390, 300], [730, 300]].forEach(([x, w]) => ctx.rect(x, 560, w, 320)); ctx.clip(); land(X, 1); ctx.restore();
        // car wall
        ctx.save(); ctx.fillStyle = C.rgba(C.mixc([28, 20, 18], [60, 40, 32], dawn), 1); ctx.beginPath(); ctx.rect(-400, 300, 1880, 1400); [[50, 330], [390, 300], [730, 300]].forEach(([x, w]) => { ctx.rect(x + w, 560, -w, 320); }); ctx.fill("evenodd"); ctx.restore();
        ctx.strokeStyle = "#140e0c"; ctx.lineWidth = 12; [[50, 330], [390, 300], [730, 300]].forEach(([x, w]) => ctx.strokeRect(x, 560, w, 320));
        // ceiling lamps
        [200, 540, 880].forEach((x) => { C.glow(ctx, x, 470, 260, [255, 200, 140], 0.35 + 0.1 * Math.sin(T * 3 + x)); ctx.fillStyle = "rgba(255,226,180,0.9)"; ctx.fillRect(x - 40, 452, 80, 10); });
        ctx.fillStyle = "#0c0807"; ctx.fillRect(-400, 300, 1880, 140);
        // bench and floor
        ctx.fillStyle = "#1c1210"; ctx.fillRect(40, BENCH - 6, 1000, 26); ctx.fillStyle = "#120c0a"; ctx.fillRect(40, BENCH + 20, 1000, FLY - BENCH - 20);
        const fg = ctx.createLinearGradient(0, FLY, 0, 1900); fg.addColorStop(0, "#1a1210"); fg.addColorStop(1, "#000"); ctx.fillStyle = fg; ctx.fillRect(-400, FLY, 1880, 900);
        // empty seats keep a faint glow of who sat there
        PASS.forEach((p, i) => { if (!p.off || T < p.off + 1) return; const g = (1 - P(48.9, 50.9)) * 0.8; if (g > 0.01 && !(i === 1 && T > 62.4)) C.glow(ctx, p.x, BENCH - 90, 90, p.rim, 0.35 * g * (0.8 + 0.2 * Math.sin(T * 2 + i))); });
        // passengers
        PASS.forEach((p, i) => {
          const on = p.on == null ? -10 : p.on; const walkIn = P(on, on + 1.6); const sat = T > on + 1.6;
          if (T < on) return;
          const light = P(on + 1.6, on + 2.2) * (p.off ? 1 - P(p.off, p.off + 0.4) : 1);
          if (!sat) { walker(C.lerp(DOOR, p.x, walkIn), p.h * 1.3, p.rim, P(on, on + 0.3), true); return; }
          if (p.off && T > p.off) {
            if (p.mode === "fade") { frontSit(p.x, p.h, p.rim, 0.6, 1 - P(p.off, p.off + 1.8), 0); return; }
            const k = P(p.off + 0.4, p.off + 3.2);
            if (p.mode === "wave") { const up = P(p.off, p.off + 0.4); const wx = C.lerp(p.x, DOOR, k); walker(wx, p.h * 1.3, p.rim, 1 - P(p.off + 2.8, p.off + 3.2), k > 0.02);
              const wv = P(p.off + 0.1, p.off + 0.5) * (1 - P(p.off + 1.2, p.off + 1.6)); if (wv > 0.01) { const s = p.h * 1.3 / 180; ctx.save(); ctx.translate(wx - 25 * s, FLY - 132 * s); ctx.rotate(-Math.PI * 0.82 + Math.sin(T * 9) * 0.25); ctx.strokeStyle = "#050405"; ctx.lineCap = "round"; ctx.lineWidth = 11 * s; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, -62 * s); ctx.stroke(); ctx.restore(); } return; }
            if (p.mode === "walk") { const k2 = P(p.off, p.off + 2.6); walker(C.lerp(p.x, DOOR, k2), p.h * 1.3, p.rim, 1 - P(p.off + 2.2, p.off + 2.6), true); return; }
          }
          frontSit(p.x, p.h, p.rim, 0.55 + 0.3 * (i === 0 ? P(59.6, 60.6) : 0), 1, light);
          if (i === 0) { const care = P(59.6, 60.6); if (care > 0.01) C.glow(ctx, p.x, BENCH - 100, 200, WARMC, 0.3 * care); }
        });
        // you: from a child to who you are now
        { const grow = P(10.6, 19.0); const h = C.lerp(120, 232, grow); const rim = C.mixc(COLD, WARMC, Math.max(P(48.9, 52), dawn));
          const look = P(53.4, 54.2) * (1 - P(56.8, 57.6));
          frontSit(540, h, rim, 0.85, 1, P(49.7, 51.4));
          if (look > 0.01) { const s = h / 180; ctx.save(); ctx.fillStyle = "#050405"; ctx.beginPath(); ctx.arc(540 - 7 * look * s, BENCH - 150 * s, 17 * s, 0, 6.283); ctx.fill(); ctx.restore(); } }
        // what they gave you floats to you
        { const fl = C.clamp((T - 48.9) / 2.6); if (fl > 0 && fl < 1) { PASS.slice(1, 4).forEach((p, i) => { const e = C.ease(C.clamp(fl * 1.2 - i * 0.1)); const x = C.lerp(p.x, 540, e), y = C.lerp(BENCH - 90, BENCH - 120, e) - Math.sin(e * 3.14) * 140; C.glow(ctx, x, y, 50, p.rim, 0.7 * (1 - e * 0.5)); ctx.fillStyle = "rgba(255,238,212,0.95)"; ctx.beginPath(); ctx.arc(x, y, 5, 0, 6.283); ctx.fill(); }); } }
        ctx.restore();
        C.dust(ctx, T, { n: 50, alpha: 0.3, seed: 4, warm: 0.7, speed: 0.2 });
      }
"""

TT = "opacity: 0, y: 24, filter: \"blur(14px)\" }, { opacity: 1, y: 0, filter: \"blur(0px)\", duration: 0.8, ease: \"power3.out\" }"
titles = [
    ("Tu vida es<br>un tren.", "title", 0.4, 3.0, "font-size:120px"),
    ("alguien sube.", "title", 12.37, 15.0, "font-size:110px; color:#ffe2bf"),
    ("alguien baja.", "title", 23.34, 25.9, "font-size:110px"),
    ("Solo un tramo.", "title", 46.11, 48.6, "font-size:110px; color:#ffe2bf"),
    ("Que valga la pena<br>el viaje.", "title", 69.65, None, "font-size:104px; color:#fff1de"),
]
markup, js = "", '    gsap.set(".hbt", { opacity: 0 });\n'
for i, (txt, cls, a, b, sty) in enumerate(titles):
    markup += f'    <div id="tr-t{i}" class="{cls} hbt" style="top:200px; {sty}">{txt}</div>\n'
    js += f'    tl.fromTo("#tr-t{i}", {{ {TT}, {a});\n'
    if b: js += f'    tl.to("#tr-t{i}", {{ opacity: 0, filter: "blur(10px)", duration: 0.4 }}, {b});\n'

S.append(("tr", 0.0, 76.0, 0.0, markup, STAGE, js))

CUES = [(0.00,2.15,"Imagina que tu vida es un tren."),(3.45,6.18,"Cuando naciste, ya había gente a bordo."),(6.95,9.93,"Tu familia. Las primeras personas que te cuidaron."),
(10.56,13.05,"Y en cada estación… alguien sube."),(13.66,16.19,"Un amigo de la escuela. Un primer amor."),(16.62,19.24,"Alguien que te enseñó algo que nunca olvidaste."),
(20.33,24.02,"Pero también… en cada estación… alguien baja."),(24.62,28.06,"A veces se despiden. A veces se van sin decir nada."),
(28.65,31.46,"Y a veces… ni te das cuenta de que ya no están."),(33.00,36.50,"Duele ver un asiento vacío. Duele no saber por qué."),
(37.63,39.28,"Pero el tren no se detiene."),(39.77,42.94,"Y no todos estaban destinados a llegar contigo hasta el final."),
(43.43,46.57,"Algunos solo tenían que acompañarte… un tramo."),(47.19,48.30,"Ese tramo importó."),(48.88,52.28,"Lo que te dieron… se quedó contigo. Aunque ellos no."),
(53.37,57.25,"No te quedes mirando por la ventana… hacia la estación que ya pasó."),(57.79,61.21,"Agradece a quien bajó. Cuida a quien sigue a tu lado."),
(61.68,64.61,"Y deja espacio… para quien todavía no ha subido."),(65.69,69.06,"Porque un día… tú también vas a ser el recuerdo de alguien."),
(69.65,72.59,"Asegúrate… de que valga la pena el viaje.")]
