"""Scan island source videos for usable drone shots.

For each video: decode at 4 fps (small), score every sample for
  text   - share of pixels in the series' overlay colours (yellow pill, pink/magenta box)
  motion - mean abs difference to the previous sample (camera movement; spikes = cuts)
  sharp  - Laplacian variance (focus / detail)
  sat    - mean saturation (turquoise sea reads well)
and write <out>/<name>.json plus a contact sheet <out>/<name>.jpg (one frame every 3 s,
timestamped, red border where overlay text was detected).

usage: python3 scripts/pulau_scan.py <video_dir> <out_dir>
"""
import json
import os
import re
import subprocess
import sys

import cv2
import numpy as np

FPS = 4
W, H = 320, 180


def frames(path):
    cmd = ['ffmpeg', '-v', 'error', '-i', path, '-vf', f'fps={FPS},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = W * H * 3
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    p.wait()


def overlay_text(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    yellow = (h >= 22) & (h <= 34) & (s > 170) & (v > 200)
    pink = (h >= 155) & (h <= 175) & (s > 140) & (v > 150)
    return float((yellow | pink).mean())


def scan(path):
    rows, prev, keep = [], None, []
    for i, f in enumerate(frames(path)):
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        motion = float(np.abs(g.astype(np.int16) - prev).mean()) if prev is not None else 0.0
        prev = g.astype(np.int16)
        rows.append({
            't': round(i / FPS, 2),
            'text': round(overlay_text(f), 4),
            'motion': round(motion, 2),
            'sharp': round(float(cv2.Laplacian(g, cv2.CV_64F).var()), 1),
            'sat': round(float(cv2.cvtColor(f, cv2.COLOR_BGR2HSV)[..., 1].mean()), 1),
        })
        if i % (FPS * 3) == 0:
            keep.append((i / FPS, f.copy(), rows[-1]['text'] > 0.004))
    return rows, keep


def sheet(keep, out):
    cols, tw, th = 6, 300, 169
    rows = (len(keep) + cols - 1) // cols
    canvas = np.full((rows * (th + 6) + 6, cols * (tw + 6) + 6, 3), 30, np.uint8)
    for k, (t, f, txt) in enumerate(keep):
        r, c = divmod(k, cols)
        y, x = 6 + r * (th + 6), 6 + c * (tw + 6)
        canvas[y:y + th, x:x + tw] = cv2.resize(f, (tw, th))
        if txt:
            cv2.rectangle(canvas, (x, y), (x + tw - 1, y + th - 1), (40, 40, 230), 5)
        label = f'{int(t // 60)}:{int(t % 60):02d}'
        cv2.rectangle(canvas, (x, y), (x + 62, y + 24), (0, 0, 0), -1)
        cv2.putText(canvas, label, (x + 5, y + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imwrite(out, canvas, [cv2.IMWRITE_JPEG_QUALITY, 85])


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for fn in sorted(os.listdir(src)):
        if not fn.endswith('.mp4'):
            continue
        name = re.match(r'Pulau (\w+)', fn).group(1).lower()
        if os.path.exists(os.path.join(out, name + '.json')):
            continue
        rows, keep = scan(os.path.join(src, fn))
        json.dump({'file': fn, 'fps': FPS, 'rows': rows}, open(os.path.join(out, name + '.json'), 'w'))
        sheet(keep, os.path.join(out, name + '.jpg'))
        print(name, len(rows) / FPS, 's', flush=True)


if __name__ == '__main__':
    main()
