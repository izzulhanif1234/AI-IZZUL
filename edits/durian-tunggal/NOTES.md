# Rumah Kedai Durian Tunggal (MCORP): edit notes

Source v0: already-edited 51.4s vertical video (1080x1920, HEVC, 30fps) with burned-in
captions/graphics. Waiting on raw footage to re-edit from scratch in HyperFrames.

## Transcript (corrected against captions + flyer)
| Time | Line |
|---|---|
| 0.0–4.0 | Ok, kalau korang tengah cari rumah kedai area Durian Tunggal, korang kena tengok video ni. |
| 4.4–9.0 | Dekat pekan Durian Tunggal, sebenarnya ada rumah kedai yang tengah dibuka untuk disewa. |
| 9.3–14.9 | Lokasi dia memang strategik. Nak ke pekan dekat, nak ke Ayer Keroh pun tak jauh. |
| 15.0–20.3 | Rumah kedai ni berkeluasan 22 x 70 kaki dengan 3 tingkat. |
| 20.4–24.0 | Dan untuk tingkat bawah, siap ada kawasan tanah di bahagian tepi. |
| 24.0–31.6 | Nak buat kafe, dobi, [? bengkel/servis] kereta, semua sesuai. |
| 31.7–36.5 | Kalau korang tengah cari lokasi untuk kembangkan bisnes, inilah peluang dia. |
| 36.9–40.5 | Scan QR code atau hubungi kami untuk maklumat lanjut. |
| 40.5–51.4 | (no speech) flyer then MCORP logo |

## Key facts (from flyer)
- RM4,200 / bulan (kadar sewaan bermula)
- Rumah kedai 3 tingkat, 22 x 70 kaki, tanah tepi di tingkat bawah
- Berdekatan: Pekan Durian Tunggal, Plaza Tol Ayer Keroh, stesen minyak
- Hubungi: 06-232 6713/4417 · 019-678 7966 · www.mcorp.gov.my · @promosihartanahmcorp

## Issues found
- Weak hook: generic "kalau korang tengah cari…". Price (RM4,200) never spoken.
- Repeats: "Durian Tunggal" at 0s and 4s; "kalau korang tengah cari" at 0s and 32s.
- Awkward pauses: 24–31s listing (~0.5–0.8s gaps x3).
- Outro logo runs 8s (43–51s); ~2s is enough.

## Demo edit v1 (HyperFrames, on the already-edited video)
Project: `hf/` (`index.html` holds the edit decision list in a comment). Staged source
`hf/assets/source.mp4` is git-ignored; recreate with:
`ffmpeg -i source.mov -c:v libx264 -crf 18 -g 30 -keyint_min 30 -pix_fmt yuv420p -movflags +faststart -c:a aac hf/assets/source.mp4`

- 51.4s -> 40.7s
- Hook (0-1.6s): cafe b-roll slow push + "3 TINGKAT + TANAH TEPI" + RM4,200/bulan chip, whoosh + bass impact
- Removed: opening line repeating "Durian Tunggal", 3 pauses in kafe/dobi/bengkel list, cat meme tail, 8s logo -> 2.2s
- Overlays: location chips (Pekan Durian Tunggal, Plaza Tol Ayer Keroh), use chips (Kafe/Dobi/Bengkel kereta), CTA card (price + phone)
- SFX: bundled Pixabay library (see hf/assets/sfx/CREDITS.md)
- Status: draft preview only; final render pending approval. Loudness -20.8 LUFS (normalise to ~-14 for social on final).
