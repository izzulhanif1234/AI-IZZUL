"""Generate index.html for the MCORP EstiMATE film: scene mounts, VO, music bed with ducking, SFX."""
import json, subprocess, sys
sys.path.insert(0, "/home/user/AI-IZZUL/scripts")
from mcorp_timeline import VO, DIALOGUE, HF

TOTAL = 116.5
SCENES = [  # id, start, duration
    ("hook", 0.0, 12.4), ("title", 12.4, 3.8), ("team", 16.2, 5.4), ("actor", 21.6, 6.25),
    ("solution", 27.85, 8.05), ("how", 35.9, 11.7), ("demo", 47.6, 18.8), ("impact", 66.4, 14.6),
    ("testi", 81.0, 24.64), ("closing", 105.64, 10.86),
]
# (id, file, start, duration, volume) -- start = visual moment - file onset
SFX = [
    ("s-rise", "riser", 8.98, 3.6, 0.28),
    ("s-tag1", "pop", 0.24, 0.6, 0.35), ("s-tag2", "pop", 3.09, 0.6, 0.35), ("s-tag3", "pop", 5.84, 0.6, 0.35),
    ("s-days", "impact-bass-1", 8.85, 1.6, 0.55),
    ("s-err", "glitch-1", 10.45, 1.3, 0.3),
    ("s-flash", "whoosh", 12.12, 0.57, 0.45),
    ("s-title", "impact-bass-2", 12.43, 2.5, 0.6),
    ("s-shine", "sparkle", 13.68, 1.4, 0.35),
    ("s-team", "whoosh-short", 16.22, 0.57, 0.4),
    ("s-actor", "whoosh", 21.5, 0.57, 0.35),
    ("s-sol", "whoosh-short", 27.8, 0.57, 0.35),
    ("s-strike", "whoosh-short", 32.08, 0.57, 0.35),
    ("s-10min", "impact-bass-1", 34.15, 1.6, 0.55),
    ("s-how", "whoosh", 35.82, 0.57, 0.35),
    ("s-c1", "pop", 36.69, 0.6, 0.4), ("s-c2", "pop", 38.59, 0.6, 0.4), ("s-c3", "pop", 40.24, 0.6, 0.4), ("s-c4", "pop", 43.22, 0.6, 0.4),
    ("s-demo", "whoosh", 47.52, 0.57, 0.4),
    ("s-click1", "click", 49.56, 0.37, 0.6), ("s-type1", "typing", 49.25, 1.0, 0.35),
    ("s-click2", "click", 51.48, 0.37, 0.6), ("s-reply1", "ping", 51.33, 1.1, 0.35),
    ("s-type2a", "typing", 53.2, 1.5, 0.35), ("s-type2b", "typing", 54.7, 1.5, 0.35), ("s-type2c", "typing", 56.2, 1.55, 0.35),
    ("s-click3", "click", 58.16, 0.37, 0.6), ("s-reply2", "ping", 58.1, 1.1, 0.35),
    ("s-qty", "pop", 62.29, 0.6, 0.4), ("s-rate", "pop", 63.09, 0.6, 0.4), ("s-kont", "pop", 64.29, 0.6, 0.4),
    ("s-total", "chime", 64.49, 2.0, 0.4),
    ("s-impact", "whoosh", 66.32, 0.57, 0.4),
    ("s-n1", "chime", 70.0, 2.0, 0.35),
    ("s-swap", "whoosh-short", 71.9, 0.57, 0.35),
    ("s-n2", "chime", 76.3, 2.0, 0.35), ("s-n3", "chime", 78.9, 2.0, 0.35),
    ("s-testi", "whoosh", 80.92, 0.57, 0.4),
    ("s-close", "whoosh", 105.56, 0.57, 0.4),
    ("s-w1", "impact-bass-1", 108.07, 1.2, 0.4), ("s-w2", "impact-bass-1", 108.69, 1.2, 0.4), ("s-w3", "impact-bass-1", 109.46, 1.4, 0.45),
    ("s-end", "impact-bass-2", 111.52, 2.5, 0.5), ("s-endsp", "sparkle", 111.9, 1.6, 0.35),
]


