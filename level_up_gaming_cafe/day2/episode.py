"""EPISODE: Level Up Gaming Cafe — Day 2   (@tumhoboss)
B (Inverter) won Decision #1. Voiced by the user's ElevenLabs take (Raqib), split per line into build/user_voice/NNN.wav.
Render:  python -m srs.engine path/to/episode.py [--sheet | --frames 3.0,20.5]
"""
import math, os as _os
import numpy as _np, soundfile as _sf
import cairo
from srs import art
from srs import voice as _V
from srs.art import W, H, src, rrect, fill_stroke, ease, eout, bout, pop_scale, SKIN, INK
from srs.engine import lt_, cam, paint_bg

TITLE = "Level Up Gaming Cafe — Day 2"
OUTPUT = "Level_Up_Gaming_Cafe_Day2.mp4"
VOICE = "hm_omega"
END_HOLD = 1.9

# ---------------- real numbers (final count, voting closed 18 Nov 8 PM) ----------------
FOLLOWERS = 161
LIKES = 213
FUND_START = 2000
FUND = FUND_START + LIKES*100            # 23,300
VOTES = {"A": 8, "B": 14, "C": 4}
_FL = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "followers.txt")
FOLLOWER_LIST = [l.strip().lstrip("@") for l in open(_FL, encoding="utf-8") if l.strip()] if _os.path.exists(_FL) else []
VIP_NAMES = ["rmenghare_19", "urfavv.sanford28._", "mohammed335060", "alimurtaza2015.2026", "justt_yachass_15"]
IDEA_BY = "typelovnish"
INVESTOR_BY = "rsz_rehan_sheikh"
BILL = [("INVERTER + BATTERY", 9500), ("3rd PC REPAIR", 4000), ("RGB LIGHTS", 1800),
        ("COFFEE MACHINE 'CHAI'", 3500), ("TOURNAMENT ENTRY", 2000)]
LEFT = FUND - sum(v for _, v in BILL)    # 2,500

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

