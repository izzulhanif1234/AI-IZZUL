"""SPD GREEN style boards H, I, J: H monochrome luxe, I architectural / land-plan, J Swiss modern colour blocks.
Each: title, problem, demo, stat -> edits/spd-green/styleboard/{H,I,J}_*.jpg"""
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from spd_styleboard_efg import IC, PROB, ico, logo, screen, spot, A, OUT, ROOT, NAVY, RED, GREEN, MINT  # noqa: E402

EMER, BRASS, SAND = "#0F8A5F", "#C8964E", "#E9E1D2"


# ============================================================ H: monochrome luxe
def h_title():
    return f"""<div class="fr" style="background:#000;font-family:'Inter Tight';color:#fff">
<div style="position:absolute;inset:0;background:url({A}/img/s01_freeze.jpg) 60% center/cover;filter:grayscale(1) contrast(1.15) brightness(.55)"></div>
<div style="position:absolute;inset:0;background:linear-gradient(90deg,#000 0%,rgba(0,0,0,.7) 40%,rgba(0,0,0,.1) 80%)"></div>
<div style="position:absolute;left:130px;top:300px;width:900px">
  <div style="font:400 20px 'Inter Tight';letter-spacing:.6em;color:rgba(255,255,255,.65)">PERBADANAN MELAKA</div>
  <div style="font:300 46px/1.25 'Inter Tight';margin-top:46px;letter-spacing:.02em">Sistem Pengurusan Data Bersepadu</div>
  <div style="font:800 210px/0.9 'Inter Tight';letter-spacing:-.05em;margin-top:10px">SPD<span style="color:{EMER}">.</span></div>
  <div style="display:flex;align-items:center;gap:22px;margin-top:44px"><i style="width:80px;height:1px;background:{EMER};display:block"></i>
  <span style="font:400 22px 'Inter Tight';letter-spacing:.28em;color:rgba(255,255,255,.8)">INOVASI DIGITAL · HIJAU · LESTARI</span></div>
</div>{logo(True)}</div>"""


def h_problem():
    cells = "".join(f'<div style="position:absolute;left:{130 + (i % 3) * 560}px;top:{380 + (i // 3) * 270}px;width:500px;border-top:1px solid rgba(255,255,255,.25);padding-top:26px">'
                    f'<div style="font:300 22px \'Inter Tight\';letter-spacing:.3em;color:{EMER}">0{i + 1}</div>'
                    f'<div style="font:600 36px/1.2 \'Inter Tight\';margin-top:14px">{t}</div></div>' for i, (k, t) in enumerate(PROB))
    return f"""<div class="fr" style="background:#0a0a0a;font-family:'Inter Tight';color:#fff">
<div style="position:absolute;right:0;top:0;width:640px;height:1080px;background:url({A}/sb/lk1-22.jpg) center/cover;filter:grayscale(1) contrast(1.1) brightness(.45)"></div>
<div style="position:absolute;right:0;top:0;width:640px;height:1080px;background:linear-gradient(90deg,#0a0a0a,rgba(10,10,10,0) 40%)"></div>
<div style="position:absolute;left:130px;top:130px"><div style="font:400 20px 'Inter Tight';letter-spacing:.6em;color:rgba(255,255,255,.6)">SEBELUM SPD</div>
<div style="font:800 96px/1 'Inter Tight';letter-spacing:-.03em;margin-top:24px">Enam cabaran<span style="color:{EMER}">.</span></div></div>{cells}{logo(True)}</div>"""


def h_demo():
    return f"""<div class="fr" style="background:#0a0a0a;font-family:'Inter Tight';color:#fff">
<div style="position:absolute;left:640px;top:140px;filter:grayscale(.15)">{screen(f"{A}/ui/s77.jpg", 1180, spot(1180, EMER), True)}</div>
<div style="position:absolute;left:130px;top:340px;width:440px">
  <div style="font:400 20px 'Inter Tight';letter-spacing:.6em;color:rgba(255,255,255,.6)">LAMAN UTAMA</div>
  <div style="font:800 66px/1.02 'Inter Tight';letter-spacing:-.03em;margin-top:24px">Semua aset.<br>Satu paparan<span style="color:{EMER}">.</span></div>
  <div style="font:300 24px/1.6 'Inter Tight';color:rgba(255,255,255,.7);margin-top:24px">Taburan premis dan tanah milik MCORP di seluruh Melaka.</div></div>
{logo(True)}</div>"""


