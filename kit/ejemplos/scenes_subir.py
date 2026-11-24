S = []

COMMON = """
      const PTS = [[100,3560],[620,3560],[880,3220],[230,2870],[840,2520],[270,2170],[800,1820],[330,1470],[740,1120],[440,790],[560,430]];
      const SEG = []; let PL = 0;
      for (let i = 1; i < PTS.length; i++) { const l = Math.hypot(PTS[i][0]-PTS[i-1][0], PTS[i][1]-PTS[i-1][1]); SEG.push(l); PL += l; }
      const at = (d) => { d = C.clamp(d, 0, PL); for (let i = 0; i < SEG.length; i++) { if (d <= SEG[i]) { const k = d / SEG[i]; return [PTS[i][0] + (PTS[i+1][0]-PTS[i][0])*k, PTS[i][1] + (PTS[i+1][1]-PTS[i][1])*k, Math.sign(PTS[i+1][0]-PTS[i][0]) || 1]; } d -= SEG[i]; } return [PTS[PTS.length-1][0], PTS[PTS.length-1][1], 1]; };
      const keys = (K, T) => { if (T <= K[0][0]) return K[0][1]; for (let i = 1; i < K.length; i++) if (T <= K[i][0]) { const k = (T - K[i-1][0]) / (K[i][0] - K[i-1][0]); return C.lerp(K[i-1][1], K[i][1], K[i-1][2] ? C.ease(k) : k); } return K[K.length-1][1]; };
      // hero distance along the path (world px)
      const HK = [[6.84,470,0],[17.04,1700,0],[22.0,2400,0],[27.83,3300,0],[33.5,4250,0],[38.5,4560,1],[48.7,4560,1],[50.9,4500,1],[68.84,4500,1],[77.0,5644,1]];
      const heroD = (T) => keys(HK, T);
      const moving = (T) => Math.abs(heroD(T + 0.05) - heroD(T - 0.05)) > 0.5;
      const STOP = [null, 17.04, 20.54, 23.19, 27.83];
      const folD = (i, T) => { const s = STOP[i]; const d = heroD(Math.min(T, s)) - 80 * i; return d; };
      const folMoving = (i, T) => T < STOP[i] && moving(T);
      // light of day: sunset -> night -> dawn
      const warmK = [[0,0.62,1],[12,0.45,1],[24,0.12,1],[31,0,1],[63,0,1],[70,0.25,1],[80,1,1]];
      const warm = (T) => keys(warmK, T);
      const sky = (T, camY, z) => {
        const w = warm(T), night = 1 - C.clamp(w * 1.6);
        const g = ctx.createLinearGradient(0, 0, 0, 1920);
        g.addColorStop(0, C.rgba(C.mixc([4, 6, 16], [26, 28, 60], w), 1));
        g.addColorStop(0.55, C.rgba(C.mixc([12, 16, 32], [150, 80, 70], w), 1));
        g.addColorStop(0.8, C.rgba(C.mixc([28, 34, 56], [255, 160, 96], w), 1));
        g.addColorStop(1, C.rgba(C.mixc([18, 20, 30], [120, 70, 60], w), 1));
        ctx.fillStyle = g; ctx.fillRect(0, 0, 1080, 1920);
        if (night > 0.02) { const r = C.rng(777); for (let i = 0; i < 160; i++) { const x = r() * 1080, y = ((r() * 2400 - camY * 0.05 * z) % 1500 + 1500) % 1500, s = 0.6 + r() * 1.8, tw = 0.6 + 0.4 * Math.sin(T * 1.3 + i); ctx.fillStyle = "rgba(225,232,255," + (0.65 * night * tw * r()) + ")"; ctx.beginPath(); ctx.arc(x, y, s, 0, 6.283); ctx.fill(); } }
      };
      const ranges = (T, camY, z) => {
        const w = warm(T);
        const off = (k) => 1250 - (camY - 2400) * 0.12 * k * z;
        [[0.4, [20, 24, 40], [60, 40, 50], 7], [0.8, [12, 14, 24], [34, 22, 28], 11]].forEach(([k, c1, c2, seed]) => {
          const r = C.rng(seed), y0 = off(k) + k * 220; ctx.fillStyle = C.rgba(C.mixc(c1, c2, w), 1);
          ctx.beginPath(); ctx.moveTo(-50, 2000); let x = -50; ctx.lineTo(x, y0);
          while (x < 1130) { x += 90 + r() * 140; ctx.lineTo(x, y0 - r() * 260 * k - 40); }
          ctx.lineTo(1130, 2000); ctx.closePath(); ctx.fill();
        });
      };
      const cam = (fx, fy, z, sy) => { ctx.translate(540, sy); ctx.scale(z, z); ctx.translate(-fx, -fy); };
      const MT = [[560,400],[640,560],[700,700],[780,920],[840,1100],[900,1400],[980,1700],[1080,2100],[1200,2600],[1400,3200],[1700,3700],[1700,4400],[-600,4400],[-600,3700],[-300,3200],[-100,2600],[30,2100],[140,1700],[230,1400],[300,1100],[360,920],[420,700],[480,560]];
      const JN = 5, MJ = []; { const r = C.rng(55); for (let i = 0; i < MT.length; i++) { const a = MT[i], b = MT[(i + 1) % MT.length]; for (let k = 0; k < JN; k++) { const f = k / JN; const amp = (k === 0 || a[1] > 3500) ? 0 : Math.min(28, 6 + (a[1] - 380) * 0.02); MJ.push([C.lerp(a[0], b[0], f) + (r() - 0.5) * 2 * amp, C.lerp(a[1], b[1], f) + (r() - 0.5) * amp]); } } }
      const mountain = (T) => {
        const w = warm(T);
        ctx.fillStyle = C.rgba(C.mixc([10, 12, 18], [22, 14, 16], w), 1);
        ctx.beginPath(); MJ.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.closePath(); ctx.fill();
        // lit face (right side) gradient
        ctx.save(); ctx.beginPath(); MJ.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.closePath(); ctx.clip();
        // rock strata and snow streaks
        { const r = C.rng(321); for (let i = 0; i < 260; i++) { const y = 420 + Math.pow(r(), 1.3) * 3300, x = 560 + (r() - 0.5) * (200 + (y - 400) * 0.9); const right = x > 560 + (y - 400) * 0.02;
            const len = 30 + r() * 90, ang = right ? 0.95 + r() * 0.3 : Math.PI - 0.95 - r() * 0.3; const snow = C.clamp(1 - (y - 450) / 1300);
            ctx.strokeStyle = right ? C.rgba(C.mixc([120, 135, 170], [255, 190, 140], w), 0.07 + 0.22 * snow * r()) : C.rgba([0, 0, 0], 0.35); ctx.lineWidth = 2 + r() * 3;
            ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.cos(ang) * len, y + Math.sin(ang) * len); ctx.stroke(); } }
        const g = ctx.createLinearGradient(560, 400, 1300, 900);
        g.addColorStop(0, C.rgba(C.mixc([60, 70, 100], [180, 110, 80], w), 0.22)); g.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = g; ctx.fillRect(-600, 380, 2400, 4100);
        // snow cap
        const sg = ctx.createLinearGradient(0, 400, 0, 1500);
        sg.addColorStop(0, C.rgba(C.mixc([150, 165, 200], [255, 205, 170], w), 0.28)); sg.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = sg; ctx.fillRect(-600, 380, 2400, 1200);
        ctx.restore();
        // rim along the ridges
        ctx.strokeStyle = C.rgba(C.mixc([170, 190, 235], [255, 200, 140], w), 0.45); ctx.lineWidth = 3;
        ctx.beginPath(); for (let i = 0; i <= 10 * JN; i++) { const [x, y] = MJ[i]; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke();
        ctx.strokeStyle = C.rgba(C.mixc([170, 190, 235], [255, 200, 140], w), 0.18); ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(560, 400); for (let i = MJ.length - 1; i >= 15 * JN; i--) { const [x, y] = MJ[i]; ctx.lineTo(x, y); } ctx.stroke();
        // trail
        ctx.setLineDash([8, 14]); ctx.strokeStyle = "rgba(220,225,240,0.13)"; ctx.lineWidth = 3;
        ctx.beginPath(); PTS.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.stroke(); ctx.setLineDash([]);
      };
      const lightTrail = (d0, k, T) => {
        if (k <= 0.01) return; const n = 40;
        for (let i = 0; i < n; i++) { const f = i / (n - 1); if (f > k) break; const d = C.lerp(d0, PL, f); const [x, y] = at(d); const a = (1 - f * 0.5) * (0.6 + 0.4 * Math.sin(T * 3 - i * 0.6));
          C.glow(ctx, x, y - 4, 26, [255, 205, 150], 0.35 * a); ctx.fillStyle = "rgba(255,238,210," + 0.8 * a + ")"; ctx.beginPath(); ctx.arc(x, y - 4, 3, 0, 6.283); ctx.fill(); }
      };
      const sitter = (x, y, h, dir, rim, rimA) => {
        const s = h / 180; ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s);
        const path = () => { ctx.beginPath(); ctx.arc(-4, -112, 15, 0, 6.283); ctx.roundRect(-24, -96, 42, 56, [14, 14, 6, 6]);
          ctx.roundRect(-22, -50, 70, 18, 8); ctx.roundRect(34, -50, 16, 50, 6); ctx.roundRect(4, -86, 12, 44, 5); };
        ctx.save(); ctx.shadowColor = C.rgba(rim, rimA); ctx.shadowBlur = 20; ctx.fillStyle = C.rgba(rim, rimA); path(); ctx.fill(); ctx.restore();
        ctx.fillStyle = "#050506"; ctx.save(); ctx.scale(0.965, 0.985); path(); ctx.fill(); ctx.restore(); ctx.restore();
      };
      const lantern = (x, y, a, T, i, boost) => {
        if (a <= 0.01) return; const fl = 0.85 + 0.15 * Math.sin(T * 9 + i * 3) * Math.sin(T * 4.3 + i);
        C.glow(ctx, x, y - 14, 150 * (1 + 0.5 * boost), [255, 190, 120], (0.35 + 0.3 * boost) * a * fl);
        C.glow(ctx, x, y - 14, 40, [255, 225, 170], 0.8 * a * fl);
        ctx.fillStyle = "#060505"; ctx.fillRect(x - 7, y - 24, 14, 22); ctx.fillRect(x - 3, y - 30, 6, 6);
        ctx.fillStyle = "rgba(255,226,170," + a * fl + ")"; ctx.fillRect(x - 4, y - 21, 8, 14);
      };
      const HS = [88, 83, 86, 81, 84];
      const people = (T, o) => {
        o = o || {};
        for (let i = 4; i >= 1; i--) {
          const d = folD(i, T), [x, y, dir] = at(d), sat = T > STOP[i] + 0.7;
          const lt = C.ease(C.prog(T, STOP[i] + 0.9, STOP[i] + 1.8));
          const boost = o.boost || 0;
          if (sat) { lantern(x + 26 * dir, y, lt, T, i, boost); sitter(x - 6 * dir, y, HS[i], -dir, C.mixc([170, 185, 220], [255, 200, 140], 0.4 + 0.6 * lt), 0.55); }
          else C.person(ctx, x, y, HS[i], { fill: "#050506", rim: C.mixc([180, 195, 230], [255, 200, 140], warm(T)), rimA: 0.6, walk: folMoving(i, T) ? T * 8 + i : null });
        }
        const [hx, hy] = at(heroD(T));
        C.person(ctx, hx, hy, HS[0], { fill: "#040405", rim: o.heroRim || C.mixc([200, 212, 240], [255, 205, 150], warm(T)), rimA: o.heroA || 0.85, walk: moving(T) ? T * 8 : null });
        if (o.wave > 0.01) { const s = HS[0] / 180, sw = Math.sin(T * 5) * 0.22 * o.wave, ang = Math.PI * (1 - o.wave) + 0.35 * o.wave + sw;
          ctx.save(); ctx.translate(hx + 25 * s, hy - 132 * s); ctx.rotate(ang); ctx.strokeStyle = "#040405"; ctx.lineCap = "round"; ctx.lineWidth = 11 * s; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, -60 * s); ctx.stroke(); ctx.restore(); }
        return [hx, hy];
      };
      const fogBand = (T, y0, y1, a, seed) => C.fog(ctx, T, { y0, y1, n: 9, alpha: a, seed, color: C.mixc([110, 120, 150], [255, 190, 150], warm(T)), drift: 14 });
      const wind = (T, a) => { if (a > 0.01) C.dust(ctx, T, { n: 120, alpha: 0.5 * a, seed: 2024, warm: 0, speed: 1.2, wind: 260, streak: 36 }); };
"""

