"""Generate hf/index.html (1920x1080, 60s) for the Bengkel Transisi MS ISO 37001 highlights.

Edit decision list and graphics timing live here. Music: 120 BPM, bars every 2s from the drop at
3.0s; every cut below sits on a beat (0.5s grid) and every section on a bar line.
Usage: python3 compose.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
W, H = 1920, 1080
DURATION = 60.0
CLIP_LEN = {"c01": 8.5, "c02": 9.6, "c03": 5.9, "c04": 5.73, "c05": 6.7, "c06": 6.7, "c07": 6.67,
            "c08": 6.77, "c09": 17.2, "c10": 8.8, "c11": 8.5, "c12": 9.1}

# Verified on-screen facts (title slide, Ucapan Aluan slide, SIRIM slide, tentatif; see NOTES.md)
F = {
    "org": "Perbadanan Melaka",
    "title": "Bengkel Transisi",
    "from": "MS ISO 37001:2016",
    "to": "MS ISO 37001:2025",
    "year": "Tahun 2026",
    "dates": "13 – 15 Oktober 2026",
    "venue": "Bilik Seminar, Aras 11, MCORP",
    "day1": "Hari Pertama · 13 Oktober 2026",
    "coo": "YBrs. Tuan Muhammad Ridzwan Yap bin Abdullah",
    "coo_role": "Ketua Pegawai Operasi, Perbadanan Melaka (MCORP)",
    "trainer": "En. Kanakaraja Muthusamy",
    "trainer_role": "Perunding · SIRIM Academy",
    "docs": ["Manual ABMS", "Pelan Risiko Bahagian / Jabatan", "Polisi-Polisi ABMS", "Prosedur Kerja"],
}

# id, clip, timeline start, duration, media in, framing start -> end (focusX, focusY, scale in 1920x1080
# source space; scale 1 = full frame), ease, playback rate
SHOTS = [
    # HOOK: six beat cuts (0.5s) teasing the day
    ("h1", "c03", 0.0, 0.5, 2.6, (960, 560, 1.3), (960, 560, 1.38), "none", 1),
    ("h2", "c08", 0.5, 0.5, 2.0, (1340, 440, 1.7), (1340, 440, 1.78), "none", 1),
    ("h3", "c10", 1.0, 0.5, 3.4, (1080, 640, 1.6), (1080, 640, 1.68), "none", 1),
    ("h4", "c09", 1.5, 0.5, 7.3, (880, 560, 1.45), (880, 560, 1.52), "none", 1),
    ("h5", "c07", 2.0, 0.5, 4.3, (820, 640, 1.45), (820, 640, 1.52), "none", 1),
    ("h6", "c11", 2.5, 0.5, 2.6, (1050, 500, 1.3), (1050, 500, 1.38), "none", 1),
    # TITLE: drop on the MCORP programme book, tilt up to the room; door-sign whip into the seminar room
    ("o1", "c01", 3.0, 3.6, 0.5, (960, 540, 1.3), (960, 540, 1.0), "expo.out", 1),
    ("o2", "c02", 6.6, 4.4, 1.6, (960, 540, 1.04), (960, 540, 1.32), "expo.in", 1),
    # DAY ONE: emcee, opening reading, COO, welcome speech
    ("p1", "c05", 11.0, 3.0, 0.6, (960, 540, 1.35), (960, 540, 1.08), "expo.out", 1),
    ("p2", "c06", 14.0, 2.0, 0.0, (1100, 600, 1.3), (1100, 600, 1.38), "none", 1),
    ("p3", "c04", 16.0, 2.0, 1.0, (1100, 560, 1.15), (1100, 560, 1.22), "none", 1),
    ("p4", "c08", 18.0, 5.0, 0.8, (1100, 540, 1.1), (1180, 520, 1.2), "none", 1),
    # BRIEFING: SIRIM Academy trainer and the room
    ("t1", "c10", 22.6, 4.4, 0.0, (1000, 560, 1.08), (1050, 560, 1.18), "none", 1),
    ("t2", "c11", 27.0, 2.0, 0.2, (1000, 540, 1.15), (1000, 540, 1.22), "none", 1),
    ("t3", "c07", 29.0, 2.0, 3.4, (900, 560, 1.2), (980, 560, 1.2), "none", 1),
    ("t4", "c10", 31.0, 2.0, 6.4, (1050, 580, 1.35), (1050, 580, 1.42), "none", 1),
    ("t5", "c09", 33.0, 2.0, 6.0, (900, 560, 1.15), (900, 560, 1.22), "none", 1),
    ("t6", "c11", 35.0, 2.0, 4.2, (1000, 540, 1.12), (1000, 540, 1.02), "none", 1),
    # MONTAGE: participants, one per beat-pair, then the tentatif screen and the room reveal
    ("m1", "c09", 37.0, 1.0, 0.5, (900, 560, 1.3), (900, 560, 1.36), "none", 1),
    ("m2", "c03", 38.0, 1.0, 3.6, (960, 560, 1.15), (960, 560, 1.2), "none", 1),
    ("m3", "c09", 39.0, 1.0, 9.3, (800, 600, 1.25), (800, 600, 1.31), "none", 1),
    ("m4", "c07", 40.0, 1.0, 0.6, (900, 600, 1.25), (900, 600, 1.31), "none", 1),
    ("m5", "c09", 41.0, 1.0, 12.6, (900, 600, 1.25), (900, 600, 1.31), "none", 1),
    ("m6", "c09", 42.0, 1.0, 15.2, (900, 620, 1.3), (900, 620, 1.36), "none", 1),
    ("m7", "c12", 43.0, 2.0, 0.0, (1150, 700, 1.15), (1100, 700, 1.25), "none", 1),
    ("m8", "c12", 45.0, 2.0, 2.0, (1000, 540, 1.1), (1000, 540, 1.1), "none", 1.5),
    # FINALE: wide room shots, impact zoom on the drop
    ("f1", "c12", 47.0, 4.0, 5.0, (960, 540, 1.35), (960, 540, 1.05), "expo.out", 1),
    ("f2", "c02", 51.0, 3.55, 6.0, (960, 540, 1.12), (960, 540, 1.0), "none", 1),
]

# --------------------------------------------------------------------------------- styles
CSS = """
@font-face { font-family: "Montserrat"; font-weight: 300; src: url(assets/fonts/Montserrat-300.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 500; src: url(assets/fonts/Montserrat-500.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 600; src: url(assets/fonts/Montserrat-600.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 700; src: url(assets/fonts/Montserrat-700.ttf); }
@font-face { font-family: "Montserrat"; font-weight: 800; src: url(assets/fonts/Montserrat-800.ttf); }
/* MCORP brand (sampled from the official logo): red #ec1c24, blue #2b3990 */
:root { --red: #ec1c24; --blue: #2b3990; --navy: #0c1440; --ink: #0a0f2c; --white: #ffffff; --mist: rgba(255,255,255,0.78); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1920px; height: 1080px; overflow: hidden; background: #000; }
#root { position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #000;
  font-family: Montserrat, sans-serif; color: var(--white); }
.clip { position: absolute; inset: 0; }
video.shot { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover; will-change: transform, opacity, filter; }
.layer { position: absolute; inset: 0; pointer-events: none; }
.mask { display: block; overflow: hidden; }
.mask > span, .mask > div { display: block; }
.kicker { font-weight: 700; font-size: 20px; letter-spacing: 0.34em; text-transform: uppercase; }
.redbar { display: inline-block; width: 46px; height: 4px; background: var(--red); vertical-align: middle; margin-right: 18px; }

#vignette { background: radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.38) 100%); z-index: 50; }
#flash { background: #fff; opacity: 0; z-index: 60; }

/* hook */
#hook-scrim { background: radial-gradient(ellipse at 50% 52%, rgba(12,20,64,0.72) 0%, rgba(12,20,64,0.55) 45%, rgba(0,0,0,0.65) 100%); z-index: 20; }
#g-hook { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 21; }
#hook-k { font-size: 24px; letter-spacing: 0.5em; margin-bottom: 22px; color: var(--mist); }
#hook-main { display: flex; align-items: baseline; justify-content: center; font-weight: 800; font-size: 150px;
  line-height: 1; letter-spacing: -0.01em; text-shadow: 0 10px 40px rgba(0,0,0,0.35); }
#hook-roll { display: inline-block; height: 1.0em; overflow: hidden; margin-left: 0; }
#hook-roll-inner > div { height: 1.0em; line-height: 1.0em; }
#hook-roll-inner .new { color: #fff; background: var(--red); padding: 0 0.12em; }
#hook-line { width: 520px; height: 4px; margin-top: 34px; background: linear-gradient(90deg, rgba(236,28,36,0), var(--red), rgba(236,28,36,0)); }

/* title */
#title-scrim { background: linear-gradient(90deg, rgba(10,15,44,0.9) 0%, rgba(10,15,44,0.72) 34%, rgba(10,15,44,0.0) 68%); z-index: 20; }
#g-title { z-index: 21; }
#title-block { position: absolute; left: 130px; top: 300px; }
#title-k { color: var(--mist); }
#title-main { font-weight: 800; font-size: 118px; line-height: 0.98; letter-spacing: -0.015em; margin-top: 26px; text-transform: uppercase; }
#title-main .red { color: var(--red); }
#title-std { display: flex; align-items: center; gap: 22px; margin-top: 34px; }
.pill { font-weight: 700; font-size: 30px; padding: 12px 22px; border-radius: 6px; letter-spacing: 0.01em; }
.pill.ghost { border: 2px solid rgba(255,255,255,0.75); }
.pill.solid { background: var(--red); }
#title-arrow { width: 54px; height: 3px; background: #fff; position: relative; }
#title-arrow::after { content: ""; position: absolute; right: -2px; top: -7px; border-left: 14px solid #fff; border-top: 8.5px solid transparent; border-bottom: 8.5px solid transparent; }
#title-info { position: absolute; left: 130px; bottom: 110px; display: flex; gap: 0; z-index: 22; }
.info { padding: 0 34px; border-left: 2px solid rgba(255,255,255,0.35); }
.info:first-child { padding-left: 0; border-left: none; }
.info .k { font-weight: 600; font-size: 15px; letter-spacing: 0.3em; color: var(--red); text-transform: uppercase; }
.info .v { font-weight: 600; font-size: 28px; margin-top: 8px; }

/* section tag */
#tag { position: absolute; left: 110px; top: 92px; z-index: 22; display: flex; align-items: center; }
#tag .kicker { font-size: 22px; background: rgba(10,15,44,0.82); padding: 14px 24px 14px 20px; }

/* lower thirds */
.lt { position: absolute; left: 110px; bottom: 96px; z-index: 22; display: flex; align-items: stretch; }
.lt-bar { width: 8px; background: var(--red); }
.lt-body { background: linear-gradient(90deg, rgba(10,15,44,0.92), rgba(43,57,144,0.82)); padding: 24px 40px 24px 30px; }
.lt-label { display: inline-block; font-weight: 700; font-size: 15px; letter-spacing: 0.3em; text-transform: uppercase;
  color: #fff; background: var(--red); padding: 6px 12px; margin-bottom: 14px; }
.lt-name { font-weight: 700; font-size: 36px; line-height: 1.1; }
.lt-role { font-weight: 500; font-size: 22px; margin-top: 8px; color: var(--mist); }

/* montage words */
#g-words { z-index: 22; }
#words { position: absolute; left: 120px; bottom: 120px; }
#words .w { font-weight: 800; font-size: 104px; line-height: 1.0; text-transform: uppercase; letter-spacing: -0.01em;
  text-shadow: 0 8px 40px rgba(0,0,0,0.45); }
#words .w.red { color: var(--red); }
#words-scrim { opacity: 0; background: linear-gradient(0deg, rgba(10,15,44,0.85) 0%, rgba(10,15,44,0.35) 45%, rgba(10,15,44,0) 70%); z-index: 20; }

/* docs */
#docs-scrim { background: linear-gradient(90deg, rgba(10,15,44,0.88) 0%, rgba(10,15,44,0.5) 45%, rgba(10,15,44,0) 70%); z-index: 20; }
#docs { position: absolute; left: 120px; top: 250px; z-index: 22; }
#docs .kicker { margin-bottom: 30px; }
.doc { display: flex; align-items: center; gap: 24px; margin-bottom: 22px; }
.doc .n { font-weight: 800; font-size: 26px; color: var(--red); width: 46px; }
.doc .t { font-weight: 700; font-size: 40px; }
.doc .rule { width: 420px; height: 1px; background: rgba(255,255,255,0.25); position: absolute; }

/* finale */
#fin-scrim { background: radial-gradient(ellipse at center, rgba(10,15,44,0.78) 0%, rgba(10,15,44,0.55) 50%, rgba(0,0,0,0.6) 100%); z-index: 20; }
#g-fin { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 21; }
#fin-k { color: var(--mist); margin-bottom: 26px; }
#fin-a { font-weight: 300; font-size: 54px; letter-spacing: 0.06em; text-transform: uppercase; }
#fin-b { font-weight: 800; font-size: 140px; line-height: 1.04; letter-spacing: -0.01em; }
#fin-b .red { color: var(--red); }
#fin-line { width: 420px; height: 4px; margin-top: 30px; background: linear-gradient(90deg, rgba(236,28,36,0), var(--red), rgba(236,28,36,0)); }

/* end card */
#end { background: #fff; z-index: 70; color: var(--ink); }
.shard { position: absolute; top: -20%; height: 140%; transform-origin: 50% 50%; }
#sh-blue { width: 1300px; background: var(--blue); z-index: 71; }
#sh-red { width: 900px; background: var(--red); z-index: 72; }
#end-corner-r { position: absolute; right: -120px; top: -60px; width: 520px; height: 260px; background: var(--red); transform: rotate(-32deg); z-index: 73; }
#end-corner-b { position: absolute; left: -160px; bottom: -110px; width: 620px; height: 240px; background: var(--blue); transform: rotate(-32deg); z-index: 73; }
#end-inner { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 74; }
#end-logo { height: 230px; width: auto; object-fit: contain; }
#end-rule { width: 120px; height: 4px; background: var(--red); margin: 40px auto 34px; }
#end-title { font-weight: 800; font-size: 50px; letter-spacing: -0.005em; text-transform: uppercase; color: var(--ink); }
#end-std { font-weight: 600; font-size: 30px; margin-top: 14px; color: var(--blue); }
#end-meta { font-weight: 500; font-size: 22px; margin-top: 26px; color: #5a607a; letter-spacing: 0.04em; }
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
        pr = f' data-playback-rate="{rate}"' if rate != 1 else ""
        vids.append(f'<video id="v-{sid}" class="clip shot" src="assets/footage/{clip}.mp4" data-start="{t}" data-duration="{d}" '
                    f'data-media-start="{ms}"{pr} data-track-index="{z % 2}" style="z-index:1" muted playsinline></video>')
        tl.append(f'tl.fromTo("#v-{sid}", {json.dumps(frame(a))}, {{...{json.dumps(frame(b))}, duration: {d}, ease: "{ease}"}}, {t});')

    def punch(sid, t, amt=1.35, blur=6, dur=0.22):
        tl.append(f'tl.fromTo("#v-{sid}", {{filter: "brightness({amt}) blur({blur}px)"}}, {{filter: "brightness(1) blur(0px)", duration: {dur}, ease: "power2.out", immediateRender: false}}, {t});')

    for sid, t in [("h2", 0.5), ("h3", 1.0), ("h4", 1.5), ("h5", 2.0), ("h6", 2.5)]:
        punch(sid, t)
    # zoom-through 11.0: outgoing o2 blurs as it accelerates, incoming p1 resolves
    tl.append('tl.fromTo("#v-o2", {filter: "blur(0px)"}, {filter: "blur(14px)", duration: 0.28, ease: "power2.in", immediateRender: false}, 10.72);')
    punch("p1", 11.0, 1.15, 14, 0.4)
    # dissolve 22.6 -> 23.0 into the briefing
    tl.append('tl.fromTo("#v-t1", {opacity: 0}, {opacity: 1, duration: 0.4, ease: "sine.inOut", immediateRender: false}, 22.6);')
    # beat-cut punches in the montage
    for sid, t in [("m2", 38), ("m3", 39), ("m4", 40), ("m5", 41), ("m6", 42), ("m7", 43)]:
        punch(sid, t, 1.2, 4, 0.18)
    punch("f1", 47.0, 1.4, 10, 0.45)
    # white flash on the drops
    for t, o in [(3.0, 0.85), (47.0, 0.7)]:
        tl.append(f'tl.fromTo("#flash", {{opacity: {o}}}, {{opacity: 0, duration: 0.4, ease: "power2.out", immediateRender: false}}, {t});')

    up = 'yPercent: 105, duration: 0.6, ease: "power3.out"'
    docs = "".join(f'<div class="doc mask"><div id="doc{i}" style="display:flex;align-items:center;gap:24px"><span class="n">0{i + 1}</span><span class="t">{d}</span></div></div>'
                   for i, d in enumerate(F["docs"]))
    graphics = f"""
      <div id="vignette" class="clip layer" data-start="0" data-duration="{DURATION}" data-track-index="3"></div>
      <div id="flash" class="clip layer" data-start="0" data-duration="{DURATION}" data-track-index="4"></div>

      <div id="hook-scrim" class="clip layer" data-start="0" data-duration="3.0" data-track-index="5"></div>
      <div id="g-hook" class="clip layer" data-start="0" data-duration="3.0" data-track-index="6">
        <div class="mask"><span id="hook-k" class="kicker">{F["title"]}</span></div>
        <div class="mask"><div id="hook-main"><span>MS ISO 37001:</span><span id="hook-roll"><div id="hook-roll-inner"><div>2016</div><div class="new">2025</div></div></span></div></div>
        <div id="hook-line"></div>
      </div>

      <div id="title-scrim" class="clip layer" data-start="3.0" data-duration="7.9" data-track-index="5"></div>
      <div id="g-title" class="clip layer" data-start="3.0" data-duration="7.9" data-track-index="6">
        <div id="title-block">
          <div class="mask"><span id="title-k" class="kicker"><i class="redbar"></i>{F["org"]} · {F["year"]}</span></div>
          <div id="title-main"><span class="mask"><span id="tm1">Bengkel</span></span><span class="mask"><span id="tm2" class="red">Transisi</span></span></div>
          <div id="title-std"><span id="std-a" class="pill ghost">{F["from"]}</span><span id="title-arrow"></span><span id="std-b" class="pill solid">{F["to"]}</span></div>
        </div>
        <div id="title-info">
          <div class="info mask"><div id="inf1"><div class="k">Tarikh</div><div class="v">{F["dates"]}</div></div></div>
          <div class="info mask"><div id="inf2"><div class="k">Tempat</div><div class="v">{F["venue"]}</div></div></div>
        </div>
      </div>

      <div id="g-tag" class="clip layer" data-start="11.2" data-duration="3.5" data-track-index="6">
        <div id="tag" class="mask"><span id="tag-in" class="kicker"><i class="redbar"></i>{F["day1"]}</span></div>
      </div>

      <div id="g-lt1" class="clip layer" data-start="18.4" data-duration="4.3" data-track-index="6">
        <div id="lt1" class="lt"><div class="lt-bar"></div><div class="lt-body"><div class="lt-label">Ucapan Aluan</div>
          <div class="lt-name">{F["coo"]}</div><div class="lt-role">{F["coo_role"]}</div></div></div>
      </div>
      <div id="g-lt2" class="clip layer" data-start="23.4" data-duration="4.4" data-track-index="6">
        <div id="lt2" class="lt"><div class="lt-bar"></div><div class="lt-body"><div class="lt-label">Taklimat Standard ISO 37001</div>
          <div class="lt-name">{F["trainer"]}</div><div class="lt-role">{F["trainer_role"]}</div></div></div>
      </div>

      <div id="words-scrim" class="clip layer" data-start="37.0" data-duration="6.0" data-track-index="5"></div>
      <div id="g-words" class="clip layer" data-start="37.0" data-duration="6.0" data-track-index="6">
        <div id="words">
          <div class="mask"><div id="w1" class="w">Penambahbaikan</div></div>
          <div class="mask"><div id="w2" class="w">&amp; Pemurnian</div></div>
          <div class="mask"><div id="w3" class="w red">Dokumen ABMS</div></div>
        </div>
      </div>

      <div id="docs-scrim" class="clip layer" data-start="43.0" data-duration="4.0" data-track-index="5"></div>
      <div id="g-docs" class="clip layer" data-start="43.0" data-duration="4.0" data-track-index="6">
        <div id="docs"><div class="mask"><span id="docs-k" class="kicker"><i class="redbar"></i>Dokumen ABMS</span></div>{docs}</div>
      </div>

      <div id="fin-scrim" class="clip layer" data-start="47.0" data-duration="7.2" data-track-index="5"></div>
      <div id="g-fin" class="clip layer" data-start="47.0" data-duration="7.2" data-track-index="6">
        <div class="mask"><span id="fin-k" class="kicker">{F["title"]} · {F["org"]}</span></div>
        <div class="mask"><span id="fin-a">Bersama ke arah</span></div>
        <div class="mask"><span id="fin-b">MS ISO 37001:<span class="red">2025</span></span></div>
        <div id="fin-line"></div>
      </div>

      <div id="end" class="clip layer" data-start="54.0" data-duration="6.0" data-track-index="7">
        <div id="end-corner-r"></div><div id="end-corner-b"></div>
        <div id="end-inner">
          <img id="end-logo" src="assets/img/mcorp-logo.png" alt="MCORP Perbadanan Melaka" />
          <div id="end-rule"></div>
          <div class="mask"><div id="end-title">{F["title"]}</div></div>
          <div class="mask"><div id="end-std">{F["from"]} kepada {F["to"]}</div></div>
          <div class="mask"><div id="end-meta">{F["dates"]}  ·  {F["venue"]}</div></div>
        </div>
      </div>
      <div id="sh-wrap" class="clip layer" data-start="53.7" data-duration="1.2" data-track-index="8" style="z-index:80">
        <div id="sh-blue" class="shard"></div><div id="sh-red" class="shard"></div>
      </div>
      <div id="fade-black" class="clip layer" data-start="59.0" data-duration="1.0" data-track-index="9"></div>
"""

    tl += [
        # hook
        'tl.fromTo("#hook-scrim", {opacity: 0}, {opacity: 1, duration: 0.25}, 0);',
        'tl.from("#hook-k", {yPercent: 110, duration: 0.45, ease: "power3.out"}, 0.05);',
        'tl.from("#hook-main", {yPercent: 105, duration: 0.55, ease: "power4.out"}, 0.45);',
        'tl.from("#hook-line", {scaleX: 0, duration: 0.8, ease: "power2.inOut"}, 0.6);',
        'tl.to("#hook-roll-inner", {yPercent: -50, duration: 0.42, ease: "power4.inOut"}, 1.9);',
        'tl.fromTo("#hook-main", {scale: 1}, {scale: 1.06, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}, 2.3);',
        'tl.fromTo("#g-hook", {filter: "blur(0px)"}, {opacity: 0, scale: 1.25, filter: "blur(10px)", duration: 0.28, ease: "power2.in", immediateRender: false}, 2.72);',
        'tl.to("#hook-scrim", {opacity: 0, duration: 0.28}, 2.72);',
        # title
        'tl.fromTo("#title-scrim", {opacity: 0}, {opacity: 1, duration: 0.6}, 3.1);',
        f'tl.from("#title-k", {{{up}}}, 3.35);',
        f'tl.from("#tm1", {{yPercent: 105, duration: 0.7, ease: "power4.out"}}, 3.5);',
        f'tl.from("#tm2", {{yPercent: 105, duration: 0.7, ease: "power4.out"}}, 3.65);',
        'tl.from("#std-a", {x: -40, opacity: 0, duration: 0.5, ease: "power3.out"}, 4.0);',
        'tl.from("#title-arrow", {scaleX: 0, transformOrigin: "0% 50%", duration: 0.4, ease: "power2.out"}, 4.3);',
        'tl.from("#std-b", {x: -40, opacity: 0, duration: 0.5, ease: "power3.out"}, 4.5);',
        'tl.fromTo("#std-b", {scale: 1}, {scale: 1.08, duration: 0.2, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}, 5.0);',
        f'tl.from("#inf1", {{{up}}}, 7.3);',
        f'tl.from("#inf2", {{{up}}}, 7.45);',
        'tl.to(["#title-block", "#title-info"], {opacity: 0, x: -40, duration: 0.4, ease: "power2.in"}, 10.3);',
        'tl.to("#title-scrim", {opacity: 0, duration: 0.4}, 10.4);',
        # day one tag
        f'tl.from("#tag-in", {{{up}}}, 11.3);',
        'tl.to("#tag-in", {yPercent: -105, duration: 0.4, ease: "power2.in"}, 14.25);',
        # lower thirds
        'tl.from("#lt1 .lt-bar", {scaleY: 0, transformOrigin: "50% 100%", duration: 0.35, ease: "power3.out"}, 18.4);',
        'tl.fromTo("#lt1 .lt-body", {clipPath: "inset(0% 100% 0% 0%)"}, {clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power3.out"}, 18.55);',
        'tl.from(["#lt1 .lt-label", "#lt1 .lt-name", "#lt1 .lt-role"], {y: 20, opacity: 0, duration: 0.45, stagger: 0.1, ease: "power3.out"}, 18.8);',
        'tl.to("#lt1", {opacity: 0, x: -30, duration: 0.35, ease: "power2.in"}, 22.3);',
        'tl.from("#lt2 .lt-bar", {scaleY: 0, transformOrigin: "50% 100%", duration: 0.35, ease: "power3.out"}, 23.4);',
        'tl.fromTo("#lt2 .lt-body", {clipPath: "inset(0% 100% 0% 0%)"}, {clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power3.out"}, 23.55);',
        'tl.from(["#lt2 .lt-label", "#lt2 .lt-name", "#lt2 .lt-role"], {y: 20, opacity: 0, duration: 0.45, stagger: 0.1, ease: "power3.out"}, 23.8);',
        'tl.to("#lt2", {opacity: 0, x: -30, duration: 0.35, ease: "power2.in"}, 27.45);',
        # montage words, one line per bar
        'tl.fromTo("#words-scrim", {opacity: 0}, {opacity: 1, duration: 0.4}, 37.0);',
        'tl.from("#w1", {yPercent: 105, duration: 0.6, ease: "power4.out"}, 37.0);',
        'tl.from("#w2", {yPercent: 105, duration: 0.6, ease: "power4.out"}, 39.0);',
        'tl.from("#w3", {yPercent: 105, duration: 0.6, ease: "power4.out"}, 41.0);',
        'tl.to(["#w1", "#w2", "#w3"], {yPercent: -105, duration: 0.4, ease: "power3.in", stagger: 0.05}, 42.55);',
        'tl.to("#words-scrim", {opacity: 0, duration: 0.3}, 42.7);',
        # docs list, one per beat
        'tl.fromTo("#docs-scrim", {opacity: 0}, {opacity: 1, duration: 0.35}, 43.0);',
        f'tl.from("#docs-k", {{{up}}}, 43.05);',
        *[f'tl.from("#doc{i}", {{yPercent: 105, duration: 0.5, ease: "power3.out"}}, {43.5 + 0.5 * i});' for i in range(4)],
        'tl.to("#docs", {opacity: 0, x: -40, duration: 0.35, ease: "power2.in"}, 46.6);',
        'tl.to("#docs-scrim", {opacity: 0, duration: 0.35}, 46.65);',
        # finale
        'tl.fromTo("#fin-scrim", {opacity: 0}, {opacity: 1, duration: 0.5}, 47.0);',
        f'tl.from("#fin-k", {{{up}}}, 47.3);',
        'tl.from("#fin-a", {yPercent: 105, duration: 0.7, ease: "power4.out"}, 47.5);',
        'tl.from("#fin-b", {yPercent: 105, duration: 0.8, ease: "power4.out"}, 47.75);',
        'tl.from("#fin-line", {scaleX: 0, duration: 1.0, ease: "power2.inOut"}, 48.2);',
        'tl.fromTo("#g-fin", {scale: 1}, {scale: 1.04, duration: 5.6, ease: "none", immediateRender: false}, 48.0);',
        # end card: brand shards sweep across, white card revealed behind them
        'tl.fromTo("#sh-blue", {x: 2200, skewX: -32}, {x: -1700, skewX: -32, duration: 1.1, ease: "power3.inOut"}, 53.7);',
        'tl.fromTo("#sh-red", {x: 2300, skewX: -32}, {x: -1500, skewX: -32, duration: 1.1, ease: "power3.inOut"}, 53.78);',
        'tl.fromTo("#end", {clipPath: "inset(0% 0% 0% 100%)"}, {clipPath: "inset(0% 0% 0% 0%)", duration: 0.75, ease: "power3.inOut"}, 53.95);',
        'tl.from("#end-corner-r", {x: 300, y: -200, duration: 0.9, ease: "power3.out"}, 54.3);',
        'tl.from("#end-corner-b", {x: -300, y: 200, duration: 0.9, ease: "power3.out"}, 54.3);',
        'tl.from("#end-logo", {scale: 0.85, opacity: 0, duration: 0.9, ease: "power3.out"}, 54.5);',
        'tl.from("#end-rule", {scaleX: 0, duration: 0.6, ease: "power2.out"}, 55.0);',
        f'tl.from("#end-title", {{{up}}}, 55.1);',
        f'tl.from("#end-std", {{{up}}}, 55.25);',
        f'tl.from("#end-meta", {{{up}}}, 55.4);',
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
