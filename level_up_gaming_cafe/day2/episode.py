"""EPISODE: Level Up Gaming Cafe — Day 2   (@tumhoboss)
B (Inverter) won Decision #1. Numbers below come from Instagram; update them and re-render.
Render:  python -m srs.engine path/to/episode.py [--sheet | --frames 3.0,20.5]
"""
import math
import cairo
from srs import art
from srs.art import W, H, src, rrect, fill_stroke, ease, eout, bout, pop_scale, SKIN, INK
from srs.engine import lt_, cam, paint_bg

TITLE = "Level Up Gaming Cafe — Day 2"
OUTPUT = "Level_Up_Gaming_Cafe_Day2.mp4"
VOICE = "hm_omega"
END_HOLD = 1.8

# ---------------- real numbers (update after the final count) ----------------
FOLLOWERS = 82
LIKES = 147
FUND_START = 2000
FUND = FUND_START + LIKES*100            # 16,700
VOTES = {"A": 4, "B": 10, "C": 4}
VIP_NAMES = ["rmenghare_19", "urfavv.sanford28._", "justt_yachass_15", "mohammed335060", "alimurtaza2015.2026"]
IDEA_BY = "typelovnish"
INVESTOR_BY = "rsz_rehan_sheikh"

# ---------------- cast (matches Day 1) ----------------
MANAGER = dict(skin=SKIN["m"], hair="side", hair_col="#1d1714", shirt="#f3efe3", jacket="#e2862b", pants="#2f4f7a",
               shoes="#f2f2ee", lanyard=True, prop="notepad", seed=1)
CHINTU = dict(skin=SKIN["d"], hair="curly", hair_col="#1d1714", shirt="#2f6db0", pants="#3a3a42", shoes="#f2f2ee", seed=2)
LUCKY = dict(skin=SKIN["m"], hair="side", shirt="#1d1d22", stripes=["#1d1d22", "#1d1d22", "#c7262f", "#1d1d22"],
             pants="#5a5a62", cap="#c7262f", shoes="#f2f2ee", seed=3)
PINKY = dict(skin=SKIN["m"], hair="none", shirt="#e85a9a", pants="#2f4f7a", shoes="#f2f2ee", seed=4)
INVESTOR = dict(skin=SKIN["l"], hair="side", hair_col="#2a2a2a", shirt="#f3efe3", jacket="#2b2b33", pants="#2b2b33",
                shoes="#1b1b1b", glasses=True, mustache=True, fat=.6, seed=5)
PRO = [dict(skin=s, hair=h, shirt="#6a3fc4", stripes=["#6a3fc4", "#6a3fc4", "#ffffff"], pants="#2b2b33",
            band="#ffd21f", shoes="#f2f2ee", seed=6+i, brow_tilt=-4, smile=-.2)
       for i, (s, h) in enumerate(((SKIN["l"], "spiky"), (SKIN["d"], "side"), (SKIN["m"], "curly")))]

# ---------------- script ----------------
LINES = [
 ("open",     "हे! कल तुमने वोट किया... आज डे टू!",            "Hey! Kal *vote* kiya... aaj *Day 2*!"),
 ("result",   "सबसे ज़्यादा वोट... बी! इन्वर्टर!",              "Sabse zyada vote... *B*! *Inverter*!"),
 ("vip",      "बयासी फॉलोअर्स... सब वी आई पी सीट पे!",         "*82 followers*... sab VIP seat pe!"),
 ("fund",     "एक सौ सैंतालीस लाइक्स... फंड सोलह हज़ार सात सौ!", "*147 likes*... fund *16,700*!"),
 ("inverter", "इन्वर्टर आ गया... लेकिन सेकंड हैंड!",             "Inverter aaya... lekin *second hand*!"),
 ("pcs",      "चलाता है सिर्फ... दो पीसी और एक पंखा!",          "Chalata hai sirf... *2 PC* aur *pankha*!"),
 ("chai",     "कमेंट वाला आइडिया... मशीन का नाम, चाय!",          "Comment wala idea... naam *Chai*!"),
 ("investor", "इन्वेस्टर आया, सौ करोड़... फिर बोला, चाय उधार!",   "Investor: *100 crore*... phir *chai udhaar*!"),
 ("prozone",  "शाम को... प्रो ज़ोन आ गया! तीन वर्सेस तीन!",      "Shaam ko... *Pro Zone* aa gaya! 3 vs 3!"),
 ("blackout", "मैच शुरू... और लाइट गई!",                      "Match shuru... aur *light gayi*!"),
 ("blackout", "इन्वर्टर ने... बचा लिया!",                       "Inverter ne... *bacha liya*!"),
 ("lucky",    "पर लकी को... दादी का फ़ोन!",                    "Par Lucky ko... *dadi* ka phone!"),
 ("lucky",    "और लकी... घर भाग गया!",                        "Aur Lucky... *ghar bhaag* gaya!"),
 ("decide",   "तीसरा प्लेयर कौन?",                            "Teesra *player* kaun?"),
 ("decide",   "मैनेजर खुद खेलेगा,",                           "*Manager* khud khelega,"),
 ("decide",   "प्रो गेमर हायर करो,",                          "*Pro gamer* hire karo,"),
 ("decide",   "या कुछ और?",                                  "Ya kuch *aur*?"),
 ("decide",   "सबसे ज़्यादा वोट वाला जीतेगा!",                  "Sabse zyada *vote* wala jeetega!"),
 ("decide",   "बॉस... तुम हो!",                              "Boss... *tum* ho!"),
]

SHOTS = [
 ("open", "cut"), ("result", "wipe"), ("vip", "wipe"), ("fund", "whip"), ("inverter", "iris"), ("pcs", "cut"),
 ("chai", "whip"), ("investor", "whip"), ("prozone", "wipe"), ("blackout", "iris"), ("lucky", "whip"), ("decide", "iris"),
]

