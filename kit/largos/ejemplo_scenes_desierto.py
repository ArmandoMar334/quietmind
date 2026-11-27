import json as _json
_T = _json.load(open('/home/claude/vL01_desierto/timing.json'))
_CH = _T['chapters']
TOTAL_S = _T['total']
LEAD = 1.0
S = []

PRE = """
      const D = window.DES, W = 1920, H = 1080;
      const T = t - __OFF__;
      const P = (a, b) => C.ease(C.prog(T, a, b));
      const K = (k) => D.keys(k, T), KC = (k) => D.kc(k, T);
"""

TT = 'opacity: 0, y: 20, filter: "blur(14px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.9, ease: "power3.out" }'

# ---------------------------------------------------------------- CH0 intro: night, endless dunes
ST0 = """
      const HZ = 600;
      const warm = P(31, 38) * 0.35;
      D.sky(ctx, HZ, [3, 5, 12], KC([[0,[10,16,34]],[38,[26,22,40]]]), C.mixc([40, 52, 86], [150, 96, 70], warm));
      D.stars(ctx, T, 1 - 0.3 * warm, 11, 320, HZ, T * 0.004);
      D.moon(ctx, 1540, 170, 26, 0.85);
      if (warm > 0.01) C.glow(ctx, 360, HZ + 30, 700, [255, 150, 80], 0.35 * warm);
      // camera: slow descent and push in
      const z = K([[0,1.0],[13,1.06],[14.2,1.0],[37,1.08]]);
      const camY = K([[0,-60],[13,0],[14.2,0],[37,10]]);
      ctx.save(); ctx.translate(960, 640); ctx.scale(z, z); ctx.translate(-960, -640 + camY);
      const cam = T * 22;
      const L1 = D.dune(ctx, { base: HZ + 40, amps: [70, 30], freqs: [0.0021, 0.0063], phases: [1, 2], off: cam * 0.25, top: [16, 20, 34], bot: [6, 7, 12], rim: [140, 160, 210], rimA: 0.25, depth: 300 });
      const L2 = D.dune(ctx, { base: HZ + 160, amps: [110, 40], freqs: [0.0016, 0.0051], phases: [3, 0.5], off: cam * 0.5, top: [12, 14, 24], bot: [4, 5, 8], rim: [150, 170, 220], rimA: 0.32, depth: 360 });
      C.fog(ctx, T, { seed: 4, n: 8, y0: HZ + 40, y1: HZ + 180, alpha: 0.18, color: [60, 70, 100], drift: 8 });
      // far walker (act 1) / close walker (act 2)
      const near = T > 14.0;
      const L3 = D.dune(ctx, { base: HZ + 330, amps: [150, 50, 14], freqs: [0.0012, 0.0041, 0.011], phases: [0.4, 1.8, 0.2], off: cam, top: [10, 11, 18], bot: [2, 2, 4], rim: [170, 185, 230], rimA: 0.42, rimW: 2.6, depth: 420 });
      if (!near) {
        const wx = C.lerp(700, 1180, C.prog(T, -1, 14)), wy = L2(wx);
        D.prints(ctx, L2, wx - 12, wx - 260, 0.6, 14);
        C.person(ctx, wx, wy + 2, 64, { fill: "#05060a", rim: [170, 185, 235], rimA: 0.55, walk: T * 6 });
      }
      ctx.restore();
      // close-up layer: the walker big in the foreground (loops past the same rock: going in circles)
      if (near) {
        const k = P(14.0, 15.2);
        const off = T * 120;
        const FG = (x) => D.ridge(x + off, { base: 950, amps: [90, 26], freqs: [0.0018, 0.006], phases: [2.2, 0.7] });
        // the same rock passes again and again (24-27)
        const loopA = P(23.6, 24.6) * (1 - P(27.2, 28.4));
        const rx = 2200 - ((T * 120 * 1.0) % 2600);
        if (loopA > 0.01) { ctx.save(); ctx.globalAlpha = loopA; D.rock(ctx, rx, FG(rx) + 20, 260, 150, "#040406", 7); ctx.restore(); }
        ctx.save(); ctx.globalAlpha = k;
        D.dune(ctx, { base: 950, amps: [90, 26], freqs: [0.0018, 0.006], phases: [2.2, 0.7], off: off, top: [13, 14, 22], bot: [1, 1, 2], rim: [180, 195, 240], rimA: 0.5, rimW: 3, depth: 300 });
        const wx = 820, wy = FG(wx);
        D.prints(ctx, FG, wx - 30, wx - 820, 0.9, 46);
        C.person(ctx, wx, wy + 4, 300, { fill: "#050608", rim: C.mixc([170, 185, 235], [255, 190, 130], warm * 2), rimA: 0.6, walk: T * 4.2 });
        ctx.restore();
      }
      D.wind(ctx, T, 0.35, { seed: 3, n: 90, y0: 640, y1: 1040, col: [170, 180, 210], speed: 260, len: 0.6 });
      C.dust(ctx, T, { n: 60, alpha: 0.18 + 0.2 * warm, seed: 4, warm: warm, speed: 0.25 });
"""

