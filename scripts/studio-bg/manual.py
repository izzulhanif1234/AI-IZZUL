"""Per-chair SAM with hand-placed positives (snapped to the bright chair pixel nearby),
automatic negatives on people and carpet. Writes mc_<n>.png."""
import sys, json, numpy as np, cv2
from PIL import Image
from autochairs import encode, decode

def run(n, chairs, out):
    im = np.asarray(Image.open(f'../dl/orig_{n}.bin').convert('RGB'))
    H, W = im.shape[:2]
    g = im.mean(2).astype(np.float32); sat = (im.max(2).astype(int) - im.min(2))
    a = np.asarray(Image.open(f'mask_birefnet-general_{n}.png')).astype(np.float32) / 255
    tex = cv2.blur(np.abs(g - cv2.GaussianBlur(g, (0, 0), 1.0)), (7, 7))
    pers = cv2.erode((a > 0.9).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    carpet = (tex > 8) & (a < 0.05)
    acc = np.zeros((H, W), np.float32)
    rng = np.random.default_rng(0)
    for ci, pts in enumerate(chairs):
        snapped = []
        for x, y in pts:
            win = g[y - 3:y + 4, x - 7:x + 8] - (sat[y - 3:y + 4, x - 7:x + 8] > 40) * 255 - (a[y - 3:y + 4, x - 7:x + 8] > 0.5) * 255
            dy, dx = np.unravel_index(np.argmax(win), win.shape)
            snapped.append((x - 7 + dx, y - 3 + dy))
        xs, ys = zip(*snapped)
        x0 = max(0, min(xs) - 80); x1 = min(W, max(xs) + 80)
        y0 = max(0, min(ys) - 60); y1 = min(H, max(ys) + 90)
        if x1 - x0 < 300: c = (x0 + x1) // 2; x0, x1 = max(0, c - 150), min(W, c + 150)
        crop = im[y0:y1, x0:x1]
        far = np.ones((y1 - y0, x1 - x0), bool)
        for x, y in snapped:
            far[max(0, y - y0 - 18):y - y0 + 18, max(0, x - x0 - 18):x - x0 + 18] = False
        emb, sc, rs = encode(crop)
        pos = [(float(x - x0), float(y - y0)) for x, y in snapped]
        ac_ = a[y0:y1, x0:x1]; tx = tex[y0:y1, x0:x1]
        best = None
        for k in (0, 3, 6, 10, 16):
            for seed in (0, 1):
                r = np.random.default_rng(seed * 7 + k)
                negs = []
                for src, kk in ((pers, 8), (carpet, k)):
                    yy, xx = np.nonzero(src[y0:y1, x0:x1] & far)
                    if len(yy) and kk:
                        for j in r.choice(len(yy), min(kk, len(yy)), replace=False):
                            negs.append((float(xx[j]), float(yy[j])))
                lg = decode(emb, sc, rs, (x1 - x0, y1 - y0), pos, negs)
                p = 1 / (1 + np.exp(-np.clip(lg, -50, 50)))
                m = p > 0.5
                hit = np.mean([m[int(y), int(x)] for x, y in pos])
                own = m & (ac_ < 0.5)
                cf = ((g[y0:y1, x0:x1] < 150) & own).sum() / max(own.sum(), 1)
                score = hit * 10 - cf * 8 + min(own.sum(), 12000) / 12000
                if best is None or score > best[0]:
                    best = (score, p, m, k, seed, hit, cf)
        _, p, m, k, seed, hit, cf = best
        print(n, 'chair', ci, 'area', int(m.sum()), 'k', k, 'seed', seed, 'hit %.2f carpet %.2f' % (hit, cf), flush=True)
        sub = acc[y0:y1, x0:x1]
        np.maximum(sub, np.clip((p - 0.3) / 0.4, 0, 1) * (cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0), out=sub)
    Image.fromarray((acc * 255).astype(np.uint8)).save(out)

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))
    for n in sys.argv[2:]:
        run(n, spec[n], f'mc_{n}.png')
