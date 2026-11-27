"""EPISODE: Level Up Gaming Cafe — Day 5 "Chor Mil Gaya!"   (@tumhoboss)
Reveal: Billu (CCTV shadow, claw scratches on the box, Rs 500 note in his plate, missing since morning).
Detective Board = correct Day 4 guessers. Follow push + PS5 fund goal + vote: Billu ki saza.
Render:  python -m srs.engine path/to/episode.py [--sheet | --frames 3.0,20.5]
"""
import math, os as _os
import cairo
from srs import art
from srs.art import W, H, src, rrect, fill_stroke, ease, eout, bout, pop_scale, SKIN, INK
from srs.engine import lt_, cam, paint_bg
import numpy as _np, soundfile as _sf
from srs import voice as _V

TITLE = "Level Up Gaming Cafe — Day 5"
OUTPUT = "Level_Up_Gaming_Cafe_Day5.mp4"
VOICE = "hm_omega"
END_HOLD = 1.8

DETECTIVES = ["justt_yachass_15", "biswaje3135c", "awaaz_of_meerut_"]   # correct Billu guesses on Day 4 (first = head detective)
DAY1_FAN = "parmar_manav_1"

# ---------------- cast (matches Day 1-4) ----------------
# ---------------- cast (matches Day 1/2) ----------------
MANAGER = dict(skin=SKIN["m"], hair="side", hair_col="#1d1714", shirt="#f3efe3", jacket="#e2862b", pants="#2f4f7a",
               shoes="#f2f2ee", lanyard=True, prop="notepad", seed=1)
MANAGER_WORRIED = dict(MANAGER, smile=-.8, brow_tilt=-9)     # brows up in the middle, mouth turned down
MANAGER_SERIOUS = dict(MANAGER, smile=-.15, brow_tilt=5)      # brows pulled in, flat mouth
CHINTU = dict(skin=SKIN["d"], hair="curly", hair_col="#1d1714", shirt="#2f6db0", pants="#3a3a42", shoes="#f2f2ee", seed=2)
LUCKY = dict(skin=SKIN["m"], hair="side", shirt="#1d1d22", stripes=["#1d1d22", "#1d1d22", "#c7262f", "#1d1d22"],
             pants="#5a5a62", cap="#c7262f", shoes="#f2f2ee", seed=3)
CHINTU_CONFUSED = dict(CHINTU, smile=-.4, brow_tilt=-6)
PINKY = dict(skin=SKIN["m"], hair="none", shirt="#e85a9a", pants="#2f4f7a", shoes="#f2f2ee", seed=4)
SUBHAM = dict(skin=SKIN["l"], hair="side", hair_col="#2a1a10", shirt="#ffd21f", stripes=["#ffd21f", "#ffd21f", "#1e2a46"],
              pants="#2b2b33", shoes="#f2f2ee", seed=9)
PRO = [dict(skin=s, hair=h, shirt="#6a3fc4", stripes=["#6a3fc4", "#6a3fc4", "#ffffff"], pants="#2b2b33",
            band="#ffd21f", shoes="#f2f2ee", seed=6+i, brow_tilt=-4, smile=-.2)
       for i, (s, h) in enumerate(((SKIN["l"], "spiky"), (SKIN["d"], "side"), (SKIN["m"], "curly")))]

TITLE = "Level Up Gaming Cafe — Day 6"
OUTPUT = "Level_Up_Gaming_Cafe_Day6.mp4"

LINES = [
 ("hook",   "इस बिल्ली के लिए... चालीस हज़ार मिल रहे थे...",        "Is billi ke liye... *40 hazaar* mil rahe the..."),
 ("hook",   "और हमने मना कर दिया!",                               "Aur humne *mana* kar diya!"),
 ("result", "क्यों? क्योंकि कांटे की टक्कर के बाद... majority ने कहा... B!", "Kyun? Kyunki kaante ki takkar ke baad... *majority* ne kaha... *B*!"),
 ("result", "Billu नहीं बिकेगा!",                                 "Billu *nahi bikega*!"),
 ("angry",  "Pro Zone वाला गुस्से में बोला... पछताओगे!",             "Pro Zone wala gusse mein bola... *pachhtaoge*!"),
 ("angry",  "और दरवाज़ा पटक के चला गया।",                          "Aur darwaza *patak* ke chala gaya."),
 ("fund",   "अब हिसाब, boss!",                                    "Ab *hisaab*, boss!"),
 ("fund",   "Likes से इकतीस सौ... shares से एक हज़ार... और तीन नए followers से... पंद्रह सौ!",
                                                                 "Likes se *31 sau*... shares se *1 hazaar*... aur teen naye followers se... *15 sau*!"),
 ("fund",   "Fund पहुँचा... सत्रह हज़ार सात सौ!",                    "Fund pahuncha... *17 hazaar 700*!"),
 ("fund",   "PS Five के लिए... अभी भी सैंतीस हज़ार तीन सौ कम।",        "PS5 ke liye... abhi bhi *37 hazaar 300* kam."),
 ("doubt",  "पर Chintu को कुछ खटक रहा था...",                       "Par *Chintu* ko kuch khatak raha tha..."),
 ("doubt",  "छह महीने पहले भागी थी? सच में?",                        "Chhe mahine pehle *bhaagi* thi? Sach mein?"),
 ("cctv",   "उसने पुरानी CCTV खोली...",                              "Usne purani *CCTV* kholi..."),
 ("cctv",   "आठ महीने पहले की recording...",                         "Aath mahine pehle ki *recording*..."),
 ("cctv",   "और console पे... Billu सो रहा था!",                      "Aur console pe... *Billu* so raha tha!"),
 ("liar",   "मतलब Billu कभी Pro Zone का था ही नहीं!",                  "Matlab Billu kabhi Pro Zone ka tha hi *nahi*!"),
 ("liar",   "वो झूठ बोल रहा था!",                                    "Wo *jhooth* bol raha tha!"),
 ("why",    "तो फिर उसे Billu क्यों चाहिए?",                           "To phir use Billu *kyun* chahiye?"),
 ("why",    "क्योंकि Billu अब famous है... तुम्हारी वजह से!",            "Kyunki Billu ab *famous* hai... tumhari wajah se!"),
 ("why",    "और Pro Zone के customers... हमारे पास आ रहे हैं!",          "Aur Pro Zone ke customers... *hamare paas* aa rahe hain!"),
 ("msg",    "तभी cafe के phone पे message आया...",                    "Tabhi cafe ke phone pe *message* aaya..."),
 ("msg",    "Three versus three rematch। जीते तो Billu तुम्हारा... हमेशा के लिए।", "Three versus three *rematch*. Jeete to Billu tumhara... *hamesha* ke liye."),
 ("msg",    "हारे... तो Billu मेरा!",                                 "Haare... to Billu *mera*!"),
 ("decide", "अब फ़ैसला तुम्हारा, boss!",                              "Ab faisla *tumhara*, boss!"),
 ("decide", "A... challenge accept! Team Level Up... Billu के लिए खेलेगी!", "*A*... challenge accept! Team Level Up... Billu ke liye *khelegi*!"),
 ("decide", "B... challenge नहीं! CCTV सबको दिखा के... उसका झूठ expose करो!", "*B*... challenge nahi! CCTV sabko dikha ke... uska jhooth *expose* karo!"),
 ("decide", "सबसे ज़्यादा comments वाला option जीतेगा!",               "Sabse zyada *comments* wala option jeetega!"),
 ("jersey", "और साथ में... team की jersey पे क्या लिखें? Comment करो!",  "Aur saath mein... team ki *jersey* pe kya likhein? Comment karo!"),
 ("jersey", "Best line... jersey पे छपेगी... तुम्हारे नाम के साथ!",      "Best line... jersey pe *chhapegi*... tumhare naam ke saath!"),
 ("army",   "और follow करो... Billu Army join करो!",                  "Aur *follow* karo... *Billu Army* join karo!"),
 ("army",   "Day Seven में... Billu Army के हर नए member का नाम... screen पे!", "Day 7 mein... Billu Army ke har naye member ka naam... *screen* pe!"),
 ("money",  "हर like... सौ। हर share... दो सौ। हर follow... पाँच सौ... PS Five के लिए!", "Har like... *100*. Har share... *200*. Har follow... *500*... PS5 ke liye!"),
 ("share",  "और ये reel उस दोस्त को भेजो... जो Pro Zone वाले जैसा झूठा है!", "Aur ye reel us dost ko bhejo... jo Pro Zone wale jaisa *jhootha* hai!"),
 ("end",    "Billu हमारा है... और हमारा ही रहेगा, boss!",               "Billu *hamara* hai... aur hamara hi *rahega*, boss!"),
]

SHOTS = [
 ("hook", "cut"), ("result", "whip"), ("angry", "cut"), ("fund", "whip"), ("doubt", "cut"), ("cctv", "cut"), ("liar", "whip"),
 ("why", "cut"), ("msg", "whip"), ("decide", "wipe"), ("jersey", "whip"), ("army", "cut"), ("money", "whip"), ("share", "cut"), ("end", "cut"),
]
_UV = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "build", "user_voice")
USER_ALL = all(_os.path.exists(_os.path.join(_UV, "%03d.wav" % (i+1))) for i in range(len(LINES)))
USER_VOICE = any(_os.path.exists(_os.path.join(_UV, "%03d.wav" % (i+1))) for i in range(len(LINES)))
_ORIG_LINE = _V.line_audio

def _trim(x, sr, thr=.015, pad=.06):
    fr = int(.01*sr); n = len(x)//fr
    rms = _np.sqrt((x[:n*fr].reshape(n, fr)**2).mean(1))
    on = _np.where(rms > thr)[0]
    if not len(on): return x
    return x[max(0, on[0]*fr-int(pad*sr)): min(len(x), (on[-1]+1)*fr+int(pad*sr))]

def _runs(x, sr, thr=.012, minf=8):
    fr = int(.01*sr); n = len(x)//fr
    q = _np.sqrt((x[:n*fr].reshape(n, fr)**2).mean(1)) < thr
    runs = []; st = None
    for i, v in enumerate(q):
        if v and st is None: st = i
        if not v and st is not None:
            if i-st >= minf: runs.append((st*.01, i*.01))
            st = None
    return runs

def _w(p):
    import re as _re
    p = _re.sub(r"\[[^\]]+\]", "", p)
    p = _re.sub(r"[*.!?,]", "", p)
    return sum(len(w)+2 for w in p.split()) + 1

