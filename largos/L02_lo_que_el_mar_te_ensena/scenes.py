import json as _json
_T = _json.load(open('/home/claude/vL02/timing.json'))
_CH = _T['chapters']
TOTAL_S = _T['total']
LEAD = 1.0
S = []

PRE = """
      const D = window.DES, M = window.MAR, W = 1920, H = 1080;
      const T = t - __OFF__;
      const P = (a, b) => C.ease(C.prog(T, a, b));
      const K = (k) => D.keys(k, T), KC = (k) => D.kc(k, T);
"""

TT = 'opacity: 0, y: 20, filter: "blur(14px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.9, ease: "power3.out" }'

# ---------------------------------------------------------------- CH0 intro: night storm, a small rowboat in the swell
ST0 = """
      const HZ = 520;
      const calm = P(28.6, 34.0);
      const fl = M.flash(T, [2.2, 8.4, 13.2, 22.0]) * (1 - calm);
      D.sky(ctx, HZ, C.mixc([4, 6, 10], [8, 12, 26], calm), C.mixc([16, 20, 28], [24, 32, 56], calm), C.mixc([40, 48, 60], [70, 84, 120], calm));
      if (fl > 0.01) { ctx.save(); ctx.fillStyle = C.rgba([170, 185, 220], 0.35 * fl); ctx.fillRect(0, 0, W, HZ + 40); ctx.restore(); }
      C.clouds(ctx, T, { seed: 5, n: 16, y0: 40, y1: HZ - 60, alpha: 0.55 * (1 - 0.7 * calm), warm: 0, drift: 40 });
      D.stars(ctx, T, calm * 0.8, 7, 200, HZ - 80, 0);
      D.moon(ctx, 1560, 190, 30, calm);
      if (fl > 0.05) { const s = T < 5 ? 1 : T < 10 ? 2 : T < 15 ? 3 : 4; M.bolt(ctx, [1500, 470, 1650, 380][s - 1], 0, HZ - 20, 30 + s, fl); }
      // camera push toward the boat
      const z = K([[0, 1.06], [24, 1.18], [35.5, 1.26]]);
      ctx.save(); ctx.translate(960, 700); ctx.scale(z, z); ctx.translate(-960, -700);
      const storm = 1 - 0.75 * calm;
      const far = { base: HZ + 12, amps: [10 * storm, 5], freqs: [0.006, 0.017], speeds: [1.2, -2.0] };
      M.water(ctx, (x) => M.surf(x, T, far), { top: C.mixc([22, 28, 40], [30, 40, 70], calm), bot: [6, 8, 12], depth: 300, rim: [150, 170, 210], rimA: 0.15 + 0.3 * fl });
      if (calm > 0.01) M.glints(ctx, T, HZ + 10, 900, [210, 220, 245], 0.6 * calm, 7, 160, 1560, 500);
      const mid = { base: 660, amps: [40 * storm, 18 * storm, 6], freqs: [0.0028, 0.008, 0.02], speeds: [0.9, -1.4, 2.4], phases: [0.3, 1.1, 2.0] };
      M.water(ctx, (x) => M.surf(x, T, mid), { top: C.mixc([18, 24, 34], [22, 32, 58], calm), bot: [4, 5, 8], depth: 360, rim: [170, 190, 230], rimA: 0.22 + 0.4 * fl });
      // the boat rides the near swell
      const near = { base: 760, amps: [62 * storm, 22 * storm, 7], freqs: [0.0024, 0.0072, 0.019], speeds: [1.0, -1.6, 2.6], phases: [1.4, 0.2, 0.9] };
      const NY = (x) => M.surf(x, T, near);
      const bx = 960 + Math.sin(T * 0.3) * 20, by = NY(bx) - 8, rot = Math.atan2(NY(bx + 60) - NY(bx - 60), 120) * 0.9;
      const rim = C.mixc([170, 190, 235], [200, 215, 255], calm);
      ctx.save(); ctx.translate(bx, by); ctx.rotate(rot);
      const row = Math.sin(T * 2.0) * (1 - 0.6 * P(24, 28));
      // oar
      ctx.save(); ctx.strokeStyle = "#05060a"; ctx.lineWidth = 7; ctx.shadowColor = C.rgba(rim, 0.5); ctx.shadowBlur = 10;
      ctx.beginPath(); ctx.moveTo(10 + row * 20, -150); ctx.lineTo(-180 - row * 60, 50); ctx.stroke(); ctx.restore();
      C.person(ctx, 0, 46, 280, { fill: "#05060a", rim: rim, rimA: 0.55 + 0.35 * fl, lean: -0.15 + 0.22 * row });
      M.boat(ctx, 0, 0, 370, 0, "#05060a", rim, 0.5 + 0.3 * fl);
      ctx.restore();
      // spray at the bow
      if (storm > 0.4) { const r = C.rng(5); ctx.save(); ctx.globalCompositeOperation = "lighter"; for (let i = 0; i < 40; i++) { const ph = (T * (0.6 + r()) + r()) % 1; ctx.fillStyle = C.rgba([210, 220, 240], 0.4 * (1 - ph) * storm); ctx.beginPath(); ctx.arc(bx + 150 + r() * 80 + ph * 120, by - 20 - Math.sin(ph * 3.1) * 90, 2 + r() * 2, 0, 6.283); ctx.fill(); } ctx.restore(); }
      const front = { base: 860, amps: [44 * storm, 16 * storm, 6], freqs: [0.002, 0.0066, 0.017], speeds: [1.3, -1.1, 2.2], phases: [2.5, 1.7, 0.3] };
      M.water(ctx, (x) => M.surf(x, T, front), { top: C.mixc([14, 18, 26], [18, 26, 48], calm), bot: [1, 1, 3], depth: 260, rim: [180, 200, 240], rimA: 0.3 + 0.4 * fl });
      ctx.restore();
      M.rain(ctx, T, 0.9 * (1 - calm), { seed: 4, n: 300, ang: 0.3, speed: 1500 });
      C.fog(ctx, T, { seed: 6, n: 8, y0: HZ - 40, y1: HZ + 120, alpha: 0.2 * storm, color: [80, 90, 110], drift: 30 });
      C.dust(ctx, T, { n: 40, alpha: 0.12, seed: 3, warm: 0, speed: 0.3 });
"""

