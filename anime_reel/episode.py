"""LAAL JHOOTH — Part 1.  Code-only anime-style reel.  python episode.py [--preview] [--frames a:b]"""
import os, sys, math, subprocess, re
import numpy as np
from gfx import *
from chars import draw_char, blink_at, talk, CAST
import sets as SETS
import audio_kit as A
from lines import LINES

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
VOICE, SPEED = "hm_omega", 1.05

# ------------------------------------------------------------------ timeline
# (set, [(line_idx, pre_pause)], lead, tail)
SHOTS = [
    ("eyes",     [(0, 0.0), (1, 0.25)], 0.25, 0.35),
    ("terrace",  [(2, 0.0), (3, 0.4)], 0.2, 0.4),
    ("kitchen",  [(4, 0.0), (5, 0.45), (6, 0.15)], 0.2, 0.55),
    ("phone",    [(7, 0.0), (8, 0.35)], 0.25, 0.45),
    ("class",    [(9, 0.0), (10, 0.4)], 0.2, 0.5),
    ("corridor", [(11, 0.0), (12, 0.3), (13, 0.5)], 0.2, 0.55),
    ("busstop",  [(14, 0.0), (15, 0.3)], 0.25, 1.6),
    ("stranger", [(16, 0.0), (17, 0.45)], 0.35, 0.7),
    ("endcard",  [], 0.0, 2.8),
]

if os.environ.get("SHORT"):
    SHOTS = [s for s in SHOTS if s[0] in ("eyes", "kitchen", "class", "endcard")]

_vo = {}


def vo(i):
    if i not in _vo:
        _vo[i] = A.tts(LINES[i][0], voice=VOICE, speed=SPEED, cache_dir=CACHE)
    return _vo[i]


def build_timeline():
    tl, t = [], 0.0
    for name, lines, lead, tail in SHOTS:
        st = t
        lt = {}
        cur = t + lead
        for (i, pre) in lines:
            cur += pre
            d = len(vo(i)) / A.SR
            lt[i] = (cur - st, cur - st + d)
            cur += d
        end = cur + tail
        tl.append(dict(name=name, start=st, end=end, dur=end - st, L=lt))
        t = end
    return tl, t


# ------------------------------------------------------------------ text overlays
WHITE_TXT = dict(fill="#ffffff", stroke=7, stroke_fill="#141432", glow=12, glow_col="#9fc4ff")
RED_TXT = dict(fill="#ff3030", stroke=7, stroke_fill="#2a0004", glow=26, glow_col="#ff1a1a")
TRUE_TXT = dict(fill="#ffffff", stroke=4, stroke_fill="#2a3a5a", glow=30, glow_col="#e8f4ff")


def tspr(text, size, sty):
    return text_sprite(text, F_ANTON, size, sty["fill"], sty["stroke"], sty["stroke_fill"], sty["glow"], sty["glow_col"])


def comp_wipe(dst, spr, cx, cy, frac, alpha=1.0, dx=0):
    """composite with left->right reveal mask."""
    if frac <= 0:
        return
    h, w = spr.shape[:2]
    cut = int(w * clamp(frac))
    s = spr.copy()
    s[:, cut:, 3] = 0
    if cut < w:
        edge = slice(max(0, cut - 30), cut)
        s[:, edge, 3] *= np.linspace(1, 0, edge.stop - edge.start)[None, :]
    comp(dst, s, cx + dx, cy, alpha)


def speech(img, text, cx, cy, size, t, t_in, t_red=None, red_mode="glitch", fi=0, true=False, wipe_dur=0.45):
    """Floating spoken text. Turns red (lie) at t_red."""
    if t < t_in:
        return 0.0
    k = (t - t_in) / 0.32
    sc = 0.75 + 0.25 * back_out(k) if k < 1 else 1.0
    float_y = math.sin(t * 2.1) * 6
    base = tspr(text, size, TRUE_TXT if true else WHITE_TXT)
    red = tspr(text, size, RED_TXT)
    if sc != 1.0:
        comp(img, base, cx, cy + float_y, min(1, k * 2), scale=sc)
        return 0.0
    if t_red is None or t < t_red:
        comp_wipe(img, base, cx, cy + float_y, (t - t_in) / wipe_dur + 0.25)
        return 0.0
    r = t - t_red
    if red_mode == "slow":
        comp(img, base, cx, cy + float_y)
        comp_wipe(img, red, cx, cy + float_y, r / 1.1)
        return 0.6 * clamp(r / 1.1)
    # glitch flip
    if r < 0.4:
        rng = np.random.default_rng(fi)
        dx = int(rng.normal(0, 22))
        comp(img, red if (fi % 2 == 0 or r > 0.25) else base, cx + dx, cy + float_y + rng.normal(0, 6), scale=1 + 0.12 * (1 - r / 0.4))
        return 1.0 - r / 0.4
    pulse = 0.85 + 0.15 * math.sin(t * 9)
    jit = 0
    if (fi % 37) in (0, 1):
        jit = 14 * (1 if fi % 2 else -1)
    comp(img, red, cx + jit, cy + float_y, pulse)
    return 0.15 if jit else 0.0


CAP_Y = 1340


def caption_sprite(cap, size=58, maxw=900):
    key = (cap, size)
    if key in _capcache:
        return _capcache[key]
    words = cap.split()
    sprs = []
    for w in words:
        hl = "*" in w
        clean = w.replace("*", "")
        col = "#ffffff"
        if hl:
            col = "#ff3b3b" if re.search(r"LAAL|JHOOTH|BIJLI|SACH", clean.upper()) else "#ffd23f"
        sprs.append(text_sprite(clean, F_POPB, size, col, 6, "#000000", 0, None, 6))
    # wrap
    lines, cur, cw = [], [], 0
    space = size * 0.28
    for s in sprs:
        w = s.shape[1] - 12
        if cur and cw + space + w > maxw:
            lines.append(cur); cur, cw = [], 0
        cur.append(s); cw += (space if len(cur) > 1 else 0) + w
    if cur:
        lines.append(cur)
    lh = sprs[0].shape[0] - 18
    tw = int(maxw + 40); th = int(lh * len(lines) + 30)
    out = np.zeros((th, tw, 4), np.float32)
    for li, ln in enumerate(lines):
        total = sum(s.shape[1] - 12 for s in ln) + space * (len(ln) - 1)
        x = (tw - total) / 2
        for s in ln:
            y0 = int(li * lh + 6); x0 = int(x) - 6
            h, w = s.shape[:2]
            reg = out[y0:y0 + h, x0:x0 + w]
            a = s[..., 3:4]
            reg[..., :3] = reg[..., :3] * (1 - a) + s[..., :3] * a
            reg[..., 3:4] = reg[..., 3:4] * (1 - a) + a
            x += w - 12 + space
    _capcache[key] = out
    return out


_capcache = {}


