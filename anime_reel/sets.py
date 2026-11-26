"""Painted backgrounds, rendered once per shot as numpy RGB at BG size (bigger than frame for camera moves)."""
import math
import numpy as np
from gfx import *

BW, BH = int(W * 1.16), int(H * 1.16)


def _ctx():
    s, ctx = new_surface(BW, BH)
    return s, ctx


def _layer(fn, blur=0):
    s, ctx = _ctx()
    fn(ctx)
    rgba = surf_to_rgba(s)
    if blur:
        rgb = blur_np(rgba[..., :3] * rgba[..., 3:4], blur)
        a = blur_np(np.repeat(rgba[..., 3:4], 3, 2), blur)[..., :1]
        rgba = np.concatenate([np.where(a > 0, rgb / np.maximum(a, 1e-4), 0), a], 2)
    return rgba


def _over(base, rgba):
    a = rgba[..., 3:4]
    return base * (1 - a) + rgba[..., :3] * a


def _clouds(ctx, rng, n, y0, y1, col, alpha, size=(120, 320)):
    for _ in range(n):
        cx, cy = rng.uniform(-100, BW + 100), rng.uniform(y0, y1)
        r = rng.uniform(*size)
        for k in range(6):
            ellipse(ctx, cx + rng.normal(0, r * 0.6), cy + rng.normal(0, r * 0.18), r * rng.uniform(0.5, 1), r * rng.uniform(0.25, 0.45))
            src(ctx, col, alpha); ctx.fill()


# ----------------------------------------------------------------- 1. storm terrace (night)
def terrace():
    rng = np.random.default_rng(3)

    def sky(ctx):
        lin(ctx, 0, 0, 0, BH, [(0, "#0b0f24"), (0.45, "#2a2350"), (0.75, "#4b3a6e"), (1, "#1a1830")]); ctx.paint()
    base = _layer(sky)[..., :3]

    def clouds(ctx):
        _clouds(ctx, rng, 26, 0, BH * 0.55, "#3a3566", 0.55, (160, 380))
        _clouds(ctx, rng, 18, 0, BH * 0.45, "#5a4d86", 0.35, (120, 260))
        _clouds(ctx, rng, 10, BH * 0.1, BH * 0.4, "#8b7bb8", 0.18, (80, 200))
    base = _over(base, _layer(clouds, 14))

    def city(ctx):
        x = -20
        while x < BW:
            w = rng.uniform(70, 170); h = rng.uniform(260, 720)
            y = BH * 0.74 - h
            src(ctx, "#141228"); ctx.rectangle(x, y, w, h + 400); ctx.fill()
            for wy in np.arange(y + 24, BH * 0.74 - 10, 34):
                for wx in np.arange(x + 12, x + w - 16, 26):
                    if rng.random() < 0.28:
                        src(ctx, rng.choice(["#ffcf7a", "#ffe6a8", "#9fc7ff"]), rng.uniform(0.5, 0.95))
                        ctx.rectangle(wx, wy, 12, 16); ctx.fill()
            x += w + rng.uniform(0, 30)
    base = _over(base, _layer(city, 2.5))

    def near(ctx):
        # terrace floor + parapet
        lin(ctx, 0, BH * 0.74, 0, BH, [(0, "#2a2840"), (1, "#0e0d18")])
        ctx.rectangle(0, BH * 0.74, BW, BH * 0.3); ctx.fill()
        src(ctx, "#1c1a2c"); ctx.rectangle(0, BH * 0.7, BW, BH * 0.05); ctx.fill()
        src(ctx, "#3d3a5a"); ctx.rectangle(0, BH * 0.7, BW, 8); ctx.fill()
        # water tank
        rrect(ctx, BW * 0.66, BH * 0.52, 260, 240, 30); src(ctx, "#101018"); ctx.fill()
        ellipse(ctx, BW * 0.66 + 130, BH * 0.52, 130, 26); src(ctx, "#1c1c2a"); ctx.fill()
        for k in range(4):
            src(ctx, "#08080d"); ctx.rectangle(BW * 0.66 + 20 + k * 70, BH * 0.52 + 230, 12, 80); ctx.fill()
        # antenna
        ctx.move_to(BW * 0.18, BH * 0.72); ctx.line_to(BW * 0.18, BH * 0.42)
        for k in range(4):
            ctx.move_to(BW * 0.18 - 70 + k * 10, BH * 0.45 + k * 40); ctx.line_to(BW * 0.18 + 70 - k * 10, BH * 0.45 + k * 40)
        src(ctx, "#0a0a12"); ctx.set_line_width(7); ctx.stroke()
        # puddles reflecting sky
        for k in range(5):
            ellipse(ctx, rng.uniform(0, BW), rng.uniform(BH * 0.8, BH * 0.97), rng.uniform(120, 260), rng.uniform(14, 30))
            src(ctx, "#6a5c9a", 0.35); ctx.fill()
    base = _over(base, _layer(near))
    return base