def _gaps(x, sr, parts, wparts=None):
    """for each '...' boundary pick the pause nearest its expected time (by spoken length), in order"""
    d = len(x)/sr; runs = _runs(x, sr)
    w = [_w(p) for p in (wparts or parts)]; tot = sum(w); acc = 0; out = []; last = 0.0
    for k in range(len(parts)-1):
        acc += w[k]; e = d*acc/tot
        cand = [r for r in runs if r[0] > last + .15 and r[1] < d - .15]
        if cand:
            r = min(cand, key=lambda r: abs((r[0]+r[1])/2 - e) - .6*(r[1]-r[0]))
            if abs((r[0]+r[1])/2 - e) < max(.6, .35*d): out.append(r); last = r[1]; continue
        out.append((e, e)); last = e
    return out

# hand-checked caption split points (seconds into the trimmed line clip)
SPLITS = {}

if USER_VOICE:
    _SAYS = [l[1] for l in LINES]
    def _user_line(say, cap, voice, cache, lang="hi"):
        i = _SAYS.index(say)
        if not _os.path.exists(_os.path.join(_UV, "%03d.wav" % (i+1))): return _ORIG_LINE(say, cap, voice, cache, lang)
        x, sr = _sf.read(_os.path.join(_UV, "%03d.wav" % (i+1)), dtype="float32")
        if x.ndim > 1: x = x.mean(1)
        x = _trim(x, sr); d = len(x)/sr
        parts = [p.strip() for p in cap.split("...") if p.strip()]
        if len(parts) < 2: return x, [(cap.replace("...", ""), 0.0, d)]
        sp = [q.strip() for q in say.split("...") if q.strip()]
        g = SPLITS.get(i+1) or _gaps(x, sr, parts, sp if len(sp) == len(parts) else None)
        segs = []; t0 = 0.0
        for k, p in enumerate(parts):
            t1 = g[k][0] if k < len(g) else d
            segs.append((p + ("..." if k < len(parts)-1 else ""), t0, max(.2, t1-t0)))
            if k < len(g): t0 = g[k][1]
        return x, segs
    _V.line_audio = _user_line
    if USER_ALL: _V.polish = lambda v, c: v
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
    for i, x in enumerate(MON_X): _monitor(c, x, 480, i in on, kind=0)
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
    "cafe3": lambda: set_cafe(on=(1, 2, 3)),
    "vip": set_vip,
    "blur": lambda: art.blurred(set_cafe(), 8, .7),
    "blur2": lambda: art.blurred(set_cafe(), 11, .6),
    "blur_street": lambda: art.blurred(set_street(), 9, .65),
}
CAP_Y = {"result": 1110, "vip": 1150, "fund": 1150, "bill": 1180, "inverter": 1150, "pcs": 1110, "investor": 1150,
         "prozone": 1150, "team": 1180, "match": 1110, "blackout": 1180, "decide": 1090}

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


# ---------------- new props for Day 2 ----------------
def chappal(ctx, x, y, s, rot=0.):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    art.ell(ctx, 0, 0, 34, 78); fill_stroke(ctx, "#2f6db0")
    art.ell(ctx, 0, 4, 26, 66); fill_stroke(ctx, "#5a9be0", INK, 2)
    src(ctx, INK); ctx.set_line_width(9); ctx.move_to(-22, -36); ctx.line_to(0, -6); ctx.line_to(22, -36); ctx.stroke()
    src(ctx, "#f3efe3"); ctx.set_line_width(5); ctx.move_to(-22, -36); ctx.line_to(0, -6); ctx.line_to(22, -36); ctx.stroke()
    ctx.restore()