def draw_caption(img, cap, t, t0, t1):
    if t < t0 - 0.05 or t > t1 + 0.3:
        return
    spr = caption_sprite(cap)
    k = (t - t0 + 0.05) / 0.18
    sc = 0.86 + 0.14 * back_out(k) if k < 1 else 1.0
    comp(img, spr, W / 2, CAP_Y, min(1.0, k * 1.5), scale=sc)


# ------------------------------------------------------------------ camera
class Cam:
    def __init__(self, keys):
        """keys: list of (t, zoom, cx, cy, cut[bool]) – cut=True snaps, else eases from previous."""
        self.keys = keys

    def at(self, t):
        ks = self.keys
        prev = ks[0]
        for k in ks[1:]:
            if t < k[0]:
                if len(k) > 4 and k[4]:
                    return prev[1:4]
                # ease towards k from prev over [prev.t, k.t]
                u = ease((t - prev[0]) / max(1e-3, k[0] - prev[0]))
                return tuple(a + (b - a) * u for a, b in zip(prev[1:4], k[1:4]))
            prev = k
        return prev[1:4]


def apply_cam(ctx, z, cx, cy, sx=0, sy=0):
    ctx.translate(W / 2 + sx, H / 2 + sy)
    ctx.scale(z, z)
    ctx.translate(-cx, -cy)


def paint_bg(ctx, bgsurf, z, cx, cy, sx, sy, par=0.55):
    ctx.save()
    zb = 1 + (z - 1) * par
    ctx.translate(W / 2 + sx * 0.6, H / 2 + sy * 0.6)
    ctx.scale(zb, zb)
    ctx.translate(-(W / 2 + (cx - W / 2) * par), -(H / 2 + (cy - H / 2) * par))
    ctx.translate(-(SETS.BW - W) / 2, -(SETS.BH - H) / 2)
    ctx.set_source_surface(bgsurf, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_BILINEAR)
    ctx.paint()
    ctx.restore()


def shake(t, t0, dur, amp, seed=1):
    if t < t0 or t > t0 + dur:
        return 0.0, 0.0
    d = 1 - (t - t0) / dur
    return noise1(t * 40, seed) * amp * d, noise1(t * 40, seed + 9) * amp * d


# ------------------------------------------------------------------ effects (cairo)
def rain(ctx, fi, n=160, col=(0.75, 0.82, 1.0), alpha=0.35, slant=0.18, seed=0):
    rng = np.random.default_rng(seed)
    xs = rng.uniform(-200, W + 200, n); ys = rng.uniform(0, H, n)
    sp = rng.uniform(70, 120, n); ln = rng.uniform(40, 110, n)
    ctx.set_line_width(2.2)
    for x, y, s, l in zip(xs, ys, sp, ln):
        yy = (y + fi * s) % (H + 200) - 100
        xx = x + yy * slant * -1
        ctx.move_to(xx, yy); ctx.line_to(xx + l * slant, yy - l)
    ctx.set_source_rgba(col[0], col[1], col[2], alpha); ctx.stroke()


def bolt(ctx, x0, y0, x1, y1, seed, alpha=1.0):
    rng = np.random.default_rng(seed)
    pts = [(x0, y0)]
    n = 14
    for i in range(1, n):
        u = i / n
        pts.append((x0 + (x1 - x0) * u + rng.normal(0, 55), y0 + (y1 - y0) * u + rng.normal(0, 10)))
    pts.append((x1, y1))
    for w, a in [(60, 0.08), (30, 0.18), (14, 0.5), (5, 1.0)]:
        ctx.move_to(*pts[0])
        for p in pts[1:]:
            ctx.line_to(*p)
        ctx.set_source_rgba(0.85, 0.9, 1, a * alpha); ctx.set_line_width(w)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
    # branches
    for b in range(3):
        i = rng.integers(3, n - 3)
        bx, by = pts[i]
        ctx.move_to(bx, by)
        for k in range(4):
            bx += rng.normal(60 * (1 if b % 2 else -1), 30); by += rng.uniform(30, 70)
            ctx.line_to(bx, by)
        ctx.set_source_rgba(0.85, 0.9, 1, 0.7 * alpha); ctx.set_line_width(3); ctx.stroke()


def roti(ctx, x, y, r, rot=0.0):
    ellipse(ctx, x, y, r, r * 0.42, rot)
    rad(ctx, x, y, 0, r, [(0, "#f2c27a"), (0.8, "#d99a4e"), (1, "#a8662e")]); ctx.fill()
    rng = np.random.default_rng(int(x * 7 + y))
    for k in range(6):
        ellipse(ctx, x + rng.normal(0, r * 0.4), y + rng.normal(0, r * 0.12), r * 0.12, r * 0.05)
        src(ctx, "#7a4418", 0.6); ctx.fill()


def heart(ctx, x, y, s, col="#ff4a6a", a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, 0.35)
    ctx.curve_to(-0.9, -0.3, -0.45, -0.95, 0, -0.45)
    ctx.curve_to(0.45, -0.95, 0.9, -0.3, 0, 0.35)
    src(ctx, col, a); ctx.fill()
    ctx.restore()


def sparkle(ctx, x, y, s, a=1.0, col="#ffffff"):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(0, -1), (0.18, -0.18), (1, 0), (0.18, 0.18), (0, 1), (-0.18, 0.18), (-1, 0), (-0.18, -0.18)])
    src(ctx, col, a); ctx.fill(); ctx.restore()


