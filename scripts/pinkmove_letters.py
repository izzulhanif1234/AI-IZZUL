"""Key the poster's own PINK / MOVE / 2026 brush lettering out as PNGs.

usage: pinkmove_letters.py POSTER.png OUT_DIR
The poster lettering is hand-painted (no font matches it), so the teaser
uses the original strokes: PINK by its hot-pink hue, MOVE and 2026 as
near-white strokes on the dark swath. Upscaled 2x before keying.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

poster, out = sys.argv[1], Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

# Title block on the 1448x1086 poster: x 60-900, y 280-570.
src = Image.open(poster).convert("RGB").crop((60, 280, 900, 570))
src = src.resize((src.width * 2, src.height * 2), Image.LANCZOS)
src = src.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
im = np.asarray(src).astype(np.float32) / 255
r, g, b = im[..., 0], im[..., 1], im[..., 2]
mx, mn = im.max(-1), im.min(-1)
d = np.maximum(mx - mn, 1e-6)
sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60

pink = ((hue > 315) | (hue < 8)) & (sat > 0.55) & (mx > 0.78)
pink[:, 1000:] = False
white = (mx > 0.86) & (sat < 0.22)
white[:, :820] = False


def components(mask, min_area, drop_top_edge=False):
    mask = ndi.binary_opening(mask, iterations=1)
    lab, _ = ndi.label(mask)
    found = []
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        area = int((lab[sl] == i).sum())
        if area < min_area or (drop_top_edge and sl[0].start <= 2):
            continue
        found.append((i, sl, area))
    return lab, found


def save(name, lab, ids):
    m = ndi.binary_closing(np.isin(lab, ids), iterations=2)
    alpha = ndi.gaussian_filter(m.astype(np.float32), 0.8)
    rgba = Image.fromarray((np.dstack([im, alpha]) * 255).astype(np.uint8), "RGBA")
    rgba = rgba.crop(rgba.getbbox())
    rgba.save(out / f"{name}.png")
    print(name, rgba.size)


lab, found = components(pink, 4000)
save("title-pink", lab, [i for i, _, _ in found])

# The white background above MOVE touches the crop's top edge; drop it.
lab, found = components(white, 3000, drop_top_edge=True)
move = [i for i, sl, _ in found if sl[0].start < 240]
year = [i for i, sl, _ in found if sl[0].start >= 240]
save("title-move", lab, move)
save("title-2026", lab, year)
