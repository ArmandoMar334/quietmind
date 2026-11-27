S = []
TOTAL_S = 95.0

STAGE = """
      const T = t;
      const keys = (K, T) => { if (T <= K[0][0]) return K[0][1]; for (let i = 1; i < K.length; i++) if (T <= K[i][0]) { const k = (T - K[i-1][0]) / (K[i][0] - K[i-1][0]); return C.lerp(K[i-1][1], K[i][1], C.ease(k)); } return K[K.length-1][1]; };
      const P = (a, b) => C.ease(C.prog(T, a, b));
      const HZ = 880, GY = 1060, W = 1080, H = 1920;
      const COLD = [150, 172, 212], WARMC = [255, 192, 124];
      const dawn = P(72, 90);
      const actB = P(40.8, 42.4), actA = 1 - actB;
      // ---------- world ----------
      C.sky(ctx, { hz: HZ, warm: dawn, glow: 0.15 + 0.65 * dawn });
      if (dawn > 0.01) { const sy = C.lerp(HZ + 60, HZ - 90, P(76, 95)); C.sun(ctx, 760, sy, 42, dawn, HZ); C.rays(ctx, 760, sy, T, 0.5 * P(80, 90), 11, 1300); }
      C.clouds(ctx, T, { seed: 8, n: 12, y0: 120, y1: HZ - 220, alpha: 0.16 * (1 - 0.3 * dawn), warm: dawn, drift: 6 });
      // ground plane
      { const g = ctx.createLinearGradient(0, HZ, 0, H); g.addColorStop(0, C.rgba(C.mixc([20, 22, 30], [80, 56, 46], dawn), 1)); g.addColorStop(0.25, C.rgba(C.mixc([8, 9, 13], [30, 22, 22], dawn), 1)); g.addColorStop(1, "#010102"); ctx.fillStyle = g; ctx.fillRect(0, HZ, W, H - HZ); }
      C.floor(ctx, T, { hz: HZ, alpha: 0.07 + 0.05 * dawn, speed: T > 89.4 ? 0.06 : 0.0, color: C.mixc([170, 185, 215], WARMC, dawn), vx: 760 });
      C.fog(ctx, T, { seed: 5, n: 8, y0: HZ - 40, y1: HZ + 120, alpha: 0.18 * (1 - 0.5 * dawn), color: C.mixc([70, 78, 96], [200, 140, 110], dawn), drift: 4 });
      const print = (x, y, s, a, col) => { if (a <= 0.01) return; ctx.save(); ctx.globalCompositeOperation = "lighter"; C.glow(ctx, x, y, 22 * s, col, 0.5 * a); ctx.fillStyle = C.rgba(col, 0.85 * a); ctx.beginPath(); ctx.ellipse(x, y, 7 * s, 3 * s, 0, 0, 6.283); ctx.fill(); ctx.restore(); };
      // child cycle: rise, walk, fall, rest
      const PER = 2.4, T0 = 3.4;
      const child = (T) => { if (T < T0) return { x: 230, lie: 1, walk: null, k: -1 }; const c = Math.floor((T - T0) / PER), f = ((T - T0) % PER) / PER; const x0 = 230 + c * 30;
        let lie = 0, x = x0, walk = null; if (f < 0.3) lie = 1 - C.ease(f / 0.3); else if (f < 0.72) { const q = (f - 0.3) / 0.42; x = x0 + q * 30; walk = q * 6.283 * 1.5; } else if (f < 0.8) { lie = C.ease((f - 0.72) / 0.08); x = x0 + 30; } else { lie = 1; x = x0 + 30; } return { x, lie, walk, k: c, f }; };

      // ================= ACT A/B: the child learning =================
      if (actA > 0.01) { ctx.save(); ctx.globalAlpha = actA;
        const ch = child(T), inner = P(35.8, 40.3);
        // hundreds of other attempts: ghost children across the plain
        const many = P(11.1, 12.5) * (1 - P(16.0, 17.6));
        if (many > 0.01) { const r = C.rng(41); for (let i = 0; i < 46; i++) { const z = 0.25 + r() * 0.75, gx = 40 + r() * 1000, gy = C.lerp(HZ + 20, GY - 10, z), ph = r() * 10, sp = 0.8 + r() * 0.5; const f = (((T * sp + ph) / PER) % 1); const lie = f < 0.3 ? 1 - C.ease(f / 0.3) : f < 0.72 ? 0 : f < 0.8 ? C.ease((f - 0.72) / 0.08) : 1;
            if (Math.abs(gx - 540) < 120 && z > 0.8) continue; ctx.save(); ctx.globalAlpha = actA * many * (0.25 + 0.45 * z); C.person(ctx, gx, gy, 100 * z, { fill: "#07070a", rim: COLD, rimA: 0.45, lean: lie * 1.45, walk: f > 0.3 && f < 0.72 ? f * 30 : null }); ctx.restore(); } }
        // follow-cam on the child
        const Z = keys([[0,2.1],[11,1.9],[12.5,1.45],[16,1.45],[17.2,1.9],[35,1.9],[40.5,2.2]], T), camX = 230 + Math.max(0, T - T0) / PER * 30 + 25;
        ctx.save(); ctx.translate(540, GY); ctx.scale(Z, Z); ctx.translate(-camX, -GY);
        for (let c = 0; c <= ch.k; c++) { const x0 = 230 + c * 30, done = c < ch.k ? 1 : C.clamp((ch.f - 0.4) / 0.3); if (done > 0) print(x0 + 12, GY + 4, 0.6, 0.5 * done * (0.5 + 0.5 * inner), C.mixc([200, 210, 235], WARMC, inner)); if (done > 0.6) print(x0 + 27, GY + 2, 0.6, 0.5 * (0.5 + 0.5 * inner), C.mixc([200, 210, 235], WARMC, inner)); }
        // the lonely spotlight on "tal vez caminar no es para ti"
        const spot = P(16.0, 17.0) * (1 - P(25.5, 28));
        if (spot > 0.01) C.cone(ctx, ch.x + 15, 0, GY + 20, 80, 320, 0.35 * spot, 0);
        // the child
        if (inner > 0.01) C.glow(ctx, ch.x, GY - 50, 60 + 200 * inner, WARMC, 0.35 * inner);
        C.person(ctx, ch.x, GY, 100, { fill: "#08080b", rim: C.mixc(COLD, WARMC, inner), rimA: 0.75, lean: ch.lie * 1.45, walk: ch.walk });
        if (inner > 0.01 && ch.lie < 0.5) { const s = 100 / 180; ctx.save(); ctx.translate(ch.x, GY); ctx.rotate(ch.lie * 1.45); C.glow(ctx, 0, -104 * s, 40, [255, 230, 180], 0.9 * inner); ctx.restore(); }
        ctx.restore();
        ctx.restore(); }

      // ================= ACT C/D/E: the adult who forgot, and the child who remains =================
      if (actB > 0.01) { ctx.save(); ctx.globalAlpha = actB;
        const AX = keys([[0,640],[89.3,640],[95,730]], T);
        const sink = keys([[0,1],[67.9,1],[71.2,0.6],[78.5,0.6],[80.5,0.3],[88.66,0.3],[89.3,0]], T);
        const warm = Math.max(P(54.5, 57), dawn);
        // the trail you walked as a child, from the horizon to here
        { const a = P(42.2, 44.5); for (let i = 0; i < 26; i++) { const q = i / 25, z = Math.pow(q, 1.6); const px = C.lerp(250, AX - 120, q) + (i % 2 ? 8 : -8) * (0.3 + z), py = C.lerp(HZ + 8, GY + 4, z); print(px, py, 0.35 + 0.7 * z, a * (0.25 + 0.5 * q) * (0.5 + 0.5 * warm), C.mixc([200, 210, 235], WARMC, warm)); } }
        // the adult (kneeling = sunk below the ground line)
        const rimA = C.mixc(COLD, WARMC, Math.max(P(67.9, 72), dawn));
        ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, GY + 2); ctx.clip();
        C.person(ctx, AX, GY + 105 * sink, 300, { fill: "#08080b", rim: rimA, rimA: 0.7, lean: 0.18 * sink, walk: T > 89.6 ? T * 5 : null });
        ctx.restore();
        ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillRect(AX - 80, GY, 160, 8);
        // the child of light beside you
        const ca = P(54.5, 56.2);
        if (ca > 0.01) { const cx = keys([[0,440],[89.3,440],[95,545]], T); const f = T < 63.3 ? (((T - 54.5) / PER) % 1) : 0.5; let lie = f < 0.3 ? 1 - C.ease(f / 0.3) : f < 0.72 ? 0 : f < 0.8 ? C.ease((f - 0.72) / 0.08) : 1; if (T > 59.5) lie = Math.min(lie, 1 - P(59.5, 60.3));
          ctx.save(); ctx.globalAlpha = actB * ca; C.glow(ctx, cx, GY - 75, 230, WARMC, 0.4); C.person(ctx, cx, GY, 150, { fill: C.rgba([255, 214, 160], 0.55), rim: [255, 214, 160], rimA: 0.9, lean: lie * 1.45, walk: T > 89.6 ? T * 6 : null }); ctx.restore();
          // laughter after falling: small sparks
          const laugh = P(62.1, 62.6) * (1 - P(64.5, 65.5)); if (laugh > 0.01) { const r = C.rng(9); for (let i = 0; i < 12; i++) { const ang = r() * 6.283, d = 30 + ((T * 40 + r() * 60) % 70); C.glow(ctx, cx + Math.cos(ang) * d, GY - 70 + Math.sin(ang) * d * 0.7, 10, [255, 225, 170], 0.7 * laugh); } } }
        // new footprints ahead when you rise and walk
        { const w = C.prog(T, 89.6, 95); for (let i = 0; i < 6; i++) { const q = i / 6; if (q > w) break; print(640 + 24 + i * 16, GY + 4, 1.6, 0.7, WARMC); print(440 + 16 + i * 18, GY + 4, 1.1, 0.7, WARMC); } }
        ctx.restore(); }
      C.dust(ctx, T, { n: 44, alpha: 0.12 + 0.3 * dawn, seed: 4, warm: dawn, speed: 0.2 });
"""

