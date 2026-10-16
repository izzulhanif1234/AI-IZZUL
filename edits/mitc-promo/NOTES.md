# MITC Melaka: 30s promo "WHERE BIG IDEAS BECOME BIG EVENTS."

Client storyboard (6 scenes) built as written, in 16:9 (`hf/`, corporate screens) and 9:16
(`hf-vertical/`, social), both generated from one EDL in `build/compose.py`.

## Sources (all real MITC material)
- Photos: official MITC media library, site.mitc.org.my (WordPress API `wp-json/wp/v2/media`).
  `build/prep_photos.sh` re-downloads and grades the 18 used (paths listed in the script).
  Assets in `hf/assets/photos/` are git-ignored.
- Logo: official `Logo-color-01.png` from the same library (globe logo, matches the client poster), unaltered.
- Copy: client storyboard + client poster (PERSIDANGAN · PAMERAN · ACARA KORPORAT; Pusat Konvensyen &
  Acara Perniagaan Bertaraf Antarabangsa / Premier International Convention & Business Events Centre;
  Versatile Event Spaces / Professional Facilities / Integrated Event Services).
- Space labels in scene 4 (Dewan Pameran, Auditorium, Ballroom, Bilik Mesyuarat) are spaces named on
  the poster and shown in the gallery photos.
- Palette sampled from the poster: navy #263353, teal #21798b, gold #e8bc38, white.

## Edit (30.0s, cuts on a 120 BPM grid)
| Time | Scene | Pictures | Graphics / transitions |
|---|---|---|---|
| 0-4 | Hook | black + impact, #mitc building zoom-in, stage lights, gala hall, stage, gala hall | ONE VENUE. / ENDLESS POSSIBILITIES. (kinetic letters) |
| 4-8 | Brand | navy, gold light beams, flare | logo from light, MITC MELAKA scale-up, 3 words one by one |
| 8-13 | Think bigger | aerial (3D dolly + gold particle parallax), empty exhibition hall | masked title + gold italic subtitle, whip pan at 12.75 |
| 13-18 | More than a venue | exhibition booths (swipe), auditorium (fast zoom), ballroom (beat), meeting room (lateral) | space labels; 3 poster cards with icons, motion-blur exit |
| 18-24 | Experience | banquet set-up, trade fair, boardroom, gala (speed ramp) -> stage (match cut), 4-shot montage, dip to black | FROM STRATEGIC MEETINGS… / …TO GRAND-SCALE EVENTS. |
| 24-30 | Closing | MITC convention centre facade, slow push, warm flare | YOUR EVENT. OUR EXPERTISE. -> logo + gold line -> MITC MELAKA + English tagline; final hit, fade |

Music (`build/make_music.py`): original synthesised cinematic-corporate score (no licence needed):
impact from black, ticking build, metallic logo hit, drop at 8s, four accented hits 13-16s, peak,
silence 23.5-24s, half-time finale with braams, final hit at 29s. SFX: whooshes (Pixabay licence).
Master -14 LUFS.

## Rebuild (from `edits/mitc-promo/`)
```bash
build/prep_photos.sh
python3 build/make_music.py hf/assets/audio/music.wav && python3 build/mix_audio.py
python3 build/compose.py
(cd hf && npx hyperframes render -o ../renders/mitc-promo-16x9.mp4 --quality delivery --sdr)
(cd hf-vertical && npx hyperframes render -o ../renders/mitc-promo-9x16.mp4 --quality delivery --sdr)
```
