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
- Blur staff names/photos in Modal Insan screens.
