"""Audio, all generated locally: Kokoro TTS voice, synthesized music bed and SFX, ducked mix."""
import os, hashlib, subprocess, json
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
TTS_DIR = os.environ.get("KOKORO_DIR", "/root/.claude/plugins/synced/c29a5480-5996-4792-9093-519cf806c241_5b58f0bf-591b-47f7-8d17-aaa1fddc18a2/code-reels-studio/assets/tts")
MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"

# ---------------- TTS ----------------
_kokoro = None
def _get_kokoro():
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        m = os.path.join(TTS_DIR, "kokoro-v1.0.int8.onnx")
        v = os.path.join(TTS_DIR, "voices-v1.0.bin")
        if not (os.path.exists(m) and os.path.exists(v)):
            raise SystemExit(f"Voice model missing. Run setup.py (downloads {MODEL_URL}).")
        _kokoro = Kokoro(m, v)
    return _kokoro

def _resample(x, sr_in):
    if sr_in == SR: return x
    from scipy.signal import resample_poly
    from math import gcd
    g = gcd(SR, sr_in)
    return resample_poly(x, SR // g, sr_in // g).astype(np.float32)

def trim(x, thr=0.012, pad=0.03):
    idx = np.where(np.abs(x) > thr)[0]
    if len(idx) == 0: return x
    a = max(0, idx[0] - int(pad * SR)); b = min(len(x), idx[-1] + int(pad * 2 * SR))
    return x[a:b]

def tts(text, voice="hm_omega", speed=1.0, lang="hi", cache_dir="cache"):
    os.makedirs(cache_dir, exist_ok=True)
    key = hashlib.md5(f"{text}|{voice}|{speed}|{lang}".encode()).hexdigest()[:16]
    path = os.path.join(cache_dir, f"tts_{key}.wav")
    if os.path.exists(path):
        x, _ = sf.read(path, dtype="float32"); return x
    k = _get_kokoro()
    samples, sr = k.create(text, voice=voice, speed=speed, lang=lang)
    x = trim(_resample(np.asarray(samples, dtype=np.float32), sr))
    x = x / (np.max(np.abs(x)) + 1e-6) * 0.89
    sf.write(path, x, SR)
    return x

# ---------------- DSP helpers ----------------
def _lp(x, f):
    return sosfilt(butter(2, f / (SR / 2), "low", output="sos"), x)
def _hp(x, f):
    return sosfilt(butter(2, f / (SR / 2), "high", output="sos"), x)
def _bp(x, lo, hi):
    return sosfilt(butter(2, [lo / (SR / 2), hi / (SR / 2)], "band", output="sos"), x)
def _t(d): return np.arange(int(d * SR)) / SR
def _env(n, a, r):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
def _noise(d, seed=0): return np.random.default_rng(seed).standard_normal(int(d * SR))
def _sweep(f0, f1, d, curve="exp"):
    t = _t(d)
    f = f0 * (f1 / f0) ** (t / d) if curve == "exp" else f0 + (f1 - f0) * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR)

