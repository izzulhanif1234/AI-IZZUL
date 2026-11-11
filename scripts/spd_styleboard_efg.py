"""SPD GREEN style boards E, F, G (corporate variants): E glass light, F bold gradient, G editorial/annual report.
Each: title, problem, demo, stat frames -> edits/spd-green/styleboard/{E,F,G}_*.jpg"""
import pathlib
import subprocess

ROOT = pathlib.Path("/home/user/AI-IZZUL")
OUT = ROOT / "edits/spd-green/styleboard"
A = "../hf/assets"
NAVY, RED, GREEN, MINT = "#2C3280", "#E31E26", "#1E8E5A", "#3FD08E"

IC = {
    "paper": '<rect x="14" y="10" width="30" height="40" rx="3"/><path d="M22 22h14M22 30h14M22 38h8"/><path d="M20 54h30V18"/>',
    "cabinet": '<rect x="14" y="8" width="36" height="48" rx="4"/><path d="M14 24h36M14 40h36M28 16h8M28 32h8M28 48h8"/>',
    "dup": '<rect x="10" y="14" width="26" height="34" rx="3"/><rect x="28" y="18" width="26" height="34" rx="3"/>',
    "clock": '<circle cx="32" cy="32" r="22"/><path d="M32 20v13l9 6"/>',
    "lost": '<rect x="12" y="12" width="28" height="38" rx="3"/><path d="M46 20c3-6 12-3 10 3-1 4-5 4-5 8M51 38v1"/>',
    "cost": '<circle cx="32" cy="32" r="22"/><path d="M26 26c0-5 13-5 13 0s-13 5-13 10 13 5 13 0M32 17v4M32 43v4"/>',
}
PROB = [("paper", "Penggunaan kertas tinggi"), ("cabinet", "Ruang simpanan fizikal besar"), ("dup", "Pertindihan data"),
        ("clock", "Carian maklumat lambat"), ("lost", "Risiko kehilangan dokumen"), ("cost", "Kos operasi tinggi")]


def ico(k, c, w=56, sw=3):
    return (f'<svg viewBox="0 0 64 64" style="width:{w}px;height:{w}px" fill="none" stroke="{c}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{IC[k]}</svg>')


def logo(dark=False):
    f = "drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 1.3px #fff) drop-shadow(0 6px 10px rgba(0,0,0,.35))" if dark else "drop-shadow(0 6px 10px rgba(0,0,0,.12))"
    return f'<img src="{A}/img/logo-pptx.png" style="position:absolute;right:56px;top:34px;width:132px;transform:perspective(600px) rotateY(-14deg);filter:{f};z-index:9">'


def screen(img, w, extra="", dark=False):
    h = round(w * 912 / 1920)
    return (f'<div style="padding:14px;border-radius:22px;background:{"#1f2330" if not dark else "linear-gradient(160deg,#30353b,#121417)"};'
            f'box-shadow:0 40px 90px rgba(10,20,50,.30)"><div style="position:relative;width:{w}px;height:{h}px;border-radius:9px;overflow:hidden;'
            f'background:url({img}) left top/cover">{extra}</div></div>')


def spot(w, color):
    k = w / 1920
    x0, y0, x1, y1 = 44 * k, 260 * k, 1856 * k, 766 * k
    return (f'<div style="position:absolute;left:{x0 - 6}px;top:{y0 - 6}px;width:{x1 - x0 + 12}px;height:{y1 - y0 + 12}px;border:4px solid {color};'
            f'border-radius:12px;box-shadow:0 0 0 9999px rgba(15,25,50,.42),0 0 40px {color}"></div>')


# ============================================================ E: glass light
E_BG = ("background:radial-gradient(60% 70% at 15% 20%,#d9f5e8 0%,transparent 60%),radial-gradient(55% 60% at 85% 30%,#dfe6ff 0%,transparent 60%),"
        "radial-gradient(70% 60% at 60% 100%,#e9fbf2 0%,transparent 60%),#f7f9fc")
E_GLASS = ("background:linear-gradient(140deg,rgba(255,255,255,.82),rgba(255,255,255,.55));border:1.5px solid rgba(255,255,255,.95);"
           "box-shadow:0 30px 70px rgba(44,50,128,.12),inset 0 1px 0 #fff;backdrop-filter:blur(20px);border-radius:28px")