# ---------------------------------------------------------------- CH1 la marea: dusk beach, the tide goes out and comes back
ST1 = """
      const HZ = 500;
      const ys = K([[0, 845], [3.4, 845], [9.6, 600], [42.4, 600], [45.6, 842]]);
      D.sky(ctx, HZ, [18, 16, 38], [86, 56, 86], [236, 150, 110]);
      C.glow(ctx, 1520, HZ, 700, [255, 160, 110], 0.3);
      // big moon on the horizon (she pulls the tide)
      C.glow(ctx, 1520, HZ - 70, 260, [255, 214, 180], 0.35); ctx.save(); ctx.fillStyle = "rgba(255,226,200,0.92)"; ctx.beginPath(); ctx.arc(1520, HZ - 70, 64, 0, 6.283); ctx.fill(); ctx.restore();
      // sea
      { const g = ctx.createLinearGradient(0, HZ, 0, ys); g.addColorStop(0, "rgb(120,84,110)"); g.addColorStop(1, "rgb(30,26,48)"); ctx.fillStyle = g; ctx.fillRect(0, HZ, W, ys - HZ + 2); }
      M.glints(ctx, T, HZ + 4, ys, [255, 210, 180], 0.8, 13, 150, 1520, 700);
      // wet sand (mirror) between the water line and the high-tide mark, then dry sand
      { const g = ctx.createLinearGradient(0, ys, 0, H); g.addColorStop(0, "rgb(70,52,70)"); g.addColorStop(C.clamp((850 - ys) / (H - ys + 1)), "rgb(44,32,44)"); g.addColorStop(1, "rgb(12,9,12)"); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(0, H);
        for (let x = 0; x <= W; x += 20) ctx.lineTo(x, ys + Math.sin(x * 0.006 + T * 0.8) * 5); ctx.lineTo(W, H); ctx.closePath(); ctx.fill(); }
      if (ys < 830) { ctx.save(); ctx.globalCompositeOperation = "lighter"; for (let i = 0; i < 12; i++) { const y = ys + 10 + i * (850 - ys) / 12; ctx.fillStyle = C.rgba([255, 200, 170], 0.05 * (1 - i / 12)); ctx.fillRect(1520 - 200 + Math.sin(T + i) * 20, y, 400 - i * 20, 2); } ctx.restore(); }
      // foam at the water's edge
      { ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.strokeStyle = "rgba(255,230,215,0.35)"; ctx.lineWidth = 3; ctx.beginPath();
        for (let x = 0; x <= W; x += 16) { const y = ys + Math.sin(x * 0.006 + T * 0.8) * 5 + Math.sin(x * 0.03 + T * 2) * 2; if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); } ctx.stroke(); ctx.restore(); }
      // boats: floating at high tide, lying tilted on the sand at low tide
      [[620, 760, 300, 0.12, 1], [1180, 740, 260, -0.1, 2], [1390, 800, 230, 0.16, 3]].forEach(([x, y, L, tilt, k]) => {
        const fl = C.clamp((ys - y - 4) / 40), bob = Math.sin(T * 1.2 + k) * 4;
        const yy = y + (fl > 0 ? bob * fl : 0) + 10 * (1 - fl), rr = C.lerp(tilt, Math.sin(T * 0.9 + k) * 0.03, fl);
        M.boat(ctx, x, yy, L, rr, "#0c080c", [255, 190, 150], 0.4);
        if (fl < 0.99) { ctx.save(); ctx.fillStyle = C.rgba([0, 0, 0], 0.35 * (1 - fl)); ctx.beginPath(); ctx.ellipse(x, y + 46, L * 0.5, 10, 0, 0, 6.283); ctx.fill(); ctx.restore(); } });
      // the person walks in and stands looking at the sea
      const px = K([[0, 330], [6.6, 330], [12.0, 900], [45.6, 900]]), walking = T > 6.6 && T < 12.0;
      const pin = P(6.4, 7.4);
      if (pin > 0.01) { ctx.save(); ctx.globalAlpha = pin; D.prints(ctx, () => 866, px - 26, Math.max(330, px - 560), 0.7, 30, [0, 0, 0]);
        C.person(ctx, px, 870, 300, { fill: "#070507", rim: [255, 196, 160], rimA: 0.6, walk: walking ? T * 4 : null }); ctx.restore(); }
      // what leaves (lanterns drift out with the tide) and comes back
      for (let i = 0; i < 4; i++) { const t0 = 28.0 + i * 1.4;
        const out = P(t0, t0 + 9), back = P(42.2 + i * 0.3, 45.4);
        if (T < t0) continue; const q = out * (1 - back);
        const x = C.lerp(900 + (i - 1.5) * 70, 1000 + (i - 1.5) * 260, q), y = C.lerp(700, HZ + 30, Math.pow(q, 0.8)), a = (1 - 0.6 * q) * P(t0, t0 + 0.8);
        C.glow(ctx, x, y, 60 * (1 - 0.7 * q), [255, 190, 120], 0.8 * a); ctx.save(); ctx.fillStyle = C.rgba([255, 230, 190], a); ctx.beginPath(); ctx.arc(x, y, 5 * (1 - 0.6 * q), 0, 6.283); ctx.fill(); ctx.restore(); }
      C.dust(ctx, T, { n: 50, alpha: 0.18, seed: 8, warm: 0.8, speed: 0.2 });
"""

