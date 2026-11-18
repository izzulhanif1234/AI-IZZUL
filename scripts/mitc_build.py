"""Build the MITC promo v5 (clean & elegant corporate cut) -> edits/mitc-promo/hf/index.html.

Direction (client): "bersih & elegan" - slow smooth camera, soft cross-dissolves, thin letter-spaced
type, uniform navy/white grade, lots of negative space. No spins/whips/flashes/HUD, no sound effects.
Music: Mixkit "Driving Ambition" (100 BPM, beat 0.6002 s): bed.wav starts at track 26.481 s, drop at
12.004 s, final chord at 50.983 s. (v4 hypermotion builder: see git history.)
"""
import json

ROOT = "/home/user/AI-IZZUL/edits/mitc-promo/hf"
B = 0.6002
BAR = 4 * B
DROP = 5 * BAR             # 12.004
F = 50.983
END = 55.6
XF = 0.3                   # half of a cross-dissolve
r = lambda x: round(x, 3)

MAIN0 = DROP + 2 * BAR     # 16.806
AW = MAIN0 + 10 * BAR      # 40.814
CLOSE = AW + 2 * BAR       # 45.616

# 10 shots, one bar each. (id, media, section, caption, pan) media "v:clip" or "i:file:width"
SHOTS = [
    ("s1", "v:l-tables", "01", "Gala Dinner · Hall B", None),
    ("s2", "v:l-ht-gate", "01", "Pameran Hang Tuah · Hall A", None),
    ("s3", "v:l-ht-houses", "01", "Pameran Hang Tuah · Hall A", None),
    ("s4", "i:ballroom.jpg:2560", "01", "Majlis Rasmi · Dewan Pameran", (-760, -860)),
    ("s5", "i:meeting.jpg:3413", "02", "Bilik Mesyuarat", (-1150, -1300)),
    ("s6", "i:lounge.jpg:2560", "02", "Ruang VIP", (-520, -640)),
    ("s7", "v:l-grand", "03", "Iskandar Shah Grand Ballroom", None),
    ("s8", "v:l-maharani", "03", "Maharani Ballroom", None),
    ("s9", "v:l-akad", "03", "Maharani Ballroom", None),
    ("s10", "v:l-prep", "04", "Perancangan · Dekorasi · Teknikal", None),
]
SECTIONS = {
    "01": ("Dewan Pameran", "Exhibition Halls"),
    "02": ("Konvensyen &amp; Mesyuarat", "Conventions &amp; Meetings"),
    "03": ("Ballroom", "Grand Ballrooms"),
    "04": ("Perkhidmatan Bersepadu", "Integrated Event Services"),
}
shots = []
for i, (sid, media, sec, cap, pan) in enumerate(SHOTS):
    t0 = MAIN0 + i * BAR
    shots.append(dict(id=sid, media=media, sec=sec, cap=cap, pan=pan, t0=r(t0), t1=r(t0 + BAR)))
secs = []
for key in SECTIONS:
    ss = [s for s in shots if s["sec"] == key]
    secs.append(dict(key=key, t0=ss[0]["t0"], t1=ss[-1]["t1"], ids=[s["id"] for s in ss]))