E_BLOBS = ('<div style="position:absolute;left:-160px;top:-180px;width:640px;height:640px;border-radius:50%;background:radial-gradient(circle,#7fe0b4,transparent 65%);opacity:.55;filter:blur(20px)"></div>'
           '<div style="position:absolute;right:-200px;bottom:-240px;width:760px;height:760px;border-radius:50%;background:radial-gradient(circle,#9aa8ff,transparent 65%);opacity:.45;filter:blur(20px)"></div>')


def e_title():
    return f"""<div class="fr" style="{E_BG};font-family:'Plus Jakarta Sans'">{E_BLOBS}
<div style="position:absolute;left:120px;top:190px;width:860px">
  <div style="display:inline-flex;align-items:center;gap:12px;padding:10px 20px;border-radius:40px;{E_GLASS};font:700 20px 'Plus Jakarta Sans';letter-spacing:.14em;color:{NAVY}"><i style="width:10px;height:10px;border-radius:50%;background:{GREEN};display:block"></i>PERBADANAN MELAKA</div>
  <div style="font:800 190px/1 'Plus Jakarta Sans';letter-spacing:-.04em;margin-top:30px;background:linear-gradient(100deg,{NAVY},{GREEN});-webkit-background-clip:text;color:transparent">SPD</div>
  <div style="font:700 54px/1.15 'Plus Jakarta Sans';color:#1B2140;margin-top:10px">Sistem Pengurusan<br>Data Bersepadu</div>
  <div style="font:500 30px/1.5 'Plus Jakarta Sans';color:#566080;margin-top:26px">Inovasi digital ke arah pengurusan hijau dan lestari</div>
</div>
<div style="position:absolute;left:1060px;top:200px;width:740px;height:700px;{E_GLASS};padding:24px">
  <div style="width:100%;height:100%;border-radius:18px;background:url({A}/img/s01_freeze.jpg) 40% center/cover"></div></div>
<div style="position:absolute;left:990px;top:760px;padding:22px 28px;{E_GLASS};display:flex;gap:18px;align-items:center">
  <div style="width:56px;height:56px;border-radius:16px;background:linear-gradient(140deg,{MINT},{GREEN});display:flex;align-items:center;justify-content:center">{ico("paper", "#fff", 34)}</div>
  <div><div style="font:800 34px 'Plus Jakarta Sans';color:{NAVY}">−25.4%</div><div style="font:600 18px 'Plus Jakarta Sans';color:#566080">permohonan kertas A4</div></div></div>
{logo()}</div>"""


def e_problem():
    cards = "".join(f'<div style="position:absolute;left:{120 + (i % 3) * 570}px;top:{330 + (i // 3) * 300}px;width:530px;height:250px;{E_GLASS};padding:38px">'
                    f'<div style="width:72px;height:72px;border-radius:20px;background:linear-gradient(140deg,{"#6f7cff" if i % 2 else MINT},{NAVY if i % 2 else GREEN});'
                    f'display:flex;align-items:center;justify-content:center;box-shadow:0 12px 24px rgba(44,50,128,.2)">{ico(k, "#fff", 40)}</div>'
                    f'<div style="font:700 32px/1.25 \'Plus Jakarta Sans\';color:#1B2140;margin-top:24px">{t}</div></div>' for i, (k, t) in enumerate(PROB))
    return f"""<div class="fr" style="{E_BG};font-family:'Plus Jakarta Sans'">{E_BLOBS}
<div style="position:absolute;left:120px;top:120px"><div style="font:700 22px 'Plus Jakarta Sans';letter-spacing:.2em;color:{GREEN}">SEBELUM SPD</div>
<div style="font:800 70px/1.1 'Plus Jakarta Sans';color:{NAVY};margin-top:10px">Enam cabaran utama</div></div>{cards}{logo()}</div>"""


def e_demo():
    return f"""<div class="fr" style="{E_BG};font-family:'Plus Jakarta Sans'">{E_BLOBS}
<div style="position:absolute;left:560px;top:170px">{screen(f"{A}/ui/s77.jpg", 1240, spot(1240, MINT))}</div>
<div style="position:absolute;left:110px;top:300px;width:520px;{E_GLASS};padding:40px">
  <div style="font:700 20px 'Plus Jakarta Sans';letter-spacing:.18em;color:{GREEN}">LAMAN UTAMA</div>
  <div style="font:800 46px/1.15 'Plus Jakarta Sans';color:{NAVY};margin-top:14px">Taburan premis &amp; tanah milik MCORP</div>
  <div style="font:500 24px/1.5 'Plus Jakarta Sans';color:#566080;margin-top:16px">Seluruh negeri Melaka dalam satu paparan bersepadu.</div></div>
{logo()}</div>"""


