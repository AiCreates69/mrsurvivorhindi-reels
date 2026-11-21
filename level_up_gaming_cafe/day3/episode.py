"""EPISODE: Level Up Gaming Cafe — Day 3   (@tumhoboss)
Branch: C won Decision #2 (battery upgrade). New 3rd player: Subham (most-liked tag).
Hook = the cafe is about to close (bills). One CTA: like = Rs 100, share = Rs 200.
Render:  python -m srs.engine path/to/episode.py [--sheet | --frames 3.0,20.5]
"""
import math, os as _os
import cairo
from srs import art
from srs.art import W, H, src, rrect, fill_stroke, ease, eout, bout, pop_scale, SKIN, INK
from srs.engine import lt_, cam, paint_bg
import numpy as _np, soundfile as _sf
from srs import voice as _V

TITLE = "Level Up Gaming Cafe — Day 3"
OUTPUT = "Level_Up_Gaming_Cafe_Day3.mp4"
VOICE = "hm_omega"
END_HOLD = 1.6

NEW_PLAYER = "SUBHAM"
GIFT_BY = "awaaz_of_meerut_"
IDEA_BY = ["justt_yachass_15", "aditya_rajput_42045", "awaaz_of_meerut_", "sultan_sheikh_0195"]
BILLS = [("RENT", 15000), ("BIJLI BILL", 4500), ("INTERNET", 1500)]
BILL_TOTAL = sum(v for _, v in BILLS)        # 21,000
PRIZE = 10000

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

# ---------------- script (offline voice; captions = the same words) ----------------
LINES = [
 ("hook",    "बॉस... कैफ़े बंद होने वाला है!",                      "Boss... cafe *band* hone wala hai!"),
 ("rewind",  "पर पहले... कल रात का मैच!",                          "Par pehle... kal raat ka *match*!"),
 ("result",  "मेजॉरिटी ने कहा... ऑप्शन सी! और सजेस्ट किया... बैटरी अपग्रेड!", "*Majority* ne kaha... option *C*!... Aur suggest kiya *battery upgrade*!"),
 ("battery", "चिंटू ने नई बैटरी लगाई...",                           "*Chintu* ne nayi battery lagayi..."),
 ("battery", "और तीनों पीसी... वापस ऑन!",                          "Aur teeno PC... *wapas ON*!"),
 ("win",     "लास्ट राउंड... पिंकी दीदी ने... हेडशॉट!",                 "Last round... *Pinky didi* ne... *headshot*!"),
 ("win",     "लेवल अप जीत गया!",                                 "*Level Up* jeet gaya!"),
 ("win",     "प्राइज़ मिला... दस हज़ार रुपये!",                       "Prize mila... *₹10,000*!"),
 ("player",  "और टीम का नया प्लेयर... शुभम!",                      "Aur team ka *naya player*... *Subham*!"),
 ("gift",    "और एक बॉस ने गिफ़्ट भेजा... जी टी ए सिक्स!",                "Aur ek boss ne gift bheja... *GTA 6*!"),
 ("gift",    "पर कैफ़े में पी एस फ़ाइव... है ही नहीं!",                   "Par cafe mein *PS5*... hai hi nahi!"),
 ("bills",   "पर अगले दिन... दरवाज़े पे एक लेटर।",                   "Par agle din... darwaze pe ek *letter*."),
 ("bills",   "महीने के बिल्स!",                                   "Mahine ke *bills*!"),
 ("bills",   "रेंट... पंद्रह हज़ार।",                                "Rent... *₹15,000*."),
 ("bills",   "बिजली... साढ़े चार हज़ार। इन्वर्टर का कमाल!",            "Bijli... *₹4,500*. Inverter ka *kamaal*!"),
 ("bills",   "इंटरनेट... पंद्रह सौ।",                                "Internet... *₹1,500*."),
 ("bills",   "टोटल... इक्कीस हज़ार!",                               "Total... *₹21,000*!"),
 ("fund",    "पिंकी दीदी का मैगी स्टॉल भी पैसे देता था...",              "Pinky didi ka *Maggi stall* bhi paise deta tha..."),
 ("fund",    "पर दीदी खेल रही थीं... तो स्टॉल बंद! कोई कमाई नहीं!",      "Par didi khel rahi thin... to stall *band*! Koi *kamaai* nahi!"),
 ("fund",    "फंड में? प्राइज़ के दस हज़ार... और तुम्हारे लाइक्स के नौ हज़ार!", "Fund mein? Prize ke *₹10,000*... aur tumhare likes ke *₹9,000*!"),
 ("fund",    "फिर भी... दो हज़ार कम!",                               "Phir bhi... *₹2,000 kam*!"),
 ("fund",    "तीन दिन में बिल नहीं भरा... तो कैफ़े पे ताला!",           "3 din mein bill nahi bhara... to cafe pe *taala*!"),
 ("cta",     "सिर्फ़ तुम बचा सकते हो, बॉस।",                        "Sirf *tum* bacha sakte ho, boss."),
 ("cta",     "हर लाइक... सौ रुपये।",                               "Har *like*... *₹100*."),
 ("cta",     "हर शेयर... दो सौ रुपये!",                             "Har *share*... *₹200*!"),
 ("cta",     "सिर्फ़ दस शेयर... और कैफ़े बच जाएगा!",                   "Sirf *10 share*... aur cafe *bach jayega*!"),
 ("cta",     "ये रील अपने गेमर ग्रुप में भेजो!",                       "Ye reel apne *gamer group* mein bhejo!"),
 ("decide",  "और पैसे कहाँ से लाएँ? तुम बताओ!",                     "Aur paise kahan se layein? *Tum* batao!"),
 ("decide",  "ए... लेट नाइट टूर्नामेंट, एंट्री फ़ीस लो!",               "*A*... late night tournament, *entry fee* lo!"),
 ("decide",  "बी... पिंकी दीदी का मैगी स्टॉल, कैफ़े के बाहर!",            "*B*... Pinky didi ka *Maggi stall*, cafe ke bahar!"),
 ("decide",  "सी... तुम्हारा अपना आइडिया! कमेंट में प्लान लिखो!",         "*C*... tumhara *apna idea*! Comment mein *plan* likho!"),
 ("decide",  "सबसे ज़्यादा कमेंट्स वाला ऑप्शन जीतेगा!",               "Sabse zyada *comments* wala option jeetega!"),
 ("end",     "कैफ़े खुला रहेगा... या बंद? बॉस... तुम हो!",              "Cafe khula rahega... ya *band*? Boss... *tum* ho!"),
]

