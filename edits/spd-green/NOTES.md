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

## Build (video)
- `python3 scripts/spd_build.py` -> `hf/compositions/s01..s20.html`, `badge.html`, `index.html`, `plan.json`.
  Scene length = lead-in + VO + tail; every beat sits on a spoken word (`S.w(line, word, nth)`); lines without
  audio yet get an estimated timing (printed as EST).
- `python3 scripts/spd_audio.py` -> `audio/mix.wav` (score + sfx + foley + VO + dialogue, music ducked under voice,
  -14 LUFS). Final picture is rendered by HyperFrames, then audio is replaced with this mix (ffmpeg mux).
- Media not in git: `hf/assets/video/s01_montage.mp4` (ffmpeg concat of l3 6.4-8.4, 25.0-26.6, 29-32 @1.5x,
  l1 2.4-4.6 @1.1x, 10.6-13 @1.2x, l2 10.6-15.8), `hf/assets/img/s01_freeze.jpg` (l2 @15.78), `hf/assets/vo/dlg_s01.wav`
  (l2 10.6-15.8, loudnorm -18).
- VO: Gemini TTS `gemini-2.5-flash-preview-tts`, voice Charon, generated in 9 chunks (`vo/take/chunks.json`; the free
  tier allows 10 requests/day and long single takes hit a 60 s gateway timeout). Chosen takes scored on pitch
  (target ~105-110 Hz, MCORP Estimate reference 97 Hz) and re-transcribed: c01_t1, c02_t3, c03_t3, c04_t2, c08_t3.
  Split per line with `split_vo.py` into `hf/assets/vo/vNN.mp3/.json`.

## v5
- Intro haze: `#s01-flash` (white) rested at opacity .35 over the first shot because the last-authored fromTo
  set its from-value at build time; every s01 fromTo now has `immediateRender:false` (blacks 50 -> 1).
  s01 also skips the scene fade-in/push (`CAM_OPEN`), and the montage is rebuilt from the 4K originals
  (`media/spd-green/lakonan/seg/*.mp4`, Lanczos + light unsharp, crf 12, g 15).
- s03: orbit RY 200 -> 350 so the back of the orbit passes above the sphere (no tile behind it); tiles fade
  before they converge; the ball's 160 px box-shadow glow (clipped into a square) replaced by `#s03-glow`
  (closest-side radial, opacity/scale only).
- Numbers: `odo()` (python) + `FX.odo` (spdfx.js) masked odometer columns with tabular figures; RM217,836
  locks digit by digit as the VO says it; `FX.bloom`, `FX.uline`; s13 day blocks 14 -> 3; s16 % tags as red
  chips with wipe; s19 KPIs roll. s19 `t_kos` now takes the 2nd "kos" (1st was "kosong").
- VO v10 "Inilah impak SPD.": the separate short request (152 Hz, Whisper LID id .98) replaced by the
  in-context cut from take4/m04 9.55-11.35 s (96 Hz, same take as v09/v13). Previous file kept in vo/take5/v10_prev.*.

## v6
- s03 tiles are solid (emerald gradient, no transparency/backdrop blur); depth only by size + shade.
- s07 search paced out: type on "pengguna", list opens, cursor glides to ELKAY and rests ~0.3 s, clicks on
  "Rekod", page loads, 1 s zoom-out, cursor waits 0.7 s before moving to the premis panel.
- VO tails that the line split had clipped re-cut from the source takes up to 150 ms of silence
  (v16 "peratus" +0.35 s, v18 "M-Corp" +0.18 s, v08 +0.08 s, v07 +0.05 s; v05 runs into v06 in its take, so it
  only gets a 60 ms fade). Previous clips in vo/pre_v6/.

## v7
- s05 is now only the SPD login (no acting photo, full demo-size browser); real SPD login page (`hf/assets/ui/login.jpg`, from the user's screenshot, browser chrome cropped);
  zoom onto the form, masked IC + password typed, click Log Masuk -> dashboard (s77), then the push into s06
  ("Sebaik log masuk ..."). Page id `s05-pd` (s05-p2 collided with the ATAS TALIAN pill).
- Music (user asked for an existing track, not a generated one): "Inspired" by Kevin MacLeod (incompetech.com),
  CC BY 4.0 - credit required: Music: "Inspired" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0.
  File in `audio/music/` (gitignored; download: https://incompetech.com/music/royalty-free/mp3-royaltyfree/Inspired.mp3).
  Mix: `SPD_VO=1 SPD_MUSIC_FILE=edits/spd-green/audio/music/Inspired.mp3 python3 scripts/spd_audio.py`
  (0.8 s fade-in, 4 s fade-out, ducked ~11 dB under VO, dips to 30% for the IMPAK SPD slam).

## v8
- Modal Insan is staff list + courses/training, not leave: s08 panel shows Senarai Latihan (s96) then Senarai
  Kakitangan (s98) on "kakitangan"; labels updated. VO v08 spliced (13.79-14.44 s removed, "cuti dan") ->
  "Modal insan menguruskan rekod berkaitan kakitangan" (same take; original in vo/splice/v08_before.*).

## v9
- Module numbering follows the demo order: 01 Aset Tak Alih (s07 callouts), 02 Aset Alih, 03 Pengurusan Stor,
  04 Modal Insan, 05 Pentadbiran (s08 callouts); s09 cards in the same order.
- s08 finale shows all five modules (3 + 2 grid, scale .32) with numbered names; Aset Tak Alih tile = s86.

## v10 (plan JPEG pelan5/PELAN-v10.jpg; not rendered yet)
- s00 opener: 3D MCORP logo "MEMPERSEMBAHKAN" -> issue question + stopwatch -> acting (s01 crossfades in, no push).
- 3D logo: `stack3d/logo3d/spd3d` (extruded copies + masked sheen) + `live3d()` swing; used in s00, s03, s20.
- s03: sphere replaced by MCORP 3D logo + SPD; tiles = 5 modules (sub-functions pending from user).
- s06: empty Stor card -> Pecahan Kategori Jawatan (s81). s09: per-card badges -> one "Impak Hijau" 5-tick panel.
- s14: before = barcode.jpg (manual note), after = manual-check.jpg (phone scan); CSS phone scanning a dummy QR.
- s15 removed (KPI scene from user to replace it). s19 KPIs: kertas, dakwat, rekod digital 90%, masa carian -80%,
  ruang simpanan -30%, kos RM217,836 (anggaran kos operasi). "Bersepadu" removed from the title.
- Pending from user: module subs, new ATA search screenshots (replace ELKAY), KPI, AI videos for s04, new VO.
