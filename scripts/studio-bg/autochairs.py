"""Find every white chair part on the floor: SAM (2x zoom crops) prompted at each bright candidate pixel;
keep segments that are bright, smooth and not part of a person."""
import sys, numpy as np, cv2
from PIL import Image
from rembg import new_session

S = new_session('sam')
CW, CH = 400, 340

def encode(img):
    h, w = img.shape[:2]
    sc = min(1024 / w, 684 / h)
    rs = cv2.resize(img, (int(w * sc + .5), int(h * sc + .5)), interpolation=cv2.INTER_CUBIC)
    pad = np.zeros((684, 1024, 3), np.uint8); pad[:rs.shape[0], :rs.shape[1]] = rs
    emb = S.encoder.run(None, {S.encoder.get_inputs()[0].name: pad.astype(np.float32)})[0]
    return emb, sc, rs.shape[:2]

def decode(emb, sc, rshape, wh, pos, neg=()):
    pts = np.array(list(pos) + list(neg) + [(0, 0)], np.float32) * sc
    lab = np.array([1] * len(pos) + [0] * len(neg) + [-1], np.float32)
    m = S.decoder.run(None, {
        'image_embeddings': emb, 'point_coords': pts[None], 'point_labels': lab[None],
        'mask_input': np.zeros((1, 1, 256, 256), np.float32), 'has_mask_input': np.zeros(1, np.float32),
        'orig_im_size': np.array([684, 1024], np.float32)})[0]
    logit = m[0, 0][:rshape[0], :rshape[1]]
    return cv2.resize(logit, wh, interpolation=cv2.INTER_LINEAR)

def run(src, mpath, fy, out, dbg=None):
    im = np.asarray(Image.open(src).convert('RGB'))
    H, W = im.shape[:2]
    g = im.mean(2).astype(np.float32); sat = (im.max(2).astype(int) - im.min(2)).astype(np.float32)
    a = np.asarray(Image.open(mpath).convert('L')).astype(np.float32) / 255
    loc = cv2.medianBlur(g.astype(np.uint8), 31).astype(np.float32)
    mu = cv2.blur(g, (5, 5)); sd = np.sqrt(np.maximum(cv2.blur(g * g, (5, 5)) - mu * mu, 0))
    cand = (g > 140) & (sat < 40) & (a < 0.3) & ((g - loc) > 16)
    hf = np.abs(g - cv2.GaussianBlur(g, (0, 0), 1.0))
    cand[:fy - 30] = False
    acc = np.zeros((H, W), np.float32)
    seen = np.zeros((H, W), bool)
    y0s = list(range(fy - 40, H - CH, 260)) + [H - CH]
    x0s = list(range(0, W - CW, 300)) + [W - CW]
    tried = acc_n = 0
    for y0 in y0s:
        for x0 in x0s:
            cc = cand[y0:y0 + CH, x0:x0 + CW]
            if cc.sum() < 10: continue
            emb, sc, rshape = encode(im[y0:y0 + CH, x0:x0 + CW])
            per = (a[y0:y0 + CH, x0:x0 + CW] < 0.5).astype(np.uint8)
            dist, lbl = cv2.distanceTransformWithLabels(per, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            zy, zx = np.nonzero(per == 0)
            lut = np.zeros((lbl.max() + 1, 2), int)
            lut[lbl[zy, zx]] = np.stack([zx, zy], 1)
            ys, xs = np.nonzero(cc)
            cells = {}
            for y, x in zip(ys, xs):
                cells.setdefault((y // 8, x // 8), (y, x))
            for (y, x) in cells.values():
                Y, X = y + y0, x + x0
                if acc[Y, X] > 0.5 or seen[Y, X]: continue
                tried += 1
                neg = [tuple(lut[lbl[y, x]])] if dist[y, x] < 80 and len(zy) else []
                p = 1 / (1 + np.exp(-np.clip(decode(emb, sc, rshape, (CW, CH), [(x, y)], neg), -50, 50)))
                m = p > 0.5
                area = m.sum()
                if 40 <= area <= 20000:
                    seen[y0:y0 + CH, x0:x0 + CW] |= cv2.erode(m.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
                if (np.nonzero(m)[0] + y0 < fy).mean() > 0.4 if area else False: continue
                if area < 40 or area > 20000: continue
                gc = g[y0:y0 + CH, x0:x0 + CW]; ac_ = a[y0:y0 + CH, x0:x0 + CW]
                own = m & (ac_ < 0.5)
                if own.sum() < 30: continue
                if (m & (ac_ > 0.5)).sum() > 0.6 * area: continue
                ring = (cv2.dilate(m.astype(np.uint8), np.ones((13, 13), np.uint8)) > 0) & ~m & (ac_ < 0.3)
                if ring.sum() < 30: continue
                gm, gr = np.median(gc[own]), np.median(gc[ring])
                if gm < 140 or gm - gr < 15: continue
                inner = cv2.erode(own.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
                if inner.sum() < 10 or np.median(hf[y0:y0 + CH, x0:x0 + CW][inner]) > 8: continue
                ys_, xs_ = np.nonzero(m)
                if max(np.ptp(ys_), np.ptp(xs_)) < 25: continue
                acc_n += 1
                sub = acc[y0:y0 + CH, x0:x0 + CW]
                np.maximum(sub, np.clip((p - 0.3) / 0.4, 0, 1), out=sub)
    print('tried', tried, 'accepted', acc_n)
    Image.fromarray((acc * 255).astype(np.uint8)).save(out)
    if dbg:
        v = im.astype(float); c = acc[..., None]
        v = v * (1 - .6 * c) + np.array([0, 255, 0]) * .6 * c
        Image.fromarray(v.astype(np.uint8)).save(dbg, quality=90)

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], *(sys.argv[5:6]))