# ---------------- script: must match the ElevenLabs take line for line ----------------
LINES = [
 ('result', '[excited] Boss! Result आ गया!', 'Boss! Result aa gaya!'),
 ('result', 'Majority ने कहा... [dramatically] B! Inverter!', '*Majority* ne kaha... *B*! *Inverter*!'),
 ('result', '[laughs] PC वाले... इस बार पीछे रह गए!', 'PC wale... is baar *peeche* reh gaye!'),
 ('vip', '[cheerfully] और cafe की family? अब एक सौ इकसठ followers!', 'Aur cafe ki *family*? Ab *161 followers*!'),
 ('vip', 'सबकी VIP seat पक्की! [excited] अपना नाम ढूँढो!', 'Sabki *VIP seat* pakki! Apna *naam* dhundo!'),
 ('fund', '[proudly] तुमने दिए... दो सौ तेरह likes!', 'Tumne diye... *213 likes*!'),
 ('fund', 'हर like सौ रुपये... मतलब इक्कीस हज़ार तीन सौ!', 'Har like ₹100... matlab *₹21,300*!'),
 ('fund', 'दो हज़ार पहले से थे... तो total... [excited] तेईस हज़ार तीन सौ!', '₹2,000 pehle se the... to total... *₹23,300*!'),
 ('fund', 'अब देखो हिसाब...', 'Ab dekho *hisaab*...'),
 ('bill', 'Inverter और battery... नौ हज़ार पाँच सौ!', 'Inverter aur battery... *₹9,500*!'),
 ('bill', 'तीसरा PC ठीक कराया... चार हज़ार!', 'Teesra PC theek karaya... *₹4,000*!'),
 ('bill', 'RGB lights... अठारह सौ!', 'RGB lights... *₹1,800*!'),
 ('bill', 'Coffee machine... साढ़े तीन हज़ार... [laughs] नाम रखा चाय!', 'Coffee machine... *₹3,500*... naam rakha *Chai*!'),
 ('bill', 'Tournament entry... दो हज़ार!', 'Tournament entry... *₹2,000*!'),
 ('bill', 'और बचे? [nervously] सिर्फ़ ढाई हज़ार!', 'Aur bache? Sirf *₹2,500*!'),
 ('inverter', 'पर inverter आया... [sarcastic] जुगाड़ Electronics से!', 'Par inverter aaya... *Jugaad Electronics* se!'),
 ('pcs', 'Light गई तो चलाएगा... सिर्फ़ दो PC और एक पंखा!', 'Light gayi to chalayega... sirf *2 PC* aur ek *pankha*!'),
 ('pcs', '[sighs] और हर दो minute... beep! beep!', 'Aur har 2 minute... *beep! beep!*'),
 ('investor', 'फिर आए investor... सौ करोड़ का offer...', 'Phir aaye investor... *₹100 crore* ka offer...'),
 ('investor', '[chuckles] और बोले... एक चाय उधार मिलेगी?', 'Aur bole... ek *chai udhaar* milegi?'),
 ('prozone', '[serious] तभी... Pro Zone वाले आ गए! Three versus three!', 'Tabhi... *Pro Zone* wale aa gaye! *3 vs 3*!'),
 ('team', 'हमारी team? Lucky... और Chintu.', 'Hamari team? *Lucky*... aur *Chintu*.'),
 ('team', '[nervously] पर तीसरा player? है ही नहीं!', 'Par *teesra player*? Hai hi nahi!'),
 ('team', 'तो आज के लिए... [excited] Pinky दीदी खेलेंगी!', 'To aaj ke liye... *Pinky didi* khelengi!'),
 ('team', '[laughs] Snacks वाली दीदी... आज gamer!', 'Snacks wali didi... aaj *gamer*!'),
 ('match', '[excited] Score... दो-दो! Last round!', 'Score... *2-2*! *Last round*!'),
 ('match', 'और तभी... [dramatically] light गुल!', 'Aur tabhi... *light gul*!'),
 ('blackout', 'Inverter... beep... beep...', 'Inverter... *beep*... *beep*...'),
 ('blackout', 'दो PC चालू... पर Pinky दीदी की screen... [gasps] काली!', '2 PC chaalu... par *Pinky didi* ki screen... *kaali*!'),
 ('decide', '[serious] अब फ़ैसला तुम्हारा, boss!', 'Ab *faisla* tumhara, boss!'),
 ('decide', 'A... पंखा बंद, Pinky दीदी का PC inverter पर!', '*A*... pankha band, Pinky didi ka PC inverter par!'),
 ('decide', 'पर inverter फट भी सकता है!', 'Par inverter *phat* bhi sakta hai!'),
 ('decide', 'B... Lucky अकेला... two versus three!', '*B*... Lucky akela... *2 vs 3*!'),
 ('decide', 'C... बचे ढाई हज़ार से कुछ और? Comment में लिखो!', '*C*... bache ₹2,500 se kuch aur? *Comment* mein likho!'),
 ('decide', 'जिस option पर सबसे ज़्यादा comments... वही जीतेगा!', 'Jis option par sabse zyada *comments*... wahi *jeetega*!'),
 ('decide', '[excited] और सुनो! Team का तीसरा player... तुम चुनोगे!', 'Aur suno! Team ka *teesra player*... *tum* chunoge!'),
 ('decide', 'अपने gamer दोस्त को tag करो!', 'Apne gamer *dost ko tag* karo!'),
 ('decide', 'जिस tag पर सबसे ज़्यादा likes... वो बनेगा Level Up का नया player!', 'Jis tag par sabse zyada *likes*... wo banega Level Up ka *naya player*!'),
 ('decide', 'Boss... [proudly] तुम हो!', 'Boss... *tum* ho!'),
]

