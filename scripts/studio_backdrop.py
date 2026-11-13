"""Swap a plain blue passport-photo backdrop for a corporate studio backdrop (no AI model).
usage: studio_backdrop.py src.jpg out_prefix
Writes <out_prefix>-gelap.jpg (charcoal studio) and <out_prefix>-cerah.jpg (light grey studio)."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

BACKDROPS = {
    # name: (edge colour, glow colour behind the subject)
    "gelap": ((34, 36, 40), (118, 121, 128)),
    "cerah": ((150, 153, 158), (236, 237, 239)),
}


def bg_alpha(img):
    """1.0 where the pixel looks like the sky-blue backdrop, 0.0 where it is the subject."""
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    s1 = (b - r - 55) / 40          # backdrop is far bluer than red
    s2 = (g - r - 35) / 35          # and cyan-ish (green well above red)
    s3 = (b - 150) / 40             # and bright
    return np.clip(np.minimum(np.minimum(s1, s2), s3), 0, 1)


def subject_alpha(img):
    bg = bg_alpha(img)
    hard = bg > 0.5
    # keep only backdrop regions connected to the top/left/right edges
    lab, n = ndi.label(hard)
    edge = set(np.unique(np.concatenate([lab[0], lab[:, 0], lab[:, -1]]))) - {0}
    keep = np.isin(lab, list(edge))
    a = 1.0 - bg
    a[~keep & hard] = 1.0           # interior blue-ish spots belong to the subject
    # solid core: anything well inside the subject is fully opaque
    core = ndi.binary_erosion(~keep, iterations=3)
    a[core] = 1.0
    return ndi.gaussian_filter(a, 0.8)


def backdrop(h, w, edge, glow):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w * 0.5, h * 0.32
    d = np.sqrt(((x - cx) / (w * 0.62)) ** 2 + ((y - cy) / (h * 0.55)) ** 2)
    t = np.clip(1 - d, 0, 1) ** 1.6
    edge, glow = np.array(edge, np.float32), np.array(glow, np.float32)
    bgimg = edge + (glow - edge) * t[..., None]
    bgimg *= (1 - 0.10 * (y / h))[..., None]           # slightly darker towards the floor
    bgimg += np.random.default_rng(1).normal(0, 1.2, bgimg.shape)  # anti-banding grain
    return bgimg


def grade(img):
    """Gentle studio look: a touch of contrast and warmth."""
    m = img.mean()
    img = (img - m) * 1.05 + m
    img[..., 0] *= 1.02
    img[..., 2] *= 0.985
    return img


def main(src, prefix):
    img = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    h, w, _ = img.shape
    a = subject_alpha(img)
    sample = img[:60, :][bg_alpha(img[:60, :]) > 0.9]
    bgcol = np.median(sample, axis=0) if len(sample) else np.array([115, 205, 245], np.float32)
    # un-mix the blue backdrop from soft edge pixels
    aa = np.clip(a, 0.05, 1)[..., None]
    fg = np.clip((img - (1 - aa) * bgcol) / aa, 0, 255)
    edge_zone = (a > 0.02) & (a < 0.98)
    fg[edge_zone, 2] = np.minimum(fg[edge_zone, 2], np.maximum(fg[edge_zone, 0], fg[edge_zone, 1]) + 25)
    fg = grade(fg)
    for name, (edge, glow) in BACKDROPS.items():
        out = fg * a[..., None] + backdrop(h, w, edge, glow) * (1 - a[..., None])
        Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(f"{prefix}-{name}.jpg", quality=95)
        print("ok", f"{prefix}-{name}.jpg")


if __name__ == "__main__":
    main(*sys.argv[1:3])
