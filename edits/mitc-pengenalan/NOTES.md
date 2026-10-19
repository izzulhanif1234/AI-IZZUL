# Hotel MITC Melaka — Video Pengenalan (16:9)

Corporate intro for social media, all on-screen text in Malay, no voiceover (music + SFX +
kinetic type, so it reads with the sound off).  Sources: `MCORP_HOTEL_PROFILE_POSTER_2026.pdf`
and https://mitchotel.com.my/ (photos, room types/sizes, Asahan hours, address, phone).

Build: `python3 scripts/mitc_build.py` → `hf/index.html` (styles in `style.css`).
Cut points live in `RAW` in the build script and snap to the music beats in
`hf/assets/bgm/beats.json` when present.

## Order (68.4 s, cuts on the beat; section openers on bar lines after the drop)
| Root time | Scene | On-screen |
|---|---|---|
| 0–2.58 | intro | "M'CORP HOTEL SDN. BHD. / MEMPERSEMBAHKAN" |
| 2.58–6.52 | title | night exterior, "HOTEL MITC / MELAKA", 4 stars |
| 6.52–10.95 | korporat | "ANAK SYARIKAT", M'Corp Hotel logo, "Ditubuhkan oleh PKNM pada 15 NOVEMBER 2016", operates Hotel MITC |
| 10.95–14.40 | lokasi | "DI JANTUNG AYER KEROH", opposite MITC, 10 min from Ayer Keroh toll |
| 14.40–18.34 | statistik (music drop) | 4★ / 188 bilik / 24 jam count-ups |
| 18.34–26.22 | 01 FASILITI | kolam renang (3 shots), lobi utama |
| 26.22–34.10 | 02 DEWAN & ACARA | Dewan Gadek (+logo), Bilik Gadek 5, Halaman Brisu (+logo) |
| 34.10–41.99 | 03 TEMPAT MAKAN | Restoran Bemban, Asahan Cafe |
| 41.99–59.72 | 04 BILIK & SUITE | AI camera-move clips: Superior Double, Superior Twin, Deluxe, Junior Suite ×2, Executive Suite ×3 (types and sizes from the website) |
| 59.72–63.66 | rumusan | 7-tile grid "SEGALANYA DI SATU DESTINASI" |
| 63.66–68.40 | penutup | MITC logo, "Tempah terus dengan kami!", 06-233 1551, mitchotel.com.my, address, M'Corp Hotel + MCORP logos |

## Media
- Photos: website uploads (`media/mitc/web`, not in git) resized to ≤2400 px in `hf/assets/img`.
  The exterior day shot and Executive Suite bedroom come from the PDF at full resolution; `room-*.jpg` are the sources of the AI room clips.
- The AI-generated host from the poster is not used (requested).
- Room clips (`hf/assets/video/*.mp4`, not in git): `scripts/mitc_room3d.py` — Depth Anything V2 Small
  depth map per photo, then a 2.5D camera move (dolly in/out, orbit, crane, push) rendered with OpenCV.
  Regenerate with:
  `python3 scripts/mitc_room3d.py edits/mitc-pengenalan/hf/assets/video IMG:MOVE:SECONDS ...`
  (moves used: double push_right, twin orbit_left, deluxe dolly_in, junior crane_up,
  junior-2 orbit_right, exec dolly_in, exec-2 push_left, exec-bath pull_out; 3 s each, double 4.2 s, exec 3.4 s).
- Fonts: Oswald, Montserrat, Playfair Display (OFL, `hf/assets/fonts`).
- SFX: Pixabay library copied from the earlier MCORP projects (`hf/assets/sfx/CREDITS.md`).
- Music: MusicGen-small take "epicB" (`scripts/musicgen_long.py epicB.wav 30 "uplifting modern corporate
  anthem, driving percussion, piano and strings, cinematic, energetic, confident, premium brand video, 120 bpm" 21`),
  ~121.8 bpm. `scripts/mitc_music.py` trims it so the drop lands on the stats scene, jumps back 12 bars
  at film 43.96 s (the take breaks up after ~49 s), loudnorm -14 LUFS, writes `bed.wav` + `beats.json`.
