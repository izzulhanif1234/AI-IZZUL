"""Build the MITC promo v4 (hypermotion cut) -> edits/mitc-promo/hf/index.html.

Music: Mixkit "Driving Ambition" (100 BPM, beat 0.6002 s). bed.wav starts at track 26.481 s so the
build-up carries a 12 s MITC introduction and the drop (track 38.485 s) lands at 12.004 s; the
final chord lands at 50.983 s. Every cut sits on the beat grid (downbeats = 2.4008 k).
No sound effects (music only).
"""
import json

ROOT = "/home/user/AI-IZZUL/edits/mitc-promo/hf"
B = 0.6002
BAR = 4 * B
DROP = 5 * BAR            # 12.004
F = 50.983                # final chord -> outro
END = 55.6
OV = 0.15                 # half-length of a transition (shots overlap by 2*OV)

S = {                     # section starts
    "logo": DROP, "sa": DROP + 2 * BAR, "sb": DROP + 6 * BAR, "sc": DROP + 8 * BAR,
    "sd": DROP + 10 * BAR, "aw": DROP + 12 * BAR, "recap": DROP + 14 * BAR, "close": F - 2.99, "out": F,
}
r = lambda x: round(x, 3)

# ------------------------------------------------------------------ montage shots
# (id, media, start, end, transition-in, caption, pan) ; media "v:name" clip or "i:file:width"
SHOTS = []


def run(start, items):
    t = start
    for it in items:
        sid, media, beats, trans, cap = it[:5]
        pan = it[5] if len(it) > 5 else None
        SHOTS.append(dict(id=sid, media=media, t0=r(t), t1=r(t + beats * B), trans=trans, cap=cap, pan=pan))
        t += beats * B
    return r(t)


run(S["sa"], [
    ("a1", "v:hall-expo", 2, "zoom", "Ekspo & Pameran"),
    ("a2", "v:hall-booths", 2, "whipL", "Ekspo & Pameran"),
    ("a3", "v:hall-robot", 2, "spin", "Pameran Teknologi"),
    ("a4", "v:ev-ht-gate", 2, "whipU", "Pameran Hang Tuah · Hall A"),
    ("a5", "v:ev-ht-houses", 2, "zoom", "Pameran Hang Tuah · Hall A"),
    ("a6", "v:prep-hall", 2, "push3d", "Gala Dinner · Hall B"),
    ("a7", "v:ev-tables", 2, "whipL", "Gala Dinner · Hall B"),
    ("a8", "i:ballroom.jpg:2560", 2, "spin", "Majlis Rasmi · Dewan Pameran", (-900, -700, 1.0, 1.08)),
])
run(S["sb"], [
    ("b1", "v:hall-stage", 2, "zoom", "Majlis Perasmian"),
    ("b2", "v:hall-seminar", 2, "whipL", "Seminar & Bengkel"),
    ("b3", "i:meeting.jpg:3413", 2, "push3d", "Bilik Mesyuarat", (-1050, -1350, 1.0, 1.06)),
    ("b4", "i:lounge.jpg:2560", 2, "whipU", "Ruang VIP", (-480, -700, 1.0, 1.06)),
])
run(S["sc"], [
    ("c1", "v:grand-ballroom", 3, "zoom", "Iskandar Shah Grand Ballroom"),
    ("c2", "v:grand-2", 2, "whipL", "Iskandar Shah Grand Ballroom"),
    ("c3", "v:maharani-hall", 3, "spin", "Maharani Ballroom"),
])
run(S["sd"], [
    ("d1", "v:hook-star", 2, "zoom", "Dekorasi & Susun Atur"),
    ("d2", "i:lobby-screen.jpg:1080", 3, "whipU", "Signage Digital", (0, 0, 1.12, 1.02)),
    ("d3", "v:hook-stage", 3, "push3d", "Teknikal, AV & Pentas"),
])
rb = (S["close"] - S["recap"]) / 4
for i, (sid, m, tr) in enumerate([("r1", "v:hall-expo", "zoom"), ("r2", "v:hall-robot", "whipL"),
                                   ("r3", "v:grand-ballroom", "whipU"), ("r4", "v:prep-hall", "spin")]):
    SHOTS.append(dict(id=sid, media=m, t0=r(S["recap"] + i * rb), t1=r(S["recap"] + (i + 1) * rb), trans=tr, cap="", pan=None, mstart=0.8))

