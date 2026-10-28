"""Closed-form matting in a thin band around the chairs so leg edges follow the real pixels."""
import sys, numpy as np, cv2
from PIL import Image
from pymatting import estimate_alpha_cf
src, mp, mm, out = sys.argv[1:5]
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float64) / 255
a = np.asarray(Image.open(mp).convert('L')).astype(np.float32) / 255     # person mask (BiRefNet + extras)
f = np.asarray(Image.open(mm).convert('L')).astype(np.float32) / 255     # merged person+chair
chair = ((f > 0.5) & (a < 0.5)).astype(np.uint8)
ys, xs = np.nonzero(chair)
y0, y1 = max(0, ys.min() - 20), min(im.shape[0], ys.max() + 20)
fgall = (f > 0.5).astype(np.uint8)
tri = np.full(f.shape, 0.5)
tri[cv2.dilate(fgall, np.ones((9, 9), np.uint8)) == 0] = 0
tri[cv2.erode(chair, np.ones((5, 5), np.uint8)) > 0] = 1
tri[a > 0.95] = 1
zone = (cv2.dilate(chair, np.ones((9, 9), np.uint8)) > 0) & (a < 0.5)
tri[~zone & (tri == 0.5)] = (f[~zone & (tri == 0.5)] > 0.5)
al = estimate_alpha_cf(im[y0:y1], tri[y0:y1])
res = f.copy()
z = zone[y0:y1]
res[y0:y1][z] = np.maximum(a[y0:y1][z], al[z])
Image.fromarray((np.clip(res, 0, 1) * 255 + .5).astype(np.uint8)).save(out)
