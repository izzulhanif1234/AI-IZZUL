"""Generate hf/index.html: Salam Jumaat motion poster for MCORP, 1080x1350 (4:5 social feed), 42s.

v4 "3D Islamic corporate": the v3 MCORP layout (white page, building photography with diagonal
blue/red bands, bold type) rebuilt on a real CSS-3D stage:
  - a drifting perspective camera (perspective-origin moves on every 3D plane) that dollies back at
    every scene change. Scenes are flat 3D planes with their own perspective, not one deep preserve-3d
    tree: Chrome mis-culls large layers inside deep preserve-3d trees (panels were clipped on the right)
  - every scene is layered in depth (photo -150, text +40..+80, tokens -600..+300) so it parallaxes
  - scene changes are 3D cube rotations with red/blue streaks flying past the lens
  - hook: an extruded 3D khatam star (MCORP blue, red core) spins and flies through the camera
  - extruded 3D lettering flipping in letter by letter; verse words fly in from depth
  - floating 3D geometric tokens with depth of field
Copy is the client's, verbatim (paragraphs gain red emphasis on key phrases only).
Earlier looks: build/compose_v3_flat.py (flat corporate), build/compose_v2_islamic.py.
Usage: python3 compose.py
"""
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
GREETING = "جُمُعَة مُبَارَكَة"
T = [7.7, 17.7, 23.3, 30.1, 34.5]  # scene changes: cube rotation centred on these instants
HALF = 0.45  # half of the cube-rotation duration
PARAS = [  # id, photo, text with [[red emphasis]]
    ("p1", "f5", "Kemajuan bermula dengan [[kesungguhan untuk berubah]], [[keberanian]] melakukan penambahbaikan "
                 "dan [[komitmen]] untuk memberikan yang terbaik."),
    ("p2", "f2", "Semoga [[MCORP]] terus melangkah ke hadapan dengan [[visi yang jelas]], [[semangat berpasukan]] "
                 "dan [[iltizam]] untuk membawa manfaat kepada organisasi serta negeri Melaka."),
    ("p3", "f9", "Moga setiap perubahan ke arah kebaikan mendapat [[reda dan keberkatan Allah SWT]]."),
]

EXTRUDE_BLUE = ", ".join(f"{i}px {i}px 0 rgb({40 - 3 * i},{54 - 4 * i},{140 - 9 * i})" for i in range(1, 9))
EXTRUDE_RED = ", ".join(f"{i * 0.7:.1f}px {i * 0.7:.1f}px 0 rgb({220 - 12 * i},{24 - 2 * i},{32 - 2 * i})" for i in range(1, 7))

