"""Storyboard JPG pages for the Gadek Hotspring video, built from frames of the rendered film.
usage: python3 scripts/gadek_storyboard.py SOURCE OUTDIR
SOURCE is the rendered MP4, or a folder of `hyperframes snapshot --keep` stills (at-<t>s.png)."""
import json, os, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..", "edits", "gadek-hotspring")
FONT = f"{ROOT}/hf/assets/fonts/Montserrat.ttf"


def font(size, weight="Regular"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


CU = json.load(open(f"{ROOT}/cues.json"))
TOTAL = CU["total"]
# where each scene sits in "Dreaming Big" (sections from librosa)
MUSIC = [(0, "Intro: piano lembut"), (19.5, "Muzik mula naik"), (28.5, "Bahagian utama, rentak penuh"),
         (88.0, "Kemuncak muzik"), (95.4, "Muzik mula turun"), (101.4, "Penutup muzik, resolusi")]


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def music_at(t0, t1):
    parts = [n for k, (t, n) in enumerate(MUSIC) if t < t1 - 0.5 and (k + 1 == len(MUSIC) or MUSIC[k + 1][0] > t0 + 0.5)]
    return " → ".join(parts)


# (name, time range, frame time, visual, music, on-screen text)
SCENES = [(sc["name"], f"{mmss(sc['start'])}–{mmss(sc['end'])}", sc["frame"], sc["visual"], music_at(sc["start"], sc["end"]), sc["text"])
          for sc in CU["scenes"]]
if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "--times":
    print(",".join(f"{s[2]:g}" for s in SCENES))
    sys.exit()

video, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
PW, COLS, ROWS = 2480, 2, 4
M, GAP = 90, 60
CW = (PW - 2 * M - GAP) // COLS
IH = CW * 9 // 16
TH = 330
HEAD = 260
PH = HEAD + ROWS * (IH + TH + GAP) + M
NAVY, ORANGE, INK, GREY = (10, 40, 84), (240, 90, 31), (25, 30, 40), (95, 105, 120)

frames = []
for i, s in enumerate(SCENES):
    p = f"{out}/_f{i:02d}.jpg"
    if os.path.isdir(video):
        Image.open(f"{video}/at-{s[2]:g}s.png").convert("RGB").resize((CW, IH), Image.LANCZOS).save(p, quality=95)
    else:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s[2]), "-i", video, "-frames:v", "1", "-vf", f"scale={CW}:{IH}", p], check=True)
    frames.append(p)

per = COLS * ROWS
pages = [SCENES[i:i + per] for i in range(0, len(SCENES), per)]
for pi, page in enumerate(pages):
    im = Image.new("RGB", (PW, PH), (246, 248, 251))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, PW, 190], fill=NAVY)
    d.text((M, 50), "STORYBOARD · VIDEO KORPORAT GADEK HOTSPRING WELLNESS & SPA RESORT", font=font(46, "Bold"), fill="white")
    d.text((M, 120), f"16:9 · 1920×1080 · {mmss(TOTAL)} · Tanpa VO · Muzik: Dreaming Big (Mixkit) · Halaman {pi + 1}/{len(pages)}", font=font(30, "Medium"), fill=(170, 200, 240))
    for j, s in enumerate(page):
        k = pi * per + j
        x = M + (j % COLS) * (CW + GAP)
        y = HEAD + (j // COLS) * (IH + TH + GAP)
        im.paste(Image.open(frames[k]), (x, y))
        d.rectangle([x, y, x + 120, y + 64], fill=ORANGE)
        d.text((x + 22, y + 10), f"{k + 1:02d}", font=font(40, "Bold"), fill="white")
        ty = y + IH + 18
        d.text((x, ty), s[0].upper(), font=font(34, "Bold"), fill=NAVY)
        tw = d.textlength(s[1], font=font(28, "SemiBold"))
        d.text((x + CW - tw, ty + 4), s[1], font=font(28, "SemiBold"), fill=ORANGE)
        ty += 52
        for label, body, col in (("VISUAL", s[3], INK), ("MUZIK", s[4], INK), ("TEKS", s[5], GREY)):
            lines = textwrap.wrap(body, 80)
            d.text((x, ty), label, font=font(22, "Bold"), fill=ORANGE)
            for ln in lines[:3]:
                d.text((x + 130, ty), ln, font=font(23, "Regular"), fill=col)
                ty += 31
            ty += 8
    rows = (len(page) + COLS - 1) // COLS
    im = im.crop((0, 0, PW, HEAD + rows * (IH + TH + GAP) + M - GAP))
    im.save(f"{out}/Storyboard-Gadek-Hotspring-{pi + 1}.jpg", quality=90)
    print("page", pi + 1)
for p in frames:
    os.remove(p)
