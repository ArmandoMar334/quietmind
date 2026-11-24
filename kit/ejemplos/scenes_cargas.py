S = []

STAGE = """
      const T = t;
      const keys = (K, T) => { if (T <= K[0][0]) return K[0][1]; for (let i = 1; i < K.length; i++) if (T <= K[i][0]) { const k = (T - K[i-1][0]) / (K[i][0] - K[i-1][0]); return C.lerp(K[i-1][1], K[i][1], C.ease(k)); } return K[K.length-1][1]; };
      const P = (a, b) => C.ease(C.prog(T, a, b));
      const FLY = 1100, BACKY = 1040, COLD = [170, 188, 225], WARMC = [255, 196, 136];
      const txt = (s, x, y, size, col, a, o) => { if (a <= 0.01) return; o = o || {}; ctx.save(); ctx.globalAlpha = a; ctx.font = (o.italic ? "italic " : "") + (o.w || "") + " " + size + "px " + (o.italic ? "'EB Garamond', Georgia, serif" : "Inter, sans-serif"); ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.shadowColor = "rgba(0,0,0,0.9)"; ctx.shadowBlur = 16; ctx.fillStyle = col; ctx.fillText(s, x, y); ctx.restore(); };
      // ---------- time & state ----------
      const tw = T < 19.2 ? T : (T < 48.9 ? 19.2 : 19.2 + (T - 48.9));
      const frozen = T > 19.2 && T < 48.9;
      const scan = C.clamp((T - 19.2) / 1.8);
      const lineup = P(19.6, 21.0) * (1 - P(44.5, 46.5));
      const allBurden = P(36.5, 38.0) * (1 - P(44.5, 46.5));
      const warm = Math.max(P(61.5, 66) * 0.6, P(72.6, 80));
      const PX = 470;
      // camera
      const CZ = keys([[0,1.04],[19,1.0],[34.5,1.0],[36.5,0.84],[44,0.84],[47,1.0],[50,1.0],[51.5,1.55],[60,1.6],[61.5,1.0],[84,1.06]], T);
      const CXc = keys([[0,540],[50,540],[51.5,PX],[60,PX],[61.5,540]], T);
      const CYc = keys([[0,900],[50,900],[51.5,930],[60,930],[61.5,900]], T);
      // sky + city
      { const g = ctx.createLinearGradient(0, 0, 0, 1920); g.addColorStop(0, C.rgba(C.mixc([5, 6, 14], [26, 18, 30], warm), 1)); g.addColorStop(0.55, C.rgba(C.mixc([16, 18, 34], [80, 46, 44], warm), 1)); g.addColorStop(1, "#000"); ctx.fillStyle = g; ctx.fillRect(0, 0, 1080, 1920); }
      ctx.save(); ctx.translate(540, 900); ctx.scale(CZ, CZ); ctx.translate(-CXc, -CYc);
      { const r = C.rng(7); for (let i = 0; i < 26; i++) { const x = -400 + i * 76, h = 220 + r() * 480, w = 70 + r() * 50; ctx.fillStyle = C.rgba(C.mixc([10, 11, 20], [24, 16, 20], warm), 1); ctx.fillRect(x, BACKY - 40 - h, w, h + 40);
          for (let k = 0; k < 24; k++) { if (r() > 0.32) continue; const wx = x + 10 + (k % 3) * (w / 3.4), wy = BACKY - 30 - h + 20 + Math.floor(k / 3) * 46; if (wy > BACKY - 60) continue; ctx.fillStyle = r() > 0.5 ? "rgba(255,206,140,0.55)" : "rgba(170,190,240,0.35)"; ctx.fillRect(wx, wy, 12, 16); } } }
      // street
      { const g = ctx.createLinearGradient(0, BACKY - 20, 0, 1900); g.addColorStop(0, C.rgba(C.mixc([20, 20, 28], [44, 32, 28], warm), 1)); g.addColorStop(1, "#000"); ctx.fillStyle = g; ctx.fillRect(-600, BACKY - 20, 2400, 1400);
        ctx.fillStyle = "rgba(200,200,220,0.12)"; ctx.fillRect(-600, FLY + 2, 2400, 3);
        for (let i = 0; i < 6; i++) { const x = -260 + i * 340; ctx.fillStyle = "#070709"; ctx.fillRect(x - 4, BACKY - 380, 8, 380); ctx.fillRect(x - 4, BACKY - 380, 40, 6); C.glow(ctx, x + 34, BACKY - 368, 220, [255, 196, 130], 0.32); C.cone(ctx, x + 34, BACKY - 368, BACKY, 30, 260, 0.12, 1); ctx.fillStyle = "rgba(255,230,180,0.95)"; ctx.beginPath(); ctx.arc(x + 34, BACKY - 368, 7, 0, 6.283); ctx.fill(); } }
      // ---------- burdens ----------
      const burden = (x, y, k, a, s) => { if (a <= 0.01) return; s = s || 1; ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.scale(s, s); C.glow(ctx, 0, 0, 80, [120, 135, 180], 0.3);
        ctx.strokeStyle = "rgba(200,212,245,0.9)"; ctx.fillStyle = "rgba(200,212,245,0.9)"; ctx.lineWidth = 4;
        if (k === "cloud") { ctx.fillStyle = "rgba(60,66,84,0.95)"; ctx.beginPath(); ctx.arc(-18, 0, 20, 0, 6.283); ctx.arc(10, -8, 24, 0, 6.283); ctx.arc(28, 4, 16, 0, 6.283); ctx.fill(); ctx.strokeStyle = "rgba(170,190,240,0.8)"; ctx.lineWidth = 2; for (let i = 0; i < 4; i++) { const yy = 26 + ((T * 70 + i * 13) % 30); ctx.beginPath(); ctx.moveTo(-18 + i * 14, yy); ctx.lineTo(-21 + i * 14, yy + 8); ctx.stroke(); } }
        if (k === "letter") { ctx.beginPath(); ctx.rect(-34, -22, 68, 44); ctx.moveTo(-34, -22); ctx.lineTo(0, 4); ctx.lineTo(34, -22); ctx.stroke(); ctx.strokeStyle = "rgba(240,120,110,0.9)"; ctx.beginPath(); ctx.moveTo(10, -22); ctx.lineTo(2, -4); ctx.lineTo(14, 4); ctx.lineTo(6, 22); ctx.stroke(); }
        if (k === "moon") { ctx.beginPath(); ctx.arc(0, 0, 26, 0.6, 5.7); ctx.arc(12, -6, 20, 5.0, 1.3, true); ctx.closePath(); ctx.fill(); ctx.font = "700 20px Inter"; ctx.fillText("z", 30, -26); ctx.fillText("z", 42, -42); }
        if (k === "cross") { ctx.fillStyle = "rgba(240,120,110,0.9)"; ctx.fillRect(-8, -28, 16, 56); ctx.fillRect(-28, -8, 56, 16); }
        if (k === "heart") { ctx.beginPath(); ctx.moveTo(0, 24); ctx.bezierCurveTo(-40, -4, -20, -34, 0, -12); ctx.bezierCurveTo(20, -34, 40, -4, 0, 24); ctx.stroke(); ctx.beginPath(); ctx.moveTo(0, -12); ctx.lineTo(-6, 0); ctx.lineTo(6, 8); ctx.lineTo(0, 22); ctx.stroke(); }
        if (k === "debt") { ctx.font = "800 46px Inter"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("$", 0, 0); ctx.beginPath(); ctx.arc(0, 0, 30, 0, 6.283); ctx.stroke(); }
        if (k === "fear") { ctx.fillStyle = "rgba(20,20,28,0.95)"; ctx.beginPath(); ctx.ellipse(0, 0, 40, 28, 0, 0, 6.283); ctx.fill(); ctx.fillStyle = "rgba(255,240,240,0.9)"; ctx.beginPath(); ctx.ellipse(-12, -2, 6, 4, 0, 0, 6.283); ctx.ellipse(12, -2, 6, 4, 0, 0, 6.283); ctx.fill(); }
        if (k === "alone") { ctx.beginPath(); ctx.arc(0, -10, 8, 0, 6.283); ctx.fill(); ctx.fillRect(-6, 0, 12, 22); ctx.beginPath(); ctx.arc(0, 4, 34, 0, 6.283); ctx.setLineDash([4, 6]); ctx.stroke(); ctx.setLineDash([]); }
        ctx.restore(); };
      // ---------- passers-by ----------
      const W = []; { const r = C.rng(42); for (let i = 0; i < 14; i++) { const back = i < 7; W.push({ back, x0: r() * 1500, dir: r() > 0.5 ? 1 : -1, sp: 40 + r() * 50, h: back ? 170 + r() * 30 : 260 + r() * 40, kind: ["heart", "debt", "fear", "alone"][i % 4], t0: [37.18, 38.45, 39.59, 40.68][i % 4] }); } }
      const wX = (w) => (((w.x0 + w.dir * w.sp * tw) % 1500) + 1500) % 1500 - 210;
      // kindness spreading: warm lights on passers-by
      const kind = (i) => P(64.2 + i * 0.7, 64.8 + i * 0.7);
      W.forEach((w, i) => { if (!w.back) return; const x = wX(w); if (Math.abs(x - PX) < 60 && lineup > 0.3) return; const dim = 1 - 0.55 * lineup;
        ctx.save(); ctx.globalAlpha = dim; C.person(ctx, x, BACKY, w.h, { fill: "#050507", rim: C.mixc(COLD, WARMC, kind(i)), rimA: 0.35 + 0.3 * kind(i), walk: !frozen ? tw * 6 + i : null }); ctx.restore();
        burden(x, BACKY - w.h - 60, w.kind, allBurden * P(w.t0, w.t0 + 0.4) * (1 - 0.5 * kind(i)), 0.8);
        if (kind(i) > 0.01) C.glow(ctx, x, BACKY - w.h * 0.6, 40, WARMC, 0.6 * kind(i)); });
      // the three you judged: passing moments, then the lineup
      const passes = [[6.31, 1, 520, 1.25, "letter"], [8.84, -1, 300, 1.0, "moon"], [11.53, 1, 260, 1.0, "cross"]];
      passes.forEach(([t0, dir, sp, hk, k], i) => { const k2 = C.clamp((T - t0) / (1180 / sp + 0.3)); if (k2 <= 0 || k2 >= 1 || T > 19.6) return; const x = dir > 0 ? -120 + k2 * 1320 : 1200 - k2 * 1320;
        const hl = P(t0, t0 + 0.3); C.person(ctx, x, FLY, 300, { fill: "#040406", rim: C.mixc([150, 160, 190], [240, 110, 100], 0.75 * hl), rimA: 0.95, walk: T * 9 }); });
      const L = [[200, "letter", 23.64], [720, "moon", 28.44], [930, "cross", 32.51]];
      L.forEach(([x, k, t0], i) => { const a = lineup * C.clamp((scan * 1080 - x) / 120 + 1); if (a <= 0.01) return;
        ctx.save(); ctx.globalAlpha = a; C.person(ctx, x, FLY, 300, { fill: "#040406", rim: C.mixc(COLD, WARMC, kind(10 + i)), rimA: 0.75 }); ctx.restore();
        burden(x, FLY - 380, k, a * P(t0, t0 + 0.5), 1.2); });
      // front passers-by
      W.forEach((w, i) => { if (w.back) return; const x = wX(w); if (lineup > 0.3) return; const dim = 1 - lineup;
        ctx.save(); ctx.globalAlpha = dim; C.person(ctx, x, FLY, w.h, { fill: "#040406", rim: C.mixc(COLD, WARMC, kind(i)), rimA: 0.45 + 0.3 * kind(i), walk: !frozen ? tw * 6 + i : null }); ctx.restore();
        burden(x, FLY - w.h - 70, w.kind, allBurden * P(w.t0, w.t0 + 0.4) * dim, 1); if (kind(i) > 0.01) C.glow(ctx, x, FLY - w.h * 0.6, 50, WARMC, 0.6 * kind(i) * dim); });
      // scan line
      if (scan > 0 && scan < 1) { const x = -100 + scan * 1300; ctx.save(); ctx.globalCompositeOperation = "lighter"; const g = ctx.createLinearGradient(x - 120, 0, x + 20, 0); g.addColorStop(0, "rgba(140,170,255,0)"); g.addColorStop(1, "rgba(160,190,255,0.35)"); ctx.fillStyle = g; ctx.fillRect(x - 120, 200, 140, 1100); ctx.restore(); }
      // you
      { const rim = C.mixc(COLD, WARMC, warm); const flinch = P(12.0, 12.4) * (1 - P(13.2, 13.8));
        ctx.save(); ctx.translate(PX, FLY); ctx.rotate(-0.12 * flinch); C.person(ctx, 0, 0, 310, { fill: "#040405", rim, rimA: 0.85 }); ctx.restore();
        // the smile and the crack inside
        const z = P(50.4, 51.6) * (1 - P(60.4, 61.5));
        if (z > 0.01) { const s = 310 / 180; ctx.save(); ctx.globalAlpha = z; ctx.strokeStyle = "rgba(255,240,225,0.9)"; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(PX, FLY - 168 * s, 9, 0.2, Math.PI - 0.2); ctx.stroke();
            ctx.strokeStyle = "rgba(160,190,255,0.85)"; ctx.lineWidth = 3; ctx.shadowColor = "rgba(140,170,255,0.9)"; ctx.shadowBlur = 12; const c = P(51.7, 54.8); ctx.beginPath(); ctx.moveTo(PX - 4, FLY - 140 * s); const pts = [[8, -126], [-6, -112], [6, -98], [-4, -86]]; pts.forEach(([dx, dy], j) => { if (j / pts.length <= c) ctx.lineTo(PX + dx, FLY + dy * s); }); ctx.stroke(); ctx.restore(); }
        // what would have helped: a warm hand reaching you
        const help = P(57.6, 58.6) * (1 - P(60.4, 61.5)); if (help > 0.01) C.glow(ctx, PX, FLY - 200, 180, WARMC, 0.4 * help);
        // be that person: ripples of warmth
        [62.67, 64.22, 66.30, 68.48].forEach((r0) => { const k = (T - r0) / 3.2; if (k <= 0 || k >= 1) return; ctx.save(); ctx.strokeStyle = C.rgba(WARMC, 0.6 * (1 - k)); ctx.lineWidth = 3; ctx.beginPath(); ctx.ellipse(PX, FLY - 150, 60 + k * 700, 30 + k * 260, 0, 0, 6.283); ctx.stroke(); ctx.restore(); });
        if (warm > 0.01) C.glow(ctx, PX, FLY - 160, 300, WARMC, 0.22 * warm);
        const bub = P(68.48, 69.0) * (1 - P(72.4, 73.0)); if (bub > 0.01) { ctx.save(); ctx.globalAlpha = bub; ctx.fillStyle = "rgba(255,244,228,0.95)"; ctx.beginPath(); ctx.roundRect(PX + 40, FLY - 470, 260, 76, 28); ctx.fill(); ctx.beginPath(); ctx.moveTo(PX + 70, FLY - 398); ctx.lineTo(PX + 50, FLY - 370); ctx.lineTo(PX + 100, FLY - 398); ctx.fill(); ctx.restore(); txt("¿Cómo estás?", PX + 170, FLY - 432, 34, "#2a1a14", bub, { w: 600 }); } }
      ctx.restore();
      // screen-space thoughts
      txt("«Qué grosero.»", 760, 820, 54, "#c3c9d8", P(15.72, 16.0) * (1 - P(18.2, 18.9)), { italic: true });
      txt("«Qué mala actitud.»", 300, 940, 54, "#c3c9d8", P(17.05, 17.3) * (1 - P(18.2, 18.9)), { italic: true });
      [["una pérdida", 37.18], ["una deuda", 38.45], ["un miedo", 39.59], ["una soledad", 40.68]].forEach(([s, t0], i) => txt(s, 540, 560 + i * 0, 44, "rgba(215,222,245,1)", P(t0, t0 + 0.3) * (1 - P(t0 + 1.1, t0 + 1.3 + (i === 3 ? 1.5 : 0))), { italic: true }));
      C.dust(ctx, T, { n: 50, alpha: 0.2 + 0.3 * warm, seed: 4, warm: warm, speed: 0.2 });
"""