def world(start, camjs, extra_before="", extra_after="", people_opts="{}", screen_after=""):
    return COMMON + f"""
      const T = t + {start};
      const HP = at(heroD(T));
{camjs}
      sky(T, CY, CZ);
      ranges(T, CY, CZ);
      ctx.save(); cam(CX, CY, CZ, CS);
{extra_before}
      mountain(T);
      const OP = {people_opts};
      people(T, OP);
{extra_after}
      ctx.restore();
{screen_after}
"""

TT = "opacity: 0, y: 24, filter: \"blur(14px)\" }, { opacity: 1, y: 0, filter: \"blur(0px)\", duration: 0.8, ease: \"power3.out\" }"

# A: base of the mountain, sunset, the group (0 - 11.7)
S.append(("sa", 0.0, 11.7, 0.0, """
    <div id="sa-k" class="kick" style="top:300px">UN GRUPO · UNA MONTAÑA</div>
    <div id="sa-t" class="title" style="top:300px; font-size:120px">Todos juntos.</div>
""", world(0.0, """
      const pk = C.ease(C.prog(T, 0.5, 10.5));
      const CZ = C.lerp(0.52, 1.75, pk), CS = C.lerp(900, 830, pk);
      const CX = C.lerp(560, C.lerp(430, HP[0], 0.5), pk), CY = C.lerp(2150, HP[1] - 30, pk);
""", extra_before="""
      C.sun(ctx, 1010, 1330, 64, 1, null);
""", extra_after="""
      fogBand(T, 3520, 3700, 0.25, 31);
""", screen_after="""
      C.dust(ctx, T, { n: 60, alpha: 0.35, seed: 41, warm: 0.9, speed: 0.3 });
"""), """
    gsap.set("#sa-t", { opacity: 0 });
    tl.fromTo("#sa-k", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 0.4);
    tl.to("#sa-k", { opacity: 0, duration: 0.35 }, 2.9);
    tl.fromTo("#sa-t", { """ + TT + """, 3.37);
    tl.to("#sa-t", { opacity: 0, filter: "blur(10px)", duration: 0.4 }, 7.2);
"""))