# ---------------- sets ----------------
def _grad(c, y0, y1, a, b):
    g = cairo.LinearGradient(0, y0, 0, y1); g.add_color_stop_rgb(0, *art.rgb(a)[:3]); g.add_color_stop_rgb(1, *art.rgb(b)[:3])
    c.set_source(g); c.rectangle(0, y0, W, y1-y0); c.fill()

def _neon(c, x0, y, x1, col, w=6):
    for lw, a in ((w*5, .12), (w*2.5, .25), (w, 1)):
        src(c, col, a); c.set_line_width(lw); c.move_to(x0, y); c.line_to(x1, y); c.stroke()

def _glow_text(c, txt, x, y, size, col, k="lucky"):
    for st, a in ((14, .15), (8, .3)):
        art.text(c, ((txt, col),), k, size, x, y, stroke=st, scol=col, alpha=a)
    art.text(c, ((txt, "#ffffff"),), k, size, x, y, stroke=3, scol=col)

def _monitor(c, x, y, on, kind=0):
    rrect(c, x-56, y-44, 112, 76, 6); fill_stroke(c, "#20202a", INK, 3)
    if on:
        if kind == 0:
            _grad(c, 0, 0, "#000", "#000")
            g = cairo.LinearGradient(0, y-38, 0, y+26); g.add_color_stop_rgb(0, .35, .75, 1); g.add_color_stop_rgb(1, .3, .8, .45)
            c.set_source(g); c.rectangle(x-50, y-38, 100, 64); c.fill()
            src(c, "#ffd21f"); c.arc(x-20, y-6, 8, 0, 6.3); c.fill(); src(c, "#e8304a"); c.rectangle(x+10, y-14, 16, 16); c.fill()
        else:
            src(c, "#2f6db0"); c.rectangle(x-50, y-38, 100, 64); c.fill()
            art.text(c, ((":(", "#ffffff"),), "popx", 22, x-26, y-14)
    else:
        src(c, "#08080c"); c.rectangle(x-50, y-38, 100, 64); c.fill()
        src(c, "#ffffff", .08); c.move_to(x-44, y-34); c.line_to(x-10, y-34); c.line_to(x-40, y+20); c.close_path(); c.fill()
    c.rectangle(x-8, y+32, 16, 18); fill_stroke(c, "#20202a", INK, 2.5)
    rrect(c, x-30, y+48, 60, 8, 3); fill_stroke(c, "#20202a", INK, 2.5)

MON_X = [72, 216, 360, 504, 648]
ON_PCS = (1, 3)

def set_cafe(on=ON_PCS):
    s, c = art._canvas()
    _grad(c, 0, 640, "#1c1436", "#3b2a63")
    src(c, "#ffffff", .03)
    for x in range(0, W, 48): c.rectangle(x, 0, 2, 640); c.fill()
    _neon(c, 0, 52, W, "#ff3fa4"); _neon(c, 0, 70, W, "#3fd8ff", 4)
    # posters
    c.save(); c.translate(120, 210); c.rotate(-.03)
    rrect(c, -70, -95, 140, 190, 6); fill_stroke(c, "#ffd21f", INK, 4)
    art.text(c, (("GAME", "#c7262f"),), "lucky", 38, 0, -50); art.text(c, (("NIGHT", "#c7262f"),), "lucky", 38, 0, -8)
    art.text(c, (("SAT 9 PM", "#2a1608"),), "lilita", 20, 0, 60); c.restore()
    rrect(c, 290, 130, 140, 50, 8); fill_stroke(c, "#e9edf0", INK, 3)
    src(c, "#9aa3a6"); [c.rectangle(300, y, 120, 3) or c.fill() for y in range(150, 176, 7)]
    art.tag(c, "AC: OUT OF ORDER", 360, 205, "#c7262f", size=13)
    rrect(c, 470, 120, 200, 110, 10); fill_stroke(c, "#120c22", "#ff3fa4", 4)
    _glow_text(c, "LEVEL UP", 570, 175, 42, "#ff3fa4")
    # desk + monitors
    for i, x in enumerate(MON_X): _monitor(c, x, 480, i in on, kind=0 if i % 2 else 1)
    c.rectangle(0, 535, W, 22); fill_stroke(c, "#4a2f22", INK, 4)
    src(c, "#2b1c14"); c.rectangle(0, 557, W, 90); c.fill()
    # chairs
    for i, x in enumerate(MON_X):
        col = "#2f6db0" if i % 2 == 0 else "#c7262f"
        rrect(c, x-36, 600, 72, 150, 16); fill_stroke(c, "#16161c", INK, 4)
        src(c, col); c.rectangle(x-26, 612, 12, 126); c.fill(); c.rectangle(x+14, 612, 12, 126); c.fill()
    # floor
    _grad(c, 640, H, "#3a3048", "#5a4a5e")
    src(c, "#ffffff", .07); c.set_line_width(2)
    for k in range(-8, 9): c.move_to(W/2+k*40, 640); c.line_to(W/2+k*190, H); c.stroke()
    for y in (700, 790, 910, 1070): c.move_to(0, y); c.line_to(W, y); c.stroke()
    src(c, "#ff3fa4", .12); art.ell(c, W/2, 760, 300, 30); c.fill()
    return art.finish(art.surf_to_pil(s), grain=5)

