/* Cinematic drawing helpers for the "Nadie va a venir" film. Pure functions of time: deterministic. */
(function () {
  const W = 1080, H = 1920;
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
      const bx = r() * 1400 - 160, by = C.lerp(o.y0, o.y1, r()), rw = 260 + r() * 380, rh = 90 + r() * 160;
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

  C.vignette = (ctx, a = 0.75) => {
    const g = ctx.createRadialGradient(W / 2, H * 0.48, H * 0.25, W / 2, H * 0.5, H * 0.78);
    g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(1, `rgba(0,0,0,${a})`);
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  };

  window.CINE = C;
})();
