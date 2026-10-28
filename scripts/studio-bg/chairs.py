import sys, numpy as np, cv2
from PIL import Image
def chair_mask(src, mpath, fy):
    im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
    g = im.mean(2); sat = im.max(2) - im.min(2)
    a = np.asarray(Image.open(mpath).convert('L')).astype(np.float32) / 255
    loc = cv2.medianBlur(g.astype(np.uint8), 41).astype(np.float32)
    c = ((g - loc) > 28) & (g > 172) & (sat < 30) & (a < 0.5)
    c[: fy + 8] = False
    c = cv2.morphologyEx(c.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(c, 8)
    keep = np.zeros_like(c)
    near = cv2.dilate((a > 0.5).astype(np.uint8), np.ones((25, 25), np.uint8))
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area > 80 and h > 20 and (near[lab == i].any()):
            keep[lab == i] = 1
    return keep
if __name__ == '__main__':
    k = chair_mask(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    im = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
    v = im.copy(); v[k > 0] = [0, 255, 0]
    Image.fromarray(v.astype(np.uint8)).crop((80, 600, 1616, 1080)).save(sys.argv[4], quality=88)
