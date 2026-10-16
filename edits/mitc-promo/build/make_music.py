"""Original score for the MITC Melaka 30s promo (synthesised, no third-party audio).

Modern cinematic corporate, 120 BPM (beat 0.5s, bar 2s), D minor epic progression i-VI-III-VII
(Dm Bb F C). Cue sheet = the client storyboard (build/compose.py):
  0.0  cinematic impact out of black, sub drop          | 0.5-4  pulse + hits on each cut, riser
  4.0  metallic hit: logo; beat starts building         | 8.0   drop: full groove (THINK BIGGER)
  12.75 whip                                            | 13/14/15/16 four accented beats (spaces)
  18-23.5 peak (EXPERIENCE)                             | 23.5-24 music stops
  24.0 huge impact + epic half-time finale               | 27.0 metallic hit: logo | 29.0 final hit
Usage: python3 make_music.py <out.wav>
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

FS = 48000
DUR = 30.0
BEAT = 0.5
BAR = 2.0
T0 = 0.0
N = int(DUR * FS)
rng = np.random.default_rng(30)


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


# ------------------------------------------------------------------ harmony (D minor)
PROG = [  # i - VI - III - VII
    ([50, 53, 57, 62, 65], 38),  # Dm
    ([50, 53, 58, 62, 65], 34),  # Bb
    ([48, 53, 57, 60, 65], 41),  # F
    ([48, 52, 55, 60, 64], 36),  # C
]


def chord_at(t):
    if t >= 28.0:
        return ([50, 57, 62, 65, 69, 74], 38)
    return PROG[int(t // BAR) % 4]


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



def metal_hit(vel=1.0, length=3.0):
    """Metallic logo hit: inharmonic partials + noise transient + low thump."""
    n = int(length * FS)
    t = np.arange(n) / FS
    parts = sum(a * np.sin(2 * np.pi * f * t + p) * np.exp(-t * d) for f, a, d, p in
                [(523, 1.0, 2.2, 0), (1307, 0.6, 3.5, 1), (2081, 0.45, 5, 2), (3311, 0.3, 7, 3), (4877, 0.2, 9, 4)])
    noise = hp(rng.standard_normal(n), 3000) * np.exp(-t / 0.04) * 0.6
    thump = np.sin(2 * np.pi * np.cumsum(60 + 80 * np.exp(-t / 0.03)) / FS) * np.exp(-t / 0.25)
    return vel * (0.5 * parts + noise + 0.8 * thump) * adsr(n, 0.001, 0.8)


def braam(m, length, vel=1.0):
    """Low brassy cinematic swell: detuned saws through an opening low-pass."""
    n = int(length * FS)
    t = np.arange(n) / FS
    x = sum(saw(hz(mm), n, (-0.12, 0.0, 0.12)) for mm in (m, m + 7, m + 12)) / 3
    cut = 300 + 2600 * np.clip(t / 0.25, 0, 1) * np.exp(-t / 1.8)
    y = np.zeros(n)
    blk = 2400
    for i in range(0, n, blk):  # time-varying low-pass by blocks
        y[i:i + blk] = lp(x[max(0, i - 4800):i + blk], max(120.0, float(cut[i])))[-min(blk, n - i):]
    return vel * y * adsr(n, 0.02, 0.6)


def tom(vel=1.0, f0=95):
    n = int(0.6 * FS)
    t = np.arange(n) / FS
    f = f0 + 60 * np.exp(-t / 0.04)
    return vel * np.sin(2 * np.pi * np.cumsum(f) / FS) * np.exp(-t / 0.22)

# ------------------------------------------------------------------ arrangement
B = {k: np.zeros(N) for k in ("pad", "strings", "bass", "keys", "pluck", "kick", "perc", "fx", "saw")}
kick_times = []
GAPS = [(23.5, 24.0)]

# 0-4 HOOK: impact from black, ticking pulse, short hits on every cut, riser into the logo
add(B["fx"], impact(1.0, 3.0), 0.0)
add(B["fx"], braam(38, 2.5, 0.55), 0.0)
for t in np.arange(0.5, 3.75, BEAT / 4):
    add(B["perc"], hat(0.05 + 0.05 * (t / 4)), t)
for t in np.arange(0.5, 3.75, BEAT / 2):
    tones, root = PROG[0]
    bn = int(0.22 * FS)
    tb = np.arange(bn) / FS
    add(B["bass"], np.sin(2 * np.pi * hz(root) * tb) * adsr(bn, 0.004, 0.08) * 0.12, t)
for t in (0.5, 1.5, 2.0, 2.5, 3.0):
    add(B["perc"], tom(0.5, 90), t)
    add(B["fx"], impact(0.35, 1.2), t)
for t in (2.5, 3.0):
    for m in (62, 65, 69):
        add(B["saw"], stab(m, 0.12, 0.3), t)
add(B["fx"], riser(1.0, 0.45), 2.95)
add(B["fx"], rev_cymbal(1.0, 0.35), 3.0)

# 4-8 BRAND: metallic logo hit, beat builds (kick on 1 and 3, then 4-on-floor), arp in
add(B["fx"], metal_hit(0.9, 3.5), 4.0)
add(B["fx"], metal_hit(0.45, 2.5), 5.5)
for t in np.arange(4.0, 8.0, BEAT):
    if t < 6.0 and (t - 4.0) % 1.0 > 0.01:
        continue
    add(B["kick"], kick(0.7), t)
    kick_times.append(t)
for t in np.arange(6.0, 7.5, BEAT / 2):
    add(B["perc"], hat(0.1, open_=((t * 2) % 1 > 0.4)), t)
for t in np.arange(7.0, 8.0, 0.125):
    add(B["perc"], snare(0.1 + 0.3 * (t - 7.0)), t)
add(B["fx"], riser(2.0, 0.4), 6.0)
add(B["fx"], rev_cymbal(1.5, 0.35), 6.5)

# 8-23.5 full groove; four accented beats 13-16; peak 18-23.5
for k in range(4, 12):
    t0 = bar(k)
    tones, root = chord_at(t0)
    n = int((BAR + 0.4) * FS)
    peak = t0 >= 18.0
    for m in tones:
        add(B["pad"], saw(hz(m), n) * adsr(n, 0.1, 0.5) * (0.10 if peak else 0.085), t0)
    if peak:
        for m in tones[-3:]:
            add(B["strings"], saw(hz(m + 12), n, (-0.11, 0.04, 0.13)) * adsr(n, 0.3, 0.6) * 0.06, t0)
    for j in range(8):
        if t0 + j * BEAT / 2 >= 23.5:
            break
        m = root + (12 if j % 4 == 3 else 0)
        bn = int(0.22 * FS)
        tb = np.arange(bn) / FS
        x = lp(saw(hz(m), bn, (0.0,)), 700) * 0.6 + np.sin(2 * np.pi * hz(m) * tb)
        add(B["bass"], x * adsr(bn, 0.004, 0.05) * 0.12, t0 + j * BEAT / 2)
    arp = sorted(tones)
    for j in range(16):
        t = t0 + j * BEAT / 4
        if t >= 23.5:
            break
        m = arp[[0, 2, 4, 2, 1, 3, 4, 3][j % 8] % len(arp)] + 12
        add(B["pluck"], pluck(m, 0.15 if j % 4 else 0.21, 0.35, 1.3 if peak else 1.0), t)
    for b in range(4):
        t = t0 + b * BEAT
        if t >= 23.5:
            break
        add(B["kick"], kick(0.85), t)
        kick_times.append(t)
        if b in (1, 3):
            add(B["perc"], clap(0.38), t)
    for j in range(8):
        t = t0 + j * BEAT / 2
        if t < 23.5:
            add(B["perc"], hat(0.12, open_=(j % 2 == 1)), t + 0.0)
add(B["fx"], impact(0.9), 8.0)
add(B["fx"], braam(38, 2.0, 0.5), 8.0)
for t in (13.0, 14.0, 15.0, 16.0):  # spaces: one hit per picture change
    add(B["fx"], impact(0.55, 1.4), t)
    add(B["perc"], tom(0.55, 80), t)
    for m in chord_at(t)[0][2:]:
        add(B["saw"], stab(m + 12, 0.11, 0.35), t)
add(B["fx"], impact(0.8), 18.0)
add(B["fx"], riser(1.5, 0.45), 22.0)
add(B["fx"], rev_cymbal(1.5, 0.4), 22.0)
for t in np.arange(22.5, 23.5, 0.125):
    add(B["perc"], snare(0.12 + 0.25 * (t - 22.5)), t)

# 24-30 FINALE: huge impact, half-time, braams, logo hit, final hit, ring-out
add(B["fx"], impact(1.0, 4.0), 24.0)
add(B["fx"], braam(38, 3.0, 0.75), 24.0)
add(B["fx"], braam(34, 3.0, 0.6), 26.0)
add(B["fx"], metal_hit(0.85, 3.0), 27.0)
add(B["fx"], impact(1.0, 3.0), 29.0)
add(B["fx"], braam(38, 2.0, 0.6), 29.0)
for t in (24.0, 25.0, 26.0, 27.0, 28.0):
    add(B["kick"], kick(0.8), t)
    kick_times.append(t)
    add(B["perc"], tom(0.4, 70), t + 0.5)
for t in (25.5, 26.5, 27.5):
    add(B["perc"], clap(0.35), t)
for k, t0 in enumerate((24.0, 26.0, 28.0)):
    tones, root = chord_at(t0) if t0 < 28 else chord_at(28.0)
    n = int(2.4 * FS)
    for m in tones:
        add(B["strings"], saw(hz(m + 12), n, (-0.11, 0.04, 0.13)) * adsr(n, 0.2, 0.8) * 0.07, t0)
        add(B["pad"], saw(hz(m), n) * adsr(n, 0.1, 0.8) * 0.1, t0)
for t, m, v in [(24.0, 74, 0.4), (26.0, 77, 0.35), (27.0, 81, 0.35), (29.0, 74, 0.45), (29.0, 62, 0.35)]:
    add(B["keys"], piano(m, v, 3.0), t)

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
bass = hp(B["bass"], 45, 3) * sc * 0.6
pluck_bus = hp(B["pluck"], 400) * (0.6 + 0.4 * sc)
keys = B["keys"]
drums = hp(B["kick"], 55, 3) * 0.5 + hp(B["perc"], 60) * 1.1
fx = hp(B["fx"], 55, 3)
saws = hp(B["saw"], 180) * (0.25 + 0.75 * sc)

dry = pad + strings + saws + bass + keys * 0.95 + pluck_bus * 0.9 + drums * 0.85 + fx * 0.55
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
st = st - 0.4 * np.stack([lp(st[0], 120), lp(st[1], 120)])  # ~-4.5 dB low shelf: keep the hits punchy, not boomy
for g0, g1 in GAPS:
    i0, i1 = int(g0 * FS), int(g1 * FS)
    st[:, i0:i1] *= np.linspace(1, 0, i1 - i0) ** 6
st *= np.clip((DUR - tt) / 1.0, 0, 1) ** 1.5  # final hit fades out over the last second
st /= np.max(np.abs(st))
st = np.tanh(1.5 * st) / np.tanh(1.5)  # gentle glue / soft clip
st *= 10 ** (-1.0 / 20)
wavfile.write(sys.argv[1], FS, (st.T * 32767).astype(np.int16))
print("wrote", sys.argv[1], f"{DUR}s")