CSS = """
      :root { --navy: #1c2747; --deep: #0f1730; --yellow: #f2c94c; --white: #ffffff; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--deep); }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: var(--deep);
        font-family: Inter, sans-serif; color: var(--white); }
      .clip { position: absolute; inset: 0; }
      .wrap { position: absolute; inset: 0; overflow: hidden; }
      .wrap img.clip { inset: auto; left: 0; top: 0; height: 1920px; }
      video.clip { width: 1080px; height: 1920px; object-fit: cover; }
      /* one grade for every picture: slightly cooler, calmer colour */
      .wrap .clip { filter: saturate(0.78) contrast(1.06) brightness(0.97); }
      .grade { background: linear-gradient(180deg, rgba(15, 23, 48, 0.35) 0%, rgba(15, 23, 48, 0.08) 22%,
          rgba(15, 23, 48, 0.08) 55%, rgba(15, 23, 48, 0.82) 80%, rgba(15, 23, 48, 0.94) 100%); }
      .tint { background: rgba(28, 39, 71, 0.22); mix-blend-mode: multiply; }
      .navy { background: radial-gradient(1200px 1200px at 50% 40%, #22305a 0%, var(--deep) 70%); }

      .k { font-weight: 500; font-size: 22px; letter-spacing: 0.42em; text-transform: uppercase; color: rgba(255,255,255,0.82); }
      .t { font-weight: 300; text-transform: uppercase; letter-spacing: 0.08em; line-height: 1.18; }
      .line { height: 2px; background: var(--yellow); transform-origin: 0 50%; }
      .center { position: absolute; left: 0; right: 0; text-align: center; }

      /* intro A */
      #ia-logo { position: absolute; left: 430px; top: 600px; width: 220px; height: 220px; }
      #ia-logo img, #lg-logo img, #o-logo img { width: 100%; height: 100%; }
      #ia-k { top: 880px; }
      #ia-line { position: absolute; left: 290px; width: 500px; top: 940px; transform-origin: 50% 50%; }
      #ia-name { top: 990px; font-size: 50px; }
      /* intro B / C : bottom-left blocks */
      .blk { position: absolute; left: 90px; right: 90px; top: 1380px; }
      .blk .k { margin-bottom: 22px; }
      .blk .t { font-size: 54px; }
      .blk .line { width: 120px; margin-top: 28px; }
      .stat { position: absolute; left: 90px; right: 90px; }
      .stat .n { font-weight: 200; font-size: 170px; line-height: 1; letter-spacing: -0.01em; }
      .stat .n small { font-size: 54px; font-weight: 300; margin-left: 14px; letter-spacing: 0.06em; }
      .stat .l { margin-top: 10px; font-weight: 400; font-size: 26px; letter-spacing: 0.24em; text-transform: uppercase; color: rgba(255,255,255,0.85); }
      #st1 { top: 470px; } #st2 { top: 860px; }
      #facts { position: absolute; left: 90px; right: 90px; top: 1330px; display: flex; justify-content: space-between; }
      .fact { width: 280px; border-top: 2px solid var(--yellow); padding-top: 22px; }
      .fact b { display: block; font-weight: 200; font-size: 96px; line-height: 1; }
      .fact span { display: block; margin-top: 10px; font-size: 22px; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(255,255,255,0.85); line-height: 1.4; }
      /* logo card */
      #lg-logo { position: absolute; left: 370px; top: 520px; width: 340px; height: 340px; }
      #lg-line { position: absolute; left: 440px; width: 200px; top: 960px; transform-origin: 50% 50%; }
      #lg-t { top: 1010px; font-size: 42px; padding: 0 90px; }
      #lg-en { top: 1240px; font-weight: 300; font-style: italic; font-size: 26px; letter-spacing: 0.06em; color: var(--yellow); }
      /* sections */
      .sec { position: absolute; left: 90px; right: 90px; top: 1390px; }
      .sec .idx { display: flex; align-items: center; gap: 22px; font-weight: 500; font-size: 24px; letter-spacing: 0.3em; color: var(--yellow); }
      .sec .idx .line { width: 90px; }
      .sec .t { margin-top: 22px; font-size: 64px; }
      .sec .en { margin-top: 8px; font-weight: 300; font-style: italic; font-size: 24px; letter-spacing: 0.08em; color: rgba(255,255,255,0.7); }
      .caps { position: relative; margin-top: 34px; height: 40px; }
      .cap { position: absolute; left: 0; top: 0; font-weight: 400; font-size: 26px; letter-spacing: 0.22em; text-transform: uppercase; color: rgba(255,255,255,0.9); white-space: nowrap; }
      /* awards */
      #aw-k { top: 300px; }
      #aw-t { top: 350px; font-size: 64px; letter-spacing: 0.3em; }
      #aw-line { position: absolute; left: 480px; width: 120px; top: 460px; transform-origin: 50% 50%; }
      #v-aw { inset: auto; left: 90px; top: 540px; width: 900px; height: 506px; object-fit: cover; border-radius: 6px; filter: saturate(0.8); }
      .badge { position: absolute; top: 1150px; width: 190px; height: 190px; border-radius: 50%; overflow: hidden; background: #fff; }
      .badge img { width: 100%; height: 100%; object-fit: cover; }
      .badge.photo img { object-position: 50% 45%; transform: scale(1.5); }
      #bd1 { left: 90px; } #bd2 { left: 330px; } #bd3 { left: 570px; } #bd4 { left: 800px; }
      .awl { position: absolute; top: 1380px; font-size: 21px; letter-spacing: 0.08em; line-height: 1.45; color: rgba(255,255,255,0.88); text-align: center; }
      .awl small { display: block; color: var(--yellow); font-size: 19px; letter-spacing: 0.04em; }
      #al1 { left: 70px; width: 470px; } #al2 { left: 550px; width: 230px; } #al3 { left: 790px; width: 220px; }
      /* close */
      #cl-t { top: 1380px; font-size: 62px; }
      #cl-s { top: 1560px; font-weight: 300; font-style: italic; font-size: 30px; letter-spacing: 0.1em; color: var(--yellow); }
      /* outro */
      #o-logo { position: absolute; left: 420px; top: 470px; width: 240px; height: 240px; }
      #o-name { top: 770px; font-size: 30px; letter-spacing: 0.3em; }
      #o-line { position: absolute; left: 480px; width: 120px; top: 840px; transform-origin: 50% 50%; }
      #o-cta { position: absolute; left: 290px; width: 500px; top: 900px; height: 76px; border: 1.5px solid var(--yellow);
        border-radius: 999px; display: flex; align-items: center; justify-content: center;
        font-weight: 500; font-size: 24px; letter-spacing: 0.32em; color: var(--yellow); }
      #o-ct { top: 1050px; font-weight: 300; font-size: 32px; letter-spacing: 0.06em; line-height: 1.75; }
      #o-addr { top: 1280px; font-weight: 300; font-size: 22px; line-height: 1.6; letter-spacing: 0.04em; color: rgba(255,255,255,0.7); padding: 0 120px; }
      #fade { position: absolute; inset: 0; background: var(--deep); opacity: 0; }
"""


