"""Anime-style bust characters drawn with cairo. Units: 1.0 = head height (~ s px)."""
import math
from gfx import *

CAST = {
    "kabir": dict(skin="#e0a67c", hair="#1b1a24", hair_hi="#4a4a66", eye="#5a3420", style="spiky",
                  top="#22304f", top2="#e9e2d3", outfit="hoodie", streak=True),
    "mummy": dict(skin="#d9996e", hair="#20161a", hair_hi="#5a3c40", eye="#3a2215", style="bun",
                  top="#c2364b", top2="#f0b43c", outfit="saree", bindi=True),
    "sir": dict(skin="#c98a5f", hair="#2a2a2e", hair_hi="#6a6a70", eye="#2a1a10", style="side",
                top="#e9eef4", top2="#33507a", outfit="shirt", glasses=True, mustache=True),
    "meera": dict(skin="#efbb93", hair="#2a1720", hair_hi="#7a4a5a", eye="#6b3a28", style="long",
                  top="#f4f1ea", top2="#3a6fb0", outfit="kurti"),
    "bunty": dict(skin="#d39468", hair="#151317", hair_hi="#454050", eye="#3a2215", style="messy",
                  top="#f2c14e", top2="#e86f3a", outfit="tee"),
    "stranger": dict(skin="#b98563", hair="#0d0d12", hair_hi="#2a2a35", eye="#ff2b2b", style="hood",
                     top="#14141c", top2="#22222e", outfit="hoodup"),
}

DEFAULT_ST = dict(turn=0.0, blink=0.0, mouth=0.0, smile=0.0, brow=0.0, look=(0.0, 0.0), blush=0.0,
                  glow=0.0, sway=0.0, breathe=0.0, light=1.0, sweat=0.0, shock=0.0, eyes_closed_happy=0.0,
                  rim=None, dark=0.0)


def _st(st):
    d = dict(DEFAULT_ST)
    d.update(st or {})
    return d