# ---------------------------------------------------------------- CH1 espejismo: amber afternoon, false lake
ST1 = """
      const HZ = 560;
      const lake = P(3.8, 7.5) * (1 - P(13.8, 17.4));
      const ghosts = P(21.0, 22.2) * (1 - P(31.2, 33.0));
      const stop = P(33.5, 36.0);
      D.sky(ctx, HZ, [24, 14, 16], [96, 52, 36], [214, 128, 70]);
      C.sun(ctx, 1500, 250, 44, 0.9);
      C.glow(ctx, 1500, HZ, 900, [255, 150, 70], 0.25);
      // camera follows the runner during the chase
      const run = P(11.6, 12.6) * (1 - P(16.6, 17.6));
      const speed = 40 + 260 * run;
      const xoff = K([[0,0],[11.6,0],[17.6,1000],[44,1300]]) + T * 30;
      // far mesas
      ctx.fillStyle = "#3a1f1a"; ctx.beginPath(); ctx.moveTo(0, HZ);
      for (let x = 0; x <= W; x += 20) { const xx = x + xoff * 0.1; ctx.lineTo(x, HZ - 30 - 46 * (0.5 + 0.5 * Math.sin(xx * 0.004 + 1)) * (Math.sin(xx * 0.0013) > 0.3 ? 1 : 0.2)); }
      ctx.lineTo(W, HZ); ctx.closePath(); ctx.fill();
      // the lake mirage on the horizon (shimmering mirror of the sky)
      if (lake > 0.01) { ctx.save(); ctx.globalAlpha = lake;
        const lx = 1260 - (xoff - K([[0,0],[11.6,0]])) * 0.0, lw = 760;
        for (let i = 0; i < 22; i++) { const y = HZ - 8 + i * 3.2, w = lw * (1 - i / 30) * (0.85 + 0.15 * Math.sin(T * 3 + i));
          const g = ctx.createLinearGradient(lx - w / 2, 0, lx + w / 2, 0); g.addColorStop(0, "rgba(255,220,180,0)"); g.addColorStop(0.5, C.rgba([255, 232, 205], 0.32 * (1 - i / 24))); g.addColorStop(1, "rgba(255,220,180,0)");
          ctx.fillStyle = g; ctx.fillRect(lx - w / 2 + Math.sin(T * 5 + i * 1.3) * 10, y, w, 2.4); }
        C.glow(ctx, lx, HZ + 20, 420, [255, 220, 190], 0.25);
        ctx.restore(); }
      D.heat(ctx, HZ - 10, HZ + 60, T, 1.2);
      const L1 = D.dune(ctx, { base: HZ + 90, amps: [60, 22], freqs: [0.0022, 0.007], phases: [0.5, 2], off: xoff * 0.35, top: [120, 66, 40], bot: [40, 22, 18], rim: [255, 200, 140], rimA: 0.35, depth: 260 });
      // the other mirages: a glowing screen, a golden summit, a crowd chasing a light
      if (ghosts > 0.01) { ctx.save(); ctx.globalCompositeOperation = "lighter";
        const a1 = ghosts * P(21.0, 22.4), a2 = ghosts * P(24.0, 25.2), a3 = ghosts * P(27.2, 28.4);
        const sh = (i) => Math.sin(T * 6 + i) * 4;
        // screen
        ctx.fillStyle = C.rgba([255, 230, 200], 0.22 * a1); ctx.strokeStyle = C.rgba([255, 240, 220], 0.55 * a1); ctx.lineWidth = 3;
        ctx.beginPath(); ctx.roundRect(420 + sh(1), HZ - 250, 120, 210, 16); ctx.fill(); ctx.stroke(); C.glow(ctx, 480, HZ - 145, 220, [255, 220, 180], 0.25 * a1);
        // golden summit with a flag
        ctx.fillStyle = C.rgba([255, 200, 120], 0.25 * a2); ctx.beginPath(); ctx.moveTo(840, HZ - 10); ctx.lineTo(960 + sh(2), HZ - 260); ctx.lineTo(1080, HZ - 10); ctx.closePath(); ctx.fill();
        ctx.strokeStyle = C.rgba([255, 225, 170], 0.6 * a2); ctx.beginPath(); ctx.moveTo(960 + sh(2), HZ - 260); ctx.lineTo(960 + sh(2), HZ - 330); ctx.stroke(); ctx.fillStyle = C.rgba([255, 225, 170], 0.6 * a2); ctx.fillRect(960 + sh(2), HZ - 330, 40, 24);
        C.glow(ctx, 960, HZ - 200, 260, [255, 200, 120], 0.25 * a2);
        // crowd walking toward a light
        C.glow(ctx, 1640, HZ - 60, 200, [255, 235, 210], 0.5 * a3);
        ctx.restore();
        ctx.save(); ctx.globalAlpha = a3; for (let i = 0; i < 7; i++) C.person(ctx, 1300 + i * 42 + ((T * 18) % 42), HZ + 4, 54 + (i % 3) * 6, { fill: "#2a1612", walk: T * 6 + i }); ctx.restore(); }
      const xs = 0;
      const FG = (x) => D.ridge(x + xoff, { base: 930, amps: [120, 30], freqs: [0.0015, 0.0052], phases: [1.4, 0.2] });
      D.dune(ctx, { base: 930, amps: [120, 30], freqs: [0.0015, 0.0052], phases: [1.4, 0.2], off: xoff, top: [70, 36, 24], bot: [12, 6, 6], rim: [255, 205, 150], rimA: 0.55, rimW: 3, depth: 320 });
      // the traveler: walks, runs to the lake, stops, then turns away
      const wx = K([[0,520],[11.6,600],[17.6,900],[33.5,900],[44,820]]), wy = FG(wx);
      D.prints(ctx, FG, wx - 30, wx - 700, 0.8, 40);
      const turned = T > 35.0;
      const lean = 0.18 * run;
      C.person(ctx, wx, wy + 4, 280, { fill: "#0b0606", rim: [255, 200, 140], rimA: 0.65, walk: T * (4 + 6 * run) * (1 - stop), lean: lean, flip: turned });
      D.wind(ctx, T, 0.3, { seed: 8, n: 70, y0: 600, y1: 1040, col: [255, 210, 160], speed: 220, len: 0.5 });
      C.dust(ctx, T, { n: 70, alpha: 0.28, seed: 6, warm: 1, speed: 0.3 });
"""

