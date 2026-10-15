"""Original "Islamic corporate" background score for the Salam Jumaat motion poster (synthesised).

Warm, hopeful and calm: D major, 96 BPM, I-V-vi-IV (D A Bm G). Piano, soft high strings,
oud/qanun-style plucks (Karplus-Strong) playing major-pentatonic figures with light ornaments,
gentle daf + shaker, a little sub bass. No low drones, no choir. Cue sheet (matches build/compose.py):
  0-3     hook: piano + bell over a soft swell, qanun run into the arch reveal (1.0), chime on the title
  3-8     pluck arpeggio + strings
  8-18    ayat: piano chords and strings only, soft and still
  18-34.6 message: full warm groove (daf, pluck, piano melody, bass)
  34.6-42 resolution on D, ring-out
Usage: python3 make_music.py <out.wav>
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, lfilter, sosfilt

FS = 48000
DUR = 42.0
N = int(DUR * FS)
BEAT = 60 / 96
BAR = 4 * BEAT
rng = np.random.default_rng(1311)

# D major chords, 2 bars each from t=3.0 (piano voicing, bass root)
PROG = [([62, 66, 69, 74], 38), ([61, 64, 69, 73], 45), ([59, 62, 66, 71], 47), ([59, 62, 67, 71], 43)]
PENTA = [62, 64, 66, 69, 71, 74, 76, 78, 81]  # D major pentatonic


def chord_at(t):
    if t < 3.0 or t >= 34.6:
        return PROG[0]
    return PROG[int((t - 3.0) // (2 * BAR)) % 4]


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


def piano(m, vel=1.0, length=2.6):
    n = int(length * FS)
    t = np.arange(n) / FS
    f = hz(m)
    out = sum((1 / k ** 1.3) * np.sin(2 * np.pi * f * k * np.sqrt(1 + 0.0004 * k * k) * t) * np.exp(-t * (0.9 + 0.8 * k))
              for k in range(1, 9) if f * k < 14000)
    return vel * out * env(n, 0.003, 0.3)


def pluck(m, length=1.4, bright=0.5, damp=0.995):
    n = int(length * FS)
    L = int(round(FS / hz(m)))
    x = np.zeros(n)
    x[:L] = lp(rng.standard_normal(L), 1500 + 6000 * bright)
    a = np.zeros(L + 2)
    a[0], a[L], a[L + 1] = 1.0, -damp / 2, -damp / 2
    y = lfilter([1.0], a, x)
    return y / (np.max(np.abs(y)) + 1e-9) * env(n, 0.002, 0.15)


def strings(m, n):
    t = np.arange(n) / FS
    vib = 1 + 0.003 * np.sin(2 * np.pi * 5.0 * t)
    x = sum(2 * ((np.cumsum(hz(m) * 2 ** (d / 12) * vib) / FS + rng.random()) % 1.0) - 1 for d in (-0.07, 0.0, 0.07)) / 3
    return lp(x, 3200)


def bell(m, vel=1.0, length=3.5):
    n = int(length * FS)
    t = np.arange(n) / FS
    return vel * sum(a * np.sin(2 * np.pi * hz(m) * r * t) * np.exp(-t * d) for r, a, d in [(1, 1, 1.0), (2.0, 0.35, 1.8), (3.0, 0.15, 3.0)]) * env(n, 0.002, 0.5)


def dum(vel=1.0):
    n = int(0.45 * FS)
    t = np.arange(n) / FS
    f = 70 + 40 * np.exp(-t / 0.025)
    return vel * np.sin(2 * np.pi * np.cumsum(f) / FS) * np.exp(-t / 0.16)


def tak(vel=1.0):
    n = int(0.3 * FS)
    t = np.arange(n) / FS
    return vel * (bp(rng.standard_normal(n), 1800, 6000) * np.exp(-t / 0.018) + hp(rng.standard_normal(n), 7000) * np.exp(-t / 0.1) * 0.4)


def shaker(vel=1.0):
    n = int(0.07 * FS)
    t = np.arange(n) / FS
    return vel * hp(rng.standard_normal(n), 6500) * np.exp(-t / 0.02)


def swell(length, vel=1.0):
    n = int(length * FS)
    t = np.arange(n) / FS
    return vel * hp(rng.standard_normal(n), 3000) * (t / length) ** 2.5


bus = {k: np.zeros(N) for k in ("piano", "str", "pluck", "bass", "perc", "fx")}
tt = np.arange(N) / FS

# hook
for t, m in [(0.0, 74), (0.0, 62), (0.6, 78), (1.2, 81)]:
    add(bus["piano"], piano(m, 0.45, 3.0), t)
add(bus["fx"], swell(1.0, 0.12), 0.0)
for i, m in enumerate([62, 64, 66, 69, 71, 74, 76, 78, 81, 83, 86]):
    add(bus["pluck"], pluck(m, 1.4, 0.8, 0.996), 0.5 + i * 0.045, 0.3)
add(bus["fx"], bell(86, 0.3), 2.6)
add(bus["fx"], bell(81, 0.2), 2.62)

# strings: whole bars throughout from 1.0, swelling in the message section
k = 0
t = 1.0
while t < DUR - 0.5:
    nxt = 3.0 if t < 3.0 else t + 2 * BAR
    nxt = min(nxt, DUR)
    tones, _ = chord_at(t + 0.01)
    n = int((nxt - t + 0.6) * FS)
    for m in tones:
        add(bus["str"], strings(m + 12, n) * env(n, 0.6, 0.8), t, 0.11)
    t = nxt
bus["str"] *= np.interp(tt, [0, 3, 8, 18, 34.6, 39, 42], [0.4, 1.0, 1.0, 1.0, 1.1, 0.8, 0.0])

# piano chords on each 2-bar chord change (3-34.6), ring at the end
t = 3.0
while t < 34.6 - 1e-6:
    tones, _ = chord_at(t)
    for j, m in enumerate(tones):
        add(bus["piano"], piano(m, 0.28, 4.5), t + j * 0.03)
    t += 2 * BAR
for j, m in enumerate([50, 62, 66, 69, 74, 78]):
    add(bus["piano"], piano(m, 0.3, 6.0), 34.6 + j * 0.04)
add(bus["fx"], bell(86, 0.25, 6.0), 34.6)

# pluck arpeggio 3-8 and 18-34.6 (16ths in the message, 8ths in the intro)
for a, b, step, v in [(3.0, 8.0, BEAT / 2, 0.32), (18.0, 34.6, BEAT / 4, 0.16)]:
    t, i = a, 0
    while t < b - 1e-6:
        tones, _ = chord_at(t)
        arp = sorted(tones) + [tones[0] + 12]
        m = arp[[0, 2, 1, 3, 4, 3, 1, 2][i % 8]] + 12
        add(bus["pluck"], pluck(m, 0.9, 0.75, 0.993), t, v * (1.25 if i % 4 == 0 else 1))
        t += step
        i += 1

# piano melody in the message section (major pentatonic, singable)
MEL = [(18.6, 74, 1), (19.2, 76, 1), (19.85, 78, 2), (21.1, 76, 1), (21.7, 74, 1), (22.3, 71, 2),
       (23.6, 69, 1), (24.2, 71, 1), (24.85, 74, 2), (26.1, 76, 1), (26.7, 78, 1), (27.3, 81, 2.5),
       (28.6, 78, 1), (29.2, 76, 1), (29.85, 74, 2), (31.1, 71, 1), (31.7, 74, 1), (32.3, 76, 1), (32.9, 74, 3)]
for t, m, b in MEL:
    add(bus["piano"], piano(m, 0.32, 2.0 + b * 0.4), t)
    add(bus["piano"], piano(m + 12, 0.08, 1.5), t)

# bass (18-34.6): root on beats 1 and 3
t = 18.0
while t < 34.6 - 1e-6:
    _, root = chord_at(t)
    n = int(BEAT * 1.6 * FS)
    tb = np.arange(n) / FS
    add(bus["bass"], (np.sin(2 * np.pi * hz(root) * tb) + 0.25 * np.sin(4 * np.pi * hz(root) * tb)) * env(n, 0.01, 0.3), t, 0.16)
    t += 2 * BEAT

# light daf groove + shaker from 20.0: D . T . D D T .
pat = ["D", None, "T", None, "D", "D", "T", None]
t, i = 20.0, 0
while t < 34.6 - 1e-6:
    h = pat[i % 8]
    if h == "D":
        add(bus["perc"], dum(0.35), t)
    elif h == "T":
        add(bus["perc"], tak(0.13), t)
    add(bus["perc"], shaker(0.035 if i % 2 else 0.06), t)
    t += BEAT / 2
    i += 1
add(bus["perc"], dum(0.4), 34.6)

# ------------------------------------------------------------------ mix
dry = bus["piano"] * 0.9 + bus["str"] + hp(bus["pluck"], 150) * 0.85 + hp(bus["bass"], 40) + hp(bus["perc"], 50) * 0.8 + bus["fx"] * 0.7
nir = int(2.6 * FS)
tir = np.arange(nir) / FS
irs = []
for _ in range(2):
    ir = lp(rng.standard_normal(nir) * np.exp(-6.9 * tir / 2.2), 8000)
    irs.append(ir / np.sqrt(np.sum(ir ** 2)))
wet = hp(bus["piano"] + bus["str"] * 0.7 + bus["pluck"] * 0.6 + bus["fx"] + bus["perc"] * 0.2, 250)
L = dry + 0.4 * fftconvolve(wet, irs[0])[:N] + 0.12 * bus["pluck"]
R = dry + 0.4 * fftconvolve(wet, irs[1])[:N] - 0.12 * bus["pluck"]
st = np.stack([L, R]) * np.clip((DUR - tt) / 3.0, 0, 1) ** 1.5
st /= np.max(np.abs(st))
st = np.tanh(1.2 * st) / np.tanh(1.2) * 10 ** (-1 / 20)
wavfile.write(sys.argv[1], FS, (st.T * 32767).astype(np.int16))
print("wrote", sys.argv[1], f"{DUR}s")