TT = "opacity: 0, y: 24, filter: \"blur(14px)\" }, { opacity: 1, y: 0, filter: \"blur(0px)\", duration: 0.8, ease: \"power3.out\" }"
titles = [
    ("Pero no sabes qué<br>traían por dentro.", "title", 19.21, 22.9, "font-size:88px"),
    ("y fingimos que<br>todo está bien.", "title", 47.11, 49.9, "font-size:96px"),
    ("Sé esa persona.", "title", 62.67, 66.0, "font-size:110px; color:#ffe2bf"),
    ("Que hoy le pese<br>un poco menos.", "title", 76.81, None, "font-size:104px; color:#fff1de"),
]
markup, js = "", '    gsap.set(".hbt", { opacity: 0 });\n'
for i, (txt, cls, a, b, sty) in enumerate(titles):
    markup += f'    <div id="cg-t{i}" class="{cls} hbt" style="top:230px; {sty}">{txt}</div>\n'
    js += f'    tl.fromTo("#cg-t{i}", {{ {TT}, {a});\n'
    if b: js += f'    tl.to("#cg-t{i}", {{ opacity: 0, filter: "blur(10px)", duration: 0.4 }}, {b});\n'

S.append(("cg", 0.0, 84.0, 0.0, markup, STAGE, js))

