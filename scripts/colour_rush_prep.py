"""Colour Rush shirt ad: cut the front + back hero shirts out of the design board,
rebuild the sliver of the back's left sleeve hidden behind the front shirt, lengthen
the torsos to real tee proportions, upscale 4x (EDSR), and key the title / partner
blocks and paint splatters off the dark background.
usage: colour_rush_prep.py source-design.jpg outdir EDSR_x4.pb"""
import sys
import cv2
import numpy as np
from PIL import Image
from rembg import new_session, remove
from scipy import ndimage

src, out, model = sys.argv[1:4]
board = cv2.imread(src)  # BGR
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel(model); sr.setModel("edsr", 4)
TARGET_HW = 1.18  # height / sleeve-to-sleeve width of a real flat tee

# ---------- segment both shirts in one pass ----------
X0, Y0, X1, Y1 = 20, 195, 1040, 760
reg = board[Y0:Y1, X0:X1]
sess = new_session("isnet-general-use")
M = np.asarray(remove(Image.fromarray(cv2.cvtColor(reg, cv2.COLOR_BGR2RGB)), session=sess, only_mask=True)) / 255.0
H, W = M.shape
yy, xx = np.mgrid[0:H, 0:W]


def split_x(y):  # front sleeve's right edge runs diagonally over the back sleeve
    y = np.asarray(y, dtype=float)
    return np.where(y < 100, 515, np.where(y <= 300, 507 + (y - 100) * 0.30, 500))


left = xx < split_x(yy)


def solid(mask):
    lab, n = ndimage.label(mask)
    if n > 1:
        sizes = ndimage.sum(mask, lab, range(1, n + 1))
        mask = lab == (1 + int(np.argmax(sizes)))
    return ndimage.binary_fill_holes(mask)


front = solid((M > 0.4) & left)
back = solid((M > 0.4) & ~left)


def close_hem(mask, from_y):
    """Body below the sleeves is a solid tube: fill each row's span, then give the hem a
    smooth bottom edge (splatter near the hem fools the matte into notches)."""
    mask = mask.copy()
    for y in range(from_y, H):
        r = np.where(mask[y])[0]
        if len(r):
            mask[y, r[0]:r[-1] + 1] = True
    cols = np.where(mask[from_y])[0]  # body columns only, never the sleeves
    bottom = np.array([from_y + np.where(mask[from_y:, x])[0].max() for x in cols])
    smooth = ndimage.minimum_filter1d(ndimage.maximum_filter1d(bottom, 41), 41)
    for x, b_ in zip(cols, smooth):
        mask[from_y:b_ + 1, x] = True
    return mask


front = close_hem(front, 365)
back = close_hem(back, 365)

# back's hidden left-sleeve wedge: mirror its right side about the body axis
rows = [np.where(back[y])[0] for y in range(380, 420)]
axis = float(np.mean([(r[0] + r[-1]) / 2 for r in rows if len(r)]))
mir_x = np.clip((2 * axis - xx).round().astype(int), 0, W - 1)
mirrored = back[yy, mir_x]
wedge = mirrored & ~back & (xx < axis) & (yy < 330)
back_full = ndimage.binary_closing(back | wedge, iterations=2)
fill = (back_full & ~back) | (left & back_full)
# rebuild the wedge from the back's own visible left sleeve, shifted outward
# (mirroring the right sleeve would drag its JETOUR logo in), seam feathered
DX = 52
shifted = np.roll(reg, -DX, axis=1)
w = cv2.GaussianBlur(fill.astype(np.float32), (0, 0), 3)[..., None]
w = np.where(fill[..., None], 1.0, w)
reg_back = (reg * (1 - w) + shifted * w).astype(np.uint8)
print("axis", round(axis, 1), "wedge px", int(wedge.sum()))


def cut(rgb_reg, mask, name, stretch_from):
    ys, xs = np.where(mask)
    pad = 6
    y0, y1, x0, x1 = ys.min() - pad, ys.max() + pad + 1, xs.min() - pad, xs.max() + pad + 1
    rgb = rgb_reg[max(0, y0):y1, max(0, x0):x1]
    a = mask[max(0, y0):y1, max(0, x0):x1].astype(np.float32)
    up = sr.upsample(rgb)
    a_up = cv2.resize(a, (up.shape[1], up.shape[0]), interpolation=cv2.INTER_LINEAR)
    a_up = cv2.GaussianBlur(a_up, (0, 0), 1.6)
    a_up = np.clip((a_up - 0.5) * 1.6 + 0.5, 0, 1)
    # lengthen the torso: stretch only the band below the chest/back print
    sw = xs.max() - xs.min()
    sh = ys.max() - ys.min()
    add = max(0, TARGET_HW * sw - sh) * 4
    s0 = (stretch_from - max(0, y0)) * 4
    top, low = up[:s0], up[s0:]
    a_top, a_low = a_up[:s0], a_up[s0:]
    nh = int(round(low.shape[0] + add))
    low = cv2.resize(low, (low.shape[1], nh), interpolation=cv2.INTER_CUBIC)
    a_low = cv2.resize(a_low, (a_low.shape[1], nh), interpolation=cv2.INTER_CUBIC)
    rgb_o = np.vstack([top, low])
    a_o = np.clip(np.vstack([a_top, a_low]), 0, 1)
    rgba = np.dstack([rgb_o, (a_o * 255).astype(np.uint8)])
    cv2.imwrite(f"{out}/{name}.png", rgba)
    print(name, rgba.shape[1], "x", rgba.shape[0], "ratio", round(rgba.shape[0] / rgba.shape[1], 3))


cut(reg, front, "shirt-front", stretch_from=345)  # below "NO FILTER. JUST COLOUR."
cut(reg_back, back_full, "shirt-back", stretch_from=300)  # below "BRIGHT"


# ---------- luminance-keyed graphics from the board ----------
def keyed(box, name, lo=46, hi=120, upscale=True):
    x0, y0, x1, y1 = box
    crop = board[y0:y1, x0:x1]
    if upscale:
        crop = sr.upsample(crop)
    c = crop.astype(np.float32)
    lum = c.max(axis=2)
    a = np.clip((lum - lo) / (hi - lo), 0, 1)
    rgb = np.clip(c / np.maximum(a, 1e-3)[..., None] * (a[..., None] > 0) * 0 + c, 0, 255)
    rgba = np.dstack([rgb, a * 255]).astype(np.uint8)
    cv2.imwrite(f"{out}/{name}.png", rgba)
    print(name, rgba.shape[1], "x", rgba.shape[0])


keyed((92, 18, 735, 208), "title-block")        # COLOUR//RUSH, MELAKA 2026, taglines
keyed((845, 52, 1292, 168), "partners")         # organised by MCS, Chery | Jetour, AJ Group
keyed((900, 680, 1536, 1024), "splat-a", upscale=False)
keyed((0, 180, 210, 720), "splat-b", upscale=False)
keyed((1286, 20, 1430, 210), "splat-c", upscale=False)
