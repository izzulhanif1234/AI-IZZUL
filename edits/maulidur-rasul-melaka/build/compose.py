"""Write the HyperFrames compositions for both deliverables from edl.py:
  hf/index.html          1920x1080  (Facebook, LinkedIn, YouTube)
  hf-vertical/index.html 1080x1920  (Instagram Reels, TikTok, Facebook Reels)
Usage: python3 compose.py
"""
import json
from pathlib import Path

import edl

HERE = Path(__file__).resolve().parent.parent
SRC_W, SRC_H = 1920, 1080

FORMATS = {
    "hf": dict(w=1920, h=1080, key="f169", vp="landscape"),
    "hf-vertical": dict(w=1080, h=1920, key="f916", vp="portrait"),
}

# Palette: deep navy of the stadium lettering, warm gold for the occasion, warm white type.
CSS = """
@font-face { font-family: "Cormorant Garamond"; font-weight: 500; src: url(assets/fonts/CormorantGaramond-500.ttf); }
@font-face { font-family: "Cormorant Garamond"; font-weight: 600; src: url(assets/fonts/CormorantGaramond-600.ttf); }
@font-face { font-family: "Cormorant Garamond"; font-weight: 700; src: url(assets/fonts/CormorantGaramond-700.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 500; src: url(assets/fonts/Montserrat-500.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 600; src: url(assets/fonts/Montserrat-600.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 700; src: url(assets/fonts/Montserrat-700.ttf); }
:root {
  --navy: #0b1d3a;
  --navy-deep: #061227;
  --gold: #d6b26a;
  --gold-soft: rgba(214, 178, 106, 0.55);
  --ivory: #fbf7ee;
  --shade: rgba(6, 18, 39, 0.78);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: __W__px; height: __H__px; overflow: hidden; background: #000; }
#root { position: relative; width: __W__px; height: __H__px; overflow: hidden; background: #000;
  font-family: Montserrat, sans-serif; color: var(--ivory); }
.clip { position: absolute; inset: 0; }
video.shot { position: absolute; width: 1920px; height: 1080px; left: __VX__px; top: __VY__px;
  object-fit: cover; will-change: transform, opacity; }
.layer { position: absolute; inset: 0; pointer-events: none; }
.kicker { font-family: Montserrat, sans-serif; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.32em; color: var(--gold); }
.serif { font-family: "Cormorant Garamond", serif; font-weight: 600; }
.mask { display: block; overflow: hidden; padding-bottom: 0.06em; }
.mask > span { display: inline-block; }
.rule { height: 2px; background: linear-gradient(90deg, var(--gold), rgba(214,178,106,0)); transform-origin: 0 50%; }
.rule.c { background: linear-gradient(90deg, rgba(214,178,106,0), var(--gold), rgba(214,178,106,0)); transform-origin: 50% 50%; }
.star { display: block; }

/* hook */
#g-hook { display: flex; flex-direction: column; align-items: center; justify-content: flex-end; padding-bottom: __HPB__px; text-align: center; }
#hook-vig { background: __HVIG__; }
#hook-kicker { font-size: __HK__px; margin-bottom: __HKM__px; }
.hook-line { font-size: __HL__px; line-height: 1.04; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em;
  text-shadow: 0 4px 30px rgba(0,0,0,0.45); }
#hook-b { color: var(--gold); }

/* title */
#title-scrim { background: __SCRIM__; }
#title-block { position: absolute; __TB_POS__ }
#title-kicker { font-size: __TK__px; }
#title-main { font-size: __TM__px; line-height: 1.0; margin-top: 18px; }
#title-level { font-size: __TL__px; font-weight: 500; letter-spacing: 0.04em; margin-top: 14px; color: #fff; }
#title-rule { width: __TRW__px; margin: 26px 0 20px; }
#title-meta { font-size: __TMETA__px; font-weight: 500; letter-spacing: 0.06em; color: rgba(251,247,238,0.86); }

/* captions */
.cap { position: absolute; inset: auto; left: 50%; __CAP_POS__ width: __CAPW__px; margin-left: -__CAPHW__px; text-align: center; }
.cap span { display: inline; font-family: Montserrat, sans-serif; font-weight: 600; font-size: __CAPF__px;
  line-height: 1.42; color: #fff; padding: 0.08em 0.38em; border-radius: 6px;
  background: rgba(6, 18, 39, 0.62); -webkit-box-decoration-break: clone; box-decoration-break: clone;
  text-shadow: 0 1px 2px rgba(0,0,0,0.35); }

/* theme lower third */
#tag { position: absolute; __TAG_POS__ display: flex; align-items: center; gap: 22px;
  padding: 18px 34px 18px 22px; background: linear-gradient(90deg, rgba(6,18,39,0.88), rgba(6,18,39,0.55));
  border-left: 3px solid var(--gold); }
#tag-k { font-size: __TAGK__px; }
#tag-t { font-size: __TAGT__px; line-height: 1.05; margin-top: 6px; }

/* closing */
#close-scrim { background: radial-gradient(ellipse at center, rgba(6,18,39,0.78) 0%, rgba(6,18,39,0.6) 55%, rgba(0,0,0,0.7) 100%); }
#g-close { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
#close-k { font-size: __CK__px; margin-bottom: 18px; }
#close-main { font-size: __CM__px; line-height: 1.0; }
#close-year { font-size: __CY__px; color: var(--gold); margin-top: 12px; letter-spacing: 0.12em; }
#close-rule { width: __CRW__px; margin: 30px auto 24px; }
#close-theme { font-size: __CT__px; font-weight: 500; letter-spacing: 0.08em; }

/* end card */
#end { background: radial-gradient(ellipse at 50% 42%, #12305e 0%, var(--navy) 45%, var(--navy-deep) 100%);
  display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
#end-pattern { opacity: 0.07; }
#end-k { font-size: __EK__px; margin: 30px 0 22px; }
#end-main { font-size: __EM__px; line-height: 1.05; max-width: __EMW__px; }
#end-level { font-size: __EL__px; font-weight: 500; letter-spacing: 0.06em; margin-top: 18px; }
#end-rule { width: __ERW__px; margin: 30px auto 24px; }
#end-meta { font-size: __EMETA__px; font-weight: 500; letter-spacing: 0.06em; color: rgba(251,247,238,0.82); }
/* Organisation logo slot: drop the official file at assets/logo.png and uncomment the <img> in the
   end card (compose.py). Kept unaltered: object-fit contain, no recolouring. */
#org-logo { height: __LOGO__px; width: auto; object-fit: contain; margin-top: 34px; }
#fade-black { background: #000; opacity: 0; }
"""