CUES = [(0.00,4.59,"Hoy te cruzaste con muchas personas."),(6.31,7.75,"El que te atendió con prisa."),(8.84,10.41,"La que no te devolvió el saludo."),
(11.53,13.27,"El que te cerró el paso en la calle."),(13.98,15.31,"Y tal vez pensaste:"),(15.72,18.03,"«Qué grosero.» «Qué mala actitud.»"),
(19.21,21.20,"Pero no sabes qué traían por dentro."),(21.89,25.75,"Tal vez el de la prisa… acababa de recibir una mala noticia."),
(26.52,30.10,"Tal vez la que no saludó… no durmió en toda la noche."),(30.79,33.37,"Tal vez el de la calle… iba al hospital."),
(34.55,36.56,"Todos cargamos algo que no se ve."),(37.18,40.15,"Una pérdida. Una deuda. Un miedo."),(40.68,43.09,"Una soledad que no le contamos a nadie."),
(44.49,48.88,"Y aun así… salimos a la calle… y fingimos que todo está bien."),(50.05,51.18,"Tú también lo has hecho."),
(51.66,55.16,"Has sonreído en días en los que por dentro te estabas cayendo."),(55.76,60.38,"Y cómo te habría ayudado… que alguien te tratara con un poco más de paciencia."),
(61.51,63.78,"Así que hoy… sé esa persona."),(64.22,65.84,"Saluda aunque no te saluden."),(66.30,68.06,"Ten paciencia con quien está lento."),
(68.48,72.13,"Pregunta «¿cómo estás?»… y quédate a escuchar la respuesta."),(72.64,76.30,"No sabes cuánto puede pesar… lo que otro está cargando."),
(76.81,80.67,"Pero sí puedes hacer… que hoy le pese un poco menos.")]
