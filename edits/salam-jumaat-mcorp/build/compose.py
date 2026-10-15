"""Generate hf/index.html: Salam Jumaat motion poster for MCORP, 1080x1350 (4:5 social feed), 42s.

Islamic visual language: deep emerald ground, gold girih (8-point star) lattice, a mihrab arch that
frames the MCORP headquarters drone shot, swinging lanterns, rising gold dust. Copy is the client's,
verbatim (paragraphs only gain gold emphasis on key phrases).
Usage: python3 compose.py
"""
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
W, H = 1080, 1350
DURATION = 42.0

AYAT = "إِنَّ اللَّهَ لَا يُغَيِّرُ مَا بِقَوْمٍ حَتَّىٰ يُغَيِّرُوا مَا بِأَنْفُسِهِمْ"
TRANSLATION = ("“Sesungguhnya Allah tidak mengubah apa yang ada pada sesuatu kaum sehingga mereka mengubah "
               "apa yang ada pada diri mereka sendiri.”")
CITATION = "Surah Ar-Ra'd, ayat 11"
# paragraphs: (id, start, end, background photo, text with [[gold emphasis]])
PARAS = [
    ("p1", 18.0, 23.6, "f5", "Kemajuan bermula dengan [[kesungguhan untuk berubah]], [[keberanian]] melakukan penambahbaikan "
                            "dan [[komitmen]] untuk memberikan yang terbaik."),
    ("p2", 23.6, 30.4, "f2", "Semoga [[MCORP]] terus melangkah ke hadapan dengan [[visi yang jelas]], [[semangat berpasukan]] "
                            "dan [[iltizam]] untuk membawa manfaat kepada organisasi serta negeri Melaka."),
    ("p3", 30.4, 34.8, "f8", "Moga setiap perubahan ke arah kebaikan mendapat [[reda dan keberkatan Allah SWT]]."),
]
ARCH = "M150,930 L150,470 C150,300 330,215 540,150 C750,215 930,300 930,470 L930,930 Z"
ARCH_OUT = "M128,952 L128,466 C128,286 318,194 540,122 C762,194 952,286 952,466 L952,952 Z"


def star_points(cx, cy, n, R, r, rot=0.0):
    pts = []
    for i in range(2 * n):
        a = rot + math.pi * i / n - math.pi / 2
        rad = R if i % 2 == 0 else r
        pts.append(f"{cx + rad * math.cos(a):.1f},{cy + rad * math.sin(a):.1f}")
    return " ".join(pts)


def star8(cx, cy, R, cls="", extra=""):
    """Classic khatam: two overlapping squares + centre circle."""
    s = R * 0.707
    return (f'<g class="{cls}" {extra}><rect x="{cx - s:.1f}" y="{cy - s:.1f}" width="{2 * s:.1f}" height="{2 * s:.1f}" pathLength="1" stroke-dasharray="1"/>'
            f'<rect x="{cx - s:.1f}" y="{cy - s:.1f}" width="{2 * s:.1f}" height="{2 * s:.1f}" transform="rotate(45 {cx} {cy})" pathLength="1" stroke-dasharray="1"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{R * 0.32:.1f}" pathLength="1" stroke-dasharray="1"/></g>')


