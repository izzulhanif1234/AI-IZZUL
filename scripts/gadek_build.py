"""Gadek Hotspring corporate video: writes edits/gadek-hotspring/hf/index.html.
Single source of timings: SHOTS (footage), PHOTOS, VO, SFX below.
Graphics live in hf/compositions/fx.html (hand-written; its times match this file).
usage: python3 scripts/gadek_build.py"""
import difflib, html as htmllib, json, os, re, subprocess

HF = os.path.join(os.path.dirname(__file__), "..", "edits", "gadek-hotspring", "hf")
TOTAL = 125.0
GRADES = json.load(open(os.path.join(HF, "..", "grades.json")))  # from `hyperframes media-treatment`
XF = 0.5  # crossfade length between consecutive shots

# (cut-in time, clip, media start, css filter) ; each shot runs to the next cut (+XF overlap)
SHOTS = [
    (0.0, "d0392", 36.0, ""),            # sky, village, hills
    (6.2, "d0388", 0.5, ""),             # KOMPLEKS AIR PANAS GADEK gate, pull back
    (12.6, "d0382", 1.0, ""),            # wide aerial of the complex (title)
    (19.2, "d0392", 42.0, "vintage"),  # history, village
    (25.0, "d0386", 2.0, "vintage"),   # Geotapak sign
    (29.8, "d0385", 2.0, ""),            # pool, colour returns at "selepas merdeka"
    (34.8, "d0389", 10.0, ""),           # chalets, greenery
    (40.0, "d0388", 8.0, ""),            # rising reveal (Kini)
    (45.6, "d0387", 14.0, ""),           # concourse with visitors
    (51.4, "d0385", 8.0, ""),            # hot spring pool
    (57.3, "d0385", 11.5, ""),
    (63.2, "d0392", 1.0, ""),            # kids pool push-in
    (68.8, "d0383", 10.0, ""),           # kids pool orbit
    (73.5, "d0389", 4.0, ""),            # chalets with private pools
    (84.4, None, "pool2", ""),           # photo
    (87.2, None, "pool4", ""),           # photo
    (90.2, "d0387", 2.0, ""),            # concourse / vendors
    (94.3, "d0392", 20.0, ""),           # hall building
    (96.6, "d0391", 4.0, ""),            # cafe
    (98.6, "d0382", 7.0, ""),            # parking
    (101.6, "d0388", 13.0, ""),          # wide: complex and main road
    (112.2, "d0389", 19.0, ""),          # fly-over to the kids pool
    (117.6, "d0383", 12.5, "endblur"),  # end-card background
]

# VO line -> start time on the EDIT timeline (laid out against the Edge TTS guide takes in
# assets/vo_edge). The final VO (Gemini "Charon", assets/vo/*.wav + whisper word timings *.wx.json)
# has its own pacing, so every edit time below (cuts, SFX, graphics) goes through warp(): a
# piecewise-linear map through the start of every word the two takes share.
VO = {"v01": 1.5, "v02": 13.6, "v03": 20.0, "v04": 30.0, "v05": 40.3, "v06": 51.8, "v07": 63.4,
      "v08": 74.0, "v09": 84.6, "v10": 90.0, "v11": 101.9, "v12": 112.6, "v13": 117.8}

SFX = [  # (time, file, volume)
    (0.1, "whoosh-cinematic.mp3", 0.25),
    (12.7, "whoosh-cinematic.mp3", 0.35), (13.15, "impact-bass-2.mp3", 0.45), (13.4, "sparkle.mp3", 0.3),
    (20.1, "whoosh-short.mp3", 0.25), (30.3, "whoosh-short.mp3", 0.25), (40.4, "whoosh-short.mp3", 0.25),
    (44.0, "pop.mp3", 0.3), (48.2, "pop.mp3", 0.3),
    (51.9, "whoosh-short.mp3", 0.25), (55.0, "pop.mp3", 0.25), (57.4, "pop.mp3", 0.25), (59.6, "pop.mp3", 0.25),
    (63.5, "whoosh-short.mp3", 0.25), (66.3, "pop.mp3", 0.25), (68.8, "pop.mp3", 0.25), (71.0, "pop.mp3", 0.25),
    (74.1, "whoosh-short.mp3", 0.25),
    (78.45, "whoosh-short.mp3", 0.25), (79.2, "whoosh-short.mp3", 0.22), (80.45, "whoosh-short.mp3", 0.22), (81.0, "whoosh-short.mp3", 0.22),
    (90.1, "whoosh-short.mp3", 0.25), (93.6, "pop.mp3", 0.25), (94.4, "pop.mp3", 0.25), (96.7, "pop.mp3", 0.25),
    (97.5, "pop.mp3", 0.25), (98.7, "pop.mp3", 0.25),
    (102.0, "whoosh-short.mp3", 0.25), (102.6, "ping.mp3", 0.25), (106.4, "whoosh-short.mp3", 0.25),
    (112.7, "whoosh-cinematic.mp3", 0.25), (117.6, "whoosh.mp3", 0.35), (117.9, "chime.mp3", 0.3),
]


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode())


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def build_warp():
    """returns (anchors [(edit_t, film_t)], {line: (film_start, film_speech_end, file_dur)})"""
    anchors, lines = [], {}
    ids = sorted(VO, key=VO.get)
    prev_old_end = prev_new_end = None
    for k in ids:
        old_s = VO[k]
        ew = json.load(open(f"{HF}/assets/vo_edge/{k}.json"))
        gw = json.load(open(f"{HF}/assets/vo/{k}.wx.json"))
        old_e = old_s + ew[-1]["end"]
        if prev_old_end is None:
            new_s = old_s
        else:
            new_s = prev_new_end + max(0.45, old_s - prev_old_end)
        gdur = dur(f"{HF}/assets/vo/{k}.wav")
        new_e = new_s + gdur
        anchors.append((old_s, new_s))
        sm = difflib.SequenceMatcher(None, [norm(w["word"]) for w in ew], [norm(w["word"]) for w in gw], autojunk=False)
        for blk in sm.get_matching_blocks():
            for i in range(blk.size):
                a_t = old_s + ew[blk.a + i]["start"]
                b_t = new_s + gw[blk.b + i]["start"]
                if a_t > anchors[-1][0] + 0.05 and b_t > anchors[-1][1] + 0.05:
                    anchors.append((a_t, b_t))
        anchors.append((old_e, new_e))
        lines[k] = (round(new_s, 3), round(new_e, 3), gdur)
        prev_old_end, prev_new_end = old_e, new_e
    return anchors, lines


