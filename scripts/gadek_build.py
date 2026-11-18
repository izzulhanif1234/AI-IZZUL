"""Gadek Hotspring corporate video: writes edits/gadek-hotspring/hf/index.html and
hf/compositions/fx.html (from edits/gadek-hotspring/fx.tpl.html), plus hf/../cues.json.

Every time in the film is a cue tied to the voice-over: the VO lines are laid end to end with the
pauses in GAPS, and cuts, SFX and graphics hang off a line's start/end or the start of one of its
script words (word timings in hf/assets/vo/<id>.words.json, from scripts/gadek_split_vo.py).
usage: python3 scripts/gadek_build.py"""
import html as htmllib, json, os, subprocess

HF = os.path.join(os.path.dirname(__file__), "..", "edits", "gadek-hotspring", "hf")
GRADES = json.load(open(os.path.join(HF, "..", "grades.json")))  # from `hyperframes media-treatment`
XF = 0.5  # crossfade length between consecutive shots
START = 1.5  # first VO line
TAIL = 3.2  # end card holds this long after the last line
# pause before each line (after the previous line ends)
GAPS = {"v02": 1.3, "v03": 1.7, "v04": 0.9, "v05": 1.2, "v06": 1.2, "v07": 1.1, "v08": 1.1, "v09": 0.8,
        "v10": 1.1, "v11": 1.0, "v12": 1.4, "v13": 0.6}
IDS = ["v01", "v02", "v03", "v04", "v05", "v06", "v07", "v08", "v09", "v10", "v11", "v12", "v13"]


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode())


def layout():
    vb, words, t = {}, {}, START
    for k in IDS:
        t += GAPS.get(k, 0)
        d = dur(f"{HF}/assets/vo/{k}.wav")
        vb[k] = (round(t, 3), round(t + d, 3), d)
        words[k] = json.load(open(f"{HF}/assets/vo/{k}.words.json"))
        t += d
    return vb, words, round(t + TAIL, 2)


VB, WORDS, TOTAL = layout()


def L(k, off=0.0):
    return round(VB[k][0] + off, 3)


def E(k, off=0.0):
    return round(VB[k][1] + off, 3)


def Wd(k, word, off=0.0, nth=1):
    """film time of the nth script word in line k that starts with `word` (case-insensitive)"""
    hits = [w for w in WORDS[k] if w["word"].lower().strip(".,?!").startswith(word.lower())]
    return round(VB[k][0] + max(0.0, hits[nth - 1]["start"]) + off, 3)


# graphics cues (fx.tpl.html reads them as C.<name>)
CUES = {
    "loc_in": Wd("v01", "Alor", -0.4), "loc_out": E("v01", 0.5),
    "ttl_in": L("v02", -0.5), "ttl_out": L("v03", -1.1),
    "bug_in": L("v03", -0.4), "bug_out": L("v13", -0.6),
    "c1_in": L("v03", 0.2), "c1_out": E("v03", 0.1),
    "c1b_in": L("v04", 0.3), "c1b_out": E("v04", 0.3),
    "c2_in": L("v05", 0.2), "c2_out": E("v05", 0.3),
    "st1": Wd("v05", "enam"), "st2": Wd("v05", "tiga", nth=1),
    "c3_in": L("v06", 0.2), "c3_out": E("v06", 0.3),
    "c3_p": [Wd("v06", "otot"), Wd("v06", "peredaran"), Wd("v06", "menenangkan")],
    "c4_in": L("v07", 0.2), "c4_out": E("v07", 0.3),
    "c4_p": [Wd("v07", "suam"), Wd("v07", "cetek"), Wd("v07", "selamat")],
    "c5_in": L("v08", 0.15), "c5_out": Wd("v08", "Pilih", -0.5),
    "rooms_in": Wd("v08", "Pilih", -0.3),
    "rooms_c": [Wd("v08", "bilik"), Wd("v08", "selesa"), Wd("v08", "chalet"), Wd("v08", "khas")],
    "rooms_out": L("v09", -0.5),
    "c5b_in": L("v09", 0.1), "c5b_out": L("v10", -0.6),
    "c6_in": L("v10", 0.2), "c6_out": E("v10", 0.3),
    "c6_p": [Wd("v10", "vendor"), Wd("v10", "dewan"), Wd("v10", "kafe"), Wd("v10", "surau"), Wd("v10", "parkir")],
    "c7_in": L("v11", 0.2), "c7_out": E("v11", 0.3),
    "pin": Wd("v11", "dua"), "hours": Wd("v11", "Kolam", -0.2),
    "tag1": Wd("v12", "Rehatkan", -0.1), "tag2": Wd("v12", "tenangkan", -0.1), "tag_out": L("v13", -0.6),
    "end_in": L("v13", -0.4), "black_out": round(TOTAL - 0.9, 2),
}