# ---------------------------------------------------------------- CH2 la ola: one runs and gets rolled; one dives under
ST2 = """
      const HZ = 560, WL = 665;
      D.sky(ctx, HZ, [14, 24, 34], [52, 78, 92], [150, 170, 170]);
      C.clouds(ctx, T, { seed: 9, n: 10, y0: 60, y1: HZ - 80, alpha: 0.3, warm: 0.1, drift: 12 });
      C.glow(ctx, 1300, HZ - 40, 700, [220, 230, 220], 0.2);
      // waves: [arrival time at xa, xa, speed, amp]
      const WV = [[11.1, 820, 250, 300], [22.0, 1000, 250, 300], [32.6, 1040, 420, 210], [38.6, 1080, 420, 220], [44.6, 1120, 420, 230]];
      const crest = WV.map(([ta, xa, v, A]) => { const xc = xa - v * (T - ta); const grow = C.clamp((2500 - xc) / 1100), decay = xc < 600 ? C.lerp(1, 0.45, C.clamp((600 - xc) / 900)) : 1; return [xc, A * (0.25 + 0.75 * grow) * decay]; });
      const prof = (u) => u < 0 ? Math.exp(-(u / 120) * (u / 120)) : Math.exp(-(u / 420) * (u / 420));
      const SY = (x) => { let y = WL + 8 * Math.sin(x * 0.012 + T * 1.6) + 5 * Math.sin(x * 0.031 - T * 2.4); for (const [xc, A] of crest) y -= A * prof(x - xc); return y; };
      // far sea band
      M.water(ctx, (x) => HZ + 4 + 3 * Math.sin(x * 0.02 + T), { top: [70, 96, 104], bot: [24, 40, 48], depth: 80 });
      M.glints(ctx, T, HZ + 4, WL - 20, [230, 240, 235], 0.5, 17, 80);
      // people (drawn before the water so the water covers them)
      const dive = Math.max(M.bump(T, 18.8, 25.8, 0.9), M.bump(T, 31.6, 33.8, 0.6), M.bump(T, 37.6, 39.8, 0.6), M.bump(T, 43.6, 45.8, 0.6));
      // A: turns and runs, then is rolled by the wave
      const aA = P(-1, 0.5) * (1 - P(12.4, 13.6));
      if (aA > 0.01) { const turn = T > 8.6, hit = P(11.0, 12.6);
        const ax = K([[0, 820], [8.8, 820], [11.0, 700], [13.6, 330]]);
        ctx.save(); ctx.globalAlpha = aA;
        C.person(ctx, ax, 800 - 60 * hit, 300, { fill: "#04080c", rim: [200, 225, 230], rimA: 0.55, walk: turn && hit < 0.1 ? T * 7 : null, flip: turn, lean: -0.15 * (turn ? 1 : 0) - 5.0 * hit });
        ctx.restore(); }
      // B: faces the wave, dives under it, comes up on the other side
      const bA = P(13.6, 14.6);
      if (bA > 0.01) { const bx = K([[13.6, 960], [26, 1000], [31, 1000], [47, 1150]]), breath = M.bump(T, 17.2, 18.8, 0.6);
        ctx.save(); ctx.globalAlpha = bA;
        C.person(ctx, bx - 40 * dive, 800 - 50 * dive, 300 * (1 + 0.02 * breath), { fill: "#04080c", rim: [210, 235, 240], rimA: 0.6, lean: 1.45 * dive });
        ctx.restore();
        if (dive > 0.5) M.bubbles(ctx, T, bx + 200, 760, dive, { seed: 3, n: 12, rise: 140, spread: 120 }); }
      // the water (semi-transparent so we see under it)
      M.water(ctx, SY, { top: [40, 78, 88], bot: [6, 18, 26], depth: 420, alpha: 0.86, rim: [220, 240, 240], rimA: 0.5, rimW: 3, step: 8 });
      // foam: crest lips and white water behind the break
      ctx.save(); ctx.globalCompositeOperation = "lighter";
      for (const [xc, A] of crest) { if (A < 40 || xc < -300 || xc > 2300) continue; const top = SY(xc);
        C.soft(ctx, xc + 120, top + A * 0.45, 260, A * 0.5, [120, 190, 180], 0.18);
        ctx.fillStyle = C.rgba([235, 248, 245], 0.55); ctx.beginPath(); ctx.moveTo(xc + 160, SY(xc + 160)); ctx.quadraticCurveTo(xc + 20, top - 34, xc - 70, top + 26 + 10 * Math.sin(T * 3)); ctx.quadraticCurveTo(xc + 10, top - 6, xc + 160, SY(xc + 160) + 10); ctx.closePath(); ctx.fill();
        const r = C.rng(Math.floor(T * 6) + 7); for (let i = 0; i < 40; i++) { const ox = (r() - 0.2) * 220, oy = -r() * 60; ctx.fillStyle = C.rgba([235, 248, 245], 0.35 * r()); ctx.beginPath(); ctx.arc(xc + ox, top + oy + 10, 1.5 + r() * 2.5, 0, 6.283); ctx.fill(); }
        for (let i = 0; i < 18; i++) { const q = (i / 18), x = xc - 40 - q * 170 + Math.sin(T * 4 + i) * 8, y = SY(x) + 10 + 20 * q; C.soft(ctx, x, y, 40, 16, [225, 240, 240], 0.16 * (1 - 0.6 * q)); } }
      // A's wipe-out burst
      { const b = M.bump(T, 11.0, 13.6, 0.5); if (b > 0.01) C.soft(ctx, 640, 700, 420, 220, [230, 240, 240], 0.35 * b); }
      ctx.restore();
      C.dust(ctx, T, { n: 50, alpha: 0.18, seed: 12, warm: 0.1, speed: 0.4, wind: 30 });
"""