def h_stat():
    return f"""<div class="fr" style="background:#0a0a0a;font-family:'Inter Tight';color:#fff">
<div style="position:absolute;left:0;top:0;width:760px;height:1080px;background:url({A}/sb/lk3-22.jpg) center/cover;filter:grayscale(1) contrast(1.1) brightness(.55)"></div>
<div style="position:absolute;left:900px;top:220px">
  <div style="font:400 20px 'Inter Tight';letter-spacing:.6em;color:rgba(255,255,255,.6)">PROSES SEWAAN</div>
  <div style="display:flex;align-items:flex-end;gap:30px;margin-top:40px">
    <div style="font:800 380px/0.8 'Inter Tight';letter-spacing:-.06em">3</div>
    <div style="font:300 64px 'Inter Tight';margin-bottom:20px">hari</div></div>
  <div style="font:300 34px 'Inter Tight';color:rgba(255,255,255,.45);margin-top:40px;text-decoration:line-through;text-decoration-color:{EMER}">sebelum ini 14 hari</div>
  <div style="width:820px;height:1px;background:rgba(255,255,255,.25);margin:46px 0 30px"></div>
  <div style="font:600 34px 'Inter Tight'"><span style="color:{EMER}">11 hari</span> dijimatkan bagi setiap permohonan</div></div>
{logo(True)}</div>"""


# ============================================================ I: architectural / land plan
I_BG = ("background:#0b1838;background-image:linear-gradient(rgba(140,170,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(140,170,255,.07) 1px,transparent 1px),"
        "linear-gradient(rgba(140,170,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(140,170,255,.035) 1px,transparent 1px);"
        "background-size:160px 160px,160px 160px,32px 32px,32px 32px")
LOTS = ('<svg viewBox="0 0 900 800" style="position:absolute;right:40px;top:120px;width:900px;height:800px" fill="none" stroke="{c}" stroke-width="1.6">'
        '<path d="M60 120 L320 60 L420 260 L180 360Z"/><path d="M420 260 L640 180 L760 380 L520 470Z"/><path d="M180 360 L420 260 L520 470 L300 560Z"/>'
        '<path d="M520 470 L760 380 L840 600 L600 680Z"/><path d="M300 560 L520 470 L600 680 L380 760Z"/><path d="M320 60 L560 20 L640 180 L420 260Z"/>'
        '<path d="M300 560 L520 470 L600 680 L380 760Z" fill="{f}" stroke="{a}" stroke-width="3"/>'
        '<circle cx="450" cy="610" r="10" fill="{a}" stroke="none"/><path d="M450 610 L640 740" stroke="{a}" stroke-dasharray="6 8"/>'
        '<text x="650" y="752" fill="{a}" stroke="none" font-family="Inter Tight" font-size="22" font-weight="600" letter-spacing="2">LOT 10 · PT 7257</text></svg>')


def i_title():
    return f"""<div class="fr" style="{I_BG};font-family:'Inter Tight';color:#fff">
{LOTS.format(c="rgba(200,215,255,.35)", f="rgba(200,150,78,.18)", a=BRASS)}
<div style="position:absolute;left:120px;top:250px;width:900px">
  <div style="font:600 20px 'Inter Tight';letter-spacing:.45em;color:{BRASS}">PERBADANAN MELAKA</div>
  <div style="font:800 200px/0.92 'Inter Tight';letter-spacing:-.04em;margin-top:30px">SPD</div>
  <div style="font:400 50px/1.15 'Inter Tight';margin-top:20px">Sistem Pengurusan<br>Data Bersepadu</div>
  <div style="display:flex;gap:26px;margin-top:46px;font:600 18px 'JetBrains Mono',monospace;color:rgba(200,215,255,.7);letter-spacing:.12em">
    <span>TANAH</span><span>·</span><span>BANGUNAN</span><span>·</span><span>SEWAAN</span><span>·</span><span>HAK MILIK</span></div>
</div>{logo(True)}</div>"""


