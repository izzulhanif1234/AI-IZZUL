"""SPD GREEN style board D: corporate look (MCORP navy + red, green for the green initiative, white, Montserrat).
Writes edits/spd-green/styleboard/D_korporat.jpg and f_D0*.jpg."""
import pathlib
import subprocess

ROOT = pathlib.Path("/home/user/AI-IZZUL")
OUT = ROOT / "edits/spd-green/styleboard"
A = "../hf/assets"
NAVY, RED, GREEN, LG, INK, GREY = "#2C3280", "#E31E26", "#1E8E5A", "#EAF5EF", "#1B2140", "#F3F5F8"

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#ccc}}
.fr{{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:Montserrat,sans-serif;color:{INK};background:#fff}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:64px;background:{NAVY};display:flex;align-items:center;padding:0 70px;color:#fff;font:600 20px Montserrat;letter-spacing:.08em}}
.bar:before{{content:"";position:absolute;left:0;top:-8px;width:100%;height:8px;background:linear-gradient(90deg,{RED} 0 30%,{GREEN} 30% 100%)}}
.card{{position:absolute;background:#fff;border-radius:18px;box-shadow:0 18px 40px rgba(27,33,64,.10),0 2px 6px rgba(27,33,64,.06)}}
.kick{{font:700 22px Montserrat;letter-spacing:.22em;color:{RED}}}
.h{{font:800 64px/1.1 Montserrat;color:{NAVY};letter-spacing:-.01em}}
"""


def logo():
    return f'<img src="{A}/img/logo-pptx.png" style="position:absolute;right:56px;top:34px;width:132px;transform:perspective(600px) rotateY(-14deg);z-index:9">'


def foot(t):
    return f'<div class="bar"><span>MCORP</span><span style="margin:0 18px;opacity:.5">|</span><span style="font-weight:500;letter-spacing:.04em">{t}</span></div>'


def ico(path, c="#fff", w=58):
    return f'<svg viewBox="0 0 64 64" style="width:{w}px;height:{w}px" fill="none" stroke="{c}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'


IC = {
    "paper": '<rect x="14" y="10" width="30" height="40" rx="3"/><path d="M22 22h14M22 30h14M22 38h8"/><path d="M20 54h30V18"/>',
    "cabinet": '<rect x="14" y="8" width="36" height="48" rx="4"/><path d="M14 24h36M14 40h36M28 16h8M28 32h8M28 48h8"/>',
    "dup": '<rect x="10" y="14" width="26" height="34" rx="3"/><rect x="28" y="18" width="26" height="34" rx="3"/>',
    "clock": '<circle cx="32" cy="32" r="22"/><path d="M32 20v13l9 6"/>',
    "lost": '<rect x="12" y="12" width="28" height="38" rx="3"/><path d="M46 20c3-6 12-3 10 3-1 4-5 4-5 8M51 38v1"/>',
    "cost": '<circle cx="32" cy="32" r="22"/><path d="M26 26c0-5 13-5 13 0s-13 5-13 10 13 5 13 0M32 17v4M32 43v4"/>',
}


def f_title():
    return f"""<div class="fr">
<div style="position:absolute;left:0;top:0;width:900px;height:1080px;background:url({A}/img/s01_freeze.jpg) center/cover;clip-path:polygon(0 0,100% 0,78% 100%,0 100%)"></div>
<div style="position:absolute;left:0;top:0;width:900px;height:1080px;background:linear-gradient(120deg,rgba(44,50,128,.88),rgba(44,50,128,.55));clip-path:polygon(0 0,100% 0,78% 100%,0 100%)"></div>
<div style="position:absolute;left:880px;top:0;width:60px;height:1080px;background:{GREEN};clip-path:polygon(40% 0,100% 0,60% 100%,0 100%)"></div>
<div style="position:absolute;left:1010px;top:300px;width:820px">
  <div class="kick">PERBADANAN MELAKA</div>
  <div style="font:800 150px/1 Montserrat;color:{NAVY};margin-top:16px;letter-spacing:-.02em">SPD</div>
  <div style="font:700 50px/1.15 Montserrat;color:{INK};margin-top:14px">Sistem Pengurusan Data Bersepadu</div>
  <div style="width:120px;height:8px;border-radius:4px;background:{GREEN};margin:34px 0 28px"></div>
  <div style="font:500 30px/1.45 Montserrat;color:#4A5170">Inovasi digital ke arah pengurusan<br>hijau dan lestari</div>
</div>
{logo()}{foot("Sistem Pengurusan Data Bersepadu (SPD)")}</div>"""


def f_problem():
    items = [("paper", "Penggunaan kertas tinggi"), ("cabinet", "Ruang simpanan fizikal besar"), ("dup", "Pertindihan data"),
             ("clock", "Carian maklumat lambat"), ("lost", "Risiko kehilangan dokumen"), ("cost", "Kos operasi tinggi")]
    cards = "".join(
        f'<div class="card" style="left:{110 + (i % 3) * 580}px;top:{330 + (i // 3) * 290}px;width:540px;height:240px;padding:36px 36px;display:flex;gap:30px;align-items:center">'
        f'<div style="width:110px;height:110px;flex:none;border-radius:24px;background:{NAVY if i % 2 == 0 else GREEN};display:flex;align-items:center;justify-content:center">{ico(IC[k])}</div>'
        f'<div><div style="font:800 26px Montserrat;color:{RED}">0{i + 1}</div><div style="font:700 32px/1.25 Montserrat;color:{INK};margin-top:6px">{t}</div></div></div>'
        for i, (k, t) in enumerate(items))
    return f"""<div class="fr" style="background:{GREY}">
<div style="position:absolute;left:110px;top:120px"><div class="kick">PENYATAAN MASALAH</div><div class="h" style="margin-top:12px">Enam cabaran sebelum SPD</div></div>
{cards}{logo()}{foot("Penyataan masalah")}</div>"""


def f_demo():
    W = 1200
    k = W / 1920
    x0, y0, x1, y1 = 44 * k, 260 * k, 1856 * k, 766 * k
    hl = (f'<div style="position:absolute;left:{x0 - 6}px;top:{y0 - 6}px;width:{x1 - x0 + 12}px;height:{y1 - y0 + 12}px;border:5px solid {GREEN};border-radius:12px;'
          f'box-shadow:0 0 0 9999px rgba(27,33,64,.35)"></div>')
    steps = [("01", "Laman Utama", True), ("02", "Aset Tak Alih", False), ("03", "Aset Alih", False), ("04", "Pengurusan Stor", False), ("05", "Modal Insan", False)]
    st = "".join(f'<div style="display:flex;align-items:center;gap:20px;padding:20px 26px;border-radius:14px;{"background:#fff;color:" + NAVY if on else "color:rgba(255,255,255,.75)"}">'
                 f'<span style="font:800 22px Montserrat;color:{RED if on else "rgba(255,255,255,.55)"}">{n}</span><span style="font:700 28px Montserrat">{t}</span></div>'
                 for n, t, on in steps)
    return f"""<div class="fr" style="background:{GREY}">
<div style="position:absolute;left:90px;top:110px"><div class="kick">DEMONSTRASI SISTEM</div><div class="h" style="margin-top:12px;font-size:56px">Laman Utama SPD</div></div>
<div style="position:absolute;left:90px;top:270px;width:{W + 32}px;padding:16px;border-radius:22px;background:#1f2330;box-shadow:0 30px 70px rgba(27,33,64,.25)">
  <div style="position:relative;width:{W}px;height:{round(W * 912 / 1920)}px;border-radius:8px;overflow:hidden;background:url({A}/ui/s77.jpg) left top/cover">{hl}</div></div>
<div style="position:absolute;left:1390px;top:270px;width:440px;height:600px;border-radius:22px;background:{NAVY};padding:30px 18px">
  <div style="font:700 18px Montserrat;letter-spacing:.2em;color:#9fd8bb;padding:0 26px 16px">MODUL SPD</div>{st}</div>
<div style="position:absolute;left:90px;top:900px;display:flex;align-items:stretch;box-shadow:0 12px 30px rgba(27,33,64,.18)">
  <div style="width:14px;background:{GREEN}"></div><div style="background:#fff;padding:18px 30px;font:700 30px Montserrat;color:{NAVY}">Taburan premis &amp; tanah milik MCORP di seluruh Melaka</div></div>
{logo()}{foot("Demonstrasi sistem · Laman Utama")}</div>"""


def f_stat():
    return f"""<div class="fr">
<div style="position:absolute;left:0;top:0;width:700px;height:1016px;background:{NAVY}"></div>
<div style="position:absolute;left:680px;top:0;width:40px;height:1016px;background:{GREEN}"></div>
<div style="position:absolute;left:100px;top:300px;width:520px;color:#fff">
  <div style="font:700 22px Montserrat;letter-spacing:.22em;color:#9fd8bb">PRODUKTIVITI</div>
  <div style="font:800 64px/1.1 Montserrat;margin-top:16px">Proses permohonan sewaan</div>
  <div style="font:500 26px/1.5 Montserrat;color:rgba(255,255,255,.75);margin-top:24px">Dari carian data hingga tawaran</div></div>
<div style="position:absolute;left:840px;top:250px;display:flex;align-items:center;gap:56px">
  <div class="card" style="position:relative;width:380px;height:380px;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <div style="font:700 24px Montserrat;letter-spacing:.18em;color:#7B8199">SEBELUM</div><div style="font:800 170px/1 Montserrat;color:#B6BBCC">14</div><div style="font:700 36px Montserrat;color:#7B8199">HARI</div></div>
  <svg viewBox="0 0 80 40" style="width:110px"><path d="M0 20h66M52 6l16 14-16 14" stroke="{RED}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <div class="card" style="position:relative;width:380px;height:380px;display:flex;flex-direction:column;align-items:center;justify-content:center;border-top:12px solid {GREEN}">
    <div style="font:700 24px Montserrat;letter-spacing:.18em;color:{GREEN}">SELEPAS</div><div style="font:800 190px/1 Montserrat;color:{NAVY}">3</div><div style="font:700 36px Montserrat;color:{NAVY}">HARI</div></div>
</div>
<div style="position:absolute;left:1060px;top:700px;padding:22px 44px;border-radius:60px;background:{GREEN};color:#fff;font:800 40px Montserrat">11 hari dijimatkan</div>
{logo()}{foot("Impak SPD · Produktiviti")}</div>"""


def f_dash():
    tiles = [("Kertas A4", "−25.4%", GREEN), ("Dakwat pencetak", "−39.7%", GREEN), ("Proses sewaan", "−79%", NAVY),
             ("Semakan aset alih", "−90%", NAVY), ("Tenaga kerja", "−50%", NAVY), ("Penjimatan / tahun", "RM217,836", RED)]
    th = "".join(f'<div class="card" style="position:relative;padding:28px 30px;border-top:8px solid {c}">'
                 f'<div style="font:700 20px Montserrat;color:#6A7090">{a}</div><div style="font:800 {58 if i < 5 else 50}px/1.15 Montserrat;color:{c};margin-top:12px">{b}</div></div>'
                 for i, (a, b, c) in enumerate(tiles))
    circ = 2 * 3.14159 * 120
    gauge = (f'<svg viewBox="0 0 280 280" style="width:300px;height:300px"><circle cx="140" cy="140" r="120" stroke="#E3E6EE" stroke-width="22" fill="none"/>'
             f'<circle cx="140" cy="140" r="120" stroke="{GREEN}" stroke-width="22" fill="none" stroke-linecap="round" stroke-dasharray="{circ * .82:.0f} {circ:.0f}" transform="rotate(-90 140 140)"/>'
             f'<text x="140" y="160" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="90" fill="{NAVY}">82</text></svg>')
    return f"""<div class="fr" style="background:{GREY}">
<div style="position:absolute;left:0;right:0;top:0;height:250px;background:linear-gradient(100deg,{NAVY} 0 60%,{GREEN})"></div>
<div style="position:absolute;left:100px;top:70px;color:#fff">
  <div style="display:inline-block;font:800 20px Montserrat;letter-spacing:.2em;background:{RED};padding:8px 16px;border-radius:6px">AKAN DATANG</div>
  <div style="font:800 76px/1 Montserrat;margin-top:18px">SPD 2.0 + Green Dashboard</div></div>
<div class="card" style="left:100px;top:310px;width:440px;height:600px;display:flex;flex-direction:column;align-items:center;justify-content:center">
  <div style="font:700 20px Montserrat;letter-spacing:.16em;color:#6A7090;margin-bottom:10px">GREEN INDEX</div>{gauge}
  <div style="margin-top:16px;padding:10px 22px;border-radius:30px;background:{LG};color:{GREEN};font:700 22px Montserrat">Advanced Green Performance</div></div>
<div style="position:absolute;left:590px;top:310px;width:1230px;display:grid;grid-template-columns:repeat(3,1fr);gap:26px">{th}</div>
{logo()}{foot("Akan datang · SPD 2.0")}</div>"""


FRAMES = [("01", "Tajuk", f_title), ("02", "Penyataan masalah", f_problem), ("03", "Demo sistem", f_demo), ("04", "Statistik", f_stat), ("05", "SPD 2.0 + Green Dashboard", f_dash)]

JS = r"""
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--proxy-server=' + (process.env.HTTPS_PROXY || 'direct://'), '--ignore-certificate-errors'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + process.argv[2] + '/styleboard_d.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  for (const id of process.argv.slice(3)) await p.locator('#' + id).screenshot({ path: process.argv[2] + '/f_' + id + '.jpg', type: 'jpeg', quality: 90 });
  await b.close();
})();
"""

if __name__ == "__main__":
    html = ['<!doctype html><html><head><meta charset="utf-8">',
            '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=block" rel="stylesheet">',
            f'<style>{CSS}</style></head><body>'] + [f'<div id="D{n}">{fn()}</div>' for n, _, fn in FRAMES] + ["</body></html>"]
    (OUT / "styleboard_d.html").write_text("\n".join(html), encoding="utf-8")
    js = OUT / "_render.js"
    js.write_text(JS)
    subprocess.run(["node", str(js), str(OUT)] + [f"D{n}" for n, _, _ in FRAMES], check=True, cwd=str(ROOT))
    js.unlink()
    from PIL import Image, ImageDraw, ImageFont
    ims = [Image.open(OUT / f"f_D{n}.jpg") for n, _, _ in FRAMES]
    W = 2400
    board = Image.new("RGB", (W, 180 + 1350 + 40 + 2 * (608 + 70)), "#ffffff")
    d = ImageDraw.Draw(board)
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    d.text((60, 45), "D · KORPORAT MCORP", fill=NAVY, font=f1)
    d.text((60, 118), "Putih bersih · biru tua & merah MCORP · hijau untuk inisiatif hijau · kad maklumat · lower-third", fill=GREEN, font=f2)
    board.paste(ims[0].resize((W, 1350)), (0, 180))
    y = 180 + 1350 + 40
    for i, (im, (n, label, _)) in enumerate(zip(ims[1:], FRAMES[1:])):
        x, yy = (i % 2) * (W // 2), y + (i // 2) * (608 + 70)
        d.text((x + 30, yy + 8), f"{n}  {label}", fill=NAVY, font=f2)
        board.paste(im.resize((W // 2 - 20, 608 - 10)), (x + 10, yy + 60))
    board.save(OUT / "D_korporat.jpg", quality=88)
    print("ok")