def lantern(x, id_):
    return f"""<svg id="{id_}" class="lantern" style="left:{x - 45}px" width="90" height="300" viewBox="0 0 90 300">
  <defs><radialGradient id="{id_}g" cx="50%" cy="55%" r="55%"><stop offset="0" stop-color="#fff6c8"/><stop offset="0.35" stop-color="#ffd36b"/>
  <stop offset="1" stop-color="#b9771a" stop-opacity="0"/></radialGradient></defs>
  <line x1="45" y1="0" x2="45" y2="120" stroke="#c9a54a" stroke-width="2"/>
  <circle cx="45" cy="124" r="5" fill="none" stroke="#e2c062" stroke-width="2"/>
  <path d="M30,140 L60,140 L68,152 L22,152 Z" fill="#c9a54a"/>
  <circle cx="45" cy="205" r="62" fill="url(#{id_}g)" opacity="0.55" class="glow"/>
  <path d="M22,152 L68,152 L78,200 L66,252 L24,252 L12,200 Z" fill="rgba(255,214,120,0.28)" stroke="#e2c062" stroke-width="2.5"/>
  <path d="M45,152 L45,252 M22,152 L12,200 L24,252 M68,152 L78,200 L66,252 M12,200 L78,200" stroke="#e2c062" stroke-width="1.4" fill="none"/>
  <path d="M24,252 L66,252 L56,266 L34,266 Z" fill="#c9a54a"/>
  <path d="M45,266 L45,290" stroke="#c9a54a" stroke-width="3"/><circle cx="45" cy="293" r="4" fill="#e2c062"/>
</svg>"""