# ---------------------------------------------------------------- CH3 lo profundo: from the storm surface down to the calm
ST3 = """
      const d = K([[0, 0], [12.2, 0], [16.4, 1], [33.4, 1], [35.6, 0.6], [38.2, 0.6], [39.8, 1], [53, 1]]);
      const sy = C.lerp(560, -460, d);
      const fl = M.flash(T, [3.0, 9.4, 35.8]);
      const SF = (x) => sy + 26 * Math.sin(x * 0.008 + T * 2.2) + 12 * Math.sin(x * 0.023 - T * 3.4);
      // stormy sky above the surface
      if (sy > -80) { D.sky(ctx, Math.max(0, sy), [6, 8, 12], [22, 26, 34], [50, 58, 70]);
        if (fl > 0.01) { ctx.save(); ctx.fillStyle = C.rgba([170, 185, 220], 0.3 * fl); ctx.fillRect(0, 0, W, Math.max(0, sy)); ctx.restore(); }
        C.clouds(ctx, T, { seed: 15, n: 12, y0: Math.min(sy - 300, 40), y1: sy - 60, alpha: 0.5, warm: 0, drift: 50 });
        M.rain(ctx, T, 0.8, { seed: 11, n: 220, ang: 0.3, speed: 1500 }); }
      // the sea: turbulent near the surface, deep calm below
      { const g = ctx.createLinearGradient(0, sy, 0, sy + 1400); g.addColorStop(0, "rgb(34,58,72)"); g.addColorStop(0.25, "rgb(12,34,52)"); g.addColorStop(0.6, "rgb(6,22,40)"); g.addColorStop(1, "rgb(3,10,22)");
        ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(-20, H + 20); for (let x = -20; x <= W + 20; x += 10) ctx.lineTo(x, SF(x)); ctx.lineTo(W + 20, H + 20); ctx.closePath(); ctx.fill(); }
      ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.strokeStyle = C.rgba([220, 235, 245], 0.55 + 0.3 * fl); ctx.lineWidth = 3; ctx.beginPath(); for (let x = -20; x <= W + 20; x += 10) { const y = SF(x); if (x === -20) ctx.moveTo(x, y); else ctx.lineTo(x, y); } ctx.stroke(); ctx.restore();
      // churn just below the surface (foam, bubbles)
      { const r = C.rng(31); ctx.save(); ctx.globalCompositeOperation = "lighter"; for (let i = 0; i < 160; i++) { const x = ((r() * W + T * (r() - 0.5) * 300) % W + W) % W, y = sy + 10 + Math.pow(r(), 2) * 260 + Math.sin(T * 3 + i) * 14; if (y < -10 || y > H + 10) continue;
        ctx.fillStyle = C.rgba([210, 230, 240], 0.3 * (1 - (y - sy) / 280)); ctx.beginPath(); ctx.arc(x, y, 1.5 + r() * 3, 0, 6.283); ctx.fill(); } ctx.restore(); }
      // light shafts in the calm
      M.shafts(ctx, T, C.clamp(d * 1.2 - 0.2), Math.max(-200, sy + 40));
      // marine snow drifting
      C.dust(ctx, T, { n: 90, alpha: 0.22 * d, seed: 33, warm: 0, speed: 0.12 });
      // the person: tossed under the surface, then floating still in the deep
      const toss = 1 - C.clamp(d * 1.4);
      const fx = 960 + Math.sin(T * 1.9) * 60 * toss + Math.sin(T * 0.3) * 20, fy = C.lerp(sy + 250, 720, C.clamp(d * 1.6)) + Math.sin(T * 0.6) * 10 + Math.sin(T * 2.7) * 22 * toss;
      const core = P(29.6, 32.6), deep = P(44.8, 50.0);
      C.glow(ctx, fx, fy - 170, 320, [120, 200, 255], 0.18 * d);
      if (core > 0.01) C.glow(ctx, fx, fy - 175, 200 + 60 * deep, [255, 210, 150], (0.4 + 0.2 * Math.sin(T * 1.2)) * core);
      C.person(ctx, fx, fy, 290, { fill: "#030a12", rim: C.mixc([150, 210, 255], [255, 210, 160], core * 0.5), rimA: 0.55 + 0.2 * d, lean: Math.sin(T * 2.3) * 0.5 * toss + Math.sin(T * 0.5) * 0.05 });
      const breathe = Math.max(M.bump(T, 39.4, 44.0, 0.6), 0.4 * d);
      M.bubbles(ctx, T, fx + 6, fy - 300, breathe, { seed: 5, n: 10, rise: 320, speed: 50, spread: 20 });
"""