# B: it gets steep, cold; the first one stays (11.1 - 19.9)
S.append(("sb", 11.1, 8.8, 0.6, """
    <div id="sb-t" class="title" style="top:300px; font-size:108px">«Yo me quedo<br>aquí.»</div>
""", world(11.1, """
      const CZ = 1.6, CS = 1040;
      const CX = C.lerp(540, HP[0], 0.45), CY = HP[1] + 140;
""", extra_after="""
      fogBand(T, HP[1] - 200, HP[1] + 400, 0.18 * C.ease(C.prog(T, 12, 15)), 32);
""", screen_after="""
      wind(T, C.ease(C.prog(T, 12.5, 14.5)));
"""), """
    gsap.set("#sb-t", { opacity: 0 });
    tl.fromTo("#sb-t", { """ + TT + """, 5.94);
    tl.to("#sb-t", { opacity: 0, filter: "blur(10px)", duration: 0.4 }, 7.9);
"""))

# C: more stop, one by one (19.3 - 30.8)
S.append(("sc", 19.3, 11.5, 0.6, """
    <div id="sc-k" class="kick" style="top:300px">NO QUIEREN LO MISMO QUE TÚ</div>
    <div id="sc-t" class="title" style="top:300px; font-size:100px">…o no lo quieren<br>todavía.</div>
""", world(19.3, """
      const zz = C.ease(C.prog(T, 19.3, 30.8));
      const CZ = C.lerp(1.45, 1.05, zz), CS = 1000;
      const CX = C.lerp(540, HP[0], 0.4), CY = HP[1] + C.lerp(220, 420, zz);
""", extra_after="""
      fogBand(T, HP[1] - 300, HP[1] + 600, 0.16, 33);
""", screen_after="""
      wind(T, 0.8);
"""), """
    gsap.set("#sc-t", { opacity: 0 });
    tl.fromTo("#sc-k", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 6.8);
    tl.to("#sc-k", { opacity: 0, duration: 0.3 }, 8.3);
    tl.fromTo("#sc-t", { """ + TT + """, 8.53);
    tl.to("#sc-t", { opacity: 0, filter: "blur(10px)", duration: 0.4 }, 10.6);
"""))