def cat_headset(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    src(ctx, INK); ctx.set_line_width(14); ctx.arc(-120, -78, 64, math.pi*1.1, math.pi*1.9); ctx.stroke()
    src(ctx, "#3fd8ff"); ctx.set_line_width(8); ctx.arc(-120, -78, 64, math.pi*1.1, math.pi*1.9); ctx.stroke()
    for side in (-1, 1):
        rrect(ctx, -120+side*62-12, -96, 24, 40, 9); fill_stroke(ctx, "#2b2b33", INK, 3)
    ctx.restore()

def rgb_strip(ctx, x, y, w, t):
    cols = ["#ff3fa4", "#ffd21f", "#3fd8ff", "#4aff7a", "#b48cff"]
    for k in range(9):
        c = cols[(k + int(t*6)) % len(cols)]
        for lw, a in ((26, .15), (12, .4)):
            src(ctx, c, a); ctx.arc(x - w/2 + k*w/8, y, lw/2, 0, 6.3); ctx.fill()
        ctx.arc(x - w/2 + k*w/8, y, 9, 0, 6.3); fill_stroke(ctx, c, INK, 2.5)
    src(ctx, INK); ctx.set_line_width(3); ctx.move_to(x-w/2-20, y-18); ctx.line_to(x+w/2+20, y-18); ctx.stroke()

def pc_tower(ctx, x, y, s, t, fixed=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -70, -220, 140, 220, 12); fill_stroke(ctx, "#20202a")
    src(ctx, "#3fd8ff" if fixed else "#5a1a1a"); rrect(ctx, -50, -200, 100, 10, 4); ctx.fill()
    for k in range(3):
        ctx.arc(0, -150 + k*50, 18, 0, 6.3); fill_stroke(ctx, "#2b2b33", INK, 2.5)
        if fixed:
            ctx.save(); ctx.translate(0, -150 + k*50); ctx.rotate(t*12)
            src(ctx, "#ff3fa4", .9); ctx.rectangle(-14, -3, 28, 6); ctx.fill(); ctx.restore()
    ctx.restore()

def ticket(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.rotate(-.08); ctx.scale(s, s)
    rrect(ctx, -150, -60, 300, 120, 12); fill_stroke(ctx, "#ffd21f")
    src(ctx, INK); ctx.set_dash([8, 6]); ctx.set_line_width(3); ctx.move_to(70, -54); ctx.line_to(70, 54); ctx.stroke(); ctx.set_dash([])
    art.text(ctx, (("ENTRY", "#c7262f"),), "lucky", 34, -40, -14); art.text(ctx, (("3 vs 3 CUP", "#2a1608"),), "lilita", 20, -40, 26)
    art.text(ctx, (("#1", "#c7262f"),), "lucky", 34, 112, 0)
    ctx.restore()

def wallet(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(math.sin(t*3)*.04)
    rrect(ctx, -120, -80, 240, 160, 18); fill_stroke(ctx, "#7a4a2a")
    rrect(ctx, 30, -40, 100, 80, 14); fill_stroke(ctx, "#9a6a40")
    ctx.arc(70, 0, 10, 0, 6.3); fill_stroke(ctx, "#ffd21f", INK, 2.5)
    ctx.save(); ctx.translate(-30, -96); ctx.rotate(-.12)
    rrect(ctx, -70, -26, 140, 52, 6); fill_stroke(ctx, "#7fe0b0")
    art.text(ctx, (("₹500", "#1f4d36"),), "pop", 26, 0, 2); ctx.restore()
    src(ctx, "#ffffff", .7); ctx.set_line_width(3)
    for k in range(3):
        a = -1.2 + k*.5; ctx.move_to(-150*math.cos(a)*-1, -150*math.sin(a)); ctx.line_to(-180*math.cos(a)*-1, -180*math.sin(a)); ctx.stroke()
    ctx.restore()

def receipt(ctx, cx, top, n_rows, rem, sc=1., hi=-1, stamp=0.):
    """itemised bill; rows 0..n_rows-1 visible, `rem` = running balance shown at the bottom"""
    if sc <= .01: return
    w, rh = 600, 62
    h = 150 + 5*rh + 120
    ctx.save(); ctx.translate(cx, top); ctx.scale(sc, sc)
    src(ctx, "#000", .3); rrect(ctx, -w/2+8, 8, w, h, 10); ctx.fill()
    ctx.move_to(-w/2, 0); ctx.line_to(w/2, 0); ctx.line_to(w/2, h)
    for k in range(16): ctx.line_to(w/2 - (k+.5)*w/16, h + (14 if k % 2 == 0 else 0))
    ctx.line_to(-w/2, h); ctx.close_path(); fill_stroke(ctx, "#fbf6e6", INK, 4)
    art.text(ctx, (("CAFE FUND · HISAAB", "#2a1608"),), "lucky", 34, 0, 44)
    art.text(ctx, (("FUND IN", "#6a5a4a"),), "popx", 22, -w/2+40, 100, anchor="lm")
    art.text(ctx, (("₹{:,}".format(FUND), "#1f6d3a"),), "pop", 26, w/2-40, 100, anchor="rm")
    src(ctx, INK); ctx.set_dash([6, 6]); ctx.set_line_width(2); ctx.move_to(-w/2+30, 128); ctx.line_to(w/2-30, 128); ctx.stroke(); ctx.set_dash([])
    for i, (name, amt) in enumerate(BILL):
        if i >= n_rows: break
        y = 160 + i*rh
        if i == hi:
            src(ctx, "#ffd21f", .45); rrect(ctx, -w/2+18, y-24, w-36, 48, 8); ctx.fill()
        art.text(ctx, ((name, "#2a1608"),), "popx", 22, -w/2+40, y, anchor="lm")
        art.text(ctx, (("- ₹{:,}".format(amt), "#c7262f"),), "pop", 24, w/2-40, y, anchor="rm")
    yb = 150 + 5*rh + 30
    src(ctx, INK); ctx.set_line_width(3); ctx.move_to(-w/2+30, yb-24); ctx.line_to(w/2-30, yb-24); ctx.stroke()
    art.text(ctx, (("BACHA", "#2a1608"),), "lucky", 34, -w/2+40, yb+16, anchor="lm")
    art.text(ctx, (("₹{:,}".format(rem), "#c7262f" if rem <= LEFT else "#1f6d3a"),), "pop", 40, w/2-40, yb+16, anchor="rm")
    if stamp > .01:
        ctx.save(); ctx.translate(120, yb-120); ctx.rotate(-.25); ctx.scale(stamp, stamp)
        src(ctx, "#c7262f", .85); ctx.set_line_width(6); rrect(ctx, -130, -40, 260, 80, 10); ctx.stroke()
        art.text(ctx, (("BAS ITNA HI!", "#c7262f"),), "lucky", 34, 0, 2, alpha=.9); ctx.restore()
    ctx.restore()

def set_match(on=(1, 2, 3)):
    """cafe at night, tournament mode: banner + three PCs lit"""
    img = set_cafe(on=on)
    return img

def glow_monitors(ctx, idx, t, cam_z=1.0):
    """after the blackout: only the inverter PCs glow"""
    for i in idx:
        x = MON_X[i]
        g = cairo.RadialGradient(x, 470, 10, x, 470, 220); g.add_color_stop_rgba(0, .4, .8, 1, .55); g.add_color_stop_rgba(1, .4, .8, 1, 0)
        ctx.set_source(g); ctx.rectangle(x-240, 230, 480, 520); ctx.fill()
        _monitor(ctx, x, 480, True, kind=0)


# ---------------- Day 3 props ----------------
BACKGROUNDS.update({"cafe3": lambda: set_cafe(on=(1, 2, 3))})
CAP_Y = {"gift": 1150, "hook": 1130, "rewind": 1130, "result": 1110, "battery": 1150, "win": 1150, "player": 1180, "bills": 1170,
         "fund": 1150, "cta": 1060, "decide": 1090, "end": 1150}

def shutter(ctx, x0, x1, top, bottom):
    if bottom <= top: return
    ctx.save(); ctx.rectangle(x0, top, x1-x0, bottom-top); ctx.clip()
    src(ctx, "#8a8f98"); ctx.rectangle(x0, top, x1-x0, bottom-top); ctx.fill()
    y = bottom
    while y > top:
        src(ctx, "#b4bac2"); ctx.rectangle(x0, y-26, x1-x0, 14); ctx.fill()
        src(ctx, "#5c616a"); ctx.rectangle(x0, y-12, x1-x0, 4); ctx.fill()
        y -= 30
    ctx.restore()
    rrect(ctx, x0-6, bottom-14, x1-x0+12, 20, 4); fill_stroke(ctx, "#4a4f58", INK, 3)
    rrect(ctx, (x0+x1)/2-30, bottom-10, 60, 16, 4); fill_stroke(ctx, "#d6a93a", INK, 2.5)

def notice(ctx, x, y, sc, rot=-.06, txt="SEALED"):
    if sc <= .01: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc)
    rrect(ctx, -150, -110, 300, 220, 8); fill_stroke(ctx, "#fbf6e6", INK, 4)
    art.text(ctx, (("NOTICE", "#2a1608"),), "lucky", 34, 0, -72)
    src(ctx, "#2a1608", .5)
    for k in range(4): ctx.rectangle(-110, -36 + k*22, 220 - (k % 2)*60, 6); ctx.fill()
    src(ctx, "#c7262f", .9); ctx.set_line_width(7); rrect(ctx, -120, 40, 240, 60, 8); ctx.stroke()
    art.text(ctx, ((txt, "#c7262f"),), "lucky", 40, 0, 72)
    ctx.restore()

def big_battery(ctx, x, y, s, charge, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -110, -200, 220, 200, 16); fill_stroke(ctx, "#1f4d36")
    rrect(ctx, -70, -222, 40, 26, 5); fill_stroke(ctx, "#c7262f"); rrect(ctx, 30, -222, 40, 26, 5); fill_stroke(ctx, "#2b2b33")
    rrect(ctx, -80, -170, 160, 120, 10); fill_stroke(ctx, "#0e2a1d", INK, 3)
    n = int(round(4*charge))
    for k in range(4):
        src(ctx, "#4aff7a" if k < n else "#244a33"); rrect(ctx, -68 + k*38, -158, 30, 96, 5); ctx.fill()
    art.text(ctx, (("NEW!", "#ffd21f"),), "lucky", 30, 0, -24)
    ctx.restore()

def cheque(ctx, x, y, sc):
    if sc <= .01: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(-.05); ctx.scale(sc, sc)
    src(ctx, "#000", .3); rrect(ctx, -236, -86, 480, 180, 12); ctx.fill()
    rrect(ctx, -240, -90, 480, 180, 12); fill_stroke(ctx, "#e8fff0", INK, 4)
    art.text(ctx, (("PRIZE · 3v3 CUP", "#1f6d3a"),), "lilita", 24, -60, -56)
    art.text(ctx, (("PAY: LEVEL UP CAFE", "#2a1608"),), "popx", 20, -60, -18)
    art.text(ctx, (("₹10,000", "#1f6d3a"),), "pop", 60, 0, 40, stroke=0)
    art.star(ctx, 190, -50, 26)
    ctx.restore()

def jersey(ctx, x, y, s, name, num="3"):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-150, -120); ctx.line_to(-60, -170); ctx.curve_to(-30, -130, 30, -130, 60, -170); ctx.line_to(150, -120)
    ctx.line_to(120, -40); ctx.line_to(90, -60); ctx.line_to(90, 150); ctx.line_to(-90, 150); ctx.line_to(-90, -60)
    ctx.line_to(-120, -40); ctx.close_path(); fill_stroke(ctx, "#ffd21f", INK, 5)
    art.text(ctx, ((name, "#1e2a46"),), "lucky", 40, 0, -70)
    art.text(ctx, ((num, "#c7262f"),), "lucky", 120, 0, 50, stroke=5, scol="#1e2a46")
    ctx.restore()

def envelope(ctx, x, y, s, open_=0.):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(-.06)
    rrect(ctx, -170, -100, 340, 200, 8); fill_stroke(ctx, "#f3e2b8", INK, 4)
    ctx.move_to(-170, -100); ctx.line_to(0, 20 - 120*open_); ctx.line_to(170, -100); src(ctx, INK); ctx.set_line_width(4); ctx.stroke()
    ctx.arc(0, 10, 26, 0, 6.3); fill_stroke(ctx, "#c7262f", INK, 3)
    art.text(ctx, (("URGENT", "#c7262f"),), "lucky", 26, 0, 70)
    ctx.restore()

def bills_board(ctx, cx, top, n, sc, total=0.):
    if sc <= .01: return
    w, rh = 600, 74
    h = 120 + 3*rh + 130
    ctx.save(); ctx.translate(cx, top); ctx.scale(sc, sc)
    src(ctx, "#000", .35); rrect(ctx, -w/2+8, 8, w, h, 12); ctx.fill()
    rrect(ctx, -w/2, 0, w, h, 12); fill_stroke(ctx, "#fbf6e6", INK, 4)
    rrect(ctx, -w/2, 0, w, 76, 12); fill_stroke(ctx, "#c7262f", INK, 4)
    art.text(ctx, (("BILLS DUE!", "#ffffff"),), "lucky", 44, 0, 40)
    for i, (nm, v) in enumerate(BILLS):
        if i >= n: break
        y = 120 + i*rh
        art.text(ctx, ((nm, "#2a1608"),), "lucky", 34, -w/2+40, y, anchor="lm")
        art.text(ctx, (("₹{:,}".format(v), "#c7262f"),), "pop", 36, w/2-40, y, anchor="rm")
    yb = 120 + 3*rh + 30
    src(ctx, INK); ctx.set_line_width(3); ctx.move_to(-w/2+30, yb-28); ctx.line_to(w/2-30, yb-28); ctx.stroke()
    if total > .01:
        art.text(ctx, (("TOTAL", "#2a1608"),), "lucky", 40, -w/2+40, yb+20, anchor="lm")
        ctx.save(); ctx.translate(w/2-40, yb+20); ctx.scale(total, total)
        art.text(ctx, (("₹{:,}".format(BILL_TOTAL), "#c7262f"),), "pop", 52, 0, 0, anchor="rm"); ctx.restore()
    ctx.restore()

def meter(ctx, cx, y, w, frac, sc=1., label="CAFE FUND"):
    if sc <= .01: return
    ctx.save(); ctx.translate(cx, y); ctx.scale(sc, sc)
    rrect(ctx, -w/2-10, -70, w+20, 150, 16); fill_stroke(ctx, "#120c22", "#ffd21f", 4)
    art.text(ctx, ((label, "#ffd21f"),), "lucky", 30, -w/2+10, -40, anchor="lm")
    art.text(ctx, (("GOAL ₹{:,}".format(BILL_TOTAL), "#ffffff"),), "popx", 20, w/2-10, -40, anchor="rm")
    rrect(ctx, -w/2+10, -6, w-20, 52, 26); fill_stroke(ctx, "#2a2238", "#ffffff", 3)
    f = max(.04, min(1, frac))
    col = "#ff5a4a" if f < .5 else ("#ffd21f" if f < .9 else "#4aff7a")
    rrect(ctx, -w/2+16, 0, (w-32)*f, 40, 20); fill_stroke(ctx, col, None)
    art.text(ctx, (("%d%%" % int(round(100*f)), "#ffffff"),), "lucky", 28, -w/2+16 + (w-32)*f - 36, 21, stroke=3)
    ctx.restore()

def padlock(ctx, x, y, s, shake=0.):
    ctx.save(); ctx.translate(x + shake, y); ctx.scale(s, s)
    src(ctx, INK); ctx.set_line_width(26); ctx.arc(0, -40, 60, math.pi, 0); ctx.stroke()
    src(ctx, "#b4bac2"); ctx.set_line_width(16); ctx.arc(0, -40, 60, math.pi, 0); ctx.stroke()
    rrect(ctx, -90, -40, 180, 150, 18); fill_stroke(ctx, "#d6a93a", INK, 5)
    ctx.arc(0, 20, 16, 0, 6.3); fill_stroke(ctx, INK, None); ctx.rectangle(-6, 20, 12, 40); ctx.fill()
    ctx.restore()

def maggi_stall(ctx, x, y, s, closed=False):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for px in (-200, 200): ctx.rectangle(px-8, -330, 16, 330); fill_stroke(ctx, "#7a4a2a", INK, 3)
    ctx.move_to(-240, -330); ctx.line_to(240, -330); ctx.line_to(210, -260); ctx.line_to(-210, -260); ctx.close_path(); fill_stroke(ctx, "#ff8a1e", INK, 4)
    for k in range(6):
        src(ctx, "#ffffff", .8); ctx.rectangle(-210 + k*70, -330, 35, 70); ctx.fill()
    rrect(ctx, -160, -250, 320, 60, 10); fill_stroke(ctx, "#ffd21f", INK, 3)
    art.text(ctx, (("MAGGI · ₹30", "#c7262f"),), "pop", 30, 0, -219)
    rrect(ctx, -230, -120, 460, 120, 8); fill_stroke(ctx, "#b8854f", INK, 4)
    for bx in (-120, 0, 120):
        art.ell(ctx, bx, -128, 50, 18); fill_stroke(ctx, "#f3efe3", INK, 3)
        src(ctx, "#f2c14e"); art.ell(ctx, bx, -134, 38, 10); ctx.fill()
    if closed:
        src(ctx, "#000", .35); rrect(ctx, -240, -340, 480, 340, 8); ctx.fill()
        ctx.save(); ctx.rotate(-.12)
        rrect(ctx, -170, -230, 340, 100, 10); fill_stroke(ctx, "#c7262f", INK, 5)
        art.text(ctx, (("CLOSED", "#ffffff"),), "lucky", 64, 0, -178); ctx.restore()
    ctx.restore()

def gift_box(ctx, x, y, s, open_):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -140, -150, 280, 150, 10); fill_stroke(ctx, "#c7262f", INK, 5)
    src(ctx, "#ffd21f"); ctx.rectangle(-18, -150, 36, 150); ctx.fill()
    ctx.save(); ctx.translate(-150, -150); ctx.rotate(-1.1*open_)
    rrect(ctx, 0, -40, 300, 44, 8); fill_stroke(ctx, "#e0303a", INK, 5)
    src(ctx, "#ffd21f"); ctx.rectangle(132, -40, 36, 44); ctx.fill()
    ctx.restore(); ctx.restore()

