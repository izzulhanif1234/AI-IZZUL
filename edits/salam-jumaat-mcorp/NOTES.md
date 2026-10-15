# Salam Jumaat (MCORP): Islamic motion poster

1080x1350 (4:5 feed), 42s, HyperFrames (`build/compose.py` -> `hf/index.html`).
Source: client Drive folder (git-ignored `media/jumaat-raw/`): DJI drone clip pulling back from the
MCORP sign (4K60, 7.8s) + 9 drone photos of the Perbadanan Melaka HQ.

## Copy (client's, verbatim)
JUMAAT YANG DIBERKATI | MCORP · Firman Allah SWT · Ar-Ra'd 13:11 (Arabic + Malay translation) ·
three message paragraphs. Added by us: the Arabic greeting "جُمُعَة مُبَارَكَة" (= Jumaat yang
diberkati) over the title; gold emphasis on key phrases of the paragraphs (wording unchanged).

## Sequence
| Time | Scene |
|---|---|
| 0-3 | gold 16-point rosette draws itself, lanterns drop in, rosette flies through as a mihrab arch opens on the drone shot of the MCORP sign; title lands by 2.6s |
| 3-8 | drone pull-back (0.5x) inside the arch, title lockup |
| 8-18 | "Firman Allah SWT", ayat revealed word by word (right to left), translation, citation; music held to drone + choir |
| 18-34.6 | three message panels over Ken Burns HQ photos, word-by-word reveal, gold light sweeps between |
| 34.6-42 | arch returns on the wide HQ shot: greeting, title, MCORP logo plaque (official logo, unaltered, on cream) |

Visual system: emerald #0b4433 / #041d16, gold gradient (#fff1b8 -> #a77b25), cream #f8f0dc;
girih lattice (8-point khatam), lanterns, gold dust. Fonts (SIL OFL): Amiri Quran (ayat), Amiri,
Cinzel, Montserrat.

Music (`build/make_music.py`): original, synthesised in maqam Hijaz on D: ney, oud and qanun
(Karplus-Strong), daf, drone, choir pad. Quiet and still under the verse. Soft whooshes on the light
sweeps (Pixabay licence). Master -14 LUFS.

## Rebuild (from `edits/salam-jumaat-mcorp/`)
```bash
build/prep_media.sh media/jumaat-raw
python3 build/make_music.py hf/assets/audio/music.wav && python3 build/mix_audio.py
python3 build/compose.py
(cd hf && npx hyperframes render -o ../renders/salam-jumaat-mcorp-4x5.mp4 --quality delivery --sdr)
```
