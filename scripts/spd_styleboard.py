"""SPD GREEN style board: two premium looks applied to five key frames.

Writes edits/spd-green/styleboard/styleboard.html and renders one JPG per direction
(A_emerald-noir.jpg, B_porcelain.jpg) plus each frame at full size.
"""
import pathlib
import subprocess

ROOT = pathlib.Path("/home/user/AI-IZZUL")
OUT = ROOT / "edits/spd-green/styleboard"
OUT.mkdir(parents=True, exist_ok=True)
A = "../hf/assets"

THEMES = {
    "A": dict(name="A · EMERALD NOIR", sub="Gelap sinematik · aksen emas halus · serif elegan",
              bg="radial-gradient(120% 90% at 18% 10%, #12402f 0%, #071a13 45%, #030806 100%)",
              ink="#F2EFE6", soft="#A9BDB2", accent="#C9A55C", accent2="#8FD0A6", line="rgba(201,165,92,.55)",
              panel="rgba(255,255,255,.035)", panelb="rgba(255,255,255,.10)", shadow="0 60px 140px rgba(0,0,0,.65)",
              grain=0.07, dark=True),
    "B": dict(name="B · PORCELAIN", sub="Cerah premium · hijau zamrud · emas lembut",
              bg="radial-gradient(120% 90% at 80% 0%, #ffffff 0%, #f6f3ec 45%, #ebe5d8 100%)",
              ink="#0E3326", soft="#5E6F67", accent="#B0823A", accent2="#1F6B4F", line="rgba(176,130,58,.55)",
              panel="rgba(255,255,255,.75)", panelb="rgba(14,51,38,.10)", shadow="0 50px 110px rgba(30,40,30,.18)",
              grain=0.035, dark=False),
}

ICONS = {  # thin geometric line icons, 64x64 viewBox
    "paper": '<rect x="14" y="10" width="30" height="40" rx="2"/><rect x="20" y="16" width="30" height="40" rx="2"/><path d="M26 28h18M26 34h18M26 40h12"/>',
    "cabinet": '<rect x="14" y="8" width="36" height="48" rx="3"/><path d="M14 24h36M14 40h36M28 16h8M28 32h8M28 48h8"/>',
    "dup": '<rect x="10" y="14" width="26" height="34" rx="2"/><rect x="28" y="16" width="26" height="34" rx="2"/><path d="M16 24h14M16 30h14M34 26h14M34 32h14"/>',
    "hourglass": '<path d="M20 8h24M20 56h24M22 8c0 14 20 16 20 24s-20 10-20 24M42 8c0 14-20 16-20 24s20 10 20 24"/>',
    "lost": '<rect x="12" y="14" width="28" height="36" rx="2"/><path d="M18 24h16M18 30h16"/><path d="M46 18c4-6 12-2 10 4-1 3-5 4-5 8M51 36v1" />',
    "cost": '<circle cx="30" cy="32" r="20"/><path d="M24 26c0-4 12-4 12 0s-12 4-12 8 12 4 12 0M30 18v4M30 42v4"/><path d="M52 18v18M46 30l6 6 6-6"/>',
}


def icon(k, color, w=86):
    return (f'<svg viewBox="0 0 64 64" style="width:{w}px;height:{w}px" fill="none" stroke="{color}" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>')


def leafline(color, w=60):
    return (f'<svg viewBox="0 0 64 64" style="width:{w}px;height:{w}px" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round">'
            f'<path d="M32 58C14 46 12 22 32 6c20 16 18 40 0 52z"/><path d="M32 56V14M32 38l-9-8M32 28l9-8"/></svg>')


def base(T, inner):
    grain = (f'<svg class="gr" width="100%" height="100%"><filter id="n{T["name"][0]}"><feTurbulence type="fractalNoise" baseFrequency=".9" '
             f'numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 1 0"/></filter>'
             f'<rect width="100%" height="100%" filter="url(#n{T["name"][0]})" opacity="{T["grain"]}"/></svg>')
    vig = ('<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(0,0,0,.55))"></div>'
           if T["dark"] else '<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,transparent 60%,rgba(120,100,60,.10))"></div>')
    badge = (f'<img src="{A}/img/logo-pptx.png" style="position:absolute;right:44px;top:30px;width:118px;transform:perspective(600px) rotateY(-18deg);'
             f'filter:drop-shadow(0 0 1.2px #fff) drop-shadow(0 0 1.2px #fff) drop-shadow(0 6px 10px rgba(0,0,0,.35))">')
    return (f'<div class="fr" style="background:{T["bg"]};color:{T["ink"]}">{inner}{vig}{grain}{badge}</div>')