# ---------------------------------------------------------------- CH2 sol del mediodía: harsh noon, the one who rushes and the one who waits
ST2 = """
      const HZ = 560;
      const eve = P(24.5, 44.0);               // sun goes down while the wise one waits
      const sunX = C.lerp(960, 1600, eve), sunY = C.lerp(90, HZ - 40, Math.pow(eve, 1.4));
      D.sky(ctx, HZ, C.mixc([22, 22, 28], [20, 14, 26], eve), C.mixc([110, 104, 96], [120, 60, 46], eve), C.mixc([200, 186, 162], [236, 140, 78], eve));
      C.glow(ctx, sunX, sunY, 700, C.mixc([255, 246, 225], [255, 150, 70], eve), 0.38);
      C.sun(ctx, sunX, sunY, 52, 1.0, HZ);
      D.heat(ctx, HZ - 20, HZ + 120, T, 2.0 * (1 - eve));
      const L1 = D.dune(ctx, { base: HZ + 70, amps: [50, 18], freqs: [0.0024, 0.008], phases: [2, 1], off: 0, top: C.mixc([120, 100, 80], [110, 60, 38], eve), bot: C.mixc([56, 44, 36], [34, 18, 16], eve), rim: [255, 240, 210], rimA: 0.3, depth: 240 });
      const FGo = { base: 920, amps: [80, 20], freqs: [0.0013, 0.006], phases: [0.6, 2.4] };
      const FG = (x) => D.ridge(x, FGo);
      D.dune(ctx, Object.assign({ off: 0, top: C.mixc([74, 60, 48], [64, 32, 22], eve), bot: C.mixc([14, 11, 10], [10, 5, 5], eve), rim: C.mixc([255, 245, 225], [255, 190, 120], eve), rimA: 0.5, rimW: 3, depth: 300 }, FGo));
      // rock arch on the right that throws shade
      const rx = 1480, ry = FG(rx) + 30;
      const shLen = C.lerp(160, 520, eve);
      ctx.save(); ctx.fillStyle = "rgba(0,0,0,0.55)"; ctx.beginPath(); ctx.ellipse(rx - shLen * 0.5 * (sunX > rx ? 1 : -1) , ry - 8, shLen, 28, 0, 0, 6.283); ctx.fill(); ctx.restore();
      D.rock(ctx, rx, ry, 360, 300, "#120c0a", 5);
      ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.strokeStyle = C.rgba(C.mixc([255, 240, 220], [255, 170, 100], eve), 0.35); ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(rx, ry - 160, 120, Math.PI * 1.15, Math.PI * 1.75); ctx.stroke(); ctx.restore();
      // A: the one who rushes (walks hard, then collapses at 12.6)
      const fall = P(12.4, 14.2);
      const ax = K([[0,260],[12.4,640],[44,640]]);
      const aA = 1 - P(22.0, 24.0);
      if (aA > 0.01) { ctx.save(); ctx.globalAlpha = aA;
        D.prints(ctx, FG, ax - 30, ax - 600, 0.7, 34);
        C.person(ctx, ax, FG(ax) + 4 + 70 * fall, 250 * (1 - 0.35 * fall), { fill: "#0c0a09", rim: [255, 248, 230], rimA: 0.55, walk: T * 7 * (1 - fall), lean: 0.25 + 1.0 * fall });
        ctx.restore(); }
      // B: the one who knows: walks in at 16.5, sits in the shade, stands at dusk
      const bIn = P(16.3, 17.3);
      if (bIn > 0.01) { ctx.save(); ctx.globalAlpha = bIn;
        const bx = K([[16.3,1040],[19.0,1360],[44,1360],[49,1500]]), sit = P(19.0, 20.0) * (1 - P(44.0, 45.0));
        const walking = (T > 16.3 && T < 19.0) || T > 45.0;
        C.person(ctx, bx, FG(bx) + 8 + 48 * sit, 250 * (1 - 0.32 * sit), { fill: "#080606", rim: C.mixc([255, 240, 220], [255, 180, 110], eve), rimA: 0.6, walk: walking ? T * 4 : null, flip: false });
        ctx.restore(); }
      // time-lapse hint: shadows racing (24-44)
      D.wind(ctx, T, 0.22, { seed: 12, n: 60, y0: 620, y1: 1040, col: [255, 240, 220], speed: 180, len: 0.5 });
      C.dust(ctx, T, { n: 60, alpha: 0.22 + 0.15 * eve, seed: 9, warm: 0.4 + 0.6 * eve, speed: 0.25 });
"""