def draw_body(ctx, c, st):
    """Torso + neck in head units, origin at chin-ish center (0,0) = face center."""
    br = st["breathe"]
    sh_y = 0.78 + br * 0.015
    skin = c["skin"]
    # neck
    ctx.save()
    poly(ctx, [(-0.15, 0.25), (0.15, 0.25), (0.17, 0.9), (-0.17, 0.9)])
    src(ctx, skin); ctx.fill()
    poly(ctx, [(-0.15, 0.3), (0.15, 0.3), (0.16, 0.52), (-0.16, 0.6)])
    src(ctx, shade(skin, -0.28)); ctx.fill()
    ctx.restore()
    top, top2 = c["top"], c["top2"]
    o = c["outfit"]
    # torso silhouette
    body = [(-0.95, 2.6), (-0.9, 1.25), (-0.78, sh_y + 0.12), (-0.35, sh_y - 0.02), (0.0, sh_y + 0.08),
            (0.35, sh_y - 0.02), (0.78, sh_y + 0.12), (0.9, 1.25), (0.95, 2.6)]
    if o == "saree":
        smooth(ctx, body, closed=True, tension=0.35); src(ctx, top); ctx.fill()
        # blouse neckline
        smooth(ctx, [(-0.33, sh_y), (0.0, 1.05), (0.33, sh_y)], closed=False)
        ctx.line_to(0.33, sh_y - 0.1); ctx.line_to(-0.33, sh_y - 0.1); ctx.close_path()
        src(ctx, skin); ctx.fill()
        # pallu across shoulder
        poly(ctx, [(0.55, sh_y + 0.02), (0.85, sh_y + 0.15), (-0.2, 2.6), (-0.75, 2.6)])
        lin(ctx, 0, 0.8, 0, 2.6, [(0, top2), (1, shade(top2, -0.25))]); ctx.fill()
        for k in range(3):
            ctx.move_to(0.5 - k * 0.05, sh_y + 0.05 + k * 0.05); ctx.line_to(-0.6 - k * 0.1, 2.6)
            src(ctx, shade(top2, -0.35), 0.5); ctx.set_line_width(0.012); ctx.stroke()
        poly(ctx, [(0.55, sh_y + 0.02), (0.85, sh_y + 0.15), (0.80, sh_y + 0.22), (0.5, sh_y + 0.08)])
        src(ctx, "#8a1f2c"); ctx.fill()
    elif o == "shirt":
        smooth(ctx, body, closed=True, tension=0.35); src(ctx, top); ctx.fill()
        # shading side
        poly(ctx, [(0.45, sh_y), (0.95, 1.3), (0.95, 2.6), (0.55, 2.6)]); src(ctx, shade(top, -0.12)); ctx.fill()
        # collar
        poly(ctx, [(-0.2, sh_y - 0.08), (0.0, 1.0), (-0.32, 0.98)]); src(ctx, "#ffffff"); ctx.fill()
        poly(ctx, [(0.2, sh_y - 0.08), (0.0, 1.0), (0.32, 0.98)]); src(ctx, "#ffffff"); ctx.fill()
        # tie
        poly(ctx, [(-0.05, 0.95), (0.05, 0.95), (0.09, 1.9), (0.0, 2.0), (-0.09, 1.9)]); src(ctx, top2); ctx.fill()
        poly(ctx, [(-0.06, 0.9), (0.06, 0.9), (0.05, 1.0), (-0.05, 1.0)]); src(ctx, shade(top2, -0.3)); ctx.fill()
        for k in range(5):
            ctx.move_to(-0.06, 1.1 + k * 0.17); ctx.line_to(0.07, 1.02 + k * 0.17)
            src(ctx, shade(top2, 0.3), 0.6); ctx.set_line_width(0.02); ctx.stroke()
    elif o == "kurti":
        smooth(ctx, body, closed=True, tension=0.35); src(ctx, top); ctx.fill()
        poly(ctx, [(0.45, sh_y), (0.95, 1.3), (0.95, 2.6), (0.55, 2.6)]); src(ctx, shade(top, -0.1)); ctx.fill()
        # neckline + embroidery
        smooth(ctx, [(-0.22, sh_y - 0.03), (0.0, 1.08), (0.22, sh_y - 0.03)], closed=False)
        ctx.line_to(0.22, sh_y - 0.1); ctx.line_to(-0.22, sh_y - 0.1); ctx.close_path(); src(ctx, skin); ctx.fill()
        smooth(ctx, [(-0.24, sh_y - 0.03), (0.0, 1.1), (0.24, sh_y - 0.03)], closed=False)
        src(ctx, top2); ctx.set_line_width(0.035); ctx.stroke()
        for k in range(7):
            ellipse(ctx, -0.36 + k * 0.12, 1.32 + 0.04 * math.sin(k), 0.02, 0.02); src(ctx, top2); ctx.fill()
        # dupatta strap
        poly(ctx, [(-0.6, sh_y + 0.05), (-0.42, sh_y), (0.3, 2.6), (0.05, 2.6)])
        lin(ctx, 0, 0.8, 0, 2.6, [(0, "#e7708c"), (1, "#b84866")]); ctx.fill()
    elif o == "tee":
        smooth(ctx, body, closed=True, tension=0.35); src(ctx, top); ctx.fill()
        smooth(ctx, [(-0.2, sh_y - 0.05), (0.0, 0.98), (0.2, sh_y - 0.05)], closed=False)
        src(ctx, shade(top, -0.3)); ctx.set_line_width(0.05); ctx.stroke()
        ellipse(ctx, 0.0, 1.7, 0.28, 0.28); src(ctx, top2); ctx.fill()
    else:  # hoodie / hoodup
        smooth(ctx, body, closed=True, tension=0.35)
        lin(ctx, 0, 0.8, 0, 2.6, [(0, shade(top, 0.08)), (1, shade(top, -0.2))]); ctx.fill()
        poly(ctx, [(0.5, sh_y + 0.02), (0.95, 1.3), (0.95, 2.6), (0.6, 2.6)]); src(ctx, shade(top, -0.22)); ctx.fill()
        if o == "hoodie":
            # inner tee + hood collar
            poly(ctx, [(-0.22, sh_y - 0.02), (0.22, sh_y - 0.02), (0.12, 1.25), (-0.12, 1.25)]); src(ctx, top2); ctx.fill()
            smooth(ctx, [(-0.62, sh_y + 0.08), (-0.4, 0.62), (-0.18, 0.86), (-0.1, 1.3), (-0.3, 1.25), (-0.55, 0.98)], True, 0.4)
            src(ctx, shade(top, 0.12)); ctx.fill()
            smooth(ctx, [(0.62, sh_y + 0.08), (0.4, 0.62), (0.18, 0.86), (0.1, 1.3), (0.3, 1.25), (0.55, 0.98)], True, 0.4)
            src(ctx, shade(top, 0.02)); ctx.fill()
            for sx in (-1, 1):
                ctx.move_to(sx * 0.12, 1.15); ctx.curve_to(sx * 0.14, 1.4, sx * 0.1, 1.6, sx * 0.13, 1.85)
                src(ctx, "#f2efe8"); ctx.set_line_width(0.025); ctx.stroke()
                ellipse(ctx, sx * 0.13, 1.87, 0.025, 0.035); src(ctx, "#cfc9bd"); ctx.fill()
            # zipper line
            ctx.move_to(0, 1.25); ctx.line_to(0, 2.6); src(ctx, shade(top, -0.4)); ctx.set_line_width(0.02); ctx.stroke()