def i_problem():
    cells = "".join(f'<div style="position:absolute;left:{120 + (i % 3) * 570}px;top:{340 + (i // 3) * 300}px;width:530px;height:250px;border:1.5px solid rgba(200,215,255,.3);'
                    f'padding:34px;background:rgba(11,24,56,.6)"><div style="position:absolute;left:-1px;top:-1px;width:26px;height:26px;border-left:3px solid {BRASS};border-top:3px solid {BRASS}"></div>'
                    f'<div style="display:flex;gap:26px;align-items:center">{ico(k, BRASS, 64, 2.2)}<div style="font:600 32px/1.25 \'Inter Tight\'">{t}</div></div>'
                    f'<div style="position:absolute;right:30px;bottom:24px;font:600 18px \'JetBrains Mono\',monospace;color:rgba(200,215,255,.55)">C-0{i + 1}</div></div>'
                    for i, (k, t) in enumerate(PROB))
    return f"""<div class="fr" style="{I_BG};font-family:'Inter Tight';color:#fff">
<div style="position:absolute;left:120px;top:120px"><div style="font:600 20px 'Inter Tight';letter-spacing:.45em;color:{BRASS}">SEBELUM SPD</div>
<div style="font:800 76px/1.05 'Inter Tight';margin-top:16px">Enam cabaran utama</div></div>{cells}{logo(True)}</div>"""


def i_demo():
    return f"""<div class="fr" style="{I_BG};font-family:'Inter Tight';color:#fff">
<div style="position:absolute;left:590px;top:170px">{screen(f"{A}/ui/s77.jpg", 1220, spot(1220, BRASS), True)}</div>
<svg style="position:absolute;left:470px;top:400px;width:200px;height:120px" viewBox="0 0 200 120"><path d="M0 100 H80 L150 20" stroke="{BRASS}" stroke-width="2" fill="none"/><circle cx="150" cy="20" r="6" fill="{BRASS}"/></svg>
<div style="position:absolute;left:120px;top:440px;width:420px">
  <div style="font:600 20px 'Inter Tight';letter-spacing:.45em;color:{BRASS}">LAMAN UTAMA</div>
  <div style="font:800 54px/1.08 'Inter Tight';margin-top:18px">Taburan premis &amp; tanah</div>
  <div style="font:400 24px/1.55 'Inter Tight';color:rgba(200,215,255,.8);margin-top:18px">Setiap lot milik MCORP dipetakan di seluruh Melaka.</div></div>
{logo(True)}</div>"""


def i_stat():
    return f"""<div class="fr" style="{I_BG};font-family:'Inter Tight';color:#fff">
<div style="position:absolute;left:120px;top:150px"><div style="font:600 20px 'Inter Tight';letter-spacing:.45em;color:{BRASS}">PRODUKTIVITI · PROSES SEWAAN</div></div>
<svg viewBox="0 0 1700 300" style="position:absolute;left:120px;top:560px;width:1700px;height:300px">
  <line x1="0" y1="150" x2="1680" y2="150" stroke="rgba(200,215,255,.35)" stroke-width="2"/>
  {''.join(f'<line x1="{i * 120}" y1="135" x2="{i * 120}" y2="165" stroke="rgba(200,215,255,.5)" stroke-width="2"/><text x="{i * 120}" y="205" text-anchor="middle" font-family="JetBrains Mono" font-size="20" fill="rgba(200,215,255,.6)">H{i}</text>' for i in range(15))}
  <rect x="0" y="120" width="1680" height="60" fill="rgba(200,215,255,.08)"/>
  <rect x="0" y="110" width="360" height="80" fill="{BRASS}"/>
  <text x="0" y="90" font-family="Inter Tight" font-weight="600" font-size="26" fill="rgba(200,215,255,.7)">Sebelum: 14 hari</text>
  <text x="380" y="165" font-family="Inter Tight" font-weight="800" font-size="34" fill="{BRASS}">Selepas: 3 hari</text></svg>
<div style="position:absolute;left:120px;top:240px;display:flex;align-items:flex-end;gap:30px"><div style="font:800 300px/0.85 'Inter Tight';letter-spacing:-.05em">11</div>
<div style="font:400 54px/1.15 'Inter Tight';margin-bottom:24px">hari<br><span style="color:{BRASS}">dijimatkan</span></div></div>
{logo(True)}</div>"""


