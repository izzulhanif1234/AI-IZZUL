"""SPD GREEN style board C: "Hyper Glass 3D" - volumetric light, reflective floor, thick glass, chrome type,
exploded UI layers. Writes edits/spd-green/styleboard/C_hyper-glass.jpg and f_C0*.jpg."""
import pathlib
import subprocess

ROOT = pathlib.Path("/home/user/AI-IZZUL")
OUT = ROOT / "edits/spd-green/styleboard"
A = "../hf/assets"

CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}body{background:#000}
.fr{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:Sora,sans-serif;color:#fff;background:#020504}
.stage{position:absolute;inset:0;background:
  radial-gradient(60% 55% at 50% 38%, rgba(30,190,120,.28) 0%, rgba(10,60,40,.18) 40%, transparent 70%),
  radial-gradient(40% 40% at 85% 10%, rgba(120,255,200,.10), transparent 70%),
  linear-gradient(#030806, #020403 60%, #000)}
.beam{position:absolute;top:-200px;width:420px;height:1500px;background:linear-gradient(180deg,rgba(150,255,210,.22),rgba(150,255,210,0) 75%);
  filter:blur(28px);transform-origin:50% 0;mix-blend-mode:screen}
.floor{position:absolute;left:-400px;right:-400px;top:700px;height:900px;transform:perspective(900px) rotateX(72deg);transform-origin:50% 0;
  background:
   repeating-linear-gradient(90deg, rgba(120,255,200,.12) 0 1px, transparent 1px 120px),
   repeating-linear-gradient(0deg, rgba(120,255,200,.10) 0 1px, transparent 1px 120px),
   radial-gradient(50% 60% at 50% 0%, rgba(40,200,130,.25), transparent 70%);
  -webkit-mask-image:linear-gradient(#000, transparent 80%)}
.bokeh{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(170,255,215,.55),rgba(170,255,215,0) 70%);filter:blur(2px)}
.chrome{background:linear-gradient(180deg,#ffffff 0%,#e9f4ef 38%,#8fa59a 52%,#f4fffa 62%,#b9cbc2 100%);-webkit-background-clip:text;color:transparent;
  filter:drop-shadow(0 2px 0 rgba(255,255,255,.25)) drop-shadow(0 30px 60px rgba(0,0,0,.6))}
.glow{text-shadow:0 0 40px rgba(120,255,190,.55)}
.glass{position:absolute;border-radius:28px;background:linear-gradient(145deg,rgba(255,255,255,.16),rgba(255,255,255,.04) 45%,rgba(255,255,255,.08));
  border:1.5px solid rgba(255,255,255,.28);box-shadow:inset 0 1px 0 rgba(255,255,255,.5),inset 0 -20px 40px rgba(0,0,0,.25),0 40px 90px rgba(0,0,0,.6),0 0 60px rgba(60,220,150,.18);
  backdrop-filter:blur(18px) saturate(140%)}
.glass:after{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(120deg,rgba(255,255,255,.28),transparent 30%);pointer-events:none}
.kick{font:600 22px Sora;letter-spacing:.38em;color:#9dfccb}
.refl{position:absolute;transform:scaleY(-1);opacity:.22;-webkit-mask-image:linear-gradient(transparent 55%,#000);filter:blur(1.5px)}
"""


def stage(extra_beams=True):
    beams = "".join(f'<div class="beam" style="left:{x}px;transform:rotate({r}deg);opacity:{o}"></div>'
                    for x, r, o in [(620, 18, .9), (900, 2, .7), (1180, -16, .85), (300, 30, .35), (1500, -28, .35)]) if extra_beams else ""
    bok = "".join(f'<div class="bokeh" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;opacity:{o}"></div>'
                  for x, y, s, o in [(160, 220, 60, .5), (1700, 160, 90, .35), (1500, 600, 40, .6), (260, 760, 110, .25), (980, 120, 30, .7),
                                     (1260, 300, 22, .8), (520, 420, 26, .6), (1820, 820, 70, .3), (80, 520, 34, .5), (1380, 900, 50, .35)])
    return f'<div class="stage"></div>{beams}<div class="floor"></div>{bok}'


def badge():
    return (f'<img src="{A}/img/logo-pptx.png" style="position:absolute;right:44px;top:30px;width:118px;transform:perspective(600px) rotateY(-18deg);'
            f'filter:drop-shadow(0 0 1.2px #fff) drop-shadow(0 0 1.2px #fff) drop-shadow(0 6px 10px rgba(0,0,0,.45));z-index:9">')


def leaf(w):
    return (f'<svg viewBox="0 0 64 64" style="width:{w}px;height:{w}px;filter:drop-shadow(0 0 18px rgba(120,255,190,.8))">'
            '<defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d9ffe9"/><stop offset=".5" stop-color="#3ee39a"/><stop offset="1" stop-color="#0e8a5a"/></linearGradient></defs>'
            '<path d="M32 60C12 47 10 21 32 4c22 17 20 43 0 56z" fill="url(#lg)"/><path d="M32 57V14M32 40l-10-9M32 29l10-9" stroke="#eafff3" stroke-width="2" fill="none" opacity=".8"/></svg>')


def f_title():
    layers = "".join(f'<div style="position:absolute;left:0;right:0;top:{250 + i * 2}px;text-align:center;font:800 330px/1 Sora;letter-spacing:-.04em;'
                     f'color:rgb({10 + i * 3},{40 + i * 6},{30 + i * 4});transform:translateZ(-{(13 - i) * 4}px)">SPD</div>' for i in range(13))
    return f"""<div class="fr">{stage()}
<div style="position:absolute;inset:0;transform:perspective(1400px) rotateX(8deg)">{layers}
  <div class="chrome" style="position:absolute;left:0;right:0;top:276px;text-align:center;font:800 330px/1 Sora;letter-spacing:-.04em">SPD</div></div>
<div style="position:absolute;left:1325px;top:250px">{leaf(130)}</div>
<div class="refl" style="left:0;right:0;top:600px;text-align:center;font:800 330px/1 Sora;letter-spacing:-.04em;color:#7fe0b0">SPD</div>
<div class="kick" style="position:absolute;left:0;right:0;top:200px;text-align:center">PERBADANAN MELAKA</div>
<div style="position:absolute;left:0;right:0;top:745px;text-align:center;font:600 52px Sora;letter-spacing:.01em" class="glow">Sistem Pengurusan Data Bersepadu</div>
<div style="position:absolute;left:0;right:0;top:825px;text-align:center;font:400 30px Sora;color:#9dfccb;letter-spacing:.06em">INOVASI DIGITAL KE ARAH PENGURUSAN HIJAU DAN LESTARI</div>
{badge()}</div>"""


def f_demo():
    W = 1180
    H = round(W * 912 / 1920)
    pop = lambda img, x0, y0, x1, y1, w, x, y, rz, z: (  # noqa: E731
        f'<div class="glass" style="left:{x}px;top:{y}px;width:{w + 28}px;padding:14px;transform:perspective(1600px) rotateY(-14deg) rotateZ({rz}deg) translateZ({z}px)">'
        f'<div style="width:{w}px;height:{(y1 - y0) * w / (x1 - x0):.0f}px;border-radius:14px;background:url({img}) -{x0 * w / (x1 - x0):.0f}px -{y0 * w / (x1 - x0):.0f}px/{1920 * w / (x1 - x0):.0f}px auto no-repeat"></div></div>')
    return f"""<div class="fr">{stage()}
<div style="position:absolute;left:330px;top:150px;width:{W + 40}px;transform:perspective(2200px) rotateY(-16deg) rotateX(6deg)">
  <div style="padding:20px;border-radius:28px;background:linear-gradient(160deg,#3a3f42,#0e1012);box-shadow:0 0 0 1px rgba(255,255,255,.18) inset,0 80px 160px rgba(0,0,0,.8),0 0 120px rgba(60,220,150,.25)">
    <div style="width:{W}px;height:{H}px;border-radius:12px;background:url({A}/ui/s77.jpg) left top/cover;filter:brightness(.55) saturate(.9)"></div></div>
  <div style="margin:0 auto;width:420px;height:26px;background:linear-gradient(#2a2e30,#0c0d0e);border-radius:0 0 18px 18px"></div>
</div>
{pop(f"{A}/ui/s77.jpg", 44, 260, 1856, 766, 980, 760, 300, -2, 220)}
{pop(f"{A}/ui/s78.jpg", 30, 160, 1240, 450, 520, 1290, 700, 3, 160)}
<div style="position:absolute;left:110px;top:700px;width:560px">
  <div class="kick">LAMAN UTAMA</div>
  <div class="chrome" style="font:800 74px/1.02 Sora;margin-top:18px;letter-spacing:-.02em">Semua aset.<br>Satu paparan.</div>
  <div style="font:400 26px/1.5 Sora;color:#b5d8c7;margin-top:18px">Taburan premis &amp; tanah milik MCORP di seluruh Melaka.</div>
</div>
{badge()}</div>"""


def f_stat():
    return f"""<div class="fr">{stage()}
<div class="kick" style="position:absolute;left:0;right:0;top:150px;text-align:center">PRODUKTIVITI · PROSES SEWAAN</div>
<div style="position:absolute;left:0;right:0;top:230px;display:flex;justify-content:center;align-items:center;gap:70px">
  <div style="font:700 220px/1 Sora;color:rgba(255,255,255,.18);position:relative">14<i style="position:absolute;left:-10px;right:-10px;top:52%;height:6px;border-radius:3px;background:linear-gradient(90deg,#ff6b6b,#ff9b6b);box-shadow:0 0 20px #ff6b6b;display:block"></i></div>
  <svg viewBox="0 0 100 40" style="width:160px"><path d="M0 20h88M72 6l16 14-16 14" stroke="#9dfccb" stroke-width="4" fill="none" stroke-linecap="round" style="filter:drop-shadow(0 0 10px #3ee39a)"/></svg>
  <div class="chrome" style="font:800 400px/0.9 Sora;letter-spacing:-.05em">3</div>
  <div class="glow" style="font:700 90px Sora">HARI</div>
</div>
<div class="refl" style="left:0;right:0;top:640px;display:flex;justify-content:center;font:800 400px/0.9 Sora;color:#6fe0a8;padding-left:250px">3</div>
<div class="glass" style="left:610px;top:770px;width:700px;height:150px;display:flex;align-items:center;justify-content:center;gap:28px">
  {leaf(70)}<div><div style="font:800 64px/1 Sora" class="glow">11 hari</div><div style="font:500 26px Sora;color:#b5d8c7;margin-top:6px">dijimatkan setiap permohonan</div></div></div>
{badge()}</div>"""


def f_dash():
    tiles = [("KERTAS A4", "−25.4%"), ("DAKWAT", "−39.7%"), ("SEWAAN", "−79%"), ("SEMAKAN ASET", "−90%"), ("TENAGA KERJA", "−50%"), ("PENJIMATAN", "RM217k")]
    layers = []
    # exploded layers: base page, panel layer, KPI layer floating towards camera
    layers.append(f'<div style="position:absolute;left:0;top:0;width:1100px;height:640px;border-radius:24px;background:url({A}/sb/ui-map.jpg) center/cover;'
                  f'filter:brightness(.35) saturate(.8);box-shadow:0 60px 120px rgba(0,0,0,.7);transform:translateZ(-220px)"></div>')
    layers.append('<div class="glass" style="left:40px;top:40px;width:1020px;height:560px;transform:translateZ(-60px)"></div>')
    kp = "".join(f'<div class="glass" style="left:{80 + (i % 3) * 330}px;top:{90 + (i // 3) * 240}px;width:300px;height:200px;padding:28px;transform:translateZ({90 + i * 18}px)">'
                 f'<div style="font:600 16px Sora;letter-spacing:.24em;color:#9dfccb">{a}</div><div class="chrome" style="font:800 {64 if i < 5 else 58}px/1.1 Sora;margin-top:22px">{b}</div></div>'
                 for i, (a, b) in enumerate(tiles))
    circ = 2 * 3.14159 * 120
    gauge = (f'<svg viewBox="0 0 280 280" style="width:330px;height:330px;filter:drop-shadow(0 0 30px rgba(62,227,154,.6))">'
             f'<circle cx="140" cy="140" r="120" stroke="rgba(255,255,255,.12)" stroke-width="16" fill="none"/>'
             f'<defs><linearGradient id="gg2"><stop offset="0" stop-color="#0e8a5a"/><stop offset="1" stop-color="#b8ffd8"/></linearGradient></defs>'
             f'<circle cx="140" cy="140" r="120" stroke="url(#gg2)" stroke-width="16" fill="none" stroke-linecap="round" stroke-dasharray="{circ * .82:.0f} {circ:.0f}" transform="rotate(-90 140 140)"/>'
             f'<text x="140" y="165" text-anchor="middle" font-family="Sora" font-weight="800" font-size="104" fill="#fff">82</text></svg>')
    return f"""<div class="fr">{stage()}
<div class="kick" style="position:absolute;left:120px;top:130px">AKAN DATANG</div>
<div class="chrome" style="position:absolute;left:120px;top:175px;font:800 150px/1 Sora;letter-spacing:-.04em">SPD 2.0</div>
<div class="glow" style="position:absolute;left:120px;top:345px;font:600 40px Sora">Green Dashboard</div>
<div style="position:absolute;left:130px;top:470px;text-align:center">{gauge}<div style="font:600 18px Sora;letter-spacing:.3em;color:#9dfccb;margin-top:8px">GREEN INDEX</div></div>
<div style="position:absolute;left:700px;top:250px;width:1100px;height:640px;transform-style:preserve-3d;transform:perspective(2000px) rotateY(-22deg) rotateX(10deg)">{''.join(layers)}{kp}</div>
{badge()}</div>"""


FRAMES = [("01", "Tajuk", f_title), ("02", "Demo sistem", f_demo), ("03", "Statistik", f_stat), ("04", "SPD 2.0 + Green Dashboard", f_dash)]

JS = r"""
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--proxy-server=' + (process.env.HTTPS_PROXY || 'direct://'), '--ignore-certificate-errors'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + process.argv[2] + '/styleboard_c.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  for (const id of process.argv.slice(3)) await p.locator('#' + id).screenshot({ path: process.argv[2] + '/f_' + id + '.jpg', type: 'jpeg', quality: 90 });
  await b.close();
})();
"""

if __name__ == "__main__":
    html = ['<!doctype html><html><head><meta charset="utf-8">',
            '<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&display=block" rel="stylesheet">',
            f'<style>{CSS}</style></head><body>'] + [f'<div id="C{n}">{fn()}</div>' for n, _, fn in FRAMES] + ["</body></html>"]
    (OUT / "styleboard_c.html").write_text("\n".join(html), encoding="utf-8")
    js = OUT / "_render.js"
    js.write_text(JS)
    subprocess.run(["node", str(js), str(OUT)] + [f"C{n}" for n, _, _ in FRAMES], check=True, cwd=str(ROOT))
    js.unlink()
    from PIL import Image, ImageDraw, ImageFont
    ims = [Image.open(OUT / f"f_C{n}.jpg") for n, _, _ in FRAMES]
    W = 2400
    board = Image.new("RGB", (W, 180 + 2 * (675 + 70)), "#050806")
    d = ImageDraw.Draw(board)
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    d.text((60, 45), "C · HYPER GLASS 3D", fill="#f2fff8", font=f1)
    d.text((60, 118), "Cahaya volumetrik · lantai berkilat · kaca 3D tebal · teks chrome · UI berlapis 3D", fill="#9dfccb", font=f2)
    for i, (im, (n, label, _)) in enumerate(zip(ims, FRAMES)):
        x, y = (i % 2) * (W // 2), 180 + (i // 2) * (675 + 70)
        d.text((x + 30, y + 10), f"{n}  {label}", fill="#f2fff8", font=f2)
        board.paste(im.resize((W // 2 - 20, 675 - 0)), (x + 10, y + 60))
    board.save(OUT / "C_hyper-glass.jpg", quality=88)
    print("ok")
