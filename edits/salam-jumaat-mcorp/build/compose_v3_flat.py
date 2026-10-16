"""Generate hf/index.html: Salam Jumaat motion poster for MCORP, 1080x1350 (4:5 social feed), 42s.

v3 "Islamic corporate": follows MCORP's own collateral (white page, building photography, red and
blue diagonal shards, bold sans type) with Islamic touches kept restrained: a faint girih texture,
the verse in Amiri Quran, the Arabic greeting. Scenes change under a diagonal brand-shard wipe.
Copy is the client's, verbatim (paragraphs gain red emphasis on key phrases only).
v2 (blue + lanterns + mihrab arch) is kept in build/compose_v2_islamic.py.
Usage: python3 compose.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
W, H = 1080, 1350
DURATION = 42.0

AYAT = "إِنَّ اللَّهَ لَا يُغَيِّرُ مَا بِقَوْمٍ حَتَّىٰ يُغَيِّرُوا مَا بِأَنْفُسِهِمْ"
TRANSLATION = ("“Sesungguhnya Allah tidak mengubah apa yang ada pada sesuatu kaum sehingga mereka mengubah "
               "apa yang ada pada diri mereka sendiri.”")
CITATION = "Surah Ar-Ra'd, ayat 11"
GREETING = "جُمُعَة مُبَارَكَة"
T = [7.7, 17.7, 23.3, 30.1, 34.5]  # scene changes (wipe covers the frame at these instants)
PARAS = [  # id, photo, text with [[red emphasis]]
    ("p1", "f5", "Kemajuan bermula dengan [[kesungguhan untuk berubah]], [[keberanian]] melakukan penambahbaikan "
                 "dan [[komitmen]] untuk memberikan yang terbaik."),
    ("p2", "f2", "Semoga [[MCORP]] terus melangkah ke hadapan dengan [[visi yang jelas]], [[semangat berpasukan]] "
                 "dan [[iltizam]] untuk membawa manfaat kepada organisasi serta negeri Melaka."),
    ("p3", "f9", "Moga setiap perubahan ke arah kebaikan mendapat [[reda dan keberkatan Allah SWT]]."),
]

CSS = """
@font-face { font-family: "Amiri Quran"; src: url(assets/fonts/AmiriQuran-400.ttf); }
@font-face { font-family: "Amiri"; font-weight: 700; src: url(assets/fonts/Amiri-700.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 400; src: url(assets/fonts/Montserrat-400.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 500; src: url(assets/fonts/Montserrat-500.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 600; src: url(assets/fonts/Montserrat-600.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 700; src: url(assets/fonts/Montserrat-700.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 800; src: url(assets/fonts/Montserrat-800.ttf); }
/* MCORP brand (sampled from the official logo) */
:root { --blue: #2b3990; --blue-d: #1c2670; --red: #ec1c24; --ink: #1a1f45; --grey: #5a6080; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1350px; overflow: hidden; background: #fff; }
#root { position: relative; width: 1080px; height: 1350px; overflow: hidden; background: #fff; color: var(--ink); font-family: Montserrat, sans-serif; }
.clip { position: absolute; inset: 0; }
.layer { position: absolute; inset: 0; pointer-events: none; }
.mask { display: block; overflow: hidden; }
.mask > span, .mask > div { display: block; }
.mask > span.pill { display: inline-block; }
#texture { opacity: 0.07; }
#texture .ln, #texture .ln * { fill: none; stroke: var(--blue); }

/* photo panels with a diagonal bottom edge, a blue band and a thin red band along it */
.hero { position: absolute; left: 0; top: 0; width: 1080px; overflow: hidden; }
.hero video, .hero img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }
.hero .tint { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(28,38,112,0.15), rgba(28,38,112,0) 40%); }
.band { position: absolute; left: -100px; width: 1300px; transform-origin: 0 0; }
.band.b { background: var(--blue); height: 34px; }
.band.r { background: var(--red); height: 10px; }

/* corner shards (static brand furniture) */
.shard { position: absolute; transform: skewX(-32deg); }
#sh1 { right: -150px; bottom: 0; width: 330px; height: 150px; background: var(--blue); }
#sh2 { right: 120px; bottom: 0; width: 70px; height: 150px; background: var(--red); }
#sh3 { left: -80px; bottom: 0; width: 210px; height: 22px; background: var(--red); transform: skewX(-32deg); }

/* logo tab */
#tab { position: absolute; left: 0; top: 0; width: 330px; height: 150px; background: #fff; display: flex; align-items: center;
  justify-content: center; border-bottom-right-radius: 18px; box-shadow: 0 10px 30px rgba(20,30,90,0.18); }
#tab img { height: 112px; width: auto; object-fit: contain; }

/* title lockup */
.lock { position: absolute; left: 90px; right: 90px; }
.lock.clip { left: 90px; right: 90px; }
.lock .ar { font-family: "Amiri", serif; font-weight: 700; font-size: 56px; line-height: 1.3; padding-top: 0.3em; color: var(--blue); text-align: left; }
.lock .big { font-weight: 800; font-size: 150px; line-height: 0.95; letter-spacing: -0.01em; color: var(--blue); }
.lock .sub { font-weight: 700; font-size: 50px; letter-spacing: 0.1em; color: var(--red); margin-top: 10px; }
.lock .rule { width: 110px; height: 6px; background: var(--red); margin-top: 26px; transform-origin: 0 50%; }
.lock .org { font-weight: 600; font-size: 24px; letter-spacing: 0.32em; color: var(--grey); margin-top: 22px; }

/* verse */
#ayat { position: absolute; left: 70px; right: 70px; top: 330px; bottom: 190px; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.pill { display: inline-block; font-weight: 700; font-size: 22px; letter-spacing: 0.3em; color: #fff; background: var(--red); padding: 10px 18px 10px 24px; }
#ar { direction: rtl; font-family: "Amiri Quran", "Amiri", serif; font-size: 80px; line-height: 2.0; color: var(--blue); margin-top: 30px; }
#ar .w { display: inline-block; margin: 0 0.12em; }
#tr { font-weight: 500; font-size: 36px; line-height: 1.5; color: var(--ink); margin-top: 26px; }
#cite { display: flex; align-items: center; justify-content: center; gap: 18px; margin-top: 32px; font-weight: 700; font-size: 26px; letter-spacing: 0.08em; color: var(--red); }
#cite i { display: block; width: 80px; height: 3px; background: var(--red); }

/* message */
.msgwrap { position: absolute; left: 90px; right: 90px; top: 470px; bottom: 200px; display: flex; align-items: center; }
.msg { display: flex; gap: 36px; }
.msg .bar { width: 10px; background: linear-gradient(180deg, var(--red) 0 34%, var(--blue) 34% 100%); flex: none; transform-origin: 50% 0; }
.msg .tx { font-weight: 600; font-size: 54px; line-height: 1.42; color: var(--ink); }
.msg .tx .w { display: inline-block; }
.msg .tx .em { color: var(--red); font-weight: 800; }
.msg .lbl { font-weight: 700; font-size: 22px; letter-spacing: 0.32em; color: var(--blue); margin-bottom: 26px; }

/* scene-change wipe */
#wipe-in { position: absolute; inset: 0; transform: translateX(2000px); }
#wipe .wb { position: absolute; top: -10%; height: 120%; transform: skewX(-20deg); }
#wipe .w1 { left: 0; width: 240px; background: var(--red); }
#wipe .w2 { left: 240px; width: 1700px; background: var(--blue); }
#wipe .w3 { left: 1940px; width: 180px; background: var(--blue-d); }
#fade { background: #fff; opacity: 0; }
"""


def star8(cx, cy, R):
    s = R * 0.707
    return (f'<rect x="{cx - s:.1f}" y="{cy - s:.1f}" width="{2 * s:.1f}" height="{2 * s:.1f}"/>'
            f'<rect x="{cx - s:.1f}" y="{cy - s:.1f}" width="{2 * s:.1f}" height="{2 * s:.1f}" transform="rotate(45 {cx} {cy})"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{R * 0.32:.1f}"/>')


def words(text):
    out = []
    for i, part in enumerate(text.replace("]]", "[[").split("[[")):
        for w in part.split():
            if out and all(c in ",.;:!?" for c in w):
                out[-1] = (out[-1][0] + w, out[-1][1])
            else:
                out.append((w, i % 2 == 1))
    return " ".join(f'<span class="w{" em" if em else ""}">{w}</span>' for w, em in out)


def hero(hid, h, slope, media, a, b):
    """Photo/video panel of height h whose bottom edge rises `slope` px from left to right."""
    d = round(b - a, 2)
    clip = f"polygon(0 0, 100% 0, 100% {h - slope}px, 0 {h}px)"
    import math
    ang = -math.degrees(math.atan2(slope, 1080))
    bands = (f'<div class="band b" style="top:{h - 6}px;transform:rotate({ang:.3f}deg)"></div>'
             f'<div class="band r" style="top:{h + 34}px;transform:rotate({ang:.3f}deg)"></div>')
    if media.endswith(".mp4"):
        src = f'<video id="{hid}-m" class="clip" src="{media}" data-start="{a}" data-duration="{d}" data-media-start="__MS__" data-playback-rate="__RATE__" data-track-index="2" muted playsinline></video>'
    else:
        src = f'<img id="{hid}-m" src="{media}" alt="" />'
    timed = f' data-start="{a}" data-duration="{d}" data-track-index="2"' if media.endswith(".mp4") else ""
    return (f'<div id="{hid}" class="hero" style="height:{h + 60}px"><div id="{hid}-ph" style="position:absolute;inset:0;clip-path:{clip}">{src}'
            f'<div class="tint clip"{timed}></div></div><div id="{hid}-bands" class="clip"{timed}>{bands}</div></div>')


def build():
    tl = []
    texture = (f'<svg id="texture" class="clip layer" width="1080" height="1350"><defs><pattern id="g" width="120" height="120" patternUnits="userSpaceOnUse">'
               f'<g class="ln" stroke-width="1.4">{star8(60, 60, 44)}<path d="M0,0 L28,28 M120,0 L92,28 M0,120 L28,92 M120,120 L92,92"/></g></pattern>'
               f'<linearGradient id="fadeg" x1="0" y1="0" x2="0" y2="1"><stop offset="0.35" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>'
               f'<mask id="m"><rect width="1080" height="1350" fill="url(#fadeg)"/></mask></defs>'
               f'<rect id="tex-r" x="-120" y="-120" width="1320" height="1590" fill="url(#g)" mask="url(#m)"/></svg>')

    scenes = []
    # 1. HOOK / TITLE (0 - T0)
    h1 = hero("hero1", 760, 150, "assets/footage/drone.mp4", 0, T[0]).replace("__MS__", "0.0").replace("__RATE__", "0.5")
    scenes.append(f"""
      <div id="s-hook" class="clip layer">
        {h1}
        <div class="lock clip" style="top:840px;bottom:auto" data-start="0" data-duration="{T[0]}" data-track-index="3">
          <div class="mask"><div id="h-ar" class="ar">{GREETING}</div></div>
          <div class="mask"><div id="h-big" class="big">JUMAAT</div></div>
          <div class="mask"><div id="h-sub" class="sub">YANG DIBERKATI</div></div>
          <div id="h-rule" class="rule"></div>
        </div>
      </div>""")
    tl += [
        'tl.fromTo("#hero1-ph", {clipPath: "polygon(100% 0, 100% 0, 100% 610px, 100% 760px)"}, {clipPath: "polygon(0% 0, 100% 0, 100% 610px, 0% 760px)", duration: 1.0, ease: "expo.inOut"}, 0.1);',
        'tl.fromTo("#hero1-m", {scale: 1.25}, {scale: 1.0, duration: 7.6, ease: "power1.out"}, 0.1);',
        'tl.fromTo("#hero1-bands .band", {xPercent: 100}, {xPercent: 0, duration: 0.9, stagger: 0.08, ease: "expo.out"}, 0.55);',
        'tl.from("#h-ar", {yPercent: 110, duration: 0.6, ease: "power3.out"}, 1.05);',
        'tl.from("#h-big", {yPercent: 105, duration: 0.75, ease: "power4.out"}, 1.2);',
        'tl.from("#h-sub", {yPercent: 110, duration: 0.6, ease: "power3.out"}, 1.45);',
        'tl.from("#h-rule", {scaleX: 0, duration: 0.6, ease: "power2.out"}, 1.7);',
    ]
    # 2. VERSE (T0 - T1)
    ws = AYAT.split()
    ar = "".join(f'<span class="w">{w}</span>' for w in ws[:6]) + "<br/>" + "".join(f'<span class="w">{w}</span>' for w in ws[6:])
    h2 = hero("hero2", 270, 70, "assets/footage/f8.jpg", T[0], T[1])
    scenes.append(f"""
      <div id="s-ayat" class="clip layer" data-start="{T[0]}" data-duration="{round(T[1] - T[0], 2)}" data-track-index="3">
        {h2}
        <div id="ayat">
          <div class="mask"><span id="a-pill" class="pill">FIRMAN ALLAH SWT</span></div>
          <div id="ar">{ar}</div>
          <div id="tr">{TRANSLATION}</div>
          <div id="cite"><i></i><span>{CITATION}</span><i></i></div>
        </div>
      </div>""")
    a = T[0]
    tl += [
        f'tl.fromTo("#hero2-m", {{scale: 1.15}}, {{scale: 1.0, duration: {round(T[1] - a, 2)}, ease: "none"}}, {a});',
        f'tl.from("#a-pill", {{yPercent: 110, duration: 0.5, ease: "power3.out"}}, {a + 0.5});',
        f'tl.from("#ar .w", {{opacity: 0, y: 20, filter: "blur(8px)", duration: 0.6, stagger: 0.3, ease: "power2.out"}}, {a + 0.85});',
        f'tl.from("#tr", {{opacity: 0, y: 22, duration: 0.8, ease: "power2.out"}}, {a + 4.6});',
        f'tl.from("#cite", {{opacity: 0, y: 16, duration: 0.6, ease: "power2.out"}}, {a + 7.2});',
        f'tl.from("#cite i", {{scaleX: 0, duration: 0.6, ease: "power2.out"}}, {a + 7.35});',
    ]
    # 3-5. MESSAGES
    for k, (pid, photo, text) in enumerate(PARAS):
        a, b = T[1 + k], T[2 + k]
        hh = hero(f"hero-{pid}", 380, 90, f"assets/footage/{photo}.jpg", a, b)
        scenes.append(f"""
      <div id="s-{pid}" class="clip layer" data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="3">
        {hh}
        <div class="msgwrap"><div id="{pid}" class="msg"><div class="bar"></div><div class="tx">{words(text)}</div></div></div>
      </div>""")
        tl += [
            f'tl.fromTo("#hero-{pid}-m", {{scale: 1.14, xPercent: 0}}, {{scale: 1.0, xPercent: {(-2, 2, -2)[k]}, duration: {round(b - a, 2)}, ease: "none"}}, {a});',
            f'tl.from("#{pid} .bar", {{scaleY: 0, duration: 0.7, ease: "power3.out"}}, {a + 0.4});',
            f'tl.from("#{pid} .tx .w", {{opacity: 0, y: 18, duration: 0.45, stagger: 0.045, ease: "power2.out"}}, {a + 0.55});',
        ]
    # 6. END (T4 - 42)
    he = hero("hero3", 760, 150, "assets/footage/drone.mp4", T[4], DURATION).replace("__MS__", "3.6").replace("__RATE__", "0.6")
    scenes.append(f"""
      <div id="s-end" class="clip layer">
        {he}
        <div class="lock clip" style="top:840px;bottom:auto" data-start="{T[4]}" data-duration="{round(DURATION - T[4], 2)}" data-track-index="3">
          <div class="mask"><div id="e-ar" class="ar">{GREETING}</div></div>
          <div class="mask"><div id="e-big" class="big">JUMAAT</div></div>
          <div class="mask"><div id="e-sub" class="sub">YANG DIBERKATI</div></div>
          <div id="e-rule" class="rule"></div>
        </div>
      </div>""")
    a = T[4]
    tl += [
        f'tl.fromTo("#hero3-m", {{scale: 1.12}}, {{scale: 1.0, duration: {round(DURATION - a, 2)}, ease: "none"}}, {a});',
        f'tl.from("#e-ar", {{yPercent: 110, duration: 0.6, ease: "power3.out"}}, {a + 0.5});',
        f'tl.from("#e-big", {{yPercent: 105, duration: 0.75, ease: "power4.out"}}, {a + 0.65});',
        f'tl.from("#e-sub", {{yPercent: 110, duration: 0.6, ease: "power3.out"}}, {a + 0.9});',
        f'tl.from("#e-rule", {{scaleX: 0, duration: 0.6, ease: "power2.out"}}, {a + 1.1});',
        'tl.fromTo("#fade", {opacity: 0}, {opacity: 1, duration: 0.8, ease: "power1.in"}, 41.2);',
    ]

    # persistent brand furniture: logo tab + corner shards (in at the start, always on top of scenes)
    tl += [
        'tl.from("#tab", {y: -170, duration: 0.8, ease: "back.out(1.4)"}, 0.9);',
        'tl.from(["#sh1", "#sh2", "#sh3"], {y: 170, duration: 0.8, stagger: 0.07, ease: "expo.out"}, 0.3);',
        'tl.fromTo("#tex-r", {x: 0, y: 0}, {x: -60, y: -120, duration: 42, ease: "none"}, 0);',
    ]
    # diagonal brand wipes at each scene change
    for t in T:
        s = round(t - 0.55, 2)
        tl.append(f'tl.fromTo("#wipe-in", {{x: 2000}}, {{x: -2600, duration: 1.1, ease: "power3.inOut", immediateRender: false}}, {s});')

    html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1350" />
    <!-- GENERATED by build/compose.py: edit that, not this file. -->
    <script src="vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1350">
      {texture}
      {"".join(scenes)}
      <div id="brand" class="clip layer" style="z-index:20">
        <div id="sh3" class="shard"></div><div id="sh1" class="shard"></div><div id="sh2" class="shard"></div>
        <div id="tab"><img src="assets/img/mcorp-logo.png" alt="MCORP Perbadanan Melaka" /></div>
      </div>
      <div id="wipe" class="clip layer" style="z-index:30"><div id="wipe-in"><div class="wb w1"></div><div class="wb w2"></div><div class="wb w3"></div></div></div>
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
