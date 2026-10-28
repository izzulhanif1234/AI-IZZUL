"""Recover dark back-row clothing/shoes seen between chairs that the person mask missed."""
import sys, numpy as np, cv2
from PIL import Image
from autochairs import encode, decode
n, fy = sys.argv[1], int(sys.argv[2])
im = np.asarray(Image.open(f'../dl/orig_{n}.bin').convert('RGB')); g = im.mean(2)
f = np.asarray(Image.open(f'm4_{n}.png')).astype(np.float32) / 255
H, W = g.shape
miss = ((g < 35) & (f < 0.3)).astype(np.uint8)
miss[:fy + 25] = 0
miss = cv2.morphologyEx(miss, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
k, lab, st, _ = cv2.connectedComponentsWithStats(miss, 8)
acc = np.zeros((H, W), np.float32)
for i in range(1, k):
    x, y, w, h, area = st[i]
    if area < 250: continue
    ys, xs = np.nonzero(lab == i)
    j = np.argmin((ys - ys.mean()) ** 2 + (xs - xs.mean()) ** 2)
    px, py = int(xs[j]), int(ys[j])
    x0 = max(0, min(W - 360, px - 180)); y0 = max(0, min(H - 300, py - 150))
    crop = im[y0:y0 + 300, x0:x0 + 360]
    emb, sc, rs = encode(crop)
    lg = decode(emb, sc, rs, (360, 300), [(float(px - x0), float(py - y0))])
    p = 1 / (1 + np.exp(-np.clip(lg, -50, 50))); m = p > 0.5
    gm = np.median(g[y0:y0 + 300, x0:x0 + 360][m]) if m.any() else 255
    ok = m.sum() < 15000 and gm < 55
    print(n, 'blob', (px, py), 'area', int(area), 'mask', int(m.sum()), 'med g %.0f' % gm, 'OK' if ok else 'skip', flush=True)
    if ok:
        sub = acc[y0:y0 + 300, x0:x0 + 360]
        np.maximum(sub, np.clip((p - 0.3) / 0.4, 0, 1) * (g[y0:y0 + 300, x0:x0 + 360] < 90), out=sub)
Image.fromarray((acc * 255).astype(np.uint8)).save(f'br_{n}.png')
