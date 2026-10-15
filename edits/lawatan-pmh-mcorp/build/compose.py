"""Generate hf/index.html (1920x1080, 60s): Sesi Lawatan Penanda Aras dan Taklimat, Perbadanan Melaka
Holdings Sdn. Bhd. (PMH), 14 Oktober 2026. Story in five chapters following the client storyboard.

Music: 120 BPM, bars every 2s from the first drop at 4.0s; cuts on beats, chapters on bar lines.
Usage: python3 compose.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
W, H = 1920, 1080
DURATION = 60.0
CLIP_LEN = {"p01": 12.9, "p02": 4.93, "p03": 6.77, "p04": 21.0, "p05": 4.67, "p06": 14.38, "p07": 10.0, "p08": 8.67,
            "p09": 8.07, "p10": 6.03, "p11": 11.44, "p12": 6.37, "p13": 11.54, "p14": 7.0, "p15": 8.1, "p16": 9.5,
            "p17": 8.2, "p18": 7.77, "p19": 5.87}

# Facts: names/titles as given in the client brief and on the corporate-information slide (p12);
# company name and subsidiary line from the PMH logo wall (p02). See NOTES.md.
F = {
    "event_a": "Sesi Lawatan Penanda Aras",
    "event_b": "dan Taklimat",
    "company": "Perbadanan Melaka Holdings Sdn. Bhd.",
    "subsidiary": "Anak syarikat milik penuh Perbadanan Melaka (MCORP)",
    "date": "14 Oktober 2026",
    "date_long": "Rabu, 14 Oktober 2026",
    "ceo": "YBhg. Datuk Saiful Hazwa bin Kipli",
    "ceo_role": "Ketua Pegawai Eksekutif MCORP merangkap Lembaga Pengarah PMH",
    "gm": "YBhg. Siti Ainshah binti Osman",
    "gm_role": "Pengurus Besar, Perbadanan Melaka Holdings Sdn. Bhd.",
}
CHAPTERS = [  # number, title, start, end
    ("01", "Pertemuan Bersama Pengurus Besar", 8.25, 10.9),
    ("02", "Bersama Warga PMH", 16.25, 18.9),
    ("03", "Ucapan Ketua Pegawai Eksekutif MCORP", 26.25, 28.9),
    ("04", "Pembentangan Informasi Korporat", 38.6, 41.3),
    ("05", "Kenangan Bersama", 48.25, 50.9),
]

# id, clip, start, duration, media in, framing start -> end (focusX, focusY, scale; 1920x1080 source
# space, scale 1 = full frame), ease, playback rate
SHOTS = [
    # HOOK 0-4: eight beat cuts
    ("h1", "p04", 0.0, 0.5, 2.0, (960, 500, 1.35), (960, 500, 1.42), "none", 1),
    ("h2", "p04", 0.5, 0.5, 7.5, (420, 560, 1.5), (420, 560, 1.57), "none", 1),
    ("h3", "p09", 1.0, 0.5, 3.0, (1480, 480, 1.55), (1480, 480, 1.62), "none", 1),
    ("h4", "p06", 1.5, 0.5, 9.0, (860, 560, 1.4), (860, 560, 1.47), "none", 1),
    ("h5", "p12", 2.0, 0.5, 2.0, (1300, 560, 1.25), (1300, 560, 1.32), "none", 1),
    ("h6", "p17", 2.5, 0.5, 1.5, (1150, 500, 1.45), (1150, 500, 1.52), "none", 1),
    ("h7", "p13", 3.0, 0.5, 7.0, (960, 560, 1.15), (960, 560, 1.22), "none", 1),
    ("h8", "p01", 3.5, 0.5, 6.5, (960, 560, 1.2), (960, 560, 1.3), "power2.in", 1),
    # TITLE 4-8: the PMH logo wall, pan reveals the staff
    ("t1", "p02", 4.0, 4.0, 0.0, (1250, 520, 1.35), (1150, 520, 1.12), "expo.out", 1),
    # 01 MEETING 8-16
    ("a1", "p01", 8.0, 3.0, 0.0, (960, 540, 1.0), (960, 560, 1.14), "none", 1),
    ("a2", "p01", 11.0, 2.5, 4.0, (1500, 470, 1.45), (1500, 470, 1.52), "none", 1),
    ("a3", "p01", 13.5, 2.5, 7.4, (500, 520, 1.45), (500, 520, 1.7), "expo.in", 1),
    # 02 WITH PMH STAFF 16-26
    ("b1", "p03", 16.0, 2.5, 1.5, (960, 540, 1.4), (960, 540, 1.1), "expo.out", 1),
    ("b2", "p04", 18.5, 2.5, 1.0, (960, 520, 1.15), (960, 520, 1.22), "none", 1),
    ("b3", "p04", 21.0, 2.0, 5.5, (900, 540, 1.15), (940, 540, 1.22), "none", 1),
    ("b4", "p04", 23.0, 2.0, 11.5, (700, 520, 1.2), (760, 520, 1.26), "none", 1),
    ("b5", "p05", 25.0, 1.0, 1.0, (960, 560, 1.15), (960, 560, 1.45), "expo.in", 1),
    # 03 CEO ADDRESS 26-36
    ("c1", "p06", 26.0, 2.0, 5.5, (900, 560, 1.45), (900, 560, 1.2), "expo.out", 1),
    ("c2", "p08", 28.0, 2.0, 0.5, (1100, 500, 1.15), (1100, 500, 1.22), "none", 1),
    ("c3", "p09", 30.0, 4.0, 0.3, (1300, 520, 1.25), (1450, 480, 1.42), "none", 1),
    ("c4", "p10", 34.0, 1.0, 0.5, (960, 540, 1.2), (960, 540, 1.26), "none", 1),
    ("c5", "p11", 35.0, 1.0, 7.0, (960, 540, 1.05), (960, 540, 1.12), "none", 1),
    # 04 CORPORATE PRESENTATION 36-48 (second drop)
    ("d1", "p12", 36.0, 2.5, 0.5, (1250, 560, 1.45), (1250, 560, 1.15), "expo.out", 1),
    ("d2", "p14", 38.5, 2.0, 0.5, (960, 560, 1.12), (1000, 560, 1.18), "none", 1),
    ("d3", "p15", 40.5, 2.0, 1.5, (1000, 560, 1.2), (1000, 560, 1.27), "none", 1),
    ("d4", "p16", 42.5, 2.0, 4.0, (960, 560, 1.12), (920, 560, 1.18), "none", 1),
    ("d5", "p17", 44.5, 1.5, 0.5, (1000, 540, 1.2), (1000, 540, 1.26), "none", 1),
    ("d6", "p18", 46.0, 2.0, 2.5, (960, 540, 1.15), (960, 540, 1.4), "expo.in", 1),
    # 05 TOGETHER 48-54
    ("e1", "p13", 48.0, 3.0, 5.0, (960, 560, 1.25), (960, 560, 1.02), "expo.out", 1),
    ("e2", "p19", 51.0, 3.55, 1.5, (960, 560, 1.22), (960, 580, 1.1), "none", 1),
]

CSS = """
@font-face { font-family: "Montserrat"; font-weight: 300; src: url(assets/fonts/Montserrat-300.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 500; src: url(assets/fonts/Montserrat-500.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 600; src: url(assets/fonts/Montserrat-600.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 700; src: url(assets/fonts/Montserrat-700.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 800; src: url(assets/fonts/Montserrat-800.ttf); }
/* PMH brand, sampled from the logo wall and the corporate slide: blue + gold star; deep navy ground */
:root { --blue: #1a56c4; --blue2: #0c64b2; --gold: #f4c21c; --navy: #081634; --white: #fff; --mist: rgba(255,255,255,0.8); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1920px; height: 1080px; overflow: hidden; background: #000; }
#root { position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #000; font-family: Montserrat, sans-serif; color: #fff; }
.clip { position: absolute; inset: 0; }
video.shot { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover; will-change: transform, opacity, filter; }
.layer { position: absolute; inset: 0; pointer-events: none; }
.mask { display: block; overflow: hidden; }
.mask > span, .mask > div { display: block; }
.kicker { font-weight: 700; font-size: 20px; letter-spacing: 0.34em; text-transform: uppercase; }
.goldbar { display: inline-block; width: 46px; height: 4px; background: var(--gold); vertical-align: middle; margin-right: 18px; }

#vignette { background: radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.4) 100%); z-index: 50; }
#flash { background: #fff; opacity: 0; z-index: 60; }
#black { background: #000; opacity: 0; z-index: 61; }
#leak { opacity: 0; z-index: 55; mix-blend-mode: screen;
  background: radial-gradient(ellipse 60% 80% at 85% 30%, rgba(255,190,90,0.95), rgba(255,120,40,0.5) 35%, rgba(255,80,0,0) 70%),
              radial-gradient(ellipse 40% 60% at 10% 80%, rgba(255,220,150,0.6), rgba(255,220,150,0) 70%); }

/* hook */
#hook-scrim { background: radial-gradient(ellipse at 50% 52%, rgba(8,22,52,0.72) 0%, rgba(8,22,52,0.5) 50%, rgba(0,0,0,0.7) 100%); z-index: 20; }
#g-hook { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 21; }
#hook-k { font-size: 22px; letter-spacing: 0.55em; color: var(--gold); margin-bottom: 26px; }
.hook-l { font-weight: 800; font-size: 124px; line-height: 1.0; letter-spacing: -0.01em; text-transform: uppercase; text-shadow: 0 10px 40px rgba(0,0,0,0.35); }
#hook-b { color: var(--gold); }
#hook-c { font-weight: 600; font-size: 26px; letter-spacing: 0.32em; text-transform: uppercase; margin-top: 30px; color: var(--mist); }
#hook-line { width: 560px; height: 4px; margin-top: 26px; background: linear-gradient(90deg, rgba(244,194,28,0), var(--gold), rgba(244,194,28,0)); }

/* title */
#title-scrim { background: linear-gradient(90deg, rgba(8,22,52,0.92) 0%, rgba(8,22,52,0.75) 38%, rgba(8,22,52,0) 66%); z-index: 20; }
#g-title { z-index: 21; }
#title-block { position: absolute; left: 130px; top: 270px; }
#title-k { color: var(--gold); }
#title-main { font-weight: 800; font-size: 92px; line-height: 1.02; letter-spacing: -0.012em; text-transform: uppercase; margin-top: 26px; }
#title-main .g { color: var(--gold); }
#title-co { font-weight: 700; font-size: 34px; margin-top: 34px; }
#title-sub { font-weight: 500; font-size: 22px; margin-top: 10px; color: var(--mist); }
#title-date { display: inline-flex; align-items: center; gap: 14px; margin-top: 34px; font-weight: 700; font-size: 24px; letter-spacing: 0.06em;
  padding: 12px 22px; background: var(--blue); border-left: 5px solid var(--gold); }

/* chapter cards */
.ch-scrim { background: linear-gradient(0deg, rgba(8,22,52,0.88) 0%, rgba(8,22,52,0.45) 30%, rgba(8,22,52,0) 55%); z-index: 20; opacity: 0; }
.ch { position: absolute; left: 120px; bottom: 100px; z-index: 22; display: flex; align-items: flex-end; gap: 30px; }
.ch-n { font-weight: 800; font-size: 170px; line-height: 0.8; color: transparent; -webkit-text-stroke: 2.5px var(--gold); }
.ch-r { padding-bottom: 6px; }
.ch-rule { width: 90px; height: 4px; background: var(--gold); margin-bottom: 18px; transform-origin: 0 50%; }
.ch-t { font-weight: 800; font-size: 54px; line-height: 1.05; text-transform: uppercase; letter-spacing: -0.005em; max-width: 1200px; }

/* lower thirds */
.lt { position: absolute; bottom: 92px; z-index: 22; display: flex; align-items: stretch; }
.lt.left { left: 110px; }
.lt.right { right: 110px; flex-direction: row-reverse; text-align: right; }
.lt-bar { width: 8px; background: var(--gold); }
.lt-body { background: linear-gradient(90deg, rgba(8,22,52,0.94), rgba(26,86,196,0.86)); padding: 22px 36px; }
.lt.right .lt-body { background: linear-gradient(270deg, rgba(8,22,52,0.94), rgba(26,86,196,0.86)); }
.lt-name { font-weight: 700; font-size: 34px; line-height: 1.12; }
.lt-role { font-weight: 500; font-size: 21px; margin-top: 8px; color: var(--mist); max-width: 760px; }

/* end card */
#end { background: #fff; z-index: 70; color: var(--navy); }
.shard { position: absolute; top: -20%; height: 140%; }
#sh-blue { width: 1300px; background: var(--blue); }
#sh-gold { width: 760px; background: var(--gold); }
#sh-navy { width: 1000px; background: var(--navy); }
#end-corner-a { position: absolute; right: -140px; top: -70px; width: 560px; height: 250px; background: var(--blue); transform: rotate(-30deg); z-index: 73; }
#end-corner-b { position: absolute; right: 60px; top: -120px; width: 90px; height: 330px; background: var(--gold); transform: rotate(-30deg); z-index: 73; }
#end-corner-c { position: absolute; left: -170px; bottom: -110px; width: 640px; height: 230px; background: var(--navy); transform: rotate(-30deg); z-index: 73; }
#end-inner { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 74; }
#end-k { color: var(--blue); font-size: 19px; }
#end-title { font-weight: 800; font-size: 60px; line-height: 1.06; text-transform: uppercase; margin-top: 22px; color: var(--navy); }
#end-rule { width: 120px; height: 4px; background: var(--gold); margin: 30px auto 26px; }
#end-co { font-weight: 700; font-size: 32px; color: var(--blue); }
#end-sub { font-weight: 500; font-size: 20px; margin-top: 8px; color: #5b6480; }
#end-date { font-weight: 600; font-size: 22px; margin-top: 22px; letter-spacing: 0.08em; color: var(--navy); }
#end-logo { height: 120px; width: auto; object-fit: contain; margin-top: 40px; }
#fade-black { background: #000; opacity: 0; z-index: 90; }
"""


def frame(f):
    X, Y, s = f
    tx, ty = s * (W / 2 - X), s * (H / 2 - Y)
    mx, my = (s * W - W) / 2, (s * H - H) / 2
    return {"x": round(max(-mx, min(mx, tx)), 2), "y": round(max(-my, min(my, ty)), 2), "scale": s}


def build():
    vids, tl = [], []
    for z, (sid, clip, t, d, ms, a, b, ease, rate) in enumerate(SHOTS):
        assert ms + d * rate <= CLIP_LEN[clip] + 1e-6, (sid, ms + d * rate, CLIP_LEN[clip])
        vids.append(f'<video id="v-{sid}" class="clip shot" src="assets/footage/{clip}.mp4" data-start="{t}" data-duration="{d}" '
                    f'data-media-start="{ms}" data-track-index="{z % 2}" style="z-index:1" muted playsinline></video>')
        tl.append(f'tl.fromTo("#v-{sid}", {json.dumps(frame(a))}, {{...{json.dumps(frame(b))}, duration: {d}, ease: "{ease}"}}, {t});')

    def punch(sid, t, amt=1.35, blur=6, dur=0.22):
        tl.append(f'tl.fromTo("#v-{sid}", {{filter: "brightness({amt}) blur({blur}px)"}}, {{filter: "brightness(1) blur(0px)", duration: {dur}, ease: "power2.out", immediateRender: false}}, {t});')

    def blur_out(sid, t, dur=0.3):
        tl.append(f'tl.fromTo("#v-{sid}", {{filter: "blur(0px)"}}, {{filter: "blur(14px)", duration: {dur}, ease: "power2.in", immediateRender: false}}, {round(t - dur, 2)});')

    for sid, t in [("h2", 0.5), ("h3", 1.0), ("h4", 1.5), ("h5", 2.0), ("h6", 2.5), ("h7", 3.0), ("h8", 3.5)]:
        punch(sid, t)
    # zoom-throughs at chapter changes (outgoing accelerates + blurs, incoming resolves)
    for out_id, in_id, t in [("h8", "t1", 4.0), ("a3", "b1", 16.0), ("b5", "c1", 26.0), ("d6", "e1", 48.0)]:
        blur_out(out_id, t)
        punch(in_id, t, 1.25, 14, 0.45)
    punch("d1", 36.0, 1.4, 10, 0.45)
    for sid, t in [("a2", 11.0), ("a3", 13.5), ("b2", 18.5), ("b3", 21.0), ("b4", 23.0), ("c2", 28.0), ("c3", 30.0),
                   ("d2", 38.5), ("d3", 40.5), ("d4", 42.5), ("d5", 44.5), ("d6", 46.0), ("e2", 51.0)]:
        punch(sid, t, 1.15, 3, 0.16)
    # white flash on both drops, black drop-gap before the second, golden light leaks on chapter changes
    for t, o in [(4.0, 0.85), (36.0, 0.75)]:
        tl.append(f'tl.fromTo("#flash", {{opacity: {o}}}, {{opacity: 0, duration: 0.45, ease: "power2.out", immediateRender: false}}, {t});')
    tl.append('tl.fromTo("#black", {opacity: 0}, {opacity: 1, duration: 0.08, immediateRender: false}, 35.72);')
    tl.append('tl.to("#black", {opacity: 0, duration: 0.05}, 36.0);')
    for t in (8.0, 16.0, 26.0, 48.0):
        tl.append(f'tl.fromTo("#leak", {{opacity: 0, x: -120}}, {{opacity: 0.85, x: 0, duration: 0.35, ease: "power2.out", immediateRender: false}}, {t - 0.2});')
        tl.append(f'tl.to("#leak", {{opacity: 0, x: 140, duration: 0.7, ease: "power2.in"}}, {t + 0.15});')

    up = 'yPercent: 105, duration: 0.6, ease: "power3.out"'
    chap_html = []
    for i, (n, title, a, b) in enumerate(CHAPTERS):
        chap_html.append(f"""
      <div id="chs{i}" class="clip layer ch-scrim" data-start="{a - 0.2}" data-duration="{round(b - a + 0.4, 2)}" data-track-index="5"></div>
      <div id="g-ch{i}" class="clip layer" data-start="{a}" data-duration="{round(b - a + 0.2, 2)}" data-track-index="6">
        <div id="ch{i}" class="ch"><div class="mask"><div id="chn{i}" class="ch-n">{n}</div></div>
          <div class="ch-r"><div id="chr{i}" class="ch-rule"></div><div class="mask"><div id="cht{i}" class="ch-t">{title}</div></div></div></div>
      </div>""")
        tl += [
            f'tl.fromTo("#chs{i}", {{opacity: 0}}, {{opacity: 1, duration: 0.4}}, {a - 0.2});',
            f'tl.from("#chn{i}", {{yPercent: 100, duration: 0.7, ease: "power4.out"}}, {a});',
            f'tl.from("#chr{i}", {{scaleX: 0, duration: 0.5, ease: "power2.out"}}, {a + 0.2});',
            f'tl.from("#cht{i}", {{yPercent: 105, duration: 0.65, ease: "power4.out"}}, {a + 0.28});',
            f'tl.to("#ch{i}", {{opacity: 0, x: -40, duration: 0.35, ease: "power2.in"}}, {b - 0.15});',
            f'tl.to("#chs{i}", {{opacity: 0, duration: 0.4}}, {b - 0.1});',
        ]

    def lt(i, side, name, role, a, b):
        tl.extend([
            f'tl.from("#lt{i} .lt-bar", {{scaleY: 0, transformOrigin: "50% 100%", duration: 0.35, ease: "power3.out"}}, {a});',
            f'tl.fromTo("#lt{i} .lt-body", {{clipPath: "{"inset(0% 100% 0% 0%)" if side == "left" else "inset(0% 0% 0% 100%)"}"}}, {{clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power3.out"}}, {a + 0.12});',
            f'tl.from(["#lt{i} .lt-name", "#lt{i} .lt-role"], {{y: 18, opacity: 0, duration: 0.45, stagger: 0.1, ease: "power3.out"}}, {a + 0.35});',
            f'tl.to("#lt{i}", {{opacity: 0, duration: 0.3, ease: "power2.in"}}, {b - 0.3});',
        ])
        return (f'<div id="g-lt{i}" class="clip layer" data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="6">'
                f'<div id="lt{i}" class="lt {side}"><div class="lt-bar"></div><div class="lt-body"><div class="lt-name">{name}</div>'
                f'<div class="lt-role">{role}</div></div></div></div>')

    lts = [lt(1, "left", F["ceo"], F["ceo_role"], 11.15, 13.45),  # CEO sits on the right of frame
           lt(2, "right", F["gm"], F["gm_role"], 13.65, 15.85)]  # GM sits on the left of frame

    graphics = f"""
      <div id="vignette" class="clip layer" data-start="0" data-duration="{DURATION}" data-track-index="3"></div>
      <div id="leak" class="clip layer" data-start="0" data-duration="{DURATION}" data-track-index="3"></div>
      <div id="flash" class="clip layer" data-start="0" data-duration="{DURATION}" data-track-index="4"></div>
      <div id="black" class="clip layer" data-start="0" data-duration="{DURATION}" data-track-index="4"></div>

      <div id="hook-scrim" class="clip layer" data-start="0" data-duration="4.0" data-track-index="5"></div>
      <div id="g-hook" class="clip layer" data-start="0" data-duration="4.0" data-track-index="6">
        <div class="mask"><span id="hook-k" class="kicker">{F["date"]}</span></div>
        <div class="mask"><div id="hook-a" class="hook-l">Lawatan Penanda Aras</div></div>
        <div class="mask"><div id="hook-b" class="hook-l">&amp; Taklimat</div></div>
        <div id="hook-line"></div>
        <div class="mask"><div id="hook-c">{F["company"]}</div></div>
      </div>

      <div id="title-scrim" class="clip layer" data-start="4.0" data-duration="4.0" data-track-index="5"></div>
      <div id="g-title" class="clip layer" data-start="4.0" data-duration="4.0" data-track-index="6">
        <div id="title-block">
          <div class="mask"><span id="title-k" class="kicker"><i class="goldbar"></i>PMH · MCORP</span></div>
          <div id="title-main"><span class="mask"><span id="tm1">{F["event_a"]}</span></span><span class="mask"><span id="tm2" class="g">{F["event_b"]}</span></span></div>
          <div class="mask"><div id="title-co">{F["company"]}</div></div>
          <div class="mask"><div id="title-sub">{F["subsidiary"]}</div></div>
          <div class="mask"><div id="title-date">{F["date_long"]}</div></div>
        </div>
      </div>
      {"".join(chap_html)}
      {"".join(lts)}

      <div id="end" class="clip layer" data-start="54.0" data-duration="6.0" data-track-index="7">
        <div id="end-corner-a"></div><div id="end-corner-b"></div><div id="end-corner-c"></div>
        <div id="end-inner">
          <div class="mask"><span id="end-k" class="kicker">Terima kasih atas kunjungan</span></div>
          <div class="mask"><div id="end-title">{F["event_a"]}<br/>{F["event_b"]}</div></div>
          <div id="end-rule"></div>
          <div class="mask"><div id="end-co">{F["company"]}</div></div>
          <div class="mask"><div id="end-sub">{F["subsidiary"]}</div></div>
          <div class="mask"><div id="end-date">{F["date"]}</div></div>
          <img id="end-logo" src="assets/img/mcorp-logo.png" alt="MCORP Perbadanan Melaka" />
        </div>
      </div>
      <div id="sh-wrap" class="clip layer" data-start="53.7" data-duration="1.25" data-track-index="8" style="z-index:80">
        <div id="sh-navy" class="shard"></div><div id="sh-blue" class="shard"></div><div id="sh-gold" class="shard"></div>
      </div>
      <div id="fade-black" class="clip layer" data-start="59.0" data-duration="1.0" data-track-index="9"></div>
"""

    tl += [
        # hook: date, then each line lands on a beat, company line, punch-out into the drop
        'tl.fromTo("#hook-scrim", {opacity: 0}, {opacity: 1, duration: 0.25}, 0);',
        f'tl.from("#hook-k", {{{up}}}, 0.05);',
        'tl.from("#hook-a", {yPercent: 105, duration: 0.55, ease: "power4.out"}, 0.5);',
        'tl.from("#hook-b", {yPercent: 105, duration: 0.55, ease: "power4.out"}, 1.5);',
        'tl.from("#hook-line", {scaleX: 0, duration: 0.8, ease: "power2.inOut"}, 1.7);',
        'tl.from("#hook-c", {yPercent: 105, duration: 0.5, ease: "power3.out"}, 2.5);',
        'tl.fromTo(["#hook-a", "#hook-b"], {scale: 1}, {scale: 1.05, duration: 0.15, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}, 3.0);',
        'tl.fromTo("#g-hook", {filter: "blur(0px)"}, {opacity: 0, scale: 1.3, filter: "blur(12px)", duration: 0.25, ease: "power2.in", immediateRender: false}, 3.72);',
        'tl.to("#hook-scrim", {opacity: 0, duration: 0.25}, 3.72);',
        # title
        'tl.fromTo("#title-scrim", {opacity: 0}, {opacity: 1, duration: 0.5}, 4.05);',
        f'tl.from("#title-k", {{{up}}}, 4.25);',
        'tl.from("#tm1", {yPercent: 105, duration: 0.7, ease: "power4.out"}, 4.35);',
        'tl.from("#tm2", {yPercent: 105, duration: 0.7, ease: "power4.out"}, 4.5);',
        f'tl.from("#title-co", {{{up}}}, 4.85);',
        f'tl.from("#title-sub", {{{up}}}, 5.0);',
        'tl.from("#title-date", {x: -40, opacity: 0, duration: 0.5, ease: "power3.out"}, 5.3);',
        'tl.to("#title-block", {opacity: 0, x: -40, duration: 0.35, ease: "power2.in"}, 7.55);',
        'tl.to("#title-scrim", {opacity: 0, duration: 0.4}, 7.6);',
        # end card: navy / blue / gold shards sweep to a white card
        'tl.fromTo("#sh-navy", {x: 2200, skewX: -30}, {x: -1700, skewX: -30, duration: 1.15, ease: "power3.inOut"}, 53.7);',
        'tl.fromTo("#sh-blue", {x: 2300, skewX: -30}, {x: -1600, skewX: -30, duration: 1.15, ease: "power3.inOut"}, 53.76);',
        'tl.fromTo("#sh-gold", {x: 2400, skewX: -30}, {x: -1300, skewX: -30, duration: 1.15, ease: "power3.inOut"}, 53.82);',
        'tl.fromTo("#end", {clipPath: "inset(0% 0% 0% 100%)"}, {clipPath: "inset(0% 0% 0% 0%)", duration: 0.75, ease: "power3.inOut"}, 53.95);',
        'tl.from(["#end-corner-a", "#end-corner-b"], {x: 300, y: -200, duration: 0.9, stagger: 0.06, ease: "power3.out"}, 54.3);',
        'tl.from("#end-corner-c", {x: -300, y: 200, duration: 0.9, ease: "power3.out"}, 54.3);',
        f'tl.from("#end-k", {{{up}}}, 54.5);',
        'tl.from("#end-title", {yPercent: 105, duration: 0.75, ease: "power4.out"}, 54.65);',
        'tl.from("#end-rule", {scaleX: 0, duration: 0.6, ease: "power2.out"}, 55.0);',
        f'tl.from("#end-co", {{{up}}}, 55.1);',
        f'tl.from("#end-sub", {{{up}}}, 55.25);',
        f'tl.from("#end-date", {{{up}}}, 55.4);',
        'tl.from("#end-logo", {scale: 0.85, opacity: 0, duration: 0.8, ease: "power3.out"}, 55.6);',
        'tl.fromTo("#end-inner", {scale: 1}, {scale: 1.03, duration: 5.0, ease: "none", immediateRender: false}, 55.0);',
        'tl.to("#fade-black", {opacity: 1, duration: 0.9, ease: "power1.in"}, 59.05);',
    ]

    html = f"""<!doctype html>
<html lang="ms" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <!-- GENERATED by build/compose.py: edit that, not this file. -->
    <script src="vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="1920" data-height="1080">
      {chr(10).join("      " + v for v in vids).strip()}
      {graphics}
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
