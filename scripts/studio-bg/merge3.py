"""Person mask ∪ prompted chair mask; carpet that leaked into a chair mask below seat level is dropped."""
import sys, numpy as np, cv2
from PIL import Image
src, mp, cp, out = sys.argv[1:5]
g = np.asarray(Image.open(src).convert('L')).astype(np.float32)
a = np.asarray(Image.open(mp).convert('L')).astype(np.float32) / 255
c = np.asarray(Image.open(cp).convert('L')).astype(np.float32) / 255
for e in sys.argv[5:]:
    c = np.maximum(c, np.asarray(Image.open(e).convert('L')).astype(np.float32) / 255)
tex = cv2.blur(np.abs(g - cv2.GaussianBlur(g, (0, 0), 1.0)), (5, 5))
hard = (c > 0.5).astype(np.uint8)
n0, lab0, st0, _ = cv2.connectedComponentsWithStats(cv2.dilate(hard, np.ones((7, 7), np.uint8)), 8)
yy = np.arange(g.shape[0])[:, None]
seat = np.zeros(g.shape, bool)
for i in range(1, n0):
    comp = lab0 == i
    rows = np.nonzero(comp.sum(1) >= 25)[0]
    top = rows[0] if len(rows) else st0[i][1]
    seat |= comp & (yy <= top + 45)
carpet = (g < 150) & (tex > 5) & (a < 0.5) & ~seat
carpet = cv2.morphologyEx(carpet.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)) > 0
c[carpet] = 0
k = cv2.morphologyEx((c > 0.5).astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(k, 8)
for i in range(1, n):
    if st[i][4] < 60: k[lab == i] = 0
c = c * (cv2.dilate(k, np.ones((3, 3), np.uint8)) > 0)
f = np.maximum(a, c)
n3, lab3, st3, _ = cv2.connectedComponentsWithStats((f > 0.3).astype(np.uint8), 8)
big = 1 + np.argmax(st3[1:, 4])
for i in range(1, n3):
    if i != big and st3[i][4] < 400: f[lab3 == i] = 0
Image.fromarray((f * 255 + .5).astype(np.uint8)).save(out)
