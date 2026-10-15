"""Original score for the PMH benchmarking visit highlights (synthesised, no third-party audio).

Trend-led corporate future-house: 120 BPM (beat 0.5s, bar 2s), G major, I-V-vi-IV, offbeat
supersaw stabs with heavy sidechain pump, shuffled hats, a "drop gap" (0.25s of silence) before
each drop. Bar 1 / first drop at 4.0s; chapter changes of the edit land on bar lines:
  0-4 hook build | 4 drop: title | 8 ch1 meeting (breakdown) | 16 ch2 staff (groove) |
  26 ch3 speech (groove + strings) | 36 ch4 presentation (second drop) | 48 ch5 together (lift) |
  54 end card (ring-out to 60)
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
T0 = 4.0
N = int(DUR * FS)
rng = np.random.default_rng(14102026)


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


# ------------------------------------------------------------------ harmony (G major)
PROG = [  # I - V/F# - vi - IV
    ([55, 59, 62, 67, 71], 43),  # G
    ([54, 57, 62, 66, 69], 42),  # D/F#
    ([52, 55, 59, 64, 67], 40),  # Em
    ([48, 55, 60, 64, 67], 36),  # C
]


def chord_at(t):
    if t >= 54.0:
        return ([55, 59, 62, 66, 69, 71, 74], 43)  # Gmaj9 ring-out
    k = int(max(0.0, t - T0) // BAR) if t >= T0 else int((t + 4.0) // BAR) % 2 * 3
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



def supersaw(m, length, vel=1.0, cutoff=5000):
    n = int(length * FS)
    x = saw(hz(m), n, (-0.18, -0.07, 0.0, 0.07, 0.18)) + 0.5 * saw(hz(m + 12), n, (-0.1, 0.1))
    return vel * lp(x, cutoff) * adsr(n, 0.005, min(0.08, length / 3))


# ------------------------------------------------------------------ arrangement
B = {k: np.zeros(N) for k in ("pad", "strings", "bass", "keys", "pluck", "kick", "perc", "fx", "saw")}
kick_times = []


def section(t):
    for lim, name in [(4, "hook"), (8, "drop1"), (16, "ch1"), (26, "ch2"), (36, "ch3"), (48, "drop2"), (54, "ch5")]:
        if t < lim:
            return name
    return "outro"


# hook (0-4): pickup build. Kick on every beat with the low-pass opening, pluck arp brightening,
# snare roll accelerating into a drop gap (3.75-4.0) and the drop.
for i, t in enumerate(np.arange(0, 3.75, BEAT)):
    add(B["kick"], lp(kick(0.5 + 0.06 * i), 250 + 700 * i), t)
    kick_times.append(t)
for j, t in enumerate(np.arange(0, 3.75, BEAT / 4)):
    tones, _ = chord_at(t)
    arp = sorted(tones)
    add(B["pluck"], pluck(arp[[0, 2, 4, 2][j % 4] % len(arp)] + 24, 0.08 + 0.12 * t / 4, 0.3, 0.5 + t / 3), t)
add(B["fx"], impact(0.5, 2.0), 0.0)
add(B["fx"], riser(3.7, 0.5), 0.05)
add(B["fx"], rev_cymbal(1.75, 0.4), 2.0)
for t in list(np.arange(2.0, 3.0, 0.25)) + list(np.arange(3.0, 3.75, 0.125)):
    add(B["perc"], snare(0.1 + 0.25 * (t - 2.0) / 1.75), t)

# drops and hits
for t, v in [(4.0, 1.0), (36.0, 1.0), (48.0, 0.8), (54.0, 0.75)]:
    add(B["fx"], impact(v), t)
for t0, L, v in [(14.0, 2.0, 0.3), (24.0, 2.0, 0.3), (34.0, 1.75, 0.45), (46.0, 2.0, 0.35), (52.0, 2.0, 0.35)]:
    add(B["fx"], riser(L, v), t0)
    add(B["fx"], rev_cymbal(L, 0.3), t0)
for t in np.arange(35.0, 35.75, 0.125):
    add(B["perc"], snare(0.12 + 0.3 * (t - 35.0)), t)

for k in range(0, 28):
    t0 = bar(k)
    if t0 >= DUR:
        break
    sec = section(t0)
    tones, root = chord_at(t0)
    arp = sorted(tones)
    n = int((BAR + 0.5) * FS)
    lvl = {"drop1": 0.10, "ch1": 0.085, "ch2": 0.09, "ch3": 0.09, "drop2": 0.10, "ch5": 0.11, "outro": 0.14}[sec]
    for m in tones:
        add(B["pad"], saw(hz(m), n) * adsr(n, 0.3, 0.6) * lvl, t0)
    # offbeat supersaw stabs: the signature of the drops
    if sec in ("drop1", "drop2", "ch5"):
        for b in range(4):
            for m in tones[1:]:
                add(B["saw"], supersaw(m + 12, 0.22, 0.12, 7000), t0 + b * BEAT + BEAT / 2)
    if sec == "ch3":
        for m in tones[-3:]:
            add(B["strings"], saw(hz(m + 12), n, (-0.11, 0.04, 0.13)) * adsr(n, 0.4, 0.8) * 0.045, t0)
    # bass
    if sec == "ch1":
        bn = int(BAR * FS)
        tb = np.arange(bn) / FS
        add(B["bass"], (np.sin(2 * np.pi * hz(root) * tb) + 0.3 * np.sin(4 * np.pi * hz(root) * tb)) * adsr(bn, 0.05, 0.3) * 0.12, t0)
    elif sec != "outro":
        for j in range(8):
            if j % 2 == 0 and sec != "ch2":
                continue  # offbeat bass in the drops (house style)
            bn = int(0.22 * FS)
            tb = np.arange(bn) / FS
            x = lp(saw(hz(root), bn, (0.0,)), 800) * 0.6 + np.sin(2 * np.pi * hz(root) * tb)
            add(B["bass"], x * adsr(bn, 0.004, 0.05) * 0.11, t0 + j * BEAT / 2)
    # keys: piano in the meeting breakdown, piano + pluck elsewhere
    if sec in ("ch1", "ch3", "ch5"):
        pat = [0, 2, 4, 3, 1, 3, 4, 2]
        for j in range(8):
            add(B["keys"], piano(arp[pat[j] % len(arp)] + 12, (0.2 if j % 4 else 0.27) * (0.8 if sec == "ch3" else 1)), t0 + j * BEAT / 2)
    if sec in ("ch2", "ch3", "drop1", "drop2", "ch5"):
        for j in range(16):
            m = arp[[0, 4, 2, 4, 1, 4, 3, 4][j % 8] % len(arp)] + 24
            add(B["pluck"], pluck(m, 0.15 if j % 4 else 0.2, 0.35, 1.2), t0 + j * BEAT / 4)
    # drums
    four = sec in ("drop1", "ch2", "ch3", "drop2", "ch5")
    if sec == "ch1" and k >= 4:  # heartbeat kick in the second half of the meeting
        for b in (0, 2):
            add(B["kick"], kick(0.55), t0 + b * BEAT)
            kick_times.append(t0 + b * BEAT)
    if four:
        for b in range(4):
            add(B["kick"], kick(0.85 if sec in ("drop1", "drop2", "ch5") else 0.72), t0 + b * BEAT)
            kick_times.append(t0 + b * BEAT)
        for b in (1, 3):
            add(B["perc"], clap(0.4), t0 + b * BEAT)
        for j in range(16):  # shuffled 16th hats, open hat on the offbeat
            sw = 0.03 if j % 2 else 0.0
            add(B["perc"], hat(0.12 if j % 4 == 2 else 0.06, open_=(j % 4 == 2)), t0 + j * BEAT / 4 + sw)

# drop gap: silence everything but the riser tail for 0.25s before each drop
GAPS = [(3.75, 4.0), (35.75, 36.0)]

# outro: ring-out phrase
for t, m, v in [(54.0, 79, 0.45), (54.0, 67, 0.35), (55.0, 83, 0.3), (56.0, 86, 0.25), (57.0, 91, 0.16)]:
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
bass = hp(B["bass"], 45, 3) * sc * 0.75
pluck_bus = hp(B["pluck"], 400) * (0.6 + 0.4 * sc)
keys = B["keys"]
drums = hp(B["kick"], 50, 3) * 0.6 + B["perc"] * 1.1
fx = hp(B["fx"], 42, 3)
saws = hp(B["saw"], 180) * (0.25 + 0.75 * sc)

dry = pad + strings + saws + bass + keys * 0.95 + pluck_bus * 0.9 + drums * 0.85 + fx * 0.7
nir = int(2.2 * FS)
tir = np.arange(nir) / FS
irs = []
for _ in range(2):
    ir = lp(rng.standard_normal(nir) * np.exp(-6.9 * tir / 1.9), 7000)
    irs.append(ir / np.sqrt(np.sum(ir**2)))
wet_src = hp(pad * 0.8 + strings + saws * 0.5 + keys + pluck_bus * 0.5 + B["perc"] * 0.15, 200)
L = dry + 0.42 * fftconvolve(wet_src, irs[0])[:N] + 0.12 * pluck_bus
R = dry + 0.42 * fftconvolve(wet_src, irs[1])[:N] - 0.12 * pluck_bus
st = np.stack([L, R])
for g0, g1 in GAPS:
    i0, i1 = int(g0 * FS), int(g1 * FS)
    st[:, i0:i1] *= np.linspace(1, 0, i1 - i0) ** 6
st *= np.clip((DUR - tt) / 3.5, 0, 1) ** 1.6  # ring-out to silence
st /= np.max(np.abs(st))
st = np.tanh(1.5 * st) / np.tanh(1.5)  # gentle glue / soft clip
st *= 10 ** (-1.0 / 20)
wavfile.write(sys.argv[1], FS, (st.T * 32767).astype(np.int16))
print("wrote", sys.argv[1], f"{DUR}s")

