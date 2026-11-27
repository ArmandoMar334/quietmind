S = []
TOTAL_S = 91.0

STAGE = """
      const T = t;
      const keys = (K, T) => { if (T <= K[0][0]) return K[0][1]; for (let i = 1; i < K.length; i++) if (T <= K[i][0]) { const k = (T - K[i-1][0]) / (K[i][0] - K[i-1][0]); return C.lerp(K[i-1][1], K[i][1], C.ease(k)); } return K[K.length-1][1]; };
      const P = (a, b) => C.ease(C.prog(T, a, b));
      const HZ = 900, W = 1080, H = 1920;
      const COLD = [150, 172, 210], WARMC = [255, 192, 124], LAMP = [255, 226, 168];
      // ---------- global state ----------
      const storm = keys([[0,0.15],[15.6,0.2],[16.4,1],[24,1],[26,0.5],[50,0.5],[52.4,0.85],[68,0.85],[72.5,0.15],[79,0]], T);
      const dawn = P(69.3, 79);
      const inner = P(37.3, 42.2);
      const pulse = P(65.4, 66.4) * (1 - P(68.1, 70.5));
      const lh = (1 - P(34.2, 35.6));
      const actB = P(23.9, 25.4), actA = 1 - actB;
      let flash = 0, boltI = -1;
      [16.0, 18.9, 21.9, 52.3, 54.4].forEach((f0, i) => { const d = T - f0; if (d >= 0 && d < 0.7) { const v = Math.exp(-d * 8) * (d < 0.06 || (d > 0.13 && d < 0.22) ? 1 : 0.55); if (v > flash) { flash = v; boltI = i; } } });
      flash *= (1 - dawn);
      // ---------- sky ----------
      C.sky(ctx, { hz: HZ, warm: dawn, glow: 0.12 + 0.7 * dawn });
      ctx.fillStyle = "rgba(0,0,0," + (0.35 * storm) + ")"; ctx.fillRect(0, 0, W, HZ);
      if (dawn > 0.01) { const sy = C.lerp(HZ + 50, HZ - 120, P(71, 90)); C.sun(ctx, 540, sy, 46, dawn, HZ); C.rays(ctx, 540, sy, T, 0.55 * P(75, 84), 11, 1300); }
      C.clouds(ctx, T, { seed: 3, n: 16, y0: 60, y1: HZ - 160, alpha: (0.12 + 0.3 * storm) * (1 - 0.5 * dawn) + 0.45 * flash, warm: dawn, drift: 8 + 30 * storm });
      // lightning bolt
      if (flash > 0.35 && boltI >= 0) { const r = C.rng(31 + boltI * 17); let x = 180 + r() * 720, y = 40; ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.strokeStyle = C.rgba([220, 228, 255], flash); ctx.lineWidth = 4; ctx.shadowColor = "rgba(190,205,255,1)"; ctx.shadowBlur = 30; ctx.beginPath(); ctx.moveTo(x, y); while (y < HZ - 40) { x += (r() - 0.5) * 90; y += 40 + r() * 60; ctx.lineTo(x, Math.min(y, HZ - 40)); } ctx.stroke(); ctx.restore(); }
      // ---------- sea (screen space) ----------
      { const g = ctx.createLinearGradient(0, HZ, 0, H); g.addColorStop(0, C.rgba(C.mixc([14, 18, 28], [90, 60, 52], dawn), 1)); g.addColorStop(0.3, C.rgba(C.mixc([5, 6, 10], [34, 24, 26], dawn), 1)); g.addColorStop(1, "#010102"); ctx.fillStyle = g; ctx.fillRect(0, HZ, W, H - HZ); }
      // light sources reflected on the water: [screenX, alpha, color]
      const refl = [];
      const CZ = keys([[0,1.1],[24.6,1.1],[48,1.3],[51.6,1.3],[56.5,0.8],[69,0.8],[91,0.92]], T);
      const BX = 430, BY = 1030;
      const fgX = 540 + (BX - 540) * CZ;
      if (dawn > 0.01) refl.push([540, 0.9 * dawn, [255, 200, 140]]);
      if (actB > 0.01 && inner > 0.01) refl.push([fgX, 0.8 * inner * actB * (1 + 0.4 * pulse) * (1 - 0.6 * dawn), WARMC]);
      if (actA > 0.01) refl.push([540, 0.5 * actA, LAMP]);
      if (actB > 0.01 && lh > 0.01) refl.push([880, 0.3 * actB * lh * (1 - dawn), LAMP]);
      { const N = 58, amp0 = (0.5 + storm * 1.5) * (1 - dawn * 0.55);
        ctx.save(); ctx.lineWidth = 2;
        for (let i = 0; i < N; i++) { const z = i / N, y = HZ + 4 + (H - HZ) * Math.pow(z, 1.9); const amp = (1.2 + 20 * z) * amp0, f = 0.012 / (0.25 + z), sp = 1.2 + storm * 1.8;
          ctx.strokeStyle = C.rgba(C.mixc(COLD, WARMC, dawn), (0.05 + 0.12 * (1 - z)) * (1 + 1.6 * flash));
          ctx.beginPath(); for (let x = -20; x <= W + 20; x += 24) { const yy = y + amp * Math.sin(x * f + T * sp + i * 1.9) + amp * 0.4 * Math.sin(x * f * 2.3 - T * sp * 0.7 + i); if (x === -20) ctx.moveTo(x, yy); else ctx.lineTo(x, yy); } ctx.stroke();
          const r = C.rng(i * 13 + 7);
          for (const [lx, la, lc] of refl) { const w = 18 + 260 * z; for (let k = 0; k < 2; k++) { const ox = Math.sin(i * 1.7 + T * 2.1 + k * 3) * w * 0.35 + (r() - 0.5) * w * 0.3; const ll = w * (0.25 + 0.4 * r()); const a = la * 0.55 * (0.4 + 0.6 * Math.abs(Math.sin(T * 3 + i + k))) * (1 - z * 0.6); ctx.strokeStyle = C.rgba(lc, a); ctx.lineWidth = 2 + 3 * z; ctx.beginPath(); ctx.moveTo(lx + ox - ll / 2, y + 2); ctx.lineTo(lx + ox + ll / 2, y + 2); ctx.stroke(); } }
        }
        ctx.restore(); }
      // ---------- helpers ----------
      const beam = (lx, ly, ang, len, spread, a) => { if (a <= 0.01) return; const dx = Math.cos(ang) * len, face = Math.sin(ang);
        ctx.save(); ctx.globalCompositeOperation = "lighter";
        if (Math.abs(dx) > 8) { const g = ctx.createLinearGradient(lx, ly, lx + dx, ly); g.addColorStop(0, C.rgba(LAMP, 0.42 * a)); g.addColorStop(1, C.rgba(LAMP, 0)); ctx.fillStyle = g; const s = spread * (0.55 + 0.45 * Math.abs(face));
          for (const k of [1, 0.6]) { ctx.beginPath(); ctx.moveTo(lx, ly - 6); ctx.lineTo(lx + dx, ly - s * k); ctx.lineTo(lx + dx, ly + s * k * 0.8); ctx.lineTo(lx, ly + 6); ctx.closePath(); ctx.fill(); } }
        ctx.restore();
        const fl = Math.pow(Math.max(0, face), 6); if (fl > 0.01) C.glow(ctx, lx, ly, len * 0.35 * fl + 20, LAMP, 0.7 * fl * a); };
      const lighthouse = (x, base, h, on, ang, beamLen, rim) => {
        const bw = h * 0.25, tw = h * 0.15, top = base - h;
        // rock
        ctx.fillStyle = "#050608"; ctx.beginPath(); ctx.moveTo(x - h * 0.55, base + h * 0.12); ctx.lineTo(x - h * 0.36, base - h * 0.02); ctx.lineTo(x - h * 0.16, base - h * 0.05); ctx.lineTo(x + h * 0.12, base - h * 0.04); ctx.lineTo(x + h * 0.33, base); ctx.lineTo(x + h * 0.6, base + h * 0.12); ctx.closePath(); ctx.fill();
        // tower
        ctx.save(); ctx.shadowColor = C.rgba(rim, 0.5); ctx.shadowBlur = h * 0.04; ctx.fillStyle = "#0b0c10"; ctx.beginPath(); ctx.moveTo(x - bw / 2, base - h * 0.03); ctx.lineTo(x - tw / 2, top + h * 0.12); ctx.lineTo(x + tw / 2, top + h * 0.12); ctx.lineTo(x + bw / 2, base - h * 0.03); ctx.closePath(); ctx.fill(); ctx.restore();
        ctx.fillStyle = "#14151b"; for (const q of [0.3, 0.62]) { const y0 = base - h * q, w0 = C.lerp(bw, tw, (q - 0.03) / 0.85); ctx.fillRect(x - w0 / 2, y0 - h * 0.06, w0, h * 0.06); }
        // windows
        if (on > 0.01) { ctx.fillStyle = C.rgba(LAMP, 0.55 * on); for (const q of [0.45, 0.75]) ctx.fillRect(x - h * 0.012, base - h * q, h * 0.024, h * 0.04); }
        // gallery, lantern, dome
        ctx.fillStyle = "#0b0c10"; ctx.fillRect(x - tw * 0.8, top + h * 0.1, tw * 1.6, h * 0.025);
        ctx.fillStyle = C.rgba(C.mixc([30, 32, 40], LAMP, on), 1); ctx.fillRect(x - tw * 0.42, top + h * 0.025, tw * 0.84, h * 0.078);
        ctx.fillStyle = "#0b0c10"; for (const k of [-0.42, -0.14, 0.14, 0.42]) ctx.fillRect(x + tw * k - 2, top + h * 0.025, 4, h * 0.078);
        ctx.beginPath(); ctx.arc(x, top + h * 0.028, tw * 0.48, Math.PI, 0); ctx.fill(); ctx.fillRect(x - 2, top - tw * 0.6, 4, tw * 0.2);
        const ly = top + h * 0.064;
        if (on > 0.01) { C.glow(ctx, x, ly, h * 0.5, LAMP, 0.55 * on); beam(x, ly, ang, beamLen, h * 0.11, on); }
      };
      const ship = (x, y, s, a) => { if (a <= 0.01) return; ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = "#06070a"; ctx.beginPath(); ctx.moveTo(-60, -10); ctx.lineTo(60, -10); ctx.lineTo(44, 8); ctx.lineTo(-48, 8); ctx.closePath(); ctx.fill(); ctx.fillRect(-20, -34, 30, 24); ctx.fillRect(-3, -70, 4, 40); ctx.fillStyle = C.rgba(LAMP, 0.8); ctx.fillRect(-14, -26, 5, 5); ctx.fillRect(0, -26, 5, 5); ctx.restore(); };
      const boat = (x, y, s, tilt) => { ctx.save(); ctx.translate(x, y); ctx.rotate(tilt); ctx.scale(s, s); ctx.fillStyle = "#040406"; ctx.beginPath(); ctx.moveTo(-95, -18); ctx.quadraticCurveTo(0, -8, 95, -24); ctx.lineTo(70, 14); ctx.quadraticCurveTo(0, 22, -72, 14); ctx.closePath(); ctx.fill(); ctx.restore(); };

      // ================= ACT A: the lighthouse =================
      if (actA > 0.01) { ctx.save(); ctx.globalAlpha = actA;
        // ships passing on the horizon
        ship(C.lerp(-80, 470, C.prog(T, 3.6, 11.5)), HZ + 2, 0.55, P(3.6, 4.6) * (1 - P(10.6, 11.8)));
        ship(C.lerp(1160, 700, C.prog(T, 4.4, 12.5)), HZ + 4, 0.42, P(4.4, 5.4) * (1 - P(11.4, 12.6)));
        const AZ = keys([[0,1.12],[12.8,1.03],[15.5,1.08],[25,1.04]], T);
        ctx.save(); ctx.translate(540, 800); ctx.scale(AZ, AZ); ctx.translate(-540, -800);
        const on = 0.75 + 0.25 * P(13.27, 14.6);
        lighthouse(540, 1085, 560, on, T * 1.05 + 1.2, 1100 + 300 * P(13.27, 14.6), C.mixc(COLD, [200, 210, 255], flash));
        // spray on the rock
        if (storm > 0.25) { const r = C.rng(77); for (let i = 0; i < 9; i++) { const ph = (T * (0.55 + r() * 0.4) + r()) % 1; const sx = 540 + (r() - 0.5) * 520, sy = 1080 - Math.sin(ph * Math.PI) * (80 + r() * 170); C.soft(ctx, sx, sy, 70 + r() * 60, 40, [190, 200, 220], 0.22 * storm * Math.sin(ph * Math.PI)); } }
        ctx.restore(); ctx.restore(); }

      // ================= ACT B: the sea, you, and the one who is lost =================
      if (actB > 0.01) { ctx.save(); ctx.globalAlpha = actB;
        // far lighthouse and the fog that swallows its light
        lighthouse(880, HZ + 10, 150, lh * (1 - dawn), T * 1.05 + 1.2, 420, COLD);
        const fogA = P(33.4, 36.3) * (1 - P(69, 77));
        if (fogA > 0.01) C.fog(ctx, T, { seed: 9, n: 7, y0: HZ - 140, y1: HZ + 20, alpha: 0.5 * fogA, color: [44, 50, 62], drift: -6 });
        // the one lost in their own storm
        const lb = P(51.6, 53.6);
        if (lb > 0.01) { const k = P(57.3, 80), x = C.lerp(150, 330, k), y = HZ + C.lerp(26, 64, k), s = C.lerp(0.32, 0.55, k);
          const bob = Math.sin(T * 2.1 + 1) * (2 + 7 * storm) * s, tilt = Math.sin(T * 1.7) * 0.1 * (0.2 + storm);
          ctx.save(); ctx.globalAlpha = actB * lb; boat(x, y + bob, s, tilt);
          C.person(ctx, x - 4 * s, y + bob - 12 * s, 150 * s, { fill: "#060608", rim: C.mixc(COLD, WARMC, Math.max(P(60.4, 63) * 0.7, dawn)), rimA: 0.55, flip: T < 60.4 });
          ctx.restore();
          // the guiding path on the water between you and them
          const path = P(60.4, 62.6) * (1 - dawn * 0.8);
          if (path > 0.01) { const tx = 540 + (BX - 540) * CZ, ty = HZ + (BY - HZ) * CZ; ctx.save(); ctx.globalCompositeOperation = "lighter"; for (let j = 0; j < 26; j++) { const q = j / 26; if (q > path) break; const px = C.lerp(tx, x, q) + Math.sin(j * 2.1 + T * 2) * 10, py = C.lerp(ty + 10, y + 6, q); ctx.fillStyle = C.rgba(WARMC, 0.35 * (1 - q * 0.5)); ctx.fillRect(px - 10 * (1 - q * 0.7), py, 20 * (1 - q * 0.7), 2.5); } ctx.restore(); } }
        // you, in the boat (camera zooms around the horizon point)
        ctx.save(); ctx.translate(540, HZ); ctx.scale(CZ, CZ); ctx.translate(-540, -HZ);
        const bob = Math.sin(T * 1.4) * (3 + 10 * storm), tilt = Math.sin(T * 1.1) * 0.045 * (0.3 + storm);
        const look = (T > 26.6 && T < 29.0) || (T > 31.7 && T < 34.0);
        const glowR = (60 + 380 * inner) * (1 + 0.35 * pulse);
        if (inner > 0.01) C.glow(ctx, BX, BY + bob - 112, glowR, WARMC, (0.45 * inner + 0.25 * pulse) * (1 - 0.4 * dawn));
        boat(BX, BY + bob, 1.0, tilt);
        ctx.save(); ctx.translate(BX, BY + bob - 14); ctx.rotate(tilt);
        C.person(ctx, 0, 0, 180, { fill: "#08080b", rim: C.mixc(COLD, WARMC, Math.max(inner, dawn)), rimA: 0.6 + 0.3 * inner, flip: look });
        if (inner > 0.01) { C.glow(ctx, 0, -104, 70, [255, 230, 180], 0.9 * inner * (1 + 0.3 * pulse)); ctx.fillStyle = C.rgba([255, 240, 210], 0.9 * inner); ctx.beginPath(); ctx.arc(0, -104, 7 + 3 * pulse, 0, 6.283); ctx.fill(); }
        ctx.restore();
        ctx.restore();
        ctx.restore(); }

      // ---------- rain, flash, dust ----------
      if (storm > 0.05) { const r = C.rng(21); ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.lineWidth = 1.6;
        for (let i = 0; i < 240; i++) { const z = 0.3 + r() * 0.7, sp = 0.7 + r() * 0.6, bx = r(), by = r();
          const x = ((bx * 1240 - T * 260 * sp * z) % 1240 + 1240) % 1240 - 80, y = ((by * 2140 + T * 1750 * sp * z) % 2140) - 110;
          ctx.strokeStyle = C.rgba([190, 205, 230], 0.16 * storm * z * (1 + flash)); ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 16 * z, y - 70 * z); ctx.stroke(); }
        ctx.restore(); }
      if (flash > 0.01) { ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.fillStyle = C.rgba([170, 185, 230], 0.28 * flash); ctx.fillRect(0, 0, W, H); ctx.restore(); }
      C.dust(ctx, T, { n: 46, alpha: 0.12 + 0.3 * Math.max(inner * 0.5, dawn), seed: 4, warm: Math.max(inner * 0.6, dawn), speed: 0.2 });
"""

