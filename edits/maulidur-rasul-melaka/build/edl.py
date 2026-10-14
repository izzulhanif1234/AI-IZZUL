"""Edit decision list for the Maulidur Rasul 1448H (Melaka) highlights. Single source of truth for
the picture compositions (compose.py) and the audio mix (mix_audio.py). All times in seconds.

Timeline: 41.4s @ 30fps. Music grid: 100 BPM, bar 1 on 4.2s, bars every 2.4s.
"""

DURATION = 41.4

# Event facts (verified: on-site banner + speech + Bernama/RTM reports of 25 Aug 2026; see NOTES.md)
EVENT = {
    "kicker": "Sambutan Maulidur Rasul 1448H / 2026M",
    "title": "Majlis Perhimpunan dan Perarakan",
    "level": "Peringkat Negeri Melaka",
    "venue": "Stadium Tun Fatimah, Bukit Serindit",
    "date": "25 Ogos 2026",
    "theme_a": "MADANI Dihayati",
    "theme_b": "Ummah Diberkati",
}

# ---------------------------------------------------------------------------------------------
# Picture. Each shot: footage file, timeline start, duration, media in-point, fade-in (dissolve),
# and framing per format as (focusX, focusY, scale) at shot start -> end, in 1920x1080 source px.
# scale 1 = the frame just covers the canvas (16:9: full frame; 9:16: full height, 608px window).
SHOTS = [
    # ---- HOOK: beat-cut montage under the theme line (voice from 8035)
    dict(id="h1", src="c8036", t=0.0, d=1.2, ms=0.3, fade=0,
         f169=((845, 600, 1.25), (845, 600, 1.17)), f916=((845, 560, 1.12), (845, 560, 1.04))),
    dict(id="h2", src="c8034", t=1.2, d=1.2, ms=9.0, fade=0,
         f169=((1000, 635, 1.42), (1000, 620, 1.5)), f916=((1000, 600, 1.0), (1000, 580, 1.08))),
    dict(id="h3", src="c8035", t=2.4, d=0.6, ms=11.5, fade=0,
         f169=((1000, 650, 1.32), (1000, 650, 1.38)), f916=((1000, 700, 1.0), (1000, 700, 1.04))),
    # ---- speed-ramped zoom-out reveal (8033 src 20.5-25.3 squeezed to 1.2s)
    dict(id="ramp", src="ramp", t=3.0, d=1.2, ms=0, fade=0,
         f169=((960, 540, 1.0), (960, 540, 1.0)), f916=((1150, 540, 1.0), (1000, 540, 1.0))),
    # ---- TITLE on the wide grandstand
    dict(id="wide1", src="c8033", t=4.2, d=4.9, ms=25.3, fade=0,
         f169=((960, 540, 1.0), (960, 520, 1.06)), f916=((560, 560, 1.0), (1180, 560, 1.0))),
    # ---- SPEECH 1 (8034, synced) then dignitaries listening (8036)
    dict(id="spk", src="c8034", t=8.6, d=6.0, ms=1.05, fade=0.5,
         f169=((985, 560, 1.04), (985, 540, 1.12)), f916=((990, 600, 1.0), (990, 570, 1.07))),
    dict(id="vip1", src="c8036", t=14.6, d=5.4, ms=2.9, fade=0,
         f169=((900, 600, 1.03), (1020, 600, 1.09)), f916=((380, 720, 1.0), (1480, 720, 1.0))),
    # ---- SPEECH 2 (8035, synced) then the dais with the speaker at the podium (8033)
    dict(id="vip2", src="c8035", t=19.4, d=6.0, ms=3.42, fade=0.4,
         f169=((960, 600, 1.0), (960, 600, 1.08)), f916=((1480, 680, 1.0), (560, 680, 1.0))),
    dict(id="dais", src="c8033", t=25.2, d=5.4, ms=1.0, fade=0,
         f169=((960, 560, 1.12), (960, 560, 1.02)), f916=((1180, 560, 1.06), (1180, 560, 1.0))),
    # ---- CLOSING on the wide (pull back)
    dict(id="wide2", src="c8033", t=30.6, d=6.0, ms=30.4, fade=0,
         f169=((960, 500, 1.16), (960, 540, 1.0)), f916=((1250, 540, 1.08), (960, 540, 1.0))),
]

# ---------------------------------------------------------------------------------------------
# Dialogue: (raw clip, media in, media out, timeline start, fade-out). Raw MOV audio, cleaned in mix.
SPEECH = [
    ("IMG_8035", 0.40, 3.16, 0.35, 0.06),  # "Madani dihayati, ummah diberkati"
    ("IMG_8034", 1.45, 11.75, 9.00, 0.15),  # "Insan agung ... umat manusia."
    ("IMG_8035", 4.62, 14.34, 20.60, 0.30),  # "Tema ini bukan sekadar ungkapan ... nilai-nilai yang diberkati"
]

# Burned-in captions (timeline start, end, text). Two uncertain words resolved; see NOTES.md.
CAPTIONS = [
    (9.06, 12.40, "Insan agung yang membawa rahmat kepada seluruh alam,"),
    (12.48, 15.20, "serta menjadi suri teladan terbaik"),
    (15.34, 19.25, "dalam setiap sisi kehidupan umat manusia."),
    (20.62, 24.72, "Tema ini bukan sekadar ungkapan untuk menghiasi sambutan,"),
    (24.84, 26.72, "ia adalah seruan,"),
    (26.78, 30.45, "supaya kita benar-benar menghayati nilai-nilai…"),
]

# Graphics windows
HOOK_WORDS = [(0.37, "a"), (2.01, "b")]  # theme halves appear as they are spoken
TITLE = (4.25, 8.75)
THEME_TAG = (20.0, 24.4)  # lower third naming the theme the speaker refers to ("tema ini")
CLOSE = (31.0, 35.7)
END = (36.0, DURATION)  # end card fades in over the wide, holds, fades to black

# SFX: (file, timeline time of the visual hit, file onset offset, volume)
SFX = [
    ("whoosh-short.mp3", 1.2, 0.08, 0.28),
    ("whoosh-short.mp3", 2.4, 0.08, 0.28),
    ("whoosh.mp3", 3.05, 0.08, 0.42),
    ("whoosh-short.mp3", 19.6, 0.08, 0.18),
    ("whoosh.mp3", 30.6, 0.08, 0.32),
    ("chime.mp3", 36.3, 0.41, 0.22),
]

# Music level automation (dB) — ducked under dialogue, full in the hook/title/close.
MUSIC_GAIN = [
    (0.0, -2), (0.30, -7), (3.05, -7), (3.25, 0), (8.70, 0), (9.0, -15), (19.3, -15),
    (19.7, -6), (20.45, -6), (20.6, -15), (30.3, -15), (30.6, 0), (41.4, 0),
]
