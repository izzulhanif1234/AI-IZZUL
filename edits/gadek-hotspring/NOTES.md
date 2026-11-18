# Gadek Hotspring Wellness & Spa Resort — Video Korporat (16:9)

1:49 (109.5 s), 1920x1080, HyperFrames project in `hf/`. `scripts/gadek_build.py` writes
`hf/index.html`, `hf/compositions/fx.html` (from `fx.tpl.html`) and `cues.json`.
Storyboard JPGs in `storyboard/` (`scripts/gadek_storyboard.py`, frames from
`hyperframes snapshot --at $(python3 scripts/gadek_storyboard.py --times)`).

Facts on screen come only from https://www.gadekhotspring.my (Sejarah Kami, Aktiviti/Fasiliti,
Jenis Bilik, Polisi pages, read 18 Nov 2026). No room prices, capacities, promos or distance claims.

## Revision 3 (client): no voice-over, better music, no bad drone moments
- No VO. On-screen chapter titles + subtitles carry the story. The v2 VO (Gemini Charon, one take,
  `vo_take.wav`, `hf/assets/vo/`) stays in the repo, unused.
- Music: "Dreaming Big" by Ahjay Stelino (Mixkit Stock Music Free License, commercial use, no
  attribution; `hf/assets/bgm/CREDITS.md`). Lyria could not be used: the Lyria 3 models have a 0
  free-tier quota on this key and Lyria RealTime needs a WebSocket, which the environment proxy does
  not carry. Beat grid `beats.json` (librosa, 136 BPM); every cut and pop-in is snapped to a beat.
  Sections: intro 0–19.5, build 19.5–28.5, main 28.5–88, peak 88–95.4, outro from 101.4.
- Footage: per-second camera speed/jerk measured with phase correlation on the proxies
  (`/tmp` analysis, not kept). Left out: d0392 12.5–28.5 (tilt to the sky, adjusting) and
  38.5–48 (fast pan, then top-down on the parking lot with the drone operator in frame),
  d0388 0–6.5 (take-off through trees and a red roof), d0386 0.5–8.5 (car roof, jerk),
  d0389 11.3–12.8 and 18.8–20.8, d0385 11.8–17.5, d0383 2.8–8.6 and 15.8–17.
- Scenes: Pembukaan · Tajuk · 01 Sejarah (2 beats, first graded "vintage") · 02 Kini · 03 Kolam
  Air Panas · 04 Kolam Kanak-Kanak · 05 Penginapan (room cards, then private-pool photos) ·
  06 Kemudahan · 07 Lokasi & Waktu (at the music peak) · Tagline · End card.
- Grades: `grades.json` ("vintage" for history, "endblur" for the end card), applied as
  `data-color-grading`; CSS filters on wrappers are not rendered.
- SFX kept light (title hit, soft whooshes/pops) under the music.

## Media (not in git)
Drive folder 16yQ8ejS1LEuc3XsHTYKvtlxh1Oty8RXG: 9 DJI clips, 4K60 HEVC. Rebuild:
`gdown <id> -O media/gadek/drone/dNNNN.mp4`, then 1080p30 H.264 proxies with a light grade
(`eq=contrast=1.06:saturation=1.22:gamma=0.98`, unsharp) into `media/gadek/proxy/`, hard-linked
into `hf/assets/video/`. Room photos + logo from the website gallery (`hf/assets/img/`).
