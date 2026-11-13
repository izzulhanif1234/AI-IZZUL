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
- s15 is now the KPI scene from the user's KPI table (media/spd-green/new12/kpi.jpg): six before->after cards,
  then RM178,141 = RM3,634 kertas + RM7,107 dakwat + RM167,400 sewaan ruang pejabat; placed after s16, fixed 13.5 s.
- s19 SPD 2.0 Green Dashboard rebuilt from the user's proposal (new12/d1-d5): 5 modules (Paperless, Carbon Saving,
  Resource Efficiency, Green Performance Monitoring, Green Analytics), KPI cards from the KPI table, division table.
- s07 now on the user's MITC screens (media/spd-green/new13 -> hf/assets/ui/mitc1-4.jpg): search "MITC" (results list
  rebuilt in HTML from the real komponen names), premis profile, komponen list (Aras 11 SEWA), dokumen sokongan,
  pelan in the PDF viewer. s08 Stor = stor1/stor2 (Senarai Stok), Pentadbiran = sistem.jpg (Sistem page).
- s03b (new, fixed 16.4 s, no VO): five modules + sub-modules in premium cards; SUBS grouped from the real sidebar
  menus (media/spd-green/sub/*.png). s04: the user's six AI clips (media/spd-green/ai6 -> hf/assets/video/ai0*.mp4,
  last-frame stills in img/) in taped photo frames on the doodle page. s13 and s16 removed (same figures as s15 KPI).

## v11
- VO: v05/v06 (chunk n3) and v09/v10/v14 (n5) came out in a different voice (median F0 140-210 Hz vs ~100 Hz elsewhere,
  heard as female / another tone). Regenerated with a style prefix in the prompt ("deep, calm, mature adult male ...
  narrator voice, steady low pitch") -> F0 94-97 Hz, LID ms 1.0, prefix not spoken (`vo/take8`). v05/v06 level-matched
  (+4 / +2.6 dB with limiter). Old lines in `vo/pre_v11_lines`.
- v19 rewritten (`vo/take10`): the Green Dashboard now names only kertas, dakwat and penjimatan kos. "Masa carian"
  (efficiency), "ruang simpanan" (rental income) dropped as not green; a CO2e / pokok try (`vo/take9`) was rejected.
  The two KPI cards stack beside the RM178,141 card.
- Music: "Inspired" (Kevin MacLeod, CC BY 4.0) replaces "Cipher" (too playful). Mixer already RMS-normalises music.
- s01 montage: light-switch and cabinet-unlock shots dropped; now blue hanging files -> archive shelf -> desk (5.87 s,
  segments c/d/e from `media/spd-green/lakonan/seg`, light grade). Added viewfinder HUD (corner brackets, blinking
  "MENCARI FAIL", stopwatch racing 00:00 -> 30:00 to match the 30-minute search KPI), shot tags, whip-blur + light-leak
  at each cut. Old montage kept as `media/spd-green/lakonan/s01_montage_v10.mp4`.
- s02/s20: MCORP logo enlarged (300 -> 450 / 210 -> 340 px) and tucked closer to the SPD mark.
- s07: cursor lands on the centre of "Lihat" under PELAN M&E GALERI PKNM (page px 1259-1309 x 680-711) as the VO says
  "pelan"; button press + ripple, URL switches to the attachment (4269), page dims, and the PDF viewer grows out of the
  thumbnail (transform-origin on the thumbnail) instead of fading in.
- Scene tails trimmed (s03b, s05, s07, s08, s14, s15, s19). Total 3:58.6.

## v12
- s03b connectors: all five are now the same straight line from the active tile's edge (tile scaled 1.14) to the
  card's near edge at title height (ctop + 86), with a node at each end. Before, they were S-curves, near-straight,
  or (module 03) started past the card edge and ran back into the box. Travelling dot and its tween no longer
  render early (immediateRender:false), which left stray dots beside idle tiles.
- VO pace: syllable rate per line ranged 5.45-7.37 syl/s (0.83-1.13 of median). Every line time-stretched with
  rubberband (formant-preserving, pitch unchanged) to the median 6.53 syl/s, within 0.88-1.20; word timings scaled.
  Now 6.30-6.64 syl/s. Pre-stretch lines in `vo/pre_pace_lines`.
- Logo lockups: `spd_mark(..., balanced=True)` pads the left by the leaf width so the SPD letters sit on the centre
  line; logo width = SPD letters width (~1.9 x font size): s02 436/230, s03 + s03b 248/130, s20 324/170.
- Total 3:57.

## v13
- s03 orbit centre: the SPD mark sat 43 px right of the logo. The 3D stack box (449 px) was wider than its 360 px
  flex parent, so it shrank while its layers kept the full width and spilled right. `stack3d` roots are now
  `flex:none`; SPD letters and logo measure centred at x = 960 in s02, s03, s03b and s20.

## v14
- KPI table revised by the user: MANFAAT BERSIH RM276,680.20 = kertas RM3,634 + dakwat RM7,107 + sewaan Aras 10
  (MITCH) RM167,400 + Aras 5 (PMPC) RM98,539.20; ruang simpanan 1,550 + 912.4 = 2,462.4 kp now rented.
  s15 cards 05/06 and the total + four chips updated; dashboard (s19) total + 4-part donut updated. v15 rewritten.
- VO "robotic / unclear": the v12 rubberband time-stretch (up to 1.2x) caused it. All 16 lines regenerated
  (`vo/take11/b`), no stretching besides the global atempo 1.1 in the mix. Prompt: Malaysian Malay, deep male
  narrator, calm unhurried steady pace, every syllable clear, numbers slow. n4/n5 needed retakes ("barcode" heard
  as "bakut"; TTS text for n5 spells it "barkod"). Result: F0 92-98 Hz, 5.4-5.9 syl/s, LID ms 1.0 on every chunk.
  Every line loudness-matched to -17 LUFS (they ranged -13.6 to -19.2, which also read as uneven delivery).
- s15 card 06 cues on "pejabat" (was "disewakan", one second before the total took over); its title is one line
  ("Sewaan ruang pejabat", floors moved to the chip) and the long figure is raised to sit level with the other cards.
- Total 4:31 (natural pace is slower; KPI scene 41 s).

## v15
- VO evenness: per-line rate incl. pauses ranged 3.7-5.1 syl/s because the TTS left very uneven pauses (15-29% of a
  line). `scripts/vo_even.py` caps every pause by punctuation ('.?!' 0.40 s, ',;:' 0.24 s, none 0.12 s) -- only
  silence is cut, with 15 ms crossfades -- then nudges a line's tempo by at most -6%/+8% (atempo). Now 4.2-5.2
  syl/s (most 4.4-5.0). Source lines in `vo/v14_lines`. Whole-script single-take TTS was tried (one streamed
  request) but the upstream returns 502 for ~4 min of audio; gemini-3.8-flash-tts skipped words and anglicised
  "aset/stor"; the 2.5 TTS free daily quota (10) was then spent.
- Length 4:31 -> 4:00.8: VO tempo 1.10 -> 1.13, scene tails trimmed, intro questions 2.1 -> 1.9 s, pauses capped.
  The full KPI sentence stays (a shorter one needs a new TTS take).
- Intro: the MCORP logo now lands in a white studio (soft mint radial, dot grid, slow-rotating emerald rings,
  diagonal light rays, logo aura, floor shadow, emerald/gold base rule, emerald-gold lens streak); vignette is held
  back while white; the studio irises closed (clip-path circle 76% -> 0 from 2.3 s) into the dark question beat,
  with the logo exiting at 2.4 s.

## v16 (final polish)
- Intro: the emerald-gold lens streak (it crossed the logo at y 498) and the floor rule are no longer animated in;
  the white studio keeps only the soft floor shadow.
- s02 title and the s03b backdrop get the same green halo as the s03 orbit core (lime radial .34/.09 + a pale
  inner core); in s02 it scales in with the logo and breathes gently.
