"""Keep dark clothing / under-seat darkness seen between people (back row, crotch gaps):
dark pixels connected to the subject inside holes or right next to it become subject."""
import sys, numpy as np, cv2
from PIL import Image
from studio import skirting
src, mp, out = sys.argv[1:4]
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
g = im.mean(2)
f = np.asarray(Image.open(mp).convert('L')).astype(np.float32) / 255
H, W = f.shape
subj = (f > 0.5).astype(np.uint8)
bgc = (f < 0.5).astype(np.uint8)
k, lab, st, _ = cv2.connectedComponentsWithStats(bgc, 4)
holes = np.zeros((H, W), bool)
for i in range(1, k):
    x, y, w, h, a = st[i]
    if x > 0 and y > 0 and x + w < W and y + h < H:
        holes |= lab == i
_, s0, s1 = skirting(g, ~cv2.dilate(subj, np.ones((7, 7), np.uint8)).astype(bool), H)
band = np.zeros((H, W), bool); band[s0 - 3:s1 + 3] = True
near = cv2.dilate(subj, np.ones((31, 31), np.uint8)) > 0
region = holes | (near & ~band)
region[:, :40] = holes[:, :40]; region[:, W - 80:] = holes[:, W - 80:]
tex = cv2.blur(np.abs(g - cv2.GaussianBlur(g, (0, 0), 1.0)), (5, 5))
up = np.roll(g, 14, 0); dn = np.roll(g, -14, 0)
thin = (g < 70) & (up > 140) & (dn > 95)
thin = cv2.dilate(thin.astype(np.uint8), np.ones((7, 9), np.uint8)) > 0
dark = (g < 40) & (tex < 8) & region & (f < 0.5) & ~thin
dark = cv2.morphologyEx(dark.astype(np.uint8), cv2.MORPH_OPEN, np.ones((4, 4), np.uint8)) > 0
k2, lab2, st2, _ = cv2.connectedComponentsWithStats(dark.astype(np.uint8), 8)
touch = cv2.dilate(subj, np.ones((5, 5), np.uint8)) > 0
keep = np.zeros((H, W), bool)
ids = np.unique(lab2[touch & dark])
for i in ids:
    if i and st2[i][4] >= 80:
        keep |= lab2 == i
add = np.clip((48 - g) / 16, 0, 1) * cv2.dilate(keep.astype(np.uint8), np.ones((3, 3), np.uint8))
add = cv2.GaussianBlur(add.astype(np.float32), (0, 0), 0.7)
print('added px', int(keep.sum()))
Image.fromarray((np.maximum(f, add) * 255 + .5).astype(np.uint8)).save(out)
