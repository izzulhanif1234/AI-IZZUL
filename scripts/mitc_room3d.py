"""AI 3D camera moves for still room photos (2.5D parallax from a depth map).

usage: python3 scripts/mitc_room3d.py OUT_DIR IMG:MOVE[:SECONDS] ...
  MOVE: dolly_in | pull_out | orbit_left | orbit_right | crane_up | crane_down | push_right | push_left

Depth comes from Depth Anything V2 (small).  Each output pixel is mapped back to the
source with a depth-dependent zoom and shift (near objects move more than far ones),
which gives the camera a real sense of moving through the room.
"""
import os
import subprocess
import sys

import cv2
import numpy as np
import torch
from PIL import Image
from transformers import pipeline

W, H, FPS = 1920, 1080, 30

# start/end of (zoom, near-zoom k, shift x, shift y); shifts are fractions of width
MOVES = {
    "dolly_in":    ((1.12, 0.00, 0.000, 0.000), (1.26, 0.10, 0.000, -0.010)),
    "pull_out":    ((1.28, 0.10, 0.000, -0.010), (1.13, 0.00, 0.000, 0.000)),
    "orbit_left":  ((1.18, 0.03, 0.040, 0.000), (1.20, 0.03, -0.040, 0.000)),
    "orbit_right": ((1.18, 0.03, -0.040, 0.000), (1.20, 0.03, 0.040, 0.000)),
    "crane_up":    ((1.17, 0.02, 0.000, 0.030), (1.22, 0.04, 0.000, -0.030)),
    "crane_down":  ((1.22, 0.04, 0.000, -0.030), (1.17, 0.02, 0.000, 0.030)),
    "push_right":  ((1.15, 0.00, -0.030, 0.000), (1.27, 0.08, 0.030, -0.006)),
    "push_left":   ((1.15, 0.00, 0.030, 0.000), (1.27, 0.08, -0.030, -0.006)),
}


def cover(img, w, h):
    ih, iw = img.shape[:2]
    s = max(w / iw, h / ih)
    nw, nh = int(round(iw * s)), int(round(ih * s))
    img = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
    x, y = (nw - w) // 2, (nh - h) // 2
    return img[y:y + h, x:x + w]


def ease(t):
    return t * t * (3 - 2 * t) if t < 1 else 1.0


def main():
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    est = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device="cpu")
    torch.set_grad_enabled(False)
    for spec in sys.argv[2:]:
        parts = spec.split(":")
        path, move = parts[0], parts[1]
        secs = float(parts[2]) if len(parts) > 2 else 3.0
        # work at 1.25x output size so the warp stays sharp
        sw, sh = int(W * 1.25), int(H * 1.25)
        src = cover(cv2.imread(path, cv2.IMREAD_COLOR), sw, sh)
        depth = np.array(est(Image.fromarray(cv2.cvtColor(src, cv2.COLOR_BGR2RGB)))["predicted_depth"].squeeze(), dtype=np.float32)
        depth = cv2.resize(depth, (sw, sh), interpolation=cv2.INTER_CUBIC)
        lo, hi = np.percentile(depth, 2), np.percentile(depth, 98)
        lin = np.clip((depth - lo) / (hi - lo + 1e-6), 0, 1)     # 1 = near
        rank = np.argsort(np.argsort(depth.ravel())).reshape(depth.shape) / depth.size
        d = (0.5 * lin + 0.5 * rank).astype(np.float32)          # spread depth evenly so the whole room moves
        d = cv2.GaussianBlur(d, (0, 0), sw / 300)                # soften edges -> fewer tears
        name = os.path.splitext(os.path.basename(path))[0]
        cv2.imwrite(os.path.join(out_dir, f"{name}-depth.png"), (d * 255).astype(np.uint8))

        gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
        px, py = (gx - W / 2) / W, (gy - H / 2) / W               # centred, width units
        a, b = MOVES[move]
        n = int(round(secs * FPS))
        out = os.path.join(out_dir, f"{name}.mp4")
        ff = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "14",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
        for f in range(n):
            e = ease(f / (n - 1))
            z, k, sx, sy = (a[i] + (b[i] - a[i]) * e for i in range(4))
            # two fixed-point passes: look depth up where the pixel actually comes from
            dd = np.full_like(px, 0.5)
            for _ in range(2):
                ux = px / (z * (1 + k * dd)) + sx * (dd - 0.35)
                uy = py / (z * (1 + k * dd)) + sy * (dd - 0.35)
                mx, my = ux * sw + sw / 2, uy * sw + sh / 2
                dd = cv2.remap(d, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            frame = cv2.remap(src, mx, my, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
            ff.stdin.write(frame.tobytes())
        ff.stdin.close()
        ff.wait()
        print("wrote", out, move, n, "frames", flush=True)


if __name__ == "__main__":
    main()