# ---------------------------------------------------------------- CH4 la corriente: top-down rip current; swim sideways, then in
ST4 = """
      const SH = 840;               // shoreline (beach below)
      const z = K([[0, 1.0], [47, 1.06]]);
      ctx.save(); ctx.translate(960, 560); ctx.scale(z, z); ctx.translate(-960, -560);
      // sea from above
      { const g = ctx.createLinearGradient(0, -100, 0, SH); g.addColorStop(0, "rgb(6,22,34)"); g.addColorStop(1, "rgb(28,74,84)"); ctx.fillStyle = g; ctx.fillRect(-100, -100, W + 200, SH + 100); }
      // the rip channel: darker band, water streaming out to sea
      const CX = 960, cw = (y) => 150 + Math.max(0, (420 - y)) * 0.6;
      { ctx.save(); for (let y = -100; y < SH; y += 8) { const w = cw(y); const g = ctx.createLinearGradient(CX - w, 0, CX + w, 0); g.addColorStop(0, "rgba(2,10,18,0)"); g.addColorStop(0.5, "rgba(2,10,18,0.55)"); g.addColorStop(1, "rgba(2,10,18,0)"); ctx.fillStyle = g; ctx.fillRect(CX - w, y, 2 * w, 8); } ctx.restore(); }
      { const r = C.rng(41); ctx.save(); ctx.globalCompositeOperation = "lighter"; for (let i = 0; i < 160; i++) { const q = (r() + T * (0.05 + r() * 0.05)) % 1, y = SH - q * (SH + 80), w = cw(y), x = CX + (r() - 0.5) * 1.6 * w;
        ctx.strokeStyle = C.rgba([150, 210, 220], 0.28 * (1 - q * 0.6)); ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + (x - CX) * 0.05, y - 22); ctx.stroke(); } ctx.restore(); }
      // breaking waves rolling to shore, broken where the channel runs
      { ctx.save(); ctx.globalCompositeOperation = "lighter"; for (let k = 0; k < 7; k++) { const y = 60 + ((k * 115 + T * 38) % 790); const a = C.clamp((y - 60) / 200) * C.clamp((SH - y) / 80);
        ctx.lineWidth = 3 + 4 * (y / SH); ctx.beginPath(); let on = false;
        for (let x = -40; x <= W + 40; x += 12) { const gap = C.clamp((Math.abs(x - CX) - cw(y) * 0.55) / 120); const yy = y + Math.sin(x * 0.01 + k) * 10; if (gap > 0.05) { if (!on) { ctx.moveTo(x, yy); on = true; } else ctx.lineTo(x, yy); } else on = false; }
        ctx.strokeStyle = C.rgba([230, 245, 245], 0.4 * a); ctx.stroke(); } ctx.restore(); }
      // beach
      { const g = ctx.createLinearGradient(0, SH, 0, H + 60); g.addColorStop(0, "rgb(150,128,100)"); g.addColorStop(1, "rgb(60,48,38)"); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(-100, H + 100);
        for (let x = -100; x <= W + 100; x += 20) ctx.lineTo(x, SH + Math.sin(x * 0.004 + 1) * 14 + Math.sin(x * 0.02 + T * 1.5) * 4); ctx.lineTo(W + 100, H + 100); ctx.closePath(); ctx.fill();
        ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.strokeStyle = "rgba(240,250,250,0.45)"; ctx.lineWidth = 4; ctx.beginPath(); for (let x = -100; x <= W + 100; x += 20) { const y = SH + Math.sin(x * 0.004 + 1) * 14 + Math.sin(x * 0.02 + T * 1.5) * 4; if (x === -100) ctx.moveTo(x, y); else ctx.lineTo(x, y); } ctx.stroke(); ctx.restore(); }
      // chevrons in the channel: the pull
      { const pa = M.bump(T, 3.6, 18.0, 1.0) * 0.8 + 0.2; ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.lineWidth = 4; ctx.lineCap = "round";
        for (let k = 0; k < 4; k++) { const q = ((T * 0.25 + k / 4) % 1), y = SH - 60 - q * 640; ctx.strokeStyle = C.rgba([170, 230, 240], 0.35 * pa * Math.sin(q * Math.PI)); ctx.beginPath(); ctx.moveTo(CX - 40, y + 26); ctx.lineTo(CX, y); ctx.lineTo(CX + 40, y + 26); ctx.stroke(); } ctx.restore(); }
      // swimmer A: swims to shore inside the channel, gets pulled out, tires, sinks
      const aA = P(3.2, 4.2) * (1 - P(15.0, 18.0));
      if (aA > 0.01) { const ay = K([[3, 640], [13.5, 430], [18, 400]]), ax = CX - 10 + Math.sin(T * 0.7) * 10, tire = P(13.6, 18.0);
        ctx.save(); ctx.globalAlpha = aA; M.ripple(ctx, T, ax, ay, 0.6 * (1 - tire)); M.swimTop(ctx, ax, ay, 2.5 * (1 - 0.25 * tire), Math.PI / 2, T * (9 - 6 * tire), "#03121a", [190, 235, 240], 0.6); ctx.restore(); }
      // swimmer B: turns sideways, leaves the channel, then swims in
      const bpos = (u) => { const x = D.keys([[18.8, CX], [22.6, CX], [26.6, 1290], [60, 1290]], u), y = D.keys([[18.8, 440], [22.6, 470], [26.6, 470], [27.2, 470], [30.4, 760], [60, 760]], u); return [x, y]; };
      const bA = P(18.8, 19.8);
      if (bA > 0.01) {
        // the route (glows again when recalled)
        const recall = Math.max(M.bump(T, 22.6, 31.0, 1.0) * 0.6, P(37.2, 40.0)); const turnGlow = M.bump(T, 40.4, 44.0, 0.6);
        ctx.save(); ctx.globalCompositeOperation = "lighter"; for (let u = 22.4; u < Math.min(T, 31.6); u += 0.22) { const [x, y] = bpos(u); ctx.fillStyle = C.rgba([255, 215, 160], 0.55 * recall * bA); ctx.beginPath(); ctx.arc(x, y, 3.5, 0, 6.283); ctx.fill(); }
        if (T > 26.6) C.glow(ctx, 1290, 470, 140, [255, 200, 140], 0.25 * recall + 0.7 * turnGlow); ctx.restore();
        const [bx, by] = bpos(T); const swimming = T < 30.4;
        const ang = D.keys([[18.8, Math.PI / 2], [22.4, Math.PI / 2], [23.4, 0], [26.6, 0], [27.6, Math.PI / 2], [60, Math.PI / 2]], T);
        ctx.save(); ctx.globalAlpha = bA; M.ripple(ctx, T, bx, by, swimming ? 0.5 : 0.25);
        if (true) M.swimTop(ctx, bx, by, 2.5, ang, T * 6, "#03121a", [255, 220, 180], 0.65, !swimming);
        else { // standing on the sand, seen from above
          C.glow(ctx, bx, by, 120, [255, 210, 160], 0.25); ctx.fillStyle = "#1a120c"; ctx.shadowColor = "rgba(255,220,180,0.6)"; ctx.shadowBlur = 16; ctx.beginPath(); ctx.ellipse(bx, by, 52, 20, 0, 0, 6.283); ctx.fill(); ctx.beginPath(); ctx.arc(bx, by - 2, 21, 0, 6.283); ctx.fill(); }
        ctx.restore(); }
      ctx.restore();
      C.dust(ctx, T, { n: 40, alpha: 0.12, seed: 44, warm: 0.3, speed: 0.2 });
"""

