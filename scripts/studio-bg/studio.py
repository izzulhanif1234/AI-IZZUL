"""v2 studio composite: white seamless background that keeps the photo's own soft shadows,
edge colours decontaminated so no carpet/wall fringe remains."""
import sys, numpy as np, cv2
from PIL import Image
from pymatting import estimate_foreground_ml

def nblur(v, w, s):
    d = cv2.GaussianBlur(w, (0, 0), s)
    return cv2.GaussianBlur(v * w, (0, 0), s) / np.maximum(d, 1e-4), d

def skirting(L, bg, H):
    rows = np.array([L[y][bg[y]].mean() if bg[y].sum() > 50 else 255 for y in range(H)])
    lo, hi = H // 2, int(H * 0.92)
    fy = lo + int(np.argmin(rows[lo:hi]))
    wall = np.median(rows[fy - 120:fy - 30]); carpet = np.median(rows[fy + 40:fy + 140])
    a = fy
    while a > lo and rows[a] < (rows[fy] + wall) / 2: a -= 1
    b = fy
    while b < hi and rows[b] < (rows[fy] + carpet) / 2: b += 1
    return fy, a - 4, b + 6

def shading(im, alpha, debug=None):
    H, W = alpha.shape
    L = im.mean(2)
    subj = alpha > 0.02
    bg = ~cv2.dilate(subj.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool)
    fy, s0, s1 = skirting(L, bg, H)
    yy = np.arange(H)[:, None]
    dist = cv2.distanceTransform((~subj).astype(np.uint8), cv2.DIST_L2, 5)
    near = np.clip(1 - (dist - 40) / 160, 0, 1)
    out = np.ones((H, W), np.float32)
    xx = np.arange(W)[None, :]
    edge = np.clip((np.minimum(xx, W - 1 - xx) - 20) / 60.0, 0, 1)
    for region, s, t, k in (((yy > s1) & np.ones((1, W), bool), 10, 0.75, 0.72),):
        w = (bg & region).astype(np.float32)
        low, den = nblur(L.astype(np.float32), w, s)
        ref = np.array([np.percentile(low[y][w[y] > 0], 80) if w[y].sum() > 40 else np.nan for y in range(H)])
        idx = np.arange(H); ok = ~np.isnan(ref)
        ref = np.interp(idx, idx[ok], ref[ok]) if ok.any() else np.full(H, 255.0)
        ref = np.convolve(np.pad(ref, 40, mode='edge'), np.ones(81) / 81, 'valid')
        ratio = np.where(den > 0.15, low / ref[:, None], 1.0)
        u = np.clip((t - ratio) / (t - 0.3), 0, 1)
        sh = u * u * (3 - 2 * u) * k * near * np.clip((yy - s1) / 35.0, 0, 1) * edge
        out = np.where(region, 1 - sh, out)
    out = cv2.GaussianBlur(out, (0, 0), 3)
    if debug: Image.fromarray((out * 255).astype(np.uint8)).save(debug)
    return out, (fy, s0, s1)

def sharpen(rgb):
    """Two-scale unsharp mask on luminance only (no colour fringing)."""
    Y = rgb @ np.array([0.299, 0.587, 0.114])
    d = np.zeros_like(Y)
    for sig, amt in ((0.8, 0.35), (1.6, 0.15)):
        hp = Y - cv2.GaussianBlur(Y, (0, 0), sig)
        hp = np.sign(hp) * np.maximum(np.abs(hp) - 0.004, 0)
        d += amt * hp
    return np.clip(rgb + d[..., None], 0, 1)

def seat_shade(S, chair):
    """Soft occlusion shadow on the floor under each chair seat, between its legs."""
    H, W = S.shape
    yy = np.arange(H)[:, None]
    hard = (chair > 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(hard, np.ones((9, 9), np.uint8)), 8)
    occ = np.zeros((H, W), np.float32)
    for i in range(1, n):
        if st[i][4] < 1500: continue
        comp = (lab == i) & (hard > 0)
        rows = np.nonzero(comp.sum(1) >= 25)[0]
        if not len(rows): continue
        top, bot = rows[0] + 20, st[i][1] + st[i][3]
        pts = cv2.findNonZero(comp.astype(np.uint8))
        hull = np.zeros((H, W), np.uint8)
        cv2.fillConvexPoly(hull, cv2.convexHull(pts), 1)
        under = (hull > 0) & ~comp & (yy > top)
        grad = np.clip(1 - 0.6 * (yy - top) / max(bot - top, 1), 0.3, 1)
        occ = np.maximum(occ, under * grad * 0.2)
    occ = cv2.GaussianBlur(occ, (0, 0), 6)
    return S * (1 - occ)

def composite(src, mpath, out, debug=None, chairpath=None):
    pil = Image.open(src)
    im = np.asarray(pil.convert('RGB')).astype(np.float64) / 255
    a = np.asarray(Image.open(mpath).convert('L')).astype(np.float64) / 255
    S, info = shading(im * 255, a, debug)
    if chairpath:
        S = seat_shade(S, np.asarray(Image.open(chairpath).convert('L')).astype(np.float32) / 255)
    fg = sharpen(estimate_foreground_ml(im, a))
    a3 = a[..., None]
    o = fg * a3 + S[..., None] * (1 - a3)
    Image.fromarray((np.clip(o, 0, 1) * 255 + .5).astype(np.uint8)).save(
        out, quality=98, subsampling=0, icc_profile=pil.info.get('icc_profile'), exif=pil.info.get('exif'))
    return info

if __name__ == '__main__':
    print(composite(sys.argv[1], sys.argv[2], sys.argv[3], None, *(sys.argv[4:5])))