def kick(T, t):
    return (f'<div style="display:flex;align-items:center;gap:18px;font:600 20px Manrope;letter-spacing:.42em;color:{T["accent"]}">'
            f'<i style="width:56px;height:1px;background:{T["accent"]};display:block"></i>{t}</div>')


def f_title(T):
    return base(T, f"""
<div style="position:absolute;left:0;right:0;top:250px;display:flex;justify-content:center">{kick(T, "PERBADANAN MELAKA")}</div>
<div style="position:absolute;left:0;right:0;top:300px;text-align:center;font:300 300px/1 Fraunces;letter-spacing:-.03em">SPD</div>
<div style="position:absolute;left:0;right:0;top:330px;display:flex;justify-content:center;transform:translateX(330px)">{leafline(T["accent2"], 76)}</div>
<div style="position:absolute;left:0;right:0;top:640px;text-align:center;font:300 46px Manrope;letter-spacing:.02em">Sistem Pengurusan Data Bersepadu</div>
<div style="position:absolute;left:760px;right:760px;top:722px;height:1px;background:{T["line"]}"></div>
<div style="position:absolute;left:0;right:0;top:752px;text-align:center;font:300 italic 36px Fraunces;color:{T["accent"]}">Inovasi digital ke arah pengurusan hijau dan lestari</div>""")


def f_problem(T):
    items = [("paper", "Penggunaan kertas tinggi"), ("cabinet", "Ruang simpanan fizikal besar"), ("dup", "Pertindihan data"),
             ("hourglass", "Carian maklumat lambat"), ("lost", "Risiko kehilangan dokumen"), ("cost", "Kos operasi tinggi")]
    cells = "".join(
        f'<div style="position:absolute;left:{170 + (i % 3) * 540}px;top:{350 + (i // 3) * 300}px;width:460px">'
        f'<div style="display:flex;align-items:flex-start;gap:28px">{icon(k, T["ink"] if not T["dark"] else T["ink"])}'
        f'<div><div style="font:300 italic 40px Fraunces;color:{T["accent"]}">0{i + 1}</div>'
        f'<div style="font:400 30px/1.3 Manrope;margin-top:6px">{t}</div></div></div>'
        f'<div style="margin-top:34px;height:1px;background:{T["line"]};opacity:.5"></div></div>' for i, (k, t) in enumerate(items))
    return base(T, f"""
<div style="position:absolute;left:170px;top:130px">{kick(T, "SEBELUM SPD")}</div>
<div style="position:absolute;left:170px;top:180px;font:300 82px/1.05 Fraunces;letter-spacing:-.02em">Enam cabaran <i style="color:{T["accent"]}">utama</i></div>
{cells}""")


def screen(img, x, y, w, rot, T, extra=""):
    h = round(w * 912 / 1920)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w + 28}px;transform:perspective(2400px) {rot};">'
            f'<div style="padding:14px;border-radius:22px;background:linear-gradient(160deg,#2b2f31,#121416);box-shadow:{T["shadow"]},0 0 0 1px rgba(255,255,255,.08) inset">'
            f'<div style="position:relative;width:{w}px;height:{h}px;border-radius:10px;overflow:hidden;background:url({img}) left top/cover">{extra}'
            f'<div style="position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.10),transparent 35%)"></div></div></div></div>')


