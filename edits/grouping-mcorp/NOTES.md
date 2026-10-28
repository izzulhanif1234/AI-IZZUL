# GROUPING MCORP — studio white background

Source: Google Photos album "GROUPING MCORP" (10 photos, Sony ILCE-6400, Lightroom export, 1616×1080).
Output: `final/GROUPING-MCORP-NN-studio.jpg`, same 1616×1080, JPEG q98 4:4:4, original EXIF + ICC kept.

Wall and grey carpet replaced with pure white (#FFFFFF), with a faint soft contact shadow
on the floor only (below the skirting line) so feet and furniture don't float.
People, sofa, chairs and stool are kept as shot; subject pixels match the original
(mean diff < 1 level, JPEG re-encode only).

Pipeline (`scripts/studio-bg/`, run from a work dir with originals in `../dl/orig_NN.bin`):
1. `mask1.py` — BiRefNet-general (rembg) subject mask per photo (one process each; it leaks memory).
2. `samchairs.py` — white chairs are dropped by BiRefNet; seeds from bright chair legs
   (`chairs.py`) prompt SAM vit_b on zoomed crops.
3. `extra.py` — hand-placed SAM prompts where the auto pass missed (photos 06, 07: second chair
   and the back-row shoes/skirt seen behind it).
4. `merge.py` — union of masks; drops carpet SAM picked up between chair legs; removes stray specks.
5. `comp.py` — composite on white + floor contact shadow.