def game_case(ctx, x, y, s, rot=0.):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -110, -150, 220, 300, 12); fill_stroke(ctx, "#1a1a22", INK, 5)
    g = cairo.LinearGradient(0, -130, 0, 130); g.add_color_stop_rgb(0, 1, .55, .2); g.add_color_stop_rgb(1, .6, .1, .45)
    rrect(ctx, -94, -134, 188, 230, 8); ctx.set_source(g); ctx.fill()
    src(ctx, "#1a1a22", .55)
    for k in range(5): ctx.rectangle(-80 + k*34, 10 - (k % 3)*30, 24, 86 + (k % 3)*30); ctx.fill()
    art.text(ctx, (("GTA 6", "#ffffff"),), "lucky", 60, 0, -70, stroke=6, scol="#1a1a22")
    art.text(ctx, (("GAME", "#ffd21f"),), "popx", 20, 0, 122)
    ctx.restore()

def console_shelf(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -230, -170, 460, 260, 10); fill_stroke(ctx, "#20202a", INK, 5)
    rrect(ctx, -210, -150, 420, 220, 6); fill_stroke(ctx, "#0b0b10", None)
    art.text(ctx, (("NO SIGNAL", "#5a6a7a"),), "popx", 26, 0, -40)
    rrect(ctx, -260, 100, 520, 30, 6); fill_stroke(ctx, "#7a4a2a", INK, 4)
    src(ctx, "#ffffff", .8); ctx.set_dash([12, 9]); ctx.set_line_width(4)
    rrect(ctx, -70, 0, 140, 96, 10); ctx.stroke(); ctx.set_dash([])
    art.text(ctx, (("PS5?", "#ffffff"),), "lucky", 34, 0, 50)
    ctx.restore()

def sweat_drop(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, -26); ctx.curve_to(16, -2, 16, 16, 0, 18); ctx.curve_to(-16, 16, -16, -2, 0, -26); ctx.close_path()
    fill_stroke(ctx, "#8fd8ff", INK, 3)
    src(ctx, "#ffffff", .8); ctx.arc(-4, 4, 4, 0, 6.3); ctx.fill()
    ctx.restore()

def big_heart(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, 60); ctx.curve_to(-120, -20, -60, -110, 0, -50); ctx.curve_to(60, -110, 120, -20, 0, 60); ctx.close_path()
    fill_stroke(ctx, "#ff3a5a", INK, 5); ctx.restore()

def paper_plane(ctx, x, y, s, rot=-.3):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.move_to(-90, 10); ctx.line_to(100, -60); ctx.line_to(20, 70); ctx.line_to(0, 20); ctx.close_path(); fill_stroke(ctx, "#ffffff", INK, 5)
    ctx.move_to(0, 20); ctx.line_to(100, -60); src(ctx, INK); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()

def chat_group(ctx, x, y, sc, t):
    if sc <= .01: return
    ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc)
    rrect(ctx, -230, -150, 460, 300, 26); fill_stroke(ctx, "#0b1f1a", "#ffffff", 4)
    rrect(ctx, -230, -150, 460, 60, 26); fill_stroke(ctx, "#1f6d4a", None)
    art.text(ctx, (("GAMER GANG", "#ffffff"),), "popx", 24, 0, -120)
    for k, (txt, right) in enumerate((("bhai ye dekh", False), ("cafe bachao!! share kar", True), ("done bhai!", False))):
        if t < .25 + k*.45: continue
        bx = 40 if right else -40
        rrect(ctx, bx - 150, -70 + k*68, 300, 52, 16); fill_stroke(ctx, "#2a7a5a" if right else "#2a2f36", None)
        art.text(ctx, ((txt, "#ffffff"),), "popx", 20, bx, -44 + k*68)
    ctx.restore()

def scanlines(ctx, t, a=.18):
    src(ctx, "#000", a)
    for y in range(0, H, 6): ctx.rectangle(0, y, W, 2); ctx.fill()
    off = (t*900) % H
    src(ctx, "#ffffff", .08); ctx.rectangle(0, off, W, 40); ctx.fill()


# =====================================================================
# Day 5 props
# =====================================================================
SPLITS = {}
CAP_Y = {"hook": 1130, "clues": 1150, "reveal": 1170, "board": 1190, "shout": 1170, "clear": 1235, "found": 1150,
         "fund": 1160, "ps5": 1160, "follow": 1080, "decide": 1110, "end": 1150}
BACKGROUNDS.update({"cafe_dim": lambda: art.blurred(set_cafe(on=(1, 2, 3)), 2, .9)})

def cash_box(ctx, x, y, s, scratch=0., label=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    src(ctx, "#000", .3); rrect(ctx, -172, -132, 352, 180, 14); ctx.fill()
    rrect(ctx, -170, -110, 340, 150, 14); fill_stroke(ctx, "#6f9a80", INK, 5)
    rrect(ctx, -180, -142, 360, 50, 12); fill_stroke(ctx, "#5d8670", INK, 5)
    rrect(ctx, -26, -112, 52, 38, 6); fill_stroke(ctx, "#e8c23a", INK, 3.5)
    src(ctx, INK); ctx.rectangle(-5, -102, 10, 16); ctx.fill()
    if label: art.text(ctx, (("CASH", "#2a4a38"),), "lilita", 34, 0, -10)
    if scratch > .01:
        for k in range(3):
            x0 = 70 + k*26; ln = scratch
            ctx.move_to(x0, -70); ctx.line_to(x0 + 46*ln, -70 + 84*ln)
            src(ctx, "#3a2a1a"); ctx.set_line_width(10); ctx.stroke_preserve()
            src(ctx, "#ffd9a0"); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()

def cat_shadow(ctx, x, y, s, a=.75, eyes=0., tail_glow=0.):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    src(ctx, "#06120a", a)
    art.ell(ctx, 0, -60, 150, 62); ctx.fill()
    art.ell(ctx, -120, -70, 70, 58); ctx.fill()
    for side in (-1, 1):
        art.poly(ctx, [(-120+side*48, -100), (-120+side*30, -150), (-120+side*12, -112)]); ctx.fill()
    ctx.move_to(130, -30); ctx.curve_to(210, -40, 200, -140, 150, -170)
    if tail_glow > .01:
        src(ctx, "#ffd21f", .9*tail_glow); ctx.set_line_width(36); ctx.stroke_preserve()
    src(ctx, "#06120a", a); ctx.set_line_width(22); ctx.stroke()
    if eyes > .01:
        for side in (-1, 1):
            g = cairo.RadialGradient(-120+side*24, -80, 0, -120+side*24, -80, 40)
            g.add_color_stop_rgba(0, 1, .95, .3, .9*eyes); g.add_color_stop_rgba(1, 1, .95, .3, 0)
            ctx.set_source(g); ctx.arc(-120+side*24, -80, 40, 0, 6.3); ctx.fill()
            src(ctx, "#fff27a", eyes); art.ell(ctx, -120+side*24, -80, 12, 9); ctx.fill()
            src(ctx, "#111", eyes); art.ell(ctx, -120+side*24, -80, 3, 8); ctx.fill()
    ctx.restore()

def cctv(ctx, lt, stamp="03:12:4", rec=True):
    """green night-vision look over whatever is drawn"""
    ctx.save(); ctx.set_operator(cairo.OPERATOR_HSL_SATURATION); src(ctx, "#808080", .95); ctx.paint(); ctx.restore()
    src(ctx, "#0b3a1c", .5); ctx.paint()
    src(ctx, "#5aff8a", .07); ctx.paint()
    scanlines(ctx, lt, .14)
    g = cairo.RadialGradient(W/2, H/2, 300, W/2, H/2, 900); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, .7)
    ctx.set_source(g); ctx.paint()
    if rec and int(lt*2) % 2 == 0: src(ctx, "#ff2a2a"); ctx.arc(46, 46, 12, 0, 6.3); ctx.fill()
    art.text(ctx, (("REC", "#ffffff"),), "popx", 24, 66, 47, anchor="lm")
    art.text(ctx, (("CAM 01 · %s%d AM" % (stamp, int(lt) % 10), "#ffffff"),), "popx", 24, W-30, 47, anchor="rm")

def note500(ctx, x, y, s, rot=0., bite=False):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -80, -36, 160, 72, 6); fill_stroke(ctx, "#a7d8b6", INK, 3.5)
    src(ctx, "#6aa882"); ctx.arc(-46, 0, 20, 0, 6.3); ctx.fill()
    art.text(ctx, (("₹500", "#1f4d36"),), "pop", 30, 16, 2)
    if bite:
        for bx, by in ((80, -30), (62, -36), (80, -10)):
            src(ctx, "#1a1226"); ctx.arc(bx, by, 16, 0, 6.3); ctx.fill()
    ctx.restore()

def cat_plate(ctx, x, y, s, note=True, t=0.):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    src(ctx, "#000", .3); art.ell(ctx, 6, 18, 150, 34); ctx.fill()
    art.ell(ctx, 0, 0, 150, 40); fill_stroke(ctx, "#8a5ad0", INK, 5)
    art.ell(ctx, 0, -8, 118, 26); fill_stroke(ctx, "#b48cff", INK, 3)
    art.text(ctx, (("BILLU", "#ffffff"),), "lilita", 20, 0, 24)
    src(ctx, "#a5652a")
    for k in range(7): ctx.arc(-80 + k*22, -10 + (k % 2)*6, 7, 0, 6.3); ctx.fill()
    if note: note500(ctx, 20, -30, .9, rot=-.18 + math.sin(t*3)*.03)
    ctx.restore()

def missing_poster(ctx, x, y, sc, t):
    if sc <= .01: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(.04); ctx.scale(sc, sc)
    src(ctx, "#000", .35); rrect(ctx, -196, -246, 400, 500, 8); ctx.fill()
    rrect(ctx, -200, -250, 400, 500, 8); fill_stroke(ctx, "#fbf6e6", INK, 5)
    art.text(ctx, (("GAYAB!", "#c7262f"),), "lucky", 70, 0, -190)
    rrect(ctx, -150, -140, 300, 220, 6); fill_stroke(ctx, "#e9e2d0", INK, 3)
    cat(ctx, 40, 60, .9, t, awake=True)
    art.text(ctx, (("BILLU · CAFE CAT", "#2a1608"),), "lilita", 28, 0, 130)
    art.text(ctx, (("SUBAH SE NAHI DIKHA", "#6a5a4a"),), "popx", 22, 0, 180)
    src(ctx, "#c7262f"); ctx.arc(0, -246, 12, 0, 6.3); ctx.fill()
    ctx.restore()