def set_street():
    s, c = art._canvas()
    _grad(c, 0, 760, "#1a1236", "#5a2f6a")
    for i, (bx, bw, bh) in enumerate(((0, 170, 520), (150, 140, 600), (560, 170, 560))):
        src(c, "#251a3e"); c.rectangle(bx, 760-bh, bw, bh); c.fill()
        for r in range(int(bh/44)-2):
            for k in range(int(bw/34)):
                if (r*7+k*3+i) % 4: src(c, "#ffd27a", .85)
                else: src(c, "#3a2c56")
                c.rectangle(bx+12+k*34, 760-bh+20+r*44, 18, 24); c.fill()
    # mobile shop
    c.rectangle(0, 560, 130, 260); fill_stroke(c, "#e9e2d0", INK, 4)
    rrect(c, 4, 520, 150, 46, 6); fill_stroke(c, "#2e9b5a", INK, 3); art.text(c, (("MOBILE", "#ffffff"),), "lilita", 24, 78, 543)
    src(c, "#9aa3a6"); [c.rectangle(10, y, 110, 4) or c.fill() for y in range(580, 800, 14)]
    # cafe front
    c.rectangle(150, 470, 570, 360); fill_stroke(c, "#2a1f44", INK, 4)
    rrect(c, 170, 340, 380, 120, 12); fill_stroke(c, "#120c22", "#ff3fa4", 5)
    _glow_text(c, "LEVEL UP", 360, 385, 64, "#ff3fa4"); art.text(c, (("GAMING CAFE", "#7fe8ff"),), "lilita", 22, 360, 437)
    c.rectangle(170, 500, 530, 300); fill_stroke(c, "#3a5a8a", INK, 4)
    src(c, "#7fd0ff", .25); c.rectangle(170, 500, 530, 300); c.fill()
    for i, x in enumerate((260, 380, 500, 620)): _monitor(c, x, 640, i in (1, 3), kind=0)
    src(c, "#ffffff", .15); c.move_to(190, 510); c.line_to(300, 510); c.line_to(200, 780); c.close_path(); c.fill()
    art.tag(c, "₹30 / HOUR", 260, 740, "#ffd21f", "#1b1208", 16, border="#1b1208")
    # pavement
    _grad(c, 820, H, "#3a2f4a", "#6a5070")
    src(c, "#ff3fa4", .12); art.ell(c, 400, 900, 260, 30); c.fill()
    src(c, "#7fe8ff", .08); art.ell(c, 380, 1000, 300, 26); c.fill()
    src(c, "#ffffff", .06); c.set_line_width(2)
    for y in (880, 960, 1080, 1220): c.move_to(0, y); c.line_to(W, y); c.stroke()
    g = cairo.RadialGradient(360, 380, 0, 360, 380, 520); g.add_color_stop_rgba(0, 1, .3, .7, .22); g.add_color_stop_rgba(1, 1, .3, .7, 0)
    c.set_source(g); c.paint()
    return art.finish(art.surf_to_pil(s), grain=5)

def _gchair(c, x, y, s, col):
    c.save(); c.translate(x, y); c.scale(s, s)
    rrect(c, -70, -300, 140, 230, 30); fill_stroke(c, "#16161c", INK, 4)
    src(c, col); rrect(c, -40, -280, 80, 60, 14); c.fill(); c.rectangle(-58, -200, 18, 120); c.fill(); c.rectangle(40, -200, 18, 120); c.fill()
    rrect(c, -90, -90, 180, 46, 14); fill_stroke(c, "#16161c", INK, 4)
    c.rectangle(-8, -44, 16, 50); fill_stroke(c, "#333", INK, 3)
    for k in (-60, 0, 60): art.ell(c, k, 14, 16, 8); fill_stroke(c, "#333", INK, 2.5)
    art.text(c, (("VIP", "#ffd21f"),), "lucky", 26, 0, -250)
    c.restore()

def set_vip():
    s, c = art._canvas()
    _grad(c, 0, 760, "#1a1236", "#3b2a63")
    _neon(c, 0, 60, W, "#ffd21f", 5)
    _grad(c, 760, H, "#2a2238", "#4a3a52")
    for k, x in enumerate((140, 360, 580)):
        g = cairo.LinearGradient(x, 0, x, 900)
        c.move_to(x-40, 60); c.line_to(x+40, 60); c.line_to(x+140, 900); c.line_to(x-140, 900); c.close_path()
        g.add_color_stop_rgba(0, 1, .95, .7, .32); g.add_color_stop_rgba(1, 1, .95, .7, .02); c.set_source(g); c.fill()
        src(c, "#fff3c0", .18); art.ell(c, x, 905, 150, 30); c.fill()
        _gchair(c, x, 900, .9, "#c7262f" if k != 1 else "#ffd21f")
    for px in (40, 680):
        c.rectangle(px-6, 860, 12, 150); fill_stroke(c, "#d6a93a", INK, 3)
        c.arc(px, 855, 14, 0, 6.3); fill_stroke(c, "#e8c25a", INK, 3)
    src(c, INK); c.set_line_width(14); c.move_to(40, 872); c.curve_to(250, 960, 470, 960, 680, 872); c.stroke()
    src(c, "#7a2fb0"); c.set_line_width(9); c.move_to(40, 872); c.curve_to(250, 960, 470, 960, 680, 872); c.stroke()
    return art.finish(art.surf_to_pil(s), grain=5)

BACKGROUNDS = {
    "street": set_street,
    "cafe": set_cafe,
    "cafe_off": lambda: set_cafe(on=()),
    "vip": set_vip,
    "blur": lambda: art.blurred(set_cafe(), 8, .7),
    "blur2": lambda: art.blurred(set_cafe(), 11, .6),
    "blur_street": lambda: art.blurred(set_street(), 9, .65),
}
CAP_Y = {"decide": 1090, "result": 1110, "vip": 1110, "pcs": 1110, "blackout": 1110, "prozone": 1150, "chai": 1150,
         "investor": 1150, "lucky": 1150, "inverter": 1150}

# ---------------- extra drawing ----------------
def head_pos(x, y, s): return x, y - 525*s