def wrap_media(sid, media, start, dur, ms=0.05):
    kind, *rest = media.split(":")
    if kind == "v":
        return (f'<div id="w-{sid}" class="wrap"><video id="m-{sid}" class="clip" src="assets/clips/{rest[0]}.mp4" '
                f'data-start="{start}" data-duration="{dur}" data-media-start="{ms}" data-track-index="0" muted playsinline></video></div>')
    f, w = rest
    return (f'<div id="w-{sid}" class="wrap"><img id="m-{sid}" class="clip" src="assets/img/{f}" data-start="{start}" '
            f'data-duration="{dur}" data-track-index="0" style="width: {w}px" alt="" /></div>')


H = []
A = H.append
A(f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="vendor/gsap.min.js"></script>
    <style>{CSS}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
      <!-- pictures (each in an untimed wrapper; dissolves animate the wrapper) -->
      <div id="bg-navy" class="clip navy" data-start="0" data-duration="{END}" data-track-index="9"></div>
""")
A("      " + wrap_media("ext", "i:exterior-hi.jpg:3413", r(2 * BAR - XF), r(BAR + 2 * XF)) + "\n")
A("      " + wrap_media("aer", "i:aerial.jpg:3413", r(3 * BAR - XF), r(2 * BAR + 2 * XF)) + "\n")
for s in shots:
    start = r(s["t0"] - XF)
    A("      " + wrap_media(s["id"], s["media"], start, r(s["t1"] + XF - start)) + "\n")
A("      " + wrap_media("cl", "i:exterior-hi.jpg:3413", r(CLOSE - XF), r(F - CLOSE + 2 * XF)) + "\n")
A(f'''      <div id="tint" class="clip tint" data-start="{r(2 * BAR - XF)}" data-duration="{r(F - 2 * BAR + 2 * XF)}" data-track-index="2"></div>
      <div id="grade" class="clip grade" data-start="{r(2 * BAR - XF)}" data-duration="{r(F - 2 * BAR + 2 * XF)}" data-track-index="2"></div>
      <div id="p-aw" class="clip navy" data-start="{r(AW - XF)}" data-duration="{r(CLOSE - AW + 2 * XF)}" data-track-index="3"></div>
      <video id="v-aw" class="clip" src="assets/video/award.mp4" data-start="{r(AW)}" data-duration="{r(CLOSE - AW)}" data-media-start="0.6" data-track-index="4" muted playsinline></video>

      <!-- type -->
      <div id="t-ia" class="clip" data-start="0" data-duration="{r(2 * BAR)}" data-track-index="5">
        <div id="ia-logo"><img src="assets/img/logo-globe.png" alt="MITC" /></div>
        <div id="ia-k" class="center k">Selamat datang ke</div>
        <div id="ia-line" class="line"></div>
        <div id="ia-name" class="center t">Melaka International<br />Trade Centre</div>
      </div>
      <div id="t-ib" class="clip" data-start="{r(2 * BAR)}" data-duration="{r(BAR)}" data-track-index="5">
        <div class="blk"><div class="k">Ayer Keroh · Melaka</div><div class="t">Pusat Konvensyen &amp; Pameran<br />Bertaraf Antarabangsa</div><div class="line"></div></div>
      </div>
      <div id="t-ic" class="clip" data-start="{r(3 * BAR)}" data-duration="{r(2 * BAR)}" data-track-index="5">
        <div id="st1" class="stat"><div class="n"><span id="n1">0.0</span><small>EKAR</small></div><div class="l">Kompleks MITC</div></div>
        <div id="st2" class="stat"><div class="n"><span id="n2">0</span><small>M²</small></div><div class="l">Ruang mesyuarat &amp; pameran fleksibel</div></div>
        <div id="facts">
          <div class="fact"><b>3</b><span>Dewan<br />Pameran</span></div>
          <div class="fact"><b>6</b><span>Bilik<br />Mesyuarat</span></div>
          <div class="fact"><b>1</b><span>Grand<br />Ballroom</span></div>
        </div>
      </div>
      <div id="t-lg" class="clip" data-start="{r(DROP)}" data-duration="{r(2 * BAR)}" data-track-index="5">
        <div id="lg-logo"><img src="assets/img/logo-globe.png" alt="MITC" /></div>
        <div id="lg-line" class="line"></div>
        <div id="lg-t" class="center t">Pusat Konvensyen &amp; Acara Perniagaan Bertaraf Antarabangsa</div>
        <div id="lg-en" class="center">Premier International Convention &amp; Business Events Centre</div>
      </div>
''')
for sc in secs:
    title, en = SECTIONS[sc["key"]]
    A(f'      <div id="t-{sc["key"]}" class="clip" data-start="{r(sc["t0"])}" data-duration="{r(sc["t1"] - sc["t0"])}" data-track-index="5">')
    A(f'        <div class="sec"><div class="idx">{sc["key"]}<div class="line"></div></div><div class="t">{title}</div><div class="en">{en}</div><div class="caps">')
    for s in shots:
        if s["sec"] == sc["key"]:
            A(f'          <div id="cap-{s["id"]}" class="cap">{s["cap"]}</div>')
    A("        </div></div>\n      </div>")
A(f'''      <div id="t-aw" class="clip" data-start="{r(AW)}" data-duration="{r(CLOSE - AW)}" data-track-index="5">
        <div id="aw-k" class="center k">Pengiktirafan</div>
        <div id="aw-t" class="center t">Diiktiraf</div>
        <div id="aw-line" class="line"></div>
        <div id="bd1" class="badge"><img src="assets/img/asean-exhibition.png" alt="" /></div>
        <div id="bd2" class="badge"><img src="assets/img/asean-meeting.png" alt="" /></div>
        <div id="bd3" class="badge"><img src="assets/img/brandlaureate.png" alt="" /></div>
        <div id="bd4" class="badge photo"><img src="assets/img/cmiea.jpg" alt="" /></div>
        <div id="al1" class="awl">ASEAN MICE Venue Standard<small>Exhibition Venue &amp; Meeting Room · 2026–2028</small></div>
        <div id="al2" class="awl">BrandLaureate BestBrands<small>MICE Venue · 2025–2026</small></div>
        <div id="al3" class="awl">CMIEA 2025<small>Excellence Service Sector</small></div>
      </div>
      <div id="t-cl" class="clip" data-start="{r(CLOSE)}" data-duration="{r(F - CLOSE)}" data-track-index="5">
        <div id="cl-t" class="center t">Lebih daripada<br />sebuah venue</div>
        <div id="cl-s" class="center">Think MICE, Think MITC.</div>
      </div>
      <div id="t-out" class="clip" data-start="{r(F)}" data-duration="{r(END - F)}" data-track-index="5">
        <div id="o-logo"><img src="assets/img/logo-globe.png" alt="MITC" /></div>
        <div id="o-name" class="center t">Melaka International Trade Centre</div>
        <div id="o-line" class="line"></div>
        <div id="o-cta">HUBUNGI KAMI</div>
        <div id="o-ct" class="center">06-233 3330 &nbsp;·&nbsp; 019-223 8622<br />generalinfo@mitc.org.my<br />site.mitc.org.my</div>
        <div id="o-addr" class="center">Aras 2, Pusat Konvensyen, Kompleks MITC, Jalan Konvensyen, Hang Tuah Jaya, 75450 Ayer Keroh, Melaka</div>
      </div>
      <div id="fx" class="clip" data-start="0" data-duration="{END}" data-track-index="6"><div id="fade"></div></div>
      <audio id="bgm" src="assets/bgm/bed.wav" data-start="0" data-duration="{END}" data-track-index="10" data-volume="1" data-fade-out="1.8"></audio>
    </div>
''')

JS = """
      (function () {
        const C = /*CFG*/;
        const { B, BAR, DROP, F, END, XF, AW, CLOSE } = C;
        const tl = gsap.timeline({ paused: true });
        const E = "sine.inOut";
        // soft cross-dissolve: incoming wrapper fades in over the cut
        const dissolveIn = (w, t, d) => tl.fromTo(w, { opacity: 0 }, { opacity: 1, duration: d || 2 * XF, ease: E, immediateRender: false }, t - (d || 2 * XF) / 2);
        const fadeUp = (s, t, d) => tl.from(s, { y: 24, opacity: 0, duration: d || 0.9, ease: "power2.out" }, t);
        const fadeOut = (s, t, d) => tl.to(s, { opacity: 0, duration: d || 0.5, ease: E }, t);
        const drawLine = (s, t) => tl.from(s, { scaleX: 0, duration: 1.0, ease: "power2.inOut" }, t);
        // slow camera: gentle push (and a small pan on stills) across the whole shot
        const drift = (s, t0, t1, pan) => tl.fromTo(s, { x: pan ? pan[0] : 0, scale: 1.0, transformOrigin: "50% 50%" },
          { x: pan ? pan[1] : 0, scale: 1.06, duration: t1 - t0 + 2 * XF, ease: "none", immediateRender: false }, t0 - XF);
        const fmt = (n) => Math.round(n).toLocaleString("en-US");

        // ---------- intro A (0 - 4.8): navy, logo, name ----------
        tl.from("#ia-logo", { opacity: 0, scale: 0.94, duration: 1.4, ease: "power2.out" }, 0.3);
        fadeUp("#ia-k", B * 2);
        drawLine("#ia-line", B * 2 + 0.2);
        fadeUp("#ia-name", BAR, 1.2);
        fadeOut("#t-ia > *", 2 * BAR - 0.6, 0.5);
        // ---------- intro B (4.8 - 7.2): exterior ----------
        dissolveIn("#w-ext", 2 * BAR, 0.8);
        tl.fromTo("#m-ext", { x: -1330, scale: 1.0, transformOrigin: "50% 50%" }, { x: -1290, scale: 1.07, duration: BAR + 2 * XF, ease: "none", immediateRender: false }, 2 * BAR - XF);
        fadeUp("#t-ib .k", 2 * BAR + 0.3);
        fadeUp("#t-ib .t", 2 * BAR + 0.55, 1.0);
        drawLine("#t-ib .line", 2 * BAR + 0.9);
        fadeOut("#t-ib .blk", 3 * BAR - 0.45, 0.4);
        // ---------- intro C (7.2 - 12.0): aerial + facts ----------
        dissolveIn("#w-aer", 3 * BAR, 0.8);
        tl.fromTo("#m-aer", { x: -1150, scale: 1.04, transformOrigin: "50% 50%" }, { x: -1450, scale: 1.0, duration: 2 * BAR + 2 * XF, ease: "none", immediateRender: false }, 3 * BAR - XF);
        const c1 = { v: 0 }, c2 = { v: 0 };
        fadeUp("#st1", 3 * BAR + 0.3);
        tl.to(c1, { v: 3.1, duration: 1.2, ease: "power2.out", onUpdate: () => (document.getElementById("n1").textContent = c1.v.toFixed(1)) }, 3 * BAR + 0.3);
        fadeUp("#st2", 3 * BAR + 2 * B);
        tl.to(c2, { v: 13090, duration: 1.2, ease: "power2.out", onUpdate: () => (document.getElementById("n2").textContent = fmt(c2.v)) }, 3 * BAR + 2 * B);
        tl.from(".fact", { y: 24, opacity: 0, duration: 0.8, ease: "power2.out", stagger: B }, 4 * BAR);
        fadeOut("#t-ic > *", DROP - 0.7, 0.5);
        tl.to("#w-aer", { opacity: 0, duration: 0.7, ease: E }, DROP - 0.7);
        // ---------- logo card on the drop ----------
        tl.from("#lg-logo", { opacity: 0, scale: 0.92, duration: 1.2, ease: "power2.out" }, DROP);
        drawLine("#lg-line", DROP + 2 * B);
        fadeUp("#lg-t", DROP + 3 * B, 1.0);
        fadeUp("#lg-en", DROP + 5 * B, 0.9);
        fadeOut("#t-lg > *", DROP + 2 * BAR - 0.6, 0.5);
        // ---------- main: one shot per bar, soft dissolves ----------
        C.shots.forEach((s, i) => {
          dissolveIn("#w-" + s.id, s.t0, i === 0 ? 0.9 : 2 * XF);
          drift("#m-" + s.id, s.t0, s.t1, s.pan);
        });
        C.secs.forEach((sc) => {
          const p = "#t-" + sc.key + " ";
          fadeUp(p + ".idx", sc.t0 + 0.35, 0.8);
          drawLine(p + ".idx .line", sc.t0 + 0.45);
          fadeUp(p + ".t", sc.t0 + 0.55, 1.0);
          fadeUp(p + ".en", sc.t0 + 0.8, 0.9);
          sc.ids.forEach((id, j) => {
            const s = C.shots.find((x) => x.id === id);
            tl.fromTo("#cap-" + id, { opacity: 0, x: -14 }, { opacity: 1, x: 0, duration: 0.6, ease: "power2.out", immediateRender: false }, s.t0 + (j === 0 ? 1.0 : 0.25));
            tl.to("#cap-" + id, { opacity: 0, duration: 0.3, ease: E }, s.t1 - 0.3);
            tl.set("#cap-" + id, { opacity: 0 }, 0);
          });
          fadeOut(p + ".sec", sc.t1 - 0.45, 0.4);
        });
        // ---------- awards ----------
        tl.fromTo("#p-aw", { opacity: 0 }, { opacity: 1, duration: 0.8, ease: E, immediateRender: false }, AW - 0.4);
        fadeUp("#aw-k", AW + 0.3);
        fadeUp("#aw-t", AW + 0.5, 1.0);
        drawLine("#aw-line", AW + 0.8);
        tl.from("#v-aw", { opacity: 0, y: 30, duration: 1.0, ease: "power2.out" }, AW + 0.6);
        ["#bd1", "#bd2", "#bd3", "#bd4"].forEach((s, i) => tl.from(s, { opacity: 0, scale: 0.9, duration: 0.8, ease: "power2.out" }, AW + 1.4 + i * B));
        ["#al1", "#al2", "#al3"].forEach((s, i) => fadeUp(s, AW + 1.8 + i * B * 1.3, 0.7));
        fadeOut(["#t-aw > *", "#v-aw"], CLOSE - 0.6, 0.5);
        // ---------- close ----------
        dissolveIn("#w-cl", CLOSE, 0.9);
        tl.fromTo("#m-cl", { x: -1300, scale: 1.1, transformOrigin: "50% 50%" }, { x: -1250, scale: 1.0, duration: F - CLOSE + 2 * XF, ease: "power1.out", immediateRender: false }, CLOSE - XF);
        fadeUp("#cl-t", CLOSE + 0.6, 1.2);
        fadeUp("#cl-s", CLOSE + 2.4, 1.0);
        fadeOut("#t-cl > *", F - 0.6, 0.5);
        tl.to(["#w-cl", "#tint", "#grade"], { opacity: 0, duration: 0.8, ease: E }, F - 0.5);
        // ---------- outro ----------
        tl.from("#o-logo", { opacity: 0, scale: 0.94, duration: 1.2, ease: "power2.out" }, F + 0.1);
        fadeUp("#o-name", F + 0.6);
        drawLine("#o-line", F + 0.9);
        fadeUp("#o-cta", F + 1.2, 0.8);
        fadeUp("#o-ct", F + 1.6, 0.9);
        fadeUp("#o-addr", F + 2.0, 0.9);
        tl.to("#fade", { opacity: 1, duration: 0.8, ease: "power1.in" }, END - 0.8);
        window.__timelines = window.__timelines || {};
        window.__timelines["main"] = tl;
      })();
"""
cfg = dict(B=B, BAR=BAR, DROP=DROP, F=F, END=END, XF=XF, AW=AW, CLOSE=CLOSE,
           shots=[{k: s[k] for k in ("id", "t0", "t1", "pan")} for s in shots], secs=secs)
A("    <script>" + JS.replace("/*CFG*/", json.dumps(cfg)) + "    </script>\n  </body>\n</html>\n")
open(f"{ROOT}/index.html", "w").write("".join(H))
print("main", r(MAIN0), "awards", r(AW), "close", r(CLOSE), "final", F, "end", END)