# (cut time, clip, media start, grade) ; each shot runs to the next cut (+XF overlap)
SHOTS = [
    (0.0, "d0392", 36.0, ""),                          # sky, village, hills
    (Wd("v01", "Tapi", -0.2), "d0388", 0.5, ""),       # "tapi di sini": the gate
    (L("v02", -0.9), "d0382", 1.0, ""),                # wide aerial (title)
    (L("v03", -0.9), "d0392", 42.0, "vintage"),        # history: village
    (Wd("v03", "pegawai", -0.3), "d0386", 2.0, "vintage"),  # Geotapak sign
    (L("v04", -0.2), "d0385", 2.0, ""),                # colour returns at "selepas merdeka"
    (Wd("v04", "Ia", -0.2), "d0389", 10.0, ""),        # chalets, greenery
    (L("v05", -0.4), "d0388", 8.0, ""),                # rising reveal (hari ini)
    (Wd("v05", "Sejak", -0.2), "d0387", 14.0, ""),     # concourse with visitors
    (L("v06", -0.4), "d0385", 8.0, ""),                # hot spring pool
    (Wd("v06", "melancarkan", -0.2), "d0385", 11.5, ""),
    (L("v07", -0.4), "d0392", 1.0, ""),                # kids pool push-in
    (Wd("v07", "Kolam", -0.2), "d0383", 10.0, ""),     # kids pool orbit
    (L("v08", -0.5), "d0389", 4.0, ""),                # chalets with private pools (room grid over it)
    (L("v09", -0.6), None, "pool2", ""),               # photo
    (Wd("v09", "bangun", -0.2), None, "pool4", ""),    # photo
    (L("v10", -0.5), "d0387", 2.0, ""),                # concourse / vendors
    (Wd("v10", "dewan", -0.2), "d0392", 20.0, ""),     # hall building
    (Wd("v10", "kafe", -0.2), "d0391", 4.0, ""),       # cafe
    (Wd("v10", "ruang", -0.2), "d0382", 7.0, ""),      # parking
    (L("v11", -0.5), "d0388", 13.0, ""),               # wide: complex and main road
    (L("v12", -0.7), "d0389", 19.0, ""),               # fly-over to the kids pool
    (L("v13", -0.4), "d0383", 12.5, "endblur"),        # end-card background
]

C = CUES
SFX = [  # (time, file, volume)
    (0.1, "whoosh-cinematic.mp3", 0.25), (SHOTS[1][0], "whoosh-short.mp3", 0.2),
    (C["ttl_in"] - 0.4, "whoosh-cinematic.mp3", 0.35), (C["ttl_in"] + 0.05, "impact-bass-2.mp3", 0.45), (C["ttl_in"] + 0.3, "sparkle.mp3", 0.3),
    (C["c1_in"] - 0.1, "whoosh-short.mp3", 0.25), (C["c1b_in"] - 0.1, "whoosh-short.mp3", 0.25), (C["c2_in"] - 0.1, "whoosh-short.mp3", 0.25),
    (C["st1"], "pop.mp3", 0.3), (C["st2"], "pop.mp3", 0.3),
    (C["c3_in"] - 0.1, "whoosh-short.mp3", 0.25), *[(t, "pop.mp3", 0.25) for t in C["c3_p"]],
    (C["c4_in"] - 0.1, "whoosh-short.mp3", 0.25), *[(t, "pop.mp3", 0.25) for t in C["c4_p"]],
    (C["c5_in"] - 0.1, "whoosh-short.mp3", 0.25), *[(t, "whoosh-short.mp3", 0.22) for t in C["rooms_c"]],
    (C["c6_in"] - 0.1, "whoosh-short.mp3", 0.25), *[(t, "pop.mp3", 0.25) for t in C["c6_p"]],
    (C["c7_in"] - 0.1, "whoosh-short.mp3", 0.25), (C["pin"], "ping.mp3", 0.25), (C["hours"], "whoosh-short.mp3", 0.25),
    (C["tag1"] - 0.3, "whoosh-cinematic.mp3", 0.25), (C["end_in"], "whoosh.mp3", 0.35), (C["end_in"] + 0.3, "chime.mp3", 0.3),
]