LAYOUT = {
    "hf": dict(
        VX=0, VY=0, HK=26, HKM=22, HL=104, HPB=118,
        HVIG="linear-gradient(180deg, rgba(6,18,39,0.15) 0%, rgba(6,18,39,0.2) 40%, rgba(6,18,39,0.78) 72%, rgba(6,18,39,0.9) 100%)",
        SCRIM="linear-gradient(180deg, rgba(6,18,39,0) 35%, rgba(6,18,39,0.55) 62%, rgba(6,18,39,0.9) 100%)",
        TB_POS="left: 120px; bottom: 96px;", TK=24, TM=92, TL=30, TRW=520, TMETA=25,
        CAP_POS="bottom: 74px;", CAPW=1500, CAPF=40,
        TAG_POS="left: 96px; top: 84px;", TAGK=16, TAGT=40,
        CK=24, CM=118, CY=46, CRW=420, CT=28,
        EK=22, EM=78, EMW=1300, EL=32, ERW=460, EMETA=26, LOGO=110,
    ),
    "hf-vertical": dict(
        VX=-420, VY=420, HK=28, HKM=24, HL=90, HPB=400,
        HVIG="linear-gradient(180deg, rgba(6,18,39,0.1) 0%, rgba(6,18,39,0.12) 40%, rgba(6,18,39,0.82) 57%, rgba(6,18,39,0.88) 80%, rgba(6,18,39,0.6) 100%)",
        SCRIM="linear-gradient(180deg, rgba(6,18,39,0) 30%, rgba(6,18,39,0.6) 55%, rgba(6,18,39,0.92) 100%)",
        TB_POS="left: 80px; right: 80px; bottom: 430px;", TK=24, TM=96, TL=36, TRW=420, TMETA=30,
        CAP_POS="top: 1390px;", CAPW=940, CAPF=46,
        TAG_POS="left: 64px; top: 250px;", TAGK=16, TAGT=42,
        CK=26, CM=108, CY=54, CRW=360, CT=32,
        EK=24, EM=94, EMW=940, EL=40, ERW=380, EMETA=32, LOGO=130,
    ),
}