TT = "opacity: 0, y: 24, filter: \"blur(14px)\" }, { opacity: 1, y: 0, filter: \"blur(0px)\", duration: 0.8, ease: \"power3.out\" }"
titles = [
    ("Cientos de veces.", 11.15, 15.4, "font-size:104px"),
    ("¿En qué momento<br>se te olvidó?", 41.5, 46.6, "font-size:96px"),
    ("Esa persona<br>sigue ahí.", 54.54, 59.2, "font-size:104px; color:#ffe2bf"),
    ("Una terquedad<br>hermosa.", 81.6, 85.6, "font-size:100px; color:#ffe2bf"),
    ("Todavía sabes<br>cómo.", 90.05, None, "font-size:108px; color:#fff1de"),
]
markup, js = "", '    gsap.set(".hbt", { opacity: 0 });\n'
for i, (txt, a, b, sty) in enumerate(titles):
    markup += f'    <div id="cm-t{i}" class="title hbt" style="top:240px; {sty}">{txt}</div>\n'
    js += f'    tl.fromTo("#cm-t{i}", {{ {TT}, {a});\n'
    if b: js += f'    tl.to("#cm-t{i}", {{ opacity: 0, filter: "blur(10px)", duration: 0.4 }}, {b});\n'
markup += '    <div id="cm-k" class="kick hbt" style="top:180px;">LEVÁNTATE</div>\n'
js += '    tl.fromTo("#cm-k", { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "none" }, 88.66);\n'
js += f'    tl.to(S("#cm-wrap"), {{ opacity: 0, duration: 0.9, ease: "none" }}, {TOTAL_S - 1.0});\n'

