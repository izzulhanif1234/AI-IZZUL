"""Cut the 11 MCORP subsidiary logos out of the strip image, upscale 4x (EDSR super-res),
key the white background to alpha. usage: logo_montage_prep.py source.png outdir EDSR_x4.pb"""
import sys
import cv2
import numpy as np

src, out, model = sys.argv[1:4]
NAMES = ["mitc", "melaka-sentral", "pmh", "mcorp-hotel", "mcs", "invest-melaka",
         "mcorp-technology", "pmpc", "mbsb", "pm-multilink", "melaka-halal-hub"]

img = cv2.imread(src)
nonwhite = img.min(axis=2) < 235
xs = np.where(nonwhite.any(axis=0))[0]
runs, s, p = [], xs[0], xs[0]
for x in xs[1:]:
    if x - p > 6:
        runs.append((s, p)); s = x
    p = x
runs.append((s, p))
assert len(runs) == len(NAMES), runs

sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel(model); sr.setModel("edsr", 4)

PAD = 4
for name, (x0, x1) in zip(NAMES, runs):
    col = nonwhite[:, x0:x1 + 1].any(axis=1)
    ys = np.where(col)[0]
    y0, y1 = ys.min(), ys.max()
    crop = img[y0 - PAD:y1 + PAD + 1, x0 - PAD:x1 + PAD + 1]
    up = sr.upsample(crop).astype(np.float32)
    # white key: alpha from distance to white, then un-premultiply against white
    a = np.clip((255 - up.min(axis=2)) / 200.0, 0, 1)
    a = np.where(a < 0.04, 0, a)
    safe = np.maximum(a, 1e-3)[..., None]
    rgb = np.clip((up - 255 * (1 - a[..., None])) / safe, 0, 255)
    rgba = np.dstack([rgb, a * 255]).astype(np.uint8)
    cv2.imwrite(f"{out}/{name}.png", rgba)
    print(name, rgba.shape[1], "x", rgba.shape[0])