# ---------------- SFX ----------------
def sfx(name):
    n = name
    if n == "boom":
        d = 2.2; x = _sweep(90, 32, d) * _env(int(d * SR), 0.005, 0.6) * 1.0
        x += _lp(_noise(d, 1), 300) * _env(int(d * SR), 0.002, 0.25) * 0.8
        return x
    if n == "hit":
        d = 1.2; x = _sweep(120, 40, d) * _env(int(d * SR), 0.002, 0.25)
        x += _bp(_noise(d, 2), 200, 3000) * _env(int(d * SR), 0.001, 0.06) * 0.5
        return x
    if n == "whoosh":
        d = 0.7; t = _t(d); e = np.sin(np.pi * t / d) ** 2
        return _bp(_noise(d, 3), 400, 4000) * e * 0.9
    if n == "pop":
        d = 0.18; return (_sweep(900, 300, d) * _env(int(d * SR), 0.001, 0.04) + _hp(_noise(d, 4), 3000) * _env(int(d * SR), 0.0005, 0.01) * 0.4)
    if n == "tick":
        d = 0.05; return _hp(_noise(d, 5), 2500) * _env(int(d * SR), 0.0003, 0.006) * 0.8
    if n == "beep":
        d = 0.5; t = _t(d); x = np.sin(2 * np.pi * 1046 * t) * ((t % 0.25) < 0.11) * 0.45
        return x * np.exp(-t * 2)
    if n == "ding":
        d = 0.9; t = _t(d)
        return (np.sin(2 * np.pi * 1320 * t) + 0.6 * np.sin(2 * np.pi * 1760 * t)) * _env(len(t), 0.002, 0.25) * 0.35
    if n == "powerdown":
        d = 1.8; t = _t(d)
        x = _sweep(240, 30, d) * np.exp(-t * 1.2) * 0.6
        x += np.sin(2 * np.pi * 50 * t) * np.exp(-t * 2.5) * 0.4 + np.sin(2 * np.pi * 100 * t) * np.exp(-t * 3) * 0.2
        x[:int(0.02 * SR)] += _noise(0.02, 6) * 0.6
        return x
    if n == "heartbeat":
        d = 0.9; x = np.zeros(int(d * SR))
        for st in (0.0, 0.28):
            th = _sweep(70, 40, 0.25) * _env(int(0.25 * SR), 0.004, 0.06)
            i = int(st * SR); x[i:i + len(th)] += th * (1 if st == 0 else 0.7)
        return x
    if n == "riser":
        d = 2.0; t = _t(d)
        x = _bp(_noise(d, 7), 800, 6000) * (t / d) ** 2 * 0.6 + _sweep(200, 1200, d) * (t / d) ** 2 * 0.25
        return x
    if n == "water":
        d = 2.0; t = _t(d)
        x = _bp(_noise(d, 8), 300, 2500) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t) ** 2) * 0.5
        return x * np.minimum(1, t * 4) * np.minimum(1, (d - t) * 4)
    if n == "crowd":
        d = 3.0; t = _t(d); x = np.zeros(len(t))
        for k in range(6):
            x += _bp(_noise(d, 20 + k), 250 + k * 60, 900 + k * 80) * (0.5 + 0.5 * np.sin(2 * np.pi * (2 + k * 0.7) * t + k))
        return x * 0.18 * np.minimum(1, t * 2) * np.minimum(1, (d - t) * 2)
    if n == "thunder":
        d = 3.5; t = _t(d)
        return _lp(_noise(d, 9), 180) * _env(len(t), 0.05, 1.0) * 1.4
    if n == "sting":
        d = 2.5; t = _t(d)
        fr = [110, 116.5, 164.8, 233]
        x = sum(np.sin(2 * np.pi * f * t) for f in fr) * _env(len(t), 0.005, 0.9) * 0.25
        h = sfx("hit"); x[:len(h)] += h
        return x
    if n == "radio":
        d = 1.2; t = _t(d)
        return _bp(_noise(d, 10), 1500, 4500) * 0.25 * (0.6 + 0.4 * np.sin(2 * np.pi * 13 * t))
    if n == "footsteps":
        d = 2.0; x = np.zeros(int(d * SR))
        for i in range(6):
            s = _lp(_noise(0.08, 30 + i), 900) * _env(int(0.08 * SR), 0.001, 0.02)
            j = int(i * 0.33 * SR); x[j:j + len(s)] += s * 0.8
        return x
    return np.zeros(int(0.1 * SR))

# ---------------- music bed ----------------
MOODS = {
    "tense":   dict(root=55.0, chord=[1, 1.5, 2, 2.378], bpm=76, tick=True),
    "dread":   dict(root=49.0, chord=[1, 1.189, 1.5, 2], bpm=60, tick=False),
    "urgent":  dict(root=55.0, chord=[1, 1.5, 2, 2.67], bpm=96, tick=True),
    "hopeful": dict(root=65.4, chord=[1, 1.26, 1.5, 2], bpm=70, tick=False),
}