def f_demo(T):
    w = 1180
    k = w / 1920
    # spotlight on the map: dim everything but the map rectangle
    x0, y0, x1, y1 = 44 * k, 260 * k, 1856 * k, 766 * k
    spot = (f'<div style="position:absolute;inset:0;background:rgba(5,12,9,.55);clip-path:polygon(0 0,100% 0,100% 100%,0 100%,0 {y0}px,{x0}px {y0}px,{x0}px {y1}px,{x1}px {y1}px,{x1}px {y0}px,0 {y0}px)"></div>'
            f'<div style="position:absolute;left:{x0}px;top:{y0}px;width:{x1 - x0}px;height:{y1 - y0}px;border:1.5px solid {T["accent"]};border-radius:6px;box-shadow:0 0 40px rgba(201,165,92,.35)"></div>'
            f'<svg viewBox="0 0 60 80" style="position:absolute;left:{860 * k}px;top:{470 * k}px;width:30px;filter:drop-shadow(0 4px 8px rgba(0,0,0,.5))"><path d="M5 5 L5 65 L20 50 L32 75 L42 70 L30 46 L52 46Z" fill="#fff" stroke="#111" stroke-width="3"/></svg>')
    return base(T, f"""
{screen(f"{A}/ui/s77.jpg", 640, 200, w, "rotateY(-9deg) rotateX(3deg)", T, spot)}
<div style="position:absolute;left:120px;top:690px;width:460px">
  {kick(T, "LAMAN UTAMA")}
  <div style="font:300 60px/1.08 Fraunces;margin-top:20px;letter-spacing:-.01em">Taburan premis &amp; tanah <i style="color:{T["accent"]}">milik MCORP</i></div>
  <div style="font:400 24px/1.5 Manrope;color:{T["soft"]};margin-top:18px">Seluruh negeri Melaka dalam satu paparan.</div>
</div>""")


def f_stat(T):
    return base(T, f"""
<div style="position:absolute;left:170px;top:200px">{kick(T, "PRODUKTIVITI · PROSES SEWAAN")}</div>
<div style="position:absolute;left:170px;top:300px;display:flex;align-items:flex-end;gap:60px">
  <div style="position:relative;font:300 250px/1 Fraunces;color:{T["soft"]};opacity:.45">14<i style="position:absolute;left:-6px;right:-6px;top:55%;height:2px;background:{T["accent"]};display:block"></i></div>
  <div style="font:300 120px/1 Fraunces;color:{T["accent"]};margin-bottom:60px">→</div>
  <div style="font:300 360px/0.9 Fraunces;letter-spacing:-.04em">3</div>
  <div style="font:400 64px Manrope;margin-bottom:40px">hari</div>
</div>
<div style="position:absolute;left:170px;top:760px;width:1580px;height:1px;background:{T["line"]}"></div>
<div style="position:absolute;left:170px;top:800px;display:flex;gap:120px;font:400 28px Manrope;color:{T["soft"]}">
  <div><b style="font:300 64px Fraunces;color:{T["ink"]}">11</b>&nbsp; hari dijimatkan</div>
  <div><b style="font:300 64px Fraunces;color:{T["ink"]}">−79%</b>&nbsp; tempoh proses</div>
</div>""")


def f_dash(T):
    tiles = [("Kertas A4", "−25.4%"), ("Dakwat pencetak", "−39.7%"), ("Proses sewaan", "−79%"), ("Semakan aset", "−90%"),
             ("Tenaga kerja", "−50%"), ("Penjimatan / tahun", "RM217,836")]
    th = "".join(f'<div style="padding:26px 28px;border-radius:18px;background:{T["panel"]};border:1px solid {T["panelb"]};backdrop-filter:blur(14px)">'
                 f'<div style="font:600 15px Manrope;letter-spacing:.24em;color:{T["soft"]};text-transform:uppercase">{a}</div>'
                 f'<div style="font:300 {54 if i < 5 else 46}px/1.1 Fraunces;margin-top:14px;color:{T["ink"] if i < 5 else T["accent"]}">{b}</div></div>'
                 for i, (a, b) in enumerate(tiles))
    circ = 2 * 3.14159 * 120
    gauge = (f'<svg viewBox="0 0 280 280" style="width:300px;height:300px"><circle cx="140" cy="140" r="120" stroke="{T["panelb"]}" stroke-width="6" fill="none"/>'
             f'<circle cx="140" cy="140" r="120" stroke="{T["accent"]}" stroke-width="6" fill="none" stroke-linecap="round" stroke-dasharray="{circ * .82:.0f} {circ:.0f}" transform="rotate(-90 140 140)"/>'
             f'<text x="140" y="160" text-anchor="middle" font-family="Fraunces" font-weight="300" font-size="96" fill="{T["ink"]}">82</text></svg>')
    return base(T, f"""
<div style="position:absolute;left:150px;top:150px">{kick(T, "AKAN DATANG")}</div>
<div style="position:absolute;left:150px;top:200px;font:300 110px/1 Fraunces;letter-spacing:-.02em">SPD <i style="color:{T["accent"]}">2.0</i></div>
<div style="position:absolute;left:150px;top:330px;font:400 30px Manrope;color:{T["soft"]}">Green Dashboard · SPD Green Index</div>
<div style="position:absolute;left:150px;top:480px;text-align:center">{gauge}<div style="font:600 15px Manrope;letter-spacing:.24em;color:{T["soft"]};margin-top:10px">OVERALL GREEN INDEX</div></div>
<div style="position:absolute;left:560px;top:430px;width:1220px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px">{th}</div>""")