def headphones(ctx, x, y, s, flip=False):
    hx, hy = head_pos(x, y, s)
    ctx.save(); ctx.translate(hx, hy); ctx.scale(s, s)
    src(ctx, INK); ctx.set_line_width(20); ctx.arc(0, 0, 92, math.pi*1.08, math.pi*1.92); ctx.stroke()
    src(ctx, "#2b2b33"); ctx.set_line_width(12); ctx.arc(0, 0, 92, math.pi*1.08, math.pi*1.92); ctx.stroke()
    for side in (-1, 1):
        rrect(ctx, side*82-16, -14, 32, 58, 12); fill_stroke(ctx, "#2b2b33", INK, 3.5)
        src(ctx, "#3fd8ff"); rrect(ctx, side*82-6, -2, 12, 34, 5); ctx.fill()
    ctx.restore()

def pinky_hair_back(ctx, x, y, s):
    hx, hy = head_pos(x, y, s)
    ctx.save(); ctx.translate(hx, hy); ctx.scale(s, s)
    art.ell(ctx, 0, 10, 86, 110); fill_stroke(ctx, "#1d1714")
    ctx.move_to(60, 20); ctx.curve_to(120, 80, 110, 170, 70, 210); ctx.curve_to(80, 150, 70, 90, 40, 60); ctx.close_path(); fill_stroke(ctx, "#1d1714")
    ctx.restore()

def pinky_hair_front(ctx, x, y, s):
    hx, hy = head_pos(x, y, s)
    ctx.save(); ctx.translate(hx, hy); ctx.scale(s, s)
    ctx.move_to(-74, 0); ctx.curve_to(-80, -110, 80, -110, 74, 0); ctx.curve_to(60, -56, 10, -66, 0, -60)
    ctx.curve_to(-10, -66, -60, -56, -74, 0); ctx.close_path(); fill_stroke(ctx, "#1d1714")
    src(ctx, "#d23b3b"); ctx.arc(0, -46, 6, 0, 6.3); ctx.fill()
    ctx.restore()

def draw_pinky(ctx, x, y, s, pose, t, mouth=0):
    pinky_hair_back(ctx, x, y, s)
    art.person(ctx, x, y, s, PINKY, pose, t=t, mouth=mouth)
    pinky_hair_front(ctx, x, y, s)

def draw_lucky(ctx, x, y, s, pose, t, mouth=0, flip=False):
    art.person(ctx, x, y, s, LUCKY, pose, t=t, mouth=mouth, flip=flip)
    headphones(ctx, x, y, s)

def cat(ctx, x, y, s, t, awake=False):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    br = math.sin(t*2.2)*3
    art.ell(ctx, 0, -60, 150, 62+br); fill_stroke(ctx, "#e8913a")
    src(ctx, "#c56a22")
    for k in range(5): rrect(ctx, 10+k*26, -118-br, 12, 46, 6); ctx.fill()
    ctx.move_to(130, -30); ctx.curve_to(190, -10, 150, 20, 60, 6); src(ctx, INK); ctx.set_line_width(26); ctx.stroke_preserve(); src(ctx, "#e8913a"); ctx.set_line_width(19); ctx.stroke()
    art.ell(ctx, -120, -70, 70, 58); fill_stroke(ctx, "#e8913a")
    for side in (-1, 1):
        art.poly(ctx, [(-120+side*48, -100), (-120+side*30, -150), (-120+side*12, -112)]); fill_stroke(ctx, "#e8913a")
    src(ctx, "#ffe2c4"); art.ell(ctx, -120, -50, 36, 20); ctx.fill()
    src(ctx, INK); ctx.set_line_width(4)
    for side in (-1, 1):
        if awake: ctx.arc(-120+side*24, -78, 8, 0, 6.3); ctx.fill()
        else: ctx.move_to(-132+side*24+12, -78); ctx.curve_to(-126+side*24+12, -70, -114+side*24+12-12, -70, -110+side*24, -78); ctx.stroke()
    src(ctx, "#e85a7a"); art.ell(ctx, -120, -60, 7, 5); ctx.fill()
    ctx.restore()

def inverter(ctx, x, y, s, t, beep=False, fail=False):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, 110, -150, 120, 150, 10); fill_stroke(ctx, "#2a2a30")      # battery
    for k, col in ((140, "#c7262f"), (200, "#1b1b1b")): rrect(ctx, k-12, -168, 24, 20, 4); fill_stroke(ctx, col)
    art.text(ctx, (("BATTERY", "#9aa3a6"),), "lilita", 18, 170, -70)
    src(ctx, INK); ctx.set_line_width(7); ctx.move_to(140, -168); ctx.curve_to(120, -220, 60, -220, 40, -180); ctx.stroke()
    src(ctx, "#c7262f"); ctx.set_line_width(4); ctx.move_to(140, -168); ctx.curve_to(120, -220, 60, -220, 40, -180); ctx.stroke()
    rrect(ctx, -150, -190, 260, 190, 14); fill_stroke(ctx, "#d9d2c0")    # inverter body
    src(ctx, "#b8b09a"); [ctx.rectangle(-130, yy, 70, 5) or ctx.fill() for yy in range(-170, -100, 12)]
    rrect(ctx, -40, -170, 130, 56, 6); fill_stroke(ctx, "#a9e07a" if not fail else "#3a4a30", INK, 3)
    art.text(ctx, (("BATT 18%" if not fail else "LOW", "#1f3a10"),), "popx", 20, 25, -142)
    on = beep and (int(t*6) % 2 == 0)
    ctx.arc(-110, -60, 14, 0, 6.3); fill_stroke(ctx, "#ff3a3a" if on else "#5a1a1a", INK, 3)
    ctx.arc(-70, -60, 14, 0, 6.3); fill_stroke(ctx, "#4aff7a" if not fail else "#1a3a20", INK, 3)
    # jugaad tape
    ctx.save(); ctx.translate(0, -95); ctx.rotate(-.35); src(ctx, "#e8d27a", .95); ctx.rectangle(-160, -14, 320, 28); ctx.fill(); ctx.restore()
    rrect(ctx, -10, -50, 110, 36, 5); fill_stroke(ctx, "#ffd21f", INK, 2.5)
    art.text(ctx, (("JUGAAD", "#c7262f"),), "lilita", 18, 45, -32)
    ctx.restore()

