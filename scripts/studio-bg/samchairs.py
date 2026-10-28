"""Recover chairs/stools the BiRefNet mask dropped: seed on bright chair legs, segment with SAM on zoomed crops."""
import sys, numpy as np, cv2
from PIL import Image
from rembg import new_session
from chairs import chair_mask

S = new_session('sam')

def sam_crop(img, pos, neg):
    """img: HxWx3 uint8 crop; pos/neg: lists of (x,y) in crop coords. returns float mask HxW."""
    h, w = img.shape[:2]
    sc = min(1024 / w, 684 / h)
    rs = cv2.resize(img, (int(w * sc + .5), int(h * sc + .5)), interpolation=cv2.INTER_AREA)
    pad = np.zeros((684, 1024, 3), np.uint8); pad[:rs.shape[0], :rs.shape[1]] = rs
    emb = S.encoder.run(None, {S.encoder.get_inputs()[0].name: pad.astype(np.float32)})[0]
    pts = np.array(pos + neg + [(0, 0)], np.float32) * sc
    lab = np.array([1] * len(pos) + [0] * len(neg) + [-1], np.float32)
    m, sc_, _ = S.decoder.run(None, {
        'image_embeddings': emb, 'point_coords': pts[None], 'point_labels': lab[None],
        'mask_input': np.zeros((1, 1, 256, 256), np.float32), 'has_mask_input': np.zeros(1, np.float32),
        'orig_im_size': np.array([684, 1024], np.float32)})
    logit = m[0, 0][:rs.shape[0], :rs.shape[1]]
    logit = cv2.resize(logit, (w, h), interpolation=cv2.INTER_LINEAR)
    return logit

def run(src, mpath, fy, out):
    im = np.asarray(Image.open(src).convert('RGB'))
    H, W = im.shape[:2]
    a = np.asarray(Image.open(mpath).convert('L')).astype(np.float32) / 255
    seeds = chair_mask(src, mpath, fy)
    n, lab, st, cen = cv2.connectedComponentsWithStats(seeds.astype(np.uint8), 8)
    person = cv2.erode((a > 0.9).astype(np.uint8), np.ones((15, 15), np.uint8))
    acc = np.zeros((H, W), np.float32)
    for i in range(1, n):
        ys, xs = np.nonzero(lab == i)
        k = np.argsort(ys)
        px, py = int(xs[k[len(k) // 2]]), int(ys[k[len(k) // 2]])
        if acc[py, px] > 0.5:
            continue
        x0 = max(0, min(W - 640, px - 320)); y0 = max(0, min(H - 420, py - 230))
        crop = im[y0:y0 + 420, x0:x0 + 640]
        pc = person[y0:y0 + 420, x0:x0 + 640]
        rng = np.random.default_rng(i)
        py_, px_ = np.nonzero(pc)
        neg = []
        if len(px_):
            idx = rng.choice(len(px_), min(8, len(px_)), replace=False)
            neg = [(float(px_[j]), float(py_[j])) for j in idx]
        # carpet negatives: far below the seed
        for dx in (-150, 150):
            cx, cy = px - x0 + dx, min(419, py - y0 + 160)
            if 0 <= cx < 640 and a[cy + y0, cx + x0] < 0.1 and seeds[cy + y0, cx + x0] == 0:
                neg.append((float(cx), float(cy)))
        logit = sam_crop(crop, [(float(px - x0), float(py - y0))], neg)
        prob = 1 / (1 + np.exp(-logit))
        area = (prob > .5).sum()
        print(f'seed {i} at ({px},{py}) area={area}', flush=True)
        if area > 60000:  # grabbed carpet/person region: skip
            continue
        acc[y0:y0 + 420, x0:x0 + 640] = np.maximum(acc[y0:y0 + 420, x0:x0 + 640], prob)
    acc[: max(0, fy - 80)] = 0
    Image.fromarray((acc * 255).astype(np.uint8)).save(out)

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
