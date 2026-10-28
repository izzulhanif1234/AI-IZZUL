"""Pure white studio background + faint floor contact shadow; subject pixels untouched."""
import sys, numpy as np, cv2
from PIL import Image

def run(src, mpath, out, shadow=True):
    pil = Image.open(src); icc = pil.info.get('icc_profile'); exif = pil.info.get('exif')
    im = np.asarray(pil.convert('RGB')).astype(np.float32) / 255
    a = np.asarray(Image.open(mpath).convert('L')).astype(np.float32) / 255
    H, W = a.shape
    bg = np.ones_like(im)
    if shadow:
        # wall/floor line = darkest background row (skirting) in the lower half
        g = im.mean(2); hard = a > 0.08
        rows = [(g[y][~hard[y]].mean() if (~hard[y]).sum() > 50 else 1, y) for y in range(H // 2, int(H * 0.92))]
        fy = min(rows)[1]
        ramp = np.clip((np.arange(H) - fy) / 60.0, 0, 1)[:, None]
        soft = cv2.GaussianBlur(np.roll(a, 6, 0), (0, 0), 18)
        tight = cv2.GaussianBlur(np.roll(a, 3, 0), (0, 0), 4)
        s = np.clip(0.16 * soft + 0.22 * tight, 0, 0.3) * ramp
        bg = bg * (1 - s[..., None])
    a3 = a[..., None]
    o = im * a3 + bg * (1 - a3)
    Image.fromarray((np.clip(o, 0, 1) * 255 + 0.5).astype(np.uint8)).save(
        out, quality=98, subsampling=0, icc_profile=icc, exif=exif)
    return fy if shadow else None

if __name__ == '__main__':
    print(run(sys.argv[1], sys.argv[2], sys.argv[3]))
