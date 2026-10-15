"""Remove a sweeping (wail) siren from speech: track its narrowband fundamental in the STFT with a
continuity-constrained peak search, then notch that bin (and its 2nd/3rd harmonics) only while the
track is present. usage: remove_siren.py in.wav out.wav [t0 t1]"""
import sys
import numpy as np
import soundfile as sf
from scipy.signal import stft, istft

x, sr = sf.read(sys.argv[1])
mono = x.mean(axis=1) if x.ndim > 1 else x
NPER, HOP = 4096, 512
f, t, Z = stft(mono, fs=sr, nperseg=NPER, noverlap=NPER - HOP)
A = np.abs(Z) + 1e-9
df = f[1] - f[0]
lo, hi = np.searchsorted(f, 550), np.searchsorted(f, 1900)
t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
t1 = float(sys.argv[4]) if len(sys.argv) > 4 else t[-1]

# continuity-constrained track (max ~250 Hz per 0.1 s)
max_jump = int(round((250 * HOP / sr / 0.1) / df)) + 2
track = np.zeros(len(t), int)
prom = np.zeros(len(t))
prev = None
for i in range(len(t)):
    col = A[lo:hi, i]
    if prev is None:
        k = int(np.argmax(col))
    else:
        a, b = max(0, prev - max_jump), min(len(col), prev + max_jump + 1)
        k = a + int(np.argmax(col[a:b]))
        if col[k] < 0.25 * col.max():  # lost it: re-acquire globally
            k = int(np.argmax(col))
    prev = k
    track[i] = lo + k
    prom[i] = 20 * np.log10(col[k] / np.median(col))

# siren present = prominent AND smoothly moving for >= 0.35 s
smooth = np.abs(np.diff(f[track], prepend=f[track[0]])) < 160
cand = (prom > 12) & smooth & (t >= t0) & (t <= t1)
need = int(0.35 / (HOP / sr))
on = np.zeros_like(cand)
run = 0
for i, c in enumerate(cand):
    run = run + 1 if c else 0
    if run >= need:
        on[i - run + 1:i + 1] = True
# bridge short gaps (< 0.15 s) inside a siren
gap = int(0.4 / (HOP / sr))
idx = np.where(on)[0]
for a, b in zip(idx, idx[1:]):
    if 1 < b - a <= gap:
        on[a:b] = True

G = np.ones_like(A)
W = 4  # +-4 bins (~47 Hz) around each harmonic
for i in np.where(on)[0]:
    f0 = f[track[i]]
    for h, depth in ((1, 0.015), (2, 0.03), (3, 0.08), (4, 0.2)):
        c = int(round(h * f0 / df))
        if c + W < len(f):
            G[c - W:c + W + 1, i] = np.minimum(G[c - W:c + W + 1, i], depth)
# smooth the gain over time so the notch never clicks
from scipy.ndimage import uniform_filter1d
G = uniform_filter1d(G, size=5, axis=1)

out = []
chans = x.T if x.ndim > 1 else [x]
for ch in chans:
    _, _, Zc = stft(ch, fs=sr, nperseg=NPER, noverlap=NPER - HOP)
    _, y = istft(Zc * G, fs=sr, nperseg=NPER, noverlap=NPER - HOP)
    out.append(y[:len(ch)])
y = np.stack(out, axis=1) if x.ndim > 1 else out[0]
sf.write(sys.argv[2], y, sr)
secs = on.sum() * HOP / sr
print(f"siren frames: {on.sum()} ({secs:.1f}s)")
runs = np.flatnonzero(np.diff(np.concatenate([[0], on.astype(int), [0]])))
for a, b in zip(runs[::2], runs[1::2]):
    print(f"  {t[a]:6.2f}-{t[b-1]:6.2f}s  f0 {f[track[a]]:.0f}->{f[track[b-1]]:.0f} Hz")