STAR = """<svg class="star" width="{s}" height="{s}" viewBox="-50 -50 100 100" fill="none" stroke="#d6b26a" stroke-width="{sw}">
<rect x="-30" y="-30" width="60" height="60"/><rect x="-30" y="-30" width="60" height="60" transform="rotate(45)"/>
<circle r="11"/></svg>"""

PATTERN = """<svg id="end-pattern" class="layer" width="100%" height="100%"><defs>
<pattern id="geo" width="140" height="140" patternUnits="userSpaceOnUse">
<g transform="translate(70 70)" fill="none" stroke="#d6b26a" stroke-width="1.4">
<rect x="-34" y="-34" width="68" height="68"/><rect x="-34" y="-34" width="68" height="68" transform="rotate(45)"/>
<circle r="14"/></g></pattern></defs><rect width="100%" height="100%" fill="url(#geo)"/></svg>"""


def frame_props(fmt, f):
    """GSAP props that put source point (X, Y) at canvas centre at scale s (clamped to cover)."""
    W, H = fmt["w"], fmt["h"]
    base = max(W / SRC_W, H / SRC_H)
    X, Y, s = f
    k = base * s
    tx = k * (SRC_W / 2 - X)
    ty = k * (SRC_H / 2 - Y)
    mx, my = (k * SRC_W - W) / 2, (k * SRC_H - H) / 2
    tx, ty = max(-mx, min(mx, tx)), max(-my, min(my, ty))
    return {"x": round(tx, 2), "y": round(ty, 2), "scale": round(k, 4)}