def draw_hair_back(ctx, c, st):
    s = c["style"]
    hc = c["hair"]
    sw = st["sway"]
    if s == "long":
        pts = [(-0.55, -0.35), (-0.62, 0.3), (-0.7 + sw * 0.03, 1.0), (-0.62 + sw * 0.04, 1.55), (-0.25, 1.35),
               (0.25, 1.35), (0.62 + sw * 0.04, 1.55), (0.7 + sw * 0.03, 1.0), (0.62, 0.3), (0.55, -0.35), (0.0, -0.72)]
        smooth(ctx, pts, True, 0.45)
        lin(ctx, 0, -0.7, 0, 1.5, [(0, hc), (1, shade(hc, -0.3))]); ctx.fill()
    elif s == "bun":
        ellipse(ctx, 0.0, -0.62, 0.26, 0.2); src(ctx, hc); ctx.fill()
        ellipse(ctx, -0.06, -0.66, 0.12, 0.06, -0.3); src(ctx, c["hair_hi"], 0.6); ctx.fill()
        smooth(ctx, [(-0.5, -0.3), (-0.5, 0.25), (0.5, 0.25), (0.5, -0.3), (0.0, -0.66)], True, 0.5)
        src(ctx, hc); ctx.fill()
        # gajra flowers
        for k in range(7):
            a = math.pi * (0.15 + k * 0.12)
            ellipse(ctx, 0.26 * math.cos(a), -0.62 + 0.2 * math.sin(a) * 0.9, 0.035, 0.035); src(ctx, "#fff8ee"); ctx.fill()
    elif s == "hood":
        smooth(ctx, [(-0.72, 0.9), (-0.74, -0.1), (-0.5, -0.72), (0.0, -0.86), (0.5, -0.72), (0.74, -0.1), (0.72, 0.9)], True, 0.45)
        lin(ctx, 0, -0.9, 0, 0.9, [(0, shade(c["top"], 0.12)), (1, c["top"])]); ctx.fill()
        smooth(ctx, [(-0.55, 0.7), (-0.56, -0.1), (-0.38, -0.58), (0.0, -0.68), (0.38, -0.58), (0.56, -0.1), (0.55, 0.7)], True, 0.45)
        src(ctx, "#050507"); ctx.fill()
    else:
        # short styles: back mass
        smooth(ctx, [(-0.52, 0.1), (-0.56, -0.4), (-0.3, -0.72), (0.1, -0.78), (0.45, -0.62), (0.57, -0.25), (0.52, 0.1)], True, 0.5)
        src(ctx, hc); ctx.fill()
        if s in ("spiky", "messy"):
            spikes = ([(-0.55, -0.5, -0.78, -0.62), (-0.38, -0.68, -0.52, -0.92), (-0.12, -0.76, -0.12, -0.98),
                       (0.14, -0.76, 0.3, -0.97), (0.38, -0.66, 0.62, -0.82), (0.55, -0.42, 0.78, -0.45),
                       (-0.56, -0.2, -0.72, -0.12), (0.56, -0.18, 0.72, -0.08)] if s == "spiky" else
                      [(-0.5, -0.55, -0.66, -0.7), (-0.25, -0.72, -0.3, -0.86), (0.05, -0.78, 0.12, -0.88),
                       (0.3, -0.7, 0.45, -0.8), (0.52, -0.5, 0.66, -0.55)])
            for (x0, y0, x1, y1) in spikes:
                x1 += sw * 0.03
                poly(ctx, [(x0 - 0.12, y0 + 0.08), (x1, y1), (x0 + 0.14, y0 + 0.1)])
                src(ctx, hc); ctx.fill()