CSS = """
@font-face { font-family: "Amiri Quran"; src: url(assets/fonts/AmiriQuran-400.ttf); }
@font-face { font-family: "Amiri"; font-weight: 400; src: url(assets/fonts/Amiri-400.ttf); }
@font-face { font-family: "Amiri"; font-weight: 700; src: url(assets/fonts/Amiri-700.ttf); }
@font-face { font-family: "Cinzel"; font-weight: 500; src: url(assets/fonts/Cinzel-500.ttf); }
@font-face { font-family: "Cinzel"; font-weight: 700; src: url(assets/fonts/Cinzel-700.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 500; src: url(assets/fonts/Montserrat-500.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 600; src: url(assets/fonts/Montserrat-600.ttf); }
:root { --em: #0b4433; --em-deep: #041d16; --gold: #e0b955; --gold-l: #fff1b8; --gold-d: #a77b25; --cream: #f8f0dc; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1350px; overflow: hidden; background: var(--em-deep); }
#root { position: relative; width: 1080px; height: 1350px; overflow: hidden; color: var(--cream); font-family: Montserrat, sans-serif;
  background: radial-gradient(ellipse 80% 65% at 50% 42%, #125a43 0%, #0b4433 40%, #041d16 100%); }
.clip { position: absolute; inset: 0; }
.layer { position: absolute; inset: 0; pointer-events: none; }
.gold { background: linear-gradient(180deg, var(--gold-l) 0%, #f0cf6e 38%, #c9982f 72%, var(--gold-d) 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; }
.mask { display: block; overflow: hidden; }
.mask > span, .mask > div { display: block; }
svg .ln, svg .ln * { fill: none; stroke: var(--gold); }

#lattice { opacity: 0.11; }
#bgimgs img { position: absolute; left: 0; top: 0; width: 1080px; height: 1350px; object-fit: cover; opacity: 0; }
#bg-tint { background: linear-gradient(180deg, rgba(4,29,22,0.82) 0%, rgba(11,68,51,0.72) 45%, rgba(4,29,22,0.92) 100%); opacity: 0; }
#rays { inset: -400px; opacity: 0; mix-blend-mode: screen;
  background: conic-gradient(from 180deg at 50% 26%, rgba(255,225,140,0) 0deg, rgba(255,225,140,0.16) 8deg, rgba(255,225,140,0) 16deg,
    rgba(255,225,140,0.12) 30deg, rgba(255,225,140,0) 40deg, rgba(255,225,140,0.14) 320deg, rgba(255,225,140,0) 330deg,
    rgba(255,225,140,0.1) 344deg, rgba(255,225,140,0) 352deg); }
#sweep { opacity: 0; mix-blend-mode: screen; background: linear-gradient(105deg, rgba(255,220,120,0) 35%, rgba(255,226,140,0.55) 50%, rgba(255,220,120,0) 65%); }
#vignette { background: radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.5) 100%); }

/* arch */
.arch-win { clip-path: path('__ARCH__'); }
.arch-win video { position: absolute; width: 1422px; height: 800px; left: -171px; top: 140px; object-fit: cover; }
.arch-win .shade { background: linear-gradient(180deg, rgba(4,29,22,0) 55%, rgba(4,29,22,0.65) 100%); }
.arch-frame { overflow: visible; }
.arch-frame .a1 { stroke-width: 4; } .arch-frame .a2 { stroke-width: 1.6; }

/* hero rosette */
#rosette { left: 0; top: 0; }
#rosette * { stroke-width: 2.2; }

/* lanterns */
.lantern { position: absolute; top: -30px; transform-origin: 45px 0px; }

/* title */
#title { position: absolute; left: 0; right: 0; top: 958px; text-align: center; }
#t-ar { font-family: "Amiri", serif; font-weight: 700; font-size: 54px; line-height: 1.25; }
#t-main { font-family: Cinzel, serif; font-weight: 700; font-size: 104px; line-height: 1.02; letter-spacing: 0.06em; }
#t-sub { font-family: Cinzel, serif; font-weight: 500; font-size: 40px; letter-spacing: 0.22em; margin-top: 6px; color: var(--cream); }
.divider { display: flex; align-items: center; justify-content: center; gap: 16px; margin: 18px auto 12px; }
.divider i { display: block; height: 1.5px; width: 150px; background: linear-gradient(90deg, rgba(224,185,85,0), var(--gold)); }
.divider i.r { background: linear-gradient(270deg, rgba(224,185,85,0), var(--gold)); }
#t-mc { font-family: Montserrat, sans-serif; font-weight: 600; font-size: 22px; letter-spacing: 0.5em; color: var(--gold); padding-left: 0.5em; }

/* panels */
.panel { position: absolute; left: 70px; right: 70px; border: 2px solid rgba(224,185,85,0.85); padding: 64px 56px;
  background: linear-gradient(180deg, rgba(4,29,22,0.72), rgba(11,68,51,0.62)); box-shadow: 0 30px 80px rgba(0,0,0,0.35); }
.panel::before { content: ""; position: absolute; inset: 10px; border: 1px solid rgba(224,185,85,0.45); }
.corner { position: absolute; width: 64px; height: 64px; }
.corner.tl { left: -22px; top: -22px; } .corner.tr { right: -22px; top: -22px; }
.corner.bl { left: -22px; bottom: -22px; } .corner.br { right: -22px; bottom: -22px; }
#ayat-panel { top: 300px; bottom: 110px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
#firman { font-family: Cinzel, serif; font-weight: 700; font-size: 30px; letter-spacing: 0.24em; }
#ar { direction: rtl; font-family: "Amiri Quran", "Amiri", serif; font-size: 70px; line-height: 2.05; margin-top: 26px; }
#ar .w { display: inline-block; margin: 0 0.12em; }
#tr { font-family: "Amiri", serif; font-size: 38px; line-height: 1.45; margin-top: 30px; color: var(--cream); }
#cite { display: flex; align-items: center; gap: 18px; margin-top: 36px; font-family: Cinzel, serif; font-weight: 700; font-size: 28px; letter-spacing: 0.08em; }
#cite i { display: block; width: 90px; height: 1.5px; background: var(--gold); }
.para { top: 0; bottom: 0; margin: auto 0; height: fit-content; text-align: center; }
.para .tx { font-family: Montserrat, sans-serif; font-weight: 500; font-size: 46px; line-height: 1.5; color: var(--cream); }
.para .tx .w { display: inline-block; }
.para .tx .em { font-weight: 600; color: var(--gold); }
.para .star-top { display: block; margin: 0 auto 28px; }

/* end */
#plaque { position: absolute; left: 50%; top: 1218px; width: 330px; height: 104px; margin-left: -165px; border-radius: 52px;
  background: var(--cream); border: 2px solid var(--gold); display: flex; align-items: center; justify-content: center; box-shadow: 0 12px 40px rgba(0,0,0,0.35); }
#plaque img { height: 80px; width: auto; object-fit: contain; }
#end-title { position: absolute; left: 0; right: 0; top: 965px; text-align: center; }
#e-ar { font-family: "Amiri", serif; font-weight: 700; font-size: 50px; line-height: 1.2; }
#e-main { font-family: Cinzel, serif; font-weight: 700; font-size: 72px; letter-spacing: 0.06em; line-height: 1.1; }
#e-sub { font-family: Cinzel, serif; font-weight: 500; font-size: 34px; letter-spacing: 0.22em; color: var(--cream); margin-top: 4px; }
#fade { background: #000; opacity: 0; }
"""


