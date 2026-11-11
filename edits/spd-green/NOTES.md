# SPD GREEN: explainer video (Anugerah Hijau Negeri Melaka 2026)

4:00, 1920x1080. Stage 1 (now): storyboard + timeline JPGs for approval. Stage 2 (on "create video"): HyperFrames build.

## Sources (Drive folder "PROJEK SPD GREEN", not in git: `media/spd-green/`)
- `PDF PENERANGAN/SLIDE ANUGERAH HJAU INOVASI SPD 2026 (Video Izzul).pptx`: red-button slides 2-18 = content to explain;
  slide 19 = SPD 2.0 + Green Dashboard; slide 20 = closing.
- `PDF PENERANGAN/Cadangan Dashboard SPD Green Index.pdf`: 7 modules, GPS weights, Green Impact Meter, slogan.
- Screenshots: DAHSBOARD, ASET ALIH, ASET TAK ALIH, PENGURUSAN MODAL INSAN, PENGURUSAN STOR (cropped to remove
  browser chrome and taskbar: y 108-1020).
- VIDEO LAKONAN folder was empty when downloaded (2026-11-11).

## Storyboard
- `scripts/spd_storyboard.py` -> `storyboard/storyboard.html` + `timeline.json`; `scripts/spd_storyboard_render.js` -> JPGs.
- 19 scenes, 4 acts. Every thumbnail is a 1920x1080 style frame (reuse as scene start points).
- SPD 2.0 homepage mock (`spd2_homepage()`): live-SPD look (maroon sidebar, MCORP header), bottom section
  "SPD 2.0 + GREEN DASHBOARD". KPIs from slides: A4 -25.4% (1,242->926), ink -39.7% (174->105), sewaan 14->3 days,
  aset alih 20->2 days, staff 18->9, RM217,836/yr. Green Index 82 = PDF weights x estimated component scores.
- SFX concept "Kertas -> Piksel": office/paper foley, pitched/reversed/granular; no stock whoosh/ding.
- Persistent MCORP 3D badge top right, rotateY swing (as mcorp-estimate `compositions/badge.html`), source logo = pptx image1.

## Revision 2 (user feedback)
- No blurring of staff names/photos.
- System parts are live-feel demos (cursor moves, clicks, typing, scroll, panels opening): S05 enter system,
  S06 Laman Utama scroll (DAHSBOARD 77-81), S07 Aset Tak Alih search "ELKAY" -> premis -> map -> hak milik docs (83-89),
  S08 Aset Alih / Stor / Modal Insan / Pentadbiran via sidebar clicks, S19 SPD 2.0 click "Green Dashboard" + scroll.
- VO script written by us (`vo-script.json`, `storyboard/SKRIP-VO.md`, 394 words): Gemini TTS voice Charon, one take,
  split with `scripts/split_vo.py` like MCORP Estimate. Key: network secret for generativelanguage.googleapis.com
  (header x-goog-api-key) on the environment; `gemini_tts.py` sends a placeholder when GEMINI_KEY_FILE is unset.
- 20 scenes; final scene timings follow the recorded VO.

## Revision 3
- VO: no "Anugerah Hijau" mention, no "kami"; general corporate tone. Title overline = PERBADANAN MELAKA (MCORP).
- S19 SPD 2.0 is the "akan datang" closer: homepage only scrolls down to the Green Dashboard section (no sidebar click,
  no Green Dashboard menu item).
- Footage (Drive VIDEO LAKONAN 1-3.MP4, 4K HEVC 29.97 -> 1080p proxies `media/spd-green/lakonan/l1-3.mp4`):
  1 = archive shelves search (off-camera chatter 15-24 s: mute), 2 = desk, acted line 10.8-15.6 s
  ("Saya tak jumpa… Mana ni? Mana ni? Tolong… cek file"), 3 = enter file room, unlock cabinet, hanging files
  (crew "1, 2, 3, action" 0-3.8 s: skip). Whisper transcripts l1-3.json.
- S01 is 18 s; scenes re-timed (S19 25 s).