def face_path(ctx, t):
    # t: turn [-0.5, 0.5]; jaw shifts and far side compresses
    k = t * 0.09
    pts = [(-0.43 + max(0, t) * 0.08, -0.4), (-0.44 + max(0, t) * 0.07, -0.05), (-0.39 + max(0, t) * 0.06, 0.2),
           (-0.2 + k, 0.43), (0.0 + k * 1.6, 0.53), (0.2 + k, 0.43), (0.39 + min(0, t) * 0.06, 0.2),
           (0.44 + min(0, t) * 0.07, -0.05), (0.43 + min(0, t) * 0.08, -0.4), (0.0, -0.62)]
    smooth(ctx, pts, True, 0.42)


def draw_eye(ctx, x, y, side, c, st, w=0.24, h=0.2):
    """side=-1 left (viewer), +1 right. Drawn mirrored so the lash flick points outward."""
    ctx.save(); ctx.translate(x, y); ctx.scale(side, 1)
    _eye(ctx, 0.0, 0.0, side, c, st, w, h)
    ctx.restore()


def _eye(ctx, x, y, side, c, st, w, h):
    blink = st["blink"]
    lx, ly = st["look"]
    lx = lx * side
    glow = st["glow"]
    shock = st["shock"]
    happy = st["eyes_closed_happy"]
    lw = 0.028
    if happy > 0.5:
        ctx.move_to(x - w * 0.5, y + 0.02); ctx.curve_to(x - w * 0.2, y - 0.09, x + w * 0.2, y - 0.09, x + w * 0.5, y + 0.02)
        src(ctx, "#1a0f10"); ctx.set_line_width(lw * 1.3); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        return
    op = 1 - blink
    hh = h * max(op, 0.0) * (1 + shock * 0.15)
    # eye white (almond)
    if op > 0.08:
        ctx.save()
        top = y - hh * 0.55
        bot = y + hh * 0.45
        ctx.move_to(x - w * 0.5, y + 0.01)
        ctx.curve_to(x - w * 0.35, top, x + w * 0.25, top - 0.01, x + w * 0.52, y - hh * 0.15 * side * 0 - 0.01)
        ctx.curve_to(x + w * 0.35, bot, x - w * 0.3, bot, x - w * 0.5, y + 0.01)
        ctx.close_path()
        src(ctx, "#fbf7f2"); ctx.fill_preserve()
        ctx.clip()
        # iris
        ir_w, ir_h = w * (0.42 if shock < 0.5 else 0.3), h * (0.78 if shock < 0.5 else 0.55)
        ix, iy = x + lx * w * 0.22, y + ly * h * 0.15
        eye_c = mix(c["eye"], "#ff2020", glow) if glow > 0 else hexc(c["eye"])
        ellipse(ctx, ix, iy, ir_w, ir_h)
        lin(ctx, 0, iy - ir_h, 0, iy + ir_h, [(0, shade(eye_c, -0.6)), (0.55, eye_c), (1, shade(eye_c, 0.35))]); ctx.fill()
        ellipse(ctx, ix, iy, ir_w, ir_h); src(ctx, shade(eye_c, -0.7)); ctx.set_line_width(0.012); ctx.stroke()
        ellipse(ctx, ix, iy + ir_h * 0.05, ir_w * 0.45, ir_h * 0.48); src(ctx, shade(eye_c, -0.75)); ctx.fill()
        # upper lid shadow
        ellipse(ctx, x, top - hh * 0.05, w * 0.6, hh * 0.32); src(ctx, "#3a2030", 0.25); ctx.fill()
        # highlights
        ellipse(ctx, ix - ir_w * 0.35, iy - ir_h * 0.4, ir_w * 0.32, ir_h * 0.24); src(ctx, "#ffffff", 0.95); ctx.fill()
        ellipse(ctx, ix + ir_w * 0.35, iy + ir_h * 0.42, ir_w * 0.13, ir_h * 0.1); src(ctx, "#ffffff", 0.85); ctx.fill()
        if glow > 0.05:
            ellipse(ctx, ix, iy, ir_w * 1.1, ir_h * 1.1); src(ctx, "#ff3030", 0.35 * glow); ctx.fill()
        ctx.restore()
    # upper lash line (thick, flick)
    top = y - hh * 0.55
    ctx.move_to(x - w * 0.55, y + 0.02 - (1 - op) * 0.0)
    ctx.curve_to(x - w * 0.35, top - 0.012, x + w * 0.25, top - 0.022, x + w * 0.56, y - 0.005)
    ctx.line_to(x + w * 0.62, y - 0.035)
    src(ctx, "#140b0d"); ctx.set_line_width(lw * (1.4 if op > 0.2 else 1.0))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
    if op > 0.2:
        bot = y + hh * 0.45
        ctx.move_to(x - w * 0.25, bot + 0.005); ctx.curve_to(x - w * 0.05, bot + 0.018, x + w * 0.2, bot + 0.012, x + w * 0.42, bot - 0.01)
        src(ctx, "#2a1718", 0.75); ctx.set_line_width(lw * 0.45); ctx.stroke()