# ---------------------------------------------------------------- CH5 el puerto: the moored boat; untie the rope and sail out
ST5 = """
      const HZ = 540;
      const go = P(41.0, 47.0), wind = P(33.0, 37.0);
      D.sky(ctx, HZ, [8, 12, 30], [40, 52, 92], C.mixc([170, 140, 140], [255, 186, 130], go));
      C.glow(ctx, 1500, HZ, 800, [255, 170, 110], 0.25 + 0.3 * go);
      D.stars(ctx, T, 0.5 * (1 - go), 51, 160, HZ - 200, 0);
      // far coast and breakwater; the harbor mouth opens to the right
      ctx.fillStyle = "#0a0c1a"; ctx.beginPath(); ctx.moveTo(0, HZ); for (let x = 0; x <= 1100; x += 20) ctx.lineTo(x, HZ - 40 - 50 * Math.max(0, Math.sin(x * 0.004 + 0.5)) - 18 * Math.sin(x * 0.02)); ctx.lineTo(1100, HZ); ctx.closePath(); ctx.fill();
      ctx.fillStyle = "#070812"; ctx.fillRect(0, HZ - 10, 1240, 12);
      [[200, 0.6], [360, 0.5], [520, 0.55], [1060, 0.5]].forEach(([x, s], i) => M.sailboat(ctx, x, HZ - 2, 90 * s * 2, Math.sin(T * 0.8 + i) * 0.03, 0, "#0b0d1a", null, 0, T));
      // water
      { const g = ctx.createLinearGradient(0, HZ, 0, H); g.addColorStop(0, "rgb(60,64,96)"); g.addColorStop(0.4, "rgb(20,24,44)"); g.addColorStop(1, "rgb(4,5,10)"); ctx.fillStyle = g; ctx.fillRect(0, HZ, W, H - HZ); }
      M.glints(ctx, T, HZ + 4, H, [255, 200, 160], 0.5 + 0.3 * go, 52, 170, 1480, 700);
      M.glints(ctx, T * (1 + wind), HZ + 40, H, [170, 190, 240], 0.25 + 0.25 * wind, 53, 120);
      // the dock (left) with posts and a bollard
      const DY = 760;
      ctx.save(); ctx.fillStyle = "#06060c"; for (let x = 40; x <= 760; x += 120) ctx.fillRect(x, DY, 18, 160); ctx.fillRect(-40, DY - 26, 820, 30);
      ctx.shadowColor = "rgba(190,200,255,0.4)"; ctx.shadowBlur = 10; ctx.fillRect(700, DY - 66, 26, 42); ctx.beginPath(); ctx.ellipse(713, DY - 66, 22, 7, 0, 0, 6.283); ctx.fill(); ctx.restore();
      // the boat
      const bx = K([[0, 1030], [41.0, 1030], [47.5, 1330], [60, 1600]]), bob = Math.sin(T * 1.1) * 4 * (1 + wind), by = 800 + bob, rot = Math.sin(T * 0.9) * 0.02 * (1 + 2 * wind);
      const sail = P(41.2, 43.4), BL = 340;
      // rope from bollard to bow (slack sag), dropped when untied
      const untie = P(38.8, 39.8);
      { const x0 = 716, y0 = DY - 60, x1 = bx - BL * 0.5, y1 = by - BL * 0.15; ctx.save(); ctx.strokeStyle = "#0c0a10"; ctx.lineWidth = 4; ctx.shadowColor = C.rgba([255, 210, 170], 0.5 + 0.4 * M.bump(T, 22.0, 26.0, 0.8)); ctx.shadowBlur = 10; ctx.beginPath();
        if (untie < 0.02) { ctx.moveTo(x0, y0); ctx.quadraticCurveTo((x0 + x1) / 2, Math.max(y0, y1) + 40 + 10 * Math.sin(T), x1, y1); }
        else { const ex = C.lerp(x0, x1 - 30, untie), ey = C.lerp(y0, 830, untie); ctx.moveTo(ex, ey); ctx.quadraticCurveTo((ex + x1) / 2, 840, x1, y1); }
        ctx.stroke(); ctx.restore(); }
      // the person on the dock: looks, walks to the bollard, unties, jumps aboard, raises the sail
      const onBoat = T > 40.9;
      const px = K([[0, 560], [37.8, 560], [38.7, 690], [40.0, 690], [40.9, 990], [60, 990]]);
      const kneel = M.bump(T, 38.7, 39.9, 0.4), jump = M.bump(T, 40.0, 40.9, 0.3);
      const pRim = C.mixc([180, 195, 255], [255, 200, 150], go);
      if (!onBoat) C.person(ctx, px, DY - 26 + 50 * kneel - 90 * Math.sin(C.prog(T, 40.0, 40.9) * Math.PI), 290 * (1 - 0.25 * kneel), { fill: "#06060c", rim: pRim, rimA: 0.6, walk: (T > 37.8 && T < 38.7) ? T * 5 : null, lean: 0.4 * kneel + 0.2 * jump });
      ctx.save(); ctx.translate(bx, by); ctx.rotate(rot);
      M.sailboat(ctx, 0, 0, BL, 0, sail, "#06060c", [255, 205, 160], 0.45, T, C.mixc([150, 150, 190], [250, 220, 190], go));
      if (onBoat) C.person(ctx, -BL * 0.3, -BL * 0.15 + 4, 260, { fill: "#06060c", rim: pRim, rimA: 0.65, lean: 0.05 });
      ctx.restore();
      // reflections
      { ctx.save(); ctx.globalCompositeOperation = "lighter"; for (let i = 0; i < 10; i++) { const y = by + 50 + i * 9; ctx.fillStyle = C.rgba([255, 205, 160], 0.06 * (1 - i / 10)); ctx.fillRect(bx - 150 + Math.sin(T * 2 + i) * 10, y, 300 - i * 16, 2); } ctx.restore(); }
      if (go > 0.01) { ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.strokeStyle = C.rgba([255, 220, 190], 0.25 * go); ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(bx - BL * 0.5, by + 20); ctx.quadraticCurveTo(bx - 300, by + 30, 1030 - 200, by + 50); ctx.stroke(); ctx.restore(); }
      C.dust(ctx, T, { n: 50, alpha: 0.15, seed: 54, warm: 0.4 + 0.5 * go, speed: 0.2, wind: 30 * wind });
"""