def table_fan(ctx, x, y, s, t, spin=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -50, -20, 100, 20, 8); fill_stroke(ctx, "#e9edf0")
    ctx.rectangle(-8, -110, 16, 92); fill_stroke(ctx, "#e9edf0")
    ctx.arc(0, -160, 66, 0, 6.3); fill_stroke(ctx, "#cfe8ff")
    a0 = t*14 if spin else 0
    for k in range(3):
        a = a0 + k*2.094
        ctx.save(); ctx.translate(0, -160); ctx.rotate(a); art.ell(ctx, 0, -30, 16, 30); fill_stroke(ctx, "#7fb6ff", INK, 2.5); ctx.restore()
    ctx.arc(0, -160, 12, 0, 6.3); fill_stroke(ctx, "#2f6db0")
    src(ctx, INK); ctx.set_line_width(2)
    for k in range(10): a = k*.628; ctx.move_to(0, -160); ctx.line_to(66*math.cos(a), -160+66*math.sin(a)); ctx.stroke()
    ctx.restore()

def chai_machine(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -110, -300, 220, 300, 18); fill_stroke(ctx, "#c7262f")
    rrect(ctx, -90, -280, 180, 70, 10); fill_stroke(ctx, "#ffd21f")
    art.text(ctx, (("CHAI", "#c7262f"),), "lucky", 50, 0, -244)
    src(ctx, "#1b1b1b"); ctx.rectangle(-70, -190, 140, 120); ctx.fill()
    rrect(ctx, -20, -190, 40, 30, 4); fill_stroke(ctx, "#9aa3a6")
    ctx.move_to(-28, -120); ctx.line_to(28, -120); ctx.line_to(22, -72); ctx.line_to(-22, -72); ctx.close_path(); fill_stroke(ctx, "#f3efe3", INK, 3)
    src(ctx, "#a5652a"); ctx.rectangle(-24, -112, 48, 12); ctx.fill()
    for k in range(3):
        ph = (t*.7 + k/3) % 1
        src(ctx, "#ffffff", .6*(1-ph)); ctx.set_line_width(5)
        xx = -12 + k*12; ctx.move_to(xx, -130-ph*60); ctx.curve_to(xx+10, -140-ph*60, xx-10, -150-ph*60, xx, -160-ph*60); ctx.stroke()
    for k, col in ((-60, "#2e9b5a"), (60, "#2f6db0")): ctx.arc(k, -40, 12, 0, 6.3); fill_stroke(ctx, col, INK, 2.5)
    ctx.restore()