CSS = """
@font-face { font-family: "Amiri Quran"; src: url(assets/fonts/AmiriQuran-400.ttf); }
@font-face { font-family: "Amiri"; font-weight: 700; src: url(assets/fonts/Amiri-700.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 500; src: url(assets/fonts/Montserrat-500.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 600; src: url(assets/fonts/Montserrat-600.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 700; src: url(assets/fonts/Montserrat-700.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 800; src: url(assets/fonts/Montserrat-800.ttf); }
/* MCORP brand (sampled from the official logo) */
:root { --blue: #2b3990; --blue-d: #1c2670; --red: #ec1c24; --ink: #1a1f45; --grey: #5a6080; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1350px; overflow: hidden; background: #fff; }
#root { position: relative; width: 1080px; height: 1350px; overflow: hidden; color: var(--ink); font-family: Montserrat, sans-serif;
  background: radial-gradient(ellipse 90% 70% at 50% 35%, #ffffff 0%, #f3f5fb 55%, #e3e8f4 100%);
  perspective: 1500px; perspective-origin: 50% 46%; }
.clip { position: absolute; inset: 0; }
.layer { position: absolute; inset: 0; pointer-events: none; }
.p3d { position: absolute; inset: 0; transform-style: preserve-3d; }
.scene { position: absolute; inset: 0; backface-visibility: hidden; transform-origin: 50% 50% -540px; perspective: 1500px; perspective-origin: 50% 46%; }
.persp { perspective: 1500px; perspective-origin: 50% 46%; }
.mask { display: block; overflow: hidden; }
.mask > span, .mask > div { display: block; }

#texture { opacity: 0.08; }
#texture .ln, #texture .ln * { fill: none; stroke: var(--blue); }

/* photo panels with a diagonal bottom edge and blue/red bands along it */
.hero { position: absolute; overflow: visible; }
.band.s { height: 60px; background: linear-gradient(180deg, rgba(20,28,86,0.18), rgba(20,28,86,0)); }
.hero video, .hero img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }
.hero .tint { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(28,38,112,0.18), rgba(28,38,112,0) 45%); }
.band { position: absolute; left: 0; width: 1100px; transform-origin: 0 0; }
.band.b { background: var(--blue); height: 36px; }
.band.r { background: var(--red); height: 11px; }

/* extruded 3D type */
.x-blue { color: #3443a6; text-shadow: __EXB__, 0 22px 28px rgba(20,28,86,0.35); }
.x-red { color: var(--red); text-shadow: __EXR__, 0 14px 20px rgba(120,10,15,0.25); }
.ch { display: inline-block; transform-origin: 50% 100%; backface-visibility: hidden; }

/* title lockup */
.lock { position: absolute; left: 90px; right: 90px; top: 830px; }
.lock .ar { font-family: "Amiri", serif; font-weight: 700; font-size: 58px; line-height: 1.3; padding-top: 0.3em; color: var(--blue); }
.lock .big, .lock .sub { perspective: 700px; }
.lock .big { font-weight: 800; font-size: 156px; line-height: 0.95; letter-spacing: -0.005em; white-space: nowrap; }
.lock .sub { font-weight: 800; font-size: 52px; letter-spacing: 0.08em; margin-top: 14px; white-space: nowrap; }
.lock .rule { width: 120px; height: 7px; background: var(--red); margin-top: 28px; transform-origin: 0 50%; }
.sheen { position: absolute; inset: -20px -40px; background: linear-gradient(105deg, rgba(255,255,255,0) 40%, rgba(255,255,255,0.85) 50%, rgba(255,255,255,0) 60%);
  mix-blend-mode: overlay; transform: translateX(-120%); }

/* 3D extruded khatam star */
.star3d { position: absolute; width: 440px; height: 440px; left: 320px; top: 340px; transform-style: preserve-3d; }
.star3d svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }

/* floating tokens */
.tok { position: absolute; transform-style: preserve-3d; }
.tok svg { display: block; overflow: visible; }

/* verse */
#ayat { position: absolute; left: 70px; right: 70px; top: 330px; bottom: 190px; text-align: center; display: flex; flex-direction: column;
  align-items: center; justify-content: center; }
.pill { display: inline-block; font-weight: 700; font-size: 22px; letter-spacing: 0.3em; color: #fff; background: var(--red); padding: 10px 18px 10px 24px;
  box-shadow: 0 10px 20px rgba(236,28,36,0.3); }
#ar { direction: rtl; font-family: "Amiri Quran", "Amiri", serif; font-size: 80px; line-height: 2.0; color: var(--blue); margin-top: 30px;
  perspective: 900px; text-shadow: 0 10px 18px rgba(43,57,144,0.25); }
#ar .w { display: inline-block; margin: 0 0.12em; }
#tr { font-weight: 500; font-size: 36px; line-height: 1.5; color: var(--ink); margin-top: 26px; }
#ayat-in { perspective: 1000px; display: flex; flex-direction: column; align-items: center; }
#tr .ln2 { display: block; }
#cite { display: flex; align-items: center; justify-content: center; gap: 18px; margin-top: 32px; font-weight: 700; font-size: 26px; letter-spacing: 0.08em; color: var(--red); }
#cite i { display: block; width: 80px; height: 3px; background: var(--red); }

/* message cards */
.card { position: absolute; left: 70px; right: 70px; top: 500px; padding: 56px 56px 56px 50px; background: #fff; border-radius: 10px;
  box-shadow: 0 40px 70px rgba(20,28,86,0.25), 0 6px 14px rgba(20,28,86,0.12); display: flex; gap: 34px; }
.card::after { content: ""; position: absolute; right: 0; top: 0; width: 140px; height: 8px; background: var(--red); border-top-right-radius: 10px; }
.card .bar { width: 10px; background: linear-gradient(180deg, var(--red) 0 34%, var(--blue) 34% 100%); flex: none; transform-origin: 50% 0; }
.card .tx { font-weight: 600; font-size: 50px; line-height: 1.42; color: var(--ink); perspective: 800px; }
.card .tx .w { display: inline-block; transform-origin: 50% 100%; }
.card .tx .em { color: var(--red); font-weight: 800; }

/* HUD (screen-locked) brand furniture */
.shard { position: absolute; transform: skewX(-32deg); }
#sh1 { right: -150px; bottom: 0; width: 330px; height: 150px; background: var(--blue); }
#sh2 { right: 120px; bottom: 0; width: 70px; height: 150px; background: var(--red); }
#sh3 { left: -80px; bottom: 0; width: 210px; height: 22px; background: var(--red); }
#tab { position: absolute; left: 0; top: 0; width: 330px; height: 150px; background: #fff; display: flex; align-items: center;
  justify-content: center; border-bottom-right-radius: 18px; box-shadow: 0 14px 30px rgba(20,30,90,0.22); }
#tab img { height: 112px; width: auto; object-fit: contain; }
.streak { position: absolute; top: -200px; height: 1750px; transform: skewX(-20deg); }
#fade { background: #fff; opacity: 0; }
"""