# ----------------------------------------------------------------- 2. kitchen (warm evening)
def kitchen():
    rng = np.random.default_rng(5)

    def room(ctx):
        lin(ctx, 0, 0, 0, BH, [(0, "#f3c98a"), (0.6, "#e4a866"), (1, "#a8693b")]); ctx.paint()
        # tiles
        for y in np.arange(BH * 0.18, BH * 0.62, 70):
            for x in np.arange(0, BW, 70):
                rrect(ctx, x + 3, y + 3, 64, 64, 6); src(ctx, "#fff1d6", 0.35); ctx.fill()
        # window with dusk
        rrect(ctx, BW * 0.08, BH * 0.08, BW * 0.34, BH * 0.22, 10); src(ctx, "#6b3f2a"); ctx.fill()
        lin(ctx, 0, BH * 0.09, 0, BH * 0.29, [(0, "#ff9a62"), (1, "#ffd59a")])
        ctx.rectangle(BW * 0.09, BH * 0.09, BW * 0.32, BH * 0.2); ctx.fill()
        ellipse(ctx, BW * 0.3, BH * 0.25, 60, 60); src(ctx, "#fff3c4", 0.9); ctx.fill()
        src(ctx, "#6b3f2a"); ctx.rectangle(BW * 0.245, BH * 0.09, 14, BH * 0.2); ctx.fill()
        # shelf with steel utensils and jars
        src(ctx, "#7a4a2a"); ctx.rectangle(BW * 0.5, BH * 0.2, BW * 0.48, 22); ctx.fill()
        for k in range(6):
            x = BW * 0.53 + k * 95
            col = ["#c84f2f", "#e2b33e", "#7a9e3a", "#d07a2a", "#8a3f6e", "#e2b33e"][k]
            rrect(ctx, x, BH * 0.2 - 110, 70, 110, 14); src(ctx, "#f6e7c8", 0.55); ctx.fill()
            rrect(ctx, x + 6, BH * 0.2 - 70, 58, 66, 10); src(ctx, col); ctx.fill()
            src(ctx, "#5a3a2a"); ctx.rectangle(x + 4, BH * 0.2 - 122, 62, 16); ctx.fill()
        for k in range(5):
            x = BW * 0.55 + k * 110
            ellipse(ctx, x, BH * 0.32, 44, 44); lin(ctx, x - 44, 0, x + 44, 0, [(0, "#8a96a6"), (0.5, "#f4f7fb"), (1, "#7b8796")]); ctx.fill()
            ctx.move_to(x, BH * 0.32 - 44); ctx.line_to(x, BH * 0.27); src(ctx, "#5a5f6a"); ctx.set_line_width(5); ctx.stroke()
        # counter
        lin(ctx, 0, BH * 0.62, 0, BH, [(0, "#5a3522"), (1, "#2e1a10")])
        ctx.rectangle(0, BH * 0.62, BW, BH); ctx.fill()
        src(ctx, "#8b5a36"); ctx.rectangle(0, BH * 0.62, BW, 18); ctx.fill()
        # tubelight glow
        rad(ctx, BW * 0.5, 0, 10, BW * 0.9, [(0, (1, 0.98, 0.9, 0.35)), (1, (1, 0.9, 0.7, 0))]); ctx.paint()
    return _layer(room, 5)[..., :3]


