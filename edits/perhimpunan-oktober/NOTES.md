# Perhimpunan Bulanan MCORP — Oktober 2026 (slide show + motion graphics)

Source: deck uploaded by the user (11 slides: 7 poster slides, 4 segment slides).
Build: unzip the source deck, `python3 -I build_motion.py <unpacked>`, zip back.

What `build_motion.py` adds (all animations start on their own when the slide opens — no clicks):

- **Poster slides (1, 2, 4, 6, 7, 9, 11):** slow Ken Burns zoom on the poster, gold light streaks,
  floating sparkles, a periodic white shine sweep. Slide 1 fades in from black; the rest use the
  Gallery transition.
- **Segment slides (3, 5, 8, 10):** "ATURCARA 01–04" tag, pulsing gold glow and three spinning
  dashed halo rings behind the speaker, light streaks, particles, one shine sweep, and a staged
  entrance (photo slides in from the right, tag wipes in, title/name float in, logos pop in).
  Fly Through (bounce) transition.

Transitions/effects are PowerPoint 2010+ (p14); older viewers fall back to fade/zoom.
Motion only plays in PowerPoint Slide Show mode; Google Slides/Keynote ignore most of it.
