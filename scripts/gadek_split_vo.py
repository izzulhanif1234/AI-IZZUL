"""Split one Gemini TTS take of the whole Gadek script into per-line clips with per-word timings.
usage: gadek_split_vo.py take.wav take.wx.json vo_lines.json outdir
Script words are aligned to the whisper words (difflib); words whisper wrote differently
(numbers, misspellings) get times interpolated between their matched neighbours. Each line is cut
at the quietest 20 ms inside the pause before the next line, then trimmed and loudness-normalised.
Writes outdir/<id>.wav and outdir/<id>.words.json ([{word, start, end}] relative to the clip)."""
import difflib, json, re, subprocess, sys
import numpy as np, soundfile as sf

take, wxf, linesf, out = sys.argv[1:5]
lines = json.load(open(linesf))
ww = json.load(open(wxf))
NUM = {"16": "enam", "2024": "dua", "30": "tiga", "25": "dua", "3": "tiga"}


def norm(w):
    w = re.sub(r"[^a-z0-9]", "", w.lower())
    return NUM.get(w, w)


toks = [(l["id"], t) for l in lines for t in l["text"].split()]
sm = difflib.SequenceMatcher(None, [norm(t) for _, t in toks], [norm(w["word"]) for w in ww], autojunk=False)
tim = [None] * len(toks)
for b in sm.get_matching_blocks():
    for k in range(b.size):
        tim[b.a + k] = [ww[b.b + k]["start"], ww[b.b + k]["end"]]
i = 0
while i < len(tim):
    if tim[i] is not None:
        i += 1
        continue
    j = i
    while j < len(tim) and tim[j] is None:
        j += 1
    t0 = tim[i - 1][1] if i > 0 else 0.0
    t1 = tim[j][0] if j < len(tim) else t0 + 0.4 * (j - i)
    step = (t1 - t0) / (j - i)
    for k in range(i, j):
        tim[k] = [t0 + step * (k - i), t0 + step * (k - i + 1)]
    i = j
print("matched", sum(1 for b in sm.get_matching_blocks() for _ in range(b.size)), "of", len(toks))

audio, sr = sf.read(take)
if audio.ndim > 1:
    audio = audio.mean(1)
ids = [l["id"] for l in lines]
first = {lid: next(k for k, (l, _) in enumerate(toks) if l == lid) for lid in ids}
last = {lid: max(k for k, (l, _) in enumerate(toks) if l == lid) for lid in ids}


def quietest(a, b):
    a, b = int(a * sr), int(b * sr)
    if b - a < int(0.02 * sr):
        return (a + b) / 2 / sr
    win = int(0.02 * sr)
    e = [np.sum(audio[x:x + win] ** 2) for x in range(a, b - win, win // 2)]
    return (a + int(np.argmin(e)) * (win // 2) + win // 2) / sr


cuts = [0.0]
for x, y in zip(ids, ids[1:]):
    cuts.append(quietest(tim[last[x]][1] - 0.05, tim[first[y]][0] + 0.05))
cuts.append(len(audio) / sr)

for n, lid in enumerate(ids):
    a, b = cuts[n], cuts[n + 1]
    raw = f"{out}/{lid}.raw.wav"
    sf.write(raw, audio[int(a * sr):int(b * sr)], sr)
    # trim edges; measure how much leading silence went so word times stay right
    lead = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", "silencedetect=n=-45dB:d=0.02", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    m = re.search(r"silence_start: (-?[\d.]+)\s*\n.*?silence_end: ([\d.]+)", lead, re.S)
    head = float(m.group(2)) if m and float(m.group(1)) <= 0.01 else 0.0
    head = max(0.0, head - 0.05)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(head), "-i", raw, "-af",
                    "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.12,areverse,"
                    "loudnorm=I=-16:TP=-1.5,aresample=48000", "-ar", "48000", f"{out}/{lid}.wav"], check=True)
    subprocess.run(["rm", raw])
    off = a + head
    words = [{"word": t, "start": round(tim[k][0] - off, 3), "end": round(tim[k][1] - off, 3)}
             for k, (l, t) in enumerate(toks) if l == lid]
    json.dump(words, open(f"{out}/{lid}.words.json", "w"), ensure_ascii=False)
    print(lid, round(a, 2), round(b, 2), "head", round(head, 2), words[0]["start"], words[-1]["end"])