# ---------------------------------------------------------------- CH6 cierre: sunrise at sea, sailing with the wake of the lessons
ST6 = """
      const HZ = 560;
      const open = P(4.8, 8.0), sunUp = P(6.0, 50.0), bravo = M.bump(T, 37.6, 43.6, 1.4);
      const sunX = 1260, sunY = C.lerp(HZ + 50, HZ - 230, sunUp);
      D.sky(ctx, HZ, C.mixc([10, 12, 26], [40, 52, 96], open), C.mixc([50, 40, 64], [214, 130, 100], open), C.mixc([120, 90, 90], [255, 200, 140], open));
      C.sun(ctx, sunX, sunY, 58, 0.3 + 0.7 * open, HZ);
      C.rays(ctx, sunX, sunY, T, 0.55 * P(7.0, 12.0), 13, 1500);
      // clouds part to the sides
      { const r = C.rng(61); for (let i = 0; i < 12; i++) { const bx = r() * W, by = 80 + r() * 300, side = bx < 960 ? -1 : 1, x = bx + side * open * (500 + r() * 400) + T * 6; C.soft(ctx, x, by, 260 + r() * 200, 70 + r() * 40, C.mixc([40, 44, 60], [255, 190, 150], open * 0.6), 0.5 * (1 - 0.6 * open)); } }
      // sea
      const z = K([[0, 1.14], [10.0, 1.14], [17.0, 1.0], [31.0, 1.0], [46, 1.1]]);
      ctx.save(); ctx.translate(960, 760); ctx.scale(z, z); ctx.translate(-960, -760);
      M.water(ctx, (x) => HZ + 3 * Math.sin(x * 0.02 + T), { top: C.mixc([60, 50, 70], [200, 130, 100], open), bot: [20, 14, 24], depth: 500 });
      M.glints(ctx, T, HZ + 4, H + 100, [255, 220, 170], 0.5 + 0.5 * open, 62, 200, sunX, 600);
      const sea = { base: 770, amps: [14 + 40 * bravo, 7 + 10 * bravo, 3], freqs: [0.003, 0.009, 0.022], speeds: [0.8, -1.3, 2.0] };
      const SY = (x) => M.surf(x, T, sea);
      // the wake: five lights, one per lesson
      { const marks = [17.4, 20.2, 23.0, 25.6, 28.4]; ctx.save(); ctx.globalCompositeOperation = "lighter";
        const pt = (q) => [C.lerp(760, 140, q), C.lerp(790, HZ + 30, Math.pow(q, 0.8))];
        const wa = P(15.0, 18.0) * (1 - 0.5 * P(31.0, 35.0));
        for (let j = 0; j < 80; j++) { const q = j / 80, [x, y] = pt(q); ctx.fillStyle = C.rgba([255, 220, 180], 0.3 * wa * (1 - q)); ctx.fillRect(x - 20 * (1 - q), y + Math.sin(T * 2 + j) * 2, 40 * (1 - q), 2); }
        marks.forEach((t0, i) => { const a = P(t0, t0 + 0.8) * (1 - 0.6 * P(31.0, 35.0)); if (a > 0.01) { const [x, y] = pt(0.16 + i * 0.17); C.glow(ctx, x, y, 80 * (1 - i * 0.12), [255, 205, 150], 0.8 * a); } });
        ctx.restore(); }
      // the boat and its sailor
      const bx = 900 + Math.sin(T * 0.25) * 20, by = SY(bx) - 6, rot = Math.atan2(SY(bx + 60) - SY(bx - 60), 120) * 0.8, BL = 360;
      ctx.save(); ctx.translate(bx, by); ctx.rotate(rot);
      M.sailboat(ctx, 0, 0, BL, 0, 1, "#0b0606", [255, 214, 160], 0.55, T, [255, 226, 196]);
      C.person(ctx, -BL * 0.3, -BL * 0.15 + 4, 250, { fill: "#0b0606", rim: [255, 214, 160], rimA: 0.7, lean: -0.04 + 0.1 * bravo * Math.sin(T * 1.6) });
      ctx.restore();
      M.water(ctx, (x) => SY(x) + 40, { top: C.mixc([40, 30, 40], [130, 76, 60], open), bot: [8, 5, 6], depth: 260, rim: [255, 214, 160], rimA: 0.35 });
      ctx.restore();
      // gulls
      if (T > 11 && T < 34) for (let i = 0; i < 3; i++) { const q = C.prog(T, 11 + i * 1.5, 30 + i), x = C.lerp(1700 + i * 80, 300, q), y = 300 + i * 40 + Math.sin(T * 0.8 + i) * 20; M.gull(ctx, x, y, 1.6 - i * 0.3, T * 5 + i, "#2a1612"); }
      C.dust(ctx, T, { n: 70, alpha: 0.3, seed: 66, warm: 1, speed: 0.2 });
"""

