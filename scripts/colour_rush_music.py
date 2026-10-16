"""Procedural 130 BPM EDM bed for the Colour Rush tee ad, arranged to the video's hits:
build 0-4.05, drop at 4.05 (tee lands), break at 10.51, drop at 11.43 (tee turns to the
back), build + stop, final hit at 16.2 (end card). Writes the track and beats.json (beat
times + downbeat indices) that the composition uses for its beat pulse.
usage: colour_rush_music.py out.wav beats.json"""
import json
import sys

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
DUR = 20.0
N = int(SR * DUR)
B = 60 / 130
rng = np.random.default_rng(130)
drums = np.zeros(N)
music = np.zeros(N)  # sidechained + reverb send


def bp(sig, lo, hi):
    return sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), sig)


def lp(sig, f):
    return sosfilt(butter(2, f, "lowpass", fs=SR, output="sos"), sig)


def hp(sig, f):
    return sosfilt(butter(2, f, "highpass", fs=SR, output="sos"), sig)


def put(buf, sig, t, g=1.0):
    i = int(t * SR)
    if i >= N:
        return
    n = min(len(sig), N - i)
    buf[i:i + n] += sig[:n] * g


def env(n, dec):
    return np.exp(-np.arange(n) / SR * dec)


def mtof(m):
    return 440 * 2 ** ((m - 69) / 12)


# ---------- instruments ----------
def kick():
    n = int(0.42 * SR)
    t = np.arange(n) / SR
    f = 46 + 120 * np.exp(-t * 30)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    s[:120] += rng.standard_normal(120) * np.linspace(0.6, 0, 120)
    return np.tanh(s * 1.6)


def clap():
    n = int(0.28 * SR)
    s = np.zeros(n)
    for d in (0, 0.011, 0.022):
        i = int(d * SR)
        s[i:] += rng.standard_normal(n - i) * env(n - i, 32 if d < 0.02 else 14)
    return bp(s, 900, 4200) * 0.9


def hat(open_=False):
    n = int((0.16 if open_ else 0.05) * SR)
    return hp(rng.standard_normal(n), 7000) * env(n, 18 if open_ else 70) * 0.5


def snare():
    n = int(0.16 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)
    return (bp(rng.standard_normal(n), 1200, 7000) * env(n, 24) + body * 0.6) * 0.8


def saw(f, n, detune=0.0):
    t = np.arange(n) / SR
    ph = (f * (1 + detune) * t + rng.random()) % 1.0
    return 2 * ph - 1


def supersaw(notes, n):
    s = np.zeros(n)
    for m in notes:
        for d in (-0.012, -0.007, -0.003, 0, 0.003, 0.007, 0.012):
            s += saw(mtof(m), n, d)
    return s / (len(notes) * 7) * 3


def impact():
    n = int(2.2 * SR)
    t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(30 + 60 * np.exp(-t * 5)) / SR) * np.exp(-t * 1.8)
    crash = lp(rng.standard_normal(n), 6000) * np.exp(-t * 2.6) * 0.35
    return np.tanh(sub * 1.4) + crash


def riser(dur):
    n = int(dur * SR)
    x = np.arange(n) / n
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    blk = 2048
    for i in range(0, n, blk):
        f = 400 + 9000 * x[i] ** 2
        out[i:i + blk] = bp(noise[i:i + blk], f * 0.7, min(f * 1.3, 20000))
    f = 110 * 2 ** (x * 3)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    return (out * 0.6 + tone) * x ** 1.6


# chord loop: Am F C G (one bar each)
CHORDS = [[57, 60, 64, 69], [53, 57, 60, 65], [55, 60, 64, 67], [55, 59, 62, 67]]
ROOTS = [33, 29, 36, 31]
ARP = [0, 2, 1, 3, 2, 1, 3, 2]

K, C, HC, HO, SN, IMP = kick(), clap(), hat(), hat(True), snare(), impact()
kicks = []