def e_stat():
    return f"""<div class="fr" style="{E_BG};font-family:'Plus Jakarta Sans'">{E_BLOBS}
<div style="position:absolute;left:0;right:0;top:150px;text-align:center;font:700 22px 'Plus Jakarta Sans';letter-spacing:.2em;color:{GREEN}">PROSES PERMOHONAN SEWAAN</div>
<div style="position:absolute;left:260px;top:260px;width:600px;height:520px;{E_GLASS};display:flex;flex-direction:column;align-items:center;justify-content:center">
  <div style="font:600 26px 'Plus Jakarta Sans';color:#566080">Sebelum</div><div style="font:800 230px/1 'Plus Jakarta Sans';color:#b9c0d8">14</div><div style="font:700 40px 'Plus Jakarta Sans';color:#8a93b0">hari</div></div>
<div style="position:absolute;left:1060px;top:230px;width:640px;height:580px;{E_GLASS};display:flex;flex-direction:column;align-items:center;justify-content:center">
  <div style="font:600 26px 'Plus Jakarta Sans';color:{GREEN}">Selepas SPD</div><div style="font:800 280px/1 'Plus Jakarta Sans';background:linear-gradient(140deg,{NAVY},{GREEN});-webkit-background-clip:text;color:transparent">3</div><div style="font:700 44px 'Plus Jakarta Sans';color:{NAVY}">hari</div></div>
<div style="position:absolute;left:0;right:0;top:860px;display:flex;justify-content:center"><div style="padding:18px 40px;border-radius:50px;background:linear-gradient(100deg,{GREEN},{MINT});color:#fff;font:800 36px 'Plus Jakarta Sans';box-shadow:0 18px 40px rgba(30,142,90,.35)">11 hari dijimatkan</div></div>
{logo()}</div>"""


# ============================================================ F: bold gradient
F_BG = f"background:linear-gradient(125deg,#141a52 0%,{NAVY} 35%,#14605a 75%,{GREEN} 100%)"
F_DECO = ('<div style="position:absolute;right:-300px;top:-300px;width:900px;height:900px;border-radius:50%;border:2px solid rgba(255,255,255,.12)"></div>'
          '<div style="position:absolute;right:-180px;top:-180px;width:660px;height:660px;border-radius:50%;border:2px solid rgba(255,255,255,.10)"></div>'
          '<div style="position:absolute;left:-200px;bottom:-260px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(63,208,142,.35),transparent 65%)"></div>'
          '<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.10) 1.5px,transparent 1.5px);background-size:34px 34px;'
          '-webkit-mask-image:linear-gradient(90deg,transparent 40%,#000)"></div>')


def f_title():
    return f"""<div class="fr" style="{F_BG};font-family:Montserrat;color:#fff">{F_DECO}
<div style="position:absolute;left:1000px;top:110px;width:820px;height:860px;border-radius:430px 430px 40px 40px;overflow:hidden;box-shadow:0 50px 120px rgba(0,0,0,.4);border:8px solid rgba(255,255,255,.15)">
  <div style="width:100%;height:100%;background:url({A}/img/s01_freeze.jpg) 42% center/cover"></div></div>
<div style="position:absolute;left:940px;top:700px;width:150px;height:150px;border-radius:50%;background:linear-gradient(140deg,{MINT},{GREEN});display:flex;align-items:center;justify-content:center;box-shadow:0 20px 40px rgba(0,0,0,.3)">
  <svg viewBox="0 0 64 64" style="width:80px"><path d="M32 58C14 46 12 22 32 6c20 16 18 40 0 52z" fill="#fff"/><path d="M32 54V16M32 38l-9-8M32 28l9-8" stroke="{GREEN}" stroke-width="3" fill="none"/></svg></div>
<div style="position:absolute;left:120px;top:250px;width:820px">
  <div style="font:700 22px Montserrat;letter-spacing:.3em;color:{MINT}">PERBADANAN MELAKA</div>
  <div style="font:900 200px/0.95 Montserrat;letter-spacing:-.03em;margin-top:24px">SPD</div>
  <div style="font:700 50px/1.15 Montserrat;margin-top:18px">Sistem Pengurusan<br>Data Bersepadu</div>
  <div style="display:flex;align-items:center;gap:18px;margin-top:40px"><i style="width:70px;height:6px;border-radius:3px;background:{RED};display:block"></i>
  <span style="font:500 28px Montserrat;color:rgba(255,255,255,.85)">Inovasi digital ke arah pengurusan hijau dan lestari</span></div>
</div>{logo(True)}</div>"""