def star8_path(cx, cy, R):
    """Filled 8-point khatam as one polygon (two squares' outline)."""
    pts = []
    for i in range(16):
        a = math.pi * i / 8 - math.pi / 2
        r = R if i % 2 == 0 else R * 0.765
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def star8_lines(cx, cy, R):
    s = R * 0.707
    return (f'<rect x="{cx - s:.1f}" y="{cy - s:.1f}" width="{2 * s:.1f}" height="{2 * s:.1f}"/>'
            f'<rect x="{cx - s:.1f}" y="{cy - s:.1f}" width="{2 * s:.1f}" height="{2 * s:.1f}" transform="rotate(45 {cx} {cy})"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{R * 0.32:.1f}"/>')


def extruded_star(sid, size, depth=16, front="#3443a6", core=True):
    """Stack of star slices along Z: dark back slices, gradient front face with white rim + red core."""
    c, R = size / 2, size / 2 * 0.98
    layers = []
    for i in range(depth):
        z = -depth * 1.6 + i * 1.6
        shade = int(28 + 22 * i / depth)
        layers.append(f'<svg class="sl" style="transform:translateZ({z:.1f}px)" viewBox="0 0 {size} {size}">'
                      f'<polygon points="{star8_path(c, c, R)}" fill="rgb({shade},{shade + 10},{shade + 70})"/></svg>')
    face = (f'<svg class="sl" style="transform:translateZ(0.5px)" viewBox="0 0 {size} {size}"><defs><linearGradient id="{sid}g" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="#5a6cd6"/><stop offset="0.55" stop-color="{front}"/><stop offset="1" stop-color="#1c2670"/></linearGradient></defs>'
            f'<polygon points="{star8_path(c, c, R)}" fill="url(#{sid}g)" stroke="#fff" stroke-width="{size * 0.012:.1f}"/>'
            f'<polygon points="{star8_path(c, c, R * 0.72)}" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="{size * 0.006:.1f}"/>'
            + (f'<circle cx="{c}" cy="{c}" r="{R * 0.26:.1f}" fill="#ec1c24" stroke="#fff" stroke-width="{size * 0.01:.1f}"/>' if core else "")
            + '</svg>')
    return "".join(layers) + face


def letters(text, cls, pid):
    out = []
    for i, ch in enumerate(text):
        out.append(f'<span class="ch {pid}" style="white-space:pre">{ch}</span>' if ch != " " else '<span class="ch" style="white-space:pre"> </span>')
    return f'<span class="{cls}">' + "".join(out) + "</span>"