# ---------------------------------------------------------------- CH3 la noche: day burns, night freezes, the storm; don't decide at night
ST3 = """
      const HZ = 590;
      const night = P(0.5, 6.0);
      const day = P(14.6, 15.4) * (1 - P(17.4, 18.4));         // "días en los que puedes con todo"
      const storm = P(23.6, 25.4) * (1 - P(31.8, 35.0));
      const dawn = P(35.8, 41.5) * 0.6;
      const lit = Math.max(1 - night, day);
      D.sky(ctx, HZ, C.mixc(C.mixc([4, 6, 14], [40, 20, 22], lit), [20, 16, 34], dawn), C.mixc(C.mixc([12, 18, 40], [200, 90, 50], lit), [70, 44, 60], dawn), C.mixc(C.mixc([40, 60, 100], [255, 170, 90], lit), [210, 120, 90], dawn));
      if (lit > 0.01) C.sun(ctx, 960, C.lerp(HZ + 60, 220, day) + (1 - day) * C.lerp(300, 0, 1 - night) , 50, lit, HZ);
      D.stars(ctx, T, (1 - lit) * (1 - storm * 0.9) * (1 - dawn), 21, 340, HZ, T * 0.006);
      D.moon(ctx, 420, 160, 22, (1 - lit) * (1 - storm) * (1 - dawn));
      if (dawn > 0.01) C.glow(ctx, 1500, HZ + 20, 800, [255, 150, 90], 0.5 * dawn);
      const cold = (1 - lit);
      const L1 = D.dune(ctx, { base: HZ + 60, amps: [60, 20], freqs: [0.002, 0.0074], phases: [1.2, 0.3], off: 0, top: C.mixc([150, 80, 44], [20, 26, 44], cold), bot: C.mixc([60, 28, 18], [6, 8, 14], cold), rim: C.mixc([255, 200, 140], [170, 200, 255], cold), rimA: 0.3, depth: 260 });
      const FGo = { base: 930, amps: [70, 24], freqs: [0.0016, 0.0058], phases: [2.0, 1.0] };
      const FG = (x) => D.ridge(x, FGo);
      D.dune(ctx, Object.assign({ off: 0, top: C.mixc([110, 56, 32], [14, 18, 30], cold), bot: C.mixc([20, 10, 6], [2, 3, 6], cold), rim: C.mixc([255, 205, 150], [190, 215, 255], cold), rimA: 0.55, rimW: 3, depth: 320 }, FGo));
      // frost glitter on the sand at night
      if (cold > 0.2) { const r = C.rng(41); ctx.save(); ctx.globalCompositeOperation = "lighter"; for (let i = 0; i < 160; i++) { const x = r() * W, y = FG(x) + 10 + r() * 140; const tw = Math.max(0, Math.sin(T * 3 + i * 1.7)); ctx.fillStyle = C.rgba([200, 225, 255], 0.5 * cold * tw * tw * (1 - storm)); ctx.fillRect(x, y, 2, 2); } ctx.restore(); }
      // the traveler: standing tall in the day, sitting hunched at night, holding still in the storm with a small light
      const px = 900, py = FG(px);
      const hunch = Math.max(P(17.6, 18.8) * (1 - P(23.0, 24.0)), storm, P(35.5, 36.5) * 0) ;
      const crouch = storm;
      const lamp = P(26.0, 27.5) * (1 - dawn * 0.6);
      if (lamp > 0.01) C.glow(ctx, px + 70, py - 40, 260, [255, 190, 110], 0.5 * lamp);
      // breath vapor in the cold
      if (cold > 0.4 && storm < 0.5) { const ph = (T * 0.45) % 1; C.soft(ctx, px + 40 + ph * 60, py - 260 * (1 - 0.3 * hunch) - ph * 20, 30 + ph * 40, 18 + ph * 20, [200, 215, 240], 0.18 * (1 - ph) * cold); }
      C.person(ctx, px, py + 6 + 70 * hunch, 300 * (1 - 0.36 * hunch), { fill: "#06070a", rim: C.mixc(C.mixc([255, 200, 140], [170, 195, 255], cold), [255, 190, 120], lamp * 0.6), rimA: 0.6, lean: 0.35 * hunch });
      if (lamp > 0.01) { ctx.save(); ctx.fillStyle = C.rgba([255, 220, 160], 0.95 * lamp); ctx.fillRect(px + 64, py - 52 + 70 * hunch * 0.3, 12, 18); ctx.restore(); }
      // the storm: walls of sand
      if (storm > 0.01) { ctx.save(); ctx.fillStyle = C.rgba([70, 60, 70], 0.35 * storm); ctx.fillRect(0, 0, W, H); ctx.restore();
        C.fog(ctx, T, { seed: 13, n: 14, y0: 200, y1: 1000, alpha: 0.45 * storm, color: [90, 80, 90], drift: 220 });
        D.wind(ctx, T, 1.4 * storm, { seed: 17, n: 320, y0: 0, y1: H, col: [200, 180, 170], speed: 1600, len: 1.6 }); }
      D.wind(ctx, T, 0.25, { seed: 19, n: 60, y0: 640, y1: 1040, col: [190, 210, 240], speed: 200, len: 0.5 });
      C.dust(ctx, T, { n: 60, alpha: 0.18 + 0.2 * dawn, seed: 14, warm: Math.max(lit, dawn), speed: 0.2 });
"""