def magnifier(ctx, x, y, r):
    src(ctx, "#ffffff", .1); ctx.arc(x, y, r, 0, 6.3); ctx.fill()
    src(ctx, INK); ctx.set_line_width(16); ctx.arc(x, y, r, 0, 6.3); ctx.stroke()
    src(ctx, "#d6a93a"); ctx.set_line_width(9); ctx.arc(x, y, r, 0, 6.3); ctx.stroke()
    a = .8; hx, hy = x + r*math.cos(a), y + r*math.sin(a)
    ctx.move_to(hx, hy); ctx.line_to(hx + 110*math.cos(a), hy + 110*math.sin(a))
    src(ctx, INK); ctx.set_line_width(34); ctx.stroke_preserve(); src(ctx, "#7a4a2a"); ctx.set_line_width(24); ctx.stroke()

def stamp(ctx, x, y, sc, txt, col="#2e9b5a", rot=-.22, size=40):
    if sc <= .01: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc)
    w = art.tw(txt, "lucky", size) + 40
    src(ctx, "#ffffff", .88); rrect(ctx, -w/2, -size*.8, w, size*1.6, 10); ctx.fill()
    src(ctx, col, .9); ctx.set_line_width(6); rrect(ctx, -w/2, -size*.8, w, size*1.6, 10); ctx.stroke()
    art.text(ctx, ((txt, col),), "lucky", size, 0, 2, alpha=.95)
    ctx.restore()

def avatar(ctx, x, y, s, col):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    src(ctx, col); ctx.arc(0, -20, 26, 0, 6.3); ctx.fill()
    ctx.move_to(-46, 50); ctx.curve_to(-46, 4, 46, 4, 46, 50); ctx.close_path(); ctx.fill()
    ctx.restore()

def detective_board(ctx, cx, top, sc, n, stamps, head=0., t=0.):
    if sc <= .01: return
    w, h = 660, 640
    ctx.save(); ctx.translate(cx, top); ctx.scale(sc, sc)
    src(ctx, "#000", .4); rrect(ctx, -w/2+8, 10, w, h, 14); ctx.fill()
    rrect(ctx, -w/2, 0, w, h, 14); fill_stroke(ctx, "#5a3a22", INK, 5)
    rrect(ctx, -w/2+18, 18, w-36, h-36, 8); fill_stroke(ctx, "#c8945a", None)
    src(ctx, "#a87440", .35)
    for k in range(60):
        ctx.arc(-w/2 + 30 + (k*97) % (w-60), 40 + (k*61) % (h-80), 3, 0, 6.3); ctx.fill()
    rrect(ctx, -200, 26, 400, 62, 8); fill_stroke(ctx, "#1e2a46", INK, 3)
    art.text(ctx, (("DETECTIVE BOARD", "#ffd21f"),), "lucky", 40, 0, 58)
    # culprit photo
    rrect(ctx, -90, 108, 180, 190, 4); fill_stroke(ctx, "#ffffff", INK, 3)
    rrect(ctx, -76, 122, 152, 130, 2); fill_stroke(ctx, "#3a3048", None)
    cat(ctx, 30, 238, .62, t, awake=True)
    art.text(ctx, (("CHOR: BILLU", "#c7262f"),), "lucky", 26, 0, 276)
    src(ctx, "#e83030"); ctx.arc(0, 112, 9, 0, 6.3); ctx.fill()
    xs = (-210, 0, 210)
    for k in range(min(n, 3)):
        x = xs[k]; y0 = 380
        src(ctx, "#c7262f"); ctx.set_line_width(4); ctx.move_to(0, 290); ctx.line_to(x, y0 - 6); ctx.stroke()
        ctx.save(); ctx.translate(x, y0 + 100); ctx.rotate((-.05, .03, -.02)[k])
        rrect(ctx, -96, -106, 192, 212, 4); fill_stroke(ctx, "#ffffff", INK, 3)
        rrect(ctx, -82, -92, 164, 120, 2); fill_stroke(ctx, ("#2f6db0", "#2e9b5a", "#e2862b")[k], None)
        avatar(ctx, 0, -40, 1.0, "#f3efe3")
        nm = "@" + DETECTIVES[k]
        fs = 22
        while art.tw(nm, "popx", fs) > 176 and fs > 12: fs -= 1
        art.text(ctx, ((nm, "#1b1b1b"),), "popx", fs, 0, 60)
        ctx.restore()
        src(ctx, "#e83030"); ctx.arc(x, y0 - 4, 9, 0, 6.3); ctx.fill()
        stamp(ctx, x + 20, y0 + 150, stamps[k], "SAHI!", "#1f8a3a", rot=-.25, size=34)
    if head > .01:
        ctx.save(); ctx.translate(-210, 372); ctx.scale(head, head)
        art.star(ctx, 0, 0, 48)
        rrect(ctx, -110, 34, 220, 40, 8); fill_stroke(ctx, "#ffd21f", INK, 3)
        art.text(ctx, (("HEAD DETECTIVE", "#c7262f"),), "lilita", 22, 0, 55)
        ctx.restore()
    ctx.restore()

def ps5(ctx, x, y, s, t=0.):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-60, 0); ctx.curve_to(-90, -150, -70, -300, -40, -330); ctx.line_to(40, -330); ctx.curve_to(70, -300, 90, -150, 60, 0); ctx.close_path()
    fill_stroke(ctx, "#f4f6fa", INK, 5)
    rrect(ctx, -26, -320, 52, 310, 10); fill_stroke(ctx, "#1b1d24", INK, 3)
    src(ctx, "#3f8cff", .6 + .4*math.sin(t*4)); ctx.rectangle(-20, -310, 40, 6); ctx.fill()
    art.text(ctx, (("PS5", "#1b1d24"),), "lucky", 34, 0, -60)
    ctx.restore()

def controller(ctx, x, y, s, rot=0.):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.move_to(-120, -30); ctx.curve_to(-150, 40, -150, 100, -100, 100); ctx.curve_to(-70, 100, -60, 40, -30, 40)
    ctx.line_to(30, 40); ctx.curve_to(60, 40, 70, 100, 100, 100); ctx.curve_to(150, 100, 150, 40, 120, -30)
    ctx.curve_to(100, -60, -100, -60, -120, -30); ctx.close_path(); fill_stroke(ctx, "#f4f6fa", INK, 5)
    src(ctx, "#1b1d24"); rrect(ctx, -40, -40, 80, 40, 8); ctx.fill()
    for k, (bx, by, col) in enumerate(((80, -24, "#4aff7a"), (100, -4, "#ff5a4a"), (60, -4, "#3fd8ff"), (80, 16, "#ff8adf"))):
        ctx.arc(bx, by, 9, 0, 6.3); fill_stroke(ctx, col, INK, 2)
    src(ctx, INK); ctx.rectangle(-96, -12, 36, 10); ctx.fill(); ctx.rectangle(-83, -25, 10, 36); ctx.fill()
    ctx.restore()

def goal_meter(ctx, cx, y, w, cur, goal, step=0, sc=1., label="PS5 FUND", flash=0.):
    if sc <= .01: return
    ctx.save(); ctx.translate(cx, y); ctx.scale(sc, sc)
    rrect(ctx, -w/2-10, -74, w+20, 160, 16); fill_stroke(ctx, "#120c22", "#3fd8ff", 4)
    art.text(ctx, ((label, "#3fd8ff"),), "lucky", 32, -w/2+10, -42, anchor="lm")
    art.text(ctx, (("GOAL ₹{:,}".format(goal), "#ffffff"),), "pop", 24, w/2-10, -42, anchor="rm")
    rrect(ctx, -w/2+10, -6, w-20, 56, 28); fill_stroke(ctx, "#2a2238", "#ffffff", 3)
    f = max(.04, min(1, cur/goal)); f2 = min(1, (cur + step)/goal)
    if step and flash > .01:
        src(ctx, "#ffd21f", .35 + .45*abs(math.sin(flash*8))); rrect(ctx, -w/2+16, 2, (w-32)*f2, 40, 20); ctx.fill()
    rrect(ctx, -w/2+16, 2, (w-32)*f, 40, 20); fill_stroke(ctx, "#4aff7a", None)
    art.text(ctx, (("₹{:,}".format(int(cur)), "#0b2a14"),), "pop", 24, -w/2+16 + (w-32)*f/2, 23)
    ctx.restore()

def follow_btn(ctx, x, y, sc, press=0.):
    if sc <= .01: return
    ctx.save(); ctx.translate(x, y); s = sc*(1 - .08*press); ctx.scale(s, s)
    src(ctx, "#000", .35); rrect(ctx, -196, -46, 400, 100, 22); ctx.fill()
    rrect(ctx, -200, -50, 400, 100, 22); fill_stroke(ctx, "#3897f0", "#ffffff", 5)
    art.text(ctx, (("FOLLOW  +", "#ffffff"),), "lucky", 56, 0, 2)
    ctx.restore()

def hisaab(ctx, cx, top, rows, sc=1., total=0., paid=0.):
    if sc <= .01: return
    w, rh = 640, 70
    h = 110 + 4*rh + 110
    ctx.save(); ctx.translate(cx, top); ctx.scale(sc, sc)
    src(ctx, "#000", .3); rrect(ctx, -w/2+8, 8, w, h, 10); ctx.fill()
    rrect(ctx, -w/2, 0, w, h, 10); fill_stroke(ctx, "#fbf6e6", INK, 4)
    art.text(ctx, (("CAFE FUND · HISAAB", "#2a1608"),), "lucky", 38, 0, 50)
    src(ctx, INK); ctx.set_dash([6, 6]); ctx.set_line_width(2); ctx.move_to(-w/2+30, 88); ctx.line_to(w/2-30, 88); ctx.stroke(); ctx.set_dash([])
    R = [("BACHA THA", "+ ₹10,300", "#1f6d3a"), ("BILLU SE MILA", "+ ₹19,000", "#1f6d3a"),
         ("KAL KE LIKES + SHARES", "+ ₹3,800", "#1f6d3a"), ("BILLS (RENT · BIJLI · NET)", "- ₹21,000", "#c7262f")]
    for i, k in enumerate(rows):
        if k <= .01: continue
        y = 130 + i*rh
        ctx.save(); ctx.translate(0, y); ctx.scale(1, k)
        art.text(ctx, ((R[i][0], "#2a1608"),), "lilita", 28, -w/2+36, 0, anchor="lm")
        art.text(ctx, ((R[i][1], R[i][2]),), "pop", 32, w/2-36, 0, anchor="rm")
        ctx.restore()
    yb = 110 + 4*rh + 50
    src(ctx, INK); ctx.set_line_width(3); ctx.move_to(-w/2+30, yb-40); ctx.line_to(w/2-30, yb-40); ctx.stroke()
    if total > .01:
        art.text(ctx, (("BACHA", "#2a1608"),), "lucky", 44, -w/2+36, yb, anchor="lm")
        ctx.save(); ctx.translate(w/2-36, yb); ctx.scale(total, total)
        art.text(ctx, (("₹12,100", "#1f6d3a"),), "pop", 54, 0, 0, anchor="rm"); ctx.restore()
    stamp(ctx, 235, 130 + 3*rh + 56, paid, "PAID!", "#1f8a3a", rot=-.12, size=32)
    ctx.restore()