SHOTS = [
 ("hook", "cut"), ("rewind", "whip"), ("result", "cut"), ("battery", "whip"), ("win", "cut"), ("player", "whip"), ("gift", "cut"),
 ("bills", "iris"), ("fund", "cut"), ("cta", "whip"), ("decide", "wipe"), ("end", "cut"),
]

# ---------------- the user's ElevenLabs voiceover ----------------
_UV = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "build", "user_voice")
USER_VOICE = all(_os.path.exists(_os.path.join(_UV, "%03d.wav" % (i+1))) for i in range(len(LINES)))

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
SPLITS = {3: [(1.03, 1.24), (1.96, 2.26)], 33: [(1.18, 1.59), (3.07, 3.31)]}

if USER_VOICE:
    _SAYS = [l[1] for l in LINES]
    def _user_line(say, cap, voice, cache, lang="hi"):
        i = _SAYS.index(say)
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
    _V.polish = lambda v, c: v

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

# ---------------- shots ----------------
def shot_world(ctx, shot, lt, T, m):
    sid = shot["id"]; L = shot["L"]
    if sid == "hook":
        ctx.save(); cam(ctx, 1.0 + .08*ease(lt/L), W/2, 700); paint_bg(ctx, "street")
        k = eout((lt - .15)/1.4)
        shutter(ctx, 170, 700, 470, 470 + 360*k)
        if lt > lt_(shot, 0, .55): notice(ctx, 440, 650, pop_scale(lt, lt_(shot, 0, .55)))
        ctx.restore()
        if int(lt*5) % 2 == 0: src(ctx, "#ff1a1a", .14); ctx.rectangle(0, 0, W, H); ctx.fill()
        art.person(ctx, 160 + math.sin(lt*30)*3, 1280, 1.1, MANAGER_WORRIED, "shrug", t=lt, mouth=m)
        sweat_drop(ctx, 250, 640 + 40*((lt*1.3) % 1), 1.0)
    elif sid == "rewind":
        ctx.save(); cam(ctx, 1.05, W/2, 640); paint_bg(ctx, "cafe3"); ctx.restore()
        for x, who in ((150, "l"), (360, "c"), (570, "p")):
            if who == "l": draw_lucky(ctx, x, 1180, .62, "idle", lt)
            elif who == "c": art.person(ctx, x, 1180, .62, CHINTU, "idle", t=lt)
            else: draw_pinky(ctx, x, 1180, .62, "idle", lt)
            headphones(ctx, x, 1180, .62)
        darken(ctx, .25)
        scanlines(ctx, lt)
    elif sid == "result":
        paint_bg(ctx, "blur2")
        art.person(ctx, 560, 1330, .95, MANAGER, "cheer" if lt > lt_(shot, 0, .3) else "point", t=lt, mouth=m, flip=True)
    elif sid == "battery":
        on = lt > lt_(shot, 1, .55)
        ctx.save(); cam(ctx, 1.0 + .06*ease(lt/L), W/2, 700); paint_bg(ctx, "cafe3" if on else "cafe_off"); ctx.restore()
        if not on: darken(ctx, .55)
        ch = ease((lt - .3)/max(.5, lt_(shot, 1, .5) - .3))
        big_battery(ctx, 220, 1060, .95, ch, lt)
        art.person(ctx, 510, 1190, .9, CHINTU, "cheer" if on else "hold", t=lt)
        chappal(ctx, 585, 1190-520, .7, rot=.5 + math.sin(lt*7)*.2)
        if on:
            for i in (1, 2, 3):
                g = cairo.RadialGradient(MON_X[i], 470, 10, MON_X[i], 470, 160); g.add_color_stop_rgba(0, .4, 1, .6, .35); g.add_color_stop_rgba(1, .4, 1, .6, 0)
                ctx.set_source(g); ctx.rectangle(MON_X[i]-170, 300, 340, 340); ctx.fill()
    elif sid == "win":
        ctx.save(); cam(ctx, 1.0 + .05*ease(lt/L), W/2, 760); paint_bg(ctx, "cafe3"); ctx.restore()
        cheer = lt > lt_(shot, 1, 0)
        for x, who in ((150, "lucky"), (360, "chintu"), (570, "pinky")):
            if who == "lucky": draw_lucky(ctx, x, 1180, .62, "cheer" if cheer else "idle", lt)
            elif who == "chintu": art.person(ctx, x, 1180, .62, CHINTU, "cheer" if cheer else "idle", t=lt)
            else: draw_pinky(ctx, x, 1180, .62, "cheer" if lt > lt_(shot, 0, .6) else "point", lt)
            headphones(ctx, x, 1180, .62)
    elif sid == "player":
        ctx.save(); cam(ctx, 1.0 + .06*ease(lt/L), W/2, 860); paint_bg(ctx, "vip")
        k = eout((lt - .2)/.9)
        x = 760 - 400*k
        art.person(ctx, x, 1170, .78, SUBHAM, "cheer" if lt > lt_(shot, 0, .7) else "idle", t=lt)
        headphones(ctx, x, 1170, .78)
        ctx.restore()
    elif sid == "gift":
        ctx.save(); cam(ctx, 1.0 + .06*ease(lt/L), W/2, 760); paint_bg(ctx, "cafe3"); ctx.restore()
        darken(ctx, .2)
        t2 = lt_(shot, 1, 0)
        if lt < t2 + .2:
            op = ease((lt - lt_(shot, 0, .5))/.5)
            gift_box(ctx, W/2, 1000, 1.0, op)
            if op > .01:
                k = eout((lt - lt_(shot, 0, .55))/.6)
                game_case(ctx, W/2, 1000 - 380*k, .55 + .45*k, rot=-.08*k)
        else:
            console_shelf(ctx, 330, 880, .9, lt)
            game_case(ctx, 110, 1080, .5, rot=-.15)
            art.person(ctx, 610, 1250, .78, CHINTU_CONFUSED, "shrug", t=lt)
    elif sid == "bills":
        paint_bg(ctx, "blur")
        darken(ctx, .3)
        if lt < lt_(shot, 1, 0) + .2:
            k = eout((lt - .1)/.8); envelope(ctx, W/2 - 300 + 300*k, 640, 1.1, open_=ease((lt - lt_(shot, 0, .7))/.4))
        art.person(ctx, 580, 1330, .85, MANAGER_WORRIED, "shrug" if lt > lt_(shot, 5, 0) else "hold", t=lt, mouth=m, flip=True)
    elif sid == "fund":
        paint_bg(ctx, "blur_street"); darken(ctx, .25)
        if lt < lt_(shot, 2, 0):
            maggi_stall(ctx, 470, 1000, .95, closed=lt > lt_(shot, 1, .45))
            if lt > lt_(shot, 1, .1): draw_pinky(ctx, 640, 1180, .42, "cheer", lt); headphones(ctx, 640, 1180, .42)
        if lt > lt_(shot, 4, .4):
            padlock(ctx, W/2, 760, pop_scale(lt, lt_(shot, 4, .4), .35)*1.0, shake=math.sin(lt*40)*4 if lt < lt_(shot, 4, .4)+.5 else 0)
        art.person(ctx, 150, 1300, .95, MANAGER_WORRIED, "shrug", t=lt, mouth=m)
    elif sid == "cta":
        paint_bg(ctx, "blur2")
        z = 1.0 + .25*ease(lt/1.2)
        ctx.save(); ctx.translate(W/2, 1500); ctx.scale(z, z); ctx.translate(-W/2, -1500)
        art.person(ctx, 360, 1560, 1.55, MANAGER_SERIOUS if lt < lt_(shot, 1, 0) else MANAGER, "point" if lt > lt_(shot, 1, 0) else "hold", t=lt, mouth=m)
        ctx.restore()
    elif sid == "decide":
        paint_bg(ctx, "blur2")
        art.person(ctx, 590, 1310, .9, MANAGER, "point", t=lt, mouth=m, flip=True)
        draw_pinky(ctx, 150, 1300, .55, "cheer" if lt > lt_(shot, 2, 0) else "idle", lt)
    elif sid == "end":
        ctx.save(); cam(ctx, 1.0 + .12*ease(lt/L), W/2, 600); paint_bg(ctx, "street")
        shutter(ctx, 170, 700, 470, 470 + 200*ease((lt - .2)/1.5))
        ctx.restore()
        if lt > lt_(shot, 0, .55):
            darken(ctx, .2)

