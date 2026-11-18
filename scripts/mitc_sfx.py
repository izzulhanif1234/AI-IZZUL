"""Synthesise the MITC promo sound design (48 kHz stereo WAV) into hf/assets/sfx2/.
Deterministic (fixed seeds). usage: python3 scripts/mitc_sfx.py OUTDIR"""
import sys, wave
import numpy as np
from scipy import signal

SR = 48000
OUT = sys.argv[1]
rng = np.random.default_rng(7)


def save(name, x):
    x = np.atleast_2d(x)
    if x.shape[0] == 1:
        x = np.vstack([x, x])
    x = x / (np.abs(x).max() + 1e-9) * 0.89
    pcm = (x.T * 32767).astype(np.int16)
    with wave.open(f"{OUT}/{name}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(name, round(x.shape[1] / SR, 3), "s")


def t_(d):
    return np.arange(int(d * SR)) / SR


def noise(d):
    return rng.standard_normal(int(d * SR))


def bp_sweep(x, f0, f1, q=1.2, steps=64):
    """band-pass with a centre frequency gliding f0 -> f1 (log), processed in blocks"""
    out = np.zeros_like(x); n = len(x); hop = n // steps
    zi = None
    for i in range(steps):
        fc = f0 * (f1 / f0) ** (i / (steps - 1))
        lo, hi = fc / (1 + 1 / q), min(fc * (1 + 1 / q), SR / 2 * 0.95)
        b, a = signal.butter(2, [lo, hi], btype="band", fs=SR)
        seg = x[i * hop:(i + 1) * hop if i < steps - 1 else n]
        if zi is None or len(zi) != max(len(a), len(b)) - 1:
            zi = signal.lfilter_zi(b, a) * 0
        y, zi = signal.lfilter(b, a, seg, zi=zi)
        out[i * hop:i * hop + len(y)] = y
    return out


def reverb(x, d=1.6, mix=0.35, seed=3):
    r = np.random.default_rng(seed)
    ir_t = t_(d)
    irL = r.standard_normal(len(ir_t)) * np.exp(-ir_t * 6 / d)
    irR = r.standard_normal(len(ir_t)) * np.exp(-ir_t * 6 / d)
    b, a = signal.butter(1, 5000, fs=SR)
    irL, irR = signal.lfilter(b, a, irL), signal.lfilter(b, a, irR)
    n = len(x) + len(ir_t)
    wL = np.pad(signal.fftconvolve(x, irL), (0, 1))[:n]
    wR = np.pad(signal.fftconvolve(x, irR), (0, 1))[:n]
    dry = np.pad(x, (0, len(ir_t)))
    s = np.abs(dry).max() / (np.abs(wL).max() + 1e-9)
    return np.vstack([dry + mix * wL * s, dry + mix * wR * s])


def pan(x, p0, p1):
    p = np.linspace(p0, p1, len(x)) * np.pi / 4 + np.pi / 4
    return np.vstack([x * np.cos(p), x * np.sin(p)])


# 1. cinematic boom: pitch-dropping sub + noise crack + long tail
d = 3.2; t = t_(d)
f = 38 + 70 * np.exp(-t * 9)
sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.4)
crack = signal.lfilter(*signal.butter(2, [200, 4000], btype="band", fs=SR), noise(d)) * np.exp(-t * 28)
body = signal.lfilter(*signal.butter(2, 180, fs=SR), noise(d)) * np.exp(-t * 4) * 0.8
boom = sub * 1.0 + crack * 0.55 + body
save("boom", reverb(boom, 2.2, 0.3))

# 2. reverse-cymbal swell, 1.2 s (2 beats), ends abruptly at its end
d = 1.2; t = t_(d)
cym = signal.lfilter(*signal.butter(2, 3500, btype="high", fs=SR), noise(d))
cym = cym * (t / d) ** 3.2
cym[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
save("swell", np.vstack([cym, cym * 0.95]))

# 3. big whoosh (0.9 s) peaking at 0.62 s, panning L->R
d = 0.9; t = t_(d); pk = 0.62
env = np.where(t < pk, (t / pk) ** 2.5, np.exp(-(t - pk) * 9))
w = bp_sweep(noise(d), 300, 2600, q=1.4) * env
w += signal.lfilter(*signal.butter(2, 220, fs=SR), noise(d)) * env * 0.6
save("whoosh-big", pan(w, -0.8, 0.8))

# 4. swish (0.36 s) peaking at 0.24 s, airy, R->L
d = 0.36; t = t_(d); pk = 0.24
env = np.where(t < pk, (t / pk) ** 2, np.exp(-(t - pk) * 22))
s = bp_sweep(noise(d), 1500, 7000, q=1.8) * env
save("swish", pan(s, 0.7, -0.7))

# 5. text hit: tight kick + click + short air (for the hook lines)
d = 0.5; t = t_(d)
f = 55 + 160 * np.exp(-t * 40)
kick = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
click = signal.lfilter(*signal.butter(2, 2500, btype="high", fs=SR), noise(d)) * np.exp(-t * 120) * 0.6
save("text-hit", reverb(kick + click, 0.5, 0.12))

# 6. UI blips (C6, E6, G6, C7): bell-ish sine with a soft 2nd harmonic
for name, fr in [("blip-1", 1046.5), ("blip-2", 1318.5), ("blip-3", 1568.0), ("blip-4", 2093.0)]:
    d = 0.45; t = t_(d)
    b = (np.sin(2 * np.pi * fr * t) + 0.3 * np.sin(2 * np.pi * fr * 2.01 * t) + 0.12 * np.sin(2 * np.pi * fr * 3 * t)) * np.exp(-t * 14)
    b[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    save(name, reverb(b, 0.7, 0.25))

# 7. shimmer: rising cluster of bell partials (badges / logo)
d = 1.6; t = t_(d); sh = np.zeros_like(t)
for i, fr in enumerate([1568, 2093, 2637, 3136, 4186, 5274]):
    st = i * 0.06; m = t >= st; tt = t[m] - st
    sh[m] += np.sin(2 * np.pi * fr * tt) * np.exp(-tt * 5) * (0.9 ** i)
save("shimmer", reverb(sh, 1.4, 0.4))

# 8. thud (pin landing)
d = 0.6; t = t_(d)
f = 45 + 90 * np.exp(-t * 25)
th = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) + signal.lfilter(*signal.butter(2, 600, fs=SR), noise(d)) * np.exp(-t * 40) * 0.5
save("thud", th)
