# Majlis Perhimpunan dan Perarakan, Sambutan Maulidur Rasul 1448H (Melaka): highlights edit

Source: 4 iPhone 16 Pro Max clips (1920x1080, 29.97fps, HEVC HLG HDR), 25 Aug 2026 ~08:33 MYT,
Stadium Tun Fatimah, Melaka (GPS +2.2035 +102.2672). Total 72.6s raw. Downloaded from the client
Drive folder into `media/event-raw/` (git-ignored).

| Clip | Length | Content | Audio |
|---|---|---|---|
| IMG_8033 | 36.5s | 0-21 medium: speaker at podium + dais; 21-25 zoom-out; 25-36 wide grandstand (signage, banner, flags, MBMB mural) | protocol greetings (names) |
| IMG_8034 | 13.5s | speaker at podium, medium close | "...Nabi dan Rasul, insan agung yang membawa rahmat kepada seluruh alam, serta menjadi suri teladan terbaik dalam setiap sisi kehidupan umat manusia." |
| IMG_8035 | 14.3s | dais of dignitaries under the event banner (camera settles by 2s) | "...MADANI dihayati, ummah diberkati. Saya [?] tema ini bukan sekadar ungkapan untuk menghiasi sambutan, ia adalah seruan, supaya kita benar-benar menghayati nilai-nilai yang [diberkati?]" |
| IMG_8036 | 8.3s | dais of dignitaries, tighter | "Itulah yang ditunjukkan oleh Rasulullah SAW ..." (rest unclear, not used) |

Not in the footage: arrivals, the procession itself, audience/crowd, group photo, close-ups.

## Verified facts used on screen
- "MAJLIS PERHIMPUNAN DAN PERARAKAN", "1448H / 2026M", Melaka state crest: on-site banner.
- Theme "MADANI Dihayati, Ummah Diberkati" (Maulidur Rasul 1448H national theme): heard in the
  speech and confirmed by Bernama / Malay Mail / NST reports of 25 Aug 2026.
- Melaka state-level celebration with the procession starting at Stadium Tun Fatimah, Bukit
  Serindit on 25 Aug 2026: Bernama report of the day.
- Deliberately NOT used: speaker / VIP names (Whisper garbles them; who is on screen is not
  confirmed), participant numbers from news reports, any claim not on the banner or in the speech.

## Needs client confirmation before publishing
1. Organiser name + official logo: not supplied. End card has a logo slot (see below).
2. Caption words resolved by ear/ASR: "**serta** menjadi" (ASR variants: tetap/datang) and
   "setiap **sisi** kehidupan" (ASR heard "sesi"). Bite 2 caption ends at "nilai-nilai…" because the
   last two words are cut off at the end of the clip.
3. "Peringkat Negeri Melaka" comes from the Bernama report, not the (partly hidden) banner.

## Edit (41.4s, both formats share one EDL: `build/edl.py`)
| Timeline | Shot | Picture | Sound / graphics |
|---|---|---|---|
| 0.0-3.0 | h1 h2 h3 | beat-cut montage: banner+crest, speaker CU, dignitaries CU (punch-in flash on each cut) | VO "MADANI dihayati, ummah diberkati" from 8035; theme words rise as spoken; boom + bell hits |
| 3.0-4.2 | ramp | 8033 zoom-out speed-ramped 2x -> 5x (frame-blended) -> 3.3x | whoosh + riser |
| 4.2-9.1 | wide1 | wide grandstand, slow push (9:16: lateral pan) | title: Sambutan Maulidur Rasul 1448H/2026M · Majlis Perhimpunan dan Perarakan · Peringkat Negeri Melaka · Stadium Tun Fatimah, Bukit Serindit · 25 Ogos 2026 |
| 8.6-14.6 | spk | speaker (8034, lip-synced), 0.5s dissolve in | bite 1 + captions |
| 14.6-20.0 | vip1 | dignitaries listening (8036), slow glide | bite 1 continues |
| 19.4-25.4 | vip2 | dais under the banner (8035, synced), 0.4s dissolve | bite 2 + captions; lower third "Tema Sambutan: MADANI Dihayati, Ummah Diberkati" |
| 25.2-30.6 | dais | podium + dais (8033), slow pull | bite 2 ends |
| 30.6-36.6 | wide2 | wide grandstand pull-back, zoom-flash in | "Selamat menyambut · Salam Maulidur Rasul · 1448H / 2026M · theme" |
| 36.0-41.4 | end | navy end card with geometric star pattern | event title, level, venue, date; fade to black, music tail |

Grade (`build/prep_footage.sh`): HLG -> BT.709 with Mobius tone-map (natural skin, keeps highlights),
contrast +5%, saturation +5%, slight warm balance, light unsharp. No skin smoothing. 8034 stabilised
(vidstab, 3% zoom); other clips were already steady (measured < 0.3 px/frame jitter).

Audio (`build/mix_audio.py`): dialogue HPF 95 Hz, light FFT denoise, -2.5 dB at 280 Hz (PA boxiness),
+2.5 dB at 3.2 kHz, 2.5:1 compression, each bite matched to -18 LUFS. Music ducked -15 dB under
speech. Master -14 LUFS integrated, -1.5 dBTP (social platform target).

Music (`build/make_music.py`): original score synthesised for this edit, so no licence is needed.
100 BPM, D major, I-V-vi-IV; bar 1 lands on the title (4.2s), every section change is on a bar line.
To swap in a licensed library track, replace `hf/assets/audio/music.wav` (41.4s) and re-run the mix.
SFX: Pixabay Content License (`hf/assets/sfx/CREDITS.md`).

Type: Cormorant Garamond (titles) + Montserrat (labels, captions), both SIL OFL, bundled in
`hf/assets/fonts/`. Palette: navy #0b1d3a (stadium lettering), gold #d6b26a, ivory #fbf7ee.

## Rebuild
```bash
build/prep_footage.sh media/event-raw          # graded footage -> hf/assets/footage (git-ignored, ~7 min)
python3 build/make_music.py hf/assets/audio/music.wav
python3 build/mix_audio.py media/event-raw     # -> hf/assets/audio/mix.wav
python3 build/compose.py                       # -> hf/index.html, hf-vertical/index.html
(cd hf && npx hyperframes render -o ../renders/maulidur-rasul-1448h-melaka-16x9.mp4 --quality delivery --sdr)
(cd hf-vertical && npx hyperframes render -o ../renders/maulidur-rasul-1448h-melaka-9x16.mp4 --quality delivery --sdr)
```
(Paths relative to `edits/maulidur-rasul-melaka/`; the raw footage path is wherever the Drive
folder was downloaded.)

Adding the logo: save the official file as `hf/assets/logo.png`, uncomment the `<img id="org-logo">`
line in the end card in `build/compose.py`, re-run compose + render.
