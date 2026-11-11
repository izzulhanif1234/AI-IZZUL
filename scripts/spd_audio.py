"""SPD GREEN soundtrack: original score + "kertas -> piksel" sound design + VO/dialogue mix.

Everything is synthesised here (no stock whoosh/pop/ding library):
  score   felt piano, marimba, warm pad, soft kit, bass, glass bells; chords follow the film's acts and
          change on the scene cuts read from spd_build (so music stays locked to picture after retiming)
  sfx     paper riffle / crumple / tear, rubber stamp, drawer slam, pencil + chalk, tuned key taps,
          barcode beep chord, abacus beads, embosser, polaroid shutter, ink drop, granular dissolve
  foley   real paper/shelf sound from the acted footage under the cold-open montage
Mix: VO + dialogue on top, music side-chained to the voice, sfx bus, short reverb sends, -14 LUFS master.

usage: python3 scripts/spd_audio.py   -> edits/spd-green/audio/mix.wav (+ stems)
"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = "/home/user/AI-IZZUL"
sys.path.insert(0, f"{ROOT}/scripts")
import spd_build as B  # noqa: E402

SR = 48000
OUT = f"{ROOT}/edits/spd-green/audio"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)

# ----------------------------------------------------------------------------- dsp helpers
def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)


def env_adsr(n, a=0.005, d=0.1, s=0.6, r=0.2, hold=None):
    t = np.arange(n) / SR
    hold = (n / SR - r) if hold is None else hold
    e = np.where(t < a, t / max(a, 1e-4), 1.0)
    e = np.where((t >= a) & (t < a + d), 1 - (1 - s) * (t - a) / d, e)
    e = np.where((t >= a + d) & (t < hold), s, e)
    e = np.where(t >= hold, s * np.clip(1 - (t - hold) / r, 0, 1), e)
    return e


def noise(dur):
    return rng.standard_normal(int(round(dur * SR)))


def pink(dur):
    n = int(dur * SR)
    X = np.fft.rfft(rng.standard_normal(n))
    f = np.arange(len(X)); f[0] = 1
    return np.fft.irfft(X / np.sqrt(f), n) * 8


def note_hz(name):
    names = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    n, o = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((names[n] + 12 * (o - 4)) / 12)


def norm(x, peak=0.9):
    m = np.max(np.abs(x)) + 1e-9
    return x / m * peak


def make_ir(dur=2.2, damp=3.2, seed=3):
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    L = r.standard_normal(n) * np.exp(-damp * t)
    R = r.standard_normal(n) * np.exp(-damp * t)
    L, R = lp(L, 7000), lp(R, 6500)
    L[:int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
    R[:int(0.017 * SR)] *= np.linspace(0, 1, int(0.017 * SR))
    return np.stack([L, R], 1) / np.sqrt(np.sum(L ** 2))


IR_HALL = make_ir(2.6, 2.4)
IR_ROOM = make_ir(0.9, 6.5, 5)


def reverb(stereo, ir, wet):
    out = np.zeros((len(stereo) + len(ir) - 1, 2))
    for c in range(2):
        out[:, c] = fftconvolve(stereo[:, c], ir[:, c])
    out[:len(stereo)] = out[:len(stereo)] * wet + stereo * (1 - wet * 0.3)
    out[len(stereo):] *= wet
    return out


# ----------------------------------------------------------------------------- instruments (mono)
def piano(f, dur, vel=0.7, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    for k in range(1, 11):
        fk = k * f * np.sqrt(1 + 0.00035 * k * k)
        if fk > 12000:
            break
        amp = (1 / k ** (1.35 / bright)) * (0.6 + 0.4 * vel)
        y += amp * np.sin(2 * np.pi * fk * t + rng.uniform(0, 6.28)) * np.exp(-t * (0.55 + 0.42 * k) * (1.2 - 0.4 * vel))
    ham = lp(noise(0.012), 2500) * np.linspace(1, 0, int(0.012 * SR)) * 0.15 * vel
    y[:len(ham)] += ham
    a = int(0.004 * SR); y[:a] *= np.linspace(0, 1, a)
    y[-int(0.08 * SR):] *= np.linspace(1, 0, int(0.08 * SR))
    return y * vel


def marimba(f, vel=0.6, dur=1.2):
    n = int(dur * SR); t = np.arange(n) / SR
    y = (np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) + 0.35 * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t * 11)
         + 0.12 * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t * 26))
    a = int(0.002 * SR); y[:a] *= np.linspace(0, 1, a)
    return y * vel


def bell(f, vel=0.5, dur=2.5):
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    for r, a, d in [(1, 1, 1.6), (2.76, .5, 3.2), (5.4, .3, 5.5), (8.93, .18, 8), (13.3, .1, 12)]:
        y += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d)
    a = int(0.001 * SR); y[:a] *= np.linspace(0, 1, a)
    return y * vel * 0.6


def pad(freqs, dur, vel=0.4, attack=1.2, release=1.6, cutoff=2200):
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    for f in freqs:
        for det in (-0.006, 0, 0.0055):
            ff = f * (1 + det)
            for k in range(1, 9):
                y += (1 / k) * np.sin(2 * np.pi * ff * k * t + rng.uniform(0, 6.28)) * (0.5 if k > 1 else 1)
    y = lp(y, cutoff)
    e = np.minimum(1, t / attack) * np.clip((dur - t) / release, 0, 1)
    lfo = 1 + 0.08 * np.sin(2 * np.pi * 0.17 * t)
    return y * e * lfo * vel / (len(freqs) * 6)


def bass(f, dur, vel=0.6):
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    return y * env_adsr(n, 0.01, 0.15, 0.7, 0.12) * vel


def kick(vel=0.7):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 46 + 70 * np.exp(-t * 28)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    y[:200] += lp(noise(200 / SR), 3000) * 0.2
    return y * vel


def hat(vel=0.25, dur=0.05):
    y = hp(noise(dur), 7000) * np.exp(-np.arange(int(dur * SR)) / SR * 70)
    return y * vel


def shaker(vel=0.2):
    n = int(0.09 * SR)
    y = bp(noise(0.09), 4000, 11000) * np.sin(np.linspace(0, np.pi, n)) ** 2
    return y * vel


def clap(vel=0.25):
    y = np.zeros(int(0.25 * SR))
    for k, d in enumerate((0, 0.011, 0.022)):
        b = bp(noise(0.2), 900, 3500) * np.exp(-np.arange(int(0.2 * SR)) / SR * (40 if k < 2 else 16))
        i = int(d * SR); y[i:i + len(b)] += b[:len(y) - i]
    return y * vel


# ----------------------------------------------------------------------------- sound design (mono)
def paper_riffle(dur=0.45, vel=0.5, rate=38):
    n = int(dur * SR); t = np.arange(n) / SR
    am = (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * rate * t * (1 + 0.6 * t / dur)))) * np.exp(-((t - dur * 0.45) / (dur * 0.35)) ** 2)
    y = bp(noise(dur), 1800, 9000) * am
    return lp(y, 9000) * vel


def paper_whoosh(dur=0.6, vel=0.45, up=True):
    n = int(dur * SR); t = np.arange(n) / SR
    x = pink(dur)
    seg = 8
    out = np.zeros(n)
    for i in range(seg):  # moving band = organic swish
        a, b = int(i * n / seg), int((i + 1) * n / seg)
        c = (500 + 4500 * (i / seg if up else 1 - i / seg))
        out[a:b] = bp(x, c * 0.6, min(c * 1.8, 20000))[a:b]
    shape = np.sin(np.pi * t / dur) ** 1.6
    crackle = np.zeros(n)
    for _ in range(int(dur * 60)):
        i = rng.integers(0, n - 300); crackle[i:i + 120] += hp(noise(120 / SR), 3000) * rng.uniform(0.2, 0.6)
    return (out * shape + crackle * shape * 0.5) * vel


def crumple(dur=0.8, vel=0.6):
    n = int(dur * SR); y = np.zeros(n)
    for _ in range(int(dur * 260)):
        i = rng.integers(0, n - 800); L = rng.integers(80, 700)
        y[i:i + L] += bp(noise(L / SR), rng.uniform(800, 3000), rng.uniform(5000, 12000)) * np.exp(-np.arange(L) / L * 4) * rng.uniform(0.2, 1)
    return y * np.linspace(0.5, 1, n) * vel


def tear(dur=0.35, vel=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    steps = 10
    for i in range(steps):
        a, b = int(i * n / steps), int((i + 1) * n / steps)
        c = 1500 + 5000 * i / steps
        y[a:b] = bp(noise(dur), c * 0.7, c * 1.6)[a:b] * (0.6 + 0.4 * np.abs(np.sin(i * 1.7)))
    return y * np.minimum(1, t * 40) * np.exp(-t * 3) * vel


def stamp(vel=0.8):
    n = int(0.5 * SR); t = np.arange(n) / SR
    f = 52 + 90 * np.exp(-t * 35)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 12)
    slap = bp(noise(0.5), 300, 2500) * np.exp(-t * 60) * 0.6
    return (body + slap) * vel


def drawer_slam(vel=0.8):
    n = int(1.6 * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    for r, a, d in [(1, 1, 3), (2.31, .6, 5), (3.87, .4, 7), (5.12, .3, 9), (7.4, .2, 13)]:
        y += a * np.sin(2 * np.pi * 70 * r * t) * np.exp(-t * d)
    y += bp(noise(1.6), 200, 3000) * np.exp(-t * 30) * 0.8
    sub = np.sin(2 * np.pi * np.cumsum(40 + 30 * np.exp(-t * 6)) / SR) * np.exp(-t * 2.2)
    return (y * 0.6 + sub) * vel


def scratch(dur=0.5, vel=0.25, chalk=False):
    n = int(dur * SR); t = np.arange(n) / SR
    jitter = np.clip(np.interp(t, np.linspace(0, dur, max(4, int(dur * 30))), rng.uniform(0.2, 1, max(4, int(dur * 30)))), 0, 1)
    y = (bp(noise(dur), 2500, 9000) if not chalk else bp(noise(dur), 1200, 7000))
    if chalk:
        y = y * (rng.uniform(0, 1, n) > 0.35)
    return y * jitter * np.sin(np.pi * t / dur) ** 0.5 * vel


def tick(f, vel=0.35, dur=0.18):
    """tuned key tap: short plucked string + click"""
    n = int(dur * SR)
    period = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, period)
    y = np.zeros(n)
    for i in range(n):
        y[i] = buf[i % period]
        buf[i % period] = 0.5 * (buf[i % period] + buf[(i + 1) % period]) * 0.996
    y[:120] += hp(noise(120 / SR), 4000) * 0.4
    return y * np.exp(-np.arange(n) / SR * 18) * vel


def glass(f, vel=0.35):
    return bell(f, vel, 1.6)


def beep_chord(vel=0.35, dur=0.28):
    n = int(dur * SR); t = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * f * 2 * t)) for f in (note_hz("D6"), note_hz("F#6"), note_hz("A6")))
    return y * env_adsr(n, 0.003, 0.05, 0.8, 0.08) * vel / 3


def laser_hum(dur=1.6, vel=0.15):
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * 120 * t) * 0.5 + bp(noise(dur), 2000, 6000) * 0.2 + np.sin(2 * np.pi * (900 + 300 * np.sin(2 * np.pi * 1.2 * t)) * t) * 0.15
    return y * np.sin(np.pi * t / dur) * vel


def abacus(dur, vel=0.3):
    n = int(dur * SR); y = np.zeros(n)
    k = 0
    tt = 0.0
    while tt < dur - 0.05:
        f = rng.choice([1800, 2100, 2400, 2700])
        b = tick(f, 0.6, 0.06)
        i = int(tt * SR); y[i:i + len(b)] += b[:n - i]
        tt += 0.035 + 0.08 * (tt / dur) ** 1.5  # rolls, then slows
        k += 1
    return y * vel


def mallet(f=note_hz("D2"), vel=0.8):
    y = piano(f, 3.0, 0.9, 0.6)
    b = bass(f, 1.2, 0.5)
    y[:len(b)] += b
    return y * vel


def embosser(vel=0.6):
    y = crumple(0.18, 0.8)
    y = np.concatenate([y, np.zeros(int(0.05 * SR))])
    y[:len(stamp(0.6))] += stamp(0.6)[:len(y)] * 0.6
    return y * vel


def shutter(vel=0.5):
    a = hp(noise(0.012), 2000) * 1.0
    gap = np.zeros(int(0.06 * SR))
    b = bp(noise(0.03), 1500, 6000) * np.exp(-np.arange(int(0.03 * SR)) / SR * 80)
    whirr = bp(noise(0.35), 300, 1200) * np.sin(2 * np.pi * 38 * np.arange(int(0.35 * SR)) / SR) ** 2 * 0.3
    return np.concatenate([a, gap, b, whirr]) * vel


def ink_drop(vel=0.5):
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 1600 * np.exp(-t * 18) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14) * vel


def dissolve(dur=1.2, vel=0.35):
    n = int(dur * SR); y = np.zeros(n)
    for _ in range(int(dur * 400)):
        i = rng.integers(0, n - 400)
        L = rng.integers(40, 300)
        y[i:i + L] += hp(noise(L / SR), 5000) * rng.uniform(0.1, 0.5)
    sh = sum(bell(note_hz(x), 0.15, dur) for x in ("A6", "D7", "F#7"))
    return (y + sh[:n] * 0.6) * np.sin(np.pi * np.arange(n) / n) * vel


def riser(dur=2.0, vel=0.4):
    n = int(dur * SR); t = np.arange(n) / SR
    x = pink(dur)
    y = np.zeros(n)
    steps = 16
    for i in range(steps):
        a, b = int(i * n / steps), int((i + 1) * n / steps)
        c = 300 + 6000 * (i / steps) ** 2
        y[a:b] = bp(x, c * 0.7, min(c * 1.5, 20000))[a:b]
    rev = piano(note_hz("D3"), dur, 0.8)[::-1] * 0.8 + piano(note_hz("A3"), dur, 0.7)[::-1] * 0.6
    return (y * (t / dur) ** 2 * 0.6 + rev[:n]) * vel


def sub_boom(vel=0.8):
    n = int(2.0 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(38 + 40 * np.exp(-t * 5)) / SR) * np.exp(-t * 1.8) * vel


def wheel(dur=0.6, vel=0.18):
    n = int(dur * SR); y = np.zeros(n)
    tt = 0.0
    while tt < dur:
        b = tick(2600, 0.5, 0.03)
        i = int(tt * SR); y[i:i + len(b)] += b[:n - i]
        tt += 0.03 + 0.04 * np.sin(np.pi * tt / dur) ** 2
    return y * vel


def click(vel=0.45):
    a = bp(noise(0.006), 2000, 9000) * np.linspace(1, 0, int(0.006 * SR))
    b = bp(noise(0.008), 1500, 7000) * np.linspace(1, 0, int(0.008 * SR)) * 0.6
    return np.concatenate([a, np.zeros(int(0.045 * SR)), b]) * vel


def slide(dur=0.45, vel=0.3):
    t = np.arange(int(dur * SR)) / SR
    return bp(noise(dur), 1200, 6000) * np.sin(np.pi * t / dur) ** 1.2 * vel


SCALE = [note_hz(n) for n in ("D5", "E5", "F#5", "A5", "B5", "D6", "E6", "F#6", "A6")]


# ----------------------------------------------------------------------------- timeline helpers
class Track:
    def __init__(self, dur):
        self.y = np.zeros((int(dur * SR) + SR * 4, 2))

    def add(self, t, x, gain=1.0, pan=0.0):
        if t < 0:
            x = x[int(-t * SR):]; t = 0
        i = int(t * SR)
        x = np.asarray(x)
        if x.ndim == 1:
            L, R = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
            x = np.stack([x * L * 1.41, x * R * 1.41], 1)
        j = min(len(self.y), i + len(x))
        if j > i:
            self.y[i:j] += x[:j - i] * gain


def load(path, gain=1.0):
    x = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(x, np.float32).reshape(-1, 2).astype(np.float64) * gain


# ----------------------------------------------------------------------------- score
CH = {  # chord tones (pad), bass root
    "D": (["D3", "F#3", "A3", "D4"], "D2"), "A": (["C#3", "E3", "A3", "E4"], "A1"), "Bm": (["B2", "D3", "F#3", "B3"], "B1"),
    "G": (["B2", "D3", "G3", "D4"], "G1"), "Em": (["B2", "E3", "G3", "E4"], "E2"), "F#m": (["C#3", "F#3", "A3", "C#4"], "F#1"),
    "Dsus": (["D3", "G3", "A3", "D4"], "D2"),
}
ARP = {"D": ["D5", "F#5", "A5", "F#5"], "A": ["C#5", "E5", "A5", "E5"], "Bm": ["B4", "D5", "F#5", "D5"], "G": ["B4", "D5", "G5", "D5"],
       "Em": ["B4", "E5", "G5", "E5"], "F#m": ["C#5", "F#5", "A5", "F#5"], "Dsus": ["D5", "G5", "A5", "G5"]}
BEAT = 60 / 96


def section(trk, t0, t1, prog, layers, vel=1.0):
    """fill [t0,t1) with bars of 4 beats cycling through prog"""
    bar = 4 * BEAT
    t, k = t0, 0
    while t < t1 - 0.3:
        c = prog[k % len(prog)]
        dur = min(bar, t1 - t)
        tones, root = CH[c]
        if "pad" in layers:
            trk["pad"].add(t, pad([note_hz(x) for x in tones], dur + 1.4, 0.55 * vel, attack=0.8, release=1.4), pan=0)
        if "bass" in layers:
            for b in range(4):
                if t + b * BEAT < t1:
                    trk["mus"].add(t + b * BEAT, bass(note_hz(root), BEAT * 0.9, 0.3 * vel))
        if "piano" in layers:
            for j, x in enumerate(tones[1:]):
                trk["mus"].add(t + j * 0.012, piano(note_hz(x) * 2, min(4, dur + 1.5), 0.35 * vel), pan=-0.2 + j * 0.2)
        if "pianosparse" in layers and k % 2 == 0:
            trk["mus"].add(t, piano(note_hz(ARP[c][0]), 4.0, 0.42 * vel), pan=-0.1)
            trk["mus"].add(t + 2 * BEAT, piano(note_hz(ARP[c][2]), 3.0, 0.3 * vel), pan=0.15)
        if "arp8" in layers or "arp16" in layers:
            step = BEAT / (4 if "arp16" in layers else 2)
            n = int(round(dur / step))
            for i in range(n):
                f = note_hz(ARP[c][i % 4]) * (2 if (i // 4) % 2 and "arp16" in layers else 1)
                trk["mus"].add(t + i * step, marimba(f, (0.28 if i % 2 else 0.36) * vel, 0.8), pan=0.35 * np.sin(i * 0.9))
        if "kick2" in layers:
            for b in (0, 2):
                if t + b * BEAT < t1:
                    trk["mus"].add(t + b * BEAT, kick(0.42 * vel))
        if "kick4" in layers:
            for b in range(4):
                if t + b * BEAT < t1:
                    trk["mus"].add(t + b * BEAT, kick(0.42 * vel))
        if "clap" in layers:
            for b in (1, 3):
                if t + b * BEAT < t1:
                    trk["mus"].add(t + b * BEAT, clap(0.2 * vel), pan=0.1)
        if "shaker" in layers:
            for i in range(8):
                if t + i * BEAT / 2 < t1:
                    trk["mus"].add(t + i * BEAT / 2 + 0.01, shaker(0.13 * vel if i % 2 else 0.08 * vel), pan=0.4)
        if "tick" in layers:
            for b in range(4):
                if t + b * BEAT < t1:
                    trk["mus"].add(t + b * BEAT, tick(1800 if b == 0 else 1400, 0.12 * vel, 0.08), pan=0.3)
        if "bells" in layers:
            for i, x in enumerate(ARP[c]):
                trk["mus"].add(t + i * BEAT, bell(note_hz(x) * 2, 0.16 * vel, 2.5), pan=-0.4 + 0.25 * i)
        t += bar
        k += 1


def score(sc, total):
    trk = {"mus": Track(total), "pad": Track(total)}
    st = {S.id: S.start for S in sc}
    en = {S.id: S.start + S.D for S in sc}
    s01 = next(S for S in sc if S.id == "s01")
    # A: cold open -- drone + clock tick, hits on the cuts, mallet at the freeze
    trk["pad"].add(0, pad([note_hz("D2"), note_hz("A2")], B.MONTAGE + 1.0, 0.5, attack=2.0, release=1.0))
    section(trk, 0, B.MONTAGE, ["Bm", "G"], ["pianosparse"], 0.6)
    trk["mus"].add(B.MONTAGE, mallet(note_hz("B1"), 0.7))
    section(trk, B.MONTAGE + 0.1, en["s01"], ["Bm", "G"], ["pad", "pianosparse"], 0.7)
    # B: title + what is SPD
    trk["mus"].add(st["s02"] - 2.0, riser(2.0, 0.5))
    section(trk, st["s02"], en["s02"], ["D", "A"], ["pad", "piano"], 0.8)
    section(trk, st["s03"], en["s03"], ["Bm", "G", "D", "A"], ["pad", "pianosparse", "arp8"], 0.75)
    section(trk, st["s04"], en["s04"], ["Em", "Bm", "G", "A"], ["pad", "pianosparse"], 0.65)
    section(trk, st["s05"], en["s05"], ["D", "A"], ["pad", "piano", "arp8"], 0.8)
    # C: system demo
    section(trk, st["s06"], en["s09"], ["D", "A", "Bm", "G"], ["pad", "arp8", "kick2", "shaker", "bass"], 0.85)
    trk["mus"].add(st["s10"] - 1.8, riser(1.8, 0.55))
    # D: impact
    section(trk, st["s11"], en["s18"], ["G", "D", "A", "Bm"], ["pad", "arp8", "kick2", "bass", "shaker", "piano"], 0.8)
    # E: SPD 2.0
    section(trk, st["s19"], en["s19"], ["Dsus", "D", "G", "A"], ["pad", "bells"], 0.8)
    section(trk, st["s19"] + 7.5, en["s19"], ["G", "A"], ["kick2", "bass"], 0.6)
    trk["mus"].add(en["s19"] - 2.2, riser(2.2, 0.45))
    # F: ending
    trk["pad"].add(st["s20"], pad([note_hz(x) for x in CH["D"][0]], en["s20"] - st["s20"] + 0.5, 0.6, attack=0.4, release=3.0))
    for j, x in enumerate(["D3", "A3", "D4", "F#4", "A4"]):
        trk["mus"].add(st["s20"] + 0.9 + j * 0.06, piano(note_hz(x), 6.5, 0.55), pan=-0.3 + 0.15 * j)
    trk["mus"].add(st["s20"] + 0.9, mallet(note_hz("D1"), 0.5))
    mus = trk["mus"].y + trk["pad"].y
    return mus


# ----------------------------------------------------------------------------- cue sheet (sound design)
def cues(sc):
    """sparse, smooth accents only: soft paper whooshes on transitions, a few tonal hits on the key reveals"""
    S = {s.id: s for s in sc}
    out = []

    def c(sid, t, snd, g=1.0, pan=0.0):
        out.append((S[sid].start + t, snd, g, pan))

    s = S["s01"]
    for k, t in enumerate(B.CUTS[1:]):
        c("s01", t - 0.25, paper_whoosh(0.5, 0.3), 0.45, (-0.4, 0.4)[k % 2])
    c("s01", B.MONTAGE - 0.05, sub_boom(0.6), 0.6)
    c("s02", 0.0, paper_whoosh(0.9, 0.35), 0.5)
    s = S["s02"]
    c("s02", s.w("v02", "SPD") - 0.15, stamp(0.6), 0.55)
    c("s02", s.w("v02", "SPD") + 0.1, dissolve(1.4, 0.35), 0.45)
    s = S["s03"]
    for i, w in enumerate(("tanah", "bangunan", "penyewaan", "penilaian", "dokumen")):
        c("s03", s.w("v03", w) - 0.1, glass(SCALE[i + 1] / 2, 0.3), 0.45, -0.5 + i * 0.25)
    c("s03", s.w("v03", "satu") - 0.2, sub_boom(0.35), 0.45)
    s = S["s04"]
    c("s04", s.D - 0.85, crumple(0.8, 0.6), 0.6)
    c("s05", 0.0, paper_whoosh(0.9, 0.5), 0.7)
    s = S["s05"]
    c("s05", 0.9, glass(note_hz("D6"), 0.4), 0.55)
    c("s05", s.D - 0.6, paper_whoosh(0.6, 0.35), 0.5)
    s = S["s06"]
    c("s06", s.w("v06", "taburan") - 0.4, paper_whoosh(0.6, 0.25, True), 0.4)
    c("s06", s.w("v06", "satu") - 0.4, paper_whoosh(0.8, 0.4, False), 0.55)
    c("s06", s.w("v06", "satu"), sub_boom(0.4), 0.45)
    s = S["s07"]
    t_taip, t_rek, t_pet, t_dok = s.w("v07", "menaip|taip"), s.w("v07", "Rekod"), s.w("v07", "peta"), s.w("v07", "dokumen")
    c("s07", 0.0, paper_whoosh(0.5, 0.3), 0.5)
    for t in (t_taip - 0.25, t_rek - 0.45, t_pet - 0.35):
        c("s07", t, click(0.35), 0.5, 0.2)
    c("s07", t_rek - 0.35, glass(SCALE[5] / 2, 0.3), 0.45)
    c("s07", t_pet - 0.2, paper_whoosh(0.5, 0.3), 0.45, 0.5)
    s = S["s08"]
    for i, w in enumerate(("Pengurusan", "Modal", "pentadbiran")):
        c("s08", s.w("v08", w) - 0.35, paper_whoosh(0.6, 0.4), 0.6, (-0.6, 0.6)[i % 2])
    c("s08", s.w("v08", "barcode") - 0.3, beep_chord(0.35), 0.55)
    c("s08", s.w("v08", "pentadbiran") + 0.25, click(0.35), 0.5)
    c("s08", s.D - 1.5, paper_whoosh(1.2, 0.45, False), 0.6)
    c("s08", s.D - 1.2, sub_boom(0.4), 0.45)
    s = S["s09"]
    for i, (w, n) in enumerate((("dokumen", 1), ("cetakan", 1), ("fail", 1), ("arkib", 1))):
        c("s09", s.w("v09", w, n) - 0.1, marimba(SCALE[2 + i], 0.4), 0.45, -0.3 + 0.2 * i)
    s = S["s10"]
    c("s10", s.w("v10", "impak") - 0.15, stamp(0.9), 0.85)
    c("s10", s.w("v10", "impak") - 0.15, sub_boom(0.8), 0.75)
    c("s10", s.D - 0.45, paper_whoosh(0.5, 0.45), 0.6)
    s = S["s13"]
    c("s13", s.w("v13", "tiga") - 0.05, sub_boom(0.4), 0.45)
    c("s13", s.w("v13", "sebelas|Sebelas") - 0.1, glass(SCALE[5], 0.35), 0.5)
    s = S["s14"]
    c("s14", s.w("v14", "imbasan") - 0.2, beep_chord(0.4), 0.6)
    c("s14", s.w("v14", "imbasan") - 0.2, laser_hum(1.6, 0.15), 0.4)
    s = S["s15"]
    c("s15", s.w("v15", "ringgit") + 0.3, mallet(note_hz("D2"), 0.55), 0.6)
    c("s15", s.w("v15", "ringgit") + 0.3, dissolve(1.0, 0.25), 0.4, 0.4)
    s = S["s16"]
    c("s16", s.w("v16", "dakwat") + 0.3, ink_drop(0.4), 0.45, 0.4)
    c("s16", s.D - 0.5, paper_whoosh(0.5, 0.4), 0.55)
    s = S["s17"]
    c("s17", s.w("v17", "digantikan") - 0.3, dissolve(1.5, 0.45), 0.6)
    c("s17", s.w("v17", "digantikan") + 0.6, glass(SCALE[5], 0.35), 0.5)
    for i, t in enumerate((s.w("v17", "bukti|Buktinya"), s.w("v17", "pemeriksaan") - 0.2)):
        c("s17", t + 0.3, shutter(0.4), 0.45, -0.4 + 0.8 * i)
    s = S["s18"]
    c("s18", s.w("v18", "pengiktirafan|diiktiraf") + 0.35, embosser(0.7), 0.65, -0.2)
    s = S["s19"]
    c("s19", 0.0, riser(2.2, 0.3), 0.5)
    c("s19", s.w("v19", "SPD") - 0.1, sub_boom(0.7), 0.6)
    c("s19", s.w("v19", "SPD") - 0.1, dissolve(1.6, 0.35), 0.45)
    c("s19", s.w("v19", "Setiap") - 0.7, paper_whoosh(0.9, 0.35), 0.5)
    for i, w in enumerate(("Kertas", "Dakwat", "Masa", "Tenaga", "kos")):
        c("s19", s.w("v19", w) - 0.05, glass(SCALE[3 + i], 0.25), 0.4, -0.4 + 0.2 * i)
    s = S["s20"]
    c("s20", max(0.5, s.w("v20", "SPD") - 0.7), paper_whoosh(0.8, 0.4, False), 0.55)
    c("s20", s.w("v20", "SPD") - 0.05, stamp(0.6), 0.55)
    return out


# ----------------------------------------------------------------------------- mix
def main():
    sc, total = B.build(write=False)
    dur = total + 0.5
    s01 = next(S for S in sc if S.id == "s01")
    # voice: VO + acted dialogue
    vo = Track(dur)
    for S in sc:
        for ln, at in S.lines:
            if ln.real and os.environ.get("SPD_VO"):  # VO is added later (atempo SPEED to match the plan)
                v = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{B.HF}/assets/vo/{ln.id}.mp3", "-af", f"atempo={B.SPEED}",
                                    "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
                vo.add(S.start + at, np.frombuffer(v, np.float32).reshape(-1, 2).astype(np.float64), 1.0)
    voice = vo.y
    foley = Track(dur)
    # sfx
    sfx = Track(dur)
    for t, snd, g, pan in cues(sc):
        sfx.add(t, norm(snd, 0.9) * 0.5, g, pan)
    # music
    mus = Track(dur)
    m = score(sc, dur)
    mus.y[:len(m)] += m[:len(mus.y)]
    mus.y = reverb(mus.y, IR_HALL, 0.35)[:len(mus.y)]
    sfx.y = reverb(sfx.y, IR_ROOM, 0.22)[:len(sfx.y)]
    # sidechain: duck music under the voice (smoothed envelope)
    env = np.abs(voice).max(1)
    win = int(0.05 * SR)
    env = np.convolve(env, np.ones(win) / win, mode="same")
    pres = np.clip(env / 0.03, 0, 1)
    att, rel = 1 - np.exp(-1 / (0.06 * SR)), 1 - np.exp(-1 / (0.6 * SR))
    sm = np.zeros_like(pres); v = 0.0
    step = 64
    for i in range(0, len(pres), step):
        target = pres[i]
        v += (target - v) * (att if target > v else rel) * step
        v = min(max(v, 0), 1)
        sm[i:i + step] = v
    duck = 1 - 0.62 * sm
    # stop the music for the IMPAK SPD slam
    s10 = next(S for S in sc if S.id == "s10")
    a, b = int((s10.start + 0.05) * SR), int((s10.start + s10.D - 0.2) * SR)
    gate = np.ones(len(duck)); gate[a:b] = 0.0
    gate[a - int(0.25 * SR):a] = np.linspace(1, 0, int(0.25 * SR))
    gate[b:b + int(0.3 * SR)] = np.linspace(0, 1, int(0.3 * SR))
    music = mus.y * (duck * gate)[:, None]
    music = np.stack([hp(music[:, ch], 32) for ch in range(2)], 1)
    music = music + 0.4 * np.stack([hp(music[:, ch], 5000) for ch in range(2)], 1)  # air
    # levels
    music = music / (np.sqrt(np.mean(music ** 2)) + 1e-9) * 0.055
    sfxb = sfx.y / (np.max(np.abs(sfx.y)) + 1e-9) * 0.42
    voice = voice / (np.max(np.abs(voice)) + 1e-9) * 0.88
    mix = voice + music + sfxb + foley.y * 0.7
    # fade tail
    n_end = int(dur * SR)
    mix = mix[:n_end]
    mix[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))[:, None]
    mix = np.tanh(mix * 1.1) / 1.1
    sf.write(f"{OUT}/premix.wav", mix.astype(np.float32), SR)
    for name, st in (("music", music), ("sfx", sfxb), ("voice", voice)):
        sf.write(f"{OUT}/stem_{name}.wav", st[:n_end].astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/premix.wav", "-af", "loudnorm=I=-14:TP=-1.0:LRA=11",
                    "-ar", "48000", f"{OUT}/mix.wav"], check=True)
    print("mix", f"{OUT}/mix.wav", round(dur, 2), "s")


if __name__ == "__main__":
    main()