# ----------------------------------------------------------------- 3. bedroom (for phone)
def bedroom():
    rng = np.random.default_rng(9)

    def room(ctx):
        lin(ctx, 0, 0, 0, BH, [(0, "#1d2442"), (1, "#0d1022")]); ctx.paint()
        # posters + fairy lights
        rrect(ctx, BW * 0.1, BH * 0.12, 300, 420, 8); src(ctx, "#c0392b", 0.7); ctx.fill()
        rrect(ctx, BW * 0.62, BH * 0.1, 340, 260, 8); src(ctx, "#2a7fbf", 0.6); ctx.fill()
        for k in range(22):
            x = k * BW / 21
            y = BH * 0.07 + 40 * math.sin(k * 0.6)
            rad(ctx, x, y, 0, 40, [(0, "#ffd27a"), (1, (1, 0.8, 0.4, 0))]); ctx.arc(x, y, 40, 0, 7); ctx.fill()
        # bed
        lin(ctx, 0, BH * 0.62, 0, BH, [(0, "#3a3f6e"), (1, "#141633")]); rrect(ctx, -40, BH * 0.62, BW + 80, BH, 40); ctx.fill()
        # window moonlight
        rad(ctx, BW * 0.85, BH * 0.45, 0, 600, [(0, (0.5, 0.65, 1, 0.35)), (1, (0.3, 0.4, 1, 0))]); ctx.paint()
    return _layer(room, 22)[..., :3]


# ----------------------------------------------------------------- 4. classroom (day)
def classroom():
    rng = np.random.default_rng(11)

    def room(ctx):
        lin(ctx, 0, 0, 0, BH, [(0, "#e8dcc0"), (1, "#c9b48c")]); ctx.paint()
        # windows with light rays
        for k in range(2):
            x = BW * (0.02 + k * 0.8)
            src(ctx, "#bfe3ff"); ctx.rectangle(x, BH * 0.08, 160, 520); ctx.fill()
            src(ctx, "#8a6a44"); ctx.rectangle(x + 74, BH * 0.08, 12, 520); ctx.fill()
        # blackboard
        rrect(ctx, BW * 0.1, BH * 0.12, BW * 0.8, BH * 0.3, 10); src(ctx, "#6b4a2a"); ctx.fill()
        lin(ctx, 0, BH * 0.13, 0, BH * 0.41, [(0, "#2f4a3a"), (1, "#22382c")])
        ctx.rectangle(BW * 0.115, BH * 0.13, BW * 0.77, BH * 0.28); ctx.fill()
        # chalk smudges + scribbles
        for k in range(14):
            ellipse(ctx, rng.uniform(BW * 0.15, BW * 0.85), rng.uniform(BH * 0.15, BH * 0.4), rng.uniform(40, 140), rng.uniform(10, 30))
            src(ctx, "#ffffff", 0.05); ctx.fill()
        ctx.set_line_width(5); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for row in range(5):
            y = BH * 0.17 + row * 80
            x = BW * 0.16 + rng.uniform(0, 60)
            while x < BW * (0.5 + rng.uniform(0, 0.3)):
                w = rng.uniform(20, 60)
                ctx.move_to(x, y + rng.uniform(-6, 6))
                ctx.curve_to(x + w * 0.3, y - 22, x + w * 0.6, y + 22, x + w, y + rng.uniform(-8, 8))
                x += w + rng.uniform(10, 34)
            src(ctx, "#f2f2e6", 0.75); ctx.stroke()
        # light rays
        for k in range(4):
            poly(ctx, [(BW * 0.02 + k * 40, BH * 0.08), (BW * 0.02 + 160 + k * 40, BH * 0.08), (BW * 0.9 + k * 80, BH), (BW * 0.5 + k * 80, BH)])
            src(ctx, "#fff6d8", 0.07); ctx.fill()
        # teacher table
        src(ctx, "#7a5230"); ctx.rectangle(0, BH * 0.78, BW, BH); ctx.fill()
        src(ctx, "#9a6a40"); ctx.rectangle(0, BH * 0.78, BW, 22); ctx.fill()
    return _layer(room, 6)[..., :3]


