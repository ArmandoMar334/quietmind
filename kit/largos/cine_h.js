/* Cinematic drawing helpers for the "Nadie va a venir" film. Pure functions of time: deterministic. */
(function () {
  const W = 1920, H = 1080;
  const C = {};
  C.W = W; C.H = H;
  C.clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  C.lerp = (a, b, k) => a + (b - a) * k;
  C.prog = (t, a, b) => C.clamp((t - a) / (b - a));
  C.ease = (x) => { x = C.clamp(x); return x * x * (3 - 2 * x); };
  C.eout = (x) => { x = C.clamp(x); return 1 - Math.pow(1 - x, 3); };
  C.rng = (seed) => { let a = seed >>> 0; return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
  const mix = (c1, c2, k) => c1.map((v, i) => Math.round(C.lerp(v, c2[i], k)));
  C.rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  C.COOL = [150, 170, 200];
  C.WARM = [255, 176, 92];
  C.mixc = mix;

  C.sky = (ctx, o) => {
    const hz = o.hz ?? 1020, warm = o.warm ?? 0, glow = o.glow ?? 0.25;
    const top = mix([2, 3, 6], [10, 14, 34], warm * 0.8);
    const mid = mix([6, 8, 14], [70, 40, 40], warm);
    const hor = mix(C.COOL, C.WARM, warm);
    const g = ctx.createLinearGradient(0, 0, 0, hz);
    g.addColorStop(0, C.rgba(top, 1));
    g.addColorStop(0.6, C.rgba(mid, 1));
    g.addColorStop(1, C.rgba(mix(mid, hor, glow), 1));
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, hz + 1);
    const f = ctx.createLinearGradient(0, hz, 0, H);
    f.addColorStop(0, C.rgba(mix([4, 5, 8], hor, glow * 0.35), 1));
    f.addColorStop(0.25, "rgb(3,3,5)");
    f.addColorStop(1, "rgb(0,0,0)");
    ctx.fillStyle = f; ctx.fillRect(0, hz, W, H - hz);
    // horizon haze line
    const hg = ctx.createLinearGradient(0, hz - 90, 0, hz + 60);
    hg.addColorStop(0, C.rgba(hor, 0));
    hg.addColorStop(0.6, C.rgba(hor, 0.35 * glow));
    hg.addColorStop(1, C.rgba(hor, 0));
    ctx.fillStyle = hg; ctx.fillRect(0, hz - 90, W, 150);
  };

  C.floor = (ctx, t, o) => {
    const hz = o.hz ?? 1020, a = o.alpha ?? 0.22, speed = o.speed ?? 0.2, vx = o.vx ?? 540;
    const col = o.color || [200, 210, 230];
    ctx.save();
    ctx.lineWidth = 1.5;
    for (let i = 0; i < 18; i++) {
      let z = ((i / 18 + t * speed) % 1);
      z = 1 - z;
      const d = 0.04 + z * z * 1.0;
      const y = hz + 22 / d;
      if (y > H) continue;
      ctx.strokeStyle = C.rgba(col, a * C.clamp((y - hz) / 500) );
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }
    for (let k = -12; k <= 12; k++) {
      const xb = vx + k * 260;
      const g = ctx.createLinearGradient(0, hz, 0, H);
      g.addColorStop(0, C.rgba(col, 0)); g.addColorStop(1, C.rgba(col, a * 0.9));
      ctx.strokeStyle = g;
      ctx.beginPath(); ctx.moveTo(vx + k * 4, hz); ctx.lineTo(xb, H); ctx.stroke();
    }
    ctx.restore();
  };

  C.dust = (ctx, t, o) => {
    const r = C.rng(o.seed ?? 7), n = o.n ?? 120, warm = o.warm ?? 0, a = o.alpha ?? 0.5;
    const col = mix([220, 228, 240], C.WARM, warm);
    const box = o.box || [0, 0, W, H];
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    for (let i = 0; i < n; i++) {
      const bx = r(), by = r(), z = 0.2 + r() * 0.8, ph = r() * 6.28, sp = (o.speed ?? 1) * (0.2 + r());
      let x = box[0] + ((bx * box[2] + Math.sin(t * 0.3 * sp + ph) * 30 * z + t * (12 + (o.wind || 0)) * sp * z) % box[2] + box[2]) % box[2];
      let y = box[1] + ((by * box[3] - t * 18 * sp * z) % box[3] + box[3]) % box[3];
      const s = 0.8 + z * 2.6;
      const tw = 0.55 + 0.45 * Math.sin(t * 1.7 * sp + ph);
      if (o.mask && !o.mask(x, y)) continue;
      if (o.streak) {
        ctx.strokeStyle = C.rgba(col, a * z * tw * 0.8); ctx.lineWidth = s * 0.9;
        ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - o.streak * z, y + o.streak * z * 0.06); ctx.stroke();
      } else {
        ctx.fillStyle = C.rgba(col, a * z * tw);
        ctx.beginPath(); ctx.arc(x, y, s, 0, 6.283); ctx.fill();
      }
    }
    ctx.restore();
  };

  C.cone = (ctx, x, y0, y1, w0, w1, alpha, warm = 0) => {
    const col = mix([215, 225, 245], C.WARM, warm);
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    const g = ctx.createLinearGradient(0, y0, 0, y1);
    g.addColorStop(0, C.rgba(col, alpha / 3));
    g.addColorStop(1, C.rgba(col, alpha * 0.05));
    ctx.fillStyle = g;
    for (const k of [1.25, 0.95, 0.65]) {
      ctx.beginPath();
      ctx.moveTo(x - w0 * k / 2, y0); ctx.lineTo(x + w0 * k / 2, y0); ctx.lineTo(x + w1 * k / 2, y1); ctx.lineTo(x - w1 * k / 2, y1); ctx.closePath();
      ctx.fill();
    }
    ctx.restore();
  };

  C.glow = (ctx, x, y, r, col, a) => {
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    const g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, C.rgba(col, a)); g.addColorStop(0.35, C.rgba(col, a * 0.35)); g.addColorStop(1, C.rgba(col, 0));
    ctx.fillStyle = g; ctx.fillRect(x - r, y - r, 2 * r, 2 * r);
    ctx.restore();
  };

  C.sun = (ctx, x, y, r, a, hz) => {
    C.glow(ctx, x, y, r * 7, [255, 150, 70], 0.5 * a);
    C.glow(ctx, x, y, r * 2.6, [255, 200, 130], 0.7 * a);
    ctx.save();
    if (hz != null) { ctx.beginPath(); ctx.rect(0, 0, W, hz); ctx.clip(); }
    ctx.fillStyle = C.rgba([255, 236, 200], a);
    ctx.beginPath(); ctx.arc(x, y, r, 0, 6.283); ctx.fill();
    ctx.restore();
  };

  C.rays = (ctx, x, y, t, a, n = 9, len = 1400) => {
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    for (let i = 0; i < n; i++) {
      const ang = -Math.PI / 2 + (i - (n - 1) / 2) * 0.17 + Math.sin(t * 0.25 + i) * 0.03;
      const w = 0.035 + 0.02 * Math.sin(i * 2.1);
      const al = a * (0.5 + 0.5 * Math.sin(t * 0.6 + i * 1.7));
      const g = ctx.createLinearGradient(x, y, x + Math.cos(ang) * len, y + Math.sin(ang) * len);
      g.addColorStop(0, C.rgba([255, 205, 140], 0.28 * al)); g.addColorStop(1, C.rgba([255, 205, 140], 0));
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.moveTo(x, y);
      ctx.lineTo(x + Math.cos(ang - w) * len, y + Math.sin(ang - w) * len);
      ctx.lineTo(x + Math.cos(ang + w) * len, y + Math.sin(ang + w) * len);
      ctx.closePath(); ctx.fill();
    }
    ctx.restore();
  };

  // silhouette person, feet at (x,y), height h. o.fill, o.rim (color), o.rimA, o.walk (phase)
  C.person = (ctx, x, y, h, o = {}) => {
    const s = h / 180, fill = o.fill || "#050506";
    const walk = o.walk ?? null;
    ctx.save();
    ctx.translate(x, y); if (o.lean) ctx.rotate(o.lean); if (o.flip) ctx.scale(-1, 1); ctx.scale(s, s);
    const path = () => {
      ctx.beginPath();
      ctx.arc(0, -158, 15, 0, 6.283);
      ctx.moveTo(-6, -144); ctx.lineTo(6, -144); ctx.lineTo(6, -138); ctx.lineTo(-6, -138); ctx.closePath();
      ctx.roundRect(-22, -138, 44, 66, [14, 14, 6, 6]);
      const sw = walk == null ? 0 : Math.sin(walk) * 9;
      ctx.roundRect(-30 - sw * 0.3, -134, 10, 58, 5);
      ctx.roundRect(20 + sw * 0.3, -134, 10, 58, 5);
      ctx.roundRect(-19 + sw * 0.5, -76, 17, 76, 6);
      ctx.roundRect(2 - sw * 0.5, -76, 17, 76, 6);
    };
    if (o.rim) {
      ctx.save();
      ctx.shadowColor = C.rgba(o.rim, o.rimA ?? 0.9);
      ctx.shadowBlur = (o.rimBlur ?? 22) * s;
      ctx.fillStyle = C.rgba(o.rim, o.rimA ?? 0.9);
      path(); ctx.fill();
      ctx.restore();
      ctx.save(); ctx.translate(o.rimDx ?? 0, 0);
      ctx.fillStyle = fill; ctx.scale(0.965, 0.985); path(); ctx.fill(); ctx.restore();
    } else {
      ctx.fillStyle = fill; path(); ctx.fill();
    }
    ctx.restore();
  };

  C.shadow = (ctx, x, y, w, a) => {
    ctx.save();
    const g = ctx.createRadialGradient(x, y, 0, x, y, w);
    g.addColorStop(0, `rgba(0,0,0,${a})`); g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = g; ctx.scale(1, 0.22); ctx.translate(0, y / 0.22 - y);
    ctx.beginPath(); ctx.arc(x, y, w, 0, 6.283); ctx.fill();
    ctx.restore();
  };

  C.clouds = (ctx, t, o) => {
    const r = C.rng(o.seed ?? 3), n = o.n ?? 14, y0 = o.y0, y1 = o.y1, a = o.alpha ?? 0.5, warm = o.warm ?? 0;
    const col = mix([120, 130, 150], [255, 190, 140], warm);
    ctx.save();
    for (let i = 0; i < n; i++) {
      const bx = r() * W * 1.4 - W * 0.2, by = C.lerp(y0, y1, r()), rw = 180 + r() * 320, rh = 40 + r() * 70;
      const x = ((bx + t * (o.drift ?? 10) * (0.5 + r())) % (W * 1.4)) - W * 0.2;
      const y = by + (o.dy ? o.dy(t, i) : 0);
      C.soft(ctx, x, y, rw * 1.25, rh * 1.6, col, a * (0.4 + r() * 0.6));
    }
    ctx.restore();
  };

  C.fog = (ctx, t, o) => {
    const r = C.rng(o.seed ?? 5), n = o.n ?? 10, a = o.alpha ?? 0.5;
    const col = o.color || [150, 160, 180];
    ctx.save();
    for (let i = 0; i < n; i++) {
      const bx = r() * (W + 320) - 160, by = C.lerp(o.y0, o.y1, r()), rw = 260 + r() * 380, rh = 90 + r() * 160;
      const part = o.part ? o.part(i, bx) : 0;
      const x = bx + Math.sin(t * 0.15 + i) * 40 + t * (o.drift ?? 6) * (0.5 + r()) + part;
      C.soft(ctx, x, by, rw * 1.3, rh * 1.7, col, a * (0.5 + r() * 0.5));
    }
    ctx.restore();
  };

  C.soft = (ctx, x, y, rx, ry, col, a) => {
    ctx.save(); ctx.translate(x, y); ctx.scale(1, ry / rx);
    const g = ctx.createRadialGradient(0, 0, 0, 0, 0, rx);
    g.addColorStop(0, C.rgba(col, a)); g.addColorStop(0.5, C.rgba(col, a * 0.55)); g.addColorStop(1, C.rgba(col, 0));
    ctx.fillStyle = g; ctx.fillRect(-rx, -rx, 2 * rx, 2 * rx); ctx.restore();
  };

  C.vignette = (ctx, a = 0.75) => { const M = Math.max(W, H);
    const g = ctx.createRadialGradient(W / 2, H * 0.48, M * 0.28, W / 2, H * 0.5, M * 0.62);
    g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(1, `rgba(0,0,0,${a})`);
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  };

  window.CINE = C;
})();

