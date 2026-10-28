"""Targeted erase of leftover carpet/shadow in a box, keeping solid black (shoes) and beige sofa."""
import sys, numpy as np, cv2
from PIL import Image
src, mp, out = sys.argv[1:4]
x0, y0, x1, y1 = map(int, sys.argv[4].split(','))
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32); g = im.mean(2); sat = im.max(2) - im.min(2)
f = np.asarray(Image.open(mp).convert('L')).astype(np.float32) / 255
box = np.zeros(f.shape, bool); box[y0:y1, x0:x1] = True
keep = ((g < 35) & (len(sys.argv) < 6)) | ((sat > 20) & (g > 120))
kill = box & ~keep
soft = cv2.GaussianBlur(kill.astype(np.float32), (0, 0), 1.0)
Image.fromarray((f * (1 - soft) * 255 + .5).astype(np.uint8)).save(out)