# ============================================================ J: Swiss modern colour blocks
def j_title():
    return f"""<div class="fr" style="background:{SAND};font-family:Archivo;color:#111">
<div style="position:absolute;left:0;top:0;width:1080px;height:1080px;background:{EMER}"></div>
<div style="position:absolute;left:1080px;top:0;width:840px;height:620px;background:url({A}/img/s01_freeze.jpg) 45% center/cover"></div>
<div style="position:absolute;left:1080px;top:620px;width:420px;height:460px;background:{NAVY}"></div>
<div style="position:absolute;left:1500px;top:620px;width:420px;height:460px;background:{SAND};display:flex;align-items:flex-end;padding:40px">
  <div style="font:600 22px/1.4 Archivo;color:#333">Inovasi digital ke arah pengurusan hijau dan lestari</div></div>
<div style="position:absolute;left:90px;top:90px;font:600 22px Archivo;letter-spacing:.2em;color:#fff">PERBADANAN MELAKA</div>
<div style="position:absolute;left:80px;top:420px;font:900 330px/0.82 Archivo;letter-spacing:-.06em;color:#fff">SPD</div>
<div style="position:absolute;left:90px;top:760px;font:600 52px/1.1 Archivo;color:#fff">Sistem Pengurusan<br>Data Bersepadu</div>
<div style="position:absolute;left:1120px;top:660px;font:900 120px/1 Archivo;color:#fff">01</div>
{logo(True)}</div>"""


def j_problem():
    cols = [EMER, NAVY, "#fff", "#fff", EMER, NAVY]
    cells = "".join(f'<div style="position:absolute;left:{(i % 3) * 640}px;top:{300 + (i // 3) * 390}px;width:640px;height:390px;background:{c};padding:48px;'
                    f'color:{"#fff" if c != "#fff" else "#111"};border-right:2px solid {SAND};border-bottom:2px solid {SAND}">'
                    f'<div style="font:900 90px/1 Archivo;opacity:.9">0{i + 1}</div><div style="font:700 40px/1.15 Archivo;margin-top:90px;max-width:480px">{t}</div></div>'
                    for i, ((k, t), c) in enumerate(zip(PROB, cols)))
    return f"""<div class="fr" style="background:{SAND};font-family:Archivo;color:#111">
<div style="position:absolute;left:80px;top:80px;font:900 120px/1 Archivo;letter-spacing:-.04em">Sebelum SPD.</div>
<div style="position:absolute;left:1100px;top:110px;width:600px;font:600 28px/1.4 Archivo;color:#333">Enam cabaran yang mencetuskan pembangunan sistem.</div>
{cells}{logo()}</div>"""


def j_demo():
    return f"""<div class="fr" style="background:{SAND};font-family:Archivo;color:#111">
<div style="position:absolute;left:0;top:0;width:560px;height:1080px;background:{NAVY};color:#fff;padding:90px 70px">
  <div style="font:900 140px/1 Archivo">02</div><div style="font:600 22px Archivo;letter-spacing:.2em;margin-top:40px;color:{MINT}">LAMAN UTAMA</div>
  <div style="font:800 54px/1.08 Archivo;margin-top:20px">Semua aset dalam satu paparan.</div>
  <div style="font:500 24px/1.5 Archivo;margin-top:24px;color:rgba(255,255,255,.75)">Taburan premis dan tanah milik MCORP di seluruh Melaka.</div></div>
<div style="position:absolute;left:640px;top:180px">{screen(f"{A}/ui/s77.jpg", 1180, spot(1180, EMER))}</div>
<div style="position:absolute;left:640px;top:820px;width:1196px;height:120px;background:{EMER};display:flex;align-items:center;padding:0 40px;color:#fff;font:700 34px Archivo">spd.pknm.gov.my</div>
{logo()}</div>"""