def words(text):
    out = []
    for i, part in enumerate(text.replace("]]", "[[").split("[[")):
        for w in part.split():
            if out and all(c in ",.;:!?" for c in w):
                out[-1] = (out[-1][0] + w, out[-1][1])
            else:
                out.append((w, i % 2 == 1))
    return " ".join(f'<span class="w{" em" if em else ""}">{w}</span>' for w, em in out)


BLEED_TOP = 80
HERO_SCALE = 1.4
# Chrome rasterises 3D-transformed layers only about one viewport wide from the layer's left edge, so
# panels stay inside 0..1080 and are enlarged by scaling their wrapper about the diagonal edge instead
# of overhanging the frame. That keeps every edge off-screen through the camera orbit and dolly.
CLIP_LEN = 7.8  # drone30.mp4, played 1:1 (no slow motion)


def hero(hid, h, slope, media, a, b, vstart=None, z=-150):
    """Photo/video panel with a diagonal bottom edge whose visible part ends at y=h (left) / h-slope (right)."""
    d = round(b - a, 2)
    pw = 1080
    h2 = h + BLEED_TOP
    sl = slope
    clip = f"polygon(0 0, 100% 0, 100% {h2 - sl:.0f}px, 0 {h2}px)"
    ang = -math.degrees(math.atan2(sl, pw))
    timed = f' data-start="{a}" data-duration="{d}" data-track-index="2"' if media.endswith(".mp4") else ""
    bands = (f'<div class="band b" style="top:{h2 - 6}px;transform:rotate({ang:.3f}deg)"></div>'
             f'<div class="band r" style="top:{h2 + 36}px;transform:rotate({ang:.3f}deg)"></div>'
             f'<div class="band s" style="top:{h2 + 47}px;transform:rotate({ang:.3f}deg)"></div>')
    if media.endswith(".mp4"):
        vs = a if vstart is None else vstart
        src = (f'<video id="{hid}-m" class="clip" src="{media}" data-start="{vs}" data-duration="{min(round(b - vs, 2), CLIP_LEN)}" '
               f'data-media-start="0" data-track-index="2" muted playsinline></video>')
    else:
        src = f'<img id="{hid}-m" src="{media}" alt="" />'
    return (f'<div id="{hid}" class="hero" style="left:0;top:{-BLEED_TOP}px;width:{pw}px;height:{h2 + 70}px;'
            f'transform-origin:540px {h2}px;transform:translateZ({z}px) scale({HERO_SCALE})">'
            f'<div id="{hid}-ph" style="position:absolute;inset:0;bottom:70px;clip-path:{clip}">{src}'
            f'<div class="tint clip"{timed}></div></div><div id="{hid}-bands" class="clip"{timed}>{bands}</div></div>')