def music(duration, intensity_fn, mood="tense", seed=1):
    m = MOODS.get(mood, MOODS["tense"])
    n = int(duration * SR); t = np.arange(n) / SR
    inten = np.array([intensity_fn(x) for x in np.arange(0, duration, 0.05)])
    inten = np.interp(t, np.arange(len(inten)) * 0.05, inten)
    # pad drone
    pad = np.zeros(n)
    for i, r in enumerate(m["chord"]):
        f = m["root"] * r
        pad += np.sin(2 * np.pi * f * t + i) * (0.5 + 0.5 * np.sin(2 * np.pi * (0.07 + 0.03 * i) * t + i))
        pad += 0.3 * np.sin(2 * np.pi * f * 2.003 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t + i * 2))
    pad = _lp(pad, 900) * 0.16
    air = _bp(_noise(duration, seed), 300, 1800) * 0.03 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * t))
    # pulse
    beat = 60 / m["bpm"]
    pulse = np.zeros(n)
    kick = _sweep(85, 38, 0.35) * _env(int(0.35 * SR), 0.003, 0.09)
    tick = _hp(_noise(0.04, 3), 3000) * _env(int(0.04 * SR), 0.0003, 0.005)
    bt = 0.0
    while bt < duration:
        i = int(bt * SR)
        lvl = inten[min(i, n - 1)]
        if lvl > 0.25:
            seg = kick[: max(0, min(len(kick), n - i))]
            pulse[i:i + len(seg)] += seg * 0.55 * lvl
        if m["tick"] and lvl > 0.15:
            for half in (0, beat / 2):
                j = int((bt + half) * SR)
                if j < n - len(tick):
                    pulse[j:j + len(tick)] += tick * 0.10 * lvl
        bt += beat
    # high tension string (rises with intensity)
    hi = np.sin(2 * np.pi * m["root"] * 8 * t) * 0.025 + np.sin(2 * np.pi * m["root"] * 8.47 * t) * 0.02
    out = (pad + air) * (0.45 + 0.55 * inten) + pulse + hi * np.clip(inten - 0.5, 0, 1) * 2
    return out.astype(np.float32)

# ---------------- mix ----------------
def place(buf, clip, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf) or i < 0: return
    seg = clip[: len(buf) - i]
    buf[i:i + len(seg)] += seg * gain

def mix_down(duration, voice_events, sfx_events, intensity_fn, mood, out_wav, music_gain=0.55, music_path=None):
    n = int(duration * SR) + SR
    vo = np.zeros(n, np.float32)
    for (at, clip) in voice_events:
        place(vo, clip, at)
    fx = np.zeros(n, np.float32)
    for (at, name, g) in sfx_events:
        place(fx, sfx(name).astype(np.float32), at, g)
    if music_path:
        mu, msr = sf.read(music_path, dtype="float32")
        if mu.ndim > 1: mu = mu.mean(axis=1)
        mu = _resample(mu, msr)
        mu = np.tile(mu, int(np.ceil(n / len(mu))))[:n] * 0.6
    else:
        mu = np.zeros(n, np.float32); mu[: int(duration * SR)] = music(duration, intensity_fn, mood)
    # sidechain duck: music dips under voice
    env = np.abs(vo)
    env = _lp(env, 6)
    env = env / (env.max() + 1e-6)
    duck = 1 - 0.55 * np.clip(env * 3, 0, 1)
    # fade out tail
    tail = np.ones(n); fo = int(1.2 * SR); end = int(duration * SR)
    tail[end - fo:end] = np.linspace(1, 0, fo); tail[end:] = 0
    mixv = vo * 1.0 + mu * music_gain * duck * tail + fx * 0.7
    mixv = mixv / (np.max(np.abs(mixv)) + 1e-6) * 0.95
    raw = out_wav.replace(".wav", "_raw.wav")
    sf.write(raw, mixv[:end], SR)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", "loudnorm=I=-14:TP=-1.0:LRA=9",
                    "-ar", str(SR), out_wav], check=True)
    return out_wav