def phone(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(math.sin(t*30)*.08)
    rrect(ctx, -30, -55, 60, 110, 10); fill_stroke(ctx, "#1b1b1b")
    src(ctx, "#2e9b5a"); rrect(ctx, -24, -46, 48, 88, 6); ctx.fill()
    art.text(ctx, (("DADI", "#ffffff"),), "lilita", 14, 0, -16)
    ctx.arc(0, 20, 10, 0, 6.3); fill_stroke(ctx, "#4aff7a", INK, 2)
    ctx.restore()

def darken(ctx, k, sat=True):
    if k <= 0: return
    if sat:
        ctx.save(); ctx.set_operator(cairo.OPERATOR_HSL_SATURATION); src(ctx, "#808080", .85*k); ctx.paint(); ctx.restore()
    src(ctx, "#05030a", .78*k); ctx.paint()

# ---------------- shots ----------------
def shot_world(ctx, shot, lt, T, m):
    sid = shot["id"]; L = shot["L"]
    z = 1.0 + .05*ease(lt/L)
    if sid == "open":
        ctx.save(); cam(ctx, z, W/2, 760); paint_bg(ctx, "street")
        art.person(ctx, 250, 1220, 1.38, dict(MANAGER, prop=None) if lt < 1.8 else MANAGER, "wave" if lt < 1.8 else "point", t=lt, mouth=m)
        ctx.restore()
    elif sid == "result":
        paint_bg(ctx, "blur2")
        art.person(ctx, 560, 1330, .95, MANAGER, "cheer" if lt > lt_(shot, 0, .6) else "point", t=lt, mouth=m, flip=True)
    elif sid == "vip":
        ctx.save(); cam(ctx, z, W/2, 760); paint_bg(ctx, "vip"); ctx.restore()
    elif sid == "fund":
        ctx.save(); cam(ctx, z, W/2, 760); paint_bg(ctx, "street")
        art.person(ctx, 200, 1225, 1.3, MANAGER, "hold" if lt < lt_(shot, 0, .5) else "cheer", t=lt, mouth=m); ctx.restore()
    elif sid == "inverter":
        ctx.save(); cam(ctx, 1.35 + .05*ease(lt/L), 360, 860); paint_bg(ctx, "cafe")
        drop = eout((lt-.2)/.45); iy = 700 + 330*drop
        if lt > .2: inverter(ctx, 290, iy, 1.0, lt, beep=lt > lt_(shot, 0, .7))
        art.person(ctx, 540, 1180, .82, CHINTU, "shrug" if lt > lt_(shot, 0, .6) else "idle", t=lt)
        if lt > .2 and lt < .75:
            src(ctx, "#ffffff", .5*(1-(lt-.2)/.55)); ctx.set_line_width(3)
            for k in range(5): ctx.move_to(220+k*40, iy-260); ctx.line_to(220+k*40, iy-330); ctx.stroke()
        ctx.restore()
    elif sid == "pcs":
        ctx.save(); cam(ctx, 1.0 + .06*ease(lt/L), W/2, 600); paint_bg(ctx, "cafe")
        for i, x in enumerate(MON_X):
            if i not in ON_PCS:
                src(ctx, "#000", .35); ctx.rectangle(x-60, 430, 120, 80); ctx.fill()
        inverter(ctx, 150, 990, .7, lt, beep=True)
        table_fan(ctx, 560, 1000, 1.0, lt, spin=True)
        ctx.restore()
    elif sid == "chai":
        ctx.save(); cam(ctx, 1.0 + .05*ease(lt/L), W/2, 900); paint_bg(ctx, "blur")
        chai_machine(ctx, 230, 1150, 1.25, lt)
        draw_pinky(ctx, 540, 1200, .9, "cheer" if lt > lt_(shot, 0, .75) else "hold", lt)
        ctx.restore()
    elif sid == "investor":
        ctx.save(); cam(ctx, 1.0 + .05*ease(lt/L), W/2, 900); paint_bg(ctx, "blur")
        art.person(ctx, 360, 1230, 1.15, INVESTOR, "point" if lt < lt_(shot, 0, .6) else "palm", t=lt, mouth=m*.0)
        ctx.restore()
    elif sid == "prozone":
        ctx.save(); cam(ctx, z, W/2, 800); paint_bg(ctx, "street")
        k = eout((lt-.3)/1.2)
        for i, sp in enumerate(PRO):
            x = 900 + i*150 - (520+0)*k - 20*i*k
            art.person(ctx, x - 40*i, 1190 - i*6, .78, sp, "point" if i == 0 and lt > 1.6 else "idle", t=lt+i)
        art.person(ctx, 120, 1230, 1.0, MANAGER, "shrug" if lt > lt_(shot, 0, .5) else "idle", t=lt, mouth=m)
        ctx.restore()
    elif sid == "blackout":
        cut = lt_(shot, 0, .62); back = lt_(shot, 1, .72)
        dark = lt > cut and lt < back
        ctx.save(); cam(ctx, 1.0 + .05*ease(lt/L), W/2, 640); paint_bg(ctx, "cafe" if not dark else "cafe_off"); ctx.restore()
        if lt > cut:
            k = 1 if dark else max(0, 1-(lt-back)/.4)*1 + .25
            k = min(1, k)
            if not dark:
                fl = 1 if int((lt-back)*14) % 3 == 0 and lt-back < .5 else 0
                darken(ctx, .25 + .5*fl, sat=False)
            else:
                darken(ctx, 1)
                if lt > lt_(shot, 1, .1):
                    on = int(lt*6) % 2 == 0
                    src(ctx, "#ff3a3a", .35 if on else .1); art.ell(ctx, 120, 1100, 90, 90); ctx.fill()
    elif sid == "lucky":
        ctx.save(); cam(ctx, 1.0 + .05*ease(lt/L), W/2, 900); paint_bg(ctx, "blur")
        run = lt_(shot, 1, .55); dx = 0 if lt < run else -900*ease((lt-run)/.6)
        draw_lucky(ctx, 380+dx, 1210, 1.0, "hold", lt)
        if lt > lt_(shot, 0, .5) and lt < run: phone(ctx, 380+dx+110, 1210-330, 1.3, lt)
        if lt > run:
            src(ctx, "#ffffff", .5); ctx.set_line_width(4)
            for k in range(5): ctx.move_to(520+dx+k*10, 700+k*80); ctx.line_to(640+dx+k*10, 700+k*80); ctx.stroke()
        ctx.restore()
    elif sid == "decide":
        paint_bg(ctx, "blur2")
        art.person(ctx, 590, 1310, .9, MANAGER, "point", t=lt, mouth=m, flip=True)
        cat(ctx, 160, 1250, .7, lt, awake=lt > lt_(shot, 5, .5))

def cues(shot):
    s = shot["id"]; c = {}
    if s == "open":     c = dict(day=(lt_(shot, 0, .62), "hit"), y=(.2, "pop"))
    if s == "result":   c = dict(title=(.1, "hit"), a=(.35, "pop"), b=(.5, "pop"), c=(.65, "pop"), win=(lt_(shot, 0, .62), "hit"), inv=(lt_(shot, 0, .8), "pop"))
    if s == "vip":      c = dict(tag=(.15, "pop"), board=(.3, "pop"), done=(lt_(shot, 0, .45), "ding"), names=(lt_(shot, 0, .55), "pop"))
    if s == "fund":     c = dict(likes=(.2, "pop"), board=(lt_(shot, 0, .1), "pop"), done=(lt_(shot, 0, .85), "ding"))
    if s == "inverter": c = dict(drop=(.62, "boom"), tag=(.7, "pop"), sh=(lt_(shot, 0, .6), "hit"), beep=(lt_(shot, 0, .85), "beep"))
    if s == "pcs":      c = dict(tag=(.2, "pop"), two=(lt_(shot, 0, .5), "pop"), fan=(lt_(shot, 0, .8), "pop"), beep=(lt_(shot, 0, .95), "beep"))
    if s == "chai":     c = dict(idea=(lt_(shot, 0, .2), "pop"), name=(lt_(shot, 0, .75), "hit"))
    if s == "investor": c = dict(tag=(.25, "pop"), cr=(lt_(shot, 0, .3), "hit"), ud=(lt_(shot, 0, .78), "hit"))
    if s == "prozone":  c = dict(card=(lt_(shot, 0, .5), "hit"), vs=(lt_(shot, 0, .8), "pop"))
    if s == "blackout": c = dict(score=(.2, "pop"), cut=(lt_(shot, 0, .62), "powerdown"), beep=(lt_(shot, 1, .25), "beep"),
                                 back=(lt_(shot, 1, .72), "ding"))
    if s == "lucky":    c = dict(tag=(.2, "pop"), call=(lt_(shot, 0, .5), "ring"), run=(lt_(shot, 1, .55), "whoosh"), team=(lt_(shot, 1, .8), "hit"))
    if s == "decide":   c = dict(title=(lt_(shot, 0, .05), "hit"), q=(lt_(shot, 0, .2), "pop"), a=(lt_(shot, 1), "pop"), b=(lt_(shot, 2), "pop"),
                                 c=(lt_(shot, 3), "pop"), cm=(lt_(shot, 4), "pop"), boss=(lt_(shot, 5, .5), "crowd"))
    for k, (t_, sfx) in list(c.items()):
        if sfx not in (None, "pop", "hit", "ding", "whoosh", "crowd", "riser"):
            c[k] = (t_, {"beep": "pop", "ring": "ding", "boom": "hit", "powerdown": "hit"}.get(sfx, "pop"))
    return c

def _count(lt, t0, dur, a, b):
    return int(a + (b-a)*ease((lt-t0)/dur)) if lt > t0 else a

def shot_ui(ctx, shot, lt, T):
    s = shot["id"]; c = cues(shot); P = lambda k, d=.28: pop_scale(lt, c[k][0], d)
    if s == "open":
        art.tag(ctx, "YESTERDAY: DECISION #1", W/2, 110, "#7a2fb0", size=24, sc=P("y"))
        art.title(ctx, "DAY 2", W/2, 210, 120, sc=P("day", .35))
    elif s == "result":
        art.title(ctx, "RESULT!", W/2, 130, 100, sc=P("title", .35))
        tot = max(1, sum(VOTES.values())); mx = max(VOTES.values())
        for k, (key, L_, t_, col) in enumerate((("a", "A", "BUY NEW PCS", "#2e9b5a"), ("b", "B", "GET AN INVERTER", "#c7262f"),
                                                 ("c", "C", "SOMETHING ELSE", "#1e2a46"))):
            sc = P(key)
            if sc <= .01: continue
            y = 280 + k*120; win = L_ == "B" and lt > c["win"][0]
            art.option(ctx, W/2, y, 640, L_, t_, col, win, sc=sc)
            f = ease((lt-c[key][0]-.2)/.9) * VOTES[L_]/mx
            ctx.save(); ctx.translate(W/2, y); ctx.scale(sc, sc)
            rrect(ctx, -228, 50, 456, 16, 6); fill_stroke(ctx, "#2a2238", None)
            rrect(ctx, -228, 50, 456*f, 16, 6); fill_stroke(ctx, col if not win else "#ffd21f", None)
            art.text(ctx, (("%d votes" % int(VOTES[L_]*ease((lt-c[key][0]-.2)/.9)), "#ffffff"),), "popx", 18, 280, 58, stroke=3)
            ctx.restore()
        art.confetti(ctx, lt-c["win"][0], 560, 360, n=40)
        art.sticker(ctx, "WINNER!", 555, 418, 64, "#ffd21f", sc=P("win"), rot=.12)
        art.tag(ctx, "MOST VOTED OPTION WINS", W/2, 680, "#ffd21f", "#1b1208", 24, sc=P("inv"), border="#1b1208")
    elif s == "vip":
        art.tag(ctx, "VIP GAMING SEATS", W/2, 120, "#7a2fb0", size=30, sc=P("tag"))
        art.board(ctx, W/2, 255, "FOLLOWERS", "{:,}".format(_count(lt, c["board"][0]+.1, 1.4, 0, FOLLOWERS)), 320, sc=P("board"))
        if lt > c["done"][0]:
            for k in range(6):
                ph = (lt-c["done"][0])*.8 - k*.15
                if 0 < ph < 1: art.heart(ctx, 120+k*100 + math.sin(k*2+ph*6)*20, 1000-ph*500, .9+.4*ph)
        pos = [(170, 470), (520, 450), (360, 560), (150, 640), (560, 630)]
        for i, (nm, (x, y)) in enumerate(zip(VIP_NAMES, pos)):
            sc = pop_scale(lt, c["names"][0] + i*.16)
            art.tag(ctx, "@" + nm, x, y + math.sin(lt*2+i)*6, "#ffffff", "#1b1208", 18, sc=sc, border="#7a2fb0")
        art.tag(ctx, "+ %d MORE VIPs" % (FOLLOWERS - len(VIP_NAMES)), W/2, 730, "#ffd21f", "#1b1208", 24,
                sc=pop_scale(lt, c["names"][0] + len(VIP_NAMES)*.16 + .1), border="#1b1208")
    elif s == "fund":
        art.tag(ctx, "%d LIKES × ₹100" % LIKES, 470, 380, "#c7262f", size=26, sc=P("likes"))
        v = _count(lt, c["board"][0]+.15, 1.5, FUND_START, FUND)
        art.board(ctx, 450, 230, "CAFE FUND", "₹{:,}".format(v), 380, sc=P("board"), vsize=66)
        if lt > c["done"][0]: art.sticker(ctx, "PAISA HI PAISA!", 450, 500, 54, "#7fe0b0", sc=P("done"), rot=-.08)
        for k in range(4):
            f = (lt - .3 - k*.3)/1.0
            if 0 < f < 1: art.heart(ctx, 620 - 170*f, 760 - 520*f + math.sin(f*6+k)*30, 1.3)
    elif s == "inverter":
        art.tag(ctx, "INVERTER ARRIVED!", W/2, 120, "#2e9b5a", size=30, sc=P("tag"))
        art.sticker(ctx, "SECOND HAND!", W/2, 260, 76, "#ff8a1e", sc=P("sh"), rot=-.08)
        art.tag(ctx, "FROM: JUGAAD ELECTRONICS", W/2, 370, "#1e2a46", size=22, sc=P("sh", .35))
        if lt > c["beep"][0] and int(lt*4) % 2 == 0: art.sticker(ctx, "BEEP!", 170, 560, 54, "#ff5a4a", sc=1, rot=.15)
    elif s == "pcs":
        art.tag(ctx, "INVERTER CAPACITY", W/2, 140, "#1e2a46", size=26, sc=P("tag"))
        art.tag(ctx, "PCs ON: 2 / 5", 220, 240, "#c7262f", size=26, sc=P("two"))
        art.tag(ctx, "+ 1 PANKHA", 500, 240, "#2f6db0", size=26, sc=P("fan"))
        if lt > c["beep"][0] and int(lt*4) % 2 == 0: art.sticker(ctx, "BEEP BEEP!", 200, 780, 54, "#ff5a4a", sc=1, rot=-.12)
    elif s == "chai":
        art.tag(ctx, "IDEA BY @" + IDEA_BY, W/2, 140, "#ffd21f", "#1b1208", 24, sc=P("idea"), border="#1b1208")
        art.tag(ctx, "COFFEE MACHINE", W/2, 220, "#1e2a46", size=26, sc=P("idea", .35))
        art.sticker(ctx, "NAAM: CHAI!", W/2, 350, 84, "#ffd21f", sc=P("name"), rot=-.06)
    elif s == "investor":
        art.tag(ctx, "INVESTOR: @" + INVESTOR_BY, W/2, 130, "#1e2a46", size=22, sc=P("tag"))
        sc = P("cr")
        if sc > .01:
            ctx.save(); ctx.translate(W/2, 250); ctx.scale(sc, sc); ctx.rotate(-.06)
            art.text(ctx, (("₹100 CRORE!", "#7fe0b0"),), "pop", 64, 0, 0, stroke=6, scol="#1b1208", shadow=4); ctx.restore()
        art.sticker(ctx, "CHAI UDHAAR?", W/2, 380, 72, "#ff8a1e", sc=P("ud"), rot=.08)
    elif s == "prozone":
        sc = P("card")
        if sc > .01:
            ctx.save(); ctx.translate(W/2, 170); ctx.scale(sc, sc)
            src(ctx, "#000", .35); rrect(ctx, -296, -66, 600, 140, 12); ctx.fill()
            rrect(ctx, -300, -70, 600, 140, 12); fill_stroke(ctx, "#1e2a46", "#ffffff", 4)
            art.text(ctx, (("TONIGHT · TOURNAMENT", "#7fb6ff"),), "lilita", 24, 0, -36)
            art.text(ctx, (("LEVEL UP", "#ff3fa4"), ("  VS  ", "#ffffff"), ("PRO ZONE", "#b48cff")), "lucky", 38, 0, 12)
            ctx.restore()
        art.sticker(ctx, "3 vs 3!", 520, 640, 80, "#ffd21f", sc=P("vs"), rot=.08)
    elif s == "blackout":
        sc = P("score")
        if sc > .01:
            ctx.save(); ctx.translate(W/2, 150); ctx.scale(sc, sc)
            rrect(ctx, -270, -50, 540, 100, 12); fill_stroke(ctx, "#1e2a46", "#ffffff", 4)
            art.text(ctx, (("LEVEL UP  0 - 0  PRO ZONE", "#ffffff"),), "lucky", 34, 0, 2)
            ctx.restore()
        if c["cut"][0] < lt < c["back"][0]:
            art.sticker(ctx, "LIGHT GAYI!", W/2, 420, 90, "#ffffff", sc=pop_scale(lt, c["cut"][0]), rot=-.06)
            if lt > c["beep"][0] and int(lt*6) % 2 == 0: art.sticker(ctx, "BEEP...", 200, 980, 56, "#ff5a4a", sc=1, rot=.1)
        if lt > c["back"][0]:
            art.sticker(ctx, "INVERTER ZINDABAD!", W/2, 420, 66, "#4aff7a", sc=P("back"), rot=-.06)
    elif s == "lucky":
        art.tag(ctx, "LUCKY · PRO GAMER", W/2, 120, "#c7262f", size=28, sc=P("tag"))
        if c["call"][0] < lt < c["run"][0]: art.sticker(ctx, "DADI CALLING...", W/2, 260, 66, "#4aff7a", sc=P("call"), rot=-.06)
        if lt > c["run"][0]: art.sticker(ctx, "BHAAG GAYA!", W/2, 300, 84, "#ff8a1e", sc=P("run"), rot=.06)
        art.tag(ctx, "TEAM: 2 / 3 PLAYERS", W/2, 430, "#c7262f", size=28, sc=P("team"))
    elif s == "decide":
        art.title(ctx, "DECISION #2", W/2, 120, 92, sc=P("title", .35))
        art.tag(ctx, "3rd PLAYER KAUN?", W/2, 220, "#c7262f", size=28, sc=P("q"))
        cur = 0
        for k, key in enumerate(("a", "b", "c")):
            if lt > c[key][0]: cur = k
        allon = lt > c["boss"][0]
        for k, (key, L_, t_, col) in enumerate((("a", "A", "MANAGER PLAYS", "#2e9b5a"), ("b", "B", "HIRE A PRO GAMER", "#c7262f"),
                                                 ("c", "C", "SOMETHING ELSE?", "#1e2a46"))):
            act = (k == cur and lt < c["cm"][0]) or (allon and int(lt*5) % 3 == k)
            art.option(ctx, W/2, 320+k*104, 640, L_, t_, col, act, sc=P(key))
        art.tag(ctx, "COMMENT  A / B / C", 260, 660, "#c7262f", size=26, sc=P("cm"))
        art.tag(ctx, "MOST VOTED OPTION WINS", 290, 730, "#ffd21f", "#1b1208", 24, sc=pop_scale(lt, c["cm"][0]+.25), border="#1b1208")
        art.sticker(ctx, "YOU'RE THE BOSS!", 330, 850, 60, "#ffd21f", sc=P("boss"), rot=-.1)
        art.confetti(ctx, lt-c["boss"][0], W/2, 600)