TT = "opacity: 0, y: 24, filter: \"blur(14px)\" }, { opacity: 1, y: 0, filter: \"blur(0px)\", duration: 0.8, ease: \"power3.out\" }"
titles = [
    ("Se mantiene<br>encendida.", 13.27, 17.6, "font-size:100px"),
    ("Siempre estuvo<br>adentro.", 40.56, 44.6, "font-size:100px; color:#ffe2bf"),
    ("Solo no<br>te apagues.", 49.10, 53.3, "font-size:110px; color:#ffe2bf"),
    ("Sigues brillando.", 65.43, 69.0, "font-size:100px; color:#ffe2bf"),
    ("Podías brillar<br>en la oscuridad.", 79.37, 83.0, "font-size:92px; color:#fff1de"),
    ("Alguien se guía<br>con tu luz.", 85.44, None, "font-size:100px; color:#fff1de"),
]
markup, js = "", '    gsap.set(".hbt", { opacity: 0 });\n'
for i, (txt, a, b, sty) in enumerate(titles):
    markup += f'    <div id="fr-t{i}" class="title hbt" style="top:240px; {sty}">{txt}</div>\n'
    js += f'    tl.fromTo("#fr-t{i}", {{ {TT}, {a});\n'
    if b: js += f'    tl.to("#fr-t{i}", {{ opacity: 0, filter: "blur(10px)", duration: 0.4 }}, {b});\n'