def speed_lines(ctx, cx, cy, fi, col=(1, 1, 1), a=0.25, n=60, r0=380):
    rng = np.random.default_rng(fi // 2)
    for k in range(n):
        ang = rng.uniform(0, 2 * math.pi)
        r1 = rng.uniform(r0, r0 + 200)
        r2 = r1 + rng.uniform(400, 900)
        w = rng.uniform(0.004, 0.012)
        ctx.move_to(cx + math.cos(ang - w) * r1, cy + math.sin(ang - w) * r1)
        ctx.line_to(cx + math.cos(ang) * r2, cy + math.sin(ang) * r2)
        ctx.line_to(cx + math.cos(ang + w) * r1, cy + math.sin(ang + w) * r1)
        ctx.close_path()
    ctx.set_source_rgba(col[0], col[1], col[2], a); ctx.fill()


# ------------------------------------------------------------------ shots
class Shot:
    set = None
    grade = (1, 1, 1)
    bloom = (0.75, 0.35)

    def __init__(self, info):
        self.i = info
        self.L = info["L"]
        self.dur = info["dur"]
        self.fx = {}

    def cam(self):
        return Cam([(0, 1.0, W / 2, H / 2)])

    def draw(self, ctx, t, fi):
        pass

    def overlay(self, img, t, fi):
        return dict()

    def shake_at(self, t):
        return (0.0, 0.0)

    def captions(self, img, t):
        items = sorted(self.L.items(), key=lambda kv: kv[1][0])
        for n, (i, (a, b)) in enumerate(items):
            nxt = items[n + 1][1][0] if n + 1 < len(items) else 1e9
            if t < nxt - 0.06:
                draw_caption(img, LINES[i][1], t, a, b)


def LT(shot, i, frac=0.0):
    a, b = shot.L[i]
    return a + (b - a) * frac


class Eyes(Shot):
    set = "void"
    bloom = (0.6, 0.6)

    def cam(self):
        return Cam([(0, 1.0, W / 2, 820), (self.dur, 1.16, W / 2, 840)])

    def draw(self, ctx, t, fi):
        red = ramp(t, LT(self, 1, 0.0) - 0.1, LT(self, 1, 0.3))
        st = dict(glow=red, look=(noise1(t * 0.8, 3) * 0.25, 0.05), blink=blink_at(t + 1.4), shock=0.0,
                  brow=-0.2, mouth=0)
        draw_char(ctx, "kabir", W / 2, 790, 2000, st)
        # red reflection band across the eyes
        if red > 0:
            lin(ctx, 0, 700, 0, 950, [(0, (1, 0, 0, 0)), (0.5, (1, 0.1, 0.1, 0.22 * red)), (1, (1, 0, 0, 0))])
            ctx.rectangle(0, 650, W, 350); ctx.fill()

    def overlay(self, img, t, fi):
        words = [("BAS 5 MINUTE", 220, 300, 64), ("MAIN THEEK HOON", 760, 260, 58), ("KAL PAKKA", 840, 1130, 70),
                 ("SACH MEIN!", 250, 1150, 66), ("I'M FINE", 560, 1560, 74)]
        g = 0.0
        for k, (w, x, y, s) in enumerate(words):
            t_in = 0.1 + k * 0.28
            if t < t_in:
                continue
            dx = math.sin(t * 0.9 + k) * 18
            a = min(1, (t - t_in) / 0.2) * (0.55 + 0.45 * abs(math.sin(t * 6 + k * 2)))
            spr = tspr(w, s, RED_TXT)
            jx = (np.random.default_rng(fi * 7 + k).normal(0, 10)) if (fi + k * 3) % 11 == 0 else 0
            comp(img, spr, x + dx + jx, y, a)
        red = ramp(t, LT(self, 1, 0.0) - 0.1, LT(self, 1, 0.3))
        flash = max(0.0, 1 - abs(t - LT(self, 1, 0.0)) / 0.12) * 0.7
        return dict(glitch=0.35 if (fi % 13 == 0) else 0.0, flash_red=flash, chroma=3 + 6 * red)


class Terrace(Shot):
    set = "terrace"
    bloom = (0.7, 0.55)
    grade = (0.85, 0.9, 1.15)

    def setup(self):
        self.strike = LT(self, 2, 0.72)

    def cam(self):
        self.setup()
        s = self.strike
        L3 = LT(self, 3, 0.0)
        return Cam([(0, 1.0, W / 2, 1000), (s, 1.12, W / 2, 980), (s + 0.01, 1.0, W / 2, 1000, True),
                    (L3, 1.0, W / 2, 1000), (L3 + 0.01, 2.0, W / 2, 1000, True), (self.dur, 2.15, W / 2, 1000)])

    def draw(self, ctx, t, fi):
        s = self.strike
        after = t >= s
        L3 = LT(self, 3, 0.0)
        flicker = (math.sin(t * 90) > 0.3) and after and t < s + 0.6
        st = dict(look=(0.0, -0.9) if not after else (0.0, 0.0), blink=0 if not after else blink_at(t, 2),
                  brow=0.5 if not after else -0.4, shock=1.0 if (after and t < L3) else 0.0,
                  glow=ramp(t, L3 + 0.9, L3 + 1.3), breathe=math.sin(t * 2.4))
        c = dict(CAST["kabir"]); c["streak"] = after
        draw_char(ctx, c, W / 2, 1040, 330, st)
        if after and t < s + 1.2:
            # electric aura
            rng = np.random.default_rng(fi)
            for k in range(10):
                x, y = W / 2 + rng.normal(0, 170), 1040 + rng.normal(0, 260)
                ctx.move_to(x, y)
                for j in range(4):
                    x += rng.normal(0, 30); y += rng.normal(0, 30); ctx.line_to(x, y)
            ctx.set_source_rgba(0.7, 0.85, 1, 0.8 * (1 - (t - s) / 1.2)); ctx.set_line_width(3); ctx.stroke()
        rain(ctx, fi, 200, alpha=0.3, seed=1)
        if s - 0.06 <= t < s + 0.25 or (s + 0.35 < t < s + 0.42):
            bolt(ctx, W / 2 + 260, -40, W / 2 + 15, 1040 - 0.6 * 330, int(t * 20))
        if 1.0 < t < 1.08:
            bolt(ctx, 100, -40, 260, 700, 77, 0.6)

    def overlay(self, img, t, fi):
        s = self.strike
        fl = 0.0
        if s - 0.02 <= t < s + 0.16:
            fl = 1.0
        elif s + 0.35 < t < s + 0.45:
            fl = 0.6
        elif 1.0 < t < 1.08:
            fl = 0.35
        L3 = LT(self, 3, 0.0)
        red = ramp(t, L3 + 0.9, L3 + 1.3)
        sx, sy = shake(t, s, 0.7, 30)
        return dict(flash_white=fl, shake=(sx, sy), chroma=8 if s <= t < s + 0.4 else red * 4,
                    glitch=0.6 if (L3 + 0.9 < t < L3 + 1.1) else 0)


def _terrace_shake(self, t):
    return shake(t, self.strike, 0.7, 30)


Terrace.shake_at = _terrace_shake


class Kitchen(Shot):
    def shake_at(self, t):
        a6 = LT(self, 6, 0.0)
        sx, sy = 0.0, 0.0
        for k in range(1, 4):
            dx, dy = shake(t, a6 + (k - 1) * 0.22 + 0.17, 0.15, 10, k)
            sx += dx; sy += dy
        return sx, sy

    set = "kitchen"
    grade = (1.05, 1.0, 0.92)

    def cam(self):
        a5 = LT(self, 5, 0.0) - 0.12
        a6 = LT(self, 6, 0.0) - 0.05
        return Cam([(0, 1.0, W / 2, 960), (a5, 1.06, W / 2, 940), (a5 + 0.01, 1.35, 640, 640, True),
                    (a6, 1.4, 640, 640), (a6 + 0.01, 1.25, W / 2, 1300, True), (self.dur, 1.32, W / 2, 1320)])

    def draw(self, ctx, t, fi):
        L4 = self.L[4]
        say_in = L4[0] + 1.0
        a6 = LT(self, 6, 0.0)
        st = dict(turn=-0.12, look=(-0.3, 0.1), mouth=talk(t, say_in, say_in + 1.0, 1), smile=0.6 if t > a6 else 0.4,
                  blink=blink_at(t, 1), brow=0.3, breathe=math.sin(t * 2), eyes_closed_happy=1.0 if t > a6 + 0.3 else 0.0)
        draw_char(ctx, "mummy", 620, 820, 360, st)
        # thali
        ellipse(ctx, W / 2, 1380, 330, 120)
        lin(ctx, W / 2 - 330, 0, W / 2 + 330, 0, [(0, "#8a96a6"), (0.45, "#f4f7fb"), (1, "#6b7786")]); ctx.fill()
        ellipse(ctx, W / 2, 1380, 280, 96); src(ctx, "#c9d1dc"); ctx.fill()
        n = 1 + sum(1 for k in range(4) if t > a6 + k * 0.22)
        for k in range(n):
            drop = 0.0
            if k > 0:
                tk = a6 + (k - 1) * 0.22
                drop = (1 - ease_out((t - tk) / 0.18)) * 500
            roti(ctx, W / 2 + (k % 2) * 14 - 7, 1370 - k * 22 - drop, 210, 0.04 * (k - 2))

    def overlay(self, img, t, fi):
        L4 = self.L[4]
        red_t = LT(self, 5, 0.0) - 0.1
        g = speech(img, "BAS EK ROTI AUR!", 560, 330, 104, t, L4[0] + 1.0, red_t, fi=fi)
        a6 = LT(self, 6, 0.0)
        sx, sy = (0, 0)
        for k in range(1, 4):
            dx, dy = shake(t, a6 + (k - 1) * 0.22 + 0.17, 0.15, 10, k)
            sx += dx; sy += dy
        return dict(glitch=g, chroma=g * 10, shake=(sx, sy), flash_red=0.35 * max(0, 1 - abs(t - red_t) / 0.1))


class Phone(Shot):
    set = "bedroom"

    def cam(self):
        b = LT(self, 8, 0.32)
        return Cam([(0, 1.0, W / 2, H / 2), (b, 1.08, W / 2, H / 2), (b + 0.01, 1.0, W / 2, H / 2, True),
                    (self.dur, 1.08, W / 2, 1000)])

    def draw(self, ctx, t, fi):
        b = LT(self, 8, 0.32)
        if t < b:
            self.draw_phone(ctx, t, fi)
        else:
            self.draw_bunty(ctx, t, fi)

    def draw_phone(self, ctx, t, fi):
        ctx.save()
        ctx.translate(W / 2, H / 2 - 40); ctx.rotate(-0.03 + math.sin(t) * 0.005)
        pw, ph = 760, 1480
        rrect(ctx, -pw / 2 - 16, -ph / 2 - 16, pw + 32, ph + 32, 90); src(ctx, "#0b0b10"); ctx.fill()
        rrect(ctx, -pw / 2, -ph / 2, pw, ph, 76)
        lin(ctx, 0, -ph / 2, 0, ph / 2, [(0, "#141a2e"), (1, "#0c1020")]); ctx.fill()
        # header
        src(ctx, "#1c2440"); ctx.rectangle(-pw / 2, -ph / 2 + 70, pw, 150); ctx.fill()
        ellipse(ctx, -pw / 2 + 110, -ph / 2 + 145, 46, 46); src(ctx, "#f2c14e"); ctx.fill()
        rrect(ctx, -pw / 2 + 25, -ph / 2 + 25, 0, 0, 0)
        ctx.restore()
        ctx.save()
        ctx.translate(W / 2, H / 2 - 40); ctx.rotate(-0.03 + math.sin(t) * 0.005)
        # notch
        rrect(ctx, -90, -ph / 2 + 18, 180, 36, 18); src(ctx, "#000000"); ctx.fill()
        # older messages (kabir's, right side)
        for k, (w, y) in enumerate([(420, -380), (300, -250)]):
            rrect(ctx, pw / 2 - 40 - w, y, w, 90, 34); src(ctx, "#2f6bff", 0.85); ctx.fill()
        ctx.restore()
        self._pt = t

    def draw_bunty(self, ctx, t, fi):
        b = LT(self, 8, 0.32)
        st = dict(blink=0.55 + 0.45 * (1 if (t * 1.3) % 2 < 0.25 else 0), mouth=0.25 + 0.15 * math.sin(t * 2), brow=-0.1,
                  look=(0.3, 0.4), breathe=math.sin(t * 1.5) * 2, sway=math.sin(t))
        draw_char(ctx, "bunty", 520, 900, 380, st)
        # blanket over shoulders
        smooth(ctx, [(60, 1900), (110, 1260), (300, 1120), (520, 1180), (740, 1110), (960, 1250), (1020, 1900)], True, 0.45)
        lin(ctx, 0, 1100, 0, 1900, [(0, "#6a4fb0"), (1, "#2e2160")]); ctx.fill()
        for k in range(6):
            ellipse(ctx, 200 + k * 140, 1500 + 40 * math.sin(k), 30, 30); src(ctx, "#f2c14e", 0.6); ctx.fill()
        # phone glow under face
        rrect(ctx, 430, 1150, 120, 200, 18); src(ctx, "#0b0b10"); ctx.fill()
        rad(ctx, 490, 1150, 0, 360, [(0, (0.6, 0.8, 1, 0.35)), (1, (0.6, 0.8, 1, 0))]); ctx.paint()
        # zzz
        for k in range(3):
            tt = (t * 0.8 + k * 0.33) % 1
            y = 520 - tt * 260; x = 820 + k * 30 + math.sin(tt * 6) * 20
            self._z = getattr(self, "_z", [])

    def overlay(self, img, t, fi):
        b = LT(self, 8, 0.32)
        g = 0.0
        if t < b:
            # header name + message bubble (text sprites)
            comp(img, text_sprite("BUNTY", F_POPB, 52, "#ffffff", 0, "#000000", 0, None, 4), 420, 330)
            comp(img, text_sprite("online", F_POP, 30, "#7ee2a8", 0, "#000000", 0, None, 4), 380, 380)
            t_in = self.L[7][0] + 0.9
            red_t = LT(self, 8, 0.0) - 0.05
            if t >= t_in:
                k = min(1, (t - t_in) / 0.22)
                isred = t >= red_t
                spr = text_sprite("bhai 5 MIN mein\npahuncha!!", F_POPB, 74,
                                  "#ffffff" if not isred else "#ffd0d0", 0, "#000000",
                                  0 if not isred else 0, None, 30, None, 4)
                h, w = spr.shape[:2]
                bub = np.zeros((h + 40, w + 60, 4), np.float32)
                col = (0.17, 0.2, 0.3) if not isred else (0.85, 0.08, 0.1)
                bub[..., :3] = col
                yy, xx = np.mgrid[0:bub.shape[0], 0:bub.shape[1]]
                r = 40
                cxm = np.clip(xx, r, bub.shape[1] - r); cym = np.clip(yy, r, bub.shape[0] - r)
                bub[..., 3] = (np.hypot(xx - cxm, yy - cym) <= r).astype(np.float32)
                y0, x0 = 20, 30
                reg = bub[y0:y0 + h, x0:x0 + w]
                a = spr[..., 3:4]
                reg[..., :3] = reg[..., :3] * (1 - a) + spr[..., :3] * a
                dx = 0
                if isred and t - red_t < 0.35:
                    dx = int(np.random.default_rng(fi).normal(0, 20))
                    g = 1 - (t - red_t) / 0.35
                comp(img, bub, 470 + dx, 880, k, scale=0.8 + 0.2 * back_out(k))
                if isred:
                    glow = tspr("LAAL", 1, RED_TXT)
                    comp(img, tspr("JHOOTH", 120, RED_TXT), 540, 1120, min(1, (t - red_t) / 0.2) * (0.85 + 0.15 * math.sin(t * 9)),
                         scale=1.0 + 0.1 * max(0, 1 - (t - red_t) / 0.3))
            return dict(glitch=g, chroma=g * 10, flash_red=0.3 * g)
        # bunty in bed: label + zzz
        comp(img, text_sprite("MEANWHILE BUNTY:", F_POPB, 48, "#ffd23f", 6, "#000000", 0, None, 8), W / 2, 230,
             min(1, (t - b) / 0.2))
        for k in range(3):
            tt = (t * 0.7 + k * 0.33) % 1
            comp(img, text_sprite("z", F_POPB, 70 + k * 16, "#ffffff", 5, "#2a2050", 0, None, 6),
                 800 + k * 40 + math.sin(tt * 6) * 18, 600 - tt * 280, math.sin(tt * math.pi))
        return dict()


class Classroom(Shot):
    def shake_at(self, t):
        return shake(t, LT(self, 10, 0.0) - 0.15, 0.9, 26, 3)

    set = "classroom"

    def cam(self):
        a10 = LT(self, 10, 0.0) - 0.1
        return Cam([(0, 1.0, W / 2, 980), (a10, 1.08, W / 2, 940), (a10 + 0.01, 1.45, W / 2, 620, True),
                    (self.dur, 1.6, W / 2, 600)])

    def draw(self, ctx, t, fi):
        L9 = self.L[9]
        a10 = LT(self, 10, 0.0)
        st = dict(mouth=talk(t, L9[0] + 1.1, L9[0] + 2.3, 4), smile=0.7, blink=blink_at(t, 4), brow=0.6,
                  breathe=math.sin(t * 2), sweat=ramp(t, a10, a10 + 0.4), look=(0.1, 0))
        draw_char(ctx, "sir", W / 2, 960, 340, st)
        # glasses glint
        g = ramp(t, L9[0] + 0.3, L9[0] + 0.6) * (1 - ramp(t, L9[0] + 0.6, L9[0] + 0.9))
        if g > 0:
            sparkle(ctx, W / 2 - 50, 960, 50 * g, g)
        # students' heads foreground
        for k, x in enumerate([90, 330, 620, 900]):
            hy = 1720 + 20 * math.sin(k * 2.1)
            if t > a10:
                hy += math.sin(t * 30 + k) * 6
            ellipse(ctx, x, hy, 150, 170); src(ctx, "#15131c"); ctx.fill()
            ellipse(ctx, x, hy + 260, 260, 160); src(ctx, "#1d2230"); ctx.fill()

    def overlay(self, img, t, fi):
        L9 = self.L[9]
        a10 = LT(self, 10, 0.0) - 0.15
        g = speech(img, "PAPER BAHUT\nEASY AAYEGA!", W / 2, 420, 110, t, L9[0] + 1.1, a10, fi=fi)
        sx, sy = shake(t, a10, 0.9, 26, 3)
        return dict(glitch=max(g, 0.3 if t > a10 and fi % 7 == 0 else 0), chroma=g * 12 + (3 if t > a10 else 0),
                    shake=(sx, sy), flash_red=0.5 * max(0, 1 - abs(t - a10) / 0.12), red_tint=0.25 * ramp(t, a10, a10 + 0.5))


class Corridor(Shot):
    set = "corridor"
    bloom = (0.7, 0.5)
    grade = (1.08, 1.0, 0.94)

    def cam(self):
        a12 = LT(self, 12, 0.0) - 0.05
        a13 = LT(self, 13, 0.0) - 0.08
        return Cam([(0, 1.0, W / 2, 1000), (a12, 1.06, W / 2, 990), (a12 + 0.01, 1.65, 790, 930, True),
                    (a13, 1.72, 790, 930), (a13 + 0.01, 1.7, 300, 930, True), (self.dur, 1.8, 300, 930)])

    def draw(self, ctx, t, fi):
        L11 = self.L[11]
        a12 = LT(self, 12, 0.0)
        a13 = LT(self, 13, 0.0)
        hap = t > a13 + 0.35
        st_k = dict(turn=0.28, look=(0.7, 0), mouth=talk(t, L11[0] + 1.2, L11[1] - 0.1, 2) * 0.6, blink=blink_at(t, 5),
                    brow=0.3 if t < a12 else (-0.2 if not hap else 0.4), shock=1.0 if (a12 + 0.6 < t < a13 + 0.35) else 0,
                    blush=1.0 if hap else 0.3, eyes_closed_happy=1.0 if hap else 0, smile=1.0 if hap else 0,
                    breathe=math.sin(t * 2.2), mouth_open=0)
        if hap:
            st_k["mouth"] = 0.7
        turn_away = ramp(t, a12 + 0.2, a12 + 0.5)
        st_m = dict(turn=-0.28 + 0.1 * turn_away, look=(-0.6 + 1.3 * turn_away, 0.1 * turn_away),
                    mouth=talk(t, a12 + 0.75, a12 + 1.6, 7) * 0.7, blink=blink_at(t, 6), brow=-0.5 if t > a12 else 0.0,
                    blush=0.4 + 0.8 * ramp(t, a12, a12 + 0.5), breathe=math.sin(t * 2.0 + 1), sway=math.sin(t * 1.3))
        draw_char(ctx, "meera", 790, 940, 300, st_m)
        draw_char(ctx, "kabir", 300, 960, 320, st_k)
        if hap:
            for k in range(7):
                tt = ((t - a13) * 0.9 + k / 7) % 1
                heart(ctx, 160 + k * 50 + math.sin(tt * 8 + k) * 30, 900 - tt * 420, 40 + 10 * (k % 3), "#ff4a6a",
                      math.sin(tt * math.pi))
            for k in range(5):
                sparkle(ctx, 120 + k * 80, 700 + 60 * math.sin(t * 3 + k), 18 + 8 * abs(math.sin(t * 5 + k)), 0.9)

    def overlay(self, img, t, fi):
        L11 = self.L[11]
        a12 = LT(self, 12, 0.0)
        a13 = LT(self, 13, 0.0) - 0.12
        g = 0.0
        if t < a12:
            speech(img, "MEERA... TUM MUJHE\nPASAND KARTI HO?", W / 2, 470, 82, t, L11[0] + 1.2, None, fi=fi)
        else:
            g = speech(img, "CHHI! BILKUL\nNAHI!", 700, 430, 118, t, a12 + 0.7, a13, fi=fi)
        return dict(glitch=g * 0.8, chroma=g * 8, flash_red=0.25 * max(0, 1 - abs(t - a13) / 0.1))


class BusStop(Shot):
    set = "busstop"
    bloom = (0.65, 0.6)
    grade = (0.9, 0.95, 1.1)

    def setup(self):
        self.red_t = self.L[15][1] + 0.15

    def cam(self):
        self.setup()
        a15 = LT(self, 15, 0.0)
        return Cam([(0, 1.0, W / 2, 1000), (a15, 1.05, 620, 960), (self.red_t, 1.25, 700, 860),
                    (self.dur, 1.45, 740, 820)])

    def draw(self, ctx, t, fi):
        a15 = LT(self, 15, 0.0)
        red = ramp(t, self.red_t, self.red_t + 1.0)
        st_s = dict(glow=red, breathe=math.sin(t * 1.2), mouth=talk(t, a15 + 0.9, a15 + 2.3, 9) * 0.4)
        draw_char(ctx, "stranger", 760, 830, 190, st_s)
        st_k = dict(turn=0.32, look=(0.8, -0.2), blink=blink_at(t, 8), brow=-0.3 if t < self.red_t else 0.6,
                    shock=1.0 if t > self.red_t + 0.3 else 0, breathe=math.sin(t * 2.6), sweat=red,
                    rim=(1, 0.2, 0.2) if red > 0 else None)
        draw_char(ctx, "kabir", 280, 1160, 360, st_k)
        rain(ctx, fi, 220, alpha=0.28, seed=4)
        # light flicker
        if t > self.red_t and (fi % 9 in (0, 1)):
            src(ctx, "#000000", 0.45); ctx.paint()

    def overlay(self, img, t, fi):
        a15 = LT(self, 15, 0.0)
        g = speech(img, "DARO MAT.\nMAIN INSAAN HOON.", 640, 430, 96, t, a15 + 0.95, self.red_t, red_mode="slow", fi=fi,
                   wipe_dur=0.9)
        red = ramp(t, self.red_t, self.red_t + 1.0)
        return dict(chroma=red * 5, red_tint=0.2 * red, glitch=0.5 if (t > self.red_t + 0.9 and fi % 11 == 0) else 0,
                    vignette_boost=red * 0.5)


class Stranger(Shot):
    set = "void"
    bloom = (0.55, 0.8)

    def setup(self):
        self.cut = LT(self, 17, 0.0) - 0.1

    def cam(self):
        self.setup()
        return Cam([(0, 1.0, W / 2, 900), (self.cut, 1.12, W / 2, 880), (self.cut + 0.01, 1.0, W / 2, 820, True),
                    (self.dur, 1.2, W / 2, 830)])

    def draw(self, ctx, t, fi):
        if t < self.cut:
            st = dict(glow=1.0, breathe=math.sin(t * 1.4) * 2, mouth=talk(t, LT(self, 16, 0.45), LT(self, 16, 0.95), 3) * 0.5)
            draw_char(ctx, "stranger", W / 2, 960, 1150, st)
        else:
            st = dict(shock=1.0, look=(0, 0), blink=0, brow=0.8, glow=0.0)
            draw_char(ctx, "kabir", W / 2, 790, 2000, st)
            # white reflection of the truth
            lin(ctx, 0, 700, 0, 950, [(0, (1, 1, 1, 0)), (0.5, (0.9, 0.95, 1, 0.18)), (1, (1, 1, 1, 0))])
            ctx.rectangle(0, 650, W, 350); ctx.fill()

    def overlay(self, img, t, fi):
        a16 = LT(self, 16, 0.42)
        if t < self.cut:
            speech(img, "TUM BHI DEKH\nSAKTE HO NA?", W / 2, 330, 112, t, a16, None, true=True, fi=fi, wipe_dur=0.7)
            return dict(vignette_boost=0.15, flash_white=0.0)
        k = t - self.cut
        return dict(flash_white=max(0, 0.9 - k * 5), vignette_boost=0.4, chroma=2)


class EndCard(Shot):
    set = "void"

    def draw(self, ctx, t, fi):
        src(ctx, "#000000"); ctx.paint()
        rad(ctx, W / 2, 900, 0, 900, [(0, (0.35, 0.0, 0.02, 0.8)), (1, (0, 0, 0, 0))]); ctx.paint()

    def captions(self, img, t):
        pass

    def overlay(self, img, t, fi):
        k = ramp(t, 0.0, 0.35)
        jit = int(np.random.default_rng(fi).normal(0, 14)) if (t < 0.4 or fi % 17 == 0) else 0
        comp(img, tspr("LAAL", 300, RED_TXT), W / 2 + jit, 760, k, scale=1.15 - 0.15 * ease_out(k))
        comp(img, tspr("JHOOTH", 190, WHITE_TXT), W / 2 - jit, 1000, ramp(t, 0.15, 0.45))
        comp(img, text_sprite("PART 1", F_POPB, 60, "#ff4a4a", 0, "#000000", 0, None, 6), W / 2, 1160, ramp(t, 0.4, 0.7))
        comp(img, text_sprite("Part 2 ke liye  FOLLOW  karo", F_POPB, 46, "#ffffff", 5, "#000000", 0, None, 6),
             W / 2, 1330, ramp(t, 0.9, 1.2) * (0.75 + 0.25 * math.sin(t * 5)))
        return dict(glitch=0.5 if t < 0.3 or fi % 17 == 0 else 0, chroma=6 if t < 0.3 else 1)


SHOT_CLASSES = dict(eyes=Eyes, terrace=Terrace, kitchen=Kitchen, phone=Phone, **{"class": Classroom},
                    corridor=Corridor, busstop=BusStop, stranger=Stranger, endcard=EndCard)

# ------------------------------------------------------------------ frame rendering
_bg_cache = {}


def get_bg(name):
    if name not in _bg_cache:
        arr = SETS.SETS[name]()
        _bg_cache[name] = np_to_surf(arr)
    return _bg_cache[name]


def make_shots():
    tl, total = build_timeline()
    shots = []
    for info in tl:
        sh = SHOT_CLASSES[info["name"]](info)
        sh.camobj = sh.cam()
        shots.append(sh)
    return shots, total


def render_frame(shots, fi):
    t_abs = fi / FPS
    sh = shots[-1]
    for s in shots:
        if s.i["start"] <= t_abs < s.i["end"]:
            sh = s
            break
    t = t_abs - sh.i["start"]
    surf, ctx = new_surface()
    z, cx, cy = sh.camobj.at(t)
    fx_shake = sh.shake_at(t)
    bgname = sh.set
    paint_bg(ctx, get_bg(bgname), z, cx, cy, *fx_shake)
    ctx.save()
    apply_cam(ctx, z, cx, cy, *fx_shake)
    sh.draw(ctx, t, fi)
    ctx.restore()
    img = surf_to_np(surf)
    fx = sh.overlay(img, t, fi) or {}
    sh.captions(img, t)
    # ---- post
    gr = np.array(sh.grade, np.float32)
    img = img * gr
    if fx.get("red_tint"):
        k = fx["red_tint"]
        img = img * (1 - k) + img * np.array([1.6, 0.55, 0.55], np.float32) * k
    thr, strength = sh.bloom
    img = bloom(np.clip(img, 0, 1), thr, strength)
    if fx.get("chroma"):
        img = chroma(img, fx["chroma"])
    if fx.get("glitch"):
        img = slice_glitch(img, fx["glitch"], fi)
    vig = vignette_mask()
    vb = fx.get("vignette_boost", 0)
    img = img * (vig if not vb else np.clip(vig - (1 - vig) * vb * 1.5, 0.05, 1))
    img = img + grain(fi) * 0.022
    if fx.get("flash_white"):
        img = img + (1 - img) * fx["flash_white"]
    if fx.get("flash_red"):
        k = fx["flash_red"]
        img = img * (1 - k) + np.array([1.0, 0.1, 0.12], np.float32) * k
    # shot fade-in from black for first frames of a few shots
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


# ------------------------------------------------------------------ audio
def tone(f, d, decay=1.2, harm=(1, 0.5, 0.25, 0.12), sr=A.SR):
    t = np.arange(int(d * sr)) / sr
    x = sum(a * np.sin(2 * np.pi * f * (i + 1) * t) * np.exp(-t * decay * (1 + i * 0.6)) for i, a in enumerate(harm))
    att = np.minimum(1, t / 0.006)
    return (x * att).astype(np.float32)


def note(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def music_lofi(dur, bpm=84, seed=2):
    sr = A.SR
    n = int(dur * sr)
    out = np.zeros(n + sr * 4, np.float32)
    beat = 60 / bpm
    prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]  # Am F C G
    bar = beat * 4
    rng = np.random.default_rng(seed)
    t = 0.0; bi = 0
    while t < dur:
        root, ch = prog[bi % 4]
        # bass
        b = tone(note(root - 12), bar, 1.4, (1, 0.3, 0.1))
        A.place(out, b * 0.5, t)
        # pad
        for m in ch:
            p = tone(note(m), bar, 0.5, (1, 0.2)) * 0.12
            A.place(out, p, t)
        # piano arpeggio 8ths
        arp = ch + [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12, ch[0] + 12]
        for k in range(8):
            mm = arp[k % len(arp)] + 12
            A.place(out, tone(note(mm), 1.2, 3.2, (1, 0.4, 0.15, 0.05)) * (0.2 + rng.uniform(-0.04, 0.04)), t + k * beat / 2)
        # soft drums
        for k in range(4):
            if k in (0, 2):
                A.place(out, _kick() * 0.55, t + k * beat)
            if k in (1, 3):
                A.place(out, _snare() * 0.25, t + k * beat)
            A.place(out, _hat() * 0.12, t + k * beat + beat / 2)
        t += bar; bi += 1
    return A._lp(out[:n], 5200).astype(np.float32)


def _kick():
    sr = A.SR
    t = np.arange(int(0.3 * sr)) / sr
    f = 50 + 90 * np.exp(-t * 30)
    return (np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 12)).astype(np.float32)


