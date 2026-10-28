"""Remove carpet pieces the person model kept around shoes / furniture bases (below the floor line)."""
import sys, numpy as np, cv2
from PIL import Image
from studio import skirting
src, mp, out = sys.argv[1:4]
chairs = sys.argv[4] if len(sys.argv) > 4 else None
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
g = im.mean(2); sat = im.max(2) - im.min(2)
f = np.asarray(Image.open(mp).convert('L')).astype(np.float32) / 255
H, W = f.shape
_, s0, s1 = skirting(g, f < 0.05, H)
tex = cv2.blur(np.abs(g - cv2.GaussianBlur(g, (0, 0), 1.0)), (5, 5))
cl = ((g > 95) & (g < 205) & (sat < 22) & (tex > 6)).astype(np.float32)
frac = cv2.blur(cl, (11, 11))
rm = (frac > 0.5) & (f > 0.05)
rm[:s1 + 5] = False
if chairs:
    c = np.asarray(Image.open(chairs).convert('L')) > 100
    rm &= ~(cv2.dilate(c.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0)
solid = cv2.erode((g < 55).astype(np.uint8), np.ones((5, 5), np.uint8))
solid = cv2.dilate(solid, np.ones((9, 9), np.uint8)) > 0
rm &= ~solid
rm = cv2.morphologyEx(rm.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0
soft = cv2.GaussianBlur(rm.astype(np.float32), (0, 0), 1.0)
print('removed px', int(rm.sum()))
Image.fromarray((np.clip(f * (1 - soft), 0, 1) * 255 + .5).astype(np.uint8)).save(out)