def f_problem():
    cards = "".join(f'<div style="position:absolute;left:{120 + (i % 3) * 570}px;top:{330 + (i // 3) * 300}px;width:530px;height:250px;border-radius:26px;'
                    f'background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.18);padding:36px;display:flex;gap:28px;align-items:center">'
                    f'<div style="width:96px;height:96px;flex:none;border-radius:50%;background:{"#fff" if i % 2 == 0 else MINT};display:flex;align-items:center;justify-content:center">{ico(k, NAVY, 48)}</div>'
                    f'<div><div style="font:900 28px Montserrat;color:{MINT}">0{i + 1}</div><div style="font:700 31px/1.25 Montserrat;margin-top:4px">{t}</div></div></div>'
                    for i, (k, t) in enumerate(PROB))
    return f"""<div class="fr" style="{F_BG};font-family:Montserrat;color:#fff">{F_DECO}
<div style="position:absolute;left:120px;top:120px"><div style="font:700 22px Montserrat;letter-spacing:.3em;color:{MINT}">SEBELUM SPD</div>
<div style="font:900 74px/1.05 Montserrat;margin-top:10px">Enam cabaran utama</div></div>{cards}{logo(True)}</div>"""


def f_demo():
    return f"""<div class="fr" style="{F_BG};font-family:Montserrat;color:#fff">{F_DECO}
<div style="position:absolute;left:600px;top:150px;transform:perspective(2200px) rotateY(-10deg)">{screen(f"{A}/ui/s77.jpg", 1200, spot(1200, MINT), True)}</div>
<div style="position:absolute;left:110px;top:330px;width:520px">
  <div style="font:700 22px Montserrat;letter-spacing:.3em;color:{MINT}">LAMAN UTAMA</div>
  <div style="font:900 60px/1.08 Montserrat;margin-top:16px">Semua aset,<br>satu paparan.</div>
  <div style="font:500 26px/1.5 Montserrat;color:rgba(255,255,255,.8);margin-top:20px">Taburan premis &amp; tanah milik MCORP di seluruh Melaka.</div></div>
<div style="position:absolute;left:110px;top:860px;display:flex;gap:14px">{''.join(f'<span style="padding:10px 18px;border-radius:30px;font:700 18px Montserrat;{"background:#fff;color:" + NAVY if j == 0 else "border:1.5px solid rgba(255,255,255,.4)"}">{t}</span>' for j, t in enumerate(["Laman Utama", "Aset Tak Alih", "Aset Alih", "Stor", "Modal Insan"]))}</div>
{logo(True)}</div>"""


def f_stat():
    return f"""<div class="fr" style="{F_BG};font-family:Montserrat;color:#fff">{F_DECO}
<div style="position:absolute;left:120px;top:170px"><div style="font:700 22px Montserrat;letter-spacing:.3em;color:{MINT}">PRODUKTIVITI</div>
<div style="font:900 64px/1.05 Montserrat;margin-top:12px">Proses permohonan sewaan</div></div>
<div style="position:absolute;left:120px;top:370px;display:flex;align-items:flex-end;gap:60px">
  <div><div style="font:600 26px Montserrat;color:rgba(255,255,255,.65)">SEBELUM</div><div style="font:900 220px/1 Montserrat;color:rgba(255,255,255,.3)">14<span style="font-size:60px"> hari</span></div></div>
  <div style="font:900 120px/1 Montserrat;color:{MINT};margin-bottom:40px">→</div>
  <div><div style="font:600 26px Montserrat;color:{MINT}">SELEPAS SPD</div><div style="font:900 300px/1 Montserrat">3<span style="font-size:80px"> hari</span></div></div></div>
<div style="position:absolute;left:120px;top:830px;display:inline-flex;align-items:center;gap:20px;padding:20px 36px;border-radius:60px;background:#fff;color:{NAVY};font:900 38px Montserrat">
  <i style="width:18px;height:18px;border-radius:50%;background:{RED};display:block"></i>11 hari dijimatkan</div>
{logo(True)}</div>"""