def draw_face(ctx, c, st):
    t = st["turn"]
    skin = c["skin"]
    # ears
    for sx in (-1, 1):
        ex = sx * (0.43 - (t * sx) * 0.06)
        ellipse(ctx, ex, 0.0, 0.07, 0.11); src(ctx, skin); ctx.fill()
        ellipse(ctx, ex, 0.0, 0.035, 0.065); src(ctx, shade(skin, -0.2)); ctx.fill()
    face_path(ctx, t)
    lin(ctx, 0, -0.6, 0, 0.55, [(0, shade(skin, 0.05)), (1, skin)]); ctx.fill_preserve()
    src(ctx, shade(skin, -0.55)); ctx.set_line_width(0.014); ctx.stroke()
    # cel shade on far side
    ctx.save()
    face_path(ctx, t); ctx.clip()
    side = 1 if t <= 0 else -1
    smooth(ctx, [(side * 0.48, -0.6), (side * 0.3, -0.2), (side * 0.33, 0.15), (side * 0.12 + t * 0.1, 0.5),
                 (side * 0.6, 0.6)], True, 0.4)
    src(ctx, shade(skin, -0.16), 0.55 + 0.25 * st["dark"]); ctx.fill()
    if st["rim"]:
        ctx.set_line_width(0.05)
        face_path(ctx, t); src(ctx, st["rim"], 0.6); ctx.stroke()
    ctx.restore()
    fx = t * 0.12
    # blush
    if st["blush"] > 0.01:
        for sx in (-1, 1):
            ellipse(ctx, sx * 0.24 + fx, 0.2, 0.1, 0.045); src(ctx, "#ff6f7d", 0.45 * st["blush"]); ctx.fill()
            for k in range(3):
                bx = sx * 0.24 + fx - 0.05 + k * 0.04
                ctx.move_to(bx + 0.015, 0.17); ctx.line_to(bx - 0.01, 0.23)
                src(ctx, "#e0404f", 0.6 * st["blush"]); ctx.set_line_width(0.01); ctx.stroke()
    # eyes
    ew = 0.25
    for sx in (-1, 1):
        compress = 1 - max(0, t * sx) * 0.5
        draw_eye(ctx, sx * 0.2 + fx * (1.1 if sx * t > 0 else 0.9), 0.02, sx, c, st, w=ew * compress, h=0.2)
    # brows
    b = st["brow"]  # -1 angry/sad-in, +1 raised
    for sx in (-1, 1):
        bx = sx * 0.2 + fx
        y_in = -0.16 - b * 0.05 + (0.03 if b < 0 else 0)
        y_out = -0.19 - b * 0.03
        ctx.move_to(bx - sx * 0.1, y_in); ctx.curve_to(bx - sx * 0.02, y_in - 0.03, bx + sx * 0.06, y_out - 0.01, bx + sx * 0.12, y_out + 0.01)
        src(ctx, shade(c["hair"], 0.05)); ctx.set_line_width(0.032); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    # nose
    ctx.move_to(0.0 + fx * 1.3, 0.16); ctx.line_to(-0.025 * (1 if t >= 0 else -1) + fx * 1.3, 0.22)
    src(ctx, shade(skin, -0.35)); ctx.set_line_width(0.018); ctx.stroke()
    # mouth
    mx, my = fx * 1.2, 0.34
    m = st["mouth"]
    sm = st["smile"]
    if c.get("mustache"):
        smooth(ctx, [(mx - 0.12, my - 0.035), (mx, my - 0.07), (mx + 0.12, my - 0.035), (mx + 0.1, my - 0.01), (mx, my - 0.035), (mx - 0.1, my - 0.01)], True, 0.4)
        src(ctx, c["hair"]); ctx.fill()
    if m > 0.05:
        mw, mh = 0.075 + sm * 0.03, 0.02 + m * 0.07
        smooth(ctx, [(mx - mw, my - sm * 0.01), (mx, my - 0.01 - sm * 0.02), (mx + mw, my - sm * 0.01), (mx + mw * 0.5, my + mh), (mx - mw * 0.5, my + mh)], True, 0.45)
        src(ctx, "#5a1820"); ctx.fill()
        ellipse(ctx, mx, my + mh * 0.75, mw * 0.5, mh * 0.3); src(ctx, "#d75a64"); ctx.fill()
    else:
        ctx.move_to(mx - 0.06 - sm * 0.02, my - sm * 0.02)
        ctx.curve_to(mx - 0.02, my + 0.012 + sm * 0.03, mx + 0.02, my + 0.012 + sm * 0.03, mx + 0.06 + sm * 0.02, my - sm * 0.02)
        src(ctx, "#4a1c1c"); ctx.set_line_width(0.018); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    if c.get("bindi"):
        ellipse(ctx, fx, -0.2, 0.025, 0.025); src(ctx, "#d4142c"); ctx.fill()
    if c.get("glasses"):
        for sx in (-1, 1):
            rrect(ctx, sx * 0.2 + fx - 0.14, -0.08, 0.28, 0.2, 0.05)
            src(ctx, "#bcd8ff", 0.18); ctx.fill_preserve()
            src(ctx, "#1d1d22"); ctx.set_line_width(0.022); ctx.stroke()
            ctx.move_to(sx * 0.2 + fx - 0.08, -0.04); ctx.line_to(sx * 0.2 + fx - 0.02, -0.07)
            src(ctx, "#ffffff", 0.7); ctx.set_line_width(0.015); ctx.stroke()
        ctx.move_to(-0.06 + fx, -0.01); ctx.line_to(0.06 + fx, -0.01); src(ctx, "#1d1d22"); ctx.set_line_width(0.02); ctx.stroke()
    if st["sweat"] > 0.01:
        sx = 0.38 + fx
        smooth(ctx, [(sx, -0.25), (sx + 0.04, -0.13), (sx, -0.1), (sx - 0.04, -0.13)], True, 0.5)
        src(ctx, "#9fd8ff", st["sweat"]); ctx.fill()


