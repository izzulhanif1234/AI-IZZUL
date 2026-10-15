# Sesi Lawatan Penanda Aras dan Taklimat, Perbadanan Melaka Holdings Sdn. Bhd. (PMH): 60s highlights

Source: 19 clips, DJI Osmo Pocket 4, 3840x2160 29.97fps HEVC 10-bit BT.709, 14 Oct 2026
09:58-13:11, ~173s total. Client Drive folder in `media/pmh-raw/` (git-ignored); `pNN` = filename order.

| Clip | Len | Content | Storyboard |
|---|---|---|---|
| p01 | 12.9 | GM and CEO MCORP on the sofa in the GM's room | 1 |
| p02 | 4.9 | PMH logo wall ("Wholly-Owned Subsidiary of Perbadanan Melaka (MCorp)"), pan to staff | 2 |
| p03 | 6.8 | leaving the room, greeting staff in the office | 2 |
| p04 | 21.0 | CEO shaking hands with staff (smiles, selfie), walks to the briefing room | 2 |
| p05 | 4.7 | staff seated waiting | 2 |
| p06 | 14.4 | CEO seated among the staff | 3 |
| p07 | 10.0 | emcee standing, staff wide | 3 |
| p08 | 8.7 | doa at the PMH podium (hands raised) | 3 |
| p09 | 8.1 | CEO speaking at the PMH podium | 3 |
| p10 | 6.0 | staff listening | 3 |
| p11 | 11.4 | corporate-information wall (board / management plaques), room wide | 3 |
| p12 | 6.4 | screen: "Pembentangan Informasi Korporat kepada YBhg. Datuk Saiful Hazwa bin Kipli, Ketua Pegawai Eksekutif MCORP merangkap Lembaga Pengarah PMH, 14 Oktober 2026 (Rabu), 10.00 pagi, Bilik Mesyuarat" | 4 |
| p13 | 11.5 | group photo, CEO with all PMH staff | (extra) |
| p14-p18 | 7-9.5 | meeting-room presentation, CEO at the head of the table | 4 |
| p19 | 5.9 | four-person posed photo at the Service Hub Centre board (13:11) | 5 |

**No souvenir handover is visible in the footage** (storyboard item 5): p19 is a posed photo only.
Chapter 5 is therefore "Kenangan Bersama" (group photo + p19). If the cenderamata clip exists,
it drops into shot e2 (51.0-54.55) in `build/compose.py`.

## Facts on screen
- Names / titles: CEO from the p12 slide; GM name and title from the client brief (name tag in
  p01/p19 reads "AINSHAH").
- Company line from the logo wall, translated: "Anak syarikat milik penuh Perbadanan Melaka (MCORP)".
- "Terima kasih atas kunjungan" on the end card is our closing line, not a quote.
- Logo: no official PMH logo file was found online; the end card uses the official MCORP logo
  (mcorp.gov.my) and the real PMH logo appears via the logo-wall footage (title, 4-8s).
- Palette from the PMH logo wall / slide: blue #1a56c4, gold #f4c21c, navy #081634.

## Edit (60.0s, 1920x1080, `build/compose.py`)
Music 120 BPM, bars every 2s from the first drop at 4.0s; cuts on beats, chapters on bar lines.

| Time | Chapter | Shots | Graphics / transitions |
|---|---|---|---|
| 0-4 | Hook | 8 beat cuts: handshake, smiling staff, podium, CEO among staff, slide, meeting, group photo, GM+CEO | "14 Oktober 2026 / Lawatan Penanda Aras / & Taklimat / PMH"; punch-out + whoosh |
| 4-8 | Title | PMH logo wall, pan to staff (drop + white flash) | event title, company, subsidiary line, date |
| 8-16 | 01 Pertemuan Bersama Pengurus Besar | p01 wide push, CEO close, GM close | gold light leak; chapter card; CEO + GM lower thirds |
| 16-26 | 02 Bersama Warga PMH | handshakes and smiles (p03, p04), staff waiting | zoom-through; chapter card |
| 26-36 | 03 Ucapan Ketua Pegawai Eksekutif MCORP | CEO among staff, doa, CEO at the podium, audience, room | zoom-through; black drop-gap 35.72-36 |
| 36-48 | 04 Pembentangan Informasi Korporat | slide (second drop, flash), meeting room x5 | chapter card at 38.6 |
| 48-54 | 05 Kenangan Bersama | group photo, posed photo | zoom-through + light leak |
| 54-60 | End card | navy/blue/gold shards to a white card | thanks line, title, company, date, MCORP logo; fade |

Grade (`build/prep_footage.sh`, shared look with the ISO 37001 edit): per-clip exposure match from
measured luma, contrast +7%, saturation +12%, soft S-curve with highlight roll-off, cool shadows /
warm mids, light clarity; 3200x1800 masters.

Audio: original synthesised score (`build/make_music.py`), trend-led future house (offbeat
supersaw stabs, heavy sidechain pump, shuffled hats, drop gaps), no third-party music. SFX
(Pixabay licence): whooshes on the hook punch-out, chapter zoom-throughs and the end-card sweep.
No VO, no camera audio. Master -14 LUFS.

## Rebuild (from `edits/lawatan-pmh-mcorp/`)
```bash
build/prep_footage.sh media/pmh-raw
python3 build/make_music.py hf/assets/audio/music.wav
python3 build/mix_audio.py
python3 build/compose.py
(cd hf && npx hyperframes render -o ../renders/lawatan-penanda-aras-pmh-16x9.mp4 --quality delivery --sdr)
```
