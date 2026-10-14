"""Split one long TTS take into per-line clips, cutting in the quietest point of each pause,
and map script tokens onto whisper word timings (for captions).
usage: split_vo.py take.wav whisper.json order.json script_dir outdir"""
import difflib, json, re, subprocess, sys, wave
import numpy as np

take, wj, orderf, sdir, out = sys.argv[1:6]
order = json.load(open(orderf))
script = {l["id"]: l["text"] for f in ("script.json", "team.json", "close.json") for l in json.load(open(f"{sdir}/{f}"))}
NUM = {"seratus": "100", "sepuluh": "10"}


def norm(w):
    w = w.lower().replace("m-corp", "mcorp").replace("s-o-r", "sor")
    return re.sub(r"[^a-z0-9]", "", NUM.get(re.sub(r"[^a-z-]", "", w), w))


# whisper words
ww = [w for s in json.load(open(wj))["segments"] for w in s["words"]]
# script tokens, tagged by line
toks = [(lid, t) for lid in order for t in script[lid].split()]
a = [norm(t) for _, t in toks]
b = [norm(w["word"]) for w in ww]
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
tim = [None] * len(toks)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        tim[blk.a + k] = (ww[blk.b + k]["start"], ww[blk.b + k]["end"])
# spread each run of unmatched tokens ("tujuh puluh tiga ribu" vs whisper "RM73,000") evenly
# across the gap between its matched neighbours
i = 0
while i < len(tim):
    if tim[i] is not None:
        i += 1; continue
    j = i
    while j < len(tim) and tim[j] is None:
        j += 1
    t0 = tim[i - 1][1] if i > 0 else 0.0
    t1 = tim[j][0] if j < len(tim) else t0 + 0.4 * (j - i)
    t1 = max(t1, t0 + 0.1 * (j - i))
    step = (t1 - t0) / (j - i)
    for k in range(i, j):
        tim[k] = (t0 + step * (k - i), t0 + step * (k - i + 1))
    i = j

# audio energy at 10 ms for gap search
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", take, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32)
hop = 160
env = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)]) + 1e-6
db = 20 * np.log10(env / 32768)
total = len(x) / 16000


def quietest(t0, t1):
    i0, i1 = int(t0 * 100), max(int(t0 * 100) + 1, int(t1 * 100))
    seg = db[i0:i1]
    return (i0 + int(np.argmin(seg))) / 100, float(seg.min())


def speech_edge(t, direction, thr=-45):
    """Walk from t until the level drops under thr: true start (direction -1) / end (+1) of speech."""
    i = int(t * 100)
    while 0 < i < len(db) - 1 and db[i] > thr:
        i += direction
    return i / 100


bounds = {}
for lid in order:
    idx = [i for i, (l, _) in enumerate(toks) if l == lid]
    bounds[lid] = (tim[idx[0]][0], tim[idx[-1]][1], idx)

cuts = [0.0]
for k in range(len(order) - 1):
    e = bounds[order[k]][1]
    s = bounds[order[k + 1]][0]
    lo, hi = min(e, s) - 0.15, max(e, s) + 0.15
    c, lvl = quietest(lo, hi)
    cuts.append(c)
    print(f"cut {order[k]}|{order[k+1]} at {c:.2f}s  level {lvl:.1f} dB  (gap {s - e:+.2f}s)")
cuts.append(total)

import os
os.makedirs(out, exist_ok=True)
for k, lid in enumerate(order):
    c0, c1 = cuts[k], cuts[k + 1]
    # trim leading/trailing silence but keep 60 ms / 250 ms of air
    s0 = max(c0, speech_edge(bounds[lid][0] + 0.02, -1) - 0.06)
    s1 = min(c1, speech_edge(bounds[lid][1] - 0.02, +1) + 0.25)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", take, "-ss", f"{s0:.3f}", "-to", f"{s1:.3f}",
                    "-af", "afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse",
                    "-ar", "48000", "-ac", "1", "-b:a", "192k", f"{out}/{lid}.mp3"], check=True)
    words = [{"start": round(tim[i][0] - s0, 3), "end": round(tim[i][1] - s0, 3), "word": toks[i][1]} for i in bounds[lid][2]]
    words[0]["start"] = max(0.0, words[0]["start"])
    json.dump(words, open(f"{out}/{lid}.json", "w"), ensure_ascii=False)
    print(f"{lid}: {s0:6.2f}-{s1:6.2f}  len {s1 - s0:5.2f}s  speech {words[-1]['end'] - words[0]['start']:5.2f}s")