def corners():
    c = ('<svg class="corner {p}" viewBox="-32 -32 64 64"><g class="ln" stroke-width="2">'
         '<rect x="-14" y="-14" width="28" height="28"/><rect x="-14" y="-14" width="28" height="28" transform="rotate(45)"/>'
         '<circle r="6" fill="#e0b955" stroke="none"/></g></svg>')
    return "".join(c.format(p=p) for p in ("tl", "tr", "bl", "br"))


def para_html(text):
    words = []  # (word, emphasised); punctuation-only tokens stick to the previous word
    for i, part in enumerate(text.replace("]]", "[[").split("[[")):
        for w in part.split():
            if words and all(c in ",.;:!?" for c in w):
                words[-1] = (words[-1][0] + w, words[-1][1])
            else:
                words.append((w, i % 2 == 1))
    return " ".join(f'<span class="w{" em" if em else ""}">{w}</span>' for w, em in words)


def build():
    tl = []
    rnd = random.Random(1311)
    # gold dust
    dust = []
    for i in range(38):
        x, y, s = rnd.uniform(20, 1060), rnd.uniform(100, 1350), rnd.uniform(3, 8)
        dust.append(f'<i id="d{i}" class="dust" style="left:{x:.0f}px;top:{y:.0f}px;width:{s:.1f}px;height:{s:.1f}px"></i>')
        dy, dur = rnd.uniform(180, 420), DURATION
        tl.append(f'tl.fromTo("#d{i}", {{y: 0, x: 0}}, {{y: {-dy:.0f}, x: {rnd.uniform(-40, 40):.0f}, duration: {dur}, ease: "none"}}, 0);')
        per = rnd.uniform(1.4, 2.6)
        tl.append(f'tl.fromTo("#d{i}", {{opacity: 0.1}}, {{opacity: {rnd.uniform(0.5, 0.95):.2f}, duration: {per:.2f}, yoyo: true, repeat: {int(DURATION / per)}, ease: "sine.inOut", immediateRender: false}}, {rnd.uniform(0, 1.5):.2f});')

    lattice = (f'<svg id="lattice" class="clip layer" width="1080" height="1350"><defs><pattern id="girih" width="120" height="120" patternUnits="userSpaceOnUse">'
               f'<g class="ln" stroke-width="1.4">{star8(60, 60, 44)}<path d="M0,0 L28,28 M120,0 L92,28 M0,120 L28,92 M120,120 L92,92 '
               f'M60,0 L60,16 M60,120 L60,104 M0,60 L16,60 M120,60 L104,60"/></g></pattern></defs>'
               f'<rect id="lattice-r" x="-120" y="-120" width="1320" height="1590" fill="url(#girih)"/></svg>')
    rosette = (f'<svg id="rosette" class="clip layer" width="1080" height="1350" viewBox="0 0 1080 1350"><g id="ros-g" class="ln">'
               f'<polygon id="ros1" points="{star_points(540, 560, 16, 300, 236)}" pathLength="1" stroke-dasharray="1"/>'
               f'<polygon id="ros2" points="{star_points(540, 560, 8, 210, 120, math.pi / 8)}" pathLength="1" stroke-dasharray="1"/>'
               f'<circle id="ros3" cx="540" cy="560" r="330" pathLength="1" stroke-dasharray="1"/><circle id="ros4" cx="540" cy="560" r="92" pathLength="1" stroke-dasharray="1"/>'
               f'</g></svg>')
    arch_frame = (f'<svg class="clip layer arch-frame" width="1080" height="1350"><g class="ln">'
                  f'<path class="a1 af" d="{ARCH}" pathLength="1" stroke-dasharray="1"/><path class="a2 af" d="{ARCH_OUT}" pathLength="1" stroke-dasharray="1"/></g>'
                  f'<g class="ln" stroke-width="2.5" id="key">{star8(540, 118, 34)}</g>'
                  f'<circle cx="540" cy="118" r="7" fill="#e0b955" id="key-dot"/></svg>')

    def arch_group(gid, a, b, ms, rate):
        d = round(b - a, 2)
        frame = (arch_frame.replace("af", f"af {gid}-af").replace('id="key"', f'id="{gid}-key"').replace('id="key-dot"', f'id="{gid}-kd"')
                 .replace('<svg class="clip layer arch-frame"', f'<svg id="{gid}-frame" class="clip layer arch-frame" data-start="{a}" data-duration="{d}" data-track-index="4"'))
        return (f'<div class="clip arch-win" id="{gid}-win" style="opacity:0"><video id="{gid}-v" class="clip" src="assets/footage/drone.mp4" data-start="{a}" '
                f'data-duration="{d}" data-media-start="{ms}" data-playback-rate="{rate}" data-track-index="3" muted playsinline></video>'
                f'<div class="clip shade" data-start="{a}" data-duration="{d}" data-track-index="3"></div></div>{frame}')

    # background photos (Ken Burns) behind the panels
    bg = [("f8", 7.8, 18.4), ("f5", 18.0, 24.0), ("f2", 23.6, 30.8), ("f9", 30.4, 35.2)]
    bg_html = "".join(f'<img id="bg-{i}" class="clip" src="assets/footage/{f}.jpg" data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="1" />'
                      for i, (f, a, b) in enumerate(bg))
    for i, (f, a, b) in enumerate(bg):
        tl.append(f'tl.fromTo("#bg-{i}", {{opacity: 0, scale: 1.12}}, {{opacity: 0.55, scale: 1.0, duration: {round(b - a, 2)}, ease: "none"}}, {a});')
        tl.append(f'tl.to("#bg-{i}", {{opacity: 0, duration: 0.4}}, {round(b - 0.4, 2)});')

    paras = []
    for pid, a, b, _, text in PARAS:
        paras.append(f'<div id="g-{pid}" class="clip layer" data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="5">'
                     f'<div id="{pid}" class="panel para">{corners()}<svg class="star-top" width="70" height="70" viewBox="-35 -35 70 70">'
                     f'<g class="ln" stroke-width="2">{star8(0, 0, 26)}</g></svg><div class="tx">{para_html(text)}</div></div></div>')
        tl += [
            f'tl.fromTo("#{pid}", {{opacity: 0, scale: 0.96}}, {{opacity: 1, scale: 1, duration: 0.6, ease: "power2.out"}}, {a + 0.15});',
            f'tl.from("#{pid} .star-top", {{rotation: -90, scale: 0.4, duration: 1.0, ease: "power3.out"}}, {a + 0.2});',
            f'tl.from("#{pid} .tx .w", {{opacity: 0, y: 16, filter: "blur(6px)", duration: 0.45, stagger: 0.045, ease: "power2.out"}}, {a + 0.45});',
            f'tl.to("#{pid}", {{opacity: 0, scale: 1.03, filter: "blur(6px)", duration: 0.45, ease: "power2.in"}}, {round(b - 0.45, 2)});',
        ]

    words = AYAT.split()
    ar_words = "".join(f'<span class="w gold">{w}</span>' for w in words[:6]) + "<br/>" + "".join(f'<span class="w gold">{w}</span>' for w in words[6:])
    html_graphics = f"""
      {lattice}
      <div id="bgimgs" class="clip layer">{bg_html}</div>
      <div id="bg-tint" class="clip layer"></div>
      <div id="rays" class="clip layer"></div>
      {rosette}
      {lanterns_html()}
      {arch_group("arch1", 0.9, 8.1, 0.0, 0.5)}
      <div id="g-title" class="clip layer" data-start="1.6" data-duration="6.5" data-track-index="5">
        <div id="title">
          <div class="mask"><div id="t-ar" class="gold">جُمُعَة مُبَارَكَة</div></div>
          <div class="mask"><div id="t-main" class="gold">JUMAAT</div></div>
          <div class="mask"><div id="t-sub">YANG DIBERKATI</div></div>
          <div class="divider" id="t-div"><i></i><svg width="28" height="28" viewBox="-14 -14 28 28"><g class="ln" stroke-width="1.8">{star8(0, 0, 11)}</g></svg><i class="r"></i></div>
          <div class="mask"><div id="t-mc">MCORP</div></div>
        </div>
      </div>
      <div id="g-ayat" class="clip layer" data-start="8.0" data-duration="10.1" data-track-index="5">
        <div id="ayat-panel" class="panel">{corners()}
          <div class="mask"><div id="firman" class="gold">Firman Allah SWT</div></div>
          <div id="ar">{ar_words}</div>
          <div id="tr">{TRANSLATION}</div>
          <div id="cite" class="gold"><i></i><span>{CITATION}</span><i></i></div>
        </div>
      </div>
      {"".join(paras)}
      {arch_group("arch2", 34.6, DURATION, 3.6, 0.6)}
      <div id="g-end" class="clip layer" data-start="35.0" data-duration="{DURATION - 35.0}" data-track-index="5">
        <div id="end-title">
          <div class="mask"><div id="e-ar" class="gold">جُمُعَة مُبَارَكَة</div></div>
          <div class="mask"><div id="e-main" class="gold">JUMAAT</div></div>
          <div class="mask"><div id="e-sub">YANG DIBERKATI</div></div>
        </div>
        <div id="plaque"><img src="assets/img/mcorp-logo.png" alt="MCORP" /></div>
      </div>
      <div id="dustbox" class="clip layer">{"".join(dust)}</div>
      <div id="sweep" class="clip layer"></div>
      <div id="vignette" class="clip layer"></div>
      <div id="fade" class="clip layer"></div>
"""

    up = 'yPercent: 110, duration: 0.8, ease: "power3.out"'
    tl += [
        # ambient: lattice drifts, rays breathe, lanterns swing
        'tl.fromTo("#lattice-r", {x: 0, y: 0}, {x: -60, y: -120, duration: 42, ease: "none"}, 0);',
        'tl.fromTo("#lattice", {opacity: 0}, {opacity: 0.11, duration: 1.5}, 0);',
        'tl.fromTo("#rays", {opacity: 0}, {opacity: 0.8, duration: 2.5, ease: "sine.out"}, 0.8);',
        'tl.to("#rays", {opacity: 0, duration: 0.8}, 7.4);',
        'tl.to("#rays", {opacity: 0.8, duration: 1.5}, 34.6);',
        'tl.fromTo("#rays", {rotation: -4}, {rotation: 4, duration: 42, ease: "none", immediateRender: false}, 0);',
        'tl.fromTo(".lantern", {rotation: -3.5}, {rotation: 3.5, duration: 2.6, yoyo: true, repeat: 15, ease: "sine.inOut", stagger: 0.7}, 0);',
        'tl.from(".lantern", {y: -260, duration: 1.4, ease: "back.out(1.4)", stagger: 0.15}, 0.3);',
        'tl.fromTo(".lantern .glow", {opacity: 0.35}, {opacity: 0.75, duration: 1.1, yoyo: true, repeat: 37, ease: "sine.inOut"}, 0);',
        # HOOK 0-3: rosette draws, flies through as the arch opens on the drone shot; title lands by 3.0
        'tl.fromTo("#ros-g > *", {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 0}, duration: 1.0, stagger: 0.07, ease: "power2.out"}, 0.0);',
        'tl.fromTo("#ros-g", {rotation: 0, svgOrigin: "540 560"}, {rotation: 30, duration: 1.6, ease: "power1.inOut"}, 0);',
        'tl.to("#rosette", {scale: 2.6, opacity: 0, transformOrigin: "540px 560px", duration: 0.7, ease: "power2.in"}, 1.0);',
        'tl.fromTo("#arch1-win", {scale: 0.55, opacity: 0, transformOrigin: "540px 560px"}, {scale: 1, opacity: 1, duration: 1.0, ease: "expo.out"}, 1.05);',
        'tl.fromTo(".arch1-af", {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 0}, duration: 1.2, stagger: 0.1, ease: "power2.inOut"}, 1.0);',
        'tl.from("#arch1-key", {rotation: -180, scale: 0, svgOrigin: "540 118", duration: 0.9, ease: "back.out(1.8)"}, 1.6);',
        'tl.from("#arch1-kd", {scale: 0, svgOrigin: "540 118", duration: 0.5, ease: "back.out(2)"}, 1.9);',
        'tl.fromTo("#arch1-v", {scale: 1.18}, {scale: 1.0, duration: 7.2, ease: "none"}, 0.9);',
        f'tl.from("#t-ar", {{{up}}}, 1.65);',
        'tl.from("#t-main", {yPercent: 110, duration: 0.85, ease: "power4.out"}, 1.85);',
        f'tl.from("#t-sub", {{{up}}}, 2.15);',
        'tl.from("#t-div i", {scaleX: 0, duration: 0.7, ease: "power2.out"}, 2.35);',
        'tl.from("#t-div svg", {rotation: -180, scale: 0, duration: 0.7, ease: "back.out(1.8)"}, 2.35);',
        f'tl.from("#t-mc", {{{up}}}, 2.55);',
        'tl.fromTo("#t-main", {filter: "brightness(1)"}, {filter: "brightness(1.45)", duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}, 2.6);',
        # transition to the verse: sweep of light, arch rises away
        'tl.fromTo("#sweep", {opacity: 1, xPercent: -100}, {opacity: 1, xPercent: 100, duration: 1.0, ease: "power2.inOut", immediateRender: false}, 7.3);',
        'tl.to(["#arch1-win", "#arch1-frame", "#title"], {y: -120, opacity: 0, filter: "blur(8px)", duration: 0.7, ease: "power2.in"}, 7.4);',
        'tl.fromTo("#bg-tint", {opacity: 0}, {opacity: 1, duration: 0.8}, 7.6);',
        # VERSE 8-18
        'tl.fromTo("#ayat-panel", {opacity: 0, scale: 0.95}, {opacity: 1, scale: 1, duration: 0.7, ease: "power2.out"}, 8.05);',
        'tl.from("#ayat-panel .corner", {rotation: -90, scale: 0, duration: 0.8, stagger: 0.06, ease: "back.out(1.6)"}, 8.15);',
        f'tl.from("#firman", {{{up}}}, 8.35);',
        'tl.from("#ar .w", {opacity: 0, y: 22, scale: 0.92, filter: "blur(10px)", duration: 0.65, stagger: 0.3, ease: "power2.out"}, 8.85);',
        'tl.fromTo("#ar", {filter: "drop-shadow(0 0 0px rgba(255,220,130,0))"}, {filter: "drop-shadow(0 0 18px rgba(255,220,130,0.55))", duration: 1.0, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}, 12.0);',
        'tl.from("#tr", {opacity: 0, y: 24, duration: 0.9, ease: "power2.out"}, 12.4);',
        'tl.from("#cite", {opacity: 0, y: 18, duration: 0.7, ease: "power2.out"}, 15.0);',
        'tl.from("#cite i", {scaleX: 0, duration: 0.7, ease: "power2.out"}, 15.2);',
        'tl.to("#ayat-panel", {opacity: 0, scale: 1.03, filter: "blur(6px)", duration: 0.5, ease: "power2.in"}, 17.5);',
        'tl.fromTo("#sweep", {opacity: 1, xPercent: -100}, {opacity: 1, xPercent: 100, duration: 1.0, ease: "power2.inOut", immediateRender: false}, 17.5);',
        'tl.fromTo("#sweep", {opacity: 1, xPercent: -100}, {opacity: 1, xPercent: 100, duration: 1.0, ease: "power2.inOut", immediateRender: false}, 23.1);',
        'tl.fromTo("#sweep", {opacity: 1, xPercent: -100}, {opacity: 1, xPercent: 100, duration: 1.0, ease: "power2.inOut", immediateRender: false}, 29.9);',
        # END 34.6-42: arch returns on the wide building shot; poster lockup + logo plaque
        'tl.to("#bg-tint", {opacity: 0, duration: 0.8}, 34.4);',
        'tl.fromTo("#sweep", {opacity: 1, xPercent: -100}, {opacity: 1, xPercent: 100, duration: 1.0, ease: "power2.inOut", immediateRender: false}, 34.3);',
        'tl.fromTo("#arch2-win", {scale: 0.6, opacity: 0, transformOrigin: "540px 560px"}, {scale: 1, opacity: 1, duration: 1.1, ease: "expo.out"}, 34.65);',
        'tl.fromTo(".arch2-af", {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 0}, duration: 1.2, stagger: 0.1, ease: "power2.inOut"}, 34.6);',
        'tl.from("#arch2-key", {rotation: -180, scale: 0, svgOrigin: "540 118", duration: 0.9, ease: "back.out(1.8)"}, 35.2);',
        'tl.from("#arch2-kd", {scale: 0, svgOrigin: "540 118", duration: 0.5, ease: "back.out(2)"}, 35.5);',
        'tl.fromTo("#arch2-v", {scale: 1.12}, {scale: 1.0, duration: 7.4, ease: "none"}, 34.6);',
        f'tl.from("#e-ar", {{{up}}}, 35.2);',
        'tl.from("#e-main", {yPercent: 110, duration: 0.85, ease: "power4.out"}, 35.4);',
        f'tl.from("#e-sub", {{{up}}}, 35.65);',
        'tl.from("#plaque", {y: 40, opacity: 0, scale: 0.9, duration: 0.8, ease: "back.out(1.6)"}, 36.0);',
        'tl.fromTo("#e-main", {filter: "brightness(1)"}, {filter: "brightness(1.45)", duration: 0.35, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}, 36.6);',
        'tl.to("#fade", {opacity: 1, duration: 0.9, ease: "power1.in"}, 41.1);',
    ]

    css = CSS.replace("__ARCH__", ARCH) + ".dust { position: absolute; border-radius: 50%; background: radial-gradient(circle, #fff4c4 0%, #f0c95e 45%, rgba(240,201,94,0) 72%); }"
    html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1350" />
    <!-- GENERATED by build/compose.py: edit that, not this file. -->
    <script src="vendor/gsap.min.js"></script>
    <style>{css}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1350">
      {html_graphics}
      <audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{DURATION}" data-track-index="10"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + l for l in tl).strip()}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (HERE / "hf/index.html").write_text(html)
    print("wrote hf/index.html")


def lanterns_html():
    return f'<div id="lanterns" class="clip layer">{lantern(96, "lan1")}{lantern(984, "lan2")}</div>'


build()
