# MCORP — Anak Syarikat Logo Montage (new project)

Source: `source-logos.png` (the strip of 11 subsidiary logos, 1920x1080, logos ~75 px tall).
Prep: `python3 scripts/logo_montage_prep.py source-logos.png hf/assets/logos EDSR_x4.pb`
cuts each logo, upscales 4x with OpenCV EDSR super-res (model: Saafke/EDSR_Tensorflow
`EDSR_x4.pb`, not stored in the repo), and keys the white background to alpha.

14 s, 1920x1080, 30 fps, HyperFrames (`hf/index.html`), SFX only (no music, so it drops
into a montage under your own track). Render: `final/MCORP-Anak-Syarikat-Logo-Montage-1080p.mp4`.

| Time | Beat |
|---|---|
| 0–1.5 | Warp-speed intro: "KUMPULAN SYARIKAT / ANAK SYARIKAT / MCORP", camera punches through |
| 1.4–7.9 | 11 logo hits, one every 0.58 s: whip-pan in from alternating sides, flash + shake, "01 / 11" tag |
| 8.0–9.7 | All 11 cards crash in from depth into a 4-4-3 wall, wall tilts flat |
| 9.3–14 | Title "ANAK SYARIKAT MCORP" slams in, light sweep, wave pulse, slow push |

Background: starfield streaks that surge on every hit, rotating red/blue light rays,
racing neon floor grid, pulsing red/blue orbs, drifting outline "MCORP" text.

Order: Invest Melaka, MITC, Melaka Sentral, PMH, MCS, MCORP Technology, M'Corp Hotel,
PMPC, MBSB, PM Multilink, Melaka Halal Hub (change `LOGOS` in `hf/index.html`).
Hit times are `HIT0 + i*STEP`; move the matching `sfx-hNN` audio starts if STEP changes.