/* Desert helpers (horizontal 1920x1080) */
(function () {
  const C = window.CINE, W = C.W, H = C.H, D = {};
  D.keys = (K, T) => { if (T <= K[0][0]) return K[0][1]; for (let i = 1; i < K.length; i++) if (T <= K[i][0]) { const k = (T - K[i-1][0]) / (K[i][0] - K[i-1][0]); return C.lerp(K[i-1][1], K[i][1], C.ease(k)); } return K[K.length-1][1]; };
  D.kc = (K, T) => { if (T <= K[0][0]) return K[0][1]; for (let i = 1; i < K.length; i++) if (T <= K[i][0]) { const k = C.ease((T - K[i-1][0]) / (K[i][0] - K[i-1][0])); return C.mixc(K[i-1][1], K[i][1], k); } return K[K.length-1][1]; };
  // sky with explicit palette
  D.sky = (ctx, hz, top, mid, hor) => {
    const g = ctx.createLinearGradient(0, 0, 0, hz + 40);
    g.addColorStop(0, C.rgba(top, 1)); g.addColorStop(0.62, C.rgba(mid, 1)); g.addColorStop(1, C.rgba(hor, 1));
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, hz + 40);
  };
  D.stars = (ctx, t, a, seed = 11, n = 260, hz = 600, rot = 0) => {
    if (a <= 0.01) return; const r = C.rng(seed);
    ctx.save(); ctx.globalCompositeOperation = "lighter";
    for (let i = 0; i < n; i++) {
      let x = r() * W * 1.2 - W * 0.1, y = r() * hz * 1.05; const s = 0.6 + r() * r() * 2.4, ph = r() * 6.28;
      if (rot) { const cx = W * 0.5, cy = -200, dx = x - cx, dy = y - cy, an = rot; x = cx + dx * Math.cos(an) - dy * Math.sin(an); y = cy + dx * Math.sin(an) + dy * Math.cos(an); }
      const tw = 0.6 + 0.4 * Math.sin(t * (0.8 + r() * 2) + ph);
      const fade = C.clamp((hz - y) / 220);
      ctx.fillStyle = C.rgba([225, 232, 255], a * tw * fade * (0.35 + 0.65 * r()));
      ctx.beginPath(); ctx.arc(x, y, s, 0, 6.283); ctx.fill();
    }
    ctx.restore();
  };
  // dune ridge height
  D.ridge = (x, o) => { let y = o.base; const A = o.amps, F = o.freqs, P = o.phases; for (let k = 0; k < A.length; k++) y -= A[k] * (0.5 + 0.5 * Math.sin(x * F[k] + P[k])); return y; };
  // draw a dune layer. o: base, amps, freqs, phases, off (x offset), top (color), bot, rim, rimA, rimW
  D.dune = (ctx, o) => {
    const off = o.off || 0, step = 12;
    const yAt = (x) => D.ridge(x + off, o);
    let minY = 1e9; for (let x = -20; x <= W + 20; x += step) minY = Math.min(minY, yAt(x));
    ctx.save();
    ctx.beginPath(); ctx.moveTo(-20, H + 10);
    for (let x = -20; x <= W + 20; x += step) ctx.lineTo(x, yAt(x));
    ctx.lineTo(W + 20, H + 10); ctx.closePath();
    const g = ctx.createLinearGradient(0, minY, 0, Math.min(H, minY + (o.depth || 420)));
    g.addColorStop(0, C.rgba(o.top, 1)); g.addColorStop(1, C.rgba(o.bot, 1));
    ctx.fillStyle = g; ctx.fill();
    if (o.rimA > 0.01) {
      ctx.globalCompositeOperation = "lighter"; ctx.lineWidth = o.rimW || 2.2;
      ctx.shadowColor = C.rgba(o.rim, o.rimA); ctx.shadowBlur = 10;
      ctx.strokeStyle = C.rgba(o.rim, o.rimA);
      ctx.beginPath(); for (let x = -20; x <= W + 20; x += step) { const y = yAt(x); if (x === -20) ctx.moveTo(x, y); else ctx.lineTo(x, y); } ctx.stroke();
    }
    ctx.restore();
    return yAt;
  };
  // sand blown off crests / wind streaks
  D.wind = (ctx, t, a, o = {}) => {
    if (a <= 0.01) return; const r = C.rng(o.seed || 5), n = o.n || 160, col = o.col || [220, 200, 170], sp = o.speed || 900, y0 = o.y0 ?? 0, y1 = o.y1 ?? H;
    ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.lineCap = "round";
    for (let i = 0; i < n; i++) { const z = 0.3 + r() * 0.7, bx = r(), by = r();
      const x = ((bx * (W + 400) + t * sp * z) % (W + 400)) - 200, y = C.lerp(y0, y1, by) + Math.sin(t * 2 + i) * 6;
      const L = (40 + 140 * z) * (o.len || 1);
      ctx.strokeStyle = C.rgba(col, a * z * 0.35); ctx.lineWidth = 0.8 + 1.6 * z;
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - L, y + L * 0.04); ctx.stroke(); }
    ctx.restore();
  };
  D.palm = (ctx, x, y, h, sway, fill = "#050507", rim = null, rimA = 0) => {
    ctx.save(); ctx.translate(x, y);
    const lean = 0.12 + sway, topX = Math.sin(lean) * h, topY = -h;
    ctx.fillStyle = fill; ctx.strokeStyle = fill;
    if (rim) { ctx.shadowColor = C.rgba(rim, rimA); ctx.shadowBlur = 14; }
    ctx.lineWidth = h * 0.05; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.quadraticCurveTo(topX * 0.2, topY * 0.55, topX, topY); ctx.stroke();
    for (let k = 0; k < 8; k++) { const an = -Math.PI / 2 + (k - 3.5) * 0.42 + Math.sin(sway * 3 + k) * 0.05; const L = h * (0.45 + 0.12 * Math.sin(k * 2.3));
      const ex = topX + Math.cos(an) * L * 1.15, ey = topY + Math.sin(an) * L * 0.5 + L * 0.35;
      ctx.lineWidth = h * 0.022; ctx.beginPath(); ctx.moveTo(topX, topY); ctx.quadraticCurveTo(topX + Math.cos(an) * L * 0.6, topY + Math.sin(an) * L * 0.6 - L * 0.1, ex, ey); ctx.stroke();
      ctx.lineWidth = h * 0.05; ctx.globalAlpha = 0.9; ctx.beginPath(); ctx.moveTo(topX + Math.cos(an) * L * 0.2, topY + Math.sin(an) * L * 0.15); ctx.quadraticCurveTo(topX + Math.cos(an) * L * 0.6, topY + Math.sin(an) * L * 0.6 - L * 0.05, ex, ey); ctx.stroke(); ctx.globalAlpha = 1; }
    ctx.restore();
  };
  D.rock = (ctx, x, y, w, h, fill = "#07070a", seed = 3) => { const r = C.rng(seed); ctx.save(); ctx.fillStyle = fill; ctx.beginPath(); ctx.moveTo(x - w / 2, y);
    const n = 9; for (let i = 0; i <= n; i++) { const q = i / n, px = x - w / 2 + w * q, py = y - h * Math.pow(Math.sin(Math.PI * q), 0.6) * (0.8 + 0.25 * r()); ctx.lineTo(px, py); }
    ctx.lineTo(x + w / 2, y); ctx.closePath(); ctx.fill(); ctx.restore(); };
  D.fire = (ctx, x, y, t, a, s = 1) => { if (a <= 0.01) return;
    C.glow(ctx, x, y - 20 * s, 380 * s, [255, 140, 60], 0.35 * a); C.glow(ctx, x, y - 14 * s, 120 * s, [255, 190, 110], 0.6 * a);
    ctx.save(); ctx.globalCompositeOperation = "lighter";
    for (let k = 0; k < 5; k++) { const ph = t * (5 + k) + k * 1.3, hh = (34 + 16 * Math.sin(ph)) * s, ww = (10 + 3 * k) * s;
      ctx.fillStyle = C.rgba(k < 2 ? [255, 230, 170] : [255, 140, 60], 0.5 * a);
      ctx.beginPath(); ctx.moveTo(x - ww + (k - 2) * 4 * s, y); ctx.quadraticCurveTo(x + Math.sin(ph) * 6 * s + (k - 2) * 3 * s, y - hh * 1.3, x + ww * 0.3 + (k - 2) * 4 * s, y - hh * 1.6); ctx.quadraticCurveTo(x + ww, y - hh * 0.5, x + ww + (k - 2) * 4 * s, y); ctx.fill(); }
    ctx.restore(); };
  // footprints along a ridge function, from x0 back to x1
  D.prints = (ctx, yAt, x0, x1, a, gap = 26, col = [0, 0, 0]) => { if (a <= 0.01) return; const dir = x1 < x0 ? -1 : 1; let k = 0;
    ctx.save(); for (let x = x0; dir < 0 ? x > x1 : x < x1; x += gap * dir, k++) { const f = 1 - Math.abs(x - x0) / Math.abs(x1 - x0 || 1);
      ctx.fillStyle = C.rgba(col, a * 0.55 * f); ctx.beginPath(); ctx.ellipse(x, yAt(x) + 4 + (k % 2) * 3, 6, 2.2, 0, 0, 6.283); ctx.fill(); } ctx.restore(); };
  D.moon = (ctx, x, y, r, a) => { if (a <= 0.01) return; C.glow(ctx, x, y, r * 8, [170, 190, 230], 0.25 * a); ctx.save(); ctx.fillStyle = C.rgba([235, 238, 245], 0.95 * a); ctx.beginPath(); ctx.arc(x, y, r, 0, 6.283); ctx.fill(); ctx.restore(); };
  D.heat = (ctx, y0, y1, t, a, col = [255, 230, 200]) => { if (a <= 0.01) return; ctx.save(); ctx.globalCompositeOperation = "lighter";
    for (let i = 0; i < 14; i++) { const y = C.lerp(y0, y1, i / 13); ctx.strokeStyle = C.rgba(col, a * 0.06); ctx.lineWidth = 3; ctx.beginPath();
      for (let x = 0; x <= W; x += 30) { const yy = y + Math.sin(x * 0.02 + t * 4 + i * 1.7) * 2.5; if (x === 0) ctx.moveTo(x, yy); else ctx.lineTo(x, yy); } ctx.stroke(); }
    ctx.restore(); };
  window.DES = D;
})();

