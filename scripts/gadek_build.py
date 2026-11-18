"""Gadek Hotspring corporate video (v3, no voice-over, cut to the music): writes
edits/gadek-hotspring/hf/index.html, hf/compositions/fx.html (from ../fx.tpl.html) and ../cues.json.

Every time is snapped to the beat grid of the music (beats.json, librosa on "The Journey" edit, 89 BPM).
Only steady stretches of the drone footage are used: per-second camera speed/jerk was measured
(phase correlation) and the take-off/adjusting parts and the shot with the operator are left out.
usage: python3 scripts/gadek_build.py"""
import html as htmllib, json, os, subprocess

HF = os.path.join(os.path.dirname(__file__), "..", "edits", "gadek-hotspring", "hf")
GRADES = json.load(open(os.path.join(HF, "..", "grades.json")))  # from `hyperframes media-treatment`
BEATS = json.load(open(os.path.join(HF, "..", "beats.json")))
MUSIC = "assets/bgm/the-journey-edit.mp3"  # "The Journey", Ahjay Stelino (Mixkit), 89 BPM, intro skipped (CREDITS.md)
# sections of the edited track (librosa): name shown on the storyboard
MUSIC_SECTIONS = [(0, "Rentak terus masuk"), (21.3, "Bahagian utama"), (42.7, "Bahagian utama (8 bar diulang)"),
                  (64.2, "Variasi"), (85.4, "Breakdown tenang"), (96.7, "Frasa penutup")]
XF = 0.5  # crossfade length between consecutive shots
TOTAL = 107.6


def B(t):
    """nearest beat to t"""
    return round(min(BEATS, key=lambda b: abs(b - t)), 3)


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode())