def _snare():
    sr = A.SR
    t = np.arange(int(0.2 * sr)) / sr
    nz = np.random.default_rng(3).standard_normal(len(t))
    return (A._bp(nz, 1500, 6000) * np.exp(-t * 22) * 0.8).astype(np.float32)


def _hat():
    sr = A.SR
    t = np.arange(int(0.05 * sr)) / sr
    nz = np.random.default_rng(4).standard_normal(len(t))
    return (A._hp(nz, 7000) * np.exp(-t * 90)).astype(np.float32)


def drone(dur, root=41.2, seed=5):
    sr = A.SR
    t = np.arange(int(dur * sr)) / sr
    x = np.zeros_like(t)
    for r, a in [(1, 0.5), (1.5, 0.25), (2, 0.25), (2.12, 0.18), (4.24, 0.06)]:
        x += a * np.sin(2 * np.pi * root * r * t + r) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * r * t))
    x += A._bp(np.random.default_rng(seed).standard_normal(len(t)), 200, 900) * 0.05
    return (A._lp(x, 1200) * 0.5).astype(np.float32)


def glitch_sfx(d=0.35, seed=1):
    sr = A.SR
    rng = np.random.default_rng(seed)
    n = int(d * sr)
    out = np.zeros(n, np.float32)
    i = 0
    while i < n:
        seg = int(rng.uniform(0.01, 0.04) * sr)
        kind = rng.integers(0, 3)
        tt = np.arange(seg) / sr
        if kind == 0:
            s = np.sign(np.sin(2 * np.pi * rng.uniform(200, 2400) * tt))
        elif kind == 1:
            s = rng.standard_normal(seg)
            s = np.round(s * 3) / 3
        else:
            s = np.zeros(seg)
        out[i:i + seg] = s[: n - i] * rng.uniform(0.3, 0.9)
        i += seg
    return (out * np.linspace(1, 0.3, n)).astype(np.float32)