STAGES = [ST0, ST1, ST2, ST3, ST4, ST5, ST6]

TITLES = {
    0: [("Lo que el mar<br>te enseña", 1.2, 9.6, "font-size:96px", "kick", "QUIET MIND"),
        ("El mar enseña.", 31.2, None, "font-size:90px; color:#e6ecff", None, None)],
    1: [("I · La marea", 0.0, 7.0, "font-size:84px; color:#ffe2d0", None, None),
        ("Lo que se retira,<br>vuelve a subir.", 41.0, None, "font-size:88px; color:#ffe2d0", None, None)],
    2: [("II · La ola", 0.0, 7.0, "font-size:84px; color:#e6f6f6", None, None),
        ("La ola que enfrentas<br>te deja pasar.", 42.4, None, "font-size:88px; color:#e6f6f6", None, None)],
    3: [("III · Lo profundo", 0.0, 7.0, "font-size:84px; color:#dceeff", None, None),
        ("En lo profundo<br>hay calma.", 45.4, None, "font-size:92px; color:#dceeff", None, None)],
    4: [("IV · La corriente", 0.0, 7.0, "font-size:84px; color:#e6f6f6", None, None),
        ("Cambia de<br>dirección.", 40.6, None, "font-size:96px; color:#ffe2bf", None, None)],
    5: [("V · El puerto", 0.0, 7.0, "font-size:84px; color:#e6ecff", None, None),
        ("En el mar<br>estás vivo.", 44.8, None, "font-size:96px; color:#ffe2bf", None, None)],
    6: [("Ahora sabes<br>leer el agua.", 35.1, 41.4, "font-size:92px; color:#fff1de", None, None),
        ("No te está hundiendo.<br>Te está enseñando a navegar.", 43.1, None, "font-size:84px; color:#fff1de", "kick", "QUIET MIND")],
}

n = len(_CH)
for i, ch in enumerate(_CH):
    start = 0.0 if i == 0 else round(ch['start'] - LEAD, 3)
    end = TOTAL_S if i == n - 1 else round(_CH[i + 1]['start'] - LEAD + 1.0, 3)
    dur = round(end - start, 3)
    off = round(ch['start'] - start, 3)
    cid = f"c{i}"
    stage = PRE.replace("__OFF__", str(off)) + STAGES[i]
    markup, js = "", f'    gsap.set("#{cid}-wrap .hbt", {{ opacity: 0 }});\n'
    for j, (txt, a, b, sty, kk, ktxt) in enumerate(TITLES[i]):
        markup += f'    <div id="{cid}-t{j}" class="title hbt" style="top:110px; {sty}">{txt}</div>\n'
        js += f'    tl.fromTo("#{cid}-t{j}", {{ {TT}, {a + off:.2f});\n'
        if b is not None: js += f'    tl.to("#{cid}-t{j}", {{ opacity: 0, filter: "blur(10px)", duration: 0.5 }}, {b + off:.2f});\n'
        else: js += f'    tl.to("#{cid}-t{j}", {{ opacity: 0, filter: "blur(10px)", duration: 0.6 }}, {max(a + off + 3.0, dur - 1.4):.2f});\n' if i < n - 1 else ""
        if kk:
            markup += f'    <div id="{cid}-k{j}" class="kick hbt" style="top:62px;">{ktxt}</div>\n'
            js += f'    tl.fromTo("#{cid}-k{j}", {{ opacity: 0 }}, {{ opacity: 1, duration: 1.0, ease: "none" }}, {a + off + 0.6:.2f});\n'
            if b is not None: js += f'    tl.to("#{cid}-k{j}", {{ opacity: 0, duration: 0.5 }}, {b + off:.2f});\n'
    if i == n - 1:
        js += f'    tl.to(S("#{cid}-wrap"), {{ opacity: 0, duration: 1.2, ease: "none" }}, {dur - 1.4:.2f});\n'
    S.append((cid, start, dur, 0.0 if i == 0 else 1.0, markup, stage, js))

# align.py joined "lo profundo. Arriba," into one segment; "Arriba" belongs to the next phrase
_fix = {"lo profundo. Arriba,": "lo profundo.", "en la superficie, la tormenta lo sacude todo.": "Arriba, en la superficie, la tormenta lo sacude todo."}
CUES = [(a, b, _fix.get(t, t)) for a, b, t in _T['cues']]