/* Sea helpers (L02 "Lo que el mar te enseña"), horizontal 1920x1080 */
(function () {
  const C = window.CINE, W = C.W, H = C.H, M = {};
  M.bump = (T, a, b, r = 0.6) => C.ease(C.prog(T, a, a + r)) * (1 - C.ease(C.prog(T, b - r, b)));
  // sea surface height: o {base, amps, freqs, speeds, phases}
  M.surf = (x, t, o) => { let y = o.base; const A = o.amps, F = o.freqs, S = o.speeds || [], P = o.phases || []; for (let k = 0; k < A.length; k++) y += A[k] * Math.sin(x * F[k] + t * (S[k] ?? 1) + (P[k] ?? k * 1.7)); return y; };
  // water body under the curve yAt(x)
  M.water = (ctx, yAt, o) => { const step = o.step || 10, bot = o.bottom ?? H + 10; let minY = 1e9; for (let x = -20; x <= W + 20; x += step) minY = Math.min(minY, yAt(x));
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.beginPath(); ctx.moveTo(-20, bot); for (let x = -20; x <= W + 20; x += step) ctx.lineTo(x, yAt(x)); ctx.lineTo(W + 20, bot); ctx.closePath();
    const g = ctx.createLinearGradient(0, minY, 0, Math.min(H + 200, minY + (o.depth || 400))); g.addColorStop(0, C.rgba(o.top, 1)); g.addColorStop(1, C.rgba(o.bot, 1)); ctx.fillStyle = g; ctx.fill(); ctx.globalAlpha = 1;
    if ((o.rimA || 0) > 0.01) { ctx.globalCompositeOperation = "lighter"; ctx.lineWidth = o.rimW || 2.2; ctx.shadowColor = C.rgba(o.rim, o.rimA); ctx.shadowBlur = 10; ctx.strokeStyle = C.rgba(o.rim, o.rimA);
      ctx.beginPath(); for (let x = -20; x <= W + 20; x += step) { const y = yAt(x); if (x === -20) ctx.moveTo(x, y); else ctx.lineTo(x, y); } ctx.stroke(); }
    ctx.restore(); };
  // shimmering horizontal glints on a sea plane between hz and y1 (cx/spread: a light path)
  M.glints = (ctx, t, hz, y1, col, a, seed = 3, n = 140, cx = null, spread = 0) => { if (a <= 0.01) return; const r = C.rng(seed); ctx.save(); ctx.globalCompositeOperation = "lighter";
    for (let i = 0; i < n; i++) { const q = r(), y = hz + Math.pow(q, 1.6) * (y1 - hz), z = (y - hz) / (y1 - hz); let x = r() * W; const rr = r(); if (cx != null) x = cx + (rr - 0.5) * spread * (0.25 + z);
      const w = (8 + r() * 40) * (0.3 + z * 1.6), tw = Math.max(0, Math.sin(t * (1 + r() * 2) + r() * 6.28)); x += Math.sin(t * 0.5 + i) * 10 * z;
      ctx.fillStyle = C.rgba(col, a * tw * (0.4 + 0.6 * z)); ctx.fillRect(x - w / 2, y, w, 1 + 2 * z); } ctx.restore(); };
  // rowboat hull, side view, waterline at (x,y), length L
  M.boat = (ctx, x, y, L, rot, fill, rim, rimA) => { ctx.save(); ctx.translate(x, y); ctx.rotate(rot || 0); const h = L * 0.16;
    const path = () => { ctx.beginPath(); ctx.moveTo(-L * 0.54, -h); ctx.lineTo(L * 0.56, -h * 1.2); ctx.quadraticCurveTo(L * 0.42, h * 0.8, L * 0.2, h * 0.8); ctx.lineTo(-L * 0.3, h * 0.8); ctx.quadraticCurveTo(-L * 0.48, h * 0.55, -L * 0.54, -h); ctx.closePath(); };
    if (rim) { ctx.save(); ctx.shadowColor = C.rgba(rim, rimA ?? 0.6); ctx.shadowBlur = 16; ctx.fillStyle = C.rgba(rim, rimA ?? 0.6); path(); ctx.fill(); ctx.restore(); }
    ctx.fillStyle = fill; ctx.save(); ctx.scale(0.985, 0.95); path(); ctx.fill(); ctx.restore(); ctx.restore(); };
  // sailboat: hull + mast + sails (sail 0..1)
  M.sailboat = (ctx, x, y, L, rot, sail, fill, rim, rimA, t = 0, canvas = null) => { M.boat(ctx, x, y, L, rot, fill, rim, rimA); ctx.save(); ctx.translate(x, y); ctx.rotate(rot || 0);
    const mh = L * 1.05, h = L * 0.16; ctx.strokeStyle = fill; ctx.lineWidth = Math.max(3, L * 0.018); if (rim) { ctx.shadowColor = C.rgba(rim, (rimA ?? 0.6) * 0.8); ctx.shadowBlur = 12; }
    ctx.beginPath(); ctx.moveTo(-L * 0.02, -h); ctx.lineTo(-L * 0.02, -h - mh); ctx.stroke();
    if (sail > 0.01) { const top = -h - mh * 0.97, bot = -h - L * 0.08, sh = (bot - top) * sail, bil = Math.sin(t * 1.3) * L * 0.02;
      ctx.fillStyle = canvas ? C.rgba(canvas, 0.92) : fill; if (canvas) { ctx.shadowColor = C.rgba(canvas, 0.5); ctx.shadowBlur = 18; } ctx.beginPath(); ctx.moveTo(L * 0.0, bot - sh); ctx.quadraticCurveTo(L * 0.3 + bil, bot - sh * 0.45, L * 0.44, bot); ctx.lineTo(L * 0.0, bot); ctx.closePath(); ctx.fill();
      ctx.beginPath(); ctx.moveTo(-L * 0.04, bot - sh * 0.9); ctx.quadraticCurveTo(-L * 0.24 - bil * 0.5, bot - sh * 0.4, -L * 0.32, bot); ctx.lineTo(-L * 0.04, bot); ctx.closePath(); ctx.fill(); }
    ctx.restore(); };
  M.rain = (ctx, t, a, o = {}) => { if (a <= 0.01) return; const r = C.rng(o.seed || 9), n = o.n || 260, col = o.col || [180, 195, 220], ang = o.ang ?? 0.25, sp = o.speed || 1400, WW = W + 400;
    ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.lineCap = "round";
    for (let i = 0; i < n; i++) { const z = 0.3 + r() * 0.7, bx = r() * WW, by = r(); const y = ((by * (H + 200) + t * sp * z) % (H + 200)) - 100; const x = (((bx - (y + t * sp * z) * ang) % WW) + WW) % WW - 200; const L = 20 + 50 * z;
      ctx.strokeStyle = C.rgba(col, a * z * 0.35); ctx.lineWidth = 0.6 + 1.2 * z; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + L * ang, y - L); ctx.stroke(); } ctx.restore(); };
  // lightning intensity at T for strike times
  M.flash = (T, times) => { let f = 0; for (const s of times) { const d = T - s; if (d >= 0 && d < 1.2) f = Math.max(f, Math.exp(-d * 5) * (0.6 + 0.4 * Math.abs(Math.sin(d * 40)))); } return f; };
  M.bolt = (ctx, x, y0, y1, seed, a) => { if (a <= 0.02) return; const r = C.rng(seed); ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.strokeStyle = C.rgba([220, 230, 255], a); ctx.shadowColor = C.rgba([200, 215, 255], a); ctx.shadowBlur = 24; ctx.lineWidth = 3;
    ctx.beginPath(); let px = x, py = y0; ctx.moveTo(px, py); while (py < y1) { py += 20 + r() * 40; px += (r() - 0.5) * 70; ctx.lineTo(px, py); } ctx.stroke(); ctx.restore(); };
  M.bubbles = (ctx, t, x, y, a, o = {}) => { if (a <= 0.01) return; const r = C.rng(o.seed || 21), n = o.n || 14, rise = o.rise || 260, sp = o.speed || 60;
    ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.lineWidth = 1.5;
    for (let i = 0; i < n; i++) { const ph = ((t * sp / rise) * (0.6 + r() * 0.8) + r()) % 1, s = 2 + r() * 6 * (o.size || 1); const bx = x + (r() - 0.5) * (o.spread || 30) + Math.sin(t * 2 + i) * 8 * ph, by = y - ph * rise;
      ctx.strokeStyle = C.rgba(o.col || [190, 225, 255], a * (1 - ph) * 0.7); ctx.beginPath(); ctx.arc(bx, by, s, 0, 6.283); ctx.stroke(); } ctx.restore(); };
  // underwater light shafts from the surface line y0
  M.shafts = (ctx, t, a, y0, col = [150, 210, 255], n = 9) => { if (a <= 0.01) return; ctx.save(); ctx.globalCompositeOperation = "lighter";
    for (let i = 0; i < n; i++) { const x = 140 + i * 210 + Math.sin(t * 0.2 + i * 1.9) * 60, w = 40 + 30 * Math.sin(i * 2.3), al = a * (0.5 + 0.5 * Math.sin(t * 0.5 + i * 1.3)), L = 900, sk = 0.25;
      const g = ctx.createLinearGradient(0, y0, 0, y0 + L); g.addColorStop(0, C.rgba(col, 0.16 * al)); g.addColorStop(1, C.rgba(col, 0)); ctx.fillStyle = g;
      ctx.beginPath(); ctx.moveTo(x - w, y0); ctx.lineTo(x + w, y0); ctx.lineTo(x + w * 2.4 + L * sk, y0 + L); ctx.lineTo(x - w * 2.4 + L * sk, y0 + L); ctx.closePath(); ctx.fill(); } ctx.restore(); };
  // top-down swimmer: (x,y) center, ang = heading (radians, 0 = right), s scale, ph stroke phase
  M.swimTop = (ctx, x, y, s, ang, ph, fill, rim, rimA = 0.6, still = false) => { ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s);
    const a1 = still ? -1 : Math.sin(ph), a2 = still ? -1 : Math.sin(ph + Math.PI);
    const arm = (side, a) => { const sx = 22, sy = 12 * side; const ex = sx + 40 * a, ey = sy + side * (10 + 10 * (1 - Math.abs(a))); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey); };
    const body = () => { ctx.beginPath(); ctx.ellipse(0, 0, 30, 15, 0, 0, 6.283); ctx.moveTo(52, 0); ctx.arc(41, 0, 11, 0, 6.283); };
    const limbs = () => { ctx.beginPath(); arm(-1, a1); arm(1, a2); const k = still ? 0 : Math.sin(ph * 2) * 4; ctx.moveTo(-24, -7); ctx.lineTo(-62, -9 + k); ctx.moveTo(-24, 7); ctx.lineTo(-62, 9 - k); };
    ctx.lineCap = "round";
    if (rim) { ctx.save(); ctx.shadowColor = C.rgba(rim, rimA); ctx.shadowBlur = 16; ctx.fillStyle = C.rgba(rim, rimA); ctx.strokeStyle = C.rgba(rim, rimA); body(); ctx.fill(); ctx.lineWidth = 12; limbs(); ctx.stroke(); ctx.restore(); }
    ctx.fillStyle = fill; ctx.strokeStyle = fill; ctx.save(); ctx.scale(0.95, 0.9); body(); ctx.fill(); ctx.lineWidth = 8.5; limbs(); ctx.stroke(); ctx.restore(); ctx.restore(); };
  M.ripple = (ctx, t, x, y, a, col = [200, 230, 255], s = 1) => { if (a <= 0.01) return; ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.lineWidth = 2;
    for (let k = 0; k < 3; k++) { const ph = (t * 0.7 + k / 3) % 1; ctx.strokeStyle = C.rgba(col, a * (1 - ph) * 0.5); ctx.beginPath(); ctx.ellipse(x, y, (40 + ph * 90) * s, (40 + ph * 90) * s * 0.8, 0, 0, 6.283); ctx.stroke(); } ctx.restore(); };
  M.gull = (ctx, x, y, s, ph, fill = "#1a1210") => { const f = Math.sin(ph) * 0.6; ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.strokeStyle = fill; ctx.lineWidth = 2.6; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(-22, -10 * f - 4); ctx.quadraticCurveTo(-10, -14 * f - 8, 0, 0); ctx.quadraticCurveTo(10, -14 * f - 8, 22, -10 * f - 4); ctx.stroke(); ctx.restore(); };
  window.MAR = M;
})();