markup += '    <div id="fr-k" class="kick hbt" style="top:180px;">NO TE APAGUES</div>\n'
js += '    tl.fromTo("#fr-k", { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "none" }, 83.4);\n'
js += f'    tl.to(S("#fr-wrap"), {{ opacity: 0, duration: 0.9, ease: "none" }}, {TOTAL_S - 1.0});\n'

S.append(("fr", 0.0, TOTAL_S, 0.0, markup, STAGE, js))

CUES = [
(0.00,1.10,"En medio del mar,"),(1.55,3.62,"hay una torre que nunca se mueve."),
(4.59,5.76,"No persigue barcos."),(6.52,7.16,"No grita."),(8.20,9.91,"No le ruega a nadie que la mire."),
(11.08,12.31,"Solo hace una cosa:"),(13.27,14.65,"se mantiene encendida."),
(15.81,17.93,"Aunque la tormenta golpee sus paredes."),(18.80,20.90,"Aunque la noche dure más de lo normal."),(21.84,23.63,"Aunque nadie le dé las gracias."),
(24.72,28.40,"Tal vez llevas mucho tiempo esperando que alguien ilumine tu camino."),
(29.34,30.89,"Que alguien te diga a dónde ir…"),(31.68,33.18,"y que todo va a estar bien."),
(34.15,36.29,"Pero hay noches en que esa luz no llega."),
(37.28,39.85,"Y ahí descubres que la luz que buscabas afuera…"),(40.56,42.18,"siempre estuvo adentro."),
(43.24,44.83,"No tienes que salvar a todos."),(45.66,48.07,"No tienes que tener todas las respuestas."),
(49.10,50.56,"Solo no te apagues."),
(51.64,53.50,"Porque alguien, en algún lugar,"),(54.20,56.19,"está perdido en su propia tormenta."),
(57.33,59.45,"Y tal vez lo único que necesita…"),(60.40,62.16,"es ver que tú sigues de pie."),
(63.17,64.35,"Que sigues intentando."),(65.43,66.50,"Que sigues brillando,"),(67.14,68.11,"aunque sea poquito."),
(69.26,72.05,"Y cuando por fin amanezca, y el mar se calme,"),(72.63,73.82,"vas a mirar atrás…"),
(74.89,78.25,"y vas a entender que la tormenta nunca fue para apagarte."),
(79.37,82.27,"Era para mostrarte que podías brillar en la oscuridad."),
(83.40,84.45,"No te apagues."),(85.44,87.48,"Alguien se está guiando con tu luz."),
]
