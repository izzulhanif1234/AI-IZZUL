"""Replace the GPT creator credit with "MCorp Estimate" and the avatar with the MCORP EstiMATE logo."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

STAGE = sys.argv[1]
FONT = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

logo = Image.open(f"{STAGE}/logo.jpg").convert("RGB")
icon = logo.crop((150, 97, 400, 347))  # calculator mark, square


def disc(size):
    """Logo icon on a white disc, antialiased via supersampling."""
    s = size * 4
    big = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
    white = Image.new("RGBA", (s, s), (255, 255, 255, 255))
    big.paste(white, (0, 0), mask)
    pad = int(s * 0.14)
    ic = icon.resize((s - 2 * pad, s - 2 * pad), Image.LANCZOS).convert("RGBA")
    big.paste(ic, (pad, pad))
    big.putalpha(mask)
    return big.resize((size, size), Image.LANCZOS)


def bounds(a, x0, y0, x1, y1, thr=60):
    reg = a[y0:y1, x0:x1]
    ys, xs = np.where(reg.max(axis=2) > thr)
    return x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max()


def fix(name, by_box, av_box, small_av_box):
    im = Image.open(f"{STAGE}/{name}.png").convert("RGB")
    a = np.array(im)
    d = ImageDraw.Draw(im)

    # credit line
    bx0, by0, bx1, by1 = bounds(a, *by_box)
    cx = (bx0 + bx1) / 2
    d.rectangle((bx0 - 4, by0 - 4, bx1 + 4, by1 + 4), fill=(0, 0, 0))
    font = ImageFont.truetype(FONT, 20)
    text = "MCorp Estimate"
    w = d.textlength(text, font=font)
    # "By Qamarul" cap top sits at by0; Noto ascent offset ~5px at 20px
    d.text((cx - w / 2, by0 - 5), text, font=font, fill=(205, 205, 205))

    # big avatar
    ax0, ay0, ax1, ay1 = bounds(a, *av_box)
    size = max(ax1 - ax0, ay1 - ay0) + 1
    d.ellipse((ax0 - 2, ay0 - 2, ax1 + 2, ay1 + 2), fill=(0, 0, 0))
    av = disc(size)
    im.paste(av, (int(ax0), int(ay0)), av)

    # small avatar in the input bar chip
    if small_av_box:
        sx0, sy0, sx1, sy1 = bounds(a, *small_av_box)
        ss = max(sx1 - sx0, sy1 - sy0) + 1
        bg = tuple(int(v) for v in a[sy0 - 3, sx0 - 3])
        d.ellipse((sx0 - 1, sy0 - 1, sx1 + 1, sy1 + 1), fill=bg)
        sm = disc(ss)
        im.paste(sm, (int(sx0), int(sy0)), sm)

    im.save(f"{STAGE}/{name}-mcorp.png")
    print(name, "credit", (bx0, by0, bx1, by1), "avatar", (ax0, ay0, ax1, ay1))


# boxes are search windows: (x0, y0, x1, y1)
fix("sor1", (800, 220, 1110, 252), (900, 85, 1010, 160), (553, 500, 580, 529))
fix("sor2", (596, 220, 906, 252), (696, 85, 806, 160), (349, 501, 376, 530))
fix("bq2", (650, 125, 960, 157), (750, 0, 860, 68), (418, 394, 447, 424))