SECTIONS = [  # id, start, end, number, title, english, sub
    ("sa", S["sa"], S["sb"], "01", "Dewan Pameran", "Exhibition Halls", "Hall A · Hall B · Hall C"),
    ("sb", S["sb"], S["sc"], "02", "Konvensyen &amp; Mesyuarat", "Conventions &amp; Meetings", "Auditorium · 6 Bilik Mesyuarat · Bilik VIP"),
    ("sc", S["sc"], S["sd"], "03", "Ballroom", "Grand Ballrooms", "Iskandar Shah · Maharani"),
    ("sd", S["sd"], S["aw"], "04", "Perkhidmatan Bersepadu", "Integrated Event Services", None),
]
SD_CHIPS = ["Dekorasi", "Signage", "Teknikal &amp; Wi-Fi", "Pasukan Berpengalaman"]


def media_el(sh, start, dur):
    kind, *rest = sh["media"].split(":")
    ms = sh.get("mstart", 0.02 if sh["media"].startswith("v:hook-") else 0.15)
    if kind == "v":
        return (f'<video id="m-{sh["id"]}" class="clip mv" src="assets/clips/{rest[0]}.mp4" data-start="{start}" '
                f'data-duration="{dur}" data-media-start="{ms}" data-track-index="0" muted playsinline></video>')
    f, w = rest
    h = ' height: 2012px;' if f == "lobby-screen.jpg" else ""
    return (f'<img id="m-{sh["id"]}" class="clip mi" src="assets/img/{f}" data-start="{start}" data-duration="{dur}" '
            f'data-track-index="0" style="width: {w}px;{h}" alt="" />')