def warp(t, A):
    if t <= A[0][0]:
        return t + A[0][1] - A[0][0]
    for (a0, b0), (a1, b1) in zip(A, A[1:]):
        if t <= a1:
            return b0 + (t - a0) * (b1 - b0) / (a1 - a0)
    return t + A[-1][1] - A[-1][0]


def music_automation(vb, TOTAL):
    hi, lo = 0.55, 0.16
    iv = sorted((s - 0.3, e + 0.3) for s, e, _ in vb.values())
    merged = [list(iv[0])]
    for s, e in iv[1:]:
        if s - merged[-1][1] < 2.0:  # short gaps stay ducked
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    pts = [(0, 0), (0.6, hi)]
    for s, e in merged:
        pts += [(s, hi), (s + 0.3, lo), (e, lo), (e + 0.6, hi)]
    pts += [(TOTAL - 2.5, hi), (TOTAL, 0)]
    return {"version": 1, "lanes": [{"target": "volume", "points": [{"t": round(t, 3), "v": v} for t, v in pts]}]}


def main():
    A, vb = build_warp()
    total = round(warp(TOTAL, A), 2)
    W = lambda t: round(warp(t, A), 3)
    clips, tl = [], []
    for i, (t, clip, ms, flt) in enumerate(SHOTS):
        t = W(t)
        end = W(SHOTS[i + 1][0]) + XF if i + 1 < len(SHOTS) else total
        d = round(end - t, 3)
        fade = "" if i == 0 else f' data-fade-in="{XF}"'
        style = ""  # grades go on the media element (data-color-grading); CSS filters are not rendered
        grade = f' data-color-grading="{htmllib.escape(json.dumps(GRADES[flt], separators=(",", ":")), quote=True)}"' if flt else ""
        if clip:
            clips.append(
                f'      <div id="w{i:02d}" class="vw" data-layout-allow-overflow{style}><video id="v{i:02d}"{grade} class="clip" '
                f'data-hf-media-start-basis="local" src="assets/video/{clip}.mp4" data-start="{t}" data-duration="{d}" '
                f'data-media-start="{ms}" data-track-index="{i % 2}"{fade} muted playsinline></video></div>')
        else:
            clips.append(
                f'      <div id="w{i:02d}" class="vw" data-layout-allow-overflow{style}><img id="v{i:02d}" class="clip" '
                f'src="assets/img/{ms}.jpg" data-start="{t}" data-duration="{d}" data-track-index="{i % 2}"{fade} /></div>')
        # slow drift on every shot; photos get a stronger Ken Burns
        s0, s1 = (1.0, 1.06) if clip else (1.04, 1.16)
        tl.append(f'        tl.fromTo("#w{i:02d}", {{ scale: {s0} }}, {{ scale: {s1}, duration: {d}, ease: "none", immediateRender: false }}, {t});')

    audio = []
    for n, (k, (s, e, d)) in enumerate(vb.items()):
        audio.append(f'      <audio id="a{k}" src="assets/vo/{k}.wav" data-start="{s}" data-duration="{round(d, 3)}" data-track-index="{20 + n % 2}" data-volume="1"></audio>')
    for j, (t, f, v) in enumerate(SFX):
        t = W(t)
        d = dur(f"{HF}/assets/sfx/{f}")
        audio.append(f'      <audio id="s{j:02d}" src="assets/sfx/{f}" data-start="{t}" data-duration="{round(d, 3)}" data-track-index="{30 + j % 4}" data-volume="{v}"></audio>')
    auto = json.dumps(music_automation(vb, total))

    html = f'''<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #050b14; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #050b14; }}
      .vw {{ position: absolute; inset: 0; overflow: hidden; }}
      .vw video, .vw img {{ position: absolute; inset: 0; width: 1920px; height: 1080px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
      <!-- footage and photos (see edits/gadek-hotspring/NOTES.md) -->
{chr(10).join(clips)}
      <div id="m-fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <audio id="bgm" data-timeline-role="music" src="assets/bgm/bed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-automation='{auto}'></audio>
{chr(10).join(audio)}
    </div>
    <script>
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
        window.__timelines = window.__timelines || {{}};
        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
'''
    html = html.replace(f'data-duration="{TOTAL}"', f'data-duration="{total}"')
    open(f"{HF}/index.html", "w").write(html)
    tpl = open(f"{HF}/../fx.tpl.html").read()
    fx = tpl.replace("/*ANCHORS*/[]", json.dumps([[round(a, 3), round(b, 3)] for a, b in A]))
    open(f"{HF}/compositions/fx.html", "w").write(fx)
    print("total", total)
    for k, (s, e, _) in vb.items():
        print(k, round(s, 2), round(e, 2))


if __name__ == "__main__":
    main()