FRAMES = [("01", "Tajuk", f_title), ("02", "Masalah (ganti doodle)", f_problem), ("03", "Demo sistem (fokus)", f_demo),
          ("04", "Statistik (ganti kalendar)", f_stat), ("05", "SPD 2.0 + Green Dashboard", f_dash)]

CSS = """*{margin:0;padding:0;box-sizing:border-box}body{background:#111}
.fr{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:Manrope}
.gr{position:absolute;inset:0;pointer-events:none;mix-blend-mode:overlay}"""


def build():
    html = ['<!doctype html><html><head><meta charset="utf-8">',
            '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;1,9..144,300&family=Manrope:wght@300;400;500;600;700&display=block" rel="stylesheet">',
            f'<style>{CSS}</style></head><body>']
    for key, T in THEMES.items():
        for n, label, fn in FRAMES:
            html.append(f'<div id="{key}{n}">{fn(T)}</div>')
    html.append("</body></html>")
    (OUT / "styleboard.html").write_text("\n".join(html), encoding="utf-8")


JS = r"""
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--proxy-server=' + (process.env.HTTPS_PROXY || 'direct://'), '--ignore-certificate-errors'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + process.argv[2] + '/styleboard.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  for (const id of process.argv.slice(3)) await p.locator('#' + id).screenshot({ path: process.argv[2] + '/f_' + id + '.jpg', type: 'jpeg', quality: 90 });
  await b.close();
})();
"""


if __name__ == "__main__":
    build()
    js = OUT / "_render.js"
    js.write_text(JS)
    ids = [k + n for k in THEMES for n, _, _ in FRAMES]
    subprocess.run(["node", str(js), str(OUT)] + ids, check=True, cwd=str(ROOT))
    js.unlink()
    # one board per direction: hero frame large + four smaller
    from PIL import Image, ImageDraw, ImageFont
    for key, T in THEMES.items():
        ims = [Image.open(OUT / f"f_{key}{n}.jpg") for n, _, _ in FRAMES]
        W = 2400
        board = Image.new("RGB", (W, 200 + 1350 + 40 + 2 * (608 + 70)), "#0d0f0e" if T["dark"] else "#efeae0")
        d = ImageDraw.Draw(board)
        try:
            f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
            f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        except OSError:
            f1 = f2 = ImageFont.load_default()
        fg = "#f2efe6" if T["dark"] else "#0e3326"
        d.text((60, 50), T["name"], fill=fg, font=f1)
        d.text((60, 125), T["sub"], fill=T["accent"], font=f2)
        board.paste(ims[0].resize((W, 1350)), (0, 200))
        y = 200 + 1350 + 40
        for i, (im, (n, label, _)) in enumerate(zip(ims[1:], FRAMES[1:])):
            x = (i % 2) * (W // 2)
            yy = y + (i // 2) * (608 + 70)
            d.text((x + 30, yy + 8), f"{n}  {label}", fill=fg, font=f2)
            board.paste(im.resize((W // 2 - 20, 608 - 10 - 0)), (x + 10, yy + 60))
        board.save(OUT / f"{key}_{'emerald-noir' if key == 'A' else 'porcelain'}.jpg", quality=88)
    print("ok")
