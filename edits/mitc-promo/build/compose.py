"""Generate the MITC Melaka 30s promo: hf/index.html (16:9, 1920x1080) and hf-vertical/index.html
(9:16, 1080x1920) from one edit decision list. Concept: "WHERE BIG IDEAS BECOME BIG EVENTS."

Structure follows the client storyboard: hook -> brand -> scale -> benefits -> experience -> closing.
All pictures are real MITC photos from the official media library (build/prep_photos.sh).
Music: 120 BPM, every cut on a beat (0.5s grid); scene changes on bar lines (build/make_music.py).
Usage: python3 compose.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DURATION = 30.0

FORMATS = {
    "hf": dict(W=1920, H=1080, key=0),
    "hf-vertical": dict(W=1080, H=1920, key=1),
}

# id, photo, start, dur, focal (16:9, 9:16) in % of the image, scale a->b, x-drift a->b (% of frame), ease, entry
SHOTS = [
    # SCENE 01 THE HOOK (0-4): black, building zoom, stage lights, halls, text
    ("h1", "building", 0.5, 1.0, ((52, 55), (61, 62)), ((1.0, 1.55), (1.0, 1.22)), (0, 0), "power3.in", "flash"),
    ("h2", "stage1", 1.5, 0.5, ((50, 42), (50, 42)), (1.15, 1.25), (0, 0), "none", "punch"),
    ("h3", "gala1", 2.0, 0.5, ((50, 50), (50, 40)), (1.12, 1.22), (0, 0), "none", "punch"),
    ("h4", "stage2", 2.5, 0.5, ((50, 40), (55, 40)), (1.15, 1.25), (0, 0), "none", "punch"),
    ("h5", "gala2", 3.0, 1.0, ((50, 42), (50, 40)), (1.05, 1.16), (0, 0), "none", "punch"),
    # SCENE 03 THINK BIGGER (8-13)
    ("a1", "aerial", 8.0, 2.0, ((55, 52), (42, 55)), (1.0, 1.32), (0, 0), "power1.in", "flash"),
    ("a2", "hallempty", 10.0, 2.75, ((50, 55), (50, 55)), (1.06, 1.2), (0, 0), "none", "punch"),
    # SCENE 04 MORE THAN A VENUE (13-18)
    ("b1", "expo", 13.0, 1.0, ((50, 45), (30, 45)), (1.15, 1.25), (0, 0), "none", "swipe"),
    ("b2", "auditorium", 14.0, 1.0, ((50, 50), (50, 55)), (1.6, 1.08), (0, 0), "expo.out", "punch"),
    ("b3", "ballroom", 15.0, 1.0, ((50, 50), (50, 50)), (1.1, 1.2), (0, 0), "none", "punch"),
    ("b4", "meeting", 16.0, 2.0, ((50, 50), (50, 50)), (1.22, 1.22), (-4, 4), "none", "punch"),
    # SCENE 05 FEEL THE EXPERIENCE (18-24)
    ("c1", "banquet", 18.0, 1.0, ((50, 50), (50, 50)), (1.05, 1.16), (0, 0), "none", "flash"),
    ("c2", "expo2", 19.0, 1.0, ((50, 40), (40, 40)), (1.1, 1.2), (0, 0), "none", "punch"),
    ("c3", "boardroom", 20.0, 1.0, ((50, 50), (40, 50)), (1.16, 1.04), (0, 0), "none", "punch"),
    ("c4", "gala3", 21.0, 1.0, ((50, 34), (50, 34)), (1.0, 1.4), (0, 0), "expo.in", "punch"),  # speed ramp
    ("c5", "stage1", 22.0, 0.5, ((50, 40), (50, 40)), (1.45, 1.18), (0, 0), "expo.out", "blur"),  # match cut on the stage
    ("c6", "gala2", 22.5, 0.25, ((50, 42), (50, 40)), (1.1, 1.16), (0, 0), "none", "punch"),
    ("c7", "show", 22.75, 0.25, ((50, 45), (50, 45)), (1.1, 1.16), (0, 0), "none", "punch"),
    ("c8", "gala1", 23.0, 0.25, ((50, 50), (50, 40)), (1.15, 1.2), (0, 0), "none", "punch"),
    ("c9", "stage2", 23.25, 0.25, ((50, 40), (55, 40)), (1.2, 1.26), (0, 0), "none", "punch"),
    # SCENE 06 THE POWERFUL CLOSING (24-30)
    ("d1", "facade", 24.0, 6.0, ((42, 45), (30, 45)), (1.0, 1.13), (0, 0), "none", "flash"),
]

SPACES = [  # scene 04 labels (spaces confirmed by the MITC poster and photographed in the gallery)
    (13.12, "DEWAN PAMERAN", "Exhibition Hall"),
    (14.12, "AUDITORIUM", "Auditorium"),
    (15.12, "BALLROOM", "Ballroom"),
    (16.12, "BILIK MESYUARAT", "Meeting Room"),
]
CARDS = [  # poster copy
    ("teal", "building", "VERSATILE", "EVENT SPACES"),
    ("navy", "badge", "PROFESSIONAL", "FACILITIES"),
    ("teal", "doc", "INTEGRATED", "EVENT SERVICES"),
]

ICONS = {
    "building": '<path d="M6 30 L32 14 L58 30 Z"/><path d="M10 30 h44 M12 34 v20 M22 34 v20 M32 34 v20 M42 34 v20 M52 34 v20 M6 56 h52"/>',
    "badge": '<circle cx="24" cy="22" r="9"/><path d="M10 50 c0-10 6-15 14-15 s14 5 14 15"/><circle cx="46" cy="38" r="9"/>'
             '<path d="M42 38 l3 3 6-6 M40 46 l-3 12 9-5 9 5 -3-12"/>',
    "doc": '<path d="M14 6 h24 l12 12 v40 h-36 Z M38 6 v12 h12"/><path d="M20 26 h20 M20 34 h14"/><circle cx="40" cy="44" r="8"/><path d="M46 50 l10 10"/>',
}

CSS = """
@font-face { font-family: "Montserrat"; font-weight: 300; src: url(assets/fonts/Montserrat-300.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 500; src: url(assets/fonts/Montserrat-500.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 600; src: url(assets/fonts/Montserrat-600.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 700; src: url(assets/fonts/Montserrat-700.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 800; src: url(assets/fonts/Montserrat-800.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 900; src: url(assets/fonts/Montserrat-900.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 800; font-style: italic; src: url(assets/fonts/Montserrat-800i.ttf); }
/* MITC poster palette */
:root { --navy: #263353; --navy-d: #141c33; --teal: #21798b; --gold: #e8bc38; --white: #fff; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: __W__px; height: __H__px; overflow: hidden; background: #000; }
#root { position: relative; width: __W__px; height: __H__px; overflow: hidden; background: #000; color: #fff; font-family: Montserrat, sans-serif; }
.clip { position: absolute; inset: 0; }
.layer { position: absolute; inset: 0; pointer-events: none; }
.shot { overflow: hidden; }
.shot img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; will-change: transform, filter; }
.mask { display: block; overflow: hidden; }
.mask > span, .mask > div { display: block; }
.ch { display: inline-block; }
.gold { color: var(--gold); }
.goldline { height: 4px; background: linear-gradient(90deg, rgba(232,188,56,0), var(--gold) 20%, #fff3c4 50%, var(--gold) 80%, rgba(232,188,56,0)); }

#vignette { background: radial-gradient(ellipse at 50% 48%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%); z-index: 60; }
#flash { background: #fff; opacity: 0; z-index: 70; }
#black { background: #000; z-index: 69; opacity: 0; }
#black0 { background: #000; z-index: 69; }

/* scene 01 text */
#hook-scrim { background: radial-gradient(ellipse at 50% 50%, rgba(20,28,51,0.55), rgba(10,14,28,0.85)); opacity: 0; z-index: 20; }
#g-hook { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 21; }
.hk1, .hk2, .xp, #e-head .l { white-space: nowrap; }
.hk1 { font-weight: 900; font-size: __HK1__px; letter-spacing: 0.04em; line-height: 1.0; }
.hk2 { font-weight: 900; font-size: __HK2__px; letter-spacing: 0.02em; line-height: 1.05; color: var(--gold); margin-top: 14px; }

/* scene 02 brand */
#brand { background: radial-gradient(ellipse 70% 60% at 50% 42%, #33456f 0%, var(--navy) 45%, var(--navy-d) 100%); z-index: 30; }
.beam { position: absolute; left: -40%; width: 180%; height: 2px; background: linear-gradient(90deg, rgba(232,188,56,0), rgba(232,188,56,0.9) 45%, #fff6d0 50%, rgba(232,188,56,0.9) 55%, rgba(232,188,56,0)); }
#flare { position: absolute; left: 50%; top: __LOGO_CY__px; width: 900px; height: 900px; margin: -450px 0 0 -450px; border-radius: 50%;
  background: radial-gradient(circle, rgba(255,246,208,0.95) 0%, rgba(232,188,56,0.55) 18%, rgba(232,188,56,0) 60%); mix-blend-mode: screen; }
.orbit { position: absolute; left: 50%; top: __LOGO_CY__px; border: 2px solid rgba(33,121,139,0.55); border-radius: 50%; }
#b-logo { position: absolute; left: 50%; top: __LOGO_CY__px; width: __LOGO__px; height: __LOGO__px; margin: -__LOGO_H__px 0 0 -__LOGO_H__px; object-fit: contain;
  filter: drop-shadow(0 20px 40px rgba(0,0,0,0.45)); }
#b-name { position: absolute; left: 0; right: 0; top: __NAME_Y__px; text-align: center; font-weight: 900; font-size: __NAME__px; letter-spacing: 0.08em; }
#b-words { position: absolute; left: 0; right: 0; top: __WORDS_Y__px; display: flex; flex-direction: __WDIR__; align-items: center; justify-content: center; gap: __WGAP__px;
  font-weight: 700; font-size: __WORDS__px; letter-spacing: 0.18em; }
#b-words .dot { width: 10px; height: 10px; border-radius: 50%; background: var(--teal); display: __DOT__; }

/* scene 03 title */
#t-scrim { background: __TSCRIM__; z-index: 20; opacity: 0; }
#t-block { position: absolute; __TPOS__ z-index: 21; }
#t-main { font-weight: 900; font-size: __TMAIN__px; line-height: 1.04; letter-spacing: 0.005em; text-shadow: 0 6px 30px rgba(0,0,0,0.35); }
#t-sub { font-weight: 800; font-style: italic; font-size: __TSUB__px; color: var(--gold); margin-top: 22px; letter-spacing: 0.01em; }
#t-line { width: __TLINE__px; margin-top: 26px; transform-origin: 0 50%; }

/* scene 04 labels + cards */
.chip { position: absolute; __CHIP_POS__ z-index: 22; display: flex; align-items: stretch; }
.chip .bar { width: 8px; background: var(--gold); }
.chip .bd { background: rgba(20,28,51,0.88); padding: 14px 26px 14px 20px; }
.chip .k { font-weight: 800; font-size: __CHIPK__px; letter-spacing: 0.12em; }
.chip .e { font-weight: 500; font-size: __CHIPE__px; color: rgba(255,255,255,0.75); margin-top: 2px; letter-spacing: 0.04em; }
#cards-scrim { background: rgba(20,28,51,0.72); opacity: 0; z-index: 23; }
#cards { position: absolute; __CARDS_POS__ display: flex; flex-direction: __CDIR__; gap: __CGAP__px; z-index: 24; }
.card { width: __CW__px; display: flex; align-items: center; gap: 26px; padding: 30px 34px; border-radius: 22px; box-shadow: 0 24px 50px rgba(0,0,0,0.4), 10px -10px 0 rgba(255,255,255,0.12); }
.card.teal { background: var(--teal); } .card.navy { background: var(--navy); border: 2px solid rgba(255,255,255,0.15); }
.card svg { width: __ICON__px; height: __ICON__px; flex: none; fill: none; stroke: #fff; stroke-width: 3; stroke-linejoin: round; stroke-linecap: round; }
.card .l1 { font-weight: 300; font-size: __CL1__px; letter-spacing: 0.06em; }
.card .l2 { font-weight: 900; font-size: __CL2__px; letter-spacing: 0.02em; line-height: 1.05; }

/* scene 05 text */
.xp { position: absolute; left: 0; right: 0; __XP_POS__ text-align: center; z-index: 22; font-weight: 900; font-size: __XP__px; letter-spacing: 0.02em;
  text-shadow: 0 6px 30px rgba(0,0,0,0.6); }
#xp-scrim { background: __XPSCRIM__; z-index: 20; opacity: 0; }

/* scene 06 closing */
#d-grade { background: linear-gradient(180deg, rgba(232,160,60,0.18), rgba(20,28,51,0.1) 50%, rgba(20,28,51,0.35)); mix-blend-mode: soft-light; z-index: 15; }
#d-scrim { background: __DSCRIM__; opacity: 0; z-index: 20; }
#d-flare { position: absolute; width: 1200px; height: 1200px; __DFLARE__ border-radius: 50%; z-index: 19; mix-blend-mode: screen; opacity: 0;
  background: radial-gradient(circle, rgba(255,230,170,0.75) 0%, rgba(232,188,56,0.25) 25%, rgba(232,188,56,0) 60%); }
#e-head { position: absolute; left: 0; right: 0; top: __EHEAD_Y__px; text-align: center; z-index: 22; transform-origin: 50% 0; }
#e-head .l { font-weight: 900; font-size: __EHEAD__px; line-height: 1.02; letter-spacing: 0.03em; text-shadow: 0 8px 40px rgba(0,0,0,0.55); }
#e-logo { position: absolute; left: 50%; top: __ELOGO_Y__px; width: __ELOGO__px; height: __ELOGO__px; margin-left: -__ELOGO_H__px; object-fit: contain; z-index: 22;
  filter: drop-shadow(0 16px 30px rgba(0,0,0,0.5)); }
#e-line { position: absolute; left: 50%; top: __ELINE_Y__px; width: __ELINE__px; margin-left: -__ELINE_H__px; z-index: 22; }
#e-name { position: absolute; left: 0; right: 0; top: __ENAME_Y__px; text-align: center; z-index: 22; font-weight: 900; font-size: __ENAME__px; letter-spacing: 0.1em; }
#e-sub { position: absolute; left: __ESUB_X__px; right: __ESUB_X__px; top: __ESUB_Y__px; text-align: center; z-index: 22; font-weight: 800; font-style: italic; font-size: __ESUB__px; color: var(--gold); line-height: 1.3; }
"""

LAYOUT = [
    dict(  # 16:9
        HK1=150, HK2=104, LOGO_CY=360, LOGO=360, NAME_Y=580, NAME=118, WORDS_Y=740, WORDS=34, WDIR="row", WGAP=30, DOT="block",
        TSCRIM="linear-gradient(90deg, rgba(20,28,51,0.88) 0%, rgba(20,28,51,0.55) 50%, rgba(20,28,51,0) 80%)",
        TPOS="left: 110px; bottom: 120px; right: 200px;", TMAIN=78, TSUB=36, TLINE=260,
        CHIP_POS="left: 90px; bottom: 90px;", CHIPK=30, CHIPE=20,
        CARDS_POS="left: 0; right: 0; top: 400px; justify-content: center;", CDIR="row", CGAP=36, CW=570, ICON=96, CL1=28, CL2=46,
        XP_POS="bottom: 120px;", XP=88, XPSCRIM="linear-gradient(0deg, rgba(10,14,28,0.85) 0%, rgba(10,14,28,0.3) 40%, rgba(10,14,28,0) 65%)",
        DSCRIM="radial-gradient(ellipse 70% 80% at 50% 50%, rgba(20,28,51,0.82), rgba(10,14,28,0.92))", DFLARE="right: -300px; top: -400px;",
        EHEAD_Y=360, EHEAD=150, ELOGO_Y=270, ELOGO=300, ELINE_Y=600, ELINE=520, ENAME_Y=630, ENAME=86, ESUB_X=200, ESUB_Y=760, ESUB=36,
        HEAD_Y_END=-250, HEAD_S_END=0.48,
    ),
    dict(  # 9:16
        HK1=128, HK2=104, LOGO_CY=700, LOGO=520, NAME_Y=1020, NAME=120, WORDS_Y=1220, WORDS=40, WDIR="column", WGAP=22, DOT="none",
        TSCRIM="linear-gradient(0deg, rgba(20,28,51,0.92) 0%, rgba(20,28,51,0.6) 45%, rgba(20,28,51,0) 75%)",
        TPOS="left: 80px; right: 80px; bottom: 260px;", TMAIN=92, TSUB=40, TLINE=240,
        CHIP_POS="left: 70px; bottom: 300px;", CHIPK=40, CHIPE=26,
        CARDS_POS="left: 0; right: 0; top: 520px; align-items: center;", CDIR="column", CGAP=40, CW=860, ICON=110, CL1=34, CL2=54,
        XP_POS="bottom: 330px;", XP=82, XPSCRIM="linear-gradient(0deg, rgba(10,14,28,0.88) 0%, rgba(10,14,28,0.35) 40%, rgba(10,14,28,0) 65%)",
        DSCRIM="linear-gradient(180deg, rgba(20,28,51,0.75), rgba(10,14,28,0.92))", DFLARE="right: -500px; top: -300px;",
        EHEAD_Y=700, EHEAD=100, ELOGO_Y=660, ELOGO=440, ELINE_Y=1140, ELINE=520, ENAME_Y=1180, ENAME=110, ESUB_X=90, ESUB_Y=1340, ESUB=44,
        HEAD_Y_END=-430, HEAD_S_END=0.62,
    ),
]


def letters(text, cls):
    return "".join(f'<span class="ch {cls}">{c}</span>' if c != " " else '<span class="ch">&nbsp;</span>' for c in text)


def build(name, fmt):
    W, H, key = fmt["W"], fmt["H"], fmt["key"]
    L = LAYOUT[key]
    css = CSS.replace("__W__", str(W)).replace("__H__", str(H))
    for k, v in sorted(L.items(), key=lambda kv: -len(kv[0])):
        css = css.replace(f"__{k}__", str(v))
    css = css.replace("__LOGO_H__", str(L["LOGO"] // 2)).replace("__ELOGO_H__", str(L["ELOGO"] // 2)).replace("__ELINE_H__", str(L["ELINE"] // 2))
    tl, html = [], []

    # ---------------------------------------------------------------- picture
    for z, (sid, photo, t, d, focal, sc, (x0, x1), ease, entry) in enumerate(SHOTS):
        fx, fy = focal[key]
        s0, s1 = sc[key] if isinstance(sc[0], tuple) else sc
        html.append(f'<div id="sh-{sid}" class="clip shot" data-start="{t}" data-duration="{d}" data-track-index="{z % 2}" style="z-index:1">'
                    f'<img id="im-{sid}" src="assets/photos/{photo}.jpg" alt="" style="object-position:{fx}% {fy}%;transform-origin:{fx}% {fy}%" /></div>')
        tl.append(f'tl.fromTo("#im-{sid}", {{scale: {s0}, xPercent: {x0}}}, {{scale: {s1}, xPercent: {x1}, duration: {d}, ease: "{ease}"}}, {t});')
        if entry == "punch":
            tl.append(f'tl.fromTo("#im-{sid}", {{filter: "brightness(1.4) blur(5px)"}}, {{filter: "brightness(1) blur(0px)", duration: 0.2, ease: "power2.out", immediateRender: false}}, {t});')
        elif entry == "blur":
            tl.append(f'tl.fromTo("#im-{sid}", {{filter: "brightness(1.2) blur(16px)"}}, {{filter: "brightness(1) blur(0px)", duration: 0.35, ease: "power3.out", immediateRender: false}}, {t});')
        elif entry == "swipe":
            tl.append(f'tl.fromTo("#sh-{sid}", {{xPercent: 100, filter: "blur(14px)"}}, {{xPercent: 0, filter: "blur(0px)", duration: 0.32, ease: "power3.out", immediateRender: false}}, {t});')
        elif entry == "flash":
            tl.append(f'tl.fromTo("#flash", {{opacity: 0.85}}, {{opacity: 0, duration: 0.4, ease: "power2.out", immediateRender: false}}, {t});')

    # hook: black open, dramatic zoom; aerial 3D dolly (parallax with the gold particles); whip pan 12.75;
    # speed-ramp blur into the match cut; dip to black 23.5-24 with the music stop
    tl += [
        'tl.to("#black0", {opacity: 0, duration: 0.08}, 0.5);',
        'tl.fromTo("#im-h1", {filter: "blur(0px)"}, {filter: "blur(6px)", duration: 0.25, ease: "power2.in", immediateRender: false}, 1.25);',
        'tl.fromTo("#sh-a1", {transformPerspective: 1400, rotationX: 16}, {rotationX: 3, duration: 2.0, ease: "power1.out", immediateRender: false}, 8.0);',
        'tl.fromTo("#sh-a2", {xPercent: 0, filter: "blur(0px)"}, {xPercent: -35, filter: "blur(18px)", duration: 0.25, ease: "power3.in", immediateRender: false}, 12.75);',
        'tl.fromTo("#im-c4", {filter: "blur(0px)"}, {filter: "blur(10px)", duration: 0.3, ease: "power3.in", immediateRender: false}, 21.7);',
        'tl.fromTo("#black", {opacity: 0}, {opacity: 1, duration: 0.15, ease: "power1.in", immediateRender: false}, 23.5);',
        'tl.to("#black", {opacity: 0, duration: 0.12}, 24.0);',
    ]

    # ---------------------------------------------------------------- SCENE 01 text
    html.append(f"""
      <div id="hook-scrim" class="clip layer" data-start="2.45" data-duration="1.55" data-track-index="5"></div>
      <div id="g-hook" class="clip layer" data-start="2.45" data-duration="1.55" data-track-index="6">
        <div class="hk1">{letters("ONE VENUE.", "k1")}</div>
        <div class="hk2">{letters("ENDLESS" if key else "ENDLESS POSSIBILITIES.", "k2")}{"<br/>" + letters("POSSIBILITIES.", "k2") if key else ""}</div>
      </div>""")
    tl += [
        'tl.fromTo("#hook-scrim", {opacity: 0}, {opacity: 1, duration: 0.2}, 2.45);',
        'tl.fromTo(".k1", {scale: 2.2, opacity: 0, filter: "blur(10px)"}, {scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.32, stagger: 0.025, ease: "power3.out"}, 2.5);',
        'tl.fromTo(".k2", {y: 60, opacity: 0}, {y: 0, opacity: 1, duration: 0.3, stagger: 0.018, ease: "back.out(2)"}, 3.0);',
        'tl.to("#g-hook", {scale: 1.25, opacity: 0, filter: "blur(10px)", duration: 0.25, ease: "power2.in"}, 3.72);',
    ]

    # ---------------------------------------------------------------- SCENE 02 brand
    words = ["PERSIDANGAN", "PAMERAN", "ACARA KORPORAT"]
    wd = "".join((f'<i class="dot"></i>' if i else "") + f'<span id="bw{i}">{w}</span>' for i, w in enumerate(words))
    beams = "".join(f'<div class="beam" id="bm{i}" style="top:{y}px"></div>' for i, y in enumerate((L["LOGO_CY"] - 210, L["LOGO_CY"] + 30, L["LOGO_CY"] + 250)))
    cy = L["LOGO_CY"]
    orbits = "".join(f'<div class="orbit" id="ob{i}" style="width:{r * 2}px;height:{r * 0.7:.0f}px;margin:{-r * 0.35:.0f}px 0 0 {-r}px"></div>' for i, r in enumerate((L["LOGO"] * 0.85, L["LOGO"] * 1.15)))
    html.append(f"""
      <div id="brand" class="clip layer" data-start="3.95" data-duration="4.1" data-track-index="7">
        {beams}{orbits}
        <div id="flare"></div>
        <img id="b-logo" src="assets/img/mitc-logo.png" alt="MITC Melaka International Trade Centre" />
        <div id="b-name">{letters("MITC MELAKA", "bn")}</div>
        <div id="b-words">{wd}</div>
      </div>""")
    tl += [
        'tl.fromTo("#brand", {clipPath: "inset(0% 0% 0% 100%)"}, {clipPath: "inset(0% 0% 0% 0%)", duration: 0.25, ease: "power3.out"}, 3.95);',
        'tl.fromTo(".beam", {xPercent: -60, opacity: 0}, {xPercent: 30, opacity: 1, duration: 1.2, stagger: 0.12, ease: "power2.out"}, 4.0);',
        'tl.to(".beam", {opacity: 0.35, duration: 1.0}, 5.3);',
        'tl.fromTo("#flare", {scale: 0.1, opacity: 0}, {scale: 1.3, opacity: 1, duration: 0.45, ease: "power3.out"}, 4.35);',
        'tl.to("#flare", {scale: 0.7, opacity: 0.35, duration: 1.2, ease: "power2.out"}, 4.8);',
        'tl.fromTo("#b-logo", {scale: 0.55, opacity: 0, filter: "brightness(3) blur(18px)"}, {scale: 1, opacity: 1, filter: "brightness(1) blur(0px)", duration: 0.75, ease: "expo.out"}, 4.5);',
        'tl.fromTo("#b-logo", {rotation: -8}, {rotation: 0, duration: 1.4, ease: "power2.out", immediateRender: false}, 4.5);',
        'tl.fromTo(".orbit", {scale: 0.4, opacity: 0, rotation: -20}, {scale: 1, opacity: 1, rotation: 10, duration: 1.4, stagger: 0.12, ease: "power3.out"}, 4.6);',
        'tl.fromTo(".bn", {scale: 0.2, opacity: 0}, {scale: 1, opacity: 1, duration: 0.45, stagger: 0.035, ease: "back.out(2.2)"}, 5.5);',
        *[f'tl.fromTo("#bw{i}", {{y: 30, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.35, ease: "power3.out"}}, {6.5 + 0.5 * i});' for i in range(3)],
        'tl.from("#b-words .dot", {scale: 0, duration: 0.3, stagger: 0.5, ease: "back.out(3)"}, 6.75);',
        'tl.fromTo("#b-logo", {y: 0}, {y: -14, duration: 3.0, ease: "sine.inOut", immediateRender: false}, 5.0);',
        'tl.to("#brand", {scale: 1.12, opacity: 0, duration: 0.2, ease: "power2.in"}, 7.82);',
    ]

    # ---------------------------------------------------------------- SCENE 03 particles (parallax foreground) + title
    import random
    rnd = random.Random(8)
    parts = []
    for i in range(26):
        x, y, s = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(3, 9)
        parts.append(f'<i id="pt{i}" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{s:.0f}px;height:{s:.0f}px;border-radius:50%;'
                     f'background:radial-gradient(circle,#fff6d0,rgba(232,188,56,0.7) 45%,rgba(232,188,56,0) 72%);filter:blur({0 if s < 6 else 1.5}px)"></i>')
        tl.append(f'tl.fromTo("#pt{i}", {{x: 0, y: 0, opacity: 0}}, {{x: {rnd.uniform(-300, -120):.0f}, y: {rnd.uniform(-160, -60):.0f}, opacity: {rnd.uniform(0.5, 1):.2f}, duration: 2.0, ease: "none"}}, 8.0);')
    html.append(f'<div id="particles" class="clip layer" data-start="8.0" data-duration="2.0" data-track-index="5" style="z-index:25">{"".join(parts)}</div>')
    tmain = ("PUSAT KONVENSYEN<br/>&amp; ACARA PERNIAGAAN<br/>BERTARAF<br/>ANTARABANGSA" if key else
             "PUSAT KONVENSYEN &amp; ACARA<br/>PERNIAGAAN BERTARAF ANTARABANGSA")
    tl_lines = tmain.split("<br/>")
    html.append(f"""
      <div id="t-scrim" class="clip layer" data-start="10.4" data-duration="2.6" data-track-index="5"></div>
      <div id="g-title" class="clip layer" data-start="10.5" data-duration="2.5" data-track-index="6" style="z-index:21">
        <div id="t-block">
          <div id="t-main">{"".join(f'<span class="mask"><span id="tl{i}">{l}</span></span>' for i, l in enumerate(tl_lines))}</div>
          <div class="mask"><div id="t-sub">Premier International Convention &amp; Business Events Centre</div></div>
          <div id="t-line" class="goldline"></div>
        </div>
      </div>""")
    tl += [
        'tl.fromTo("#t-scrim", {opacity: 0}, {opacity: 1, duration: 0.4}, 10.4);',
        *[f'tl.from("#tl{i}", {{yPercent: 110, duration: 0.55, ease: "power4.out"}}, {10.6 + 0.12 * i:.2f});' for i in range(len(tl_lines))],
        'tl.from("#t-sub", {yPercent: 110, duration: 0.5, ease: "power3.out"}, 11.9);',
        'tl.from("#t-line", {scaleX: 0, duration: 0.6, ease: "power2.out"}, 12.0);',
        'tl.to("#g-title", {xPercent: -30, opacity: 0, filter: "blur(10px)", duration: 0.25, ease: "power3.in"}, 12.75);',
        'tl.to("#t-scrim", {opacity: 0, duration: 0.25}, 12.75);',
    ]

    # ---------------------------------------------------------------- SCENE 04 labels + cards
    for i, (t, k, e) in enumerate(SPACES):
        end = 17.0 if i == 3 else t + 0.84
        html.append(f'<div id="chip{i}" class="chip" data-start="{t}" data-duration="{round(end - t, 2)}" data-track-index="7">'
                    f'<div class="bar"></div><div class="bd"><div class="k">{k}</div><div class="e">{e}</div></div></div>')
        tl += [f'tl.fromTo("#chip{i} .bd", {{clipPath: "inset(0% 100% 0% 0%)"}}, {{clipPath: "inset(0% 0% 0% 0%)", duration: 0.3, ease: "power3.out"}}, {t + 0.05:.2f});',
               f'tl.from("#chip{i} .bar", {{scaleY: 0, duration: 0.2, ease: "power3.out"}}, {t});']
    cards = "".join(f'<div class="card {c}" id="cd{i}"><svg viewBox="0 0 64 64">{ICONS[ic]}</svg><div><div class="l1">{a}</div><div class="l2">{b}</div></div></div>'
                    for i, (c, ic, a, b) in enumerate(CARDS))
    html.append(f"""
      <div id="cards-scrim" class="clip layer" data-start="16.8" data-duration="1.25" data-track-index="5"></div>
      <div id="g-cards" class="clip layer" data-start="16.8" data-duration="1.25" data-track-index="6" style="z-index:24"><div id="cards">{cards}</div></div>""")
    tl += [
        'tl.fromTo("#cards-scrim", {opacity: 0}, {opacity: 1, duration: 0.25}, 16.8);',
        'tl.fromTo("#im-b4", {filter: "blur(0px)"}, {filter: "blur(6px)", duration: 0.3, immediateRender: false}, 16.8);',
        *[f'tl.fromTo("#cd{i}", {{y: 120, opacity: 0, rotationX: -40, transformPerspective: 900}}, {{y: 0, opacity: 1, rotationX: 0, duration: 0.45, ease: "back.out(1.5)"}}, {16.9 + 0.12 * i:.2f});' for i in range(3)],
        *[f'tl.fromTo("#cd{i} svg", {{scale: 0.3, rotation: -30}}, {{scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2.5)", immediateRender: false}}, {17.0 + 0.12 * i:.2f});' for i in range(3)],
        'tl.to("#cards", {xPercent: -60, opacity: 0, filter: "blur(16px)", duration: 0.25, ease: "power3.in"}, 17.78);',
        'tl.to("#cards-scrim", {opacity: 0, duration: 0.2}, 17.8);',
    ]

    # ---------------------------------------------------------------- SCENE 05 text
    xp1 = "FROM STRATEGIC<br/>MEETINGS…" if key else "FROM STRATEGIC MEETINGS…"
    xp2 = "…TO GRAND-SCALE<br/>EVENTS." if key else "…TO GRAND-SCALE EVENTS."
    html.append(f"""
      <div id="xp-scrim" class="clip layer" data-start="19.3" data-duration="4.2" data-track-index="5"></div>
      <div id="xp1" class="xp" data-start="19.4" data-duration="1.55" data-track-index="6"><span class="mask"><span id="xp1t">{xp1}</span></span></div>
      <div id="xp2" class="xp gold" data-start="21.0" data-duration="2.45" data-track-index="6"><span class="mask"><span id="xp2t">{xp2}</span></span></div>""")
    tl += [
        'tl.fromTo("#xp-scrim", {opacity: 0}, {opacity: 1, duration: 0.3}, 19.3);',
        'tl.from("#xp1t", {yPercent: 105, duration: 0.5, ease: "power4.out"}, 19.45);',
        'tl.to("#xp1t", {yPercent: -105, duration: 0.3, ease: "power3.in"}, 20.65);',
        'tl.from("#xp2t", {yPercent: 105, duration: 0.5, ease: "power4.out"}, 21.05);',
        'tl.fromTo("#xp2t", {scale: 1}, {scale: 1.08, duration: 2.0, ease: "none", immediateRender: false}, 21.4);',
        'tl.to("#xp-scrim", {opacity: 0, duration: 0.2}, 23.3);',
    ]

    # ---------------------------------------------------------------- SCENE 06 closing
    html.append(f"""
      <div id="d-grade" class="clip layer" data-start="24" data-duration="6" data-track-index="5"></div>
      <div id="d-flare" data-start="24" data-duration="6" data-track-index="5" ></div>
      <div id="d-scrim" class="clip layer" data-start="24" data-duration="6" data-track-index="5"></div>
      <div id="e-head" data-start="25.9" data-duration="4.1" data-track-index="6">
        <div class="mask"><div class="l" id="eh1">{letters("YOUR EVENT.", "e1")}</div></div>
        <div class="mask"><div class="l gold" id="eh2">{letters("OUR EXPERTISE.", "e2")}</div></div>
      </div>
      <img id="e-logo" src="assets/img/mitc-logo.png" alt="MITC" data-start="26.9" data-duration="3.1" data-track-index="7" />
      <div id="e-line" class="goldline" data-start="26.9" data-duration="3.1" data-track-index="7"></div>
      <div id="e-name" data-start="27.9" data-duration="2.1" data-track-index="7">{letters("MITC MELAKA", "en")}</div>
      <div id="e-sub"  data-start="27.9" data-duration="2.1" data-track-index="7"><span class="mask"><span id="es">Premier International Convention &amp; Business Events Centre</span></span></div>""")
    L_ = L
    tl += [
        'tl.fromTo("#d-flare", {opacity: 0, scale: 0.6}, {opacity: 1, scale: 1.1, duration: 3.0, ease: "power2.out"}, 24.0);',
        'tl.fromTo("#d-scrim", {opacity: 0}, {opacity: 0.55, duration: 1.2, ease: "power1.inOut"}, 25.0);',
        'tl.to("#d-scrim", {opacity: 0.95, duration: 0.8, ease: "power1.inOut"}, 26.9);',
        'tl.fromTo(".e1", {opacity: 0, scale: 1.6, filter: "blur(12px)"}, {opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, stagger: 0.03, ease: "power3.out"}, 26.0);',
        'tl.fromTo(".e2", {opacity: 0, scale: 1.6, filter: "blur(12px)"}, {opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, stagger: 0.03, ease: "power3.out"}, 26.4);',
        f'tl.to("#e-head", {{y: {L_["HEAD_Y_END"]}, scale: {L_["HEAD_S_END"]}, duration: 0.6, ease: "power3.inOut"}}, 26.95);',
        'tl.fromTo("#e-logo", {scale: 0.5, opacity: 0, filter: "brightness(3) blur(14px)"}, {scale: 1, opacity: 1, filter: "brightness(1) blur(0px)", duration: 0.7, ease: "expo.out"}, 27.05);',
        'tl.fromTo("#e-line", {scaleX: 0}, {scaleX: 1, duration: 0.7, ease: "power2.inOut"}, 27.2);',
        'tl.fromTo(".en", {opacity: 0, y: 40}, {opacity: 1, y: 0, duration: 0.4, stagger: 0.03, ease: "back.out(1.8)"}, 28.0);',
        'tl.from("#es", {yPercent: 110, duration: 0.5, ease: "power3.out"}, 28.35);',
        'tl.fromTo("#e-logo", {y: 0}, {y: -6, duration: 2.0, ease: "sine.inOut", immediateRender: false}, 28.0);',
        'tl.fromTo("#flash", {opacity: 0.5}, {opacity: 0, duration: 0.5, ease: "power2.out", immediateRender: false}, 29.0);',
        'tl.to("#black", {opacity: 1, duration: 0.55, ease: "power1.in"}, 29.45);',
    ]

    doc = f"""<!doctype html>
<html lang="ms" data-resolution="{'portrait' if key else 'landscape'}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <!-- GENERATED by build/compose.py: edit that, not this file. -->
    <script src="vendor/gsap.min.js"></script>
    <style>{css}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="{W}" data-height="{H}">
      {chr(10).join("      " + h for h in html).strip()}
      <div id="vignette" class="clip layer"></div>
      <div id="black0" class="clip layer" data-start="0" data-duration="0.6" data-track-index="8"></div>
      <div id="black" class="clip layer"></div>
      <div id="flash" class="clip layer"></div>
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
    (HERE / name / "index.html").write_text(doc)
    print("wrote", name + "/index.html")


for name, fmt in FORMATS.items():
    build(name, fmt)