def build(name, fmt):
    L = LAYOUT[name]
    css = CSS.replace("__W__", str(fmt["w"])).replace("__H__", str(fmt["h"]))
    for k, v in L.items():
        css = css.replace(f"__{k}__", str(v))
    css = css.replace("__CAPHW__", str(L["CAPW"] // 2))
    E = edl.EVENT
    vertical = fmt["h"] > fmt["w"]

    vids, tl = [], []
    for z, s in enumerate(edl.SHOTS):
        src = f"assets/footage/{s['src']}.mp4"
        vids.append(
            f'<video id="v-{s["id"]}" class="clip shot" src="{src}" data-start="{s["t"]}" data-duration="{s["d"]}" '
            f'data-media-start="{s["ms"]}" data-track-index="{z % 2}" style="z-index:{z + 1}" muted playsinline></video>'
        )
        a, b = (frame_props(fmt, f) for f in s[fmt["key"]])
        tl.append(f'tl.fromTo("#v-{s["id"]}", {json.dumps(a)}, {{...{json.dumps(b)}, duration: {s["d"]}, ease: "none"}}, {s["t"]});')
        if s["fade"]:
            tl.append(f'tl.fromTo("#v-{s["id"]}", {{opacity: 0}}, {{opacity: 1, duration: {s["fade"]}, ease: "sine.inOut", immediateRender: false}}, {s["t"]});')
    # hook: punch-in "zoom transition" on each beat cut
    for t in (1.2, 2.4):
        sid = next(x["id"] for x in edl.SHOTS if x["t"] == t)
        tl.append(f'tl.fromTo("#v-{sid}", {{filter: "brightness(1.35) blur(6px)"}}, {{filter: "brightness(1) blur(0px)", duration: 0.22, ease: "power2.out", immediateRender: false}}, {t});')
    tl.append('tl.fromTo("#v-wide2", {filter: "brightness(1.3) blur(8px)"}, {filter: "brightness(1) blur(0px)", duration: 0.35, ease: "power2.out", immediateRender: false}, 30.6);')

    caps = []
    for i, (a, b, text) in enumerate(edl.CAPTIONS):
        caps.append(f'<div id="cap{i}" class="clip cap" data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="5"><span>{text}</span></div>')
        tl.append(f'tl.from("#cap{i}", {{opacity: 0, y: 14, duration: 0.18, ease: "power2.out"}}, {a});')
        tl.append(f'tl.to("#cap{i}", {{opacity: 0, duration: 0.14, ease: "power1.in"}}, {round(b - 0.14, 2)});')

    hook_end, (t0, t1), (g0, g1), (c0, c1), (e0, e1) = 3.05, edl.TITLE, edl.THEME_TAG, edl.CLOSE, edl.END
    ha, hb = edl.HOOK_WORDS[0][0], edl.HOOK_WORDS[1][0]
    br = "<br/>" if vertical else " "
    theme_a = E["theme_a"].upper().replace(" ", br)
    theme_b = E["theme_b"].upper().replace(" ", br)
    title_main = E["title"].replace(" dan ", "<br/>dan ")
    end_main = "Sambutan<br/>Maulidur Rasul<br/>1448H / 2026M" if vertical else "Sambutan Maulidur Rasul<br/>1448H / 2026M"
    close_main = "Salam<br/>Maulidur Rasul" if vertical else "Salam Maulidur Rasul"

    graphics = f"""
      <div id="hook-vig" class="clip layer" data-start="0" data-duration="{hook_end}" data-track-index="3" style="z-index:20"></div>
      <div id="g-hook" class="clip layer" data-start="0" data-duration="{hook_end}" data-track-index="4" style="z-index:21">
        <div id="hook-kicker" class="kicker">Maulidur Rasul 1448H</div>
        <div class="hook-line serif mask"><span id="hook-a">{theme_a}</span></div>
        <div class="hook-line serif mask"><span id="hook-b">{theme_b}</span></div>
      </div>

      <div id="title-scrim" class="clip layer" data-start="{t0 - 0.05}" data-duration="{round(t1 - t0 + 0.4, 2)}" data-track-index="3" style="z-index:20"></div>
      <div id="g-title" class="clip layer" data-start="{t0}" data-duration="{round(t1 - t0 + 0.35, 2)}" data-track-index="4" style="z-index:21">
        <div id="title-block">
          <div class="mask"><span id="title-kicker" class="kicker">{E["kicker"]}</span></div>
          <div id="title-main" class="serif"><span class="mask"><span id="title-l1">{title_main.split("<br/>")[0]}</span></span><span class="mask"><span id="title-l2">{title_main.split("<br/>")[1]}</span></span></div>
          <div class="mask"><span id="title-level">{E["level"]}</span></div>
          <div id="title-rule" class="rule"></div>
          <div class="mask"><span id="title-meta">{E["venue"]}{"<br/>" if vertical else "&nbsp;&nbsp;·&nbsp;&nbsp;"}{E["date"]}</span></div>
        </div>
      </div>

      <div id="g-tag" class="clip layer" data-start="{g0}" data-duration="{round(g1 - g0, 2)}" data-track-index="4" style="z-index:21">
        <div id="tag">{STAR.format(s=46, sw=4)}<div><div id="tag-k" class="kicker">Tema Sambutan</div>
          <div id="tag-t" class="serif">{E["theme_a"]}, {E["theme_b"]}</div></div></div>
      </div>

      <div id="captions" class="clip layer" style="z-index:22" data-start="0" data-duration="{edl.DURATION}" data-track-index="5">{"".join(caps)}</div>

      <div id="close-scrim" class="clip layer" data-start="{c0 - 0.2}" data-duration="{round(c1 - c0 + 0.6, 2)}" data-track-index="3" style="z-index:20"></div>
      <div id="g-close" class="clip layer" data-start="{c0}" data-duration="{round(c1 - c0 + 0.4, 2)}" data-track-index="4" style="z-index:21">
        <div id="close-k" class="kicker">Selamat menyambut</div>
        <div id="close-main" class="serif"><span class="mask"><span id="close-l1">{close_main}</span></span></div>
        <div class="serif mask"><span id="close-year">1448H / 2026M</span></div>
        <div id="close-rule" class="rule c"></div>
        <div class="mask"><span id="close-theme">{E["theme_a"]}, {E["theme_b"]}</span></div>
      </div>

      <div id="end" class="clip layer" data-start="{e0}" data-duration="{round(e1 - e0, 2)}" data-track-index="6" style="z-index:30">
        {PATTERN}
        <div id="end-star">{STAR.format(s=74 if not vertical else 86, sw=3)}</div>
        <div class="mask"><span id="end-k" class="kicker">{E["title"]}</span></div>
        <div id="end-main" class="serif"><span class="mask"><span id="end-l1">{end_main}</span></span></div>
        <div class="mask"><span id="end-level">{E["level"]}</span></div>
        <div id="end-rule" class="rule c"></div>
        <div class="mask"><span id="end-meta">{E["venue"]}{"<br/>" if vertical else "&nbsp;&nbsp;·&nbsp;&nbsp;"}{E["date"]}</span></div>
        <!-- <img id="org-logo" src="assets/logo.png" alt="" /> -->
      </div>
      <div id="fade-black" class="clip layer" data-start="{e1 - 1.0}" data-duration="1.0" data-track-index="7" style="z-index:40"></div>
"""

    up = 'yPercent: 110, duration: 0.7, ease: "power3.out"'
    tl += [
        # hook: theme words rise out of a mask as they are spoken, soft blur-in
        f'tl.from("#hook-kicker", {{opacity: 0, scale: 1.12, duration: 0.6, ease: "power2.out"}}, 0.05);',
        f'tl.fromTo("#hook-a", {{yPercent: 105, filter: "blur(10px)"}}, {{yPercent: 0, filter: "blur(0px)", duration: 0.55, ease: "power3.out"}}, {ha});',
        f'tl.fromTo("#hook-b", {{yPercent: 105, filter: "blur(10px)"}}, {{yPercent: 0, filter: "blur(0px)", duration: 0.55, ease: "power3.out"}}, {hb});',
        f'tl.fromTo("#g-hook", {{filter: "blur(0px)"}}, {{opacity: 0, scale: 1.08, filter: "blur(8px)", duration: 0.3, ease: "power2.in", immediateRender: false}}, {hook_end - 0.3});',
        f'tl.to("#hook-vig", {{opacity: 0, duration: 0.3}}, {hook_end - 0.3});',
        # title: staggered mask reveals, gold rule draws, quiet exit
        f'tl.from("#title-scrim", {{opacity: 0, duration: 0.6, ease: "sine.out"}}, {t0 - 0.05});',
        f'tl.from("#title-kicker", {{{up}}}, {t0 + 0.05});',
        f'tl.from("#title-l1", {{{up}}}, {t0 + 0.18});',
        f'tl.from("#title-l2", {{{up}}}, {t0 + 0.3});',
        f'tl.from("#title-level", {{{up}}}, {t0 + 0.5});',
        f'tl.from("#title-rule", {{scaleX: 0, duration: 0.8, ease: "power2.inOut"}}, {t0 + 0.6});',
        f'tl.from("#title-meta", {{{up}}}, {t0 + 0.8});',
        f'tl.to("#title-block", {{opacity: 0, y: -16, duration: 0.4, ease: "power2.in"}}, {t1});',
        f'tl.to("#title-scrim", {{opacity: 0, duration: 0.45, ease: "sine.in"}}, {t1});',
        # theme lower third
        f'tl.from("#tag", {{xPercent: -18, opacity: 0, duration: 0.6, ease: "power3.out"}}, {g0});',
        f'tl.from("#tag .star", {{rotation: -90, scale: 0.6, duration: 0.9, ease: "power2.out"}}, {g0});',
        f'tl.to("#tag", {{opacity: 0, x: -30, duration: 0.4, ease: "power2.in"}}, {g1 - 0.4});',
        # closing
        f'tl.from("#close-scrim", {{opacity: 0, duration: 0.5}}, {c0 - 0.2});',
        f'tl.from("#close-k", {{opacity: 0, scale: 1.12, duration: 0.8, ease: "power2.out"}}, {c0});',
        f'tl.from("#close-l1", {{yPercent: 110, duration: 0.8, ease: "power3.out"}}, {c0 + 0.15});',
        f'tl.from("#close-year", {{yPercent: 110, duration: 0.7, ease: "power3.out"}}, {c0 + 0.4});',
        f'tl.from("#close-rule", {{scaleX: 0, duration: 0.9, ease: "power2.inOut"}}, {c0 + 0.6});',
        f'tl.from("#close-theme", {{yPercent: 110, duration: 0.7, ease: "power3.out"}}, {c0 + 0.85});',
        f'tl.to("#g-close", {{opacity: 0, duration: 0.45, ease: "power1.in"}}, {c1 - 0.05});',
        f'tl.to("#close-scrim", {{opacity: 0, duration: 0.5}}, {c1});',
        # end card: dissolve in over the wide, ornament turns, slow breathing push, fade to black
        f'tl.from("#end", {{opacity: 0, duration: 0.6, ease: "sine.inOut"}}, {e0});',
        f'tl.from("#end-star .star", {{rotation: -45, scale: 0.7, opacity: 0, duration: 1.2, ease: "power2.out"}}, {e0 + 0.2});',
        f'tl.from("#end-k", {{{up}}}, {e0 + 0.45});',
        f'tl.from("#end-l1", {{{up}}}, {e0 + 0.6});',
        f'tl.from("#end-level", {{{up}}}, {e0 + 0.8});',
        f'tl.from("#end-rule", {{scaleX: 0, duration: 0.9, ease: "power2.inOut"}}, {e0 + 0.9});',
        f'tl.from("#end-meta", {{{up}}}, {e0 + 1.05});',
        f'tl.fromTo("#end-pattern", {{scale: 1.0}}, {{scale: 1.06, duration: {round(e1 - e0, 2)}, ease: "none"}}, {e0});',
        f'tl.to("#fade-black", {{opacity: 1, duration: 0.9, ease: "power1.in"}}, {round(e1 - 1.0, 2)});',
    ]

    html = f"""<!doctype html>
<html lang="ms" data-resolution="{fmt["vp"]}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={fmt["w"]}, height={fmt["h"]}" />
    <!-- GENERATED by build/compose.py from build/edl.py: edit those, not this file. -->
    <script src="vendor/gsap.min.js"></script>
    <style>{css}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{edl.DURATION}" data-width="{fmt["w"]}" data-height="{fmt["h"]}">
      {chr(10).join("      " + v for v in vids).strip()}
      {graphics}
      <audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{edl.DURATION}" data-track-index="10"></audio>
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
    (HERE / name / "index.html").write_text(html)
    print("wrote", name + "/index.html")


for name, fmt in FORMATS.items():
    build(name, fmt)
