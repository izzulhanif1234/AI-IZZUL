"""Even out VO delivery without re-synthesis (v15).
1) Pauses: every silent run (< -42 dB, >= 0.12 s) is capped by the punctuation of the word before it
   ('.?!' 0.40 s, ',;:' 0.24 s, none 0.12 s); the excess is cut from the middle of the silence with a 15 ms crossfade.
   Only silence is removed, so the voice itself is untouched.
2) Pace: lines whose speaking rate (syllables per voiced second) is off the median get a gentle atempo, capped at -6% / +8%
   (larger stretches -- v12 went to 1.2x with rubberband -- made the voice sound robotic).
Word timings in vNN.json are remapped. usage: vo_even.py src_dir dst_dir script.json"""
import json, re, subprocess, sys
import numpy as np

SR = 48000
src, dst, sj = sys.argv[1:4]
script = {l["id"]: l["text"] for l in json.load(open(sj))}


def load(f):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(pcm, np.float32).astype(np.float64)


def save(y, f):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f64le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "libmp3lame", "-b:a", "192k", f],
                   input=y.astype(np.float64).tobytes(), check=True)


def syl(t):
    return len(re.findall(r"[aeiou]+", t.lower().replace("spd", "es pi di").replace("m-corp", "em kop")))


def db_frames(y):
    hop = SR // 100
    fr = y[: len(y) // hop * hop].reshape(-1, hop)
    return 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)


def cap_pauses(y, words):
    db = db_frames(y)
    q = db < -42
    runs, i = [], 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]:
                j += 1
            runs.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    first = np.argmax(~q) / 100
    last = (len(q) - np.argmax(~q[::-1])) / 100
    cuts = []  # (start, end) seconds to remove
    for a, b in runs:
        if a <= first or b >= last or b - a < 0.12:
            continue
        # word that ends nearest the start of this silence
        w = min(words, key=lambda w: abs(w["end"] - a)) if words else None
        p = w["word"][-1] if w and abs(w["end"] - a) < 0.35 else ""
        cap = 0.40 if p in ".?!" else 0.24 if p in ",;:" else 0.12
        if b - a > cap + 0.02:
            ex = (b - a) - cap
            m = (a + b) / 2
            cuts.append((m - ex / 2, m + ex / 2))
    # head / tail silence
    if first > 0.12:
        cuts.insert(0, (0.0, first - 0.10))
    if (len(y) / SR) - last > 0.30:
        cuts.append((last + 0.25, len(y) / SR))
    out, pos, xf = [], 0, int(0.015 * SR)
    for a, b in cuts:
        ia, ib = int(a * SR), int(b * SR)
        seg = y[pos:ia].copy()
        if out and len(seg) > xf and len(out[-1]) > xf:
            prev = out[-1]
            ramp = np.linspace(0, 1, xf)
            seg[:xf] = seg[:xf] * ramp + prev[-xf:] * (1 - ramp)
            out[-1] = prev[:-xf]
        out.append(seg)
        pos = ib
    out.append(y[pos:])

    def remap(t):
        sh = 0.0
        for a, b in cuts:
            if t >= b:
                sh += b - a
            elif t > a:
                sh += t - a
        return max(0.0, t - sh)
    return np.concatenate(out), remap, sum(b - a for a, b in cuts)


rates, stage = {}, {}
for v in script:
    y = load(f"{src}/{v}.mp3")
    W = json.load(open(f"{src}/{v}.json"))
    y2, remap, cut = cap_pauses(y, W)
    for w in W:
        w["start"], w["end"] = round(remap(w["start"]), 3), round(remap(w["end"]), 3)
    voiced = (db_frames(y2) > -40).sum() / 100
    rates[v] = syl(script[v]) / voiced
    stage[v] = (y2, W, len(y) / SR, cut)
med = float(np.median(list(rates.values())))
for v, (y2, W, d0, cut) in stage.items():
    f = min(1.08, max(0.94, med / rates[v]))
    if abs(f - 1) < 0.02:
        f = 1.0
    tmp = f"{dst}/{v}.mp3"
    save(y2, tmp)
    if f != 1.0:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"atempo={f:.4f}", "-ar", str(SR), "-c:a", "libmp3lame", "-b:a", "192k", tmp + ".t.mp3"], check=True)
        subprocess.run(["mv", tmp + ".t.mp3", tmp], check=True)
        for w in W:
            w["start"], w["end"] = round(w["start"] / f, 3), round(w["end"] / f, 3)
    json.dump(W, open(f"{dst}/{v}.json", "w"), ensure_ascii=False)
    print(f"{v:5} {d0:6.2f}s -> {len(y2) / SR / f:6.2f}s  (pauses -{cut:4.2f}s, rate {rates[v]:.2f} syl/s, tempo {f:.3f})")