def spot(ctx, x, top, bottom, a=.35):
    g = cairo.LinearGradient(x, top, x, bottom)
    g.add_color_stop_rgba(0, 1, .95, .7, a); g.add_color_stop_rgba(1, 1, .95, .7, .04)
    ctx.move_to(x-30, top); ctx.line_to(x+30, top); ctx.line_to(x+130, bottom); ctx.line_to(x-130, bottom); ctx.close_path()
    ctx.set_source(g); ctx.fill()

def zzz(ctx, x, y, t):
    for k in range(3):
        ph = (t*.6 + k/3) % 1
        art.text(ctx, (("z", "#ffffff"),), "lucky", 30 + 16*ph, x + 40*ph + k*6, y - 90*ph, alpha=1-ph, stroke=3, scol=INK)

def money_bed(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for r in range(3):
        for k in range(6 - r):
            note500(ctx, -200 + r*40 + k*80, -r*26, .75, rot=((k*37 + r*11) % 7 - 3)*.05)
    ctx.restore()


# =====================================================================
# Day 5 v3: Pro Zone owner claims Billu
# =====================================================================
CAP_Y.update({"knock": 1150, "claim": 1190, "dilemma": 1150, "decide": 1150, "cta": 1180, "end": 1150, "fund": 1160, "ps5": 1160})
OWNER = dict(skin=SKIN["l"], hair="spiky", hair_col="#1d1714", shirt="#6a3fc4", jacket="#1d1d22", pants="#2b2b33",
             shoes="#f2f2ee", seed=12, brow_tilt=-3, smile=.35)
OWNER_ANGRY = dict(OWNER, brow_tilt=9, smile=-.5)
PS5_GOAL = 55000

def owner_extras(ctx, x, y, s):
    hx, hy = head_pos(x, y, s)
    ctx.save(); ctx.translate(hx, hy); ctx.scale(s, s)
    for side in (-1, 1):
        rrect(ctx, side*34 - 28, -22, 56, 34, 10); fill_stroke(ctx, "#111", INK, 3)
        src(ctx, "#ffffff", .35); ctx.rectangle(side*34 - 20, -16, 12, 6); ctx.fill()
    src(ctx, INK); ctx.set_line_width(5); ctx.move_to(-6, -8); ctx.line_to(6, -8); ctx.stroke()
    ctx.restore()
    ctx.save(); ctx.translate(x, y - 340*s); ctx.scale(s, s)
    src(ctx, "#e8c23a"); ctx.set_line_width(9); ctx.arc(0, -20, 52, .3, math.pi - .3); ctx.stroke()
    ctx.restore()

def draw_owner(ctx, x, y, s, pose, t, angry=False, flip=False):
    art.person(ctx, x, y, s, OWNER_ANGRY if angry else OWNER, pose, t=t, flip=flip)
    owner_extras(ctx, x, y, s)

def cheque40(ctx, x, y, sc):
    if sc <= .01: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(-.05); ctx.scale(sc, sc)
    src(ctx, "#000", .3); rrect(ctx, -236, -86, 480, 180, 12); ctx.fill()
    rrect(ctx, -240, -90, 480, 180, 12); fill_stroke(ctx, "#efe6ff", INK, 4)
    art.text(ctx, (("PRO ZONE GAMING", "#6a3fc4"),), "lilita", 24, -60, -56)
    art.text(ctx, (("FOR: BILLU", "#2a1608"),), "popx", 20, -60, -18)
    art.text(ctx, (("₹40,000", "#6a3fc4"),), "pop", 64, 0, 40, stroke=0)
    ctx.restore()

def door(ctx, x, y, open_, t, silhouette=False):
    """cafe glass door seen from inside; open_ 0..1"""
    rrect(ctx, x - 170, y - 560, 340, 560, 8); fill_stroke(ctx, "#120c22", INK, 6)
    g = cairo.LinearGradient(0, y - 560, 0, y); g.add_color_stop_rgb(0, .55, .6, .9); g.add_color_stop_rgb(1, .25, .2, .45)
    ctx.set_source(g); ctx.rectangle(x - 150, y - 540, 300, 530); ctx.fill()
    if silhouette:
        src(ctx, "#0a0712", .9)
        ctx.arc(x, y - 400, 52, 0, 6.3); ctx.fill()
        rrect(ctx, x - 80, y - 350, 160, 340, 40); ctx.fill()
    w = 300*(1 - .85*open_)
    src(ctx, "#7fd0ff", .25); ctx.rectangle(x - 150, y - 540, w, 530); ctx.fill()
    rrect(ctx, x - 150 + w - 22, y - 300, 12, 80, 6); fill_stroke(ctx, "#d6a93a", INK, 2)
    art.text(ctx, (("LEVEL UP", "#ff3fa4"),), "lucky", 34, x - 150 + w/2, y - 470, alpha=.8)


# =====================================================================
# Day 6: Billu NOT FOR SALE
# =====================================================================
CAP_Y.update({"hook": 1150, "result": 1170, "angry": 1150, "fund": 1160, "doubt": 1150, "cctv": 1130, "liar": 1170, "why": 1170,
              "msg": 1190, "decide": 1150, "jersey": 1170, "army": 1170, "money": 1170, "share": 1170, "end": 1150})
FUND_ROWS = [("31 LIKES", "+ ₹3,100"), ("5 SHARES", "+ ₹1,000"), ("3 NAYE FOLLOWERS", "+ ₹1,500")]
B_COMMENTS = [("_.aryan._thakur", "Billu nhi bikegaaa"), ("justt_yachass_15", "B nhi dena billu"), ("biswaje3135c", "B")]

def comment_bubble(ctx, x, y, sc, user, txt):
    if sc <= .01: return
    ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc)
    w = max(art.tw(txt, "lilita", 30), art.tw("@" + user, "popx", 20)) + 110
    src(ctx, "#000", .3); rrect(ctx, -w/2 + 6, -40, w, 92, 20); ctx.fill()
    rrect(ctx, -w/2, -46, w, 92, 20); fill_stroke(ctx, "#ffffff", INK, 3)
    src(ctx, "#c13584"); ctx.arc(-w/2 + 46, 0, 26, 0, 6.3); ctx.fill()
    avatar(ctx, -w/2 + 46, 6, .45, "#ffffff")
    art.text(ctx, (("@" + user, "#6a6a6a"),), "popx", 20, -w/2 + 84, -18, anchor="lm")
    art.text(ctx, ((txt, "#1b1b1b"),), "lilita", 30, -w/2 + 84, 16, anchor="lm")
    ctx.restore()

def fund_card(ctx, cx, top, rows, sc, total):
    if sc <= .01: return
    w = 640
    ctx.save(); ctx.translate(cx, top); ctx.scale(sc, sc)
    src(ctx, "#000", .3); rrect(ctx, -w/2 + 8, 8, w, 420, 10); ctx.fill()
    rrect(ctx, -w/2, 0, w, 420, 10); fill_stroke(ctx, "#fbf6e6", INK, 4)
    art.text(ctx, (("PS5 FUND · KAL KI KAMAI", "#2a1608"),), "lucky", 36, 0, 50)
    src(ctx, INK); ctx.set_dash([6, 6]); ctx.set_line_width(2); ctx.move_to(-w/2 + 30, 88); ctx.line_to(w/2 - 30, 88); ctx.stroke(); ctx.set_dash([])
    for i, k in enumerate(rows):
        if k <= .01: continue
        y = 130 + i*70
        ctx.save(); ctx.translate(0, y); ctx.scale(1, k)
        art.text(ctx, ((FUND_ROWS[i][0], "#2a1608"),), "lilita", 32, -w/2 + 36, 0, anchor="lm")
        art.text(ctx, ((FUND_ROWS[i][1], "#1f6d3a"),), "pop", 34, w/2 - 36, 0, anchor="rm")
        ctx.restore()
    src(ctx, INK); ctx.set_line_width(3); ctx.move_to(-w/2 + 30, 330); ctx.line_to(w/2 - 30, 330); ctx.stroke()
    if total > .01:
        art.text(ctx, (("TOTAL", "#2a1608"),), "lucky", 44, -w/2 + 36, 376, anchor="lm")
        ctx.save(); ctx.translate(w/2 - 36, 376); ctx.scale(total, total)
        art.text(ctx, (("₹17,700", "#1f6d3a"),), "pop", 54, 0, 0, anchor="rm"); ctx.restore()
    ctx.restore()

def big_phone(ctx, x, y, sc, lines_on, t):
    if sc <= .01: return
    ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc); ctx.rotate(math.sin(t*2)*.02)
    rrect(ctx, -230, -380, 460, 760, 48); fill_stroke(ctx, "#111", INK, 6)
    rrect(ctx, -206, -350, 412, 700, 32); fill_stroke(ctx, "#0e1b16", None)
    rrect(ctx, -206, -350, 412, 90, 32); fill_stroke(ctx, "#3a1f6e", None)
    src(ctx, "#6a3fc4"); ctx.arc(-150, -305, 28, 0, 6.3); ctx.fill()
    art.text(ctx, (("PZ", "#ffffff"),), "lucky", 26, -150, -303)
    art.text(ctx, (("PRO ZONE", "#ffffff"),), "lucky", 34, -100, -305, anchor="lm")
    msgs = ["3v3 REMATCH.", "JEETE TO BILLU TUMHARA", "HAMESHA KE LIYE.", "HAARE... TO BILLU MERA! 😈"]
    msgs[-1] = "HAARE... TO BILLU MERA!"
    for k, m in enumerate(msgs):
        a = lines_on[k] if k < len(lines_on) else 0
        if a <= .01: continue
        yy = -210 + k*120
        ctx.save(); ctx.translate(-180, yy); ctx.scale(a, a)
        w = art.tw(m, "lilita", 30) + 40
        rrect(ctx, 0, -38, w, 76, 22); fill_stroke(ctx, "#2a2240" if k < 3 else "#7a1f2a", None)
        art.text(ctx, ((m, "#ffffff"),), "lilita", 30, 20, 0, anchor="lm")
        ctx.restore()
    ctx.restore()