def rain_bed(d, seed=3):
    nz = np.random.default_rng(seed).standard_normal(int(d * A.SR))
    x = A._bp(nz, 800, 7000) * 0.25 + A._lp(nz, 400) * 0.2
    return x.astype(np.float32)


def build_audio(shots, total, out_wav):
    sr = A.SR
    n = int((total + 1) * sr)
    voice = np.zeros(n, np.float32)
    for sh in shots:
        for i, (a, b) in sh.L.items():
            A.place(voice, vo(i), sh.i["start"] + a)
    S = {sh.i["name"]: sh for sh in shots}
    st = lambda nm: S[nm].i["start"]
    en = lambda nm: S[nm].i["end"]
    mus = np.zeros(n, np.float32)
    # hook: dark drone + riser
    d0 = en("terrace") if "terrace" in S else en("eyes")
    dr = drone(d0 + 0.5, 46.25)
    A.place(mus, dr * np.minimum(1, np.arange(len(dr)) / (0.3 * sr)), 0.0, 0.8)
    # comedy lofi from kitchen to end of corridor
    c0 = st("kitchen")
    c1 = en("corridor") if "corridor" in S else en([k for k in S if k != "endcard"][-1])
    lo = music_lofi(c1 - c0 + 0.6)
    fade = np.ones(len(lo), np.float32); fo = int(0.5 * sr); fade[-fo:] = np.linspace(1, 0, fo)
    fi_ = int(0.15 * sr); fade[:fi_] = np.linspace(0, 1, fi_)
    A.place(mus, lo * fade, c0, 0.9)
    # dread
    b0 = st("busstop") if "busstop" in S else st("endcard")
    dd = drone(total - b0 + 0.5, 36.7, 9)
    env = np.ones(len(dd), np.float32); env[: int(1.0 * sr)] = np.linspace(0, 1, int(1.0 * sr))
    A.place(mus, dd * env, b0, 1.0)
    # sfx
    fx = np.zeros(n, np.float32)

    def S_(name, at, g=1.0):
        A.place(fx, A.sfx(name).astype(np.float32), at, g)

    def G(at, g=0.7, seed=1, d=0.35):
        A.place(fx, glitch_sfx(d, seed), at, g)

    if "eyes" in S:
        e = S["eyes"]
        G(0.1, 0.35, 1, 0.25); G(e.i["start"] + LT(e, 1, 0.0) - 0.1, 0.6, 2)
        S_("riser", 0.0, 0.5)
        S_("boom", e.i["start"] + LT(e, 1, 0.0) - 0.05, 0.6)
    if "terrace" in S:
        tr = S["terrace"]
        A.place(fx, rain_bed(tr.dur), tr.i["start"], 0.55)
        S_("thunder", tr.i["start"] + 1.0, 0.6)
        S_("boom", tr.i["start"] + tr.strike - 0.02, 1.0); S_("thunder", tr.i["start"] + tr.strike, 1.0)
        S_("hit", tr.i["start"] + LT(tr, 3, 0.0) - 0.02, 0.8)
        G(tr.i["start"] + LT(tr, 3, 0.0) + 0.9, 0.5, 3)
    if "kitchen" in S:
        k = S["kitchen"]
        S_("whoosh", k.i["start"] - 0.15, 0.6)
        S_("pop", k.i["start"] + k.L[4][0] + 1.0, 0.7)
        G(k.i["start"] + LT(k, 5, 0.0) - 0.1, 0.8, 4); S_("sting", k.i["start"] + LT(k, 5, 0.0) - 0.1, 0.35)
        for j in range(3):
            S_("pop", k.i["start"] + LT(k, 6, 0.0) + j * 0.22 + 0.17, 0.9)
    if "phone" in S:
        p = S["phone"]
        S_("whoosh", p.i["start"] - 0.15, 0.5)
        S_("ding", p.i["start"] + p.L[7][0] + 0.9, 0.7)
        G(p.i["start"] + LT(p, 8, 0.0) - 0.05, 0.8, 5)
        S_("whoosh", p.i["start"] + LT(p, 8, 0.32) - 0.1, 0.5)
    if "class" in S:
        c = S["class"]
        S_("whoosh", c.i["start"] - 0.15, 0.5)
        A.place(fx, A.sfx("crowd").astype(np.float32)[: int(c.dur * sr)], c.i["start"], 0.25)
        S_("pop", c.i["start"] + c.L[9][0] + 1.1, 0.6)
        G(c.i["start"] + LT(c, 10, 0.0) - 0.15, 1.0, 6, 0.5); S_("boom", c.i["start"] + LT(c, 10, 0.0) - 0.15, 0.8)
    if "corridor" in S:
        co = S["corridor"]
        S_("whoosh", co.i["start"] - 0.15, 0.5)
        S_("pop", co.i["start"] + co.L[11][0] + 1.2, 0.5)
        S_("pop", co.i["start"] + LT(co, 12, 0.0) + 0.7, 0.6)
        G(co.i["start"] + LT(co, 13, 0.0) - 0.12, 0.7, 7)
        S_("ding", co.i["start"] + LT(co, 13, 0.0) + 0.35, 0.6)
    if "busstop" in S:
        b = S["busstop"]
        A.place(fx, rain_bed(b.dur + (S["stranger"].dur if "stranger" in S else 0), 8), b.i["start"], 0.6)
        S_("footsteps", b.i["start"] + 0.2, 0.4)
        S_("heartbeat", b.i["start"] + b.red_t - 0.2, 1.0); S_("heartbeat", b.i["start"] + b.red_t + 0.8, 1.0)
        S_("sting", b.i["start"] + b.red_t, 0.6)
    if "stranger" in S:
        s = S["stranger"]
        S_("riser", s.i["start"], 0.5)
        S_("heartbeat", s.i["start"] + 0.3, 0.8); S_("heartbeat", s.i["start"] + 1.3, 0.8)
        S_("hit", s.i["start"] + s.cut, 1.0); S_("boom", s.i["start"] + s.cut, 0.8)
    if "endcard" in S:
        ec = S["endcard"]
        G(ec.i["start"], 0.8, 8, 0.4); S_("boom", ec.i["start"], 0.9)
    # music duck under voice
    env = A._lp(np.abs(voice), 6)
    env = env / (env.max() + 1e-6)
    duck = 1 - 0.6 * np.clip(env * 3, 0, 1)
    mixv = voice * 1.0 + mus * 0.32 * duck + fx * 0.55
    end = int(total * sr)
    fo = int(0.6 * sr)
    mixv[end - fo:end] *= np.linspace(1, 0, fo)
    mixv = mixv[:end]
    mixv = mixv / (np.max(np.abs(mixv)) + 1e-6) * 0.95
    import soundfile as sf
    raw = out_wav.replace(".wav", "_raw.wav")
    sf.write(raw, mixv, sr)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-ar", str(sr), out_wav],
                   check=True)
    return out_wav


