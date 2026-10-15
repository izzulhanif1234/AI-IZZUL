"""Original Islamic-style background score for the Salam Jumaat motion poster (synthesised, no samples).

Maqam Hijaz on D (D Eb F# G A Bb C D). Instruments modelled in code: ney (breathy flute with vibrato),
oud and qanun (Karplus-Strong plucked strings), daf (frame drum, dum/tak + jingles), drone and a soft
"aah" choir pad. Cue sheet (matches build/compose.py):
  0-3.2  hook: drone swell, shimmer, qanun glissando into the arch reveal (1.0), chime on the title
  3.2-8  ney phrase over the drone
  8-18   ayat: drone + choir pad only, music held low and still out of respect for the verse
  18-34.6 message: oud ostinato + soft daf (maqsum) + ney phrases
  34.6-42 closing: qanun glissando, final D, ring-out
Usage: python3 make_music.py <out.wav>
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, lfilter, sosfilt

FS = 48000
DUR = 42.0
N = int(DUR * FS)
EIGHTH = 1 / 3  # 90 BPM
rng = np.random.default_rng(1311)
HIJAZ = [62, 63, 66, 67, 69, 70, 72, 74]  # D4 Eb F# G A Bb C D5


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lp(x, f, o=2):
    return sosfilt(butter(o, f, "low", fs=FS, output="sos"), x)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, "high", fs=FS, output="sos"), x)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], "band", fs=FS, output="sos"), x)


def env(n, a, r):
    e = np.ones(n)
    na, nr = max(1, int(a * FS)), min(n, max(1, int(r * FS)))
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= 0.5 * (1 + np.cos(np.linspace(0, np.pi, nr)))
    return e


def add(bus, sig, t, g=1.0):
    i = int(round(t * FS))
    if i >= N:
        return
    j = min(N, i + len(sig))
    bus[i:j] += g * sig[: j - i]


def pluck(m, length=1.6, bright=0.5, damp=0.996):
    """Karplus-Strong string: noise burst through a tuned, damped comb (oud / qanun)."""
    n = int(length * FS)
    L = int(round(FS / hz(m)))
    x = np.zeros(n)
    burst = rng.standard_normal(L)
    x[:L] = lp(burst, 1500 + 6000 * bright)
    a = np.zeros(L + 2)
    a[0], a[L], a[L + 1] = 1.0, -damp / 2, -damp / 2
    y = lfilter([1.0], a, x)
    return y / (np.max(np.abs(y)) + 1e-9) * env(n, 0.002, 0.15)


def ney(m, length, vel=1.0, bend=0.0):
    n = int(length * FS)
    t = np.arange(n) / FS
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.2 * t) * np.clip(t / 0.6, 0, 1)
    f = hz(m) * vib * (1 + bend * np.exp(-t / 0.15))
    ph = 2 * np.pi * np.cumsum(f) / FS
    tone = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    breath = bp(rng.standard_normal(n), hz(m) * 0.8, hz(m) * 4) * 0.35
    return vel * (tone + breath) * env(n, 0.18, 0.35)


def dum(vel=1.0):
    n = int(0.5 * FS)
    t = np.arange(n) / FS
    f = 62 + 35 * np.exp(-t / 0.03)
    return vel * (np.sin(2 * np.pi * np.cumsum(f) / FS) * np.exp(-t / 0.22) + lp(rng.standard_normal(n), 300) * np.exp(-t / 0.05) * 0.4)


def tak(vel=1.0):
    n = int(0.35 * FS)
    t = np.arange(n) / FS
    slap = bp(rng.standard_normal(n), 1800, 6000) * np.exp(-t / 0.02)
    jingle = hp(rng.standard_normal(n), 7000) * np.exp(-t / 0.12) * 0.45
    return vel * (slap + jingle)


def saw_pad(m, n, voices=(-0.08, 0.0, 0.08)):
    t = np.arange(n) / FS
    return sum(2 * ((hz(m) * 2 ** (d / 12) * t + rng.random()) % 1.0) - 1 for d in voices) / len(voices)


def choir(m, n):
    """Soft 'aah': saw stack through two vowel formants."""
    x = saw_pad(m, n, (-0.1, -0.03, 0.04, 0.11))
    return bp(x, 600, 1100) * 0.8 + bp(x, 1000, 1500) * 0.5


def shimmer(length):
    n = int(length * FS)
    t = np.arange(n) / FS
    x = hp(rng.standard_normal(n), 6000) * (t / length) ** 2
    return x


def boom(vel=1.0, length=3.0):
    n = int(length * FS)
    t = np.arange(n) / FS
    f = 40 + 25 * np.exp(-t / 0.2)
    return vel * np.sin(2 * np.pi * np.cumsum(f) / FS) * np.exp(-t / 1.0) * env(n, 0.002, 0.8)


def chime(m, vel=1.0, length=4.0):
    n = int(length * FS)
    t = np.arange(n) / FS
    out = sum(a * np.sin(2 * np.pi * hz(m) * r * t) * np.exp(-t * d) for r, a, d in [(1, 1, 0.8), (2.76, 0.4, 1.6), (5.4, 0.2, 3.0)])
    return vel * out * env(n, 0.003, 0.5)


bus = {k: np.zeros(N) for k in ("drone", "pad", "ney", "oud", "qanun", "daf", "fx")}

# drone: D2 + A2 + D3, swelling in, dipping a touch during the verse
for m, g in [(38, 0.5), (45, 0.3), (50, 0.25)]:
    bus["drone"][:] += g * lp(saw_pad(m, N, (-0.05, 0.05)), 900)
tt = np.arange(N) / FS
bus["drone"] *= np.interp(tt, [0, 2.5, 8, 18, 34.6, 39, 42], [0.0, 0.9, 0.75, 0.9, 1.0, 0.7, 0.0])

# choir pad: D minor-ish colour of Hijaz (D F# A), (G Bb D) in the verse
for t0, t1, notes in [(1.0, 8.2, [62, 66, 69]), (8.0, 13.2, [62, 66, 69]), (13.0, 18.2, [67, 70, 74]),
                      (18.0, 34.8, [62, 66, 69]), (34.6, 42.0, [62, 66, 69, 74])]:
    n = int((t1 - t0) * FS)
    for m in notes:
        add(bus["pad"], choir(m, n) * env(n, 1.2, 1.5), t0, 0.22)

# hook FX
add(bus["fx"], shimmer(1.0) * 0.25, 0.0)
add(bus["fx"], boom(0.7), 1.0)
for i, m in enumerate([62, 63, 66, 67, 69, 70, 72, 74, 75, 78, 79, 81]):  # qanun glissando up the maqam
    add(bus["qanun"], pluck(m, 1.6, 0.8, 0.997), 0.45 + i * 0.045, 0.35)
add(bus["fx"], chime(86, 0.35), 2.6)
add(bus["fx"], chime(81, 0.25), 2.62)

# ney phrases (start, [(midi, beats)], vel)
PHRASES = [
    (3.3, [(69, 1.5), (70, 0.5), (69, 1), (67, 1), (66, 2), (67, 1), (69, 3)], 0.32),
    (18.6, [(62, 1), (63, 1), (66, 2), (67, 1), (69, 3)], 0.26),
    (24.0, [(72, 1), (70, 1), (69, 2), (67, 1), (66, 1), (67, 2)], 0.26),
    (30.6, [(69, 1), (70, 1), (72, 1.5), (70, 0.5), (69, 3)], 0.28),
    (35.4, [(74, 2), (72, 1), (70, 1), (69, 2), (66, 1), (63, 1), (62, 5)], 0.3),
]
BEAT = 2 * EIGHTH
for t0, notes, v in PHRASES:
    t = t0
    for m, b in notes:
        L = b * BEAT
        add(bus["ney"], ney(m, L + 0.25, v, bend=-0.015), t)
        t += L

# oud ostinato (18-32): Hijaz figure on D, 8ths
OST = [62, 69, 66, 69, 63, 69, 66, 62]
t = 18.0
k = 0
while t < 34.6 - 1e-6:
    m = OST[k % 8] - (12 if k % 8 == 0 else 0)
    add(bus["oud"], pluck(m, 1.2, 0.35, 0.994), t, 0.32 if k % 4 == 0 else 0.22)
    t += EIGHTH
    k += 1

# daf, maqsum (D T . T D . T .) from 20.0, soft
pat = ["D", "T", None, "T", "D", None, "T", None]
t = 20.0
k = 0
while t < 34.6 - 1e-6:
    h = pat[k % 8]
    if h == "D":
        add(bus["daf"], dum(0.45), t)
    elif h == "T":
        add(bus["daf"], tak(0.16), t)
    t += EIGHTH
    k += 1
add(bus["daf"], dum(0.55), 34.6)

# closing glissando + final chime
for i, m in enumerate([74, 72, 70, 69, 67, 66, 63, 62]):
    add(bus["qanun"], pluck(m, 2.0, 0.7, 0.997), 34.0 + i * 0.07, 0.3)
add(bus["fx"], boom(0.5), 34.6)
add(bus["fx"], chime(86, 0.3, 6.0), 34.6)
add(bus["fx"], chime(86, 0.28, 5.0), 36.6)
for m in (50, 57, 62, 66, 69):
    add(bus["oud"], pluck(m, 4.0, 0.4, 0.998), 34.6, 0.22)

# ------------------------------------------------------------------ mix
dry = (bus["drone"] * 0.16 + bus["pad"] * 0.55 + bus["ney"] * 0.9 + hp(bus["oud"], 70) * 0.8
       + bus["qanun"] * 0.6 + hp(bus["daf"], 45) * 0.75 + hp(bus["fx"], 30) * 0.6)
nir = int(3.2 * FS)
tir = np.arange(nir) / FS
irs = []
for _ in range(2):
    ir = lp(rng.standard_normal(nir) * np.exp(-6.9 * tir / 2.8), 6500)
    irs.append(ir / np.sqrt(np.sum(ir**2)))
wet = hp(bus["pad"] * 0.5 + bus["ney"] + bus["oud"] * 0.7 + bus["qanun"] + bus["fx"] * 0.5 + bus["daf"] * 0.3, 200)
L = dry + 0.55 * fftconvolve(wet, irs[0])[:N] + 0.1 * bus["oud"]
R = dry + 0.55 * fftconvolve(wet, irs[1])[:N] - 0.1 * bus["oud"]
st = np.stack([L, R]) * np.clip((DUR - tt) / 3.0, 0, 1) ** 1.5
st /= np.max(np.abs(st))
st = np.tanh(1.3 * st) / np.tanh(1.3) * 10 ** (-1 / 20)
wavfile.write(sys.argv[1], FS, (st.T * 32767).astype(np.int16))
print("wrote", sys.argv[1], f"{DUR}s")