# D: alone; pull back to see the lanterns below; then the summit (30.2 - 42.8)
S.append(("sd", 30.2, 12.6, 0.6, """
    <div id="sd-t" class="title" style="top:300px; font-size:150px">Solo tú.</div>
    <div id="sd-k" class="kick" style="top:300px">LO QUE FALTA POR SUBIR</div>
""", world(30.2, """
      const out = C.ease(C.prog(T, 31.0, 35.5)), up = C.ease(C.prog(T, 37.3, 41.5));
      const CZ = C.lerp(C.lerp(1.15, 0.52, out), 0.9, up);
      const CS = C.lerp(1000, 820, out);
      const CX = C.lerp(C.lerp(HP[0], 560, out), 560, up);
      const CY = C.lerp(C.lerp(HP[1] + 200, 2050, out), 1050, up);
""", extra_after="""
      fogBand(T, 2000, 3300, 0.12, 34);
""", screen_after="""
      wind(T, 0.6 + 0.4 * C.ease(C.prog(T, 36.2, 37.0)) * (1 - C.ease(C.prog(T, 38.5, 40))));
"""), """
    gsap.set(["#sd-t", "#sd-k"], { opacity: 0 });
    tl.fromTo("#sd-t", { opacity: 0, scale: 0.94, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.8, ease: "power3.out" }, 4.93);
    tl.to("#sd-t", { opacity: 0, filter: "blur(10px)", duration: 0.35 }, 6.9);
    tl.fromTo("#sd-k", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 7.24);
    tl.to("#sd-k", { opacity: 0, duration: 0.3 }, 8.8);
"""))

