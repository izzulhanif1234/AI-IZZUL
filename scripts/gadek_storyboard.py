"""Storyboard JPG pages for the Gadek Hotspring video, built from frames of the rendered film.
usage: python3 scripts/gadek_storyboard.py SOURCE OUTDIR
SOURCE is the rendered MP4, or a folder of `hyperframes snapshot --keep` stills (at-<t>s.png)."""
import json, os, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..", "edits", "gadek-hotspring")
VO = {l["id"]: l["text"] for l in json.load(open(f"{ROOT}/vo_lines.json"))}
FONT = f"{ROOT}/hf/assets/fonts/Montserrat.ttf"


def font(size, weight="Regular"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


CU = json.load(open(f"{ROOT}/cues.json"))
C, SH, TOTAL = CU["cues"], CU["shots"], CU["total"]
STARTS = [SH[i]["t"] for i in (0, 2, 3, 5, 7, 9, 11, 13, 14, 16, 20, 21, 22)] + [TOTAL]


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


# (scene, frame time, footage, VO ids, on-screen text); time ranges come from the shot cuts
SCENES = [
    ("Pembukaan", C["loc_in"] + 1.2, "Drone: kampung & bukit Alor Gajah → \"tapi di sini\": gerbang Kompleks Air Panas Gadek", ["v01"], "Pin lokasi: ALOR GAJAH · MELAKA"),
    ("Tajuk", C["ttl_in"] + 2.5, "Drone: aerial penuh kompleks", ["v02"], "Logo Gadek Hotspring Wellness & Spa Resort + kilatan; Kampung Ganun · Alor Gajah · Melaka"),
    ("01 · Sejarah (1)", C["c1_out"] - 1.5, "Drone kampung + papan tanda Geotapak (gred vintaj, rasa lama)", ["v03"], "Rahsia Zaman British / Air yang dipercayai mampu mengubati penyakit"),
    ("01 · Sejarah (2)", C["c1b_out"] - 2.0, "Kolam air panas & chalet (warna kembali)", ["v04"], "Bukan Air Biasa / Mata air panas semula jadi dari dalam bumi"),
    ("02 · Kini", C["c2_out"] - 0.8, "Drone naik dedah kompleks → ruang legar dengan pengunjung", ["v05"], "Warisan Dihidupkan Semula; kad 16.12.2024 Mula beroperasi; kad 30 Warga kerja (kiraan naik)"),
    ("03 · Kolam Air Panas", C["c3_out"] - 0.8, "Orbit kolam air panas dewasa", ["v06"], "Lepaskan Penat + Lega ketegangan otot · Lancar peredaran darah · Tenangkan fikiran"),
    ("04 · Kolam Kanak-Kanak", C["c4_out"] - 0.8, "Push-in ke taman permainan air → orbit kolam kanak-kanak", ["v07"], "Dunia Si Kecil + Air suam semula jadi · Kawasan cetek · Selamat & mesra keluarga"),
    ("05 · Penginapan", C["rooms_out"] - 0.6, "Drone chalet berkolam peribadi → 4 kad bilik muncul ikut VO", ["v08"], "Satu Hari Tak Cukup? Kad: Single Room · Deluxe Room · Chalet Single · Chalet Family (tiada harga)"),
    ("05 · Penginapan (2)", C["c5b_out"] - 1.0, "Foto kolam peribadi chalet (Ken Burns)", ["v09"], "Berendam Di Bawah Bintang / Kolam air panas peribadi di setiap chalet"),
    ("06 · Kemudahan", C["c6_out"] - 0.8, "Ruang vendor → dewan → kafe → parkir", ["v10"], "Semuanya Ada Di Sini + Tapak vendor · Dewan majlis · Kafe · Surau · Parkir luas"),
    ("07 · Lokasi & Waktu", C["c7_out"] - 0.8, "Drone luas: kompleks & jalan utama", ["v11"], "Mudah Dikunjungi / Melalui jalan Melaka–Tampin; kad lokasi Kampung Ganun, 78000 Alor Gajah; Waktu operasi kolam (Isnin tutup)"),
    ("Tagline", C["tag_out"] - 0.4, "Drone melintasi chalet ke kolam kanak-kanak", ["v12"], "Rehatkan tubuh, tenangkan minda."),
    ("Penutup", C["end_in"] + 3.0, "Latar kabur + kad akhir", ["v13"], "Logo, Tempah sekarang · gadekhotspring.my, 010-279 6397, @gadekhotspring, @gadek.hotspring, alamat"),
]
SCENES = [(n, f"{mmss(STARTS[i])}–{mmss(STARTS[i + 1])}", round(t, 2), *rest) for i, (n, t, *rest) in enumerate(SCENES)]
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
    d.text((M, 120), f"16:9 · 1920×1080 · {mmss(TOTAL)} · VO Bahasa Melayu · Halaman {pi + 1}/{len(pages)}", font=font(30, "Medium"), fill=(170, 200, 240))
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
        for label, body, col in (("VISUAL", s[3], INK), ("VO", " ".join(VO[v] for v in s[4]), INK), ("TEKS", s[5], GREY)):
            lines = textwrap.wrap(body, 80)
            d.text((x, ty), label, font=font(22, "Bold"), fill=ORANGE)
            for ln in lines[:3]:
                d.text((x + 120, ty), ln, font=font(23, "Regular"), fill=col)
                ty += 31
            ty += 8
    rows = (len(page) + COLS - 1) // COLS
    im = im.crop((0, 0, PW, HEAD + rows * (IH + TH + GAP) + M - GAP))
    im.save(f"{out}/Storyboard-Gadek-Hotspring-{pi + 1}.jpg", quality=90)
    print("page", pi + 1)
for p in frames:
    os.remove(p)