def storefront(ctx, x, y, s, name, col, crowd, empty=False):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -150, -260, 300, 260, 8); fill_stroke(ctx, "#20182e", INK, 5)
    rrect(ctx, -160, -310, 320, 64, 10); fill_stroke(ctx, col, INK, 4)
    art.text(ctx, ((name, "#ffffff"),), "lucky", 32, 0, -278)
    src(ctx, "#ffd98a" if not empty else "#3a3448", .9 if not empty else .6); ctx.rectangle(-130, -230, 260, 200); ctx.fill()
    for k in range(crowd):
        avatar(ctx, -100 + (k % 5)*50, -60 - (k // 5)*60, .55, ("#2f6db0", "#c7262f", "#2e9b5a", "#e2862b", "#7a2fb0")[k % 5])
    if empty:
        art.text(ctx, (("KHAALI", "#9a90b0"),), "lucky", 40, 0, -120)
    ctx.restore()

def shot_world(ctx, shot, lt, T, m):
    sid = shot["id"]; L = shot["L"]
    if sid == "hook":
        paint_bg(ctx, "blur2"); darken(ctx, .45)
        spot(ctx, W/2, 0, 1200, .45)
        cat(ctx, W/2 + 40, 1080, 1.35, lt, awake=True)
        cat_headset(ctx, W/2 + 40, 1080, 1.35)
    elif sid == "result":
        paint_bg(ctx, "cafe3"); darken(ctx, .3)
        cat(ctx, W/2 + 40, 1120, 1.1, lt, awake=True)
        art.person(ctx, 600, 1330, .6, MANAGER, "cheer", t=lt, mouth=m, flip=True)
    elif sid == "angry":
        ctx.save(); cam(ctx, 1.0, W/2, 700); paint_bg(ctx, "cafe3"); ctx.restore()
        darken(ctx, .45)
        slam = lt > lt_(shot, 1, .45)
        shake = math.sin(lt*70)*10 if slam and lt < lt_(shot, 1, .45) + .5 else 0
        ctx.save(); ctx.translate(shake, 0)
        door(ctx, W/2, 1000, 0 if slam else .85, lt)
        if not slam:
            draw_owner(ctx, W/2, 1140, .72, "point", lt, angry=True)
        ctx.restore()
        art.person(ctx, 110, 1330, .6, MANAGER_WORRIED, "shrug", t=lt, mouth=m)
    elif sid == "fund":
        paint_bg(ctx, "blur"); darken(ctx, .3)
        art.person(ctx, 600, 1330, .7, MANAGER, "cheer" if lt > lt_(shot, 2, 0) else "hold", t=lt, mouth=m, flip=True)
    elif sid == "doubt":
        paint_bg(ctx, "cafe3"); darken(ctx, .45)
        spot(ctx, 330, 0, 1200, .35)
        art.person(ctx, 330, 1250, .85, CHINTU_CONFUSED, "shrug", t=lt)
    elif sid == "cctv":
        on = lt > lt_(shot, 1, .2)
        ctx.save(); cam(ctx, 1.0 + .25*ease((lt - lt_(shot, 2, 0))/.8), W/2, 640); paint_bg(ctx, "cafe")
        console_shelf(ctx, W/2, 560, .95, lt)
        if on: cat(ctx, W/2 + 80, 640, .8, lt, awake=False)
        ctx.restore()
        if on:
            cctv(ctx, lt, stamp="02:41:1")
            art.tag(ctx, "MAR 2026 · 8 MAHINE PEHLE", W/2, 120, "#120c22", "#4aff7a", 26, border="#4aff7a")
            if lt > lt_(shot, 2, .5):
                src(ctx, "#ff3a3a"); ctx.set_line_width(8); ctx.arc(W/2 + 60, 660, 150 + 6*math.sin(lt*8), 0, 6.3); ctx.stroke()
        else:
            paint_bg(ctx, "blur2"); darken(ctx, .3)
            art.person(ctx, 330, 1300, .75, CHINTU, "hold", t=lt)
            ctx.save(); ctx.translate(500, 860); ctx.scale(1.2, 1.2)
            rrect(ctx, -150, -100, 300, 190, 10); fill_stroke(ctx, "#1b1d24", INK, 5)
            src(ctx, "#0b3a1c"); ctx.rectangle(-134, -86, 268, 160); ctx.fill()
            art.text(ctx, (("CCTV ARCHIVE", "#4aff7a"),), "popx", 22, 0, -10)
            art.text(ctx, (("loading...", "#4aff7a"),), "popx", 16, 0, 20, alpha=.6 + .4*math.sin(lt*6))
            ctx.restore()
    elif sid == "liar":
        paint_bg(ctx, "blur2"); darken(ctx, .3)
        draw_owner(ctx, W/2, 1330, .95, "shrug", lt, angry=False)
    elif sid == "why":
        paint_bg(ctx, "blur2"); darken(ctx, .35)
        if lt < lt_(shot, 2, 0):
            cat(ctx, W/2 + 40, 1060, 1.2, lt, awake=True); cat_headset(ctx, W/2 + 40, 1060, 1.2)
            if lt > lt_(shot, 1, 0):
                for k in range(8):
                    a = (lt*.7 + k/8) % 1
                    big_heart(ctx, 120 + (k*83) % 480, 1000 - 500*a, .25 + .1*(k % 3))
        else:
            storefront(ctx, 190, 1060, .95, "PRO ZONE", "#6a3fc4", 0, empty=True)
            storefront(ctx, 530, 1060, .95, "LEVEL UP", "#ff3fa4", 10)
    elif sid == "msg":
        paint_bg(ctx, "blur2"); darken(ctx, .4)
        if int(lt*3) % 2 == 0: src(ctx, "#6a3fc4", .06); ctx.paint()
    elif sid == "decide":
        paint_bg(ctx, "blur2"); darken(ctx, .2)
        cat(ctx, 300, 1250, .75, lt, awake=True)
        art.person(ctx, 600, 1330, .6, MANAGER, "point", t=lt, mouth=m, flip=True)
    elif sid == "jersey":
        paint_bg(ctx, "blur2"); darken(ctx, .25)
        art.person(ctx, 600, 1330, .6, MANAGER, "point", t=lt, mouth=m, flip=True)
    elif sid == "army":
        paint_bg(ctx, "blur2"); darken(ctx, .3)
        cat(ctx, W/2 + 30, 1240, .8, lt, awake=True)
    elif sid == "money":
        paint_bg(ctx, "blur2"); darken(ctx, .25)
        art.person(ctx, 590, 1330, .6, MANAGER, "point", t=lt, mouth=m, flip=True)
        cat(ctx, 220, 1260, .7, lt, awake=True)
    elif sid == "share":
        paint_bg(ctx, "blur2"); darken(ctx, .3)
        draw_owner(ctx, 230, 1330, .75, "shrug", lt)
        art.person(ctx, 590, 1330, .6, MANAGER, "cheer", t=lt, mouth=m, flip=True)
    elif sid == "end":
        ctx.save(); cam(ctx, 1.0 + .1*ease(lt/L), W/2, 700); paint_bg(ctx, "cafe3"); ctx.restore()
        darken(ctx, .3)
        cat(ctx, W/2 + 60, 1080, 1.3, lt, awake=True); cat_headset(ctx, W/2 + 60, 1080, 1.3)
        art.person(ctx, 120, 1330, .55, CHINTU, "cheer", t=lt)
        draw_lucky(ctx, 620, 1330, .55, "cheer", lt)

def cues(shot):
    s = shot["id"]; c = {}
    if s == "hook":   c = dict(chq=(.15, "pop"), x=(lt_(shot, 1, .3), "hit"), nfs=(lt_(shot, 1, .55), "crowd"))
    if s == "result": c = dict(t=(lt_(shot, 0, .35), "pop"), b=(lt_(shot, 0, .85), "hit"), c0=(lt_(shot, 1, 0), "pop"),
                           c1=(lt_(shot, 1, .3), "pop"), c2=(lt_(shot, 1, .6), "pop"))
    if s == "angry":  c = dict(p=(lt_(shot, 0, .6), "hit"), slam=(lt_(shot, 1, .45), "hit"))
    if s == "fund":   c = dict(card=(lt_(shot, 0, .2), "whoosh"), r0=(lt_(shot, 1, .1), "pop"), r1=(lt_(shot, 1, .4), "pop"), r2=(lt_(shot, 1, .8), "ding"),
                           tot=(lt_(shot, 2, .5), "ding"), ps=(lt_(shot, 3, .2), "pop"), kam=(lt_(shot, 3, .6), "hit"))
    if s == "doubt":  c = dict(q=(lt_(shot, 0, .5), "pop"), six=(lt_(shot, 1, .1), "pop"), sach=(lt_(shot, 1, .7), "hit"))
    if s == "cctv":   c = dict(rec=(lt_(shot, 1, .2), "riser"), billu=(lt_(shot, 2, .5), "hit"))
    if s == "liar":   c = dict(nahi=(lt_(shot, 0, .6), "hit"), liar=(lt_(shot, 1, .3), "hit"))
    if s == "why":    c = dict(q=(.1, "pop"), fam=(lt_(shot, 1, .3), "crowd"), cust=(lt_(shot, 2, .2), "whoosh"))
    if s == "msg":    c = dict(ph=(.05, "ding"), m0=(lt_(shot, 1, .05), "pop"), m1=(lt_(shot, 1, .35), "pop"), m2=(lt_(shot, 1, .75), "pop"), m3=(lt_(shot, 2, .3), "hit"))
    if s == "decide": c = dict(title=(.05, "hit"), a=(lt_(shot, 1), "pop"), b=(lt_(shot, 2), "pop"), rule=(lt_(shot, 3, .1), "pop"))
    if s == "jersey": c = dict(j=(.1, "whoosh"), q=(lt_(shot, 0, .5), "pop"), best=(lt_(shot, 1, .3), "ding"), nm=(lt_(shot, 1, .7), "pop"))
    if s == "army":   c = dict(btn=(lt_(shot, 0, .2), "pop"), army=(lt_(shot, 0, .6), "crowd"), list=(lt_(shot, 1, .3), "riser"))
    if s == "money":  c = dict(like=(lt_(shot, 0, .05), "pop"), share=(lt_(shot, 0, .35), "pop"), fol=(lt_(shot, 0, .62), "ding"), bar=(lt_(shot, 0, .85), "pop"))
    if s == "share":  c = dict(pl=(.1, "whoosh"), j=(lt_(shot, 0, .6), "hit"))
    if s == "end":    c = dict(t=(.2, "hit"), boom=(lt_(shot, 0, .7), "crowd"))
    return c

def shot_ui(ctx, shot, lt, T):
    s = shot["id"]; c = cues(shot); P = lambda k, d=.28: pop_scale(lt, c[k][0], d)
    if s == "hook":
        art.tag(ctx, "DAY 6", W/2, 90, "#7a2fb0", size=28, sc=pop_scale(lt, .05))
        sc = P("chq", .35)
        if sc > .01 and lt < c["x"][0] + .4:
            cheque40(ctx, W/2, 330, sc*(1 - .3*ease((lt - c["x"][0])/.3)))
        if lt > c["x"][0]:
            ctx.save(); ctx.translate(W/2, 330); k = P("x", .3); ctx.scale(max(.02, k), max(.02, k))
            src(ctx, "#ff3a3a"); ctx.set_line_width(28)
            ctx.move_to(-160, -110); ctx.line_to(160, 110); ctx.move_to(160, -110); ctx.line_to(-160, 110); ctx.stroke(); ctx.restore()
        if lt > c["nfs"][0]:
            art.title(ctx, "NOT FOR SALE!", W/2, 560, 92, col="#4aff7a", sc=P("nfs", .35))
    elif s == "result":
        if lt > c["t"][0]: art.tag(ctx, "KAANTE KI TAKKAR...", W/2, 110, "#1e2a46", size=30, sc=P("t"))
        if lt > c["b"][0]:
            art.title(ctx, "MAJORITY NE KAHA: B!", W/2, 220, 70, col="#4aff7a", sc=P("b", .35))
            art.confetti(ctx, lt - c["b"][0], W/2, 260, n=40)
        for k, key in enumerate(("c0", "c1", "c2")):
            if lt > c[key][0]:
                comment_bubble(ctx, W/2 + (-30, 20, -10)[k], 420 + k*140, 1.35*P(key), B_COMMENTS[k][0], B_COMMENTS[k][1])
    elif s == "angry":
        if c["p"][0] < lt < c["slam"][0]: art.sticker(ctx, "PACHHTAOGE!", W/2, 230, 96, "#ff5a4a", sc=P("p", .35), rot=-.06)
        if lt > c["slam"][0]: art.sticker(ctx, "DHADAAM!", W/2, 260, 100, "#ffd21f", sc=P("slam", .3), rot=.06)
    elif s == "fund":
        rows = [P("r0", .25), P("r1", .25), P("r2", .25)]
        if lt < c["ps"][0]:
            fund_card(ctx, W/2, 110, rows, P("card", .35), total=P("tot", .35))
            if lt > c["r2"][0]: art.sticker(ctx, "FOLLOW = SABSE ZYADA!", W/2, 610, 46, "#ffd21f", sc=pop_scale(lt, c["r2"][0] + .2), rot=-.05)
        else:
            art.title(ctx, "MISSION PS5", W/2, 140, 84, col="#3fd8ff", sc=P("ps", .35))
            goal_meter(ctx, W/2, 330, 600, 17700, PS5_GOAL, sc=P("ps"))
            if lt > c["kam"][0]: art.sticker(ctx, "₹37,300 KAM!", W/2, 520, 76, "#ff5a4a", sc=P("kam", .35), rot=-.05)
    elif s == "doubt":
        if lt > c["q"][0] and lt < c["six"][0]:
            art.title(ctx, "?", 480, 560, 200, col="#ffd21f", sc=P("q", .35))
        if lt > c["six"][0]:
            art.tag(ctx, "\"6 MAHINE PEHLE BHAAGA THA\"", W/2, 220, "#6a3fc4", size=30, sc=P("six"))
        if lt > c["sach"][0]: art.sticker(ctx, "SACH MEIN?", W/2, 360, 90, "#ffd21f", sc=P("sach", .35), rot=-.06)
    elif s == "cctv":
        if lt > c["billu"][0]: art.sticker(ctx, "BILLU ISI CAFE MEIN THA!", W/2, 300, 54, "#ffd21f", sc=P("billu", .35), rot=-.05)
    elif s == "liar":
        if lt > c["nahi"][0]: art.tag(ctx, "BILLU KABHI PRO ZONE KA NAHI THA", W/2, 150, "#1e2a46", size=28, sc=P("nahi"))
        if lt > c["liar"][0]:
            stamp(ctx, W/2, 420, P("liar", .3), "JHOOTHA!", "#c7262f", rot=-.15, size=84)
    elif s == "why":
        art.title(ctx, "BILLU KYUN CHAHIYE?", W/2, 130, 70, col="#ffd21f", sc=P("q", .35))
        if c["fam"][0] < lt < c["cust"][0]:
            art.sticker(ctx, "BILLU = FAMOUS!", W/2, 290, 76, "#ff3fa4", sc=P("fam", .35), rot=-.05)
            art.tag(ctx, "TUMHARI WAJAH SE", W/2, 390, "#7a2fb0", size=30, sc=pop_scale(lt, c["fam"][0] + .25))
        if lt > c["cust"][0]:
            art.sticker(ctx, "CUSTOMERS HAMARE PAAS!", W/2, 300, 56, "#4aff7a", sc=P("cust", .35), rot=-.05)
    elif s == "msg":
        on = [P("m0"), P("m1"), P("m2"), P("m3")]
        big_phone(ctx, W/2, 640, P("ph", .35)*.95, on, lt)
        if lt > c["m3"][0]: art.sticker(ctx, "CHALLENGE!", W/2, 150, 90, "#ff5a4a", sc=P("m3", .35), rot=-.06)
    elif s == "decide":
        art.title(ctx, "FAISLA TUMHARA!", W/2, 120, 86, sc=P("title", .35))
        cur = -1
        for k, key in enumerate(("a", "b")):
            if lt > c[key][0]: cur = k
        for k, (key, L_, t_, col) in enumerate((("a", "A", "CHALLENGE ACCEPT! BILLU KE LIYE KHELO", "#2e9b5a"),
                                                 ("b", "B", "CCTV DIKHAO, JHOOTH EXPOSE KARO", "#c7262f"))):
            art.option(ctx, W/2, 270 + k*110, 660, L_, t_, col, k == cur and lt < c["rule"][0], sc=P(key))
        if lt > c["rule"][0]:
            art.tag(ctx, "COMMENT  A  ya  B", W/2, 520, "#c7262f", size=34, sc=P("rule"))
            art.tag(ctx, "MOST COMMENTED OPTION WINS", W/2, 590, "#ffd21f", "#1b1208", 24, sc=pop_scale(lt, c["rule"][0] + .2), border="#1b1208")
    elif s == "jersey":
        sc = P("j", .35)
        if sc > .01:
            ctx.save(); ctx.translate(W/2 - 60, 560); ctx.scale(sc*1.5, sc*1.5); jersey(ctx, 0, 0, 1.0, "??????", "1"); ctx.restore()
        if lt > c["q"][0]: art.title(ctx, "JERSEY PE KYA LIKHEIN?", W/2, 140, 64, col="#ffd21f", sc=P("q", .35))
        if lt > c["best"][0]: art.sticker(ctx, "BEST LINE = JERSEY PE!", W/2, 880, 50, "#4aff7a", sc=P("best"), rot=-.05)
        if lt > c["nm"][0]: art.tag(ctx, "+ TUMHARA NAAM", W/2, 960, "#120c22", "#ffd21f", 30, sc=P("nm"), border="#ffd21f")
    elif s == "army":
        follow_btn(ctx, W/2, 160, P("btn", .35), press=max(0, math.sin(lt*5))*.6)
        if lt > c["army"][0]: art.title(ctx, "BILLU ARMY", W/2, 300, 100, col="#ff3fa4", sc=P("army", .35))
        if lt > c["list"][0]:
            sc = P("list", .35)
            ctx.save(); ctx.translate(W/2, 600); ctx.scale(max(.02, sc), max(.02, sc))
            rrect(ctx, -270, -170, 540, 340, 16); fill_stroke(ctx, "#120c22", "#ff3fa4", 4)
            art.text(ctx, (("DAY 7 · NEW MEMBERS", "#ff3fa4"),), "lucky", 32, 0, -130)
            for k in range(3):
                avatar(ctx, -200, -50 + k*80, .55, "#ffffff")
                art.text(ctx, (("@tumhara_naam" if k == 0 else "@........", "#ffffff"),), "popx", 30, -150, -44 + k*80, anchor="lm",
                         alpha=1 if k == 0 else .5)
            ctx.restore()
    elif s == "money":
        art.title(ctx, "PS5 FUND", W/2, 110, 80, col="#3fd8ff", sc=pop_scale(lt, .05, .35))
        if lt > c["like"][0]:
            sc = P("like", .35)
            ctx.save(); ctx.translate(150, 330); ctx.scale(max(.02, sc*.7), max(.02, sc*.7)); big_heart(ctx, 0, 0, 1.0)
            art.text(ctx, (("₹100", "#ffffff"),), "pop", 52, 0, 130, stroke=5, scol="#1b1208"); ctx.restore()
        if lt > c["share"][0]:
            sc = P("share", .35)
            ctx.save(); ctx.translate(360, 330); ctx.scale(max(.02, sc*.8), max(.02, sc*.8)); paper_plane(ctx, 0, -10, 1.0)
            art.text(ctx, (("₹200", "#4aff7a"),), "pop", 52, 0, 120, stroke=5, scol="#1b1208"); ctx.restore()
        if lt > c["fol"][0]:
            sc = P("fol", .35)
            ctx.save(); ctx.translate(575, 320); ctx.scale(max(.02, sc*.42), max(.02, sc*.42)); follow_btn(ctx, 0, 0, 1.0); ctx.restore()
            art.text(ctx, (("₹500", "#ffd21f"),), "pop", 60, 575, 420, scale=max(.02, sc), stroke=5, scol="#1b1208")
        if lt > c["bar"][0]: goal_meter(ctx, W/2, 620, 600, 17700, PS5_GOAL, sc=P("bar"))
    elif s == "share":
        sc = P("pl", .35)
        ctx.save(); ctx.translate(W/2 + 60, 400); ctx.scale(max(.02, sc*1.3), max(.02, sc*1.3)); paper_plane(ctx, 0, 0, 1.0); ctx.restore()
        art.title(ctx, "JHOOTHE DOST KO BHEJO", W/2, 160, 62, col="#ffd21f", sc=pop_scale(lt, .15, .35))
        if lt > c["j"][0]: stamp(ctx, 230, 700, P("j", .3), "PRO ZONE JAISA!", "#c7262f", rot=-.12, size=40)
    elif s == "end":
        art.title(ctx, "BILLU HAMARA HAI!", W/2, 170, 84, col="#4aff7a", sc=P("t", .35))
        art.confetti(ctx, lt - c["boom"][0], W/2, 200, n=40)
        art.tag(ctx, "VOTING BAND: 28 NOV, 8 PM", W/2, 300, "#c7262f", size=26, sc=pop_scale(lt, c["boom"][0] + .1))
        art.tag(ctx, "DAY 7: 29 NOV · 7:30 PM", W/2, 360, "#7a2fb0", size=26, sc=pop_scale(lt, c["boom"][0] + .25))
