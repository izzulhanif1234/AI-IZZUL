# MITC: promo reel (9:16, no voiceover)

29.8 s, 1080x1920, HyperFrames project in `hf/` (single `hf/index.html`). Content follows the MITC
poster "Pusat Konvensyen & Acara Perniagaan Bertaraf Antarabangsa" plus facts from site.mitc.org.my.
No voiceover (requested). Music plus kinetic text only.

## Storyboard (cuts on the music's beat grid: beat 0.545 s, downbeats 0.51 + 2.18k)
| Root time | Scene | On screen | Photo |
|---|---|---|---|
| 0-2.69 | hook | "Cari venue / bertaraf / ANTARABANGSA / di Melaka?" one line per beat | banquet hall |
| 2.69-7.05 | brand | Persidangan · Pameran · Acara Korporat, MITC globe logo, then the poster headline + EN line | building exterior |
| 7.05-9.23 | location | pin drop, "Ayer Keroh, Melaka", "Di tengah-tengah destinasi pelancongan utama Melaka" | aerial |
| 9.23-13.59 | 01 Ruang Acara Fleksibel | chips follow the photo: Dewan Pameran / Ballroom / Majlis Perkahwinan | exhibition hall, ballroom, wedding hall |
| 13.59-17.95 | 02 Kemudahan Profesional | chips: Bilik Mesyuarat / Bilik VIP / Bilik Lembaga Pengarah | meeting room, function room, lounge |
| 17.95-21.22 | 03 Perkhidmatan Bersepadu | "Sokongan profesional dari perancangan hingga hari acara anda." | lobby digital screen, al fresco |
| 21.22-25.6 | awards | "Diiktiraf", BrandLaureate ceremony clip, ASEAN MICE Venue Standard x2 (2026-2028), BrandLaureate BestBrands (MICE Venue 2025-2026) | |
| 25.6-29.8 | outro | logo, "Lebih daripada sebuah venue", "Destinasi untuk acara luar biasa", CTA, 06-233 3330 / 019-223 8622, generalinfo@mitc.org.my, site.mitc.org.my, address | #mitc signage |

## Media
- Photos, logo, award badges and `assets/video/award.mp4` (24-33 s of MITC_BOTY_2026-1.mp4) come from
  site.mitc.org.my (wp-content/uploads). Photos downscaled to <=2400 px.
- Music: "Raising Me Higher" by Ahjay Stelino, Mixkit (https://assets.mixkit.co/music/34/34.mp3),
  Mixkit Stock Music Free License (commercial use, no attribution needed). `assets/bgm/bed.wav` =
  0-18.40 s + 81.62 s-end of the track, 60 ms crossfade at a beat-matched point (onset correlation),
  loudnorm -16 LUFS. The edit lands on the track's bigger section at 18.4 s; last hit 25.6 s = outro.
- SFX: bundled Pixabay library (`hf/assets/sfx/CREDITS.md`).
- Final export loudness-normalised to -14 LUFS with ffmpeg after render.

## Revision 1
- Pillar chips now arrive one per photo cut and light up yellow while that photo is on screen,
  so the 01/02 cards no longer read as the same frame twice.
- Ballroom photo was used in both the hook and pillar 01: hook now uses the banquet photo, pillar 03
  uses the lobby digital-screen photo.
