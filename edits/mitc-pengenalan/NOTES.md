# Hotel MITC Melaka — Video Pengenalan (16:9)

Corporate intro for social media, all on-screen text in Malay.  Sources:
`MCORP_HOTEL_PROFILE_POSTER_2026.pdf` and https://mitchotel.com.my/ (photos, room types/sizes,
Asahan hours, address, phone).

Build (current, v3): `python3 scripts/mitc_build.py` → `hf/index.html` (styles in `style-v3.css`),
then in `hf/`: `npx hyperframes@0.8.174 render -q delivery -f 30 -o ../final/MITC-Pengenalan-v3-1080p.mp4`.
The v2 luxury cut is rebuilt with `scripts/mitc_build_v2.py` (`style-v2.css`) — both write `hf/index.html`.

## v3 — corporate hypermotion (current, `final/MITC-Pengenalan-v3-1080p.mp4`, 86 s, silent)
Requested after v2: "not interactive", wants hypermotion / motion graphics, more wow, more corporate; still no music.
- Navy / white / gold + electric blue, Inter Display (bundled .otf), grid backgrounds.
- Cuts: whip pans with motion blur + light streak, zoom-through, vertical whip, spin (`cut()`);
  photos get a speed-ramped push (fast then easing out).
- Chapter wipes: skewed navy panel with gold leading edge, giant outline number, kinetic word (`chapter()`).
- Kinetic type: 3D flying letters on "MITC", per-letter reveals, slot-machine digits for 15.11.2016 and 4/188/24 (`roll()`).
- Scenes: triple diagonal sweep into the title; light corporate panel with flipping M'Corp logo card;
  location map pin with pulse rings, callout tags and coordinates (2.27° U · 102.28° T); three stat cards;
  3D photo gallery for the halls; slat reveal for dining; AI room clips with spec chips; 12-tile 3D mosaic;
  end card with buttons and a cursor that clicks "TEMPAH SEKARANG".
- HUD from the first chapter to the recap: "HOTEL MITC" / "AYER KEROH · MELAKA" tags and a 4-segment
  chapter progress bar that fills as the film plays.
- Lower-thirds: blue kicker tag, white title plate with gold bar, navy sub-line, room spec chips.

### v3.1 polish (after feedback: some words ran off the frame, scenes too fast)
- Slower: 67.6 s → 86 s; transitions 0.28 s out / 0.65 s in; chapter wipes 0.5 s; lower-thirds hold longer.
- Overflow fixed (checked with `npx hyperframes inspect`): chapter titles 104 px at x 700, map tags wrap
  on two lines, map pin moved clear of "AYER KEROH,", mosaic title 92 px.
- Every full-screen photo is now an AI depth camera move too (`scripts/mitc_room3d.py`):
  ext-night dolly_in 6.0 s, ext-day crane_up 5.6, pool-2 push_right 4.4, pool-night orbit_left 3.0,
  lobby dolly_in 3.0, gadek push_left 3.0, gadek5 orbit_right 2.8, brisu-aerial dolly_in 2.8,
  bemban push_right 6.0, asahan-live orbit_left 3.0.
- UI feel: a cursor hovers each stat card (card lifts with a gold glow) and clicks "Dewan Gadek" in the
  3D gallery before zooming into it; sheen sweeps across lower-third plates, the logo cards and the end logo;
  drifting gold bokeh on the navy scenes; lower-thirds drift slowly while on screen.

| Root time | Scene |
|---|---|
| 0–4.2 | opening: "M'CORP HOTEL SDN. BHD. / PENGENDALI HOTEL MITC · MELAKA", diagonal sweeps |
| 4.2–10.0 | title over the night exterior (AI dolly), zoom-through out |
| 10.0–15.6 | korporat: logo card, "ANAK SYARIKAT PKNM · DITUBUHKAN 15.11.2016" |
| 15.6–21.0 | lokasi: "AYER KEROH, MELAKA", MITC + 10 minit dari Tol Ayer Keroh |
| 21.0–26.3 | 4★ / 188 bilik / 24 jam cards, cursor hover |
| 25.8–35.9 | 01 FASILITI: kolam renang ×2, lobi utama |
| 35.4–47.9 | 02 DEWAN & ACARA: 3D gallery + click, Dewan Gadek, Bilik Gadek 5, Halaman Brisu |
| 47.4–56.4 | 03 TEMPAT MAKAN: slats, Restoran Bemban, Asahan Cafe |
| 55.9–75.7 | 04 BILIK & SUITE: 8 AI camera-move clips, 5 room types |
| 75.7–79.7 | mosaic "SEGALANYA DI SATU DESTINASI" |
| 79.7–86.0 | end card, button click, contacts, M'Corp Hotel + MCORP logos |

