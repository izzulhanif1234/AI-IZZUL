# Gadek Hotspring Wellness & Spa Resort — Video Korporat (16:9)

1:48 (107.6 s), 1920x1080, HyperFrames project in `hf/`. `scripts/gadek_build.py` writes
`hf/index.html` and `hf/compositions/fx.html` (from `fx.tpl.html`) plus `cues.json`.
Every cut, SFX and graphic is a cue tied to the VO: a line's start/end or the start of one of its
script words, so changing the VO re-times the whole film. Storyboard JPGs in `storyboard/`
(`scripts/gadek_storyboard.py`, frames from `hyperframes snapshot --at $(... --times)`).

Facts on screen and in the VO come only from https://www.gadekhotspring.my (Sejarah Kami,
Aktiviti/Fasiliti, Jenis Bilik, Tarikan, Polisi pages, read 18 Nov 2026).
Revision 2 (client): livelier VO script (`vo_lines.json`; first draft in `vo_lines_v1.json`),
no room prices, capacities or promo notes anywhere (room cards show name + one plain line).

## Scenes
Pembukaan · Tajuk · 01 Sejarah (2 beats, first one graded "vintage") · 02 Kini (16.12.2024, 30
warga kerja) · 03 Kolam Air Panas · 04 Kolam Kanak-Kanak · 05 Penginapan (4 room cards, then
private-pool photos) · 06 Kemudahan · 07 Lokasi & Waktu (25 km, pool hours) · Tagline · End card.
See the storyboard JPGs for frames, VO and on-screen text per scene.

## Audio
- VO: Google Gemini TTS `gemini-2.5-flash-preview-tts`, voice "Charon", the whole script as ONE
  take (`vo_take.wav`; prompt prefix "Say in a warm, lively and confident Malaysian corporate
  documentary narrator voice, with natural pauses between paragraphs:"). One request per take keeps
  the tone even and stays inside the free tier (10 requests/day). `scripts/gadek_split_vo.py`
  aligns script words to whisper-small words and cuts each line at the quietest point of the pause
  → `hf/assets/vo/<id>.wav` + `<id>.words.json`. Each clip was re-transcribed: no clipped words.
  `gemini-3.8-flash-tts` reads style prefixes aloud and rejects systemInstruction: not used.
  The key is read from a local file (`GEMINI_KEY_FILE`), passed as `?key=` (the environment proxy
  overwrites the `x-goog-api-key` header with an old, invalid key).
- Music: MusicGen-small (`scripts/musicgen_long.py`), two 60 s generations whose continuation broke
  after ~50 s; bed = A 0–50 + B 0–46 + A 2–50 with 3 s crossfades, loudnorm −16 LUFS,
  ducked to 0.16 under VO, faded at the end by automation.
- SFX: shared Pixabay library (`hf/assets/sfx/CREDITS.md`).
- Grades: `grades.json` (normalised `hyperframes media-treatment` patches: "vintage" for the
  history shots, "endblur" for the end card). CSS filters on wrappers are not rendered.

## Media (not in git)
Drive folder 16yQ8ejS1LEuc3XsHTYKvtlxh1Oty8RXG: 9 DJI clips, 4K60 HEVC. Rebuild:
`gdown <id> -O media/gadek/drone/dNNNN.mp4`, then 1080p30 H.264 proxies with a light grade
(`eq=contrast=1.06:saturation=1.22:gamma=0.98`, unsharp) into `media/gadek/proxy/`, hard-linked
into `hf/assets/video/`. Room photos + logo from the website gallery (`hf/assets/img/`).
