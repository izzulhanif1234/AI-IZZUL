# MCORP Estimate — Video Ulasan Pengguna (16:9)

Testimonial-only cut: Puan Rahimah binti Osman then YB Datuk Mohd Noor Helmy.
No voiceover, no QR. Their own words carry the film; motion graphics, UI
callouts and SFX pop up on what they say.

Build: `python3 scripts/ulasan_build.py` → `hf/index.html`, `hf/compositions/{fx,captions,badge}.html`
(fx is generated from `fx.tpl.html` with the times computed in the script).

## Order (~75.8 s)
| Root time | Section | Source | On-screen |
|---|---|---|---|
| 0–3.0 | Title "APA KATA PENGGUNA?" | rahimah2 b-roll | two portraits, slam type |
| 3.0–27.1 | Puan Rahimah (01 IMPAK, 02 HARAPAN) | rahimah3 7.93–11.92, 16.88–37.02 | name card, RM500,000 counter, b-roll "Jabatan tanpa latar teknikal ✓ Sangat membantu", "Amat digalakkan" stamp |
| 27.1 | red wipe → YB Datuk | | |
| 27.1–55.0 | YB Datuk (03 MASALAH, 04 PENYELESAIAN) | helmy3 0.55–28.40 | name card, Orang awam/Penduduk/Rakyat + DIPERTIKAI?, RM50,000?/RM20,000? tags, 10 KALI, cost-breakdown UI with MAHAL/MURAH |
| 55.0–58.2 | pull quote "Sebab nak selesaikan salah faham" | helmy3 28.70–31.95 | |
| 58.2–71.8 | YB Datuk (05 MANFAAT) | helmy3 37.80–51.40 | Orang teknikal / Bukan teknikal ✓, b-roll, BERMANFAAT, LEBIH MELUAS |
| 71.8–75.8 | MCORP Estimate logo only | | |

## Media prep
- Interviews re-encoded from the 4K originals to 2560x1440 so punch-ins stay sharp;
  audio from the cleaned/normalised tracks (helmy3 has the ambulance siren removed).
- Cut points verified by re-transcribing each isolated cut (faster-whisper large-v3).
- Music: MusicGen-small (`scripts/musicgen_long.py`); its continuation passes broke
  after ~50 s, so the bed is the first 30 s generation looped on a beat-aligned bar
  (8.864 s → 29.264 s), loudnorm -16 LUFS, ducked to 0.15 under speech.