def build():
    tl = []
    rnd = random.Random(37)

    texture = ('<svg id="texture" class="clip layer" width="1080" height="1350"><defs><pattern id="g" width="120" height="120" patternUnits="userSpaceOnUse">'
               f'<g class="ln" stroke-width="1.4">{star8_lines(60, 60, 44)}<path d="M0,0 L28,28 M120,0 L92,28 M0,120 L28,92 M120,120 L92,92"/></g></pattern></defs>'
               '<rect id="tex-r" x="-200" y="-200" width="1480" height="1750" fill="url(#g)"/></svg>')

    # floating 3D tokens at depth (far ones blurred = depth of field)
    toks = []
    for i in range(16):
        z = rnd.choice([-700, -560, -420, -320, 180, 260]) if i % 5 else rnd.choice([-640, -480])
        x, y = rnd.uniform(-120, 1120), rnd.uniform(-60, 1350)
        size = rnd.uniform(46, 110) if z < 0 else rnd.uniform(26, 44)
        col = ["#2b3990", "#ec1c24", "#9aa6d8"][i % 3]
        blur = 2.5 if z < -500 else (1.2 if z < -350 else (3.0 if z > 0 else 0))
        kind = i % 2
        inner = (f'<g fill="none" stroke="{col}" stroke-width="3">{star8_lines(size / 2, size / 2, size * 0.45)}</g>' if kind == 0 else
                 f'<rect x="{size * 0.2:.0f}" y="{size * 0.2:.0f}" width="{size * 0.6:.0f}" height="{size * 0.6:.0f}" fill="{col}" opacity="0.85" transform="rotate(45 {size / 2} {size / 2})"/>')
        toks.append(f'<div id="tk{i}" class="tok" style="left:{x:.0f}px;top:{y:.0f}px;transform:translateZ({z}px)">'
                    f'<svg width="{size:.0f}" height="{size:.0f}" style="filter:blur({blur}px);opacity:{0.55 if z < 0 else 0.8}">{inner}</svg></div>')
        dur = rnd.uniform(5, 9)
        tl.append(f'tl.fromTo("#tk{i} svg", {{rotationY: 0, rotationZ: {rnd.uniform(-30, 30):.0f}}}, {{rotationY: 360, rotationZ: {rnd.uniform(60, 180):.0f}, duration: {dur:.1f}, repeat: {int(DURATION / dur)}, ease: "none"}}, 0);')
        tl.append(f'tl.fromTo("#tk{i}", {{y: 0}}, {{y: {-rnd.uniform(120, 320):.0f}, duration: {DURATION}, ease: "none"}}, 0);')

    scenes = []
    # ---------------------------------------------------------------- 1. HOOK / TITLE
    t1 = T[0] + HALF
    scenes.append(f"""
      <div id="s1" class="scene">
        {hero("hero1", 700, 150, "assets/footage/drone30.mp4", 0, t1, vstart=0.35, z=-140)}
        <div class="lock clip" style="top:850px;bottom:auto" data-start="0" data-duration="{t1}" data-track-index="3" id="lock1">
          <div class="mask"><div id="h-ar" class="ar">{GREETING}</div></div>
          <div class="big">{letters("JUMAAT", "x-blue", "c1")}</div>
          <div class="sub">{letters("YANG DIBERKATI", "x-red", "c2")}</div>
          <div id="h-rule" class="rule"></div>
          <div class="sheen" id="sheen1"></div>
        </div>
      </div>
      <div id="star-hook" class="clip persp" data-start="0" data-duration="2.2" data-track-index="4">
        <div id="star1" class="star3d">{extruded_star("st1", 440)}</div>
      </div>""")
    tl += [
        # 3D star: spins toward camera, then flies through the lens
        'tl.fromTo("#star1", {rotationY: -200, rotationX: 28, z: -900, scale: 0.6}, {rotationY: 20, rotationX: 8, z: 0, scale: 1, duration: 1.15, ease: "power3.out"}, 0);',
        'tl.to("#star1", {rotationY: 90, rotationX: -10, z: 1300, duration: 0.6, ease: "power3.in"}, 1.05);',
        'tl.to("#star1 .sl", {opacity: 0, duration: 0.25}, 1.45);',
        # photo panel flies in from deep space, swinging flat
        'tl.fromTo("#hero1", {z: -1600, rotationY: 38, rotationX: 14, y: 120, scale: 1.4, transformOrigin: "540px 780px"}, {z: -140, rotationY: 0, rotationX: 0, y: 0, scale: 1.4, duration: 1.5, ease: "expo.out"}, 0.9);',
        'tl.fromTo("#hero1-m", {scale: 1.1}, {scale: 1.0, duration: 7.2, ease: "none"}, 0.9);',
        'tl.fromTo("#hero1-bands .band", {xPercent: 100}, {xPercent: 0, duration: 0.9, stagger: 0.08, ease: "expo.out"}, 1.5);',
        # extruded letters flip up one by one
        'tl.from("#h-ar", {yPercent: 110, duration: 0.6, ease: "power3.out"}, 1.55);',
        'tl.fromTo(".c1", {rotationX: -100, z: -160, opacity: 0}, {rotationX: 0, z: 0, opacity: 1, duration: 0.7, stagger: 0.06, ease: "back.out(1.6)"}, 1.7);',
        'tl.fromTo(".c2", {rotationX: -100, z: -120, opacity: 0}, {rotationX: 0, z: 0, opacity: 1, duration: 0.55, stagger: 0.03, ease: "back.out(1.6)"}, 2.05);',
        'tl.from("#h-rule", {scaleX: 0, duration: 0.6, ease: "power2.out"}, 2.4);',
        'tl.to("#sheen1", {x: "240%", duration: 1.2, ease: "power2.inOut"}, 2.8);',
        # the title block floats slightly toward camera while the photo hangs back
        f'tl.fromTo("#lock1", {{z: 0, rotationY: 0}}, {{z: 70, rotationY: -6, duration: {t1 - 2.4:.2f}, ease: "sine.inOut", immediateRender: false}}, 2.4);',
    ]

    # ---------------------------------------------------------------- 2. VERSE
    a2, b2 = T[0] - HALF, T[1] + HALF
    ws = AYAT.split()
    ar = "".join(f'<span class="w">{w}</span>' for w in ws[:6]) + "<br/>" + "".join(f'<span class="w">{w}</span>' for w in ws[6:])
    scenes.append(f"""
      <div id="s2" class="scene clip" data-start="{a2}" data-duration="{round(b2 - a2, 2)}" data-track-index="3">
        {hero("hero2", 240, 70, "assets/footage/f8.jpg", a2, b2, z=-160)}
        <div id="ayat"><div id="ayat-in">
          <div class="mask"><span id="a-pill" class="pill">FIRMAN ALLAH SWT</span></div>
          <div id="ar">{ar}</div>
          <div id="tr">{TRANSLATION}</div>
          <div id="cite"><i></i><span>{CITATION}</span><i></i></div>
        </div></div>
      </div>""")
    a = T[0]
    tl += [
        f'tl.fromTo("#hero2-m", {{scale: 1.15}}, {{scale: 1.0, duration: {b2 - a2:.2f}, ease: "none"}}, {a2});',
        f'tl.from("#a-pill", {{yPercent: 110, duration: 0.5, ease: "power3.out"}}, {a + 0.5});',
        f'tl.fromTo("#ar .w", {{z: 650, opacity: 0, filter: "blur(10px)"}}, {{z: 0, opacity: 1, filter: "blur(0px)", duration: 0.85, stagger: 0.3, ease: "power3.out"}}, {a + 0.8});',
        f'tl.fromTo("#tr", {{rotationX: -70, opacity: 0, transformOrigin: "50% 0%"}}, {{rotationX: 0, opacity: 1, duration: 0.9, ease: "power3.out"}}, {a + 4.6});',
        f'tl.from("#cite", {{opacity: 0, y: 16, duration: 0.6, ease: "power2.out"}}, {a + 7.2});',
        f'tl.from("#cite i", {{scaleX: 0, duration: 0.6, ease: "power2.out"}}, {a + 7.35});',
        f'tl.fromTo("#ayat", {{z: 0, rotationY: 4}}, {{z: 60, rotationY: -4, duration: {b2 - a - 0.5:.2f}, ease: "sine.inOut", immediateRender: false}}, {a});',
    ]

    # ---------------------------------------------------------------- 3-5. MESSAGES
    for k, (pid, photo, text) in enumerate(PARAS):
        a_, b_ = T[1 + k] - HALF, T[2 + k] + HALF
        st = T[1 + k]
        scenes.append(f"""
      <div id="s-{pid}" class="scene clip" data-start="{a_}" data-duration="{round(b_ - a_, 2)}" data-track-index="3">
        {hero(f"hero-{pid}", 360, 90, f"assets/footage/{photo}.jpg", a_, b_, z=-180)}
        <div id="{pid}" class="card"><div class="bar"></div><div class="tx">{words(text)}</div></div>
      </div>""")
        sgn = (1, -1, 1)[k]
        tl += [
            f'tl.fromTo("#hero-{pid}-m", {{scale: 1.16, xPercent: 0}}, {{scale: 1.0, xPercent: {-2 * sgn}, duration: {b_ - a_:.2f}, ease: "none"}}, {a_});',
            f'tl.fromTo("#{pid}", {{z: -500, rotationX: 24, rotationY: {-18 * sgn}, y: 120, opacity: 0}}, {{z: 40, rotationX: 4, rotationY: {-5 * sgn}, y: 0, opacity: 1, duration: 1.1, ease: "expo.out", immediateRender: false}}, {st + 0.05});',
            f'tl.to("#{pid}", {{z: 90, rotationX: -2, rotationY: {4 * sgn}, duration: {b_ - st - 1.2:.2f}, ease: "sine.inOut"}}, {st + 1.15});',
            f'tl.from("#{pid} .bar", {{scaleY: 0, duration: 0.7, ease: "power3.out"}}, {st + 0.45});',
            f'tl.fromTo("#{pid} .tx .w", {{rotationX: -90, opacity: 0}}, {{rotationX: 0, opacity: 1, duration: 0.5, stagger: 0.04, ease: "back.out(1.4)", immediateRender: false}}, {st + 0.55});',
        ]

    # ---------------------------------------------------------------- 6. END
    a6 = T[4] - HALF
    scenes.append(f"""
      <div id="s6" class="scene">
        {hero("hero3", 700, 150, "assets/footage/drone30.mp4", a6, DURATION, vstart=round(a6 + 0.1, 2), z=-140)}
        <div class="lock clip" style="top:850px;bottom:auto" data-start="{a6}" data-duration="{round(DURATION - a6, 2)}" data-track-index="3" id="lock2">
          <div class="mask"><div id="e-ar" class="ar">{GREETING}</div></div>
          <div class="big">{letters("JUMAAT", "x-blue", "c3")}</div>
          <div class="sub">{letters("YANG DIBERKATI", "x-red", "c4")}</div>
          <div id="e-rule" class="rule"></div>
          <div class="sheen" id="sheen2"></div>
        </div>
        <div id="star-end-wrap" class="clip persp" data-start="{a6}" data-duration="{round(DURATION - a6, 2)}" data-track-index="4">
          <div id="star2" class="star3d" style="left:760px;top:900px;width:200px;height:200px">{extruded_star("st2", 200, 12)}</div>
        </div>
      </div>""")
    a = T[4]
    tl += [
        f'tl.fromTo("#hero3-m", {{scale: 1.08}}, {{scale: 1.0, duration: {DURATION - a6:.2f}, ease: "none"}}, {a6});',
        f'tl.from("#e-ar", {{yPercent: 110, duration: 0.6, ease: "power3.out"}}, {a + 0.5});',
        f'tl.fromTo(".c3", {{rotationX: -100, z: -160, opacity: 0}}, {{rotationX: 0, z: 0, opacity: 1, duration: 0.7, stagger: 0.06, ease: "back.out(1.6)", immediateRender: false}}, {a + 0.65});',
        f'tl.fromTo(".c4", {{rotationX: -100, z: -120, opacity: 0}}, {{rotationX: 0, z: 0, opacity: 1, duration: 0.55, stagger: 0.03, ease: "back.out(1.6)", immediateRender: false}}, {a + 1.0});',
        f'tl.from("#e-rule", {{scaleX: 0, duration: 0.6, ease: "power2.out"}}, {a + 1.35});',
        f'tl.to("#sheen2", {{x: "240%", duration: 1.2, ease: "power2.inOut"}}, {a + 1.8});',
        f'tl.fromTo("#star2", {{z: -900, rotationY: -270, rotationX: 30, opacity: 0}}, {{z: 60, rotationY: 0, rotationX: 10, opacity: 1, duration: 1.4, ease: "expo.out", immediateRender: false}}, {a + 0.9});',
        f'tl.to("#star2", {{rotationY: 360, duration: {DURATION - a - 2.3:.2f}, ease: "none"}}, {a + 2.3});',
        f'tl.fromTo("#lock2", {{z: 0, rotationY: 0}}, {{z: 70, rotationY: -6, duration: {DURATION - a - 1.5:.2f}, ease: "sine.inOut", immediateRender: false}}, {a + 1.5});',
        'tl.fromTo("#fade", {opacity: 0}, {opacity: 1, duration: 0.8, ease: "power1.in"}, 41.2);',
    ]

    # ---------------------------------------------------------------- camera + cube transitions
    order = ["#s1", "#s2", "#s-p1", "#s-p2", "#s-p3", "#s6"]
    tl += [
        'tl.fromTo([".scene", ".persp"], {perspectiveOrigin: "40% 42%"}, {perspectiveOrigin: "60% 50%", duration: 7, yoyo: true, repeat: 5, ease: "sine.inOut"}, 0);',
        'tl.fromTo("#s1", {z: -200}, {z: 0, duration: 2.2, ease: "power3.out"}, 0);',
        'tl.fromTo("#tex-r", {x: 0, y: 0}, {x: -60, y: -120, duration: 42, ease: "none"}, 0);',
    ]
    for i, t in enumerate(T):
        s = round(t - HALF, 2)
        out_, in_ = order[i], order[i + 1]
        tl += [
            f'tl.fromTo("{out_}", {{rotationY: 0}}, {{rotationY: -90, duration: {2 * HALF}, ease: "power2.inOut", immediateRender: false}}, {s});',
            f'tl.fromTo("{in_}", {{rotationY: 90}}, {{rotationY: 0, duration: {2 * HALF}, ease: "power2.inOut", immediateRender: false}}, {s});',
            f'tl.to("{out_}", {{z: -220, duration: {HALF}, ease: "power2.in"}}, {s});',
            f'tl.fromTo("{in_}", {{z: -220}}, {{z: 0, duration: {2 * HALF + 0.2}, ease: "power3.inOut", immediateRender: false}}, {s});',
            f'tl.fromTo(["#stk-r", "#stk-b"], {{x: 1500, z: 300}}, {{x: -1900, z: 300, duration: 0.7, stagger: 0.06, ease: "power2.inOut", immediateRender: false}}, {round(t - 0.35, 2)});',
        ]
    # HUD intro
    tl += [
        'tl.from("#tab", {y: -170, rotationX: -90, transformOrigin: "50% 0%", duration: 0.9, ease: "back.out(1.4)"}, 1.0);',
        'tl.from(["#sh1", "#sh2", "#sh3"], {y: 170, duration: 0.8, stagger: 0.07, ease: "expo.out"}, 0.4);',
        f'tl.fromTo("#tab", {{rotationY: 0}}, {{rotationY: 360, duration: 1.2, ease: "power3.inOut", immediateRender: false}}, {T[4] + 1.2});',
    ]

    html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1350" />
    <!-- GENERATED by build/compose.py: edit that, not this file. -->
    <script src="vendor/gsap.min.js"></script>
    <style>{CSS.replace("__EXB__", EXTRUDE_BLUE).replace("__EXR__", EXTRUDE_RED)}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1350">
      <div id="bg" class="clip persp">
        <div class="clip" style="transform:translateZ(-600px) scale(1.42)">{texture}</div>
        {"".join(toks)}
      </div>
      {"".join(scenes)}
      <div id="streaks" class="clip persp"><div id="stk-r" class="streak" style="width:160px;background:#ec1c24;transform:translateX(1500px) skewX(-20deg)"></div>
        <div id="stk-b" class="streak" style="width:320px;background:#2b3990;transform:translateX(1500px) skewX(-20deg)"></div></div>
      <div id="hud" class="clip layer" style="z-index:20;perspective:900px">
        <div id="sh3" class="shard"></div><div id="sh1" class="shard"></div><div id="sh2" class="shard"></div>
        <div id="tab"><img src="assets/img/mcorp-logo.png" alt="MCORP Perbadanan Melaka" /></div>
      </div>
      <div id="fade" class="clip layer" style="z-index:40"></div>
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


build()