# ------------------------------------------------------------------ html
CSS = open(f"{ROOT}/../style.v4.css").read()
H = []
A = H.append
A(f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="vendor/gsap.min.js"></script>
    <style>
{CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
""")

# ---- intro picture layers
A(f'''      <!-- ================= INTRO (0 - {r(DROP)}) over the build-up ================= -->
      <div id="w-x1" class="wrap"><img id="x1" class="clip" src="assets/img/exterior-hi.jpg" data-start="0" data-duration="{r(2 * BAR + OV)}" data-track-index="0" style="width: 3413px" alt="" /></div>
      <div id="w-x2" class="wrap"><img id="x2" class="clip" src="assets/img/aerial.jpg" data-start="{r(2 * BAR - OV)}" data-duration="{r(2 * BAR)}" data-track-index="0" style="width: 3413px" alt="" /></div>
      <div id="w-strips" class="wrap">
        <div id="st1" class="strip"><video id="sv1" class="clip" src="assets/clips/hall-expo.mp4" data-start="{r(3 * BAR - OV)}" data-duration="{r(BAR + 2 * OV)}" data-media-start="0" data-track-index="1" muted playsinline></video></div>
        <div id="st2" class="strip"><img id="sv2" class="clip" src="assets/img/meeting.jpg" data-start="{r(3 * BAR - OV)}" data-duration="{r(BAR + 2 * OV)}" data-track-index="1" style="width: 3413px; height: 1920px; left: -1400px" alt="" /></div>
        <div id="st3" class="strip"><video id="sv3" class="clip" src="assets/clips/grand-ballroom.mp4" data-start="{r(3 * BAR - OV)}" data-duration="{r(BAR + 2 * OV)}" data-media-start="0" data-track-index="1" muted playsinline></video></div>
      </div>
      <div id="w-x3" class="wrap"><img id="x3" class="clip" src="assets/img/exterior-hi.jpg" data-start="{r(4 * BAR - OV)}" data-duration="{r(BAR + 2 * OV)}" data-track-index="0" style="width: 3413px" alt="" /></div>
      <div id="sh-intro" class="clip shade-intro" data-start="0" data-duration="{r(DROP)}" data-track-index="2"></div>
''')
# ---- logo scene background
A(f'''      <!-- ================= LOGO ({r(DROP)}) ================= -->
      <div id="w-lg" class="wrap"><video id="lgv" class="clip mv" src="assets/clips/logo-bg.mp4" data-start="{r(DROP)}" data-duration="{r(2 * BAR + OV)}" data-media-start="0" data-track-index="0" muted playsinline></video></div>
      <div id="sh-logo" class="clip shade-logo" data-start="{r(DROP)}" data-duration="{r(2 * BAR + OV)}" data-track-index="2"></div>
''')
# ---- montage shots
A("      <!-- ================= MONTAGE (hypermotion) ================= -->")
for i, sh in enumerate(SHOTS):
    start = r(sh["t0"] - OV)
    dur = r(sh["t1"] + OV - start)
    A(f'      <div id="w-{sh["id"]}" class="wrap">{media_el(sh, start, dur)}</div>')
A(f'      <div id="sh-mont" class="clip shade-mont" data-start="{r(S["sa"])}" data-duration="{r(S["aw"] - S["sa"])}" data-track-index="2"></div>')
A(f'      <div id="sh-recap" class="clip shade-full" data-start="{r(S["recap"])}" data-duration="{r(S["close"] - S["recap"])}" data-track-index="2"></div>')
# ---- awards / close / outro backgrounds
A(f'''      <div id="p-aw" class="clip" data-start="{r(S["aw"] - OV)}" data-duration="{r(S["recap"] - S["aw"] + 2 * OV)}" data-track-index="1"><div id="aw-bg"></div></div>
      <video id="v-aw" class="clip" src="assets/video/award.mp4" data-start="{r(S["aw"])}" data-duration="{r(S["recap"] - S["aw"])}" data-media-start="0.6" data-track-index="3" muted playsinline></video>
      <div id="w-cl" class="wrap"><img id="cl" class="clip" src="assets/img/exterior-hi.jpg" data-start="{r(S["close"] - OV)}" data-duration="{r(F - S["close"] + 2 * OV)}" data-track-index="0" style="width: 3413px" alt="" /></div>
      <div id="sh-close" class="clip shade-close" data-start="{r(S["close"])}" data-duration="{r(F - S["close"])}" data-track-index="2"></div>
      <div id="w-out" class="wrap"><img id="ob" class="clip" src="assets/img/signage.jpg" data-start="{r(F)}" data-duration="{r(END - F)}" data-track-index="0" style="width: 3413px" alt="" /></div>
      <div id="sh-out" class="clip shade-out" data-start="{r(F)}" data-duration="{r(END - F)}" data-track-index="2"></div>
''')

# ---- text layers
A(f'''      <!-- ================= TYPE ================= -->
      <div id="t-intro" class="clip" data-start="0" data-duration="{r(DROP)}" data-track-index="4">
        <div id="streak"></div>
        <div id="i-k1" class="kicker c">Selamat datang ke</div>
        <div id="i-k2" class="kicker c dim">Ayer Keroh · Melaka · Malaysia</div>
        <div id="i-title">
          <div class="ln" id="it1">Melaka</div>
          <div class="ln" id="it2">International</div>
          <div class="ln y" id="it3">Trade Centre</div>
          <div id="it-bar"></div>
        </div>
        <div id="i-stat1" class="stat"><div class="k">Kompleks seluas</div><div class="v"><span id="n1">0.0</span><small>ekar</small></div></div>
        <div id="i-stat2" class="stat"><div class="v"><span id="n2">0</span><small>m²</small></div><div class="k">ruang mesyuarat &amp; pameran fleksibel</div></div>
        <div id="lab1" class="slab"><b>3</b>Dewan<br />Pameran</div>
        <div id="lab2" class="slab"><b>6</b>Bilik<br />Mesyuarat</div>
        <div id="lab3" class="slab"><b>1</b>Grand<br />Ballroom</div>
        <div id="think1" class="think">Think <span>MICE,</span></div>
        <div id="think2" class="think">Think <span class="y">MITC!</span></div>
      </div>
      <div id="t-logo" class="clip" data-start="{r(DROP)}" data-duration="{r(2 * BAR)}" data-track-index="4">
        <div id="rays"></div>
        <div id="lg"><img src="assets/img/logo-globe.png" alt="MITC" /></div>
        <div id="lg-head">
          <div class="t">Pusat Konvensyen &amp; Acara Perniagaan Bertaraf Antarabangsa</div>
          <div class="en">Premier International Convention &amp; Business Events Centre</div>
          <div class="pill">Persidangan · Pameran · Acara Korporat</div>
        </div>
      </div>
      <div id="hud" class="clip" data-start="{r(S["sa"])}" data-duration="{r(S["aw"] - S["sa"])}" data-track-index="5">
        <div class="br tl"></div><div class="br tr"></div><div class="br bl"></div><div class="br brr"></div>
        <div id="hud-l">MITC · MELAKA</div>
        <div id="hud-r">THINK MICE, THINK MITC</div>
        <div id="hud-bar"><div id="hud-fill"></div></div>
      </div>
''')
for sid, t0, t1, num, title, en, sub in SECTIONS:
    caps = [sh for sh in SHOTS if t0 - 0.01 <= sh["t0"] < t1 - 0.01]
    A(f'      <div id="t-{sid}" class="clip" data-start="{r(t0)}" data-duration="{r(t1 - t0)}" data-track-index="4">')
    A(f'        <div class="sec"><div class="num">{num}</div><div class="en">{en}</div><div class="ttl">{title}</div>'
      + (f'<div class="sub">{sub}</div>' if sub else "")
      + ('<div class="chips">' + "".join(f'<div class="chip">{c}</div>' for c in SD_CHIPS) + "</div>" if sid == "sd" else "")
      + "</div>")
    for sh in caps:
        A(f'        <div id="cap-{sh["id"]}" class="cap"><i></i>{sh["cap"]}</div>')
    A("      </div>")
A(f'''      <div id="t-aw" class="clip" data-start="{r(S["aw"])}" data-duration="{r(S["recap"] - S["aw"])}" data-track-index="4">
        <div id="aw-title"><div class="k kicker">Bertaraf antarabangsa</div><div class="t">Diiktiraf</div></div>
        <div id="bd1" class="badge"><img src="assets/img/asean-exhibition.png" alt="" /></div>
        <div id="bd2" class="badge"><img src="assets/img/asean-meeting.png" alt="" /></div>
        <div id="bd3" class="badge"><img src="assets/img/brandlaureate.png" alt="" /></div>
        <div id="bd4" class="badge photo"><img src="assets/img/cmiea.jpg" alt="" /></div>
        <div id="al1" class="aw-label">ASEAN MICE Venue Standard<small>Exhibition Venue &amp; Meeting Room · 2026–2028</small></div>
        <div id="al2" class="aw-label">BrandLaureate BestBrands<small>MICE Venue · 2025–2026</small></div>
        <div id="al3" class="aw-label">CMIEA 2025<small>Excellence Service Sector</small></div>
      </div>
      <div id="t-recap" class="clip" data-start="{r(S["recap"])}" data-duration="{r(S["close"] - S["recap"])}" data-track-index="4">
        <div id="rc1" class="think big">Think <span>MICE.</span></div>
        <div id="rc2" class="think big">Think <span class="y">MITC.</span></div>
      </div>
      <div id="t-close" class="clip" data-start="{r(S["close"])}" data-duration="{r(F - S["close"])}" data-track-index="4">
        <div id="cl-t">Lebih daripada<br />sebuah venue.</div>
        <div id="cl-s">Destinasi untuk acara yang luar biasa</div>
      </div>
      <div id="t-out" class="clip" data-start="{r(F)}" data-duration="{r(END - F)}" data-track-index="4">
        <div id="out-logo"><img src="assets/img/logo-globe.png" alt="MITC" /></div>
        <div id="out-name">Melaka International Trade Centre</div>
        <div id="out-cta">HUBUNGI KAMI SEKARANG</div>
        <div id="out-contact">
          <div class="ct"><svg viewBox="0 0 24 24" fill="#f7c731" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z" /></svg><span>06-233 3330 &nbsp;|&nbsp; 019-223 8622</span></div>
          <div class="ct"><svg viewBox="0 0 24 24" fill="#f7c731" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z" /></svg><span>generalinfo@mitc.org.my</span></div>
          <div class="ct"><svg viewBox="0 0 24 24" fill="#f7c731" aria-hidden="true"><circle cx="12" cy="12" r="9.5" fill="none" stroke="#f7c731" stroke-width="2" /><path d="M2.5 12h19M12 2.5c3 3.2 3 15.8 0 19M12 2.5c-3 3.2-3 15.8 0 19" fill="none" stroke="#f7c731" stroke-width="1.6" /></svg><span>site.mitc.org.my</span></div>
        </div>
        <div id="out-addr">Aras 2, Pusat Konvensyen, Kompleks MITC,<br />Jalan Konvensyen, Hang Tuah Jaya, 75450 Ayer Keroh, Melaka</div>
      </div>
      <div id="fx" class="clip" data-start="0" data-duration="{END}" data-track-index="6"><div id="leak"></div><div id="flash"></div><div id="fade"></div></div>
      <audio id="bgm" src="assets/bgm/bed.wav" data-start="0" data-duration="{END}" data-track-index="10" data-volume="1" data-fade-out="1.5"></audio>
    </div>
''')

# ------------------------------------------------------------------ timeline
cfg = dict(B=B, BAR=BAR, DROP=DROP, F=F, END=END, OV=OV, S=S,
           shots=[{k: v for k, v in sh.items() if k in ("id", "t0", "t1", "trans", "pan", "media")} for sh in SHOTS],
           sections=[[s[0], s[1], s[2]] for s in SECTIONS])
JS = open(f"{ROOT}/../timeline.v4.js").read().replace("/*CFG*/", json.dumps(cfg))
A("    <script>\n" + JS + "\n    </script>\n  </body>\n</html>\n")
open(f"{ROOT}/index.html", "w").write("".join(H))
print("shots", len(SHOTS), "sections", {k: r(v) for k, v in S.items()})