# ---------------------------------------------------------------- CH4 las dunas se mueven: time-lapse of shifting dunes; walk with the wind
ST4 = """
      const HZ = 560;
      const lapse = K([[0,0.25],[5.0,1.0],[15.5,1.0],[17.0,2.4],[26,2.4],[28,0.6],[43,0.5]]);
      // accumulated phase of the dunes (integral approximated by piecewise sum)
      const ph = T * 0.9 + 1.6 * P(5, 15.5) * 10 + 2.4 * P(17, 26) * 9 + 0.6 * P(28, 43) * 15;
      D.sky(ctx, HZ, [10, 10, 26], [52, 40, 76], [176, 120, 120]);
      D.stars(ctx, T, 0.35, 31, 200, HZ - 120, 0);
      C.glow(ctx, 960, HZ + 30, 900, [230, 150, 120], 0.25);
      const L1 = D.dune(ctx, { base: HZ + 60, amps: [70, 30], freqs: [0.0021, 0.0064], phases: [ph * 0.15, ph * 0.31 + 2], off: 0, top: [70, 50, 70], bot: [22, 16, 26], rim: [255, 200, 180], rimA: 0.3, depth: 240 });
      const L2 = D.dune(ctx, { base: HZ + 200, amps: [120, 40], freqs: [0.0016, 0.0049], phases: [ph * 0.25 + 1, -ph * 0.4], off: 0, top: [54, 38, 56], bot: [14, 10, 18], rim: [255, 205, 185], rimA: 0.38, depth: 320 });
      // spindrift: sand streaming off the crests
      { const r = C.rng(51); ctx.save(); ctx.globalCompositeOperation = "lighter";
        for (let i = 0; i < 26; i++) { const x0 = r() * W, y0 = L2(x0), len = 80 + r() * 200 * lapse; const g = ctx.createLinearGradient(x0, y0, x0 + len, y0 - 10); g.addColorStop(0, C.rgba([255, 215, 190], 0.18 * Math.min(1, lapse))); g.addColorStop(1, "rgba(255,215,190,0)"); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.quadraticCurveTo(x0 + len * 0.5, y0 - 30, x0 + len, y0 - 8 - r() * 20); ctx.lineTo(x0 + len, y0); ctx.closePath(); ctx.fill(); }
        ctx.restore(); }
      // foreground crest the walker treads on; it moves under his feet
      const FGo = { base: 900, amps: [100, 26, 10], freqs: [0.0014, 0.0055, 0.016], phases: [ph * 0.18 + 0.5, ph * 0.33, ph * 0.9] };
      const FG = (x) => D.ridge(x, FGo);
      D.dune(ctx, Object.assign({ off: 0, top: [40, 28, 40], bot: [6, 4, 8], rim: [255, 210, 190], rimA: 0.55, rimW: 3, depth: 320 }, FGo));
      // ripples on the foreground sand
      { ctx.save(); ctx.strokeStyle = "rgba(255,210,190,0.08)"; ctx.lineWidth = 2; for (let i = 0; i < 9; i++) { ctx.beginPath(); for (let x = 0; x <= W; x += 30) { const y = FG(x) + 40 + i * 22 + Math.sin(x * 0.03 + ph * 2 + i) * 4; if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); } ctx.stroke(); } ctx.restore(); }
      // the walker: short, firm steps (from 31.4), moving with the wind
      const steady = P(27.5, 29.5);
      const wx = K([[0,700],[27,760],[43,1080]]);
      const sway = Math.sin(T * 2.3) * 0.08 * (1 - steady) * Math.min(1, lapse);
      C.person(ctx, wx, FG(wx) + 4, 280, { fill: "#07050a", rim: [255, 205, 185], rimA: 0.6, walk: T * (3 + 2.5 * steady), lean: sway + 0.06 * steady });
      D.prints(ctx, FG, wx - 26, wx - 500, 0.7 * (0.4 + 0.6 * steady), 26);
      D.wind(ctx, T, 0.55 + 0.4 * Math.min(1.5, lapse) * 0.4, { seed: 23, n: 140, y0: 520, y1: 1060, col: [255, 215, 195], speed: 500 + 300 * lapse, len: 0.8 });
      C.dust(ctx, T, { n: 70, alpha: 0.25, seed: 15, warm: 0.7, speed: 0.4, wind: 40 });
"""

