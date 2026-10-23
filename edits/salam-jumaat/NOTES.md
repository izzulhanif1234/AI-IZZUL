# Salam Jumaat — MCORP (Remotion, 9:16)

32 s, 1080x1920, 30 fps, for Reels / TikTok / Shorts / Story. Tema ornamen Islamik:
zamrud gelap + emas, bintang lapan (Rub el Hizb), bingkai mihrab, frieze bintang,
habuk emas. Transisi antara babak = "star wipe" (bintang lapan membesar dari tengah).

```
npm i
npm run studio      # Remotion Studio: semua teks boleh diubah di panel props
npm run render      # -> final/salam-jumaat-9x16.mp4
```

Teks (ayat, terjemahan, doa, kata kunci) ialah props dalam `src/schema.ts`, jadi minggu
depan cukup tukar teks di Studio atau `--props`. `muzik: false` buang muzik latar.

## Babak
| Masa | Babak | Isi |
|---|---|---|
| 0.0–5.5 | intro | Medalion Rub el Hizb dilukis emas, "جمعة مباركة" di tengah, SALAM / JUMAAT (huruf naik + kilauan emas) |
| 4.7–14.0 | ayat | Star wipe -> tingkap mihrab (dron tarik ke belakang dari logo MCORP), ayat Arab didedah kanan->kiri, terjemahan perkataan demi perkataan, Surah Al-Ma'idah ayat 2 |
| 13.2–20.9 | doa1 | Montaj dron (pintu masuk -> menara + bukit -> pintu masuk) di jalur atas, bingkai mihrab penuh, "Ya Allah," + doa, "Melaka" emas |
| 20.1–28.0 | doa2 | Kurniakan / KEMAJUAN, / KEMAKMURAN / dan / KESEJAHTERAAN — setiap kata kunci = potongan foto + kilatan emas + chime |
| 27.2–32.0 | end | Bangunan MCORP (langit biru) dalam mihrab, logo atas plak gading, SALAM JUMAAT + جمعة مباركة |

Masa babak: `src/theme.ts` (`SCENES`). Ornamen: `src/ornaments.tsx`. Kesan: `src/effects.tsx`.

## Media (tidak dalam git — `media/` di-ignore)
Folder Drive `17mbbzm-Sk5vFVR_kfPBzbvE3DFD4WBga` (gdown --folder) -> `media/jumaat-src/`, kemudian:
- foto dron 8064x4536 -> `public/media/drone1..9.jpg` (4096x2304, ikut susunan nama fail)
- `bangunan MCORP` -> `public/media/bangunan.jpg`; `logo MCORP` (PNG lutsinar, trim) -> `public/media/logo.png`
- `dji_fly_..._0246` (11.5 s, pintu masuk) -> `public/media/drone_entrance.mp4` (scale=-2:1920, 30 fps, x264 crf 19)
- `dji_fly_..._0247` (7.8 s, logo) -> `public/media/drone_logo.mp4` (2560x1440, 30 fps, crf 18)
- Fon (Amiri, Cinzel, Cormorant Garamond, Montserrat) dimuat turun ke `public/fonts/`, dimuat via FontFace dalam `src/fonts.ts`.

## Audio
- Muzik latar: MusicGen-small (`scripts/musicgen_long.py`, seed 7, prompt "peaceful middle eastern ambient music,
  soft oud melody over warm string pad, slow tempo, spiritual and hopeful, cinematic, no drums"). Generasi pertama
  pudar sendiri ~26 s dan sambungan pecah selepas 50 s, jadi `bed.wav` = 0–26 s + crossfade 3 s ke 2–12 s
  (33 s), loudnorm -18 LUFS. Volum 0.6 dalam video, fade masuk 1 s / keluar 1.7 s.
- Eksport akhir: render Remotion, kemudian loudnorm 2-pass ke -14 LUFS / -1.5 dBTP (video `-c:v copy`).
- `final/cover.jpg` = frame 4.2 s (intro) untuk thumbnail/cover.
- SFX Pixabay (`public/sfx/CREDITS.md`): whoosh-short pada setiap star wipe, sparkle pada intro & end card, chime lembut pada 3 kata kunci.