# (cut time, clip, media start, grade); every shot is inside a measured steady stretch
SHOTS = [
    (0.0, "d0392", 31.0, ""),             # village & hills, slow drift
    (B(5.6), "d0388", 7.0, ""),           # rising reveal of the complex
    (B(10.8), "d0382", 2.0, ""),          # wide aerial (title)
    (B(16.2), "d0386", 11.5, "vintage"),  # Geotapak sign, history
    (B(21.5), "d0385", 0.5, ""),          # the hot spring water itself, colour returns
    (B(26.9), "d0388", 14.0, ""),         # wide rising (Kini)
    (B(30.9), "d0387", 3.0, ""),          # concourse tracking shot
    (B(35.0), "d0385", 6.3, ""),          # hot spring pool orbit
    (B(40.4), "d0392", 0.1, ""),          # kids pool push-in (one long move)
    (B(52.2), "d0389", 0.0, ""),          # chalets with private pools (room grid over it)
    (B(60.3), None, "pool2", ""),         # photo
    (B(62.4), None, "pool4", ""),         # photo
    (B(64.4), "d0387", 17.5, ""),         # concourse with visitors
    (B(68.4), "d0391", 5.0, ""),          # cafe
    (B(72.4), "d0382", 8.5, ""),          # parking / wide
    (B(76.4), "d0388", 15.5, ""),         # wide: complex and main road
    (B(85.6), "d0389", 22.0, ""),         # fly-over to the kids pool (breakdown)
    (B(91.0), "d0383", 9.0, ""),          # kids pool orbit, calm
    (B(96.9), "d0382", 3.0, "endblur"),   # end-card background (blurred)
]
S = [t for t, *_ in SHOTS]
CUES = {
    "loc_in": B(1.5), "loc_out": B(5.0),
    "ttl_in": S[2] + 0.35, "ttl_out": B(15.7),
    "bug_in": B(16.4), "bug_out": S[18] - 0.6,
    "c1_in": B(16.6), "c1_out": B(21.0), "c1b_in": B(22.0), "c1b_out": B(26.4),
    "c2_in": B(27.3), "c2_out": B(34.5), "st1": B(29.0), "st2": B(31.5),
    "c3_in": B(35.4), "c3_out": B(39.9), "c3_p": [B(36.6), B(37.5), B(38.3)],
    "c4_in": B(40.9), "c4_out": B(51.7), "c4_p": [B(42.9), B(44.3), B(45.6)],
    "c5_in": B(52.6), "c5_out": B(54.4), "rooms_in": B(54.9),
    "rooms_c": [B(55.0), B(55.7), B(56.4), B(57.1)], "rooms_out": B(59.8),
    "c5b_in": B(60.6), "c5b_out": B(63.9),
    "c6_in": B(64.8), "c6_out": B(75.9), "c6_p": [B(66.8), B(68.1), B(69.5), B(70.8), B(72.1)],
    "c7_in": B(76.8), "c7_out": B(85.1), "pin": B(78.2), "hours": B(80.0),
    "tag1": B(86.5), "tag2": B(88.5), "tag_out": B(95.8),
    "end_in": S[18], "black_out": round(TOTAL - 0.9, 2),
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
    ("Pembukaan", 0, B(3.5), "Drone: kampung & bukit Alor Gajah → kompleks didedahkan dari atas", "Pin lokasi: ALOR GAJAH · MELAKA"),
    ("Tajuk", 2, C["ttl_in"] + 3.0, "Drone: aerial penuh kompleks", "Logo Gadek Hotspring Wellness & Spa Resort + kilatan; Kampung Ganun · Alor Gajah · Melaka"),
    ("01 · Sejarah (1)", 3, C["c1_out"] - 1.2, "Papan tanda Geotapak (gred vintaj, rasa lama)", "Rahsia Zaman British / Pegawai & askar British dikatakan berendam di sini untuk mengubati penyakit"),
    ("01 · Sejarah (2)", 4, C["c1b_out"] - 1.2, "Air kolam air panas dari atas (warna kembali ikut rentak)", "Bukan Air Biasa / Mata air panas semula jadi, mengalir terus dari dalam bumi"),
    ("02 · Kini", 5, C["c2_out"] - 0.8, "Drone naik dedah kompleks → ruang legar", "Warisan Dihidupkan Semula; kad 16.12.2024 Mula beroperasi; kad 30 Warga kerja"),
    ("03 · Kolam Air Panas", 7, C["c3_out"] - 0.8, "Orbit kolam air panas dewasa", "Lepaskan Penat + Lega ketegangan otot · Lancar peredaran darah · Tenangkan fikiran"),
    ("04 · Kolam Kanak-Kanak", 8, C["c4_out"] - 0.8, "Push-in panjang ke taman permainan air", "Dunia Si Kecil + Air suam semula jadi · Kawasan cetek · Selamat & mesra keluarga"),
    ("05 · Penginapan", 9, C["rooms_out"] - 0.6, "Drone chalet berkolam peribadi → 4 kad bilik ikut beat", "Satu Hari Tak Cukup? Kad: Single Room · Deluxe Room · Chalet Single · Chalet Family (tiada harga)"),
    ("05 · Penginapan (2)", 10, C["c5b_out"] - 1.0, "Foto kolam peribadi chalet (Ken Burns)", "Berendam Di Bawah Bintang / Kolam air panas peribadi di setiap chalet"),
    ("06 · Kemudahan", 12, C["c6_out"] - 0.8, "Ruang legar → kafe → aerial luas", "Semuanya Ada Di Sini + Tapak vendor · Dewan majlis · Kafe · Surau · Parkir luas"),
    ("07 · Lokasi & Waktu", 15, C["c7_out"] - 0.8, "Drone luas: kompleks & jalan utama", "Mudah Dikunjungi / Melalui jalan Melaka–Tampin; kad Kampung Ganun; waktu operasi kolam"),
    ("Tagline", 16, C["tag_out"] - 0.4, "Drone melintasi chalet → orbit kolam kanak-kanak (breakdown tenang)", "Rehatkan tubuh, tenangkan minda."),
    ("Penutup", 18, C["end_in"] + 3.5, "Latar kabur + kad akhir pada frasa penutup lagu", "Logo, Tempah sekarang · gadekhotspring.my, 010-279 6397, @gadekhotspring, @gadek.hotspring, alamat"),
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
    json.dump({"total": TOTAL, "music": MUSIC, "music_sections": MUSIC_SECTIONS, "cues": CUES, "shots": shots_out, "scenes": scenes}, open(f"{HF}/../cues.json", "w"), indent=1)
    print("total", TOTAL)


if __name__ == "__main__":
    main()
