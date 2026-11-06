# Salam Jumaat: Amanah & Tanggungjawab (9:16)

37 s, 1080x1920 @30fps, HyperFrames project in `hf/` (single composition `hf/index.html`).
No music; sound effects only (bundled Pixabay SFX, see `hf/assets/sfx/CREDITS.md`).
Look: navy MCORP corporate palette, red + gold accents, faint 8-point star pattern, corner frame.
Fonts are local (Amiri for Arabic, Montserrat for Latin) in `hf/assets/fonts/`.

## Storyboard
| Time | Scene | On-screen |
|---|---|---|
| 0-4.4 | Title | TAZKIRAH JUMAAT / SALAM JUMAAT |
| 4.4-11.4 | Hadith | "Sabda Rasulullah SAW", كُلُّكُمْ رَاعٍ وَكُلُّكُمْ مَسْئُولٌ عَنْ رَعِيَّتِهِ (wiped in right-to-left) |
| 11.4-19.4 | Maksud | Malay translation word by word, source: al-Bukhari 2554, Muslim 1829, JAKIM 40 Hadis |
| 19.4-27.4 | Mesej | "Setiap amanah ... dengan penuh:" + cards 01 INTEGRITI, 02 KEIKHLASAN, 03 DEDIKASI |
| 27.4-32.4 | Semoga | "...manfaat kepada masyarakat serta menyumbang kepada pembangunan negeri." |
| 32.5-37 | End card | MCORP Perbadanan Melaka logo, SALAM JUMAAT |

## Source note
The link the user gave (hadith-web, id 3898) is Sahih al-Bukhari 2409, worded
كُلُّكُمْ رَاعٍ وَمَسْؤُولٌ عَنْ رَعِيَّتِهِ. The on-screen Arabic follows the user's text
(وَكُلُّكُمْ مَسْئُولٌ), which is the Sahih Muslim 1829 wording.

## Render
`cd hf && npx --yes hyperframes@0.8.155 render -q high -o preview/high.mp4`, then
`ffmpeg -i preview/high.mp4 -c copy -movflags +faststart ../final/Salam-Jumaat-Amanah-9x16-v3.mp4`.
Loudness: -16.6 LUFS integrated, peak -3.7 dBFS.

## Revision 2
- Arabic wipe clipped the shadda/damma above كُلُّكُمْ (clip-path inset was the line box).
  Inset now extends -60% above and below, so all harakat stay visible during and after the wipe.

## Revision 3
- Removed the "Tema: Amanah & Tanggungjawab" line from the title card (user request).
