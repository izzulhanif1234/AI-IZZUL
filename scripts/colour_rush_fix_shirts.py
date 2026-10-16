"""Repair the two cut-off sleeves on the Colour Rush shirt cutouts (run after colour_rush_prep.py).

front: the JETOUR sleeve tip was clipped where it overlapped the back shirt on the board.
       Its outline is restored by mirroring the clean CHERY sleeve's silhouette; the new
       sliver is inpainted from the sleeve fabric.
back:  the left sleeve was hidden behind the front shirt on the board, so its pixels were a
       patch job. It is replaced by the mirrored right sleeve, with the JETOUR logo
       inpainted out first so no reversed text appears.
usage: colour_rush_fix_shirts.py hf/assets/img"""
import sys

import cv2
import numpy as np

d = sys.argv[1]


def load(name):
    im = cv2.imread(f"{d}/{name}", cv2.IMREAD_UNCHANGED)
    return im[..., :3].copy(), im[..., 3].astype(np.float32) / 255


def axis_of(a):
    H = a.shape[0]
    xs = [np.where(a[int(f * H)] > 0.5)[0] for f in (0.05, 0.55, 0.6)]
    return float(np.mean([(x[0] + x[-1]) / 2 for x in xs]))


def mirror(img, axis):
    W = img.shape[1]
    src = np.clip(np.round(2 * axis - np.arange(W)).astype(int), 0, W - 1)
    return img[:, src]


def feather(mask, px):
    return cv2.GaussianBlur(mask.astype(np.float32), (0, 0), px)


# ---------- front: restore the JETOUR sleeve tip ----------
rgb, a = load("shirt-front.png")
H, W = a.shape
ax = axis_of(a)
am = mirror(a, ax)
yy, xx = np.mgrid[0:H, 0:W]
zone = (xx > ax + 450) & (yy > 0.08 * H) & (yy < 0.48 * H)
new = zone & (am > 0.5) & (a < 0.5)
a2 = np.where(zone, np.maximum(a, am), a)
# inpaint the new sliver plus a thin band of the old (dark-fringed) cut edge
band = cv2.dilate(new.astype(np.uint8), np.ones((15, 15), np.uint8)) > 0
inp = cv2.inpaint(rgb, (band & zone).astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)
rgb2 = np.where((band & zone)[..., None], inp, rgb)
cv2.imwrite(f"{d}/shirt-front.png", np.dstack([rgb2, (np.clip(a2, 0, 1) * 255).astype(np.uint8)]))
print("front axis", round(ax, 1), "restored px", int(new.sum()))

# ---------- back: rebuild the left sleeve from the right one ----------
rgb, a = load("shirt-back.png")
H, W = a.shape
ax = axis_of(a)
yy, xx = np.mgrid[0:H, 0:W]
right_sleeve = (xx > ax + 520) & (yy > 0.25 * H) & (yy < 0.55 * H)
logo = right_sleeve & (rgb.min(axis=2) > 140) & (a > 0.5)
logo = cv2.dilate(logo.astype(np.uint8), np.ones((13, 13), np.uint8)) > 0
clean = cv2.inpaint(rgb, logo.astype(np.uint8) * 255, 15, cv2.INPAINT_TELEA)
src_rgb = mirror(clean, ax)
src_a = mirror(a, ax)
# weight: 1 on the sleeve, fading out toward the shoulder seam / body
x_in = ax - 560  # sleeve meets body around here
# only below the shoulder line: the left shoulder itself was visible on the board and is fine
w = np.clip((x_in - xx) / 110.0, 0, 1) * np.clip((yy - 0.2 * H) / (0.08 * H), 0, 1) * (yy < 0.6 * H)
w = feather(w, 6)
rgb2 = (rgb * (1 - w[..., None]) + src_rgb * w[..., None]).astype(np.uint8)
a2 = a * (1 - w) + src_a * w
cv2.imwrite(f"{d}/shirt-back.png", np.dstack([rgb2, (np.clip(a2, 0, 1) * 255).astype(np.uint8)]))
print("back axis", round(ax, 1), "logo px", int(logo.sum()))
