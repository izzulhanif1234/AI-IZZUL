"""Synthesize the Pink Move teaser's own SFX (bass hit, swoosh, riser).

usage: pinkmove_sfx.py OUT_DIR
Writes bass-hit.wav, swoosh.wav, riser.wav (48 kHz stereo) so hits land
exactly on frame and nothing needs licensing.
"""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(7)
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)


def t(sec):
    return np.arange(int(sec * SR)) / SR


def norm(x, peak_db=-1.0):
    return x / np.max(np.abs(x)) * 10 ** (peak_db / 20)


def stereo(left, right=None):
    return np.stack([left, left if right is None else right], axis=1)


def band(x, lo, hi):
    return sosfilt(butter(4, [lo, hi], btype="band", fs=SR, output="sos"), x)


# Bass hit: pitch-dropping sub, a click transient and a short noise thump.
tt = t(1.4)
freq = 38 + 90 * np.exp(-tt * 9)
sub = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-tt * 2.6)
sub = np.tanh(sub * 2.2)
click = band(rng.standard_normal(len(tt)), 1500, 9000) * np.exp(-tt * 140) * 0.6
thump = band(rng.standard_normal(len(tt)), 60, 400) * np.exp(-tt * 22) * 0.9
hit = sub + click + thump
hit[: int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))
sf.write(out / "bass-hit.wav", stereo(norm(hit, -0.8)), SR)

# Swoosh: noise through a band sweeping up then down, panned left to right.
tt = t(0.55)
env = np.interp(tt, [0, 0.22, 0.55], [0, 1, 0]) ** 1.6
noise = rng.standard_normal(len(tt))
centre = np.interp(tt, [0, 0.22, 0.55], [500, 5200, 900])
chunks = []
step = 512
for i in range(0, len(tt), step):
    c = centre[i]
    seg = band(noise[max(0, i - 2048): i + step], c * 0.6, min(c * 1.6, SR / 2 - 100))
    chunks.append(seg[-min(step, len(tt) - i):])
sw = np.concatenate(chunks)[: len(tt)] * env
pan = np.interp(tt, [0, 0.55], [0.15, 0.85])
sf.write(out / "swoosh.wav", norm(stereo(sw * (1 - pan), sw * pan), -2.0), SR)

# Riser: swelling noise plus a rising tone, ending abruptly on the hit.
tt = t(0.5)
env = (tt / tt[-1]) ** 2.2
tone = np.sin(2 * np.pi * np.cumsum(np.interp(tt, [0, 0.5], [220, 1400])) / SR)
rs = (band(rng.standard_normal(len(tt)), 2000, 12000) * 0.7 + tone * 0.25) * env
sf.write(out / "riser.wav", stereo(norm(rs, -3.0)), SR)
print("wrote", sorted(p.name for p in out.glob("*.wav")))