# E: the temptation to go back (42.2 - 52.4)
S.append(("se", 42.2, 10.2, 0.6, """
    <div id="se-k1" class="kick" style="top:300px">VOLVER A LO CONOCIDO</div>
    <div id="se-k2" class="kick" style="top:300px">VOLVER A ENCAJAR</div>
    <div id="se-t" class="title" style="top:300px; font-size:110px">Muy tentador.</div>
""", world(42.2, """
      const k = C.ease(C.prog(T, 42.2, 52.4));
      const CZ = C.lerp(1.7, 1.25, k), CS = C.lerp(760, 640, k);
      const CX = C.lerp(560, HP[0], 0.6), CY = HP[1];
""", people_opts="{ boost: 0.4 * C.ease(C.prog(T, 44, 47)) }", screen_after="""
      wind(T, 0.5);
"""), """
    gsap.set(["#se-k1", "#se-k2", "#se-t"], { opacity: 0 });
    tl.fromTo("#se-k1", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 3.41);
    tl.to("#se-k1", { opacity: 0, duration: 0.3 }, 4.9);
    tl.fromTo("#se-k2", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 5.04);
    tl.to("#se-k2", { opacity: 0, duration: 0.3 }, 6.4);
    tl.fromTo("#se-t", { """ + TT + """, 7.85);
    tl.to("#se-t", { opacity: 0, filter: "blur(10px)", duration: 0.4 }, 9.6);
"""))

# F: not wrong, just different; a faint trail of light appears upward (51.8 - 64.6)
S.append(("sf", 51.8, 12.8, 0.6, """
    <div id="sf-t" class="title" style="top:300px; font-size:96px">no significa que<br>estés equivocado.</div>
    <div id="sf-t2" class="title" style="top:300px; font-size:120px; color:#ffe2bf">al principio.</div>
""", world(51.8, """
      const k = C.ease(C.prog(T, 51.8, 64.6));
      const CZ = C.lerp(1.25, 0.95, k), CS = 900;
      const CX = C.lerp(HP[0], 560, 0.4 + 0.3 * k), CY = HP[1] - 160 * k;
""", extra_after="""
      lightTrail(heroD(T) + 30, C.ease(C.prog(T, 57.44, 62.8)), T);
""", screen_after="""
      wind(T, 0.35);
"""), """
    gsap.set(["#sf-t", "#sf-t2"], { opacity: 0 });
    tl.fromTo("#sf-t", { """ + TT + """, 3.07);
    tl.to("#sf-t", { opacity: 0, filter: "blur(10px)", duration: 0.4 }, 5.6);
    tl.fromTo("#sf-t2", { """ + TT + """, 11.46);
"""))