def groove(t0, beats, bar0=0, lead=True):
    for k in range(beats):
        t = t0 + k * B
        bar = (bar0 + k // 4) % 4
        put(drums, K, t, 0.95)
        kicks.append(t)
        if k % 2 == 1:
            put(drums, C, t, 0.55)
        put(drums, HO, t + B / 2, 0.35)
        for q in range(4):
            put(drums, HC, t + q * B / 4, 0.18 if q % 2 else 0.12)
        nb = int(B / 2 * SR)  # offbeat bass
        bass = lp(saw(mtof(ROOTS[bar]), nb) + 0.5 * saw(mtof(ROOTS[bar] + 12), nb), 520) * env(nb, 6)
        put(music, bass, t + B / 2, 0.55)
        if k % 4 == 0:
            n = int(4 * B * SR)
            put(music, lp(supersaw(CHORDS[bar], n), 3200), t, 0.55)
        if lead:
            for q in range(4):
                n = int(B / 4 * SR)
                note = CHORDS[bar][ARP[(k * 4 + q) % 8]] + 12
                pl = lp(saw(mtof(note), n) + saw(mtof(note), n, 0.004), 4200) * env(n, 22)
                put(music, pl, t + q * B / 4, 0.22)


def build(t0, beats, bar0=0, cutoff=(500, 2600)):
    total = beats * B
    for k in range(0, beats, 4):  # filtered chords opening up
        bar = (bar0 + k // 4) % 4
        n = int(min(4, beats - k) * B * SR)
        f = cutoff[0] + (cutoff[1] - cutoff[0]) * k / max(1, beats)
        put(music, lp(supersaw(CHORDS[bar], n), f), t0 + k * B, 0.45)
    t = t0  # snare roll: quarters -> eighths -> sixteenths -> 32nds, swelling
    while t < t0 + total - 1e-6:
        x = (t - t0) / total
        step = B if x < 0.25 else B / 2 if x < 0.5 else B / 4 if x < 0.8 else B / 8
        put(drums, SN, t, 0.15 + 0.55 * x)
        t += step
    put(music, riser(total), t0, 0.7)


# ---------- arrangement ----------
INTRO = 4.05 - 8 * B
put(music, riser(INTRO + 0.05), 0, 0.35)
build(INTRO, 8, cutoff=(350, 2400))
put(drums, IMP, 1.62, 0.55)  # title slam
put(drums, IMP, 4.05, 1.0)  # tee lands: drop 1
groove(4.05, 14)
build(4.05 + 14 * B, 2, bar0=3, cutoff=(800, 2800))
put(drums, IMP, 11.43, 0.9)  # turn to the back: drop 2
groove(11.43, 8)
build(11.43 + 8 * B, 2, bar0=2, cutoff=(800, 3000))
put(drums, IMP, 16.2, 1.1)  # end-card hit
groove(16.2, 8)

# ---------- mix ----------
side = np.ones(N)
for t in kicks:
    i = int(t * SR)
    n = min(int(B * SR), N - i)
    side[i:i + n] = np.minimum(side[i:i + n], 1 - 0.7 * np.exp(-np.arange(n) / SR * 11))
music *= side
ir_n = int(1.3 * SR)
ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 4.5)
wet = fftconvolve(music, ir)[:N] * 0.012
mono = drums + music
L = mono + wet + np.roll(wet, 331)
R = mono + wet - np.roll(wet, 517) * 0.5
gap = slice(int(16.06 * SR), int(16.19 * SR))  # hard stop before the end-card hit
L[gap] *= 0.05
R[gap] *= 0.05
fade = np.ones(N)
fs = int(18.6 * SR)
fade[fs:] = np.linspace(1, 0, N - fs) ** 1.5
st = np.stack([L * fade, R * fade], axis=1)
st = st / np.percentile(np.abs(st), 99.9)  # gentle bus clip, not a wall of distortion
st = np.tanh(st * 1.2) / np.tanh(1.2) * 0.89
sf.write(sys.argv[1], st.astype(np.float32), SR)

beats, down = [], []
for t0, n in [(INTRO, 8), (4.05, 14), (11.43, 8), (16.2, 8)]:
    for k in range(n):
        if k % 4 == 0:
            down.append(len(beats))
        beats.append(round(t0 + k * B, 3))
json.dump({"beats": beats, "downbeats": down, "bpm": 130}, open(sys.argv[2], "w"))
print("ok", len(beats), "beats")