SHOTS = [
 ("result", "cut"), ("vip", "whip"), ("fund", "wipe"), ("bill", "whip"), ("inverter", "iris"), ("pcs", "cut"),
 ("investor", "whip"), ("prozone", "wipe"), ("team", "whip"), ("match", "cut"), ("blackout", "cut"), ("decide", "iris"),
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
SPLITS = {2: [(1.01, 1.29)], 8: [(1.23, 1.51), (2.22, 2.47)], 13: [(0.70, 0.88), (2.14, 2.39)]}

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

# ---------------- shots ----------------
def shot_world(ctx, shot, lt, T, m):
    sid = shot["id"]; L = shot["L"]
    z = 1.0 + .05*ease(lt/L)
    if sid == "result":
        paint_bg(ctx, "blur2")
        art.person(ctx, 560, 1330, .95, MANAGER, "cheer" if lt > lt_(shot, 1, .55) else "point", t=lt, mouth=m, flip=True)
    elif sid == "vip":
        ctx.save(); cam(ctx, z, W/2, 760); paint_bg(ctx, "vip"); ctx.restore()
    elif sid == "fund":
        ctx.save(); cam(ctx, z, W/2, 760); paint_bg(ctx, "blur_street")
        art.person(ctx, 200, 1225, 1.3, MANAGER, "hold" if lt < lt_(shot, 2, .6) else "cheer", t=lt, mouth=m); ctx.restore()
    elif sid == "bill":
        paint_bg(ctx, "blur")
        k = None
        for i in range(len(shot["lines"])):
            if lt >= lt_(shot, i, 0): k = i
        ix, iy = W/2, 1000
        # one prop per line, popping in under the receipt
        if k is not None:
            s_ = max(.02, pop_scale(lt, lt_(shot, k, .05), .35))
            ctx.save(); ctx.translate(ix, iy); ctx.scale(s_, s_); ctx.translate(-ix, -iy)
            if k == 0: inverter(ctx, ix+20, iy+90, .7, lt)
            elif k == 1:
                pc_tower(ctx, ix-150, iy+110, .8, lt)
                for j, x in enumerate((ix+20, ix+130, ix+240)):
                    _monitor(ctx, x, iy+10, lt > lt_(shot, 1, .55) or j < 2, kind=0)
            elif k == 2: rgb_strip(ctx, ix, iy, 460, lt)
            elif k == 3: chai_machine(ctx, ix-130, iy+150, .75, lt); draw_pinky(ctx, ix+170, iy+250, .45, "cheer" if lt > lt_(shot, 3, .8) else "hold", lt)
            elif k == 4: ticket(ctx, ix, iy, 1.0)
            elif k == 5: wallet(ctx, ix, iy+10, 1.0, lt)
            ctx.restore()
    elif sid == "inverter":
        ctx.save(); cam(ctx, 1.35 + .05*ease(lt/L), 360, 860); paint_bg(ctx, "cafe3")
        drop = eout((lt-.2)/.45); iy = 700 + 330*drop
        if lt > .2: inverter(ctx, 290, iy, 1.0, lt, beep=lt > lt_(shot, 0, .7))
        art.person(ctx, 540, 1180, .82, CHINTU, "shrug" if lt > lt_(shot, 0, .6) else "idle", t=lt)
        if lt > .2 and lt < .75:
            src(ctx, "#ffffff", .5*(1-(lt-.2)/.55)); ctx.set_line_width(3)
            for k in range(5): ctx.move_to(220+k*40, iy-260); ctx.line_to(220+k*40, iy-330); ctx.stroke()
        ctx.restore()
    elif sid == "pcs":
        ctx.save(); cam(ctx, 1.0 + .06*ease(lt/L), W/2, 600); paint_bg(ctx, "cafe3")
        off = lt > lt_(shot, 0, .45)
        for i, x in enumerate(MON_X):
            if i not in (1, 3) or (i == 2 and off):
                pass
        if off:   # middle PC (on mains only) can't run on the inverter
            src(ctx, "#000", .55); ctx.rectangle(MON_X[2]-60, 430, 120, 80); ctx.fill()
            art.tag(ctx, "X", MON_X[2], 470, "#c7262f", size=26)
        inverter(ctx, 150, 990, .7, lt, beep=lt > lt_(shot, 1, .4))
        table_fan(ctx, 560, 1000, 1.0, lt, spin=True)
        ctx.restore()
    elif sid == "investor":
        ctx.save(); cam(ctx, 1.0 + .05*ease(lt/L), W/2, 900); paint_bg(ctx, "blur")
        art.person(ctx, 360, 1230, 1.15, INVESTOR, "point" if lt < lt_(shot, 1, 0) else "palm", t=lt, mouth=0)
        if lt > lt_(shot, 1, .55): chai_machine(ctx, 620, 1250, .45, lt)
        ctx.restore()
    elif sid == "prozone":
        ctx.save(); cam(ctx, z, W/2, 800); paint_bg(ctx, "street")
        k = eout((lt-.3)/1.2)
        for i, sp in enumerate(PRO):
            x = 900 + i*150 - 520*k - 20*i*k
            art.person(ctx, x - 40*i, 1190 - i*6, .78, sp, "point" if i == 0 and lt > 1.6 else "idle", t=lt+i)
        art.person(ctx, 120, 1230, 1.0, MANAGER, "shrug" if lt > lt_(shot, 0, .5) else "idle", t=lt, mouth=m)
        ctx.restore()
    elif sid == "team":
        # L0: Lucky -> Chintu, L1: empty third chair, L2: Pinky didi walks in, L3: she's a gamer today
        keys = [(0, 215, 1.45), (lt_(shot, 0, .45), 360, 1.45), (lt_(shot, 1, 0), 520, 1.45), (lt_(shot, 3, .3), 360, 1.0)]
        fx, zz = 215, 1.45
        for i, (t0, x_, z_) in enumerate(keys):
            if lt >= t0:
                p_ = ease((lt-t0)/.5)
                fx = fx + (x_-fx)*p_; zz = zz + (z_-zz)*p_
        ctx.save(); cam(ctx, zz, fx, 900); paint_bg(ctx, "vip")
        draw_lucky(ctx, 175, 1160, .58, "cheer" if lt > lt_(shot, 3, .5) else "idle", lt, mouth=0)
        art.person(ctx, 360, 1160, .58, CHINTU, "cheer" if lt > lt_(shot, 3, .5) else "idle", t=lt)
        chappal(ctx, 428, 1160-345, .55, rot=.5 + math.sin(lt*6)*.15)
        t_in = lt_(shot, 2, .25)
        if lt > t_in:
            k = eout((lt - t_in)/.8)
            px = 820 - (820-545)*k
            draw_pinky(ctx, px, 1160, .58, "cheer" if lt > lt_(shot, 3, .2) else "point", lt)
            if lt > lt_(shot, 3, .1): headphones(ctx, px, 1160, .58)
        ctx.restore()
    elif sid == "match":
        dark = lt > lt_(shot, 1, .6)
        ctx.save(); cam(ctx, 1.05 + .08*ease(lt/L), W/2, 640); paint_bg(ctx, "cafe3" if not dark else "cafe_off"); ctx.restore()
        if dark:
            darken(ctx, 1)
    elif sid == "blackout":
        ctx.save(); cam(ctx, 1.1 + .1*ease(lt/L), W/2, 640); paint_bg(ctx, "cafe_off"); ctx.restore()
        darken(ctx, 1)
        on = lt > lt_(shot, 0, .2)
        if on:
            ctx.save(); cam(ctx, 1.1 + .1*ease(lt/L), W/2, 640); glow_monitors(ctx, (1, 3), lt)
            if lt > lt_(shot, 1, .45):
                _monitor(ctx, MON_X[2], 480, False)
            ctx.restore()
        b = int(lt*6) % 2 == 0
        src(ctx, "#ff3a3a", .35 if b else .1); art.ell(ctx, 120, 1060, 90, 90); ctx.fill()
        inverter(ctx, 150, 1110, .55, lt, beep=True)
        if lt > lt_(shot, 1, .5): draw_pinky(ctx, 560, 1240, .55, "shrug", lt)
    elif sid == "decide":
        paint_bg(ctx, "blur2")
        art.person(ctx, 590, 1310, .9, MANAGER, "point", t=lt, mouth=m, flip=True)
        cat(ctx, 160, 1250, .7, lt, awake=lt > lt_(shot, 5, .5))

def cues(shot):
    s = shot["id"]; c = {}
    if s == "result":   c = dict(title=(.1, "hit"), a=(lt_(shot, 1, 0), "pop"), b=(lt_(shot, 1, .2), "pop"), c=(lt_(shot, 1, .35), "pop"),
                                 win=(lt_(shot, 1, .55), "hit"), cnt=(lt_(shot, 1, .7), "ding"), maj=(lt_(shot, 1, .1), "pop"))
    if s == "vip":      c = dict(tag=(.1, "pop"), board=(lt_(shot, 0, .3), "pop"), list=(lt_(shot, 0, .55), "whoosh"),
                                 find=(lt_(shot, 1, .55), "ding"))
    if s == "fund":     c = dict(likes=(lt_(shot, 0, .2), "pop"), x100=(lt_(shot, 1, .1), "pop"), plus=(lt_(shot, 2, .1), "pop"),
                                 total=(lt_(shot, 2, .65), "ding"), his=(lt_(shot, 3, .3), "hit"))
    if s == "bill":     c = dict(r=(.05, "whoosh"), **{"l%d" % i: (lt_(shot, i, .55), "tick") for i in range(5)},
                                 three=(lt_(shot, 1, .8), "ding"), left=(lt_(shot, 5, .55), "hit"))
    if s == "inverter": c = dict(drop=(.62, "boom"), tag=(.7, "pop"), sh=(lt_(shot, 0, .6), "hit"), beep=(lt_(shot, 0, .85), "beep"))
    if s == "pcs":      c = dict(tag=(.2, "pop"), two=(lt_(shot, 0, .55), "pop"), fan=(lt_(shot, 0, .85), "pop"), beep=(lt_(shot, 1, .45), "beep"))
    if s == "investor": c = dict(tag=(.25, "pop"), cr=(lt_(shot, 0, .55), "hit"), ud=(lt_(shot, 1, .55), "hit"))
    if s == "prozone":  c = dict(card=(lt_(shot, 0, .35), "hit"), vs=(lt_(shot, 0, .8), "pop"))
    if s == "team":     c = dict(q=(.05, "pop"), p1=(lt_(shot, 0, .2), "hit"), p2=(lt_(shot, 0, .6), "hit"), q3=(lt_(shot, 1, .2), "pop"),
                                 none=(lt_(shot, 1, .6), "hit"), guest=(lt_(shot, 2, .55), "ding"), gamer=(lt_(shot, 3, .5), "hit"))
    if s == "match":    c = dict(score=(.1, "pop"), last=(lt_(shot, 0, .6), "riser"), cut=(lt_(shot, 1, .6), "powerdown"))
    if s == "blackout": c = dict(beep=(lt_(shot, 0, .2), "beep"), two=(lt_(shot, 1, .1), "pop"), black=(lt_(shot, 1, .8), "boom"))
    if s == "decide":   c = dict(title=(lt_(shot, 0, .05), "hit"), a=(lt_(shot, 1), "pop"), risk=(lt_(shot, 2, .1), "pop"), b=(lt_(shot, 3), "pop"),
                                 c=(lt_(shot, 4), "pop"), cm=(lt_(shot, 5, .1), "pop"), p3=(lt_(shot, 6, .1), "whoosh"), tag=(lt_(shot, 7, .05), "pop"),
                                 feat=(lt_(shot, 8, .6), "ding"), boss=(lt_(shot, 9, .5), "crowd"))
    for k, (t_, sfx) in list(c.items()):
        if sfx not in (None, "pop", "hit", "ding", "whoosh", "crowd", "riser"):
            c[k] = (t_, {"beep": "pop", "tick": "pop", "boom": "hit", "powerdown": "hit"}.get(sfx, "pop"))
    return c

def _count(lt, t0, dur, a, b):
    return int(a + (b-a)*ease((lt-t0)/dur)) if lt > t0 else a

def shot_ui(ctx, shot, lt, T):
    s = shot["id"]; c = cues(shot); P = lambda k, d=.28: pop_scale(lt, c[k][0], d)
    if s == "result":
        art.tag(ctx, "DAY 2", W/2, 50, "#7a2fb0", size=26, sc=P("title"))
        art.title(ctx, "RESULT!", W/2, 140, 100, sc=P("title", .35))
        mx = max(VOTES.values())
        for k, (key, L_, t_, col) in enumerate((("a", "A", "BUY NEW PCS", "#2e9b5a"), ("b", "B", "GET AN INVERTER", "#c7262f"),
                                                 ("c", "C", "SOMETHING ELSE", "#1e2a46"))):
            sc = P(key)
            if sc <= .01: continue
            y = 280 + k*120; win = L_ == "B" and lt > c["win"][0]
            art.option(ctx, W/2, y, 640, L_, t_, col, win, sc=sc)
            f = ease((lt-c["cnt"][0])/1.0) * VOTES[L_]/mx
            ctx.save(); ctx.translate(W/2, y); ctx.scale(sc, sc)
            rrect(ctx, -228, 50, 456, 16, 6); fill_stroke(ctx, "#2a2238", None)
            rrect(ctx, -228, 50, 456*f, 16, 6); fill_stroke(ctx, col if not win else "#ffd21f", None)
            ctx.restore()
        art.confetti(ctx, lt-c["win"][0], 560, 360, n=40)
        art.sticker(ctx, "WINNER!", 555, 418, 64, "#ffd21f", sc=P("win"), rot=.12)
        art.sticker(ctx, "MAJORITY KA FAISLA!", W/2, 680, 58, "#ff8a1e", sc=P("maj"), rot=-.05)
    elif s == "vip":
        art.tag(ctx, "VIP SEATS", 170, 110, "#7a2fb0", size=30, sc=P("tag"))
        art.board(ctx, 500, 120, "FOLLOWERS", "{:,}".format(_count(lt, c["board"][0]+.1, 1.6, 36, FOLLOWERS)), 260, sc=P("board"), vsize=46)
        names = FOLLOWER_LIST or VIP_NAMES
        sc = P("list", .4)
        if sc > .01:
            top, hgt = 210, 780
            ctx.save(); ctx.translate(W/2, top + hgt/2); ctx.scale(sc, sc); ctx.translate(-W/2, -(top + hgt/2))
            rrect(ctx, 50, top, 620, hgt, 26); fill_stroke(ctx, "#120c22", "#ffd21f", 5)
            art.text(ctx, (("VIP LIST · %d BOSS" % len(names), "#ffd21f"),), "lucky", 32, W/2, top+44)
            ctx.save(); rrect(ctx, 56, top+78, 608, hgt-90, 20); ctx.clip()
            row = 42; rows = (len(names)+1)//2
            span = max(0, rows*row - (hgt-120))
            dur = max(1.0, shot["L"] - c["list"][0] - .5)
            off = span * min(1, max(0, (lt - c["list"][0] - .3) / dur))
            for i, nm in enumerate(names):
                r_, col = i // 2, i % 2
                y = top + 108 + r_*row - off
                if y < top+50 or y > top+hgt+30: continue
                if r_ % 2 == 0 and col == 0:
                    src(ctx, "#ffffff", .05); ctx.rectangle(56, y-row/2, 608, row); ctx.fill()
                x0 = 70 + col*300
                art.star(ctx, x0+12, y, 8)
                nm_ = "@" + nm
                fs = 20 if len(nm_) <= 20 else max(14, int(20*20/len(nm_)))
                art.text(ctx, ((nm_, "#ffffff"),), "popx", fs, x0+28, y, anchor="lm")
            ctx.restore()
            g = cairo.LinearGradient(0, top+78, 0, top+150); g.add_color_stop_rgba(0, .07, .05, .13, 1); g.add_color_stop_rgba(1, .07, .05, .13, 0)
            ctx.set_source(g); ctx.rectangle(56, top+78, 608, 72); ctx.fill()
            g = cairo.LinearGradient(0, top+hgt-80, 0, top+hgt-12); g.add_color_stop_rgba(0, .07, .05, .13, 0); g.add_color_stop_rgba(1, .07, .05, .13, 1)
            ctx.set_source(g); ctx.rectangle(56, top+hgt-80, 608, 70); ctx.fill()
            ctx.restore()
        art.sticker(ctx, "APNA NAAM DHUNDO!", W/2, 1040, 60, "#ffd21f", sc=P("find"), rot=-.05)
    elif s == "fund":
        lk = _count(lt, c["likes"][0]+.1, 1.0, 0, LIKES)
        art.board(ctx, 450, 200, "TUMHARE LIKES", "{:,} ❤".format(lk).replace(" ❤", ""), 380, sc=P("likes"), vsize=62)
        if lt > c["x100"][0]:
            art.tag(ctx, "× ₹100 HAR LIKE", 450, 330, "#c7262f", size=28, sc=P("x100"))
            v = _count(lt, c["x100"][0]+.4, 1.0, 0, LIKES*100)
            art.tag(ctx, "= ₹{:,}".format(v), 450, 405, "#1f4d36", "#ffd21f", size=40, sc=P("x100", .35), border="#ffd21f")
        if lt > c["plus"][0]:
            art.tag(ctx, "+ ₹2,000 PEHLE SE", 450, 495, "#2f6db0", size=28, sc=P("plus"))
        if lt > c["total"][0]:
            art.board(ctx, 450, 640, "TOTAL FUND", "₹{:,}".format(FUND), 400, sc=P("total", .35), vsize=66)
            art.sticker(ctx, "PAISA HI PAISA!", 470, 790, 50, "#7fe0b0", sc=pop_scale(lt, c["total"][0]+.3), rot=-.08)
        art.sticker(ctx, "AB HISAAB!", 470, 900, 56, "#ffd21f", sc=P("his"), rot=.07)
        for k in range(4):
            f = (lt - .3 - k*.3)/1.0
            if 0 < f < 1: art.heart(ctx, 640 - 120*f, 760 - 520*f + math.sin(f*6+k)*30, 1.3)
    elif s == "bill":
        n = sum(1 for i in range(5) if lt > c["l%d" % i][0])
        rem = FUND - sum(v for _, v in BILL[:n])
        hi = n-1 if n and lt < lt_(shot, min(n, 5), 0) + .01 else -1
        receipt(ctx, W/2, 60, n, rem, sc=P("r", .35), hi=n-1, stamp=P("left", .35))
        if lt > c["three"][0] and lt < lt_(shot, 2, 0):
            art.sticker(ctx, "3 PCs CHALU!", W/2, 820, 50, "#4aff7a", sc=P("three"), rot=-.05)
        if lt > lt_(shot, 3, .7) and lt < lt_(shot, 4, 0):
            art.sticker(ctx, "NAAM: CHAI!", W/2, 820, 56, "#ffd21f", sc=pop_scale(lt, lt_(shot, 3, .7)), rot=-.05)
            art.tag(ctx, "IDEA BY @" + IDEA_BY, W/2, 885, "#ffd21f", "#1b1208", 20, sc=pop_scale(lt, lt_(shot, 3, .75)), border="#1b1208")
    elif s == "inverter":
        art.tag(ctx, "INVERTER ARRIVED!", W/2, 120, "#2e9b5a", size=30, sc=P("tag"))
        art.sticker(ctx, "SECOND HAND!", W/2, 260, 76, "#ff8a1e", sc=P("sh"), rot=-.08)
        art.tag(ctx, "FROM: JUGAAD ELECTRONICS", W/2, 370, "#1e2a46", size=22, sc=P("sh", .35))
        if lt > c["beep"][0] and int(lt*4) % 2 == 0: art.sticker(ctx, "BEEP!", 170, 560, 54, "#ff5a4a", sc=1, rot=.15)
    elif s == "pcs":
        art.tag(ctx, "LIGHT GAYI TO...", W/2, 140, "#1e2a46", size=26, sc=P("tag"))
        art.tag(ctx, "INVERTER: 2 PCs", 220, 240, "#c7262f", size=26, sc=P("two"))
        art.tag(ctx, "+ 1 PANKHA", 520, 240, "#2f6db0", size=26, sc=P("fan"))
        if lt > c["beep"][0] and int(lt*4) % 2 == 0: art.sticker(ctx, "BEEP BEEP!", 200, 780, 54, "#ff5a4a", sc=1, rot=-.12)
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
    elif s == "team":
        art.title(ctx, "HAMARI TEAM", W/2, 120, 80, sc=P("q", .35))
        if c["p1"][0] < lt < c["p2"][0]:
            art.tag(ctx, "PLAYER 1 · LUCKY", W/2, 230, "#c7262f", size=30, sc=P("p1"))
        if c["p2"][0] < lt < c["q3"][0]:
            art.tag(ctx, "PLAYER 2 · CHINTU", W/2, 230, "#2f6db0", size=30, sc=P("p2"))
        if c["q3"][0] < lt < c["guest"][0]:
            art.tag(ctx, "PLAYER 3 · ???", W/2, 230, "#1e2a46", size=30, sc=P("q3"))
            if lt > c["none"][0]: art.sticker(ctx, "HAI HI NAHI!", W/2, 340, 70, "#ff5a4a", sc=P("none"), rot=-.06)
        if lt > c["guest"][0]:
            art.tag(ctx, "PLAYER 3 · PINKY DIDI", W/2, 230, "#e85a9a", size=30, sc=P("guest"))
            art.sticker(ctx, "SIRF AAJ KE LIYE!", W/2, 330, 50, "#7fe0b0", sc=pop_scale(lt, c["guest"][0]+.2), rot=-.05)
        if lt > c["gamer"][0]:
            art.sticker(ctx, "SNACKS → GAMER!", W/2, 420, 54, "#ffd21f", sc=P("gamer"), rot=.05)
    elif s == "match":
        sc = P("score")
        if sc > .01:
            ctx.save(); ctx.translate(W/2, 150); ctx.scale(sc, sc)
            rrect(ctx, -270, -50, 540, 100, 12); fill_stroke(ctx, "#1e2a46", "#ffffff", 4)
            art.text(ctx, (("LEVEL UP  2 - 2  PRO ZONE", "#ffffff"),), "lucky", 34, 0, 2)
            ctx.restore()
        if c["last"][0] < lt < c["cut"][0]: art.sticker(ctx, "LAST ROUND!", W/2, 300, 76, "#ff8a1e", sc=P("last"), rot=-.05)
        if lt > c["cut"][0]: art.sticker(ctx, "LIGHT GUL!", W/2, 470, 100, "#ffffff", sc=P("cut"), rot=-.06)
    elif s == "blackout":
        if int(lt*6) % 2 == 0: art.sticker(ctx, "BEEP...", 210, 900, 56, "#ff5a4a", sc=1, rot=.1)
        art.tag(ctx, "INVERTER: 2 PCs ON", W/2, 140, "#2e9b5a", size=28, sc=P("two"))
        if lt > c["black"][0]:
            art.sticker(ctx, "PINKY DI KI SCREEN KAALI!", W/2, 300, 50, "#ff5a4a", sc=P("black"), rot=-.05)
            art.tag(ctx, "LEVEL UP: 2 PLAYERS ONLY", W/2, 640, "#c7262f", size=26, sc=pop_scale(lt, c["black"][0]+.3))
    elif s == "decide":
        art.title(ctx, "DECISION #2", W/2, 120, 92, sc=P("title", .35))
        art.tag(ctx, "LAST ROUND KAISE KHELEIN?", W/2, 220, "#c7262f", size=26, sc=P("title", .4))
        cur = 0
        for k, key in enumerate(("a", "b", "c")):
            if lt > c[key][0]: cur = k
        allon = lt > c["boss"][0]
        for k, (key, L_, t_, col) in enumerate((("a", "A", "FAN OFF, PINKY DI KA PC ON", "#2e9b5a"), ("b", "B", "LUCKY SOLO: 2 vs 3", "#c7262f"),
                                                 ("c", "C", "BACHE 2,500 SE KUCH AUR", "#1e2a46"))):
            act = (k == cur and lt < c["cm"][0]) or (allon and int(lt*5) % 3 == k)
            art.option(ctx, W/2, 320+k*104, 640, L_, t_, col, act, sc=P(key))
        if c["risk"][0] < lt < c["b"][0]: art.sticker(ctx, "RISK: INVERTER PHAT SAKTA HAI!", W/2, 650, 40, "#ff5a4a", sc=P("risk"), rot=-.04)
        if c["cm"][0] < lt < c["p3"][0]:
            art.tag(ctx, "COMMENT  A / B / C", 260, 660, "#c7262f", size=26, sc=P("cm"))
            art.tag(ctx, "MOST COMMENTED OPTION WINS", 300, 730, "#ffd21f", "#1b1208", 22, sc=pop_scale(lt, c["cm"][0]+.25), border="#1b1208")
        if c["p3"][0] < lt < lt_(shot, 9, 0) + .3:
            sc = P("p3", .35)
            if sc > .01:
                ctx.save(); ctx.translate(W/2, 880); ctx.scale(sc, sc)
                src(ctx, "#000", .35); rrect(ctx, -296, -116, 600, 236, 18); ctx.fill()
                rrect(ctx, -300, -120, 600, 236, 18); fill_stroke(ctx, "#120c22", "#ffd21f", 5)
                art.text(ctx, (("PLAYER 3 = TUMHARA DOST!", "#ffd21f"),), "lucky", 38, 0, -78)
                if lt > c["tag"][0]:
                    rrect(ctx, -260, -36, 520, 54, 27); fill_stroke(ctx, "#2a2238", "#ffffff", 2)
                    art.text(ctx, (("@tumhara_dost", "#7fb6ff"), ("  team mein aa ja!", "#ffffff")), "popx", 22, -10, -9)
                    art.heart(ctx, 232, -9, .8)
                    art.text(ctx, (("TAG KARO · SABSE ZYADA LIKES", "#7fe0b0"),), "popx", 20, 0, 50)
                    art.text(ctx, (("= LEVEL UP KA NAYA PLAYER", "#7fe0b0"),), "popx", 20, 0, 82)
                ctx.restore()
            if lt > c["feat"][0]: art.sticker(ctx, "NAYA PLAYER!", 540, 740, 46, "#ff3fa4", sc=P("feat"), rot=.1)
        art.sticker(ctx, "YOU'RE THE BOSS!", 330, 850, 60, "#ffd21f", sc=P("boss"), rot=-.1)
        art.confetti(ctx, lt-c["boss"][0], W/2, 600)
