"""Original background score for the Maulidur Rasul 1448H highlights (synthesised, no third-party samples).

Warm, reverent, uplifting: string-like pads, piano arpeggio, sub bass, soft kick only in the
builds. 100 BPM (beat 0.6s); the grid is anchored so bar 1 lands on the title reveal at 4.2s and
every section change in the edit falls on a bar line (see NOTES.md for the cue sheet).

Usage: python3 make_music.py <out.wav>
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

FS = 48000
DUR = 41.4
BEAT = 0.6
BAR = 4 * BEAT
T0 = 4.2  # bar 1 downbeat (title reveal)
N = int(DUR * FS)
rng = np.random.default_rng(1448)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def bar(k):
    return T0 + k * BAR


def env(n, a, r, sustain_to=None):
    """Linear attack, flat, raised-cosine release over the last r seconds."""
    e = np.ones(n)
    na, nr = max(1, int(a * FS)), max(1, int(r * FS))
    e[:na] = np.linspace(0, 1, na)
    nr = min(nr, n)
    e[-nr:] *= 0.5 * (1 + np.cos(np.linspace(0, np.pi, nr)))
    return e


def add(bus, sig, t):
    i = int(round(t * FS))
    if i >= bus.shape[-1]:
        return
    j = min(bus.shape[-1], i + sig.shape[-1])
    bus[..., i:j] += sig[..., : j - i]


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=FS, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=FS, output="sos"), x)


# ---------------------------------------------------------------- harmony
#            start bar, chord name, bass midi, pad voicing
CHORDS = [
    (-1.75, "D", 38, [50, 57, 62, 66]),  # intro drone (from 0.0s)
    (0, "D", 38, [50, 57, 62, 66, 69]),
    (1, "A/C#", 37, [52, 57, 61, 64, 69]),
    (2, "Bm", 35, [50, 54, 59, 62, 66]),
    (3, "Gadd9", 43, [50, 55, 59, 62, 69]),
    (4, "D", 38, [50, 57, 62, 66, 69]),
    (5, "A", 45, [52, 57, 61, 64, 69]),
    (6, "Bm", 35, [50, 54, 59, 62, 66]),
    (7, "Gadd9", 43, [50, 55, 59, 62, 69]),
    (8, "D", 38, [50, 57, 62, 66, 69]),
    (9, "A/C#", 37, [52, 57, 61, 64, 69]),
    (10, "Bm", 35, [50, 54, 59, 62, 66]),
    (11, "Gadd9", 43, [50, 55, 59, 62, 67, 69]),
    (12, "A", 45, [52, 57, 61, 64, 69, 73]),
    (13, "Dadd9", 38, [50, 57, 62, 64, 66, 69, 74]),  # resolves at 35.4s, rings through the end card
]


def chord_span(i):
    s = bar(CHORDS[i][0]) if i else 0.0
    e = bar(CHORDS[i + 1][0]) if i + 1 < len(CHORDS) else DUR
    return s, e


# ---------------------------------------------------------------- instruments
def saw_stack(f, n, detune=(-0.07, 0.0, 0.07)):
    t = np.arange(n) / FS
    out = np.zeros(n)
    for d in detune:
        ph = rng.random()
        out += 2 * ((f * 2 ** (d / 12) * t + ph) % 1.0) - 1
    return out / len(detune)


def piano(m, vel=1.0, length=2.6):
    n = int(length * FS)
    t = np.arange(n) / FS
    f = hz(m)
    out = np.zeros(n)
    for k in range(1, 9):
        fk = f * k * np.sqrt(1 + 0.0004 * k * k)
        if fk > 12000:
            break
        out += (1 / k**1.4) * np.sin(2 * np.pi * fk * t) * np.exp(-t * (1.2 + 0.9 * k))
    out *= env(n, 0.004, 0.3)
    return vel * out


def kick(vel=1.0):
    n = int(0.5 * FS)
    t = np.arange(n) / FS
    f = 45 + 75 * np.exp(-t / 0.03)
    return vel * np.sin(2 * np.pi * np.cumsum(f) / FS) * np.exp(-t / 0.18)


def boom(vel=1.0, length=2.4):
    n = int(length * FS)
    t = np.arange(n) / FS
    f = 34 + 30 * np.exp(-t / 0.25)
    body = np.sin(2 * np.pi * np.cumsum(f) / FS) * np.exp(-t / 0.7)
    noise = lp(rng.standard_normal(n), 700) * np.exp(-t / 0.12) * 0.6
    return vel * (body + noise) * env(n, 0.002, 0.4)


def riser(length):
    n = int(length * FS)
    t = np.arange(n) / FS
    x = rng.standard_normal(n)
    # stack of band-limited noise layers fading in from dark to bright
    prog = (t / length) ** 2
    dark, bright = lp(x, 900), hp(x, 2500)
    tone = np.sin(2 * np.pi * np.cumsum(220 * 2 ** (2 * t / length)) / FS) * 0.15
    return (dark * (1 - prog) * 0.5 + bright * prog + tone) * prog**1.5


def shaker(vel=1.0):
    n = int(0.08 * FS)
    t = np.arange(n) / FS
    return vel * hp(rng.standard_normal(n), 6000) * np.exp(-t / 0.018)


# ---------------------------------------------------------------- arrangement
pad = np.zeros(N)
strings = np.zeros(N)
bass = np.zeros(N)
keys = np.zeros(N)
drums = np.zeros(N)
fx = np.zeros(N)

for i, (_, name, b, voicing) in enumerate(CHORDS):
    s, e = chord_span(i)
    n = int((e - s + 0.6) * FS)  # overlap into the next chord, released smoothly
    for m in voicing:
        add(pad, saw_stack(hz(m), n) * env(n, 0.5, 0.9) * 0.16, s)
    # strings: brighter octave layer only in the builds
    if s >= bar(7) - 0.01:
        lvl = 0.05 if s < bar(11) - 0.01 else 0.10
        for m in voicing[-3:]:
            add(strings, saw_stack(hz(m + 12), n, (-0.1, 0.05, 0.12)) * env(n, 0.8, 1.2) * lvl, s)
    if s > 0:
        bn = int((e - s + 0.35) * FS)  # tail overlaps the next root: no gap at chord changes
        tb = np.arange(bn) / FS
        sub = np.sin(2 * np.pi * hz(b) * tb) + 0.35 * np.sin(4 * np.pi * hz(b) * tb)
        add(bass, sub * env(bn, 0.12, 0.5) * 0.10, s)

# intro: bell-like piano hits on the hook cuts, riser into the title reveal
for t, m in [(0.0, 74), (1.2, 78), (2.4, 81)]:
    add(keys, piano(m, 0.55, 3.0), t)
    add(keys, piano(m - 12, 0.35, 3.0), t)
add(fx, boom(0.6), 0.0)
add(fx, riser(1.2) * 0.22, 3.0)
add(fx, boom(0.75), T0)


def arp(k0, k1, step, vel, pattern=(0, 2, 4, 3, 1, 3, 4, 2)):
    t = bar(k0)
    idx = 0
    while t < bar(k1) - 1e-6:
        ci = max(i for i, c in enumerate(CHORDS) if bar(c[0]) <= t + 1e-6)
        v = sorted(CHORDS[ci][3])
        m = v[pattern[idx % len(pattern)] % len(v)] + 12
        accent = 1.0 if idx % 4 == 0 else 0.78
        add(keys, piano(m, vel * accent), t)
        t += step
        idx += 1


arp(0, 2, BEAT / 2, 0.30)  # title: flowing 8ths
arp(2, 6.5, BEAT, 0.22)  # speech 1: sparse quarters
arp(6.5, 11, BEAT / 2, 0.24)  # speech 2: 8ths return
arp(11, 13, BEAT / 2, 0.34)  # closing lift
add(keys, piano(74, 0.5, 5.0), bar(13))
add(keys, piano(62, 0.4, 5.0), bar(13))
add(keys, piano(81, 0.25, 5.0), bar(13) + 2 * BEAT)

# soft kick on 1 and 3: title, last half of speech 2, closing
for k0, k1, v in [(0, 2, 0.45), (9, 11, 0.35), (11, 13, 0.55)]:
    t = bar(k0)
    while t < bar(k1) - 1e-6:
        add(drums, kick(v), t)
        t += 2 * BEAT
for k in np.arange(bar(11), bar(13), BEAT / 4):
    beat_pos = round((k - T0) / (BEAT / 4)) % 4
    add(drums, shaker(0.05 if beat_pos % 2 else 0.09), k)
add(fx, riser(1.2) * 0.2, bar(11) - 1.2)
add(fx, boom(0.65), bar(11))

# ---------------------------------------------------------------- mix
pad = lp(pad, 2200)
strings = hp(lp(strings, 5200), 250)
# gentle swell automation on the pad (quiet start, breathing through the speech, lift at the close)
autom = np.interp(
    np.arange(N) / FS,
    [0, 4.2, 9.0, 19.8, 30.6, 36.6, 40.0, DUR],
    [0.6, 1.0, 0.85, 0.9, 1.15, 1.0, 0.5, 0.0],
)
dry = pad * autom + strings * autom + hp(bass, 40) + keys * 1.1 + hp(drums, 40) * 0.8 + hp(fx, 40) * 0.7

# stereo: simple width from decorrelated reverb + slight keys pan
nir = int(2.6 * FS)
tir = np.arange(nir) / FS
irL = rng.standard_normal(nir) * np.exp(-6.9 * tir / 2.4)
irR = rng.standard_normal(nir) * np.exp(-6.9 * tir / 2.4)
irL, irR = lp(irL, 6000) / np.sqrt(np.sum(irL**2)), lp(irR, 6000) / np.sqrt(np.sum(irR**2))
wet_src = hp(pad * autom + strings * autom + keys + fx * 0.3, 180)
wetL = fftconvolve(wet_src, irL)[:N]
wetR = fftconvolve(wet_src, irR)[:N]
L = dry + 0.55 * wetL + keys * 0.08
R = dry + 0.55 * wetR - keys * 0.08
st = np.stack([L, R])
# fade the tail to true silence
fade = np.clip((DUR - np.arange(N) / FS) / 2.4, 0, 1) ** 2
st *= fade
st /= np.max(np.abs(st)) / 10 ** (-1.0 / 20)
wavfile.write(sys.argv[1], FS, (st.T * 32767).astype(np.int16))
print("wrote", sys.argv[1], f"{DUR}s")