# ------------------------------------------------------------------ main
_SHOTS = None


def _init():
    global _SHOTS
    _SHOTS, _ = make_shots()


def _work(fi):
    return render_frame(_SHOTS, fi).tobytes()


def main():
    import multiprocessing as mp
    shots, total = make_shots()
    nfr = int(total * FPS)
    for sh in shots:
        print(f"{sh.i['name']:9s} {sh.i['start']:6.2f} -> {sh.i['end']:6.2f}")
    print("total", round(total, 2), "s,", nfr, "frames")
    out_dir = os.path.join(HERE, "out")
    os.makedirs(out_dir, exist_ok=True)
    if "--stills" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")]
        from PIL import Image
        for tt in ts:
            fi = int(tt * FPS)
            Image.fromarray(render_frame(shots, fi)).resize((540, 960)).save(os.path.join(HERE, "preview", f"f_{tt:05.2f}.jpg"), quality=88)
        return
    wav = build_audio(shots, total, os.path.join(out_dir, "mix.wav"))
    a, b = 0, nfr
    if "--frames" in sys.argv:
        a, b = [int(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(":")]
    out = os.path.join(out_dir, "laal_jhooth_short.mp4" if os.environ.get("SHORT") else "laal_jhooth_part1.mp4")
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-ss", f"{a / FPS}", "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium",
           "-crf", "26" if os.environ.get("SHORT") else "19", "-maxrate", "6M", "-bufsize", "12M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with mp.Pool(os.cpu_count(), initializer=_init) as pool:
        for k, buf in enumerate(pool.imap(_work, range(a, b), chunksize=4)):
            ff.stdin.write(buf)
            if k % 48 == 0:
                print("frame", a + k, "/", b, flush=True)
    ff.stdin.close(); ff.wait()
    print("wrote", out)


if __name__ == "__main__":
    main()