def draw_hair_front(ctx, c, st):
    s = c["style"]
    hc, hh = c["hair"], c["hair_hi"]
    sw = st["sway"] * 0.02
    t = st["turn"] * 0.1
    if s == "spiky" or s == "messy":
        bangs = [(-0.5, -0.45, -0.46, 0.0), (-0.36, -0.5, -0.3, -0.08), (-0.2, -0.55, -0.12, -0.12),
                 (-0.02, -0.56, 0.04, -0.06), (0.16, -0.55, 0.22, -0.14), (0.32, -0.5, 0.36, -0.06),
                 (0.46, -0.45, 0.5, 0.02)]
        cap = [(-0.55, -0.2), (-0.53, -0.5), (-0.3, -0.72), (0.05, -0.76), (0.38, -0.66), (0.55, -0.45), (0.55, -0.2), (0.0, -0.45)]
        smooth(ctx, cap, True, 0.45); src(ctx, hc); ctx.fill()
        for (x0, y0, x1, y1) in bangs:
            poly(ctx, [(x0 - 0.1 + t, y0), (x1 + sw + t, y1), (x0 + 0.11 + t, y0 - 0.02)]); src(ctx, hc); ctx.fill()
        # ring highlight
        ctx.save(); smooth(ctx, cap, True, 0.45); ctx.clip()
        for k in range(5):
            x = -0.35 + k * 0.16 + t
            poly(ctx, [(x - 0.05, -0.6), (x + 0.03, -0.62), (x + 0.0, -0.48)]); src(ctx, hh, 0.85); ctx.fill()
        ctx.restore()
        if c.get("streak"):
            poly(ctx, [(0.16 + t, -0.66), (0.24 + t, -0.64), (0.19 + t, -0.45), (0.26 + t, -0.44), (0.15 + t, -0.16), (0.17 + t, -0.38), (0.11 + t, -0.4)])
            src(ctx, "#f5f2ff"); ctx.fill()
    elif s == "long":
        cap = [(-0.56, -0.05), (-0.55, -0.5), (-0.28, -0.74), (0.12, -0.76), (0.45, -0.62), (0.57, -0.35), (0.56, 0.05), (0.3, -0.35), (0.05, -0.42), (-0.25, -0.3)]
        smooth(ctx, cap, True, 0.45); src(ctx, hc); ctx.fill()
        # side swept bangs
        for (x0, x1, y1) in [(-0.1, -0.34, -0.05), (0.05, -0.12, -0.1), (0.2, 0.12, -0.15), (0.34, 0.4, -0.02)]:
            smooth(ctx, [(x0 - 0.12 + t, -0.5), (x1 + sw + t, y1), (x0 + 0.12 + t, -0.5)], True, 0.3); src(ctx, hc); ctx.fill()
        # side locks
        for sx in (-1, 1):
            smooth(ctx, [(sx * 0.42, -0.4), (sx * 0.5 + sw, 0.3), (sx * 0.46 + sw, 0.8), (sx * 0.38, 0.35), (sx * 0.36, -0.3)], True, 0.45)
            src(ctx, hc); ctx.fill()
        ctx.save(); smooth(ctx, cap, True, 0.45); ctx.clip()
        ctx.arc(0.0, -0.1, 0.52, math.pi * 1.15, math.pi * 1.6); src(ctx, hh, 0.9); ctx.set_line_width(0.05); ctx.stroke()
        ctx.restore()
        # hair clip
        rrect(ctx, 0.3, -0.5, 0.12, 0.04, 0.02); src(ctx, "#ffd45a"); ctx.fill()
    elif s == "bun":
        # middle parting
        smooth(ctx, [(-0.5, -0.05), (-0.48, -0.45), (-0.2, -0.68), (0.0, -0.6), (0.2, -0.68), (0.48, -0.45), (0.5, -0.05),
                     (0.36, -0.35), (0.05, -0.5), (0.0, -0.45), (-0.05, -0.5), (-0.36, -0.35)], True, 0.45)
        src(ctx, hc); ctx.fill()
        ctx.move_to(0, -0.62); ctx.line_to(0, -0.47); src(ctx, "#c4122a"); ctx.set_line_width(0.03); ctx.stroke()
        ctx.arc(-0.18, -0.35, 0.3, math.pi * 1.2, math.pi * 1.5); src(ctx, hh, 0.7); ctx.set_line_width(0.03); ctx.stroke()
    elif s == "side":
        smooth(ctx, [(-0.52, -0.1), (-0.5, -0.5), (-0.2, -0.72), (0.2, -0.72), (0.5, -0.52), (0.53, -0.15), (0.4, -0.38), (-0.1, -0.45), (-0.38, -0.36)], True, 0.45)
        src(ctx, hc); ctx.fill()
        ctx.move_to(-0.2, -0.7); ctx.curve_to(-0.15, -0.6, -0.1, -0.5, -0.12, -0.45); src(ctx, shade(hc, 0.3)); ctx.set_line_width(0.02); ctx.stroke()
        # grey temples
        for sx in (-1, 1):
            ellipse(ctx, sx * 0.48, -0.2, 0.04, 0.09); src(ctx, "#9a9aa2", 0.8); ctx.fill()
    elif s == "hood":
        # hood brim shadow over forehead
        smooth(ctx, [(-0.56, -0.05), (-0.5, -0.55), (0.0, -0.7), (0.5, -0.55), (0.56, -0.05), (0.3, -0.3), (0.0, -0.36), (-0.3, -0.3)], True, 0.45)
        src(ctx, "#040406"); ctx.fill()