# ---------------------------------------------------------------- CH5 el oasis: palms, water, fire, rest without guilt
ST5 = """
      const HZ = 590;
      const reveal = P(2.6, 7.6);
      const kneel = P(11.6, 12.6) * (1 - P(15.0, 15.8));
      const sleep = P(15.2, 16.4) * (1 - P(42.6, 43.8));
      const fire = P(13.0, 16.0);
      D.sky(ctx, HZ, [3, 5, 14], [12, 20, 42], [36, 52, 84]);
      D.stars(ctx, T, 1, 61, 360, HZ, T * 0.012);
      D.moon(ctx, 1380, 150, 30, 1);
      const L1 = D.dune(ctx, { base: HZ + 50, amps: [50, 20], freqs: [0.0022, 0.007], phases: [0.2, 1.4], off: 0, top: [22, 28, 46], bot: [6, 8, 14], rim: [170, 195, 240], rimA: 0.28, depth: 240 });
      // camera eases in to the oasis
      const z = K([[0,1.0],[8,1.12],[44,1.2]]);
      ctx.save(); ctx.translate(960, 700); ctx.scale(z, z); ctx.translate(-960, -700);
      const GY = 820;
      // ground
      { const g = ctx.createLinearGradient(0, GY - 60, 0, H); g.addColorStop(0, "#0d1120"); g.addColorStop(1, "#010103"); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(-200, H + 200); for (let x = -200; x <= W + 200; x += 20) ctx.lineTo(x, GY - 40 * Math.sin(x * 0.0016 + 0.4) - 10); ctx.lineTo(W + 200, H + 200); ctx.closePath(); ctx.fill(); }
      // water pool with moon reflection
      ctx.save(); ctx.globalAlpha = reveal;
      ctx.fillStyle = "#0a1428"; ctx.beginPath(); ctx.ellipse(980, GY + 40, 360, 46, 0, 0, 6.283); ctx.fill();
      ctx.save(); ctx.beginPath(); ctx.ellipse(980, GY + 40, 360, 46, 0, 0, 6.283); ctx.clip(); ctx.globalCompositeOperation = "lighter";
      for (let i = 0; i < 12; i++) { const y = GY + 8 + i * 6, w = 50 + 14 * Math.sin(T * 2 + i); ctx.fillStyle = C.rgba([210, 225, 255], 0.22 * (1 - i / 12)); ctx.fillRect(1180 + Math.sin(T * 1.6 + i) * 8 - w / 2, y, w, 2); }
      if (fire > 0.01) for (let i = 0; i < 10; i++) { const y = GY + 10 + i * 6, w = 40 + 10 * Math.sin(T * 3 + i); ctx.fillStyle = C.rgba([255, 170, 90], 0.25 * fire * (1 - i / 10)); ctx.fillRect(740 + Math.sin(T * 2.6 + i) * 6 - w / 2, y, w, 2); }
      ctx.restore();
      // palms
      const sw = Math.sin(T * 0.7) * 0.03;
      D.palm(ctx, 640, GY + 10, 420, -0.18 + sw, "#03040a", [150, 175, 230], 0.35);
      D.palm(ctx, 1330, GY + 20, 480, 0.06 + sw * 0.8, "#03040a", [150, 175, 230], 0.35);
      D.palm(ctx, 1500, GY + 10, 330, 0.2 + sw * 1.2, "#03040a", [150, 175, 230], 0.3);
      D.palm(ctx, 470, GY + 20, 300, -0.32 + sw, "#03040a", [150, 175, 230], 0.3);
      ctx.restore();
      // fire
      D.fire(ctx, 760, GY + 30, T, fire, 1.0);
      // the traveler: arrives, kneels to drink, sleeps by the fire, stands again at the end
      const tx = K([[0,180],[11.4,860],[15.0,860],[16.4,640],[42.6,640],[44.4,690]]);
      const walking = (T < 11.4) || (T > 15.0 && T < 16.4) || T > 43.6;
      if (sleep > 0.5) { ctx.save(); ctx.fillStyle = "#05060a"; ctx.shadowColor = C.rgba([255, 170, 100], 0.6 * fire); ctx.shadowBlur = 16; ctx.beginPath(); ctx.ellipse(tx - 20, GY + 48, 120, 22, -0.03, 0, 6.283); ctx.fill(); ctx.beginPath(); ctx.arc(tx + 92, GY + 36, 18, 0, 6.283); ctx.fill(); ctx.restore(); }
      else C.person(ctx, tx, GY + 56 + 46 * kneel, 280 * (1 - 0.3 * kneel), { fill: "#05060a", rim: C.mixc([170, 195, 240], [255, 180, 110], fire), rimA: 0.6, walk: walking ? T * 4 : null, lean: 0.5 * kneel });
      ctx.restore();
      // fireflies / sparks
      if (fire > 0.01) { const r = C.rng(71); ctx.save(); ctx.globalCompositeOperation = "lighter"; for (let i = 0; i < 14; i++) { const ph = (T * (0.3 + r() * 0.3) + r()) % 1; ctx.fillStyle = C.rgba([255, 190, 110], 0.7 * fire * (1 - ph)); ctx.beginPath(); ctx.arc(760 + (r() - 0.5) * 60 + Math.sin(T + i) * 20, 820 - ph * 260, 2, 0, 6.283); ctx.fill(); } ctx.restore(); }
      C.dust(ctx, T, { n: 50, alpha: 0.15, seed: 16, warm: 0.3 * fire, speed: 0.15 });
"""