def j_stat():
    return f"""<div class="fr" style="background:{SAND};font-family:Archivo;color:#111">
<div style="position:absolute;left:0;top:0;width:960px;height:1080px;background:#fff"></div>
<div style="position:absolute;left:960px;top:0;width:960px;height:1080px;background:{EMER}"></div>
<div style="position:absolute;left:90px;top:120px;font:600 24px Archivo;letter-spacing:.2em;color:#888">SEBELUM</div>
<div style="position:absolute;left:70px;top:230px;font:900 520px/0.8 Archivo;letter-spacing:-.06em;color:#d8d2c4">14</div>
<div style="position:absolute;left:90px;top:760px;font:700 60px Archivo;color:#999">hari</div>
<div style="position:absolute;left:1050px;top:120px;font:600 24px Archivo;letter-spacing:.2em;color:#fff">SELEPAS SPD</div>
<div style="position:absolute;left:1030px;top:230px;font:900 520px/0.8 Archivo;letter-spacing:-.06em;color:#fff">3</div>
<div style="position:absolute;left:1050px;top:760px;font:700 60px Archivo;color:#fff">hari</div>
<div style="position:absolute;left:1500px;top:820px;width:420px;height:260px;background:{NAVY};color:#fff;padding:40px">
  <div style="font:900 80px/1 Archivo">11</div><div style="font:600 26px Archivo;margin-top:10px">hari dijimatkan</div></div>
{logo(True)}</div>"""


BOARDS = {
    "H": ("H · MONOKROM MEWAH", "Foto hitam-putih · tipografi putih tajam · satu aksen zamrud", "H_monokrom-mewah", [h_title, h_problem, h_demo, h_stat], "#000000", "#ffffff", EMER),
    "I": ("I · ARKITEKTURAL / PELAN TANAH", "Biru tua · grid pelan · garisan lot · aksen tembaga", "I_pelan-tanah", [i_title, i_problem, i_demo, i_stat], "#0b1838", "#ffffff", BRASS),
    "J": ("J · SWISS MODEN", "Blok warna padu · grid tegas · tipografi besar", "J_swiss-moden", [j_title, j_problem, j_demo, j_stat], SAND, "#111111", EMER),
}
LABELS = ["Tajuk", "Penyataan masalah", "Demo sistem", "Statistik"]

JS = r"""
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--proxy-server=' + (process.env.HTTPS_PROXY || 'direct://'), '--ignore-certificate-errors'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + process.argv[2] + '/styleboard_hij.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  for (const id of process.argv.slice(3)) await p.locator('#' + id).screenshot({ path: process.argv[2] + '/f_' + id + '.jpg', type: 'jpeg', quality: 90 });
  await b.close();
})();
"""

if __name__ == "__main__":
    css = "*{margin:0;padding:0;box-sizing:border-box}body{background:#ccc}.fr{position:relative;width:1920px;height:1080px;overflow:hidden}"
    html = ['<!doctype html><html><head><meta charset="utf-8">',
            '<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;600;800;900&family=Archivo:wght@500;600;700;800;900&family=JetBrains+Mono:wght@600&family=Montserrat:wght@600;700&display=block" rel="stylesheet">',
            f'<style>{css}</style></head><body>']
    ids = []
    for key, (_, _, _, fns, _, _, _) in BOARDS.items():
        for i, fn in enumerate(fns):
            html.append(f'<div id="{key}{i + 1}">{fn()}</div>')
            ids.append(f"{key}{i + 1}")
    html.append("</body></html>")
    (OUT / "styleboard_hij.html").write_text("\n".join(html), encoding="utf-8")
    js = OUT / "_render.js"
    js.write_text(JS)
    subprocess.run(["node", str(js), str(OUT)] + ids, check=True, cwd=str(ROOT))
    js.unlink()
    from PIL import Image, ImageDraw, ImageFont
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    for key, (name, sub, fname, fns, bg, fg, acc) in BOARDS.items():
        ims = [Image.open(OUT / f"f_{key}{i + 1}.jpg") for i in range(len(fns))]
        W = 2400
        w3 = (W - 40) // 3
        board = Image.new("RGB", (W, 180 + 1350 + 40 + 50 + round(w3 * 9 / 16) + 30), bg)
        d = ImageDraw.Draw(board)
        d.text((60, 45), name, fill=fg, font=f1)
        d.text((60, 118), sub, fill=acc, font=f2)
        board.paste(ims[0].resize((W, 1350)), (0, 180))
        y = 180 + 1350 + 40
        for i, im in enumerate(ims[1:]):
            x = 10 + i * (w3 + 10)
            d.text((x + 10, y + 4), f"0{i + 2}  {LABELS[i + 1]}", fill=fg, font=f2)
            board.paste(im.resize((w3, round(w3 * 9 / 16))), (x, y + 50))
        board.save(OUT / f"{fname}.jpg", quality=88)
    print("ok")