def cues(shot):
    s = shot["id"]; c = {}
    if s == "hook":    c = dict(day=(.05, "pop"), shut=(.15, "whoosh"), seal=(lt_(shot, 0, .55), "hit"))
    if s == "rewind":  c = dict(rw=(.05, "whoosh"), sc=(lt_(shot, 0, .5), "pop"))
    if s == "result":  c = dict(a=(.05, "pop"), b=(.15, "pop"), c=(.25, "pop"), win=(lt_(shot, 0, .3), "hit"), idea=(lt_(shot, 0, .62), "ding"))
    if s == "battery": c = dict(bt=(.3, "pop"), on=(lt_(shot, 1, .55), "ding"))
    if s == "win":     c = dict(hs=(lt_(shot, 0, .7), "hit"), sc=(lt_(shot, 1, .1), "crowd"), chq=(lt_(shot, 2, .4), "ding"))
    if s == "player":  c = dict(tag=(.3, "pop"), name=(lt_(shot, 0, .65), "hit"), jer=(lt_(shot, 0, .7), "crowd"))
    if s == "gift":    c = dict(tag=(lt_(shot, 0, .55), "pop"), ps=(lt_(shot, 1, .55), "hit"))
    if s == "bills":   c = dict(env=(.1, "whoosh"), fan=(lt_(shot, 1, .1), "hit"), r0=(lt_(shot, 2, .4), "pop"), r1=(lt_(shot, 3, .3), "pop"),
                            r2=(lt_(shot, 4, .4), "pop"), tot=(lt_(shot, 5, .45), "hit"))
    if s == "fund":    c = dict(stall=(.1, "pop"), shut=(lt_(shot, 1, .45), "hit"), zero=(lt_(shot, 1, .7), "pop"),
                            m=(lt_(shot, 2, .05), "pop"), lk=(lt_(shot, 2, .6), "pop"), kam=(lt_(shot, 3, .5), "hit"),
                            lock=(lt_(shot, 4, .4), "hit"), days=(lt_(shot, 4, .55), "riser"))
    if s == "cta":     c = dict(tum=(lt_(shot, 0, .4), "hit"), like=(lt_(shot, 1, .2), "pop"), share=(lt_(shot, 2, .2), "ding"),
                            ten=(lt_(shot, 3, .2), "riser"), safe=(lt_(shot, 3, .75), "crowd"), grp=(lt_(shot, 4, .05), "whoosh"))
    if s == "decide":  c = dict(title=(.05, "hit"), a=(lt_(shot, 1), "pop"), b=(lt_(shot, 2), "pop"), c=(lt_(shot, 3), "pop"), rule=(lt_(shot, 4, .1), "pop"))
    if s == "end":     c = dict(q=(.2, "riser"), boss=(lt_(shot, 0, .7), "crowd"))
    return c