# ---------------------------------------------------------------- CH6 cierre: dawn, the end of the sand, looking back
ST6 = """
      const HZ = 580;
      const dawn = P(-1.0, 8.0);
      const sunUp = P(2.0, 40.0);
      const look = T > 8.2 && T < 26.8;
      const go = P(33.6, 46.0);
      const sunX = 1380, sunY = C.lerp(HZ + 40, HZ - 260, sunUp);
      D.sky(ctx, HZ, C.mixc([10, 10, 26], [36, 40, 78], dawn), C.mixc([60, 36, 60], [214, 124, 92], dawn), C.mixc([170, 100, 80], [255, 196, 130], dawn));
      D.stars(ctx, T, 0.5 * (1 - dawn), 81, 200, HZ - 100, 0);
      C.sun(ctx, sunX, sunY, 60, 1.0, HZ);
      C.rays(ctx, sunX, sunY, T, 0.6 * P(5, 14), 13, 1500);
      // the shore: a strip of sea and green at the end of the sand
      const shore = P(1.0, 5.0);
      if (shore > 0.01) { ctx.save(); ctx.globalAlpha = shore;
        const g = ctx.createLinearGradient(900, 0, 1920, 0); g.addColorStop(0, "rgba(255,214,160,0)"); g.addColorStop(0.35, "rgba(255,214,160,0.75)"); g.addColorStop(1, "rgba(255,200,150,0.5)");
        ctx.fillStyle = g; ctx.fillRect(900, HZ - 3, 1020, 9);
        ctx.save(); ctx.globalCompositeOperation = "lighter"; for (let i = 0; i < 8; i++) { const y = HZ + 8 + i * 5; ctx.fillStyle = C.rgba([255, 200, 140], 0.12 * (1 - i / 8)); ctx.fillRect(sunX - 160 + Math.sin(T * 2 + i) * 14, y, 320 - i * 20, 2); } ctx.restore();
        [[1120, 70, -0.1], [1170, 54, 0.15], [1560, 82, 0.05], [1610, 60, -0.2], [1760, 66, 0.12]].forEach(([x, h, l]) => D.palm(ctx, x, HZ + 2, h, l + Math.sin(T * 0.6 + x) * 0.03, "#2a1814"));
        ctx.restore(); }
      const L1 = D.dune(ctx, { base: HZ + 70, amps: [50, 18], freqs: [0.0022, 0.0075], phases: [0.8, 2.6], off: 0, top: [150, 84, 60], bot: [50, 26, 24], rim: [255, 214, 160], rimA: 0.4, depth: 240 });
      // camera pulls back while he looks at the road behind (the trail of lessons)
      const z = K([[0,1.12],[8,1.12],[14,0.96],[27,0.96],[33,1.04],[46,1.1]]);
      ctx.save(); ctx.translate(960, 800); ctx.scale(z, z); ctx.translate(-960, -800);
      const FGo = { base: 910, amps: [110, 26], freqs: [0.0014, 0.005], phases: [2.6, 0.8] };
      const FG = (x) => D.ridge(x, FGo);
      // the winding trail behind him across the far dunes, with five small lights (the lessons)
      const trail = P(9.0, 14.0) * (1 - go * 0.7);
      if (trail > 0.01) { ctx.save(); ctx.globalCompositeOperation = "lighter";
        const pt = (q) => [C.lerp(820, 60, q) + Math.sin(q * 9) * 90, C.lerp(FG(820) + 10, HZ + 90, Math.pow(q, 0.7))];
        for (let j = 0; j < 90; j++) { const q = j / 90, [x, y] = pt(q); ctx.fillStyle = C.rgba([255, 200, 140], 0.4 * trail * (1 - q * 0.6)); ctx.beginPath(); ctx.ellipse(x, y, 5 * (1 - q * 0.7), 2 * (1 - q * 0.7), 0, 0, 6.283); ctx.fill(); }
        const marks = [[0.86, 15.0], [0.68, 18.0], [0.5, 19.3], [0.32, 21.0], [0.16, 23.2]];
        marks.forEach(([q, t0], i) => { const a = P(t0, t0 + 0.8) * trail; if (a > 0.01) { const [x, y] = pt(q); C.glow(ctx, x, y - 6, 70 * (1 - q * 0.5), [255, 205, 150], 0.7 * a); } });
        ctx.restore(); }
      D.dune(ctx, Object.assign({ off: 0, top: [96, 52, 36], bot: [14, 8, 8], rim: [255, 220, 170], rimA: 0.6, rimW: 3, depth: 320 }, FGo));
      const wx = K([[0,820],[33.6,820],[46,1240]]);
      D.prints(ctx, FG, wx - 30, wx - 820, 0.8, 42);
      C.person(ctx, wx, FG(wx) + 4, 300, { fill: "#0a0605", rim: [255, 214, 160], rimA: 0.7, walk: T > 33.6 ? T * 4 : null, flip: look });
      ctx.restore();
      C.dust(ctx, T, { n: 80, alpha: 0.35, seed: 18, warm: 1, speed: 0.25 });
"""

