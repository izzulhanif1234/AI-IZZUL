"""Gadek Hotspring corporate video (v3, no voice-over, cut to the music): writes
edits/gadek-hotspring/hf/index.html, hf/compositions/fx.html (from ../fx.tpl.html) and ../cues.json.

Every time is snapped to the beat grid of the music (beats.json, librosa on "Dreaming Big", 136 BPM).
Only steady stretches of the drone footage are used: per-second camera speed/jerk was measured
(phase correlation) and the take-off/adjusting parts and the shot with the operator are left out.
usage: python3 scripts/gadek_build.py"""
import html as htmllib, json, os, subprocess

HF = os.path.join(os.path.dirname(__file__), "..", "edits", "gadek-hotspring", "hf")
GRADES = json.load(open(os.path.join(HF, "..", "grades.json")))  # from `hyperframes media-treatment`
BEATS = json.load(open(os.path.join(HF, "..", "beats.json")))
MUSIC = "assets/bgm/dreaming-big.mp3"
XF = 0.5  # crossfade length between consecutive shots
TOTAL = 109.5


def B(t):
    """nearest beat to t"""
    return round(min(BEATS, key=lambda b: abs(b - t)), 3)


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode())


# (cut time, clip, media start, grade); every shot is inside a measured steady stretch
SHOTS = [
    (0.0, "d0392", 29.5, ""),             # village & hills, slow drift
    (B(6.7), "d0388", 7.0, ""),           # rising reveal of the complex
    (B(12.0), "d0382", 2.0, ""),          # wide aerial (title)
    (B(19.5), "d0386", 11.5, "vintage"),  # Geotapak sign, history
    (B(26.5), "d0389", 0.5, ""),          # chalets & kids pool from above, colour returns
    (B(33.5), "d0388", 14.0, ""),         # wide rising (Kini)
    (B(37.7), "d0387", 3.0, ""),          # concourse tracking shot
    (B(42.0), "d0385", 2.0, ""),          # hot spring pool
    (B(46.4), "d0385", 6.3, ""),
    (B(51.0), "d0392", 1.0, ""),          # kids pool push-in
    (B(55.4), "d0383", 9.0, ""),          # kids pool orbit
    (B(60.0), "d0389", 0.0, ""),          # chalets with private pools (room grid over it)
    (B(70.0), None, "pool2", ""),         # photo
    (B(72.5), None, "pool4", ""),         # photo
    (B(75.0), "d0387", 17.5, ""),         # concourse with visitors
    (B(78.5), "d0391", 5.0, ""),          # cafe
    (B(82.0), "d0382", 7.5, ""),          # parking
    (B(86.0), "d0388", 15.5, ""),         # wide: complex and main road (climax)
    (B(95.4), "d0389", 21.0, ""),         # fly-over to the kids pool
    (B(101.4), "d0382", 4.0, "endblur"), # end-card background (blurred)
]
S = [t for t, *_ in SHOTS]
CUES = {
    "loc_in": B(1.8), "loc_out": B(5.8),
    "ttl_in": S[2] + 0.35, "ttl_out": B(18.9),
    "bug_in": B(19.9), "bug_out": S[19] - 0.6,
    "c1_in": B(20.1), "c1_out": B(25.9), "c1b_in": B(27.0), "c1b_out": B(32.9),
    "c2_in": B(34.0), "c2_out": B(41.3), "st1": B(35.8), "st2": B(38.4),
    "c3_in": B(42.5), "c3_out": B(50.4), "c3_p": [B(44.4), B(45.7), B(47.0)],
    "c4_in": B(51.5), "c4_out": B(59.4), "c4_p": [B(53.4), B(54.7), B(56.0)],
    "c5_in": B(60.5), "c5_out": B(63.4), "rooms_in": B(63.9),
    "rooms_c": [B(64.4), B(65.3), B(66.2), B(67.1)], "rooms_out": B(69.5),
    "c5b_in": B(70.5), "c5b_out": B(74.5),
    "c6_in": B(75.5), "c6_out": B(85.4), "c6_p": [B(77.4), B(78.5), B(79.6), B(80.7), B(81.8)],
    "c7_in": B(86.4), "c7_out": B(94.8), "pin": B(87.8), "hours": B(89.6),
    "tag1": B(96.4), "tag2": B(97.8), "tag_out": B(100.8),
    "end_in": S[19], "black_out": round(TOTAL - 0.9, 2),
}
C = CUES
SFX = [  # light touches only: the music carries the film
    (C["ttl_in"] - 0.5, "whoosh-cinematic.mp3", 0.3), (C["ttl_in"], "impact-bass-2.mp3", 0.35), (C["ttl_in"] + 0.25, "sparkle.mp3", 0.25),
    *[(C[k] - 0.1, "whoosh-short.mp3", 0.15) for k in ("c1_in", "c2_in", "c3_in", "c4_in", "c5_in", "c6_in", "c7_in")],
    *[(t, "pop.mp3", 0.15) for t in (C["st1"], C["st2"], *C["c3_p"], *C["c4_p"], *C["c6_p"])],
    *[(t, "whoosh-short.mp3", 0.13) for t in C["rooms_c"]],
    (C["end_in"] + 0.3, "chime.mp3", 0.25),
]
# storyboard rows: (name, first shot, frame time, visual, on-screen text)
SCENES = [
    ("Pembukaan", 0, B(4.5), "Drone: kampung & bukit Alor Gajah → kompleks didedahkan dari atas", "Pin lokasi: ALOR GAJAH · MELAKA"),
    ("Tajuk", 2, C["ttl_in"] + 3.0, "Drone: aerial penuh kompleks", "Logo Gadek Hotspring Wellness & Spa Resort + kilatan; Kampung Ganun · Alor Gajah · Melaka"),
    ("01 · Sejarah (1)", 3, C["c1_out"] - 1.2, "Papan tanda Geotapak (gred vintaj, rasa lama)", "Rahsia Zaman British / Pegawai & askar British dikatakan berendam di sini untuk mengubati penyakit"),
    ("01 · Sejarah (2)", 4, C["c1b_out"] - 1.2, "Chalet & kolam kanak-kanak dari atas (warna kembali)", "Bukan Air Biasa / Mata air panas semula jadi, mengalir terus dari dalam bumi"),
    ("02 · Kini", 5, C["c2_out"] - 0.8, "Drone naik dedah kompleks → ruang legar", "Warisan Dihidupkan Semula; kad 16.12.2024 Mula beroperasi; kad 30 Warga kerja"),
    ("03 · Kolam Air Panas", 7, C["c3_out"] - 0.8, "Orbit kolam air panas dewasa", "Lepaskan Penat + Lega ketegangan otot · Lancar peredaran darah · Tenangkan fikiran"),
    ("04 · Kolam Kanak-Kanak", 9, C["c4_out"] - 0.8, "Push-in ke taman permainan air → orbit kolam kanak-kanak", "Dunia Si Kecil + Air suam semula jadi · Kawasan cetek · Selamat & mesra keluarga"),
    ("05 · Penginapan", 11, C["rooms_out"] - 0.6, "Drone chalet berkolam peribadi → 4 kad bilik ikut beat", "Satu Hari Tak Cukup? Kad: Single Room · Deluxe Room · Chalet Single · Chalet Family (tiada harga)"),
    ("05 · Penginapan (2)", 12, C["c5b_out"] - 1.0, "Foto kolam peribadi chalet (Ken Burns)", "Berendam Di Bawah Bintang / Kolam air panas peribadi di setiap chalet"),
    ("06 · Kemudahan", 14, C["c6_out"] - 0.8, "Ruang legar → kafe → parkir", "Semuanya Ada Di Sini + Tapak vendor · Dewan majlis · Kafe · Surau · Parkir luas"),
    ("07 · Lokasi & Waktu", 17, C["c7_out"] - 0.8, "Drone luas: kompleks & jalan utama (kemuncak muzik)", "Mudah Dikunjungi / Melalui jalan Melaka–Tampin; kad Kampung Ganun; waktu operasi kolam"),
    ("Tagline", 18, C["tag_out"] - 0.4, "Drone melintasi chalet ke kolam kanak-kanak", "Rehatkan tubuh, tenangkan minda."),
    ("Penutup", 19, C["end_in"] + 3.5, "Latar kabur + kad akhir, muzik selesai", "Logo, Tempah sekarang · gadekhotspring.my, 010-279 6397, @gadekhotspring, @gadek.hotspring, alamat"),
]


