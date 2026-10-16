# Colour Rush Melaka 2026 — Tee Ad (work in progress)

Source: `source-design.jpg` (tee design board). Only the two hero shirts (front + back) are used.
Prep: `python3 scripts/colour_rush_prep.py source-design.jpg hf/assets/img EDSR_x4.pb`
- rembg (isnet-general-use) mattes both shirts; the back's left-sleeve sliver hidden behind
  the front shirt is rebuilt from its own visible sleeve.
- Torsos lengthened below the print to real tee proportions (height ≈ 1.18 × width).
- 4x EDSR upscale; title block, partner block and paint splatters luminance-keyed.

Composition `hf/index.html` (20 s, SFX only, no music): hook "NO FILTER. JUST COLOUR." →
title slam → tee drops in spinning → detail whip-zooms (collar, CHERY, JETOUR, fabric) →
spin to back + "RUN LOUD LIVE BRIGHT" → turntable → front + back end card with partners.

Renders: `final/Colour-Rush-Tee-Ad-1080p.mp4` (16:9) and `final/Colour-Rush-Tee-Ad-9x16-1080x1920.mp4` (9:16), 20 s, 30 fps, -14 LUFS. Music: `scripts/colour_rush_music.py` (130 BPM, drops on 4.05 / 11.43 / 16.2). 9:16 project: `python3 scripts/colour_rush_build.py edits/colour-rush-ad` regenerates `hf-916/` from `hf/index.html`.
