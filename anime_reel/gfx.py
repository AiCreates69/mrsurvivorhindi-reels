"""Drawing helpers: cairo paths, gradients, PIL text sprites, cairo<->numpy, post FX."""
import math, os, functools
import numpy as np
import cairo
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FPS = 24
FONT_DIR = "/root/.claude/plugins/synced/c29a5480-5996-4792-9093-519cf806c241_5b58f0bf-591b-47f7-8d17-aaa1fddc18a2/code-reels-studio/assets/fonts"
FONT_DIR = os.environ.get("REEL_FONTS", FONT_DIR)
F_ANTON = os.path.join(FONT_DIR, "Anton-Regular.ttf")
F_POP = os.path.join(FONT_DIR, "Poppins-ExtraBold.ttf")
F_POPB = os.path.join(FONT_DIR, "Poppins-Black.ttf")


def hexc(h, a=1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


def mix(c1, c2, k):
    c1 = hexc(c1) if isinstance(c1, str) else c1
    c2 = hexc(c2) if isinstance(c2, str) else c2
    return tuple(a + (b - a) * k for a, b in zip(c1, c2))


def shade(c, k):
    """k<0 darker, k>0 lighter."""
    c = hexc(c) if isinstance(c, str) else c
    if k < 0:
        return tuple(v * (1 + k) for v in c[:3]) + (c[3] if len(c) > 3 else 1,)
    return tuple(v + (1 - v) * k for v in c[:3]) + (c[3] if len(c) > 3 else 1,)


def src(ctx, c, a=None):
    c = hexc(c) if isinstance(c, str) else c
    if len(c) == 3:
        c = c + (1,)
    ctx.set_source_rgba(c[0], c[1], c[2], c[3] if a is None else a)


def lin(ctx, x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for o, c in stops:
        c = hexc(c) if isinstance(c, str) else c
        if len(c) == 3:
            c = c + (1,)
        g.add_color_stop_rgba(o, *c)
    ctx.set_source(g)
    return g


def rad(ctx, x, y, r0, r1, stops):
    g = cairo.RadialGradient(x, y, r0, x, y, r1)
    for o, c in stops:
        c = hexc(c) if isinstance(c, str) else c
        if len(c) == 3:
            c = c + (1,)
        g.add_color_stop_rgba(o, *c)
    ctx.set_source(g)
    return g


def smooth(ctx, pts, closed=True, tension=0.5):
    """Catmull-Rom spline through points as cubic beziers."""
    n = len(pts)
    if n < 2:
        return
    ctx.move_to(*pts[0])
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        k = tension / 3 * 2
        c1 = (p1[0] + (p2[0] - p0[0]) * k / 2, p1[1] + (p2[1] - p0[1]) * k / 2)
        c2 = (p2[0] - (p3[0] - p1[0]) * k / 2, p2[1] - (p3[1] - p1[1]) * k / 2)
        ctx.curve_to(*c1, *c2, *p2)
    if closed:
        ctx.close_path()


def poly(ctx, pts):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()


def ellipse(ctx, x, y, rx, ry, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(max(rx, 1e-3), max(ry, 1e-3))
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def back_out(x, s=1.7):
    x = min(1.0, max(0.0, x)) - 1
    return x * x * ((s + 1) * x + s) + 1


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ramp(t, a, b):
    if b <= a:
        return 1.0 if t >= a else 0.0
    return clamp((t - a) / (b - a))


def noise1(x, seed=0):
    """cheap smooth 1D value noise in [-1,1]."""
    i = math.floor(x)
    f = x - i

    def h(n):
        n = (n * 374761393 + seed * 668265263) & 0xFFFFFFFF
        n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
        return ((n ^ (n >> 16)) & 0xFFFF) / 32767.5 - 1

    u = f * f * (3 - 2 * f)
    return h(i) * (1 - u) + h(i + 1) * u


# ------------------------------------------------------------------ surfaces
def new_surface(w=W, h=H):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w), int(h))
    return s, cairo.Context(s)


def surf_to_np(s):
    """cairo ARGB32 (premultiplied BGRA) -> float32 RGB (opaque assumed)."""
    s.flush()
    a = np.ndarray((s.get_height(), s.get_stride() // 4, 4), np.uint8, s.get_data())[:, : s.get_width()]
    return a[..., [2, 1, 0]].astype(np.float32) / 255.0


def surf_to_rgba(s):
    s.flush()
    a = np.ndarray((s.get_height(), s.get_stride() // 4, 4), np.uint8, s.get_data())[:, : s.get_width()]
    rgba = a[..., [2, 1, 0, 3]].astype(np.float32) / 255.0
    al = rgba[..., 3:4]
    rgba[..., :3] = np.where(al > 0, rgba[..., :3] / np.maximum(al, 1e-6), 0)
    return rgba


def np_to_surf(rgb):
    h, w = rgb.shape[:2]
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    a = np.ndarray((h, s.get_stride() // 4, 4), np.uint8, s.get_data())
    u8 = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    a[:, :w, 0] = u8[..., 2]
    a[:, :w, 1] = u8[..., 1]
    a[:, :w, 2] = u8[..., 0]
    a[:, :w, 3] = 255
    s.mark_dirty()
    return s


def blur_np(img, r):
    """Gaussian-ish blur on float RGB via PIL (downscale trick for big radii)."""
    if r <= 0:
        return img
    h, w = img.shape[:2]
    k = 1
    while r / k > 12 and min(h, w) / (k * 2) > 32:
        k *= 2
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    if k > 1:
        im = im.resize((max(1, w // k), max(1, h // k)), Image.BILINEAR)
    im = im.filter(ImageFilter.GaussianBlur(r / k))
    if k > 1:
        im = im.resize((w, h), Image.BILINEAR)
    return np.asarray(im).astype(np.float32) / 255.0


# ------------------------------------------------------------------ text sprites
@functools.lru_cache(maxsize=64)
def font(path, size):
    return ImageFont.truetype(path, size)


@functools.lru_cache(maxsize=256)
def text_sprite(text, fpath, size, fill="#ffffff", stroke=0, stroke_fill="#000000", glow=0, glow_col=None, pad=None,
                max_w=None, spacing=0):
    """RGBA float sprite (premultiplied not used; straight alpha) of multi-line centered text with optional glow."""
    f = font(fpath, size)
    lines = text.split("\n")
    asc, desc = f.getmetrics()
    lh = asc + desc + spacing
    widths = [f.getlength(l) for l in lines]
    tw = int(max(widths)) + 2 * stroke
    th = lh * len(lines) + 2 * stroke
    pad = pad if pad is not None else int(glow * 2.5 + 8)
    im = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fc = tuple(int(v * 255) for v in hexc(fill)[:3]) + (255,)
    sc = tuple(int(v * 255) for v in hexc(stroke_fill)[:3]) + (255,)
    for i, l in enumerate(lines):
        x = pad + stroke + (tw - 2 * stroke - widths[i]) / 2
        y = pad + stroke + i * lh
        d.text((x, y), l, font=f, fill=fc, stroke_width=stroke, stroke_fill=sc)
    if glow:
        gc = hexc(glow_col or fill)
        a = im.split()[3].filter(ImageFilter.GaussianBlur(glow))
        g = Image.new("RGBA", im.size, tuple(int(v * 255) for v in gc[:3]) + (0,))
        g.putalpha(a.point(lambda v: min(255, int(v * 1.8))))
        g.alpha_composite(im)
        im = g
    return np.asarray(im).astype(np.float32) / 255.0


def comp(dst, spr, cx, cy, alpha=1.0, scale=1.0, add=False):
    """Composite RGBA sprite centered at (cx,cy) onto float RGB dst in place."""
    if alpha <= 0.003:
        return
    if abs(scale - 1) > 0.01:
        h, w = spr.shape[:2]
        im = Image.fromarray((spr * 255).astype(np.uint8), "RGBA").resize(
            (max(1, int(w * scale)), max(1, int(h * scale))), Image.BILINEAR)
        spr = np.asarray(im).astype(np.float32) / 255.0
    h, w = spr.shape[:2]
    x0 = int(round(cx - w / 2))
    y0 = int(round(cy - h / 2))
    X0, Y0 = max(0, x0), max(0, y0)
    X1, Y1 = min(dst.shape[1], x0 + w), min(dst.shape[0], y0 + h)
    if X1 <= X0 or Y1 <= Y0:
        return
    s = spr[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    a = s[..., 3:4] * alpha
    d = dst[Y0:Y1, X0:X1]
    if add:
        d += s[..., :3] * a
    else:
        d[:] = d * (1 - a) + s[..., :3] * a


# ------------------------------------------------------------------ post FX
_VIG = None
_GRAIN = None


def vignette_mask():
    global _VIG
    if _VIG is None:
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H / 2) / (H * 0.58)) ** 2)
        _VIG = np.clip(1 - (d - 0.55) * 0.75, 0.35, 1)[..., None].astype(np.float32)
    return _VIG


def grain(i):
    global _GRAIN
    if _GRAIN is None:
        rng = np.random.default_rng(7)
        _GRAIN = [rng.normal(0, 1, (H // 2, W // 2, 1)).astype(np.float32) for _ in range(6)]
    g = _GRAIN[i % 6]
    return np.repeat(np.repeat(g, 2, 0), 2, 1)


def bloom(img, thr=0.72, strength=0.5, radius=28, tint=None):
    small = img[::4, ::4]
    b = np.clip((small - thr) / (1 - thr), 0, 1)
    b = blur_np(b, radius / 4)
    im = Image.fromarray((b * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    b = np.asarray(im).astype(np.float32) / 255.0
    if tint is not None:
        b = b * np.array(tint[:3], np.float32)
    return 1 - (1 - img) * (1 - b * strength)


def chroma(img, px):
    if px < 1:
        return img
    px = int(px)
    out = img.copy()
    out[:, px:, 0] = img[:, :-px, 0]
    out[:, :-px, 2] = img[:, px:, 2]
    return out


def slice_glitch(img, amount, seed, y0=0, y1=H):
    if amount <= 0:
        return img
    rng = np.random.default_rng(seed)
    out = img.copy()
    for _ in range(int(4 + amount * 10)):
        y = rng.integers(y0, max(y0 + 1, y1 - 10))
        hh = int(rng.integers(6, 60))
        dx = int(rng.normal(0, 40 * amount))
        out[y:y + hh] = np.roll(img[y:y + hh], dx, axis=1)
    return out