# ----------------------------------------------------------------- 5. corridor with arches (sunset)
def corridor():
    rng = np.random.default_rng(13)

    def far(ctx):
        lin(ctx, 0, 0, 0, BH, [(0, "#ff9a5a"), (0.35, "#ffc27a"), (0.6, "#ffe1a8"), (1, "#f4b07a")]); ctx.paint()
        ellipse(ctx, BW * 0.7, BH * 0.36, 120, 120); src(ctx, "#fff6d6"); ctx.fill()
        rad(ctx, BW * 0.7, BH * 0.36, 100, 600, [(0, (1, 0.95, 0.8, 0.7)), (1, (1, 0.8, 0.5, 0))]); ctx.paint()
        # trees
        for k in range(9):
            cx, cy = rng.uniform(0, BW), rng.uniform(BH * 0.38, BH * 0.5)
            for j in range(7):
                ellipse(ctx, cx + rng.normal(0, 70), cy + rng.normal(0, 40), rng.uniform(60, 120), rng.uniform(50, 90))
                src(ctx, rng.choice(["#3f6b3a", "#5a8a40", "#2f5530", "#7aa24a"]), 0.95); ctx.fill()
        src(ctx, "#3a6a3a"); ctx.rectangle(0, BH * 0.5, BW, BH * 0.1); ctx.fill()
    base = _layer(far, 10)[..., :3]

    def arches(ctx):
        # wall with arches (perspective-less frontal arcade)
        wall = "#e9c48c"
        src(ctx, wall)
        ctx.rectangle(0, 0, BW, BH)
        aw, gap = 330, 110
        x = -120
        while x < BW:
            ctx.new_sub_path(); ctx.move_to(x, BH * 0.62)
            ctx.line_to(x, BH * 0.3); ctx.arc(x + aw / 2, BH * 0.3, aw / 2, math.pi, 0); ctx.line_to(x + aw, BH * 0.62); ctx.close_path()
            x += aw + gap
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); ctx.fill()
        ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
        # pillar shading + capitals
        x = -120
        while x < BW:
            lin(ctx, x - gap, 0, x, 0, [(0, "#c9965e"), (1, "#f0d29e")]); ctx.rectangle(x - gap, 0, gap, BH * 0.62); ctx.fill()
            src(ctx, "#b5824a"); ctx.rectangle(x - gap - 14, BH * 0.29, gap + 28, 26); ctx.fill()
            ctx.arc(x + aw / 2, BH * 0.3, aw / 2 + 12, math.pi, 0); src(ctx, "#c8935a"); ctx.set_line_width(20); ctx.stroke()
            x += aw + gap
        # top beam + ceiling shadow
        lin(ctx, 0, 0, 0, BH * 0.16, [(0, "#5a3a2a"), (1, (0.35, 0.22, 0.16, 0))]); ctx.rectangle(0, 0, BW, BH * 0.16); ctx.fill()
        # railing (balusters)
        src(ctx, "#d7b98a"); ctx.rectangle(0, BH * 0.54, BW, 28); ctx.fill()
        for bx in np.arange(10, BW, 58):
            smooth(ctx, [(bx, BH * 0.56), (bx + 22, BH * 0.56), (bx + 26, BH * 0.585), (bx + 18, BH * 0.6), (bx + 24, BH * 0.615),
                         (bx + 22, BH * 0.625), (bx, BH * 0.625), (bx - 2, BH * 0.615), (bx + 4, BH * 0.6), (bx - 4, BH * 0.585)], True, 0.4)
            lin(ctx, bx - 4, 0, bx + 26, 0, [(0, "#b38a58"), (0.5, "#f2dcae"), (1, "#a87c4a")]); ctx.fill()
        # floor tiles (checker, perspective)
        lin(ctx, 0, BH * 0.62, 0, BH, [(0, "#b89a74"), (1, "#5c4632")]); ctx.rectangle(0, BH * 0.625, BW, BH); ctx.fill()
        for r in range(12):
            y0 = BH * 0.625 + (r ** 1.6) * 9
            y1 = BH * 0.625 + ((r + 1) ** 1.6) * 9
            n = 8
            for cidx in range(-6, n + 6):
                if (cidx + r) % 2:
                    continue
                def px(c, y):
                    return BW / 2 + (c - n / 2) * (BW / n) * (0.6 + (y - BH * 0.625) / (BH * 0.375) * 1.4)
                poly(ctx, [(px(cidx, y0), y0), (px(cidx + 1, y0), y0), (px(cidx + 1, y1), y1), (px(cidx, y1), y1)])
                src(ctx, "#3d5f6e", 0.55); ctx.fill()
        # sun patches through arches on floor
        x = -120
        while x < BW:
            poly(ctx, [(x + 40, BH * 0.63), (x + aw - 40, BH * 0.63), (x + aw + 160, BH), (x + 160, BH)])
            src(ctx, "#ffd890", 0.28); ctx.fill()
            x += aw + gap
    base = _over(base, _layer(arches, 1.2))
    return base