def media_len(clip, cache={}):
    if clip not in cache:
        cache[clip] = dur(f"{HF}/assets/video/{clip}.mp4")
    return cache[clip]


def music_automation(total):
    pts = [(0, 0), (0.4, 0.9), (total - 2.2, 0.9), (total, 0)]
    return {"version": 1, "lanes": [{"target": "volume", "points": [{"t": t, "v": v} for t, v in pts]}]}


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
    for j, (t, f, v) in enumerate(sorted(SFX)):
        audio.append(f'      <audio id="s{j:02d}" src="assets/sfx/{f}" data-start="{round(t, 3)}" data-duration="{round(dur(f"{HF}/assets/sfx/{f}"), 3)}" data-track-index="{30 + j % 4}" data-volume="{v}"></audio>')
    auto = json.dumps(music_automation(TOTAL))

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
      <audio id="bgm" data-timeline-role="music" src="{MUSIC}" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-automation='{auto}'></audio>
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
    ends = [sc[1] for sc in SCENES[1:]]
    scenes = [{"name": n, "start": SHOTS[i][0], "end": SHOTS[ends[k]][0] if k < len(ends) else TOTAL, "frame": round(f, 2),
               "visual": v, "text": tx} for k, (n, i, f, v, tx) in enumerate(SCENES)]
    json.dump({"total": TOTAL, "cues": CUES, "shots": shots_out, "scenes": scenes}, open(f"{HF}/../cues.json", "w"), indent=1)
    print("total", TOTAL)


if __name__ == "__main__":
    main()