# G: you can love them, and still keep going (64.0 - 71.4)
S.append(("sg", 64.0, 7.4, 0.6, """
    <div id="sg-t" class="title" style="top:300px; font-size:100px; color:#ffe2bf">Y aun así…<br>seguir subiendo.</div>
""", world(64.0, """
      const k = C.ease(C.prog(T, 64.0, 71.4));
      const CZ = C.lerp(0.62, 1.2, k), CS = C.lerp(700, 900, k);
      const CX = C.lerp(560, HP[0], k * 0.5), CY = C.lerp(1700, HP[1] - 80, k);
""", extra_after="""
      lightTrail(heroD(T) + 30, 1, T);
""", people_opts="{ boost: C.ease(C.prog(T, 64.3, 65.5)) * (1 - 0.6 * C.ease(C.prog(T, 68, 70))), wave: C.ease(C.prog(T, 65.6, 66.2)) * (1 - C.ease(C.prog(T, 67.3, 67.8))) }"), """
    gsap.set("#sg-t", { opacity: 0 });
    tl.fromTo("#sg-t", { """ + TT + """, 3.76);
"""))

# H: summit at dawn, sea of clouds (70.8 - 84.0)
S.append(("sh", 70.8, 13.2, 0.7, """
    <div id="sh-k" class="kick" style="top:300px; color:#ffe2bf">NO TODOS VAN A SUBIR CONTIGO</div>
    <div id="sh-t" class="title" style="top:300px; font-size:112px; color:#fff1de">Sube de todas<br>formas.</div>
""", world(70.8, """
      const k = C.ease(C.prog(T, 70.8, 84));
      const CZ = C.lerp(1.15, 0.9, k), CS = C.lerp(980, 1060, k);
      const CX = C.lerp(HP[0], 560, 0.5 + 0.5 * k), CY = HP[1] - 20;
""", extra_before="""
      { const rise = C.ease(C.prog(T, 72, 82)); C.sun(ctx, 830, C.lerp(1000, 740, rise), 46, 0.4 + 0.6 * rise, null); C.rays(ctx, 830, C.lerp(1000, 740, rise), T, 0.5 * rise, 9, 1400); }
""", extra_after="""
      fogBand(T, 1150, 1600, 0.28, 35);
      fogBand(T, 1350, 1900, 0.35, 36);
""", screen_after="""
      C.dust(ctx, T, { n: 80, alpha: 0.4, seed: 42, warm: 1, speed: 0.3 });
"""), """
    gsap.set(["#sh-k", "#sh-t"], { opacity: 0 });
    tl.fromTo("#sh-k", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 5.73);
    tl.to("#sh-k", { opacity: 0, duration: 0.35 }, 7.6);
    tl.fromTo("#sh-t", { opacity: 0, scale: 0.92, filter: "blur(22px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 1.0, ease: "power3.out" }, 7.88);
"""))

CUES = [(0.00,2.79,"Imagina que un grupo decide subir una montaña."),(3.37,6.39,"Todos juntos. Riendo. Con ganas."),
(6.84,8.57,"Los primeros pasos son fáciles."),(9.03,10.64,"Todos caminan al mismo ritmo."),(11.12,13.07,"Pero el camino empieza a empinarse."),
(13.53,15.28,"Hace frío. Duele."),(15.75,17.85,"Y alguien dice: «Yo me quedo aquí.»"),(19.48,22.70,"Más arriba, otro se detiene. Luego otro."),
(23.19,24.93,"No porque sean malas personas."),(25.28,27.38,"Solo… no quieren lo mismo que tú."),(27.83,29.29,"O no lo quieren todavía."),
(30.65,34.01,"Y de pronto miras a tu alrededor… y ya no hay nadie."),(35.13,38.76,"Solo tú. El viento. Y lo que falta por subir."),
(39.20,41.25,"Ahí es donde casi todos regresan."),(42.49,45.19,"Porque bajar significa volver a estar acompañado."),
(45.61,48.28,"Volver a lo conocido. Volver a encajar."),(48.73,50.94,"Y es tentador. Muy tentador."),(52.12,52.97,"Pero escucha esto."),
(53.45,57.01,"Que se queden atrás… no significa que tú estés equivocado."),(57.44,59.72,"Significa que elegiste algo diferente."),
(60.14,63.88,"Y lo diferente casi siempre se camina solo… al principio."),(64.37,67.33,"Puedes quererlos. Puedes agradecerles el camino."),
(67.76,69.89,"Y aun así… seguir subiendo."),(71.05,73.92,"Porque allá arriba hay algo que ellos no van a ver."),(74.30,76.11,"Y que tú necesitas ver."),
(76.53,78.26,"No todos van a subir contigo."),(78.68,80.43,"Sube de todas formas.")]
