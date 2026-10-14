"""Original score for the Bengkel Transisi MS ISO 37001 highlights (synthesised, no third-party audio).

Modern cinematic-corporate: 120 BPM (beat 0.5s, bar 2s), E major, I-V-vi-IV. Bar 1 is the drop at
3.0s; every section change in the edit lands on a bar line (cue sheet in NOTES.md):
  0-3 hook (beat stabs on each cut, filter-swept kick, riser) | 3 drop / title | 11 day one |
  23 briefing (full groove) | 37 montage (peak) | 47 finale | 55 end card (ring-out to 60)
Usage: python3 make_music.py <out.wav>
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

FS = 48000
DUR = 60.0
BEAT = 0.5
BAR = 2.0
T0 = 3.0
N = int(DUR * FS)
rng = np.random.default_rng(37001)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def bar(k):
    return T0 + k * BAR


def add(bus, sig, t, gain=1.0):
    i = int(round(t * FS))
    if i >= bus.shape[-1] or i + sig.shape[-1] <= 0:
        return
    if i < 0:
        sig, i = sig[-i:], 0
    j = min(bus.shape[-1], i + sig.shape[-1])
    bus[i:j] += gain * sig[: j - i]


def lp(x, f, o=2):
    return sosfilt(butter(o, f, "low", fs=FS, output="sos"), x)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, "high", fs=FS, output="sos"), x)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], "band", fs=FS, output="sos"), x)


def adsr(n, a, r):
    e = np.ones(n)
    na, nr = max(1, int(a * FS)), min(n, max(1, int(r * FS)))
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= 0.5 * (1 + np.cos(np.linspace(0, np.pi, nr)))
    return e


# ------------------------------------------------------------------ harmony (E major)
#  bar range -> (chord tones for pads, bass root)
PROG = [  # I - V/D# - vi - IV
    ([52, 56, 59, 64, 68], 40),  # E
    ([51, 54, 59, 63, 66], 39),  # B/D#
    ([49, 56, 61, 64, 68], 37),  # C#m
    ([45, 52, 57, 61, 64], 33),  # A
]


def chord_at(t):
    if t < T0:
        return PROG[0]
    k = int((t - T0) // BAR)
    if t >= 55.0:  # ring-out on the tonic
        return ([52, 56, 59, 63, 64, 68, 71], 40)
    return PROG[k % 4]


# ------------------------------------------------------------------ instruments
def pluck(m, vel=1.0, length=0.9, bright=1.0):
    n = int(length * FS)
    t = np.arange(n) / FS
    f = hz(m)
    out = np.zeros(n)
    for k in range(1, 14):
        if f * k > 14000:
            break
        out += (1 / k) * np.sin(2 * np.pi * f * k * t + k) * np.exp(-t * (6 + 9 * k / bright))
    return vel * out * adsr(n, 0.002, 0.08)


def piano(m, vel=1.0, length=2.4):
    n = int(length * FS)
    t = np.arange(n) / FS
    f = hz(m)
    out = np.zeros(n)
    for k in range(1, 10):
        fk = f * k * np.sqrt(1 + 0.0004 * k * k)
        if fk > 14000:
            break
        out += (1 / k**1.35) * np.sin(2 * np.pi * fk * t) * np.exp(-t * (1.0 + 0.85 * k))
    return vel * out * adsr(n, 0.003, 0.25)


def saw(f, n, detune=(-0.08, 0.0, 0.08)):
    t = np.arange(n) / FS
    return sum(2 * ((f * 2 ** (d / 12) * t + rng.random()) % 1.0) - 1 for d in detune) / len(detune)


def stab(m, vel=1.0, length=0.32):
    n = int(length * FS)
    t = np.arange(n) / FS
    x = saw(hz(m), n, (-0.12, 0.0, 0.1))
    dark, bright = lp(x, 900), lp(x, 6000)
    e = np.exp(-t / 0.06)
    return vel * (bright * e + dark * (1 - e)) * adsr(n, 0.004, 0.12)


def kick(vel=1.0, punch=1.0):
    n = int(0.45 * FS)
    t = np.arange(n) / FS
    f = 56 + 110 * np.exp(-t / 0.028)
    body = np.sin(2 * np.pi * np.cumsum(f) / FS) * np.exp(-t / 0.17)
    click = hp(rng.standard_normal(n), 3000) * np.exp(-t / 0.004) * 0.25 * punch
    return vel * np.tanh(1.6 * (body + click))


def clap(vel=1.0):
    n = int(0.35 * FS)
    t = np.arange(n) / FS
    x = bp(rng.standard_normal(n), 900, 5000)
    e = np.zeros(n)
    for d in (0.0, 0.011, 0.022):
        e += (t >= d) * np.exp(-np.clip(t - d, 0, None) / (0.009 if d < 0.02 else 0.11))
    return vel * x * e * 0.8


def hat(vel=1.0, open_=False):
    n = int((0.25 if open_ else 0.06) * FS)
    t = np.arange(n) / FS
    return vel * hp(rng.standard_normal(n), 7500) * np.exp(-t / (0.08 if open_ else 0.014))


def snare(vel=1.0):
    n = int(0.22 * FS)
    t = np.arange(n) / FS
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05)
    nz = bp(rng.standard_normal(n), 1500, 9000) * np.exp(-t / 0.07)
    return vel * (0.5 * tone + nz)


def impact(vel=1.0, length=3.5):
    n = int(length * FS)
    t = np.arange(n) / FS
    f = 32 + 40 * np.exp(-t / 0.18)
    boom = np.sin(2 * np.pi * np.cumsum(f) / FS) * np.exp(-t / 0.9)
    crash = hp(rng.standard_normal(n), 4000) * np.exp(-t / 1.1) * 0.22
    body = lp(rng.standard_normal(n), 500) * np.exp(-t / 0.15) * 0.5
    return vel * (boom + crash + body) * adsr(n, 0.001, 0.6)


def riser(length, vel=1.0):
    n = int(length * FS)
    t = np.arange(n) / FS
    p = t / length
    x = rng.standard_normal(n)
    noise = lp(x, 1500) * (1 - p) + hp(x, 3000) * p
    tone = np.sin(2 * np.pi * np.cumsum(180 * 2 ** (2.5 * p)) / FS) * 0.12
    return vel * (noise * 0.6 + tone) * p**2.2


def rev_cymbal(length=1.5, vel=1.0):
    n = int(length * FS)
    t = np.arange(n) / FS
    x = hp(rng.standard_normal(n), 5000) * np.exp(-t / 0.6)
    return vel * x[::-1]


# ------------------------------------------------------------------ arrangement
B = {k: np.zeros(N) for k in ("pad", "strings", "bass", "keys", "pluck", "kick", "perc", "fx")}
kick_times = []


def section(t):
    if t < 3:
        return "hook"
    if t < 11:
        return "title"
    if t < 23:
        return "day1"
    if t < 37:
        return "brief"
    if t < 47:
        return "montage"
    if t < 55:
        return "finale"
    return "outro"


# hook: stabs + filtered kicks on every cut (beats), riser + reverse cymbal into the drop
for i, t in enumerate(np.arange(0, 3.0, BEAT)):
    tones, root = chord_at(t)
    for m in tones[2:]:
        add(B["keys"], stab(m + 12, 0.22 + 0.04 * i), t)
    add(B["kick"], lp(kick(0.55 + 0.07 * i), 300 + 900 * i), t)
    kick_times.append(t)
add(B["fx"], impact(0.55, 2.5), 0.0)
add(B["fx"], riser(1.5, 0.45), 1.5)
add(B["fx"], rev_cymbal(1.5, 0.35), 1.5)
for t in np.arange(2.0, 3.0, 0.125):  # snare build
    add(B["perc"], snare(0.12 + 0.25 * (t - 2.0)), t)

# drops / big hits
for t, v in [(3.0, 1.0), (47.0, 1.0), (55.0, 0.8)]:
    add(B["fx"], impact(v), t)
add(B["fx"], riser(2.0, 0.4), 45.0)
add(B["fx"], rev_cymbal(2.0, 0.35), 45.0)
add(B["fx"], riser(2.0, 0.3), 21.0)
add(B["fx"], rev_cymbal(1.2, 0.25), 35.8)
for t in np.arange(46.0, 47.0, 0.125):
    add(B["perc"], snare(0.1 + 0.3 * (t - 46.0)), t)

# per-bar parts
for k in range(0, 29):
    t0 = bar(k)
    if t0 >= DUR:
        break
    sec = section(t0)
    tones, root = chord_at(t0)
    n = int((BAR + 0.5) * FS)
    # pads every bar from the drop
    lvl = {"title": 0.12, "day1": 0.11, "brief": 0.12, "montage": 0.13, "finale": 0.15, "outro": 0.15}[sec]
    for m in tones:
        add(B["pad"], saw(hz(m), n) * adsr(n, 0.25, 0.6) * lvl, t0)
    if sec in ("montage", "finale", "outro"):
        for m in tones[-3:]:
            add(B["strings"], saw(hz(m + 12), n, (-0.11, 0.04, 0.13)) * adsr(n, 0.4, 0.8) * 0.06, t0)
    # bass: whole notes in the title, driving 8ths later
    if sec == "title":
        bn = int(BAR * FS)
        tb = np.arange(bn) / FS
        add(B["bass"], (np.sin(2 * np.pi * hz(root) * tb) + 0.3 * np.sin(4 * np.pi * hz(root) * tb)) * adsr(bn, 0.03, 0.3) * 0.14, t0)
    elif sec != "outro":
        for j in range(8):
            bn = int(0.24 * FS)
            tb = np.arange(bn) / FS
            m = root + (12 if j % 4 == 3 else 0)
            x = lp(saw(hz(m), bn, (0.0,)), 700) * 0.6 + np.sin(2 * np.pi * hz(m) * tb)
            add(B["bass"], x * adsr(bn, 0.004, 0.06) * 0.11, t0 + j * BEAT / 2)
    # piano arpeggio (8ths), pluck ostinato (16ths)
    arp = sorted(tones)
    pat = [0, 2, 4, 3, 1, 3, 4, 2]
    if sec in ("title", "day1", "brief", "montage", "finale"):
        for j in range(8):
            m = arp[pat[j] % len(arp)] + 12
            add(B["keys"], piano(m, 0.26 if j % 4 else 0.34), t0 + j * BEAT / 2)
    if sec in ("day1", "brief", "montage", "finale"):
        for j in range(16):
            m = arp[[0, 4, 2, 4, 1, 4, 3, 4][j % 8] % len(arp)] + 24
            add(B["pluck"], pluck(m, 0.16 if j % 4 else 0.22, 0.4, 1.4 if sec in ("montage", "finale") else 0.9), t0 + j * BEAT / 4)
    # drums
    if sec == "title" and k >= 2:
        for b in (0, 2):
            add(B["kick"], kick(0.6), t0 + b * BEAT)
            kick_times.append(t0 + b * BEAT)
    if sec == "day1":
        for b in (0, 2):
            add(B["kick"], kick(0.7), t0 + b * BEAT)
            kick_times.append(t0 + b * BEAT)
        for j in range(8):
            add(B["perc"], hat(0.10 if j % 2 else 0.05), t0 + j * BEAT / 2)
    if sec in ("brief", "montage", "finale"):
        for b in range(4):
            add(B["kick"], kick(0.8), t0 + b * BEAT)
            kick_times.append(t0 + b * BEAT)
        for b in (1, 3):
            add(B["perc"], clap(0.32 if sec == "brief" else 0.4), t0 + b * BEAT)
        for j in range(8):
            add(B["perc"], hat(0.14, open_=(j % 2 == 1 and sec != "brief")), t0 + j * BEAT / 2)
        if sec in ("montage", "finale"):
            for j in range(16):
                add(B["perc"], hat(0.05), t0 + j * BEAT / 4 + 0.01)

# outro: sustained tonic, final piano phrase
for t, m, v in [(55.0, 76, 0.45), (55.0, 64, 0.35), (56.0, 80, 0.3), (57.0, 83, 0.25), (58.0, 88, 0.18)]:
    add(B["keys"], piano(m, v, 4.0), t)

# ------------------------------------------------------------------ mix
tt = np.arange(N) / FS
# sidechain pump from every kick (pads, strings, bass, pluck duck ~6 dB, 180ms recovery)
sc = np.ones(N)
for kt in kick_times:
    i = int(kt * FS)
    m = int(0.22 * FS)
    j = min(N, i + m)
    sc[i:j] = np.minimum(sc[i:j], 1 - 0.5 * np.exp(-np.arange(j - i) / FS / 0.09))
pad = lp(B["pad"], 2600) * sc
strings = hp(lp(B["strings"], 6500), 300) * sc
bass = hp(B["bass"], 40, 3) * sc
pluck_bus = hp(B["pluck"], 400) * (0.6 + 0.4 * sc)
keys = B["keys"]
drums = hp(B["kick"], 48, 3) * 0.8 + B["perc"]
fx = hp(B["fx"], 42, 3)

dry = pad + strings + bass + keys * 0.95 + pluck_bus * 0.9 + drums * 0.85 + fx * 0.7
nir = int(2.2 * FS)
tir = np.arange(nir) / FS
irs = []
for _ in range(2):
    ir = lp(rng.standard_normal(nir) * np.exp(-6.9 * tir / 1.9), 7000)
    irs.append(ir / np.sqrt(np.sum(ir**2)))
wet_src = hp(pad * 0.8 + strings + keys + pluck_bus * 0.5 + B["perc"] * 0.15, 200)
L = dry + 0.42 * fftconvolve(wet_src, irs[0])[:N] + 0.12 * pluck_bus
R = dry + 0.42 * fftconvolve(wet_src, irs[1])[:N] - 0.12 * pluck_bus
st = np.stack([L, R])
st *= np.clip((DUR - tt) / 3.5, 0, 1) ** 1.6  # ring-out to silence
st /= np.max(np.abs(st))
st = np.tanh(1.5 * st) / np.tanh(1.5)  # gentle glue / soft clip
st *= 10 ** (-1.0 / 20)
wavfile.write(sys.argv[1], FS, (st.T * 32767).astype(np.int16))
print("wrote", sys.argv[1], f"{DUR}s")
