# MITC: promo reel (9:16, no voiceover)

32.9 s, 1080x1920 (v2), HyperFrames project in `hf/` (single `hf/index.html`). Content follows the MITC
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
- `hf/assets/video/` is git-ignored; recreate the award clip with:
  `ffmpeg -ss 24 -t 9 -i MITC_BOTY_2026-1.mp4 -an -vf scale=1280:720 -c:v libx264 -crf 20 -g 25 -keyint_min 25 -pix_fmt yuv420p -movflags +faststart hf/assets/video/award.mp4`
  (source: https://site.mitc.org.my/wp-content/uploads/2026/02/MITC_BOTY_2026-1.mp4).
- Final export (`final/MITC-Promo-v1.mp4`): loudnorm -14 LUFS, then a true-peak limiter; measured
  -13.6 LUFS, -1.9 dBTP.

## Revision 1
- Pillar chips now arrive one per photo cut and light up yellow while that photo is on screen,
  so the 01/02 cards no longer read as the same frame twice.
- Ballroom photo was used in both the hook and pillar 01: hook now uses the banquet photo, pillar 03
  uses the lobby digital-screen photo.

## Revision 2 (music + SFX)
- Music replaced: "Driving Ambition" by Ahjay Stelino (Mixkit, genre Film Score / corporate,
  https://assets.mixkit.co/music/32/32.mp3, Mixkit Stock Music Free License). 100 BPM, beat 0.6002 s.
  `assets/bgm/bed.wav` = 35.5225-60.67 s (build -> drop at 38.485 lands on the logo reveal, video 2.962 s)
  + 93.08 s-end (ending phrase, last chord 96.07 s lands on the outro, video 28.137 s), 80 ms crossfade
  on a beat, loudnorm -16 LUFS.
- Whole composition retimed by K = 0.6002/0.545 (old beat grid -> new), outro shifted -0.056 s onto
  the final chord; total 32.8 s. All times in the storyboard above scale by K.
- Sound design re-done with synthesized SFX (`scripts/mitc_sfx.py`, deterministic) in `hf/assets/sfx/`:
  text hits on each hook line, reverse swell + cinematic boom on the drop / awards / outro, big
  whoosh into each pillar and the location, swish on every photo cut, ascending blips on the chips
  and badges, shimmer on logo and badges, thud on the pin landing. The old Pixabay set was removed.
- Final: `final/MITC-Promo-v2.mp4`, -14.7 LUFS, -2.8 dBTP.

## Revision 3 (TikTok b-roll, 43.6 s)
- Photo `ballroom.jpg` is actually the exhibition hall (Dewan Pameran) dressed for an event: relabelled.
- B-roll from MITC's TikTok (@mitcmelaka1), cut by `scripts/mitc_clips.sh` into `hf/assets/clips/`.
  Rules: no on-screen captions/title cards, no presenters or talking heads, only 720p+ sources, each
  in-point on the sharpest window of the shot (Laplacian variance per frame). 576p uploads dropped.
- Structure: hook (gala stage, star arch) -> brand (exterior) -> location (aerial) -> 01 Dewan Pameran /
  Grand Ballroom / Maharani Ballroom -> 02 meeting + VIP -> "Satu Venue, Pelbagai Acara" (Pameran Hang
  Tuah 4K, gala dinner Hall B, Maharani pelamin/akad) -> 03 services (Dekorasi, Teknikal & Wi-Fi,
  Signage, Pasukan Berpengalaman) -> awards -> outro (final chord 38.94 s).
- Music re-cut: 35.5225-71.47 s + 93.08 s-end (offset 36 beats), drop on the logo at 2.962 s.
- `storyboard-v3.jpg`: one frame per shot. Final `final/MITC-Promo-v3.mp4`, 43.7 s, -14.4 LUFS, -2.2 dBTP.

## Revision 4 (hypermotion corporate cut, 55.7 s, no SFX)
- Built by `scripts/mitc_build.py` from `style.v4.css` + `timeline.v4.js` (all times derive from the
  beat grid there). Music only: bed.wav = Driving Ambition 26.481-74.47 s + 93.08 s-end; drop at
  12.004 s, final chord at 50.983 s.
- 0-12 s MITC introduction over the build: name, 3.1 ekar, 13,090 m2 (site.mitc.org.my/about),
  3 Dewan Pameran (Hall A/B/C) · 6 Bilik Mesyuarat · 1 Grand Ballroom (venue page), "Think MICE,
  Think MITC!" with an accelerating zoom into the facade sign (exterior-hi.jpg, sign at 2082,1012 px).
- Sections 01 Dewan Pameran (8 shots), 02 Konvensyen & Mesyuarat, 03 Ballroom (3 shots only),
  04 Perkhidmatan Bersepadu; transitions zoom / whipL / whipU / spin / push3d on untimed wrappers,
  punch-in + drift on every shot, HUD frame, light leaks; awards now include CMIEA 2025.
- New hall clips (GoTravel Expo, Karnival Kerjaya TVET, Hang Tuah houses, Grand Ballroom 2nd angle,
  logo-bg) in `scripts/mitc_clips.sh`; hook-star limited to its sharp 6.6-8.4 s window.
- `storyboard-v4.jpg`; final `final/MITC-Promo-v4.mp4`, -13.8 LUFS, -2.8 dBTP.