## v2 — luxury cut (`scripts/mitc_build_v2.py`, superseded)
Requested after v1: look more stylish / luxurious, less basic; drop "MEMPERSEMBAHKAN";
"Di jantung Ayer Keroh" sounded wrong; **no music** (audio is added on the platform), so the
render is silent.
- Letterbox bars (70 px), Cormorant Garamond serif + Montserrat light tracked caps, gold hairlines.
- Slow cross-dissolves, letter-by-letter title reveals, no flashes / zoom-blur / pop SFX.
- Grade, vignette and film grain are applied to the whole render by `scripts/mitc_finish.sh`
  (warm, -10% saturation, soft vignette until the end card, luma grain; two-pass 9.5 Mbit/s, silent).
  Per-element `data-color-grading` was tried first but pushed the HyperFrames render past 25 min.
  Render: `npx hyperframes@0.8.174 render -q delivery -f 30 -o ../final/_raw-v2.mp4` in `hf/`, then
  `scripts/mitc_finish.sh edits/mitc-pengenalan/final/_raw-v2.mp4 edits/mitc-pengenalan/final/MITC-Pengenalan-v2-1080p.mp4`.
- Corporate scene on an ivory panel; Asahan as a diptych; closing triptych
  "Di mana keselesaan bertemu keanggunan."; ivory end card with gold frame.

| Root time | Scene | On-screen |
|---|---|---|
| 0–3.0 | intro | "M'CORP HOTEL SDN. BHD." between gold hairlines |
| 3.0–8.0 | title | night exterior, "SELAMAT DATANG KE / HOTEL MITC / AYER KEROH · MELAKA", 4 stars |
| 8.0–12.8 | korporat | M'Corp Hotel logo, "ANAK SYARIKAT PKNM", "Ditubuhkan pada 15 November 2016" |
| 12.8–17.0 | lokasi | "Ayer Keroh, Melaka" — opposite MITC, 10 min from Ayer Keroh toll |
| 17.0–20.8 | statistik | 4★ / 188 bilik penginapan / 24 jam perkhidmatan |
| 20.8–29.2 | I Fasiliti | kolam renang, kolam waktu malam, lobi utama |
| 29.2–39.4 | II Dewan & Acara | Dewan Gadek (+gold logo), Bilik Gadek 5, Halaman Brisu |
| 39.4–47.8 | III Tempat Makan | Restoran Bemban, Asahan Cafe (diptych) |
| 47.8–67.2 | IV Bilik & Suite | AI camera-move clips: Superior Double, Superior Twin, Deluxe, Junior Suite ×2, Executive Suite ×3 |
| 67.2–71.2 | triptych | "Di mana keselesaan bertemu keanggunan." |
| 71.2–76.4 | penutup | MITC logo, "Tempah terus dengan kami", 06-233 1551 · mitchotel.com.my, address, M'Corp Hotel + MCORP logos |

## Media
- Photos: website uploads (`media/mitc/web`, not in git) resized to ≤2400 px in `hf/assets/img`.
  The exterior day shot and Executive Suite bedroom come from the PDF at full resolution;
  `room-*.jpg` are the sources of the AI room clips.
- The AI-generated host from the poster is not used (requested).
- Room clips (`hf/assets/video/*.mp4`, not in git): `scripts/mitc_room3d.py` — Depth Anything V2 Small
  depth map per photo, then a 2.5D camera move (dolly in/out, orbit, crane, push) rendered with OpenCV.
  Regenerate with:
  `python3 scripts/mitc_room3d.py edits/mitc-pengenalan/hf/assets/video IMG:MOVE:SECONDS ...`
  (double push_right 4.2 s, twin orbit_left, deluxe dolly_in, junior crane_up, junior-2 orbit_right,
  exec dolly_in 3.4 s, exec-2 push_left, exec-bath pull_out; 3 s unless noted).
- Fonts: Cormorant Garamond, Montserrat (OFL, `hf/assets/fonts`).

## v1 (superseded)
Bold condensed type, flashes, beat-synced MusicGen bed and SFX (commit eb6de26).