def media_len(clip, cache={}):
    if clip not in cache:
        cache[clip] = dur(f"{HF}/assets/video/{clip}.mp4")
    return cache[clip]


def music_automation(vb, total):
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
    pts += [(total - 2.5, hi), (total, 0)]
    return {"version": 1, "lanes": [{"target": "volume", "points": [{"t": round(t, 3), "v": v} for t, v in pts]}]}


def main():
    clips, tl, shots_out = [], [], []
    for i, (t, clip, ms, grd) in enumerate(SHOTS):
        end = SHOTS[i + 1][0] + XF if i + 1 < len(SHOTS) else TOTAL
        d = round(end - t, 3)
        if clip and ms + d > media_len(clip) - 0.05:  # never run past the end of the footage
            ms = round(max(0.0, media_len(clip) - 0.05 - d), 2)
        shots_out.append({"t": t, "end": round(end, 3), "clip": clip or ms, "ms": ms})
        fade = "" if i == 0 else f' data-fade-in="{XF}"'
        grade = f' data-color-grading="{htmllib.escape(json.dumps(GRADES[grd], separators=(",", ":")), quote=True)}"' if grd else ""
        if clip:
            clips.append(
                f'      <div id="w{i:02d}" class="vw" data-layout-allow-overflow><video id="v{i:02d}"{grade} class="clip" '
                f'data-hf-media-start-basis="local" src="assets/video/{clip}.mp4" data-start="{t}" data-duration="{d}" '
                f'data-media-start="{ms}" data-track-index="{i % 2}"{fade} muted playsinline></video></div>')
        else:
            clips.append(
                f'      <div id="w{i:02d}" class="vw" data-layout-allow-overflow><img id="v{i:02d}" class="clip" '
                f'src="assets/img/{ms}.jpg" data-start="{t}" data-duration="{d}" data-track-index="{i % 2}"{fade} /></div>')
        s0, s1 = (1.0, 1.06) if clip else (1.04, 1.16)  # slow drift; photos get a stronger Ken Burns
        tl.append(f'        tl.fromTo("#w{i:02d}", {{ scale: {s0} }}, {{ scale: {s1}, duration: {d}, ease: "none", immediateRender: false }}, {t});')

    audio = []
    for n, (k, (s, e, d)) in enumerate(VB.items()):
        audio.append(f'      <audio id="a{k}" src="assets/vo/{k}.wav" data-start="{s}" data-duration="{round(d, 3)}" data-track-index="{20 + n % 2}" data-volume="1"></audio>')
    for j, (t, f, v) in enumerate(sorted(SFX)):
        audio.append(f'      <audio id="s{j:02d}" src="assets/sfx/{f}" data-start="{round(t, 3)}" data-duration="{round(dur(f"{HF}/assets/sfx/{f}"), 3)}" data-track-index="{30 + j % 4}" data-volume="{v}"></audio>')
    auto = json.dumps(music_automation(VB, TOTAL))

    page = f'''<!doctype html>
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
    open(f"{HF}/index.html", "w").write(page)
    tpl = open(f"{HF}/../fx.tpl.html").read()
    open(f"{HF}/compositions/fx.html", "w").write(tpl.replace("/*CUES*/{}", json.dumps(CUES)))
    json.dump({"total": TOTAL, "vo": VB, "cues": CUES, "shots": shots_out}, open(f"{HF}/../cues.json", "w"), indent=1)
    print("total", TOTAL)
    for k, (s, e, _) in VB.items():
        print(k, s, e)


if __name__ == "__main__":
    main()