# ============================================================ G: editorial / annual report
def g_title():
    return f"""<div class="fr" style="background:#fff;font-family:Montserrat">
<div style="position:absolute;inset:0;background:url({A}/img/s01_freeze.jpg) center/cover"></div>
<div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,16,40,.92) 0%,rgba(10,16,40,.75) 38%,rgba(10,16,40,.05) 75%)"></div>
<div style="position:absolute;left:120px;top:120px;width:6px;height:840px;background:linear-gradient({RED},{GREEN})"></div>
<div style="position:absolute;left:170px;top:260px;color:#fff;width:820px">
  <div style="font:600 22px Montserrat;letter-spacing:.32em;color:rgba(255,255,255,.7)">PERBADANAN MELAKA · 2026</div>
  <div style="font:800 64px/1.08 Montserrat;margin-top:28px">Pembangunan<br>Sistem Pengurusan<br>Data Bersepadu <span style="color:{MINT}">(SPD)</span></div>
  <div style="width:90px;height:4px;background:{RED};margin:36px 0 30px"></div>
  <div style="font:400 30px/1.5 'Playfair Display';font-style:italic;color:rgba(255,255,255,.9)">Inovasi digital ke arah pengurusan hijau dan lestari</div>
</div>{logo(True)}</div>"""


def g_problem():
    rows = "".join(f'<div style="display:grid;grid-template-columns:90px 1fr;align-items:center;padding:22px 0;border-bottom:1px solid #d9dce6">'
                   f'<div style="font:800 34px Montserrat;color:{RED}">0{i + 1}</div><div style="font:600 34px Montserrat;color:#1B2140">{t}</div></div>'
                   for i, (k, t) in enumerate(PROB))
    return f"""<div class="fr" style="background:#fff;font-family:Montserrat">
<div style="position:absolute;right:0;top:0;width:780px;height:1080px;background:url({A}/sb/lk1-22.jpg) center/cover"></div>
<div style="position:absolute;right:0;top:0;width:780px;height:1080px;background:linear-gradient(90deg,#fff 0%,rgba(255,255,255,0) 25%)"></div>
<div style="position:absolute;left:130px;top:110px;width:950px">
  <div style="font:600 22px Montserrat;letter-spacing:.32em;color:{GREEN}">PENYATAAN MASALAH</div>
  <div style="font:400 72px/1.1 'Playfair Display';color:{NAVY};margin:18px 0 34px">Enam cabaran <i>sebelum SPD</i></div>{rows}</div>
{logo()}</div>"""


def g_demo():
    return f"""<div class="fr" style="background:#F4F2EE;font-family:Montserrat">
<div style="position:absolute;left:0;top:0;width:500px;height:1080px;background:{NAVY}"></div>
<div style="position:absolute;left:90px;top:200px;width:380px;color:#fff">
  <div style="font:600 22px Montserrat;letter-spacing:.32em;color:{MINT}">MODUL 01</div>
  <div style="font:400 64px/1.1 'Playfair Display';margin-top:20px">Laman Utama</div>
  <div style="width:70px;height:4px;background:{RED};margin:30px 0"></div>
  <div style="font:400 26px/1.6 Montserrat;color:rgba(255,255,255,.85)">Taburan premis dan tanah milik MCORP di seluruh Melaka, dalam satu paparan.</div></div>
<div style="position:absolute;left:520px;top:200px">{screen(f"{A}/ui/s77.jpg", 1290, spot(1290, MINT))}</div>
<div style="position:absolute;left:720px;top:900px;font:600 20px Montserrat;letter-spacing:.2em;color:#8a8f9f">SISTEM PENGURUSAN DATA · SPD.PKNM.GOV.MY</div>
{logo()}</div>"""