def draw_char(ctx, name, x, y, s, st=None, flip=False):
    """Draw bust with face center at (x, y), head height s px."""
    c = CAST[name] if isinstance(name, str) else name
    st = _st(st)
    ctx.save()
    ctx.translate(x, y + st["breathe"] * s * 0.01)
    ctx.scale(s * (-1 if flip else 1), s)
    draw_hair_back(ctx, c, st)
    draw_body(ctx, c, st)
    draw_face(ctx, c, st)
    draw_hair_front(ctx, c, st)
    if c["style"] == "hood":
        # face half lost in the hood's shadow
        ctx.save(); face_path(ctx, 0); ctx.clip()
        lin(ctx, 0, -0.6, 0, 0.5, [(0, (0, 0, 0, 0.92)), (0.55, (0, 0, 0, 0.75)), (1, (0, 0, 0, 0.35))]); ctx.paint()
        ctx.restore()
        if st["glow"] > 0:
            for sx in (-1, 1):
                ellipse(ctx, sx * 0.2, 0.03, 0.09, 0.06); src(ctx, "#ff3a3a", st["glow"]); ctx.fill()
                ellipse(ctx, sx * 0.2, 0.03, 0.04, 0.03); src(ctx, "#fff0f0", st["glow"]); ctx.fill()
    ctx.restore()


def blink_at(t, seed=0, period=3.1):
    """returns blink amount for time t (seconds)."""
    ph = (t + seed * 1.37) % period
    if ph < 0.12:
        return math.sin(ph / 0.12 * math.pi)
    return 0.0


def talk(t, t0, t1, seed=0):
    if t < t0 or t > t1:
        return 0.0
    v = abs(math.sin((t - t0) * 17 + seed)) * (0.55 + 0.45 * abs(noise1((t - t0) * 6, seed)))
    return v