S.append(("cm", 0.0, TOTAL_S, 0.0, markup, STAGE, js))

CUES = [
(0.00,2.31,"Hubo un tiempo en que no sabías caminar."),
(3.46,4.40,"Te levantabas,"),(4.79,5.77,"dabas un paso…"),(6.42,7.37,"y te caías."),
(8.31,8.94,"Una vez."),(9.66,10.62,"Diez veces."),(11.15,12.57,"Cientos de veces."),
(13.62,15.61,"Y nadie, nunca, te dijo:"),(16.07,17.64,"“tal vez caminar no es para ti”."),
(18.68,20.18,"Nadie te dijo que lo dejaras."),(20.90,22.24,"Que ya era suficiente."),(23.07,24.82,"Que lo intentaras el próximo año."),
(25.88,27.55,"Y tú tampoco lo pensaste."),(28.51,30.08,"No te daba vergüenza caerte."),(30.80,32.44,"No contabas los intentos."),(33.20,34.74,"No te comparabas con nadie."),
(35.76,37.02,"Solo te levantabas…"),(37.55,40.30,"porque algo dentro de ti sabía que podías."),
(41.50,43.14,"¿En qué momento se te olvidó eso?"),(44.23,46.87,"¿Cuándo empezaste a creer que caer es fracasar?"),
(47.99,50.50,"¿Cuándo empezaste a rendirte al tercer intento…"),(50.60,53.37,"si antes no te rendías ni al intento cien?"),
(54.54,55.82,"Esa persona sigue ahí."),(56.78,59.37,"La que se agarraba de lo que fuera para ponerse de pie."),(60.38,62.12,"La que se reía después de caer."),
(63.32,64.68,"No perdiste esa fuerza."),(65.36,66.86,"Solo dejaste de usarla."),
(67.92,71.19,"Así que la próxima vez que caigas, recuerda quién eres."),
(72.22,74.59,"Eres alguien que ya aprendió lo más difícil…"),(75.38,76.30,"sin saber hablar,"),(76.83,77.92,"sin entender nada,"),(78.56,80.49,"sin que nadie le prometiera nada."),
(81.60,85.02,"Solo con piernas temblorosas y una terquedad hermosa."),
(86.38,87.57,"Ya lo hiciste una vez."),(88.66,89.30,"Levántate."),(90.05,91.32,"Todavía sabes cómo."),
]
