# GROUPING MCORP — studio white background

Source: Google Photos album "GROUPING MCORP" (10 photos, Sony ILCE-6400, Lightroom export, 1616×1080).
Output: `final/GROUPING-MCORP-NN-studio.jpg`, same 1616×1080, JPEG q98 4:4:4, original EXIF + ICC kept.

Wall and grey carpet replaced with pure white. Floor keeps the photo's own soft shadows
(under the sofa, around feet and chair legs), lifted from the carpet so the tile pattern
doesn't come through. Edge colours are decontaminated (no carpet/wall fringe).
People, sofa, chairs and stool are kept as shot.

Pipeline v2 (`scripts/studio-bg/`, run from a work dir with originals in `../dl/orig_NN.bin`):
1. `mask1.py` — BiRefNet-general (rembg) person mask per photo (one process each; it leaks memory).
2. `manual.py chairs.json 04 05 06 07 08` — each white chair segmented by SAM vit_b from hand-placed
   points (seat + every visible leg, snapped to the bright pixel), best of 10 negative-prompt variants.
3. `merge3.py` — person ∪ chairs, carpet leaking below seat level dropped.
   (06, 07 also take `extra.py` chair/body prompts from v1.)
4. `refine.py` — closed-form matting in a thin band around the chairs for clean leg edges.
5. `backrow.py` — back-row shoes/skirts visible between chairs recovered with SAM.
6. `studio.py` — white background + real floor shadows, foreground colour decontamination.