# ----------------------------------------------------------------- 6. rainy bus stop (night)
def busstop():
    rng = np.random.default_rng(17)

    def far(ctx):
        lin(ctx, 0, 0, 0, BH, [(0, "#05060c"), (0.5, "#0d1424"), (1, "#05060a")]); ctx.paint()
        # bokeh city lights
        for k in range(70):
            x, y = rng.uniform(0, BW), rng.uniform(BH * 0.2, BH * 0.6)
            r = rng.uniform(14, 60)
            col = rng.choice(["#ff9a3c", "#ffd27a", "#4ab0ff", "#ff4a6a", "#9affd0"])
            rad(ctx, x, y, 0, r, [(0, hexc(col, 0.55)), (0.7, hexc(col, 0.25)), (1, hexc(col, 0))]); ctx.arc(x, y, r, 0, 7); ctx.fill()
    base = _layer(far, 6)[..., :3]

    def near(ctx):
        # road + wet reflections
        lin(ctx, 0, BH * 0.66, 0, BH, [(0, "#0e1220"), (1, "#05060a")]); ctx.rectangle(0, BH * 0.66, BW, BH); ctx.fill()
        for k in range(40):
            x = rng.uniform(0, BW)
            col = rng.choice(["#ff9a3c", "#4ab0ff", "#ff4a6a"])
            lin(ctx, 0, BH * 0.66, 0, BH, [(0, hexc(col, 0.25)), (1, hexc(col, 0))])
            ctx.rectangle(x, BH * 0.66, rng.uniform(4, 14), BH * 0.34); ctx.fill()
        # bus shelter
        src(ctx, "#1a1e2a"); ctx.rectangle(BW * 0.08, BH * 0.28, 22, BH * 0.4); ctx.fill()
        ctx.rectangle(BW * 0.92, BH * 0.28, 22, BH * 0.4); ctx.fill()
        poly(ctx, [(BW * 0.03, BH * 0.27), (BW * 0.98, BH * 0.25), (BW * 0.98, BH * 0.28), (BW * 0.03, BH * 0.3)]); src(ctx, "#232838"); ctx.fill()
        # glass panel
        src(ctx, "#5a7aa8", 0.1); ctx.rectangle(BW * 0.1, BH * 0.3, BW * 0.4, BH * 0.3); ctx.fill()
        # sign
        rrect(ctx, BW * 0.62, BH * 0.31, 200, 70, 10); src(ctx, "#f2c14e"); ctx.fill()
        # streetlight cone
        poly(ctx, [(BW * 0.5 - 30, BH * 0.12), (BW * 0.5 + 30, BH * 0.12), (BW * 0.5 + 520, BH * 0.95), (BW * 0.5 - 520, BH * 0.95)])
        lin(ctx, 0, BH * 0.12, 0, BH * 0.95, [(0, (1, 0.85, 0.55, 0.35)), (1, (1, 0.8, 0.5, 0.02))]); ctx.fill()
        ellipse(ctx, BW * 0.5, BH * 0.12, 50, 16); src(ctx, "#fff2c8"); ctx.fill()
        src(ctx, "#111111"); ctx.rectangle(BW * 0.5 - 6, 0, 12, BH * 0.115); ctx.fill()
        # pool of light on ground
        ellipse(ctx, BW * 0.5, BH * 0.9, 520, 90); src(ctx, "#ffcf8a", 0.12); ctx.fill()
    base = _over(base, _layer(near, 1.5))
    return base


def void(col1="#120406", col2="#000000"):
    def f(ctx):
        rad(ctx, BW / 2, BH * 0.45, 0, BH * 0.7, [(0, col1), (1, col2)]); ctx.paint()
    return _layer(f)[..., :3]


SETS = dict(terrace=terrace, kitchen=kitchen, bedroom=bedroom, classroom=classroom, corridor=corridor,
            busstop=busstop, void=void)
