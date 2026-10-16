"""Cinematic score for the Colour Rush tee ad (31 s cut): a MusicGen orchestral bed with
synthesized trailer hits laid exactly on the picture's four moments (title slam, tee lands,
turn to the back, end card). Each hit = reverse swell into a low brass "braam" + sub boom,
in the bed's key, with the bed ducked under it. No noise transients (those read as gunshots).
Writes the track and beats.json for the composition's pulse.
usage: colour_rush_score.py bed.wav out.wav beats.json [bed_offset_s]"""
import json
import sys

import librosa
import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

bed_path, out_path, beats_path = sys.argv[1:4]
offset = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
SR = 44100
DUR = 31.0
N = int(SR * DUR)
HITS = [(3.04, 0.7), (7.275, 1.0), (18.365, 0.9), (25.6, 1.15)]  # (time, strength)
rng = np.random.default_rng(31)

bed, _ = librosa.load(bed_path, sr=SR, mono=True)
bed = bed[int(offset * SR):]
if len(bed) < N:
    bed = np.concatenate([bed, np.zeros(N - len(bed))])
bed = bed[:N]
bed /= np.abs(bed).max() + 1e-9

# key of the bed -> root for the hits
chroma = librosa.feature.chroma_cqt(y=librosa.resample(bed, orig_sr=SR, target_sr=22050), sr=22050).mean(axis=1)
major = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
minor = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
scores = [(np.corrcoef(np.roll(major, k), chroma)[0, 1], k, "maj") for k in range(12)]
scores += [(np.corrcoef(np.roll(minor, k), chroma)[0, 1], k, "min") for k in range(12)]
_, root, mode = max(scores)
print("bed key", ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][root], mode)


def lp(x, f):
    return sosfilt(butter(2, f, "lowpass", fs=SR, output="sos"), x)


def mtof(m):
    return 440 * 2 ** ((m - 69) / 12)


def saw(f, n, det=0.0):
    t = np.arange(n) / SR
    return 2 * ((f * (1 + det) * t + rng.random()) % 1.0) - 1


def braam(n_sec=4.0):
    n = int(n_sec * SR)
    t = np.arange(n) / SR
    base = 24 + root + 12  # low register, octave 1-2
    notes = [base, base + 7, base + 12] if mode == "maj" else [base, base + 7, base + 12, base + 15]
    s = np.zeros(n)
    for m in notes:
        for d in (-0.006, -0.002, 0.002, 0.006):
            s += saw(mtof(m), n, d)
    s /= len(notes) * 4
    # filter blooms open then closes, like a brass section swelling
    out = np.zeros(n)
    blk = 1024
    for i in range(0, n, blk):
        x = i / SR
        f = 250 + 1700 * np.exp(-((x - 0.25) ** 2) / 0.35) + 200 * np.exp(-x)
        out[i:i + blk] = lp(s[i:i + blk], f)
    amp = np.minimum(1, t / 0.06) * np.exp(-t * 0.85)
    sub = np.sin(2 * np.pi * np.cumsum(mtof(base - 12) * (1 + 0.6 * np.exp(-t * 9))) / SR) * np.exp(-t * 1.1)
    return np.tanh(out * amp * 2.2) * 0.8 + sub * 0.9


def swell(n_sec=1.6):
    """Reverse-reverb swell built from the braam itself (a sucking-in rise, no noise)."""
    b = braam(n_sec)
    ir = rng.standard_normal(int(2.0 * SR)) * np.exp(-np.arange(int(2.0 * SR)) / SR * 2.0)
    wet = fftconvolve(b, ir)[: len(b)]
    wet = wet[::-1] / (np.abs(wet).max() + 1e-9)
    return wet * np.linspace(0, 1, len(wet)) ** 2


hits = np.zeros(N)
duck = np.ones(N)
for t, g in HITS:
    b = braam()
    i = int(t * SR)
    n = min(len(b), N - i)
    hits[i:i + n] += b[:n] * g
    sw = swell()
    j = max(0, i - len(sw))
    hits[j:i] += sw[len(sw) - (i - j):] * 0.35 * g
    k = np.arange(min(int(2.5 * SR), N - i))
    duck[i:i + len(k)] = np.minimum(duck[i:i + len(k)], 1 - 0.45 * np.exp(-k / SR * 1.4))

# long hall reverb on the hits only
ir_n = int(3.0 * SR)
ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 2.2)
ir = lp(ir, 5000)
hits_wet = fftconvolve(hits, ir)[:N]
hits_wet /= np.abs(hits_wet).max() + 1e-9
hits /= np.abs(hits).max() + 1e-9

mix = bed * duck * 0.62 + hits * 0.55 + hits_wet * 0.22
fade = np.ones(N)
fi = int(0.6 * SR)
fade[:fi] = np.linspace(0, 1, fi)
fo = int((DUR - 2.4) * SR)
fade[fo:] = np.linspace(1, 0, N - fo) ** 1.4
mix *= fade
mix = np.tanh(mix / np.percentile(np.abs(mix), 99.95) * 1.1) / np.tanh(1.1) * 0.9
st = np.stack([mix, np.roll(mix, 220) * 0.96 + mix * 0.04], axis=1)  # slight width
sf.write(out_path, st.astype(np.float32), SR)

# beat grid of the bed (for the subtle pulse); fall back to the hits alone
tempo, frames = librosa.beat.beat_track(y=librosa.resample(bed, orig_sr=SR, target_sr=22050), sr=22050)
tempo = float(np.atleast_1d(tempo)[0])
beats = [round(float(x), 3) for x in librosa.frames_to_time(frames, sr=22050)] if 60 <= tempo <= 150 else []
beats = sorted(set(beats + [t for t, _ in HITS]))
down = [beats.index(t) for t, _ in HITS]
json.dump({"beats": beats, "downbeats": down, "bpm": round(tempo, 1)}, open(beats_path, "w"))
print("tempo", round(tempo, 1), "beats", len(beats))
