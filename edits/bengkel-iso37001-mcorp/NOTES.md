# Bengkel Transisi MS ISO 37001:2016 kepada MS ISO 37001:2025 (MCORP): 60s highlights

Source: 12 clips, DJI Osmo Pocket 4, 3840x2160 29.97fps HEVC 10-bit BT.709, 13 Oct 2026 08:58-09:20,
~100s total. Client Drive folder downloaded to `media/prog2-raw/` (git-ignored); `cNN` = Drive order.

| Clip | Len | Content |
|---|---|---|
| c01 | 8.5 | MCORP programme book on blue table, tilt up to participants |
| c02 | 9.6 | door sign, fast slide past into seminar room; emcee + title slide |
| c03 | 5.9 | participants at tables, pan |
| c04 | 5.7 | COO (pink shirt) seated, reading |
| c05 | 6.7 | emcee at mic in front of the title slide, pulls back to the room |
| c06 | 6.7 | man in black reading at the front (darker exposure, +0.5 EV) |
| c07 | 6.7 | participants, women at tables |
| c08 | 6.8 | COO giving Ucapan Aluan, slide with name/title behind |
| c09 | 17.2 | long participant pan, several good faces / laptops |
| c10 | 8.8 | SIRIM Academy trainer presenting "ISO 37001:2025 Awareness" |
| c11 | 8.5 | trainer over participants' shoulders |
| c12 | 9.1 | monitor showing "Tentatif Bengkel", fast pan to the full room |

## Facts on screen (all read off slides in the footage)
- Title slide: "Bengkel Transisi MS ISO 37001:2016 kepada MS ISO 37001:2025, Perbadanan Melaka
  Tahun 2026"; Perunding: En. Kanakaraja Muthusamy; 8.30 pagi - 5.00 petang; Bilik Seminar, Aras 11,
  MCORP; logos MCORP + SIRIM.
- Ucapan Aluan slide: YBrs. Tuan Muhammad Ridzwan Yap bin Abdullah, Ketua Pegawai Operasi,
  Perbadanan Melaka (MCORP).
- SIRIM slide: "ISO 37001:2025 Awareness", Trainer Name: Kanakaraja Muthusamy, SIRIM Academy.
- Tentatif: 13 (Selasa), 14 (Rabu), 15 (Khamis) Oktober 2026; "Penambahbaikan & Pemurnian
  Dokumen ABMS"; document types Manual ABMS, Pelan Risiko Bahagian/Jabatan, Polisi-Polisi ABMS,
  Prosedur Kerja.
- Logo: official file from mcorp.gov.my (`hf/assets/img/mcorp-logo.png`), used unaltered on a
  white card (its navy wordmark disappears on dark backgrounds). Brand colours sampled from it:
  red #ec1c24, blue #2b3990.
- Not named on screen: the emcee, the man reading in c06 (role unknown), participants.

## Edit (60.0s, 1920x1080, `build/compose.py`)
Music 120 BPM, bars every 2s from the drop at 3.0s. Cuts on beats, sections on bar lines.

| Time | Section | Shots | Graphics |
|---|---|---|---|
| 0-3 | Hook | 6 punch-ins, 0.5s each (slide, COO, trainer, 3 participants) with flash-cut | "Bengkel Transisi / MS ISO 37001:" year rolls 2016 -> **2025** (red) |
| 3-11 | Title | c01 book (impact zoom on the drop) -> tilt up; c02 door-sign whip into room | kicker Perbadanan Melaka · Tahun 2026, BENGKEL TRANSISI, 2016 -> 2025 pills, Tarikh / Tempat |
| 11-23 | Day one | zoom-through into emcee, reading, COO seated, COO speech | "Hari Pertama · 13 Oktober 2026"; lower third Ucapan Aluan |
| 23-37 | Briefing | trainer, over-shoulder, participants (dissolve in) | lower third Taklimat Standard ISO 37001 / En. Kanakaraja Muthusamy / Perunding · SIRIM Academy |
| 37-47 | Montage | 6 participant cuts (1s), tentatif screen, sped room pan (1.5x) | "Penambahbaikan / & Pemurnian / Dokumen ABMS" one line per bar; 4 ABMS document types one per beat |
| 47-54 | Finale | full-room wide (impact zoom + flash), emcee room wide | "Bersama ke arah MS ISO 37001:2025" |
| 54-60 | End card | brand shards (blue/red) sweep to white card | MCORP logo, title, standard, dates · venue; fade to black |

Grade (`build/prep_footage.sh`): per-clip exposure match, contrast +7%, saturation +12%, soft
S-curve with highlight roll-off (white walls / windows), cool shadows + warm mids, light clarity;
downscaled to 3200x1800 masters (punch-ins up to 1.7x stay sharp at 1080p).

Audio (`build/make_music.py`, `build/mix_audio.py`): original synthesised score (no licence needed):
E major I-V-vi-IV, stabs on the hook cuts, drop at 3s, four-on-the-floor from the briefing, peak in
the montage, impact at 47s, ring-out on the end card. SFX (Pixabay licence): year-roll click, whip,
zoom-through, end-card sweep. No VO, no camera audio. Master -14 LUFS.

## Rebuild (from `edits/bengkel-iso37001-mcorp/`)
```bash
build/prep_footage.sh media/prog2-raw     # ~15 min, 4 clips in parallel
python3 build/make_music.py hf/assets/audio/music.wav
python3 build/mix_audio.py
python3 build/compose.py
(cd hf && npx hyperframes render -o ../renders/bengkel-transisi-iso37001-mcorp-16x9.mp4 --quality delivery --sdr)
```
