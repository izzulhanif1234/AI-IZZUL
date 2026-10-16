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

Render: `final/Colour-Rush-Tee-Ad-1080p.mp4` (20 s, 1080p30, -14 LUFS).
