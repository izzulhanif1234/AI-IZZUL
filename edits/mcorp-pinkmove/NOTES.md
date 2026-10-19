# MCORP Pink Move 2026 — Teaser 15 s (16:9)

Teaser for the poster "MCORP PINK MOVE 2026" (Zumba • Fitness • Awareness,
27 Oktober 2026, 5.00 petang, Lobi MCORP). Built in **Remotion** (first
Remotion project in this repo; the others are HyperFrames) using the vendored
Remotion skills in `.claude/skills/`.

- Studio: `cd remotion && npm i && npm run dev`
- Render: `npx remotion render PinkMoveTeaser out/teaser.mp4 --concurrency=4 --crf=16 --audio-bitrate=320k`
- Master: the render's audio through `alimiter=limit=0.84` (video stream copied)
  → `final/MCORP-PinkMove-Teaser-v1-1080p.mp4` (-12.3 LUFS, -1.2 dBTP).

## Timeline (30 fps, 450 frames, cuts on the 120 BPM beat grid)
| Time | Scene (`src/scenes/`) | On-screen | Audio |
|---|---|---|---|
| 0–3 s | `Opening` | Plain pink ribbon streams in and ties itself into the awareness loop, turns into the client's pink ribbon, flies beside 2026. MCORP zoom-punch at 0.5 s + shake, PINK / MOVE slide in, 2026 stamps at 1.5 s, pink light leak | whoosh + swoosh + riser, bass hit 0.5 s & 1.5 s |
| 3–6 s | `Tagline` | ZUMBA • FITNESS • AWARENESS one per beat in a maroon pill, "~ Satu Rentak, Seribu Semangat ~" writes on, participants rise in | whip per word |
| 6–11 s | `Info` | Tarikh / Masa / Tempat cards slide in over the MCORP building; animated calendar, clock to 5:00, pin drop | ding when the date lands (6.4 s) |
| 11–13 s | `DressCode` | Maroon TeamSync Retreat tee drops in; tudung pink example in a ring | thump, whip |
| 13–15 s | `Mandatory` | Logo plate with two ribbons, "KEHADIRAN SEMUA WARGA KERJA MCORP", ADALAH **DIWAJIBKAN** rubber stamp at 13.5 s | music dips 13.2–13.5 s, riser → bass hit |

Every cut (3, 6, 11, 13 s) is a custom `pinkSlash` transition (`src/fx.tsx`) centred
on the cut with a swoosh peaking on it; middle scenes carry 5 extra frames each side.

## Assets (`remotion/public/`)
- `img/title-pink|move|2026.png`: the poster's own brush lettering, keyed out by
  `scripts/pinkmove_letters.py` (no font matches it; Knewave/Permanent Marker etc. were tried).
- `img/pink-ribbon.png`: client-supplied ribbon (Google screenshot in the Drive folder),
  keyed off white with the separator gaps refilled white.
- `img/building.jpg` (client upload), `img/shirt.png` (client photo, background removed
  with rembg isnet), `img/people-cut.png` / `img/woman.jpg` (participants cropped from
  the poster, cut out with rembg `u2net_human_seg`), `img/logo.png`.
- The first "bangunan MCORP" upload in Drive was actually an MITC brochure; replaced.
- `audio/music.wav`: MusicGen-small, prompt "high energy zumba fitness dance music, latin
  house, congas and timbales…", 120.4 BPM stretched to exactly 120 and trimmed to start on
  a downbeat, so beat k falls on frame 15k.
- `audio/bass-hit|swoosh|riser.wav`: synthesized by `scripts/pinkmove_sfx.py`;
  `whoosh|whip|ding.wav` from remotion.media (listed in the remotion-markup sfx rule).
- Fonts are local woff2 copies (Kanit 800/900 italic, Montserrat 700–900, Kaushan Script)
  because headless Chrome here rejects the proxy's certificate for fonts.gstatic.com.

## Render notes
- `lightLeak()` needs WebGL2; `remotion.config.ts` uses `swangle` (software ANGLE) because
  `angle`, `egl` and `swiftshader` could not create a WebGL2 context in this container.
- Full 1080p render takes ~4.5 min on 4 cores.
