"""Generate topographic contour-line SVGs used by film.html.

  assets/topo/bg-<n>.svg   full-frame 1920x1080 contour fields (island-like bumps + smooth noise)
  assets/topo/ring.svg     wobbly concentric contours around the centre, for the "topo" reveal transition
  assets/topo/topo.js      both, as window.TOPO for pages opened from file://
Each <path> carries pathLength=1 so the page can draw it on with stroke-dashoffset.

usage: python3 topo.py
"""
import json
import os

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'assets', 'topo')
W, H = 1920, 1080
PAD = 60   # fields extend past the frame so contours never trace its border


def noise(seed, cells, w=W + 2 * PAD, h=H + 2 * PAD):
    rng = np.random.default_rng(seed)
    g = rng.random((cells[1], cells[0])).astype(np.float32)
    return cv2.GaussianBlur(cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC), (0, 0), 25)


def field(seed):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[-PAD:H + PAD, -PAD:W + PAD].astype(np.float32)
    f = np.zeros(xx.shape, np.float32)
    for _ in range(6):                       # island-like bumps
        cx, cy = rng.uniform(-100, W + 100), rng.uniform(-100, H + 100)
        sx, sy = rng.uniform(160, 420), rng.uniform(120, 320)
        f += rng.uniform(.6, 1.2) * np.exp(-(((xx - cx) / sx) ** 2 + ((yy - cy) / sy) ** 2))
    return f + .55 * noise(seed + 1, (9, 6)) + .25 * noise(seed + 2, (20, 12))


def ring_field(seed):
    yy, xx = np.mgrid[-PAD:H + PAD, -PAD:W + PAD].astype(np.float32)
    d = np.hypot((xx - W / 2) / W, (yy - H / 2) / W)
    return -(d + .06 * noise(seed, (8, 5)) + .02 * noise(seed + 1, (22, 13)))


def paths(f, levels):
    out = []
    lo, hi = float(f.min()), float(f.max())
    for i, lv in enumerate(np.linspace(lo, hi, levels + 2)[1:-1]):
        m = (f >= lv).astype(np.uint8) * 255
        cs, _ = cv2.findContours(m, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        for c in cs:
            if len(c) < 40:
                continue
            c = cv2.approxPolyDP(c, 1.2, True)[:, 0, :] - PAD
            d = 'M' + ' L'.join(f'{x} {y}' for x, y in c) + ' Z'
            out.append((i, d))
    return out


def svg(ps, levels, cls):
    body = '\n'.join(f'<path class="{cls} l{i}{" major" if i % 4 == 0 else ""}" pathLength="1" d="{d}"/>' for i, d in ps)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" data-levels="{levels}">\n'
            f'{body}\n</svg>\n')


def main():
    os.makedirs(OUT, exist_ok=True)
    for n, seed in enumerate([3, 11, 27]):
        ps = paths(field(seed), 22)
        open(os.path.join(OUT, f'bg-{n}.svg'), 'w').write(svg(ps, 22, 'c'))
        print('bg', n, len(ps), 'paths')
    ps = paths(ring_field(5), 26)
    open(os.path.join(OUT, 'ring.svg'), 'w').write(svg(ps, 26, 'r'))
    print('ring', len(ps), 'paths')
    # same SVGs as a script so pages opened from file:// can inline them without fetch()
    js = {'bg': [open(os.path.join(OUT, f'bg-{n}.svg')).read() for n in range(3)], 'ring': open(os.path.join(OUT, 'ring.svg')).read()}
    open(os.path.join(OUT, 'topo.js'), 'w').write('window.TOPO=' + json.dumps(js) + ';\n')


if __name__ == '__main__':
    main()