def g_stat():
    return f"""<div class="fr" style="background:#fff;font-family:Montserrat">
<div style="position:absolute;left:0;top:0;width:820px;height:1080px;background:url({A}/sb/lk3-22.jpg) center/cover"></div>
<div style="position:absolute;left:0;top:0;width:820px;height:1080px;background:linear-gradient(0deg,rgba(10,16,40,.75),rgba(10,16,40,.1) 60%)"></div>
<div style="position:absolute;left:80px;top:900px;font:600 22px Montserrat;letter-spacing:.24em;color:#fff">SEBELUM: 14 HARI SECARA MANUAL</div>
<div style="position:absolute;left:940px;top:180px;width:880px">
  <div style="font:600 22px Montserrat;letter-spacing:.32em;color:{GREEN}">PRODUKTIVITI · SEWAAN</div>
  <div style="font:400 56px/1.15 'Playfair Display';color:{NAVY};margin-top:20px">Proses permohonan sewaan kini</div>
  <div style="font:800 360px/0.9 Montserrat;color:{NAVY};letter-spacing:-.04em;margin-top:30px">3<span style="font-size:90px;letter-spacing:0"> hari</span></div>
  <div style="height:1px;background:#d9dce6;margin:40px 0 30px"></div>
  <div style="display:flex;gap:70px"><div><div style="font:800 64px Montserrat;color:{GREEN}">11</div><div style="font:600 22px Montserrat;color:#6A7090">hari dijimatkan</div></div>
  <div><div style="font:800 64px Montserrat;color:{RED}">−79%</div><div style="font:600 22px Montserrat;color:#6A7090">tempoh proses</div></div></div></div>
{logo()}</div>"""


BOARDS = {
    "E": ("E · KORPORAT KACA", "Gradien lembut · kad kaca lut sinar · moden & bersih", "E_korporat-kaca", [e_title, e_problem, e_demo, e_stat], "#f7f9fc", NAVY),
    "F": ("F · GRADIEN BERANI", "Biru tua ke zamrud · foto dalam bentuk · grafik kaya", "F_gradien-berani", [f_title, f_problem, f_demo, f_stat], "#141a52", "#ffffff"),
    "G": ("G · EDITORIAL / LAPORAN TAHUNAN", "Foto penuh dari lakonan · grid kemas · angka besar · serif + sans", "G_editorial", [g_title, g_problem, g_demo, g_stat], "#ffffff", NAVY),
}
LABELS = ["Tajuk", "Penyataan masalah", "Demo sistem", "Statistik"]

JS = r"""
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--proxy-server=' + (process.env.HTTPS_PROXY || 'direct://'), '--ignore-certificate-errors'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + process.argv[2] + '/styleboard_efg.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  for (const id of process.argv.slice(3)) await p.locator('#' + id).screenshot({ path: process.argv[2] + '/f_' + id + '.jpg', type: 'jpeg', quality: 90 });
  await b.close();
})();
"""

if __name__ == "__main__":
    css = "*{margin:0;padding:0;box-sizing:border-box}body{background:#ccc}.fr{position:relative;width:1920px;height:1080px;overflow:hidden}"
    html = ['<!doctype html><html><head><meta charset="utf-8">',
            '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Playfair+Display:ital,wght@0,400;1,400&display=block" rel="stylesheet">',
            f'<style>{css}</style></head><body>']
    ids = []
    for key, (_, _, _, fns, _, _) in BOARDS.items():
        for i, fn in enumerate(fns):
            html.append(f'<div id="{key}{i + 1}">{fn()}</div>')
            ids.append(f"{key}{i + 1}")
    html.append("</body></html>")
    (OUT / "styleboard_efg.html").write_text("\n".join(html), encoding="utf-8")
    js = OUT / "_render.js"
    js.write_text(JS)
    subprocess.run(["node", str(js), str(OUT)] + ids, check=True, cwd=str(ROOT))
    js.unlink()
    from PIL import Image, ImageDraw, ImageFont
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    for key, (name, sub, fname, fns, bg, fg) in BOARDS.items():
        ims = [Image.open(OUT / f"f_{key}{i + 1}.jpg") for i in range(len(fns))]
        W = 2400
        board = Image.new("RGB", (W, 180 + 1350 + 40 + 50 + round((W - 40) // 3 * 9 / 16) + 30), bg)
        d = ImageDraw.Draw(board)
        d.text((60, 45), name, fill=fg, font=f1)
        d.text((60, 118), sub, fill=GREEN if bg != "#141a52" else MINT, font=f2)
        board.paste(ims[0].resize((W, 1350)), (0, 180))
        y = 180 + 1350 + 40
        w3 = (W - 40) // 3
        for i, im in enumerate(ims[1:]):
            x = 10 + i * (w3 + 10)
            d.text((x + 10, y + 4), f"0{i + 2}  {LABELS[i + 1]}", fill=fg, font=f2)
            board.paste(im.resize((w3, round(w3 * 9 / 16))), (x, y + 50))
        board.save(OUT / f"{fname}.jpg", quality=88)
    print("ok")
