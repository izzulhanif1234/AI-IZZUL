"""Merge BiRefNet subject mask with SAM chair mask; below seat level keep only the light chair frame (drops carpet seen through it)."""
import sys, numpy as np, cv2
from PIL import Image
src, mp, cp, out = sys.argv[1:5]
g = np.asarray(Image.open(src).convert('L')).astype(np.float32)
a = np.asarray(Image.open(mp)).astype(np.float32) / 255
p = np.asarray(Image.open(cp)).astype(np.float32) / 255
c = (p > 0.5).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(c, np.ones((7, 7), np.uint8)), 8)
H = g.shape[0]
below = np.zeros_like(c, bool)
yy = np.arange(H)[:, None]
for i in range(1, n):
    below |= (lab == i) & (yy > st[i][1] + 45)
k = c.copy()
k[below & (g < 145) & (a < 0.5)] = 0
k = cv2.morphologyEx(k, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
n2, lab2, st2, _ = cv2.connectedComponentsWithStats(k, 8)
for i in range(1, n2):
    if st2[i][4] < 50: k[lab2 == i] = 0
ch = cv2.GaussianBlur(k.astype(np.float32), (0, 0), 0.8)
f = np.maximum(a, ch)
n3, lab3, st3, _ = cv2.connectedComponentsWithStats((f > 0.3).astype(np.uint8), 8)
big = 1 + np.argmax(st3[1:, 4])
for i in range(1, n3):
    if i != big and st3[i][4] < 1500: f[lab3 == i] = 0
Image.fromarray((f * 255 + .5).astype(np.uint8)).save(out)