def shot_ui(ctx, shot, lt, T):
    s = shot["id"]; c = cues(shot); P = lambda k, d=.28: pop_scale(lt, c[k][0], d)
    if s == "hook":
        art.tag(ctx, "DAY 3", W/2, 70, "#7a2fb0", size=28, sc=P("day"))
        art.title(ctx, "CAFE BAND?!", W/2, 200, 96, col="#ff5a4a", sc=P("shut", .35))
    elif s == "rewind":
        art.text(ctx, (("<< KAL RAAT", "#ffffff"),), "lucky", 64, W/2, 180, stroke=6, scol="#1b1208")
        sc = P("sc")
        if sc > .01:
            ctx.save(); ctx.translate(W/2, 360); ctx.scale(sc, sc)
            rrect(ctx, -270, -50, 540, 100, 12); fill_stroke(ctx, "#1e2a46", "#ffffff", 4)
            art.text(ctx, (("LEVEL UP  2 - 2  PRO ZONE", "#ffffff"),), "lucky", 34, 0, 2)
            ctx.restore()
        art.sticker(ctx, "LAST ROUND", W/2, 520, 60, "#ff8a1e", sc=P("sc", .4), rot=-.05)
    elif s == "result":
        art.title(ctx, "RESULT!", W/2, 120, 96, sc=P("a", .35))
        for k, (key, L_, t_, col) in enumerate((("a", "A", "PINKY DI KA PC ON", "#2e9b5a"), ("b", "B", "LUCKY SOLO 2 vs 3", "#c7262f"),
                                                 ("c", "C", "BATTERY UPGRADE", "#1e2a46"))):
            win = L_ == "C" and lt > c["win"][0]
            art.option(ctx, W/2, 260 + k*104, 640, L_, t_, col, win, sc=P(key))
        art.confetti(ctx, lt - c["win"][0], 560, 470, n=40)
        art.sticker(ctx, "MAJORITY KA FAISLA!", W/2, 600, 56, "#ffd21f", sc=P("win"), rot=-.05)
        if lt > c["idea"][0]:
            art.tag(ctx, "IDEA BY", 220, 695, "#ff3fa4", size=24, sc=P("idea"))
            for i, nm in enumerate(IDEA_BY):
                art.tag(ctx, "@" + nm, 220, 750 + i*50, "#120c22", "#ffd21f", 24, sc=pop_scale(lt, c["idea"][0] + .2 + i*.2), border="#ffd21f")
    elif s == "battery":
        art.tag(ctx, "₹2,500 = NAYI BATTERY", W/2, 140, "#1f4d36", "#ffd21f", 30, sc=P("bt"), border="#ffd21f")
        if lt > c["on"][0]:
            art.sticker(ctx, "3 / 3 PC ON!", W/2, 290, 80, "#4aff7a", sc=P("on"), rot=-.06)
    elif s == "win":
        if c["hs"][0] < lt < c["sc"][0]:
            art.sticker(ctx, "HEADSHOT!", W/2, 250, 96, "#ff5a4a", sc=P("hs"), rot=-.08)
        if lt > c["sc"][0]:
            sc = P("sc")
            ctx.save(); ctx.translate(W/2, 160); ctx.scale(sc, sc)
            rrect(ctx, -280, -54, 560, 108, 12); fill_stroke(ctx, "#1e2a46", "#ffd21f", 5)
            art.text(ctx, (("LEVEL UP  3 - 2  PRO ZONE", "#ffd21f"),), "lucky", 36, 0, 2)
            ctx.restore()
            art.title(ctx, "JEET GAYE!", W/2, 300, 92, sc=pop_scale(lt, c["sc"][0] + .1, .35))
            art.confetti(ctx, lt - c["sc"][0], W/2, 300, n=60)
        cheque(ctx, W/2, 500, P("chq", .35))
    elif s == "player":
        art.tag(ctx, "PLAYER 3 · MOST LIKED TAG", W/2, 130, "#7a2fb0", size=26, sc=P("tag"))
        if lt > c["name"][0]:
            art.title(ctx, NEW_PLAYER + "!", W/2, 250, 110, sc=P("name", .35))
            sc = P("jer", .4)
            if sc > .01:
                ctx.save(); ctx.translate(560, 560); ctx.scale(sc, sc); ctx.translate(-560, -560); jersey(ctx, 560, 560, .8, NEW_PLAYER); ctx.restore()
            art.sticker(ctx, "WELCOME TO LEVEL UP!", 300, 420, 44, "#ffd21f", sc=pop_scale(lt, c["jer"][0] + .3), rot=-.06)
    elif s == "gift":
        art.tag(ctx, "SURPRISE GIFT!", W/2, 230, "#ff3fa4", size=34, sc=pop_scale(lt, .1))
        if lt > c["tag"][0]:
            art.tag(ctx, "GIFT BY @" + GIFT_BY, W/2, 300, "#120c22", "#ffd21f", 26, sc=P("tag"), border="#ffd21f")
        if lt > c["ps"][0]:
            art.sticker(ctx, "NO PS5!", W/2, 420, 96, "#ff5a4a", sc=P("ps"), rot=-.07)
    elif s == "bills":
        n = sum(1 for k in ("r0", "r1", "r2") if lt > c[k][0])
        if lt > c["fan"][0]:
            bills_board(ctx, W/2, 120, n, P("fan", .35), total=P("tot", .35) if lt > c["tot"][0] else 0)
        if c["r1"][0] < lt < c["r2"][0]:
            art.sticker(ctx, "INVERTER KA KAMAAL!", W/2, 700, 46, "#ff8a1e", sc=pop_scale(lt, lt_(shot, 3, .6)), rot=.05)
            inverter(ctx, 160, 860, .45, lt, beep=True)
        if lt > c["tot"][0]:
            art.sticker(ctx, "3 DIN MEIN!", W/2, 720, 64, "#ff5a4a", sc=pop_scale(lt, c["tot"][0] + .35), rot=-.06)
    elif s == "fund":
        if lt < c["m"][0]:
            art.tag(ctx, "PINKY DI KA MAGGI STALL", W/2, 160, "#e85a9a", size=28, sc=P("stall"))
            art.tag(ctx, "ROZ KI KAMAAI: ₹1,500", W/2, 230, "#1f4d36", "#ffd21f", 24, sc=pop_scale(lt, c["stall"][0] + .3), border="#ffd21f")
            if lt > c["zero"][0]: art.sticker(ctx, "AAJ: ₹0!", W/2, 380, 80, "#ff5a4a", sc=P("zero"), rot=-.06)
            return
        f = 10000/BILL_TOTAL
        if lt > c["lk"][0]: f = (10000 + 9000*ease((lt - c["lk"][0])/1.0))/BILL_TOTAL
        meter(ctx, W/2, 200, 600, f, sc=P("m"))
        art.tag(ctx, "₹10,000 PRIZE", W/2, 330, "#1f4d36", "#ffd21f", 24, sc=P("m", .4), border="#ffd21f")
        if lt > c["lk"][0]: art.tag(ctx, "+ ₹9,000 TUMHARE LIKES", W/2, 390, "#c7262f", size=24, sc=P("lk"))
        if lt > c["kam"][0]: art.sticker(ctx, "SIRF ₹2,000 KAM!", W/2, 500, 64, "#ff5a4a", sc=P("kam"), rot=-.06)
        if lt > c["days"][0]:
            d = 3
            art.tag(ctx, "%d DIN BAAKI" % d, W/2, 960, "#c7262f", size=40, sc=P("days"))
    elif s == "cta":
        if c["tum"][0] < lt < c["like"][0]:
            art.title(ctx, "SIRF TUM!", W/2, 220, 110, sc=P("tum", .35))
        f = 19000/BILL_TOTAL
        if lt > c["ten"][0]: f = f + (1 - f)*ease((lt - c["ten"][0])/1.2)
        if lt > c["like"][0]:
            meter(ctx, W/2, 140, 600, f, sc=P("like"))
            sc = P("like", .35)
            if sc > .01:
                ctx.save(); ctx.translate(200, 380); ctx.scale(sc, sc); big_heart(ctx, 0, 0, 1.0)
                art.text(ctx, (("= ₹100", "#ffffff"),), "pop", 44, 0, 120, stroke=5, scol="#1b1208"); ctx.restore()
        if lt > c["share"][0]:
            sc = P("share", .35)
            if sc > .01:
                ctx.save(); ctx.translate(520, 380); ctx.scale(sc*1.15, sc*1.15); paper_plane(ctx, 0, -10, 1.0)
                art.text(ctx, (("= ₹200", "#4aff7a"),), "pop", 48, 0, 110, stroke=5, scol="#1b1208"); ctx.restore()
            art.sticker(ctx, "SHARE = DOUBLE!", 520, 560, 40, "#4aff7a", sc=pop_scale(lt, c["share"][0] + .4), rot=.08)
        if c["ten"][0] < lt < c["grp"][0]:
            art.sticker(ctx, "10 SHARE = ₹2,000", W/2, 640, 60, "#4aff7a", sc=P("ten"), rot=-.05)
            if lt > c["safe"][0]: art.sticker(ctx, "CAFE SAFE!", W/2, 780, 80, "#ffd21f", sc=P("safe"), rot=.06)
        if lt > c["grp"][0]:
            chat_group(ctx, W/2, 820, .85*P("grp", .35), lt - c["grp"][0])
            art.sticker(ctx, "SHARE KARO, CAFE BACHAO!", W/2, 990, 48, "#ffd21f", sc=pop_scale(lt, c["grp"][0] + 1.0), rot=-.05)
    elif s == "decide":
        art.title(ctx, "DECISION #3", W/2, 120, 92, sc=P("title", .35))
        art.tag(ctx, "PAISE KAHAN SE LAYEIN?", W/2, 220, "#c7262f", size=28, sc=P("title", .4))
        cur = -1
        for k, key in enumerate(("a", "b", "c")):
            if lt > c[key][0]: cur = k
        for k, (key, L_, t_, col) in enumerate((("a", "A", "LATE NIGHT TOURNAMENT", "#2e9b5a"), ("b", "B", "PINKY DI KA MAGGI STALL", "#c7262f"),
                                                 ("c", "C", "TUMHARA PLAN (COMMENT MEIN)", "#1e2a46"))):
            art.option(ctx, W/2, 320 + k*104, 640, L_, t_, col, k == cur and lt < c["rule"][0], sc=P(key))
        if lt > c["rule"][0]:
            art.tag(ctx, "COMMENT  A / B / C", W/2, 660, "#c7262f", size=30, sc=P("rule"))
            art.tag(ctx, "MOST COMMENTED OPTION WINS", W/2, 730, "#ffd21f", "#1b1208", 22, sc=pop_scale(lt, c["rule"][0] + .25), border="#1b1208")
            art.tag(ctx, "LIKE = ₹100 · SHARE = ₹200", W/2, 800, "#1f4d36", "#ffffff", 24, sc=pop_scale(lt, c["rule"][0] + .45))
    elif s == "end":
        art.title(ctx, "KHULA YA BAND?", W/2, 200, 88, col="#ff5a4a", sc=P("q", .35))
        if lt > c["boss"][0]:
            art.sticker(ctx, "YOU'RE THE BOSS!", W/2, 380, 66, "#ffd21f", sc=P("boss"), rot=-.08)
            art.tag(ctx, "SHARE KARO · CAFE BACHAO", W/2, 480, "#1f4d36", "#ffffff", 28, sc=pop_scale(lt, c["boss"][0] + .3))