STAGES = [ST0, ST1, ST2, ST3, ST4, ST5, ST6]

TITLES = {
    0: [("Lo que el desierto<br>te enseña", 1.2, 9.6, "font-size:96px", "kick", "QUIET MIND"),
        ("Es una escuela.", 33.9, None, "font-size:90px; color:#f1e2d0", None, None)],
    1: [("I · El espejismo", 0.0, 7.0, "font-size:84px; color:#ffe2bf", None, None),
        ("No todo lo que brilla<br>es agua.", 31.0, 44.7, "font-size:90px; color:#ffe2bf", None, None)],
    2: [("II · El sol del mediodía", 0.0, 7.0, "font-size:84px; color:#fff3e0", None, None),
        ("La prisa no te hace<br>llegar antes.", 45.0, None, "font-size:90px; color:#ffe2bf", None, None)],
    3: [("III · La noche", 0.0, 7.0, "font-size:84px; color:#e6ecff", None, None),
        ("No decidas<br>de noche.", 32.2, None, "font-size:96px; color:#e6ecff", None, None)],
    4: [("IV · Las dunas se mueven", 0.0, 7.0, "font-size:84px; color:#ffe2d6", None, None),
        ("Muévete con<br>el viento.", 39.6, None, "font-size:96px; color:#ffe2d6", None, None)],
    5: [("V · El oasis", 0.0, 7.0, "font-size:84px; color:#e6ecff", None, None),
        ("Descansar también<br>es parte del camino.", 27.0, None, "font-size:88px; color:#ffe2bf", None, None)],
    6: [("Más ligero. Más fuerte.<br>Más tú.", 28.2, 34.6, "font-size:88px; color:#fff1de", None, None),
        ("No estás perdido.<br>Estás cruzando.", 37.9, None, "font-size:100px; color:#fff1de", "kick", "QUIET MIND")],
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

_fix = {"esto lo quiero yo…": "¿esto lo quiero yo…", "por qué te sientes culpable cuando tú descansas?": "¿por qué te sientes culpable cuando tú descansas?"}
CUES = [(a, b, _fix.get(t, t)) for a, b, t in _T['cues']]