def speech_intervals():
    iv = []
    for lid, at in VO.items():
        w = json.load(open(f"{HF}/assets/vo/{lid}.json"))
        iv.append((at + w[0]["start"], at + w[-1]["end"], "vo"))
    for clip, rs, ss, dur in DIALOGUE:
        iv.append((rs, rs + dur, "dlg"))
    return sorted(iv)


def duck_lane():
    BASE, VO_LVL, DLG_LVL, R = 0.6, 0.2, 0.1, 0.3
    pts = [(0.0, 0.0), (0.5, BASE)]
    for s, e, kind in speech_intervals():
        lvl = VO_LVL if kind == "vo" else DLG_LVL
        pts += [(s - R, BASE), (s, lvl), (e, lvl), (e + R + 0.2, BASE)]
    pts += [(TOTAL - 2.5, BASE), (TOTAL, 0.0)]
    # collapse overlaps: keep time order, and when two speech blocks are close, stay ducked
    pts.sort()
    out = []
    for t, v in pts:
        t = max(0.0, round(t, 3))
        if out and t <= out[-1][0]:
            out[-1] = (out[-1][0], min(out[-1][1], v))
        else:
            out.append((t, v))
    # a dip that recovers for less than 0.6s just stays ducked
    clean = [out[0]]
    for i in range(1, len(out)):
        clean.append(out[i])
    return {"version": 1, "lanes": [{"target": "volume", "points": [{"t": t, "v": v} for t, v in clean]}]}


def main():
    mounts = "\n".join(
        f'      <div id="m-{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
        f'data-start="{st}" data-duration="{du}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
        for i, (sid, st, du) in enumerate(SCENES))
    def dur(path):
        return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode())
    def speech_end(lid):
        return json.load(open(f"{HF}/assets/vo/{lid}.json"))[-1]["end"] + 0.35
    vo = "\n".join(
        f'      <audio id="vo-{lid}" src="assets/vo/{lid}.mp3" data-start="{at}" data-duration="{min(speech_end(lid), dur(f"{HF}/assets/vo/{lid}.mp3")):.3f}" data-track-index="{20 + n % 2}" data-volume="1" data-fade-out="0.15"></audio>'
        for n, (lid, at) in enumerate(VO.items()))
    ends, rows = [], []
    for (i, f, st, d, v) in sorted(SFX, key=lambda x: x[2]):
        d = min(d, dur(f"{HF}/assets/sfx/{f}.mp3"))
        k = next((k for k, e in enumerate(ends) if e <= st), None)
        if k is None:
            ends.append(0); k = len(ends) - 1
        ends[k] = st + d
        rows.append(f'      <audio id="{i}" src="assets/sfx/{f}.mp3" data-start="{st}" data-duration="{d:.3f}" data-track-index="{30 + k}" data-volume="{v}"></audio>')
    sfx = "\n".join(rows)
    lane = json.dumps(duck_lane(), separators=(",", ":"))
    html = f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="vendor/gsap.min.js"></script>
    <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #06112b;
      }}
      #root {{
        position: relative;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #06112b;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
      <!-- scenes (see edits/mcorp-estimate/NOTES.md for the storyboard) -->
{mounts}
      <!-- subtitles over everything -->
      <div id="m-captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-track-kind="captions" data-width="1920" data-height="1080"></div>

      <!-- voiceover: ms-MY Osman, script from MCORP EstiMATE 13.10.pdf -->
{vo}
      <!-- music bed, ducked under every VO line and dialogue cut -->
      <audio id="bgm" data-timeline-role="music" src="assets/bgm/bed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-automation='{lane}'></audio>
      <!-- sfx -->
{sfx}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    open(f"{HF}/index.html", "w").write(html)
    print("index.html written;", len(SCENES), "scenes,", len(SFX), "sfx")


if __name__ == "__main__":
    main()
