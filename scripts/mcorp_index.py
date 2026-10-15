"""Generate index.html for the MCORP EstiMATE film: scene mounts, VO, music bed with ducking, SFX."""
import json, subprocess, sys
sys.path.insert(0, "/home/user/AI-IZZUL/scripts")
from mcorp_timeline import VO, DIALOGUE, HF

TOTAL = 118.6
SCENES = [  # id, start, duration
    ("hook", 0.0, 12.35), ("title", 12.35, 3.4), ("team", 15.75, 4.45), ("actor", 20.2, 7.4),
    ("solution", 27.6, 7.95), ("how", 35.55, 12.05), ("demo", 47.6, 21.0), ("segmen", 68.6, 13.6),
    ("testi", 82.2, 26.98), ("closing", 109.18, 9.42),
]
# (id, file, start, duration, volume) -- start = visual moment - file onset
SFX = [
    ("s-rise", "riser", 8.88, 3.6, 0.28),
    ("s-tag1", "pop", 0.14, 0.6, 0.35), ("s-tag2", "pop", 2.06, 0.6, 0.35), ("s-tag3", "pop", 5.24, 0.6, 0.35),
    ("s-days", "impact-bass-1", 8.63, 1.6, 0.55),
    ("s-err", "glitch-1", 10.33, 1.3, 0.3),
    ("s-flash", "whoosh", 12.07, 0.57, 0.45),
    ("s-title", "impact-bass-2", 12.38, 2.5, 0.6),
    ("s-shine", "sparkle", 13.43, 1.4, 0.35),
    ("s-team", "whoosh-short", 15.67, 0.57, 0.4),
    ("s-actor", "whoosh", 20.12, 0.57, 0.35),
    ("s-sol", "whoosh-short", 27.52, 0.57, 0.35),
    ("s-strike", "whoosh-short", 31.52, 0.57, 0.35),
    ("s-10min", "impact-bass-1", 33.65, 1.6, 0.55),
    ("s-how", "whoosh", 35.47, 0.57, 0.35),
    ("s-c1", "pop", 36.94, 0.6, 0.4), ("s-c2", "pop", 38.39, 0.6, 0.4), ("s-c3", "pop", 40.17, 0.6, 0.4), ("s-c4", "pop", 43.34, 0.6, 0.4),
    ("s-demo", "whoosh", 47.52, 0.57, 0.4),
    ("s-type1", "typing", 49.35, 0.9, 0.35), ("s-click1", "click", 49.66, 0.37, 0.6),
    ("s-click2", "click", 51.76, 0.37, 0.6), ("s-reply1", "ping", 51.58, 1.1, 0.35),
    ("s-sortbl", "pop", 53.59, 0.6, 0.4),
    ("s-bq", "whoosh-short", 55.57, 0.57, 0.35),
    ("s-type2a", "typing", 55.45, 1.5, 0.35), ("s-type2b", "typing", 56.95, 1.5, 0.35), ("s-type2c", "typing", 58.45, 1.1, 0.35),
    ("s-click3", "click", 60.41, 0.37, 0.6), ("s-reply2", "ping", 60.33, 1.1, 0.35),
    ("s-qty", "pop", 63.69, 0.6, 0.4), ("s-rate", "pop", 64.34, 0.6, 0.4), ("s-kont", "pop", 65.69, 0.6, 0.4),
    ("s-total", "chime", 65.89, 2.0, 0.4),
    ("s-seg", "whoosh", 68.52, 0.57, 0.4),
    ("s-segq", "whoosh-short", 68.62, 0.57, 0.3),
    ("s-hub", "impact-bass-1", 70.35, 1.6, 0.55),
    ("s-lines", "whoosh-short", 71.62, 0.57, 0.35),
    ("s-g1", "pop", 74.29, 0.6, 0.45), ("s-g2", "pop", 76.18, 0.6, 0.45),
    ("s-g3", "pop", 77.64, 0.6, 0.45), ("s-g4", "pop", 79.44, 0.6, 0.45),
    ("s-segend", "chime", 80.39, 2.0, 0.35),
    ("s-testi", "whoosh", 82.12, 0.57, 0.4),
    ("s-close", "whoosh", 109.1, 0.57, 0.4),
    ("s-w1", "impact-bass-1", 110.49, 1.2, 0.4), ("s-w2", "impact-bass-1", 111.23, 1.2, 0.4), ("s-w3", "impact-bass-1", 112.05, 1.4, 0.45),
    ("s-end", "impact-bass-2", 113.01, 2.5, 0.5), ("s-endsp", "sparkle", 113.3, 1.6, 0.35),
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
      <!-- small 3D-swinging logo badge, top right, whole film -->
      <div id="m-badge" data-composition-id="badge" data-composition-src="compositions/badge.html" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
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
