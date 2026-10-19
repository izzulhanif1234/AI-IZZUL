"""Build the Hotel MITC intro video (HyperFrames) -> edits/mitc-pengenalan/hf/index.html

usage: python3 scripts/mitc_build.py

v4, "digital experience" UI hypermotion: one continuous 3D camera through floating glass
panels, and a cursor that actually uses them — company timeline, location map with a
route from the Ayer Keroh toll, KPI dashboard, a hotel app window whose tabs (Fasiliti,
Dewan & Acara, Santapan, Bilik & Suite) are clicked, cards that expand into full-screen AI
camera-move clips, a room selector with live previews, and a booking widget.
Silent (music is added on the platform).  Styles: edits/mitc-pengenalan/style-v4.css.
Earlier cuts: scripts/mitc_build_v3.py (hypermotion), scripts/mitc_build_v2.py (luxury).
"""
import json
import os

HF = os.path.join(os.path.dirname(__file__), "..", "edits", "mitc-pengenalan", "hf")
W, H = 1920, 1080
P3 = 1800          # transformPerspective for the 3D camera moves

clips, tl = [], []


def at(t):
    return f"{t:.3f}"


def js(d):
    parts = []
    for k, v in d.items():
        parts.append(f"{k}: {v[1:]}" if isinstance(v, str) and v.startswith("@") else f"{k}: {json.dumps(v)}")
    return "{ " + ", ".join(parts) + " }"


def tw(sel, frm, to, start):
    to = dict(to)
    to.setdefault("ease", "power3.out")
    to["immediateRender"] = False
    tl.append(f"tl.fromTo({json.dumps(sel)}, {js(frm)}, {js(to)}, {at(start)});")


def clip(cid, start, end, inner, cls="", track=1, style=""):
    st = f' style="{style}"' if style else ""
    clips.append(f'<div id="{cid}" class="clip {cls}" data-start="{at(start)}" '
                 f'data-duration="{at(end - start)}" data-track-index="{track}"{st}>{inner}</div>')


def video(cid, src, start, end, cls="", style="", media_start=0.0, track=2):
    st = f' style="{style}"' if style else ""
    clips.append(f'<video id="{cid}" class="clip vclip {cls}" src="assets/video/{src}.mp4" data-start="{at(start)}" '
                 f'data-duration="{at(end - start)}" data-media-start="{media_start}" data-hf-media-start-basis="local" '
                 f'data-track-index="{track}"{st} muted playsinline></video>')


def chars(text, cls="ch"):
    out = []
    for word in text.split(" "):
        if word.startswith("&"):
            out.append(f'<span class="w"><span class="{cls}">{word}</span></span>')
            continue
        out.append('<span class="w">' + "".join(f'<span class="{cls}">{c}</span>' for c in word) + "</span>")
    return " ".join(out)


def roll(cid, text, start, stagger=0.08, dur=1.5):
    html, k = [], 0
    for c in text:
        if c.isdigit():
            stack = "".join(f"<span>{n % 10}</span>" for n in range(20))
            html.append(f'<span class="roll"><span class="roll-s" id="{cid}-d{k}">{stack}</span></span>')
            tw(f"#{cid}-d{k}", {"yPercent": 0}, {"yPercent": -(10 + int(c)) / 20 * 100, "duration": dur + k * 0.06, "ease": "expo.out"}, start + k * stagger)
            k += 1
        else:
            html.append(f'<span class="roll-c">{c}</span>')
    return "".join(html)


def panel_in(sels, t, d=1, stagger=0.1, dur=1.3):
    """Panels arrive in 3D, as if the camera is travelling sideways onto them."""
    for i, s in enumerate(sels):
        tw(s, {"x": 760 * d, "z": -500, "rotationY": -32 * d, "opacity": 0, "transformPerspective": P3},
           {"x": 0, "z": 0, "rotationY": 0, "opacity": 1, "transformPerspective": P3, "duration": dur, "ease": "power3.out"}, t + i * stagger)


def panel_out(sels, t, d=1, stagger=0.06, dur=1.0):
    for i, s in enumerate(sels):
        tw(s, {"x": 0, "z": 0, "rotationY": 0, "opacity": 1, "transformPerspective": P3},
           {"x": -760 * d, "z": -500, "rotationY": 32 * d, "opacity": 0, "transformPerspective": P3, "duration": dur, "ease": "power3.in"}, t + i * stagger)


def hover(el, glow, t_in, t_out, lift=12, scale=1.03):
    tw(el, {"y": 0, "scale": 1}, {"y": -lift, "scale": scale, "duration": 0.4, "ease": "power2.out"}, t_in)
    tw(el, {"y": -lift, "scale": scale}, {"y": 0, "scale": 1, "duration": 0.45, "ease": "power2.inOut"}, t_out)
    if glow:
        tw(glow, {"opacity": 0}, {"opacity": 1, "duration": 0.35, "ease": "power2.out"}, t_in)
        tw(glow, {"opacity": 1}, {"opacity": 0, "duration": 0.4, "ease": "power2.inOut"}, t_out)


# ---------------------------------------------------------------- cursor (one, global)
CUR = {"x": 1700, "y": 1000}


def cshow(t, x, y):
    tw("#cursor", {"x": CUR["x"], "y": CUR["y"]}, {"x": x, "y": y, "duration": 0.02, "ease": "none"}, t - 0.03)
    CUR.update(x=x, y=y)
    tw("#cursor", {"opacity": 0}, {"opacity": 1, "duration": 0.3, "ease": "none"}, t)


def chide(t):
    tw("#cursor", {"opacity": 1}, {"opacity": 0, "duration": 0.25, "ease": "none"}, t)


def cmove(t0, t1, x, y):
    """Move the cursor tip to (x, y) between t0 and t1."""
    tw("#cursor", {"x": CUR["x"], "y": CUR["y"]}, {"x": x, "y": y, "duration": round(t1 - t0, 3), "ease": "power2.inOut"}, t0)
    CUR.update(x=x, y=y)


def cclick(t):
    tw("#cur-i", {"scale": 1}, {"scale": 0.8, "duration": 0.1, "ease": "power2.out"}, t)
    tw("#cur-i", {"scale": 0.8}, {"scale": 1, "duration": 0.22, "ease": "power2.out"}, t + 0.1)
    tw("#cur-r", {"scale": 0, "opacity": 0.9}, {"scale": 3.6, "opacity": 0, "duration": 0.65, "ease": "power2.out"}, t)


# ---------------------------------------------------------------- full-screen expansion of a card
def expand(cid, src, rect, t_open, t_close, t_end, kicker, title, sub, media_start=0.0):
    """A card at rect (x, y, w, h; 16:9) grows into a full-screen AI clip, then (optionally) shrinks back."""
    x, y, w, _ = rect
    s = round(w / 1920, 4)
    video(cid, src, t_open, t_end, cls="xv", media_start=media_start, track=12)
    tw(f"#{cid}", {"x": x, "y": y, "scale": s}, {"x": 0, "y": 0, "scale": 1, "duration": 0.85, "ease": "expo.inOut"}, t_open)
    cap_end = (t_close or t_end) - 0.05
    clip(f"{cid}-cap", t_open + 0.7, cap_end, (
        '<div class="xcap-sh"></div><div class="xcap">'
        f'<div class="m"><div class="xcap-k" id="{cid}-k"><span></span>{kicker}</div></div>'
        f'<div class="xcap-t" id="{cid}-t">{chars(title)}</div>'
        f'<div class="m"><div class="xcap-s" id="{cid}-s">{sub}</div></div></div>'), "ovl xc", 13)
    tw(f"#{cid}-cap .xcap-sh", {"opacity": 0}, {"opacity": 1, "duration": 0.6, "ease": "power2.out"}, t_open + 0.7)
    tw(f"#{cid}-k", {"yPercent": 110}, {"yPercent": 0, "duration": 0.7, "ease": "expo.out"}, t_open + 0.9)
    tw(f"#{cid}-t .ch", {"yPercent": 110, "opacity": 0}, {"yPercent": 0, "opacity": 1, "duration": 0.8, "ease": "expo.out", "stagger": 0.025}, t_open + 1.0)
    tw(f"#{cid}-s", {"yPercent": 110}, {"yPercent": 0, "duration": 0.8, "ease": "expo.out"}, t_open + 1.4)
    tw(f"#{cid}-cap .xcap", {"x": 0}, {"x": 18, "duration": round(cap_end - t_open - 0.7, 3), "ease": "none"}, t_open + 0.7)
    tw(f"#{cid}-cap", {"opacity": 1}, {"opacity": 0, "duration": 0.35, "ease": "power2.in"}, cap_end - 0.4)
    if t_close:
        tw(f"#{cid}", {"x": 0, "y": 0, "scale": 1}, {"x": x, "y": y, "scale": s, "duration": 0.75, "ease": "expo.inOut"}, t_close)


ICON = {
    "pin": '<svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.6A2.6 2.6 0 1 1 12 6.4a2.6 2.6 0 0 1 0 5.2z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>',
    "web": '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm6.9 6h-3a15.6 15.6 0 0 0-1.4-3.6A8 8 0 0 1 18.9 8zM12 4c.8 1.2 1.5 2.5 1.9 4h-3.8c.4-1.4 1.1-2.8 1.9-4zM4.3 14a8.2 8.2 0 0 1 0-4h3.4a16.5 16.5 0 0 0 0 4H4.3zm.8 2h3c.3 1.3.8 2.5 1.4 3.6A8 8 0 0 1 5.1 16zm3-8h-3a8 8 0 0 1 4.4-3.6C8.9 5.5 8.4 6.7 8.1 8zM12 20c-.8-1.2-1.5-2.5-1.9-4h3.8c-.4 1.4-1.1 2.8-1.9 4zm2.3-6H9.7a14.7 14.7 0 0 1 0-4h4.6a14.7 14.7 0 0 1 0 4zm.3 5.6c.6-1.1 1.1-2.3 1.4-3.6h3a8 8 0 0 1-4.4 3.6zm1.7-5.6a16.5 16.5 0 0 0 0-4h3.4a8.2 8.2 0 0 1 0 4h-3.4z"/></svg>',
    "cal": '<svg viewBox="0 0 24 24"><path d="M7 2v2H5a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-2V2h-2v2H9V2H7zm-2 7h14v10H5V9z"/></svg>',
    "user": '<svg viewBox="0 0 24 24"><path d="M12 12a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9zm0 2c-4.4 0-8 2.2-8 5v2h16v-2c0-2.8-3.6-5-8-5z"/></svg>',
    "bed": '<svg viewBox="0 0 24 24"><path d="M3 6v13h2v-2h14v2h2v-6a4 4 0 0 0-4-4h-6v5H5V6H3zm5 6a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>',
    "check": '<svg viewBox="0 0 24 24"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.5-1.5z"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6-1.4-1.4 4.6-4.6-4.6-4.6z"/></svg>',
}

# ================================================================ TIMELINE
T = dict(intro=0.0, corp=6.5, lok=15.0, dash=23.5, app=30.5, book=83.2, end=90.8, fin=96.7)
TOTAL = T["fin"]

# ---- persistent background: deep navy, drifting light orbs, perspective grid floor, bokeh
dots = []
seed = 11
for i in range(26):
    seed = (seed * 1103515245 + 12345) % 2147483648
    x = seed % 1920
    seed = (seed * 1103515245 + 12345) % 2147483648
    y = seed % 1080
    sz = 4 + (seed % 18)
    dots.append(f'<span class="pt{" gold" if i % 3 == 0 else ""}" id="pt{i}" style="left:{x}px;top:{y}px;width:{sz}px;height:{sz}px"></span>')
    tw(f"#pt{i}", {"y": 0}, {"y": -(80 + (seed % 160)), "duration": TOTAL, "ease": "none"}, 0)
clip("bg", 0, TOTAL, (
    '<div class="orb orb-a" id="orb-a"></div><div class="orb orb-b" id="orb-b"></div><div class="orb orb-c" id="orb-c"></div>'
    '<div class="floor-w"><div class="floor" id="floor"></div></div>' + "".join(dots)), "bg", 0)
tw("#orb-a", {"x": 0, "y": 0}, {"x": 700, "y": 200, "duration": TOTAL, "ease": "sine.inOut"}, 0)
tw("#orb-b", {"x": 0, "y": 0}, {"x": -600, "y": -150, "duration": TOTAL, "ease": "sine.inOut"}, 0)
tw("#orb-c", {"x": 0, "y": 0}, {"x": 300, "y": -260, "duration": TOTAL, "ease": "sine.inOut"}, 0)
# the floor slides at every camera move (parallax of the "world")
FLOOR = [0]


def travel(t, dx=-480):
    tw("#floor", {"x": FLOOR[0]}, {"x": FLOOR[0] + dx, "duration": 1.4, "ease": "power3.inOut"}, t)
    FLOOR[0] += dx


# ---- 0. intro: company card, then the camera flies through it into the hotel's "site"
i1 = T["corp"]
clip("intro", 0, i1 + 0.6, (
    '<div class="glass i-card" id="i-card"><div class="plate" id="i-plate"><img src="assets/img/mcorp-hotel-logo.png" alt="M\'Corp Hotel Sdn. Bhd."/>'
    '<span class="sheen" id="i-sh"></span></div><div class="i-cap" id="i-cap">ANAK SYARIKAT MCORP</div></div>'
    '<div class="glass win hero" id="hero"><div class="bar"><i></i><i></i><i></i><div class="url">mitchotel.com.my</div></div>'
    '<div class="hero-img"><img id="hero-img" src="assets/img/ext-night.jpg" alt=""/><div class="hero-sh"></div></div>'
    '<div class="hero-txt"><div class="m"><div class="hero-k" id="hero-k">SELAMAT DATANG KE</div></div>'
    f'<div class="hero-t" id="hero-t">{chars("HOTEL MITC")}</div>'
    f'<div class="hero-s" id="hero-s">{chars("AYER KEROH · MELAKA")}</div>'
    '<div class="hero-row"><span class="stars" id="hero-st">&#9733;&#9733;&#9733;&#9733;</span><span class="pill" id="hero-pill">Hotel bertaraf 4 bintang</span></div></div></div>'), "", 3)
tw("#i-card", {"scale": 0.8, "rotationX": 35, "opacity": 0, "transformPerspective": P3},
   {"scale": 1, "rotationX": 0, "opacity": 1, "transformPerspective": P3, "duration": 1.4, "ease": "expo.out"}, 0.3)
tw("#i-sh", {"xPercent": -150}, {"xPercent": 450, "duration": 1.1, "ease": "power2.inOut"}, 1.3)
tw("#i-cap", {"opacity": 0, "y": 14}, {"opacity": 1, "y": 0, "duration": 0.8}, 1.1)
tw("#i-card", {"z": 0, "opacity": 1, "transformPerspective": P3}, {"z": 900, "opacity": 0, "transformPerspective": P3, "duration": 0.9, "ease": "power3.in"}, 2.6)
tw("#hero", {"z": -1200, "rotationX": 28, "opacity": 0, "transformPerspective": P3},
   {"z": 0, "rotationX": 0, "opacity": 1, "transformPerspective": P3, "duration": 1.6, "ease": "expo.out"}, 3.0)
tw("#hero-img", {"scale": 1.3}, {"scale": 1.06, "duration": 3.6, "ease": "power2.out"}, 3.0)
tw("#hero-k", {"yPercent": 110}, {"yPercent": 0, "duration": 0.7, "ease": "expo.out"}, 3.8)
tw("#hero-t .ch", {"yPercent": 110, "opacity": 0}, {"yPercent": 0, "opacity": 1, "duration": 0.8, "ease": "expo.out", "stagger": 0.04}, 3.9)
tw("#hero-s .ch", {"opacity": 0, "x": -12}, {"opacity": 1, "x": 0, "duration": 0.5, "ease": "expo.out", "stagger": 0.02}, 4.5)
tw(["#hero-st", "#hero-pill"], {"opacity": 0, "y": 16}, {"opacity": 1, "y": 0, "duration": 0.7, "ease": "back.out(1.8)", "stagger": 0.12}, 4.9)
panel_out(["#hero"], i1 - 0.4)
travel(i1 - 0.4)

# ---- 1. korporat: about panel, company timeline, photo card
c0, c1 = T["corp"], T["lok"]
clip("corp", c0 - 0.4, c1 + 0.6, (
    '<div class="glass p-about" id="p-about"><div class="plate sm"><img src="assets/img/mcorp-hotel-logo.png" alt="M\'Corp Hotel Sdn. Bhd."/></div>'
    '<div class="kick">PROFIL SYARIKAT</div><div class="h2">Anak syarikat MCORP</div>'
    '<div class="body">M&#8217;Corp Hotel Sdn. Bhd. ditubuhkan oleh MCORP pada 15 November 2016 dan dipertanggungjawabkan '
    'mengurus serta mengendalikan operasi Hotel MITC, Ayer Keroh, Melaka.</div></div>'
    '<div class="glass p-time" id="p-time"><div class="kick">SEJARAH RINGKAS</div>'
    '<div class="tl-line"><div class="tl-fill" id="tl-fill"></div></div>'
    f'<div class="tl-node n1" id="tn1"><b>{roll("tld", "15.11.2016", c0 + 1.6, dur=1.3)}</b><span>Ditubuhkan oleh MCORP</span></div>'
    '<div class="tl-node n2" id="tn2"><i id="tn2-dot"></i><b>KINI</b><span>Mengurus Hotel MITC</span></div>'
    '<div class="tip" id="tip"><b>Hotel MITC</b><span>188 bilik &#183; bertaraf 4 bintang</span></div></div>'
    '<div class="glass p-photo" id="p-photo"><img id="pp-img" src="assets/img/ext-wide.jpg" alt=""/><div class="pp-glow" id="pp-g"></div>'
    '<div class="pp-l"><b>Hotel MITC</b><span>Ayer Keroh, Melaka</span></div></div>'), "", 3)
panel_in(["#p-about", "#p-time", "#p-photo"], c0 - 0.4)
tw("#tl-fill", {"scaleX": 0}, {"scaleX": 1, "duration": 1.6, "ease": "power2.inOut"}, c0 + 2.6)
tw("#tn2-dot", {"scale": 0}, {"scale": 1, "duration": 0.5, "ease": "back.out(3)"}, c0 + 4.1)
tw("#pp-img", {"scale": 1.25}, {"scale": 1.05, "duration": 8.5, "ease": "power2.out"}, c0)
cshow(c0 + 3.6, 1780, 1010)
cmove(c0 + 3.7, c0 + 4.6, 1668, 418)
tw("#tn2", {"scale": 1}, {"scale": 1.08, "duration": 0.35, "ease": "power2.out"}, c0 + 4.6)
tw("#tip", {"opacity": 0, "y": 16, "scale": 0.9}, {"opacity": 1, "y": 0, "scale": 1, "duration": 0.5, "ease": "back.out(2)"}, c0 + 4.7)
tw("#tip", {"opacity": 1}, {"opacity": 0, "duration": 0.3}, c0 + 6.2)
tw("#tn2", {"scale": 1.08}, {"scale": 1, "duration": 0.35}, c0 + 6.2)
cmove(c0 + 6.2, c0 + 7.0, 1372, 736)
hover("#p-photo", "#pp-g", c0 + 6.9, c0 + 8.1, lift=8, scale=1.02)
panel_out(["#p-about", "#p-time", "#p-photo"], c1 - 0.4)
travel(c1 - 0.4)

# ---- 2. lokasi: real OSM map of Ayer Keroh (scripts/mitc_map.py), real OSRM route from the toll, click the hotel pin
l0, l1 = T["lok"], T["dash"]
MX, MY = 210, 130      # map panel origin on screen
MAP = json.load(open(os.path.join(HF, "assets", "map.json")))
(tx, ty), (hx, hy), (mx_, my_) = MAP["toll"], MAP["hotel"], MAP["mitc"]
rpts = " ".join(f"{x},{y}" for x, y in MAP["route"])
rL, (cx_, cy_) = MAP["route_len"], MAP["route_mid"]
svg = (f'<svg class="map-svg" viewBox="0 0 1500 820" width="1500" height="820">'
       f'<polyline id="route-glow" points="{rpts}" class="route-glow" style="stroke-dasharray:{rL};stroke-dashoffset:{rL}"/>'
       f'<polyline id="route" points="{rpts}" class="route" style="stroke-dasharray:{rL};stroke-dashoffset:{rL}"/></svg>')
tw(["#route", "#route-glow"], {"strokeDashoffset": rL}, {"strokeDashoffset": 0, "duration": 2.0, "ease": "power2.inOut"}, l0 + 2.6)
clip("lok", l0 - 0.4, l1 + 0.6, (
    '<div class="glass p-map" id="p-map"><div class="map-in" id="map-in" style="transform-origin:' + f'{hx}px {hy}px' + '">'
    '<img class="map-img" src="assets/img/map-ayerkeroh.jpg" alt="Peta Ayer Keroh"/>' + svg +
    f'<div class="mk toll" id="mk-toll" style="left:{tx}px;top:{ty}px"><i></i><span>Plaza Tol Air Keroh</span></div>'
    f'<div class="mk blue sm left" id="mk-mitc" style="left:{mx_}px;top:{my_}px"><i></i><span>MITC</span></div>'
    f'<div class="mk gold right" id="mk-hotel" style="left:{hx}px;top:{hy}px"><b class="pulse" id="pulse"></b>' + ICON["pin"] + '<span>Hotel MITC</span></div>'
    f'<div class="route-chip" id="r-chip" style="left:{cx_ + 40}px;top:{cy_ - 22}px">{MAP["km"]} km &#183; &#177; 10 minit dari tol</div>'
    f'<div class="pop" id="pop" style="left:{hx - 450}px;top:{hy - 400}px"><img src="assets/img/ext-day.jpg" alt=""/>'
    '<b>Hotel MITC</b><span>Bertentangan Pusat Dagangan Antarabangsa Melaka (MITC)</span><em>&#9733;&#9733;&#9733;&#9733;</em></div></div>'
    '<div class="map-title"><div class="kick">LOKASI STRATEGIK</div><div class="h2">Ayer Keroh, Melaka</div></div>'
    '<div class="map-attr">Data peta &#169; penyumbang OpenStreetMap</div></div>'), "", 3)
panel_in(["#p-map"], l0 - 0.4)
tw("#map-in", {"scale": 1.12}, {"scale": 1, "duration": 3.6, "ease": "power2.out"}, l0 - 0.4)
for i, (m, tt) in enumerate([("#mk-toll", 1.9), ("#mk-hotel", 2.2), ("#mk-mitc", 2.5)]):
    tw(m, {"y": -120, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.8, "ease": "bounce.out"}, l0 + tt)
tw("#pulse", {"scale": 0.3, "opacity": 0.9}, {"scale": 3, "opacity": 0, "duration": 1.6, "ease": "power2.out"}, l0 + 4.5)
tw("#r-chip", {"opacity": 0, "scale": 0.8}, {"opacity": 1, "scale": 1, "duration": 0.6, "ease": "back.out(2)"}, l0 + 4.0)
cmove(l0 + 4.4, l0 + 5.4, MX + hx, MY + hy - 30)
cclick(l0 + 5.5)
tw("#pop", {"opacity": 0, "y": 20, "scale": 0.92}, {"opacity": 1, "y": 0, "scale": 1, "duration": 0.6, "ease": "back.out(1.8)"}, l0 + 5.6)
cmove(l0 + 6.6, l0 + 7.6, 1500, 940)
panel_out(["#p-map"], l1 - 0.4)
travel(l1 - 0.4)

# ---- 3. dashboard: four KPI tiles, hovered one by one
d0, d1 = T["dash"], T["app"]
RING_C = 2 * 3.14159 * 70
tiles = [
    ('<div class="ring"><svg viewBox="0 0 160 160"><circle cx="80" cy="80" r="70" class="rg-bg"/>'
     f'<circle id="ring" cx="80" cy="80" r="70" class="rg-fg" transform="rotate(-90 80 80)" style="stroke-dasharray:{RING_C:.1f};stroke-dashoffset:{RING_C:.1f}"/></svg>'
     '<div class="ring-n">4<em>&#9733;</em></div></div>', "BERTARAF BINTANG"),
    (f'<div class="kpi-n">{roll("k188", "188", d0 + 1.2)}</div><div class="bars">' +
     "".join(f'<i id="bar{i}" style="height:{h}px"></i>' for i, h in enumerate([30, 46, 38, 60, 52, 74, 90])) + "</div>", "BILIK PENGINAPAN"),
    ('<div class="clock"><i class="hand h" id="hh"></i><i class="hand m" id="hm"></i><b></b></div>'
     f'<div class="kpi-n sm">{roll("k24", "24", d0 + 1.5)}<em>JAM</em></div>', "PERKHIDMATAN"),
    (f'<div class="kpi-n">{roll("k7", "7", d0 + 1.8)}</div><div class="dots7">' +
     "".join(f'<i id="d7{i}"></i>' for i in range(7)) + "</div>", "KEMUDAHAN UTAMA"),
]
th = "".join(f'<div class="glass kpi" id="kpi{i}"><div class="kpi-glow" id="kg{i}"></div>{body}<div class="kpi-l">{lab}</div></div>'
             for i, (body, lab) in enumerate(tiles))
clip("dash", d0 - 0.4, d1 + 0.6, ('<div class="dash-h" id="dash-h"><div class="kick">HOTEL MITC DALAM ANGKA</div>'
                                  '<div class="h1">Selesa. Strategik. Lengkap.</div></div>' + th), "", 3)
panel_in(["#dash-h"] + [f"#kpi{i}" for i in range(4)], d0 - 0.4, stagger=0.09)
tw("#ring", {"strokeDashoffset": RING_C}, {"strokeDashoffset": RING_C * 0.2, "duration": 1.6, "ease": "power2.inOut"}, d0 + 1.0)
for i in range(7):
    tw(f"#bar{i}", {"scaleY": 0}, {"scaleY": 1, "duration": 0.7, "ease": "back.out(1.6)"}, d0 + 1.3 + i * 0.07)
    tw(f"#d7{i}", {"scale": 0, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.4, "ease": "back.out(3)"}, d0 + 1.9 + i * 0.08)
tw("#hh", {"rotation": 0}, {"rotation": 360 + 300, "duration": 2.4, "ease": "power2.inOut"}, d0 + 1.2)
tw("#hm", {"rotation": 0}, {"rotation": 720 * 2, "duration": 2.4, "ease": "power2.inOut"}, d0 + 1.2)
KX = [140, 560, 980, 1400]
for i in range(4):
    hx, ht = KX[i] + 190, d0 + 2.6 + i * 0.9
    cmove(ht - 0.6, ht, hx, 610)
    hover(f"#kpi{i}", f"#kg{i}", ht, ht + 0.75)
panel_out(["#dash-h"] + [f"#kpi{i}" for i in range(4)], d1 - 0.4, stagger=0.05)
travel(d1 - 0.4)

# ---- 4. app window: tabs, cards, expansions, room selector
a0, a1 = T["app"], T["book"]
WX, WY = 140, 80
CY = WY + 96            # top of the content area on screen
TABS = [("Fasiliti", 360, 170), ("Dewan &amp; Acara", 560, 250), ("Santapan", 840, 190), ("Bilik &amp; Suite", 1060, 230)]


def tab_center(i):
    _, x, w_ = TABS[i]
    return WX + x + w_ // 2, WY + 48


def card(cid, img, w, h, name, sub, extra=""):
    return (f'<div class="card" id="{cid}" style="width:{w}px"><div class="card-img" style="height:{h}px">'
            f'<img id="{cid}-i" src="assets/img/{img}.jpg" alt=""/>{extra}</div><div class="card-glow" id="{cid}-g"></div>'
            f'<div class="card-l"><b>{name}</b><span>{sub}</span></div></div>')


tabs_html = "".join(f'<div class="tab" id="tab{i}" style="left:{x}px;width:{w_}px">{n}</div>' for i, (n, x, w_) in enumerate(TABS))
CHIPS = ["Kolam Renang", "Spa", "Layanan Bilik", "Dobi", "Kafe", "Perkhidmatan 24 Jam"]
tc0 = ('<div class="tc" id="tc0"><div class="tc-h"><div class="kick">01 &#183; FASILITI</div><div class="h2">Ruang santai untuk semua</div></div>'
       '<div class="row" style="top:170px">'
       + card("f-c0", "pool-2", 480, 270, "Kolam Renang", "Santai bersama keluarga")
       + card("f-c1", "pool-kids", 480, 270, "Taman Air Kanak-kanak", "Ceria untuk si kecil")
       + card("f-c2", "lobby", 480, 270, "Lobi Utama", "Perkhidmatan mesra 24 jam") + "</div>"
       '<div class="chips" style="top:560px">' + "".join(f'<span class="chip" id="fch{i}"><i></i>{c}</span>' for i, c in enumerate(CHIPS)) + "</div></div>")
tc1 = ('<div class="tc" id="tc1"><div class="tc-h"><div class="kick">02 &#183; DEWAN &amp; ACARA</div><div class="h2">Ruang majlis serba guna</div></div>'
       '<div class="feat" id="e-f" style="left:60px;top:150px"><img id="e-f-i" src="assets/img/gadek.jpg" alt=""/><div class="card-glow" id="e-f-g"></div>'
       '<img class="feat-logo" src="assets/img/gadek-logo.png" alt="Gadek Ballroom"/>'
       '<div class="feat-l"><b>Dewan Gadek</b><span>Perkahwinan &#183; Persidangan &#183; Jamuan rasmi</span></div></div>'
       '<div class="side" id="e-s0" style="left:1060px;top:150px"><img src="assets/img/gadek5.jpg" alt=""/><div class="card-glow" id="e-s0-g"></div>'
       '<div class="feat-l sm"><b>Bilik Gadek 5</b><span>Mesyuarat &amp; bengkel</span></div></div>'
       '<div class="side" id="e-s1" style="left:1060px;top:432px"><img src="assets/img/brisu-aerial.jpg" alt=""/><div class="card-glow" id="e-s1-g"></div>'
       '<div class="feat-l sm"><b>Halaman Brisu</b><span>Majlis terbuka di tengah taman</span></div></div></div>')
tc2 = ('<div class="tc" id="tc2"><div class="tc-h"><div class="kick">03 &#183; SANTAPAN</div><div class="h2">Citarasa tempatan &amp; antarabangsa</div></div>'
       '<div class="feat" id="m-0" style="left:60px;top:150px;width:740px;height:416px"><img src="assets/img/bemban.jpg" alt=""/><div class="card-glow" id="m-0-g"></div>'
       '<div class="feat-l"><b>Restoran Bemban</b><span>Bufet sarapan &#183; tengah hari &#183; malam</span></div></div>'
       '<div class="feat" id="m-1" style="left:840px;top:150px;width:740px;height:416px"><img src="assets/img/asahan.jpg" alt=""/><div class="card-glow" id="m-1-g"></div>'
       '<div class="feat-l"><b>Asahan Cafe</b><span>Kafe konsep Nyonya &#183; hiburan secara langsung</span></div></div>'
       '<div class="info" style="left:60px;top:600px"><i class="ico">' + ICON["check"] + '</i>Sarapan, makan tengah hari &amp; makan malam setiap hari</div>'
       '<div class="info" style="left:840px;top:600px"><span class="clock sm"><i class="hand h" id="ah"></i><i class="hand m" id="am"></i><b></b></span>'
       'Dibuka 10:00 pagi hingga 12:00 malam</div></div>')
ROOMS = [("room-double", "Superior Double", "Katil Queen", "172.76 kps"),
         ("room-twin", "Superior Twin", "2 Katil Bujang", "172.76 kps"),
         ("room-deluxe", "Deluxe", "1 Queen + 1 Bujang", "185.75 kps"),
         ("room-junior", "Junior Suite", "Katil King &#183; ruang tamu", "464.47 kps"),
         ("room-exec", "Executive Suite", "Katil King &#183; lounge", "637.23 kps")]
rows = "".join(f'<div class="rrow" id="rr{i}" style="top:{150 + i * 112}px"><div class="rrow-bg" id="rr{i}-bg"></div>'
               f'<b>{n}</b><span>{bed} &#183; {sz}</span><i class="ico">{ICON["arrow"]}</i></div>' for i, (_, n, bed, sz) in enumerate(ROOMS))
spec = "".join(f'<div class="spec" id="spec{i}"><span class="chip"><i></i>{bed}</span><span class="chip"><i></i>{sz}</span>'
               f'<span class="chip"><i></i>WiFi percuma</span></div>' for i, (_, n, bed, sz) in enumerate(ROOMS))
tc3 = ('<div class="tc" id="tc3"><div class="tc-h"><div class="kick">04 &#183; BILIK &amp; SUITE</div><div class="h2">188 bilik untuk setiap keperluan</div></div>'
       '<div class="prev" style="left:60px;top:150px"><img src="assets/img/room-double.jpg" alt=""/></div>'
       f'{rows}<div class="specs" style="left:60px;top:735px">{spec}</div></div>')
clip("app", a0 - 0.4, a1 + 0.6, (
    '<div class="glass win app" id="win"><div class="topbar"><div class="logo-pill"><img src="assets/img/mitc-logo.png" alt="MITC Hotel"/></div>'
    f'{tabs_html}<div class="tab-ind" id="tab-ind"></div><div class="btn-book" id="btn-top">Tempah</div></div>'
    f'<div class="content">{tc0}{tc1}{tc2}{tc3}</div></div>'), "", 3)
tw("#win", {"y": 500, "rotationX": 32, "opacity": 0, "transformPerspective": P3},
   {"y": 0, "rotationX": 0, "opacity": 1, "transformPerspective": P3, "duration": 1.5, "ease": "expo.out"}, a0 - 0.4)

IND = {"i": 0}


def select_tab(i, t):
    """Cursor clicks tab i at t; indicator slides, old content leaves, new arrives."""
    _, x, w_ = TABS[i]
    tw("#tab-ind", {"x": TABS[IND["i"]][1] + 20, "scaleX": TABS[IND["i"]][2] - 40},
       {"x": x + 20, "scaleX": w_ - 40, "duration": 0.6, "ease": "expo.inOut"}, t + 0.05)
    tw(f"#tab{i}", {"opacity": 0.55}, {"opacity": 1, "duration": 0.3, "ease": "none"}, t + 0.05)
    if i:
        tw(f"#tab{i - 1}", {"opacity": 1}, {"opacity": 0.55, "duration": 0.3, "ease": "none"}, t + 0.05)
        tw(f"#tc{i - 1}", {"opacity": 1, "x": 0}, {"opacity": 0, "x": -60, "duration": 0.4, "ease": "power2.in"}, t + 0.05)
    tw(f"#tc{i}", {"opacity": 0, "x": 60}, {"opacity": 1, "x": 0, "duration": 0.7, "ease": "expo.out"}, t + 0.4)
    IND["i"] = i


# initial indicator position (under Fasiliti, hidden until the first click)
tw("#tab-ind", {"x": TABS[0][1] + 20, "scaleX": 1}, {"x": TABS[0][1] + 20, "scaleX": TABS[0][2] - 40, "duration": 0.01, "ease": "none"}, a0)

# -- Fasiliti
tF = a0 + 1.6
cmove(tF - 0.9, tF, *tab_center(0))
cclick(tF)
select_tab(0, tF)
for i in range(3):
    tw(f"#f-c{i}", {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.8, "ease": "expo.out"}, tF + 0.5 + i * 0.12)
for i in range(len(CHIPS)):
    tw(f"#fch{i}", {"scale": 0, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.45, "ease": "back.out(2.2)"}, tF + 1.3 + i * 0.09)
r0 = (WX + 60, CY + 170, 480, 270)
cmove(tF + 1.4, tF + 2.4, r0[0] + 240, r0[1] + 135)
hover("#f-c0", "#f-c0-g", tF + 2.4, tF + 3.1)
x0 = tF + 3.2
cclick(x0)
chide(x0 + 0.3)
expand("x-pool", "pool-2", r0, x0 + 0.1, x0 + 4.8, x0 + 5.6, "01 &#183; FASILITI", "Kolam Renang", "Kolam renang &amp; taman permainan air kanak-kanak")
cshow(x0 + 5.6, r0[0] + 240, r0[1] + 135)
cmove(x0 + 5.8, x0 + 6.6, WX + 1100 + 240, CY + 170 + 135)
hover("#f-c2", "#f-c2-g", x0 + 6.6, x0 + 7.4)

# -- Dewan & Acara
tD = x0 + 8.0
cmove(tD - 0.8, tD, *tab_center(1))
cclick(tD)
select_tab(1, tD)
for j, s_ in enumerate(["#e-f", "#e-s0", "#e-s1"]):
    tw(s_, {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.8, "ease": "expo.out"}, tD + 0.5 + j * 0.12)
cmove(tD + 1.3, tD + 2.1, WX + 1060 + 260, CY + 150 + 129)
hover("#e-s0", "#e-s0-g", tD + 2.1, tD + 2.9, lift=8)
cmove(tD + 2.9, tD + 3.5, WX + 1060 + 260, CY + 432 + 129)
hover("#e-s1", "#e-s1-g", tD + 3.5, tD + 4.3, lift=8)
rD = (WX + 60, CY + 150, 960, 540)
cmove(tD + 4.3, tD + 5.1, rD[0] + 480, rD[1] + 270)
hover("#e-f", "#e-f-g", tD + 5.1, tD + 5.6, lift=6, scale=1.015)
xD = tD + 5.7
cclick(xD)
chide(xD + 0.3)
expand("x-gadek", "gadek", rD, xD + 0.1, xD + 4.5, xD + 5.3, "02 &#183; DEWAN &amp; ACARA", "Dewan Gadek", "Perkahwinan, persidangan &amp; jamuan rasmi")
cshow(xD + 5.3, rD[0] + 480, rD[1] + 270)

# -- Santapan
tS = xD + 6.6
cmove(tS - 1.0, tS, *tab_center(2))
cclick(tS)
select_tab(2, tS)
for j, s_ in enumerate(["#m-0", "#m-1"]):
    tw(s_, {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.8, "ease": "expo.out"}, tS + 0.5 + j * 0.14)
rS = (WX + 60, CY + 150, 740, 416)
cmove(tS + 1.2, tS + 2.0, rS[0] + 370, rS[1] + 208)
hover("#m-0", "#m-0-g", tS + 2.0, tS + 2.6, lift=8, scale=1.02)
xS = tS + 2.7
cclick(xS)
chide(xS + 0.3)
expand("x-bemban", "bemban", rS, xS + 0.1, xS + 4.5, xS + 5.3, "03 &#183; SANTAPAN", "Restoran Bemban", "Bufet sarapan, makan tengah hari &amp; makan malam")
cshow(xS + 5.3, rS[0] + 370, rS[1] + 208)
cmove(xS + 5.4, xS + 6.2, WX + 840 + 370, CY + 150 + 208)
hover("#m-1", "#m-1-g", xS + 6.2, xS + 7.2, lift=8, scale=1.02)
tw("#ah", {"rotation": 0}, {"rotation": 300, "duration": 1.4, "ease": "power2.inOut"}, xS + 6.2)
tw("#am", {"rotation": 0}, {"rotation": 720, "duration": 1.4, "ease": "power2.inOut"}, xS + 6.2)

# -- Bilik & Suite: click each row, the preview plays that room's AI clip
tB = xS + 8.0
cmove(tB - 0.8, tB, *tab_center(3))
cclick(tB)
select_tab(3, tB)
for i in range(5):
    tw(f"#rr{i}", {"x": 60, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.7, "ease": "expo.out"}, tB + 0.5 + i * 0.08)
PR = (WX + 60, CY + 150, 1000, 562)
pv_style = f"left:{PR[0]}px;top:{PR[1]}px;width:{PR[2]}px;height:{PR[3]}px;right:auto;bottom:auto"
picks = [tB + 1.4 + i * 2.5 for i in range(5)]
for i, (vid, n, bed, sz) in enumerate(ROOMS):
    tp = picks[i]
    rx, ry = WX + 1100 + 240, CY + 150 + 50 + i * 112
    cmove(tp - 0.7, tp, rx, ry)
    cclick(tp)
    tw(f"#rr{i}-bg", {"opacity": 0}, {"opacity": 1, "duration": 0.3, "ease": "power2.out"}, tp + 0.05)
    tw(f"#rr{i}", {"x": 0}, {"x": -10, "duration": 0.3, "ease": "power2.out"}, tp + 0.05)
    tw(f"#spec{i}", {"opacity": 0, "y": 14}, {"opacity": 1, "y": 0, "duration": 0.5, "ease": "expo.out"}, tp + 0.2)
    end_v = picks[i + 1] + 0.45 if i < 4 else a1 + 0.1
    video(f"pv{i}", vid, tp + 0.1, end_v, cls="pv", style=pv_style, track=8)
    tw(f"#pv{i}", {"opacity": 0, "scale": 1.04}, {"opacity": 1, "scale": 1, "duration": 0.45, "ease": "power2.out"}, tp + 0.1)
    if i < 4:
        tw(f"#rr{i}-bg", {"opacity": 1}, {"opacity": 0, "duration": 0.3, "ease": "power2.in"}, picks[i + 1] + 0.05)
        tw(f"#rr{i}", {"x": -10}, {"x": 0, "duration": 0.3, "ease": "power2.in"}, picks[i + 1] + 0.05)
        tw(f"#spec{i}", {"opacity": 1}, {"opacity": 0, "duration": 0.25, "ease": "power2.in"}, picks[i + 1])
# last: open the Executive Suite full screen from the preview
cmove(picks[4] + 0.8, picks[4] + 1.5, PR[0] + 500, PR[1] + 281)
xR = picks[4] + 1.7
cclick(xR)
chide(xR + 0.3)
expand("x-exec", "room-exec-2", PR, xR + 0.1, None, a1 + 0.7, "04 &#183; BILIK &amp; SUITE", "Executive Suite", "Katil King &#183; ruang makan &amp; lounge &#183; 637.23 kaki persegi")
tw("#x-exec", {"scale": 1, "opacity": 1, "transformPerspective": P3}, {"scale": 0.7, "opacity": 0, "z": -400, "transformPerspective": P3, "duration": 0.8, "ease": "power3.in"}, a1 - 0.2)
panel_out(["#win"], a1 - 0.4)
travel(a1 - 0.4)

# ---- 5. booking widget
b0, b1 = T["book"], T["end"]
BX, BY = 1000, 170
cal_cells = []
for dnum in range(1, 31):
    idx = dnum + 1           # month starts on the 3rd column
    col, row = idx % 7, idx // 7
    cal_cells.append(f'<span class="day" id="day{dnum}" style="left:{20 + col * 78}px;top:{60 + row * 52}px">{dnum}</span>')
clip("book", b0 - 0.4, b1 + 0.6, (
    '<div class="glass sum" id="sum"><img src="assets/img/room-exec.jpg" alt=""/><div class="sum-t"><div class="kick">PILIHAN ANDA</div>'
    '<div class="h3">Executive Suite</div><div class="sum-r"><span class="chip"><i></i>Katil King</span><span class="chip"><i></i>637.23 kps</span></div></div></div>'
    '<div class="glass bk" id="bk"><div class="h3">Tempah Penginapan</div>'
    '<div class="fld" id="f-in" style="left:50px;top:110px"><i class="ico">' + ICON["cal"] + '</i><small>DAFTAR MASUK</small>'
    '<b class="ph" id="f-in-ph">Pilih tarikh</b><b class="val" id="f-in-v">12</b></div>'
    '<div class="fld" style="left:350px;top:110px"><i class="ico">' + ICON["cal"] + '</i><small>DAFTAR KELUAR</small>'
    '<b class="ph" id="f-out-ph">Pilih tarikh</b><b class="val" id="f-out-v">15</b></div>'
    '<div class="fld wide" style="left:50px;top:260px"><i class="ico">' + ICON["user"] + '</i><small>TETAMU</small>'
    '<b class="val on" id="g-n1">1 Dewasa</b><b class="val" id="g-n2">2 Dewasa</b>'
    '<span class="pm" style="left:440px">&#8722;</span><span class="pm" id="g-plus" style="left:510px">+</span></div>'
    '<div class="fld wide" style="left:50px;top:390px"><i class="ico">' + ICON["bed"] + '</i><small>JENIS BILIK</small><b class="val on">Executive Suite</b></div>'
    '<div class="nights" id="nights">3 malam</div>'
    '<div class="bk-btn" id="bk-btn"><span class="ripple" id="bk-rip"></span>TEMPAH SEKARANG</div>'
    '<div class="bk-note">atau hubungi 06-233 1551</div>'
    '<div class="cal" id="cal"><div class="cal-h">Pilih tarikh</div>' + "".join(cal_cells) +
    '</div></div>'
    '<div class="toast" id="toast"><i class="ico">' + ICON["check"] + '</i><div><b>Terima kasih!</b>'
    '<span>Tempah terus di mitchotel.com.my atau hubungi 06-233 1551</span></div></div>'), "", 3)
panel_in(["#sum", "#bk"], b0 - 0.4, stagger=0.12)
cmove(b0 + 0.6, b0 + 1.6, BX + 50 + 140, BY + 110 + 55)
cclick(b0 + 1.7)
tw("#cal", {"opacity": 0, "y": -16, "scale": 0.96}, {"opacity": 1, "y": 0, "scale": 1, "duration": 0.45, "ease": "back.out(1.8)"}, b0 + 1.8)


def day_xy(dnum):
    idx = dnum + 1
    return BX + 50 + 20 + (idx % 7) * 78 + 30, BY + 270 + 60 + (idx // 7) * 52 + 22


cmove(b0 + 2.0, b0 + 2.6, *day_xy(12))
cclick(b0 + 2.7)
tw("#day12", {"scale": 1, "backgroundColor": "rgba(214, 174, 94, 0)"}, {"scale": 1.08, "backgroundColor": "rgba(214, 174, 94, 1)", "duration": 0.2, "ease": "power2.out"}, b0 + 2.7)
cmove(b0 + 2.9, b0 + 3.4, *day_xy(15))
cclick(b0 + 3.5)
tw("#day15", {"scale": 1, "backgroundColor": "rgba(214, 174, 94, 0)"}, {"scale": 1.08, "backgroundColor": "rgba(214, 174, 94, 1)", "duration": 0.2, "ease": "power2.out"}, b0 + 3.5)
for dn in (13, 14):
    tw(f"#day{dn}", {"backgroundColor": "rgba(214, 174, 94, 0)"}, {"backgroundColor": "rgba(214, 174, 94, 0.28)", "duration": 0.3, "ease": "none"}, b0 + 3.55)
tw("#cal", {"opacity": 1}, {"opacity": 0, "duration": 0.3, "ease": "power2.in"}, b0 + 4.0)
tw(["#f-in-ph", "#f-out-ph"], {"opacity": 1}, {"opacity": 0, "duration": 0.2}, b0 + 4.1)
tw(["#f-in-v", "#f-out-v"], {"opacity": 0, "y": 10}, {"opacity": 1, "y": 0, "duration": 0.4, "ease": "back.out(2)"}, b0 + 4.2)
tw("#nights", {"opacity": 0, "scale": 0.8}, {"opacity": 1, "scale": 1, "duration": 0.4, "ease": "back.out(2)"}, b0 + 4.4)
cmove(b0 + 4.3, b0 + 4.9, BX + 50 + 510 + 23, BY + 260 + 45)
cclick(b0 + 5.0)
tw("#g-n1", {"opacity": 1, "y": 0}, {"opacity": 0, "y": -10, "duration": 0.2}, b0 + 5.05)
tw("#g-n2", {"opacity": 0, "y": 10}, {"opacity": 1, "y": 0, "duration": 0.3, "ease": "back.out(2)"}, b0 + 5.15)
cmove(b0 + 5.3, b0 + 5.9, BX + 340, BY + 600)
cclick(b0 + 6.0)
tw("#bk-btn", {"scale": 1}, {"scale": 0.95, "duration": 0.1, "ease": "power2.out"}, b0 + 6.0)
tw("#bk-btn", {"scale": 0.95}, {"scale": 1, "duration": 0.35, "ease": "back.out(3)"}, b0 + 6.1)
tw("#bk-rip", {"scale": 0, "opacity": 0.7}, {"scale": 9, "opacity": 0, "duration": 0.8, "ease": "power2.out"}, b0 + 6.0)
tw("#toast", {"y": -140, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "back.out(1.6)"}, b0 + 6.2)
chide(b1 - 0.5)
panel_out(["#sum", "#bk", "#toast"], b1 - 0.4)
travel(b1 - 0.4)

# ---- 6. end card
n0, n1 = T["end"], TOTAL
clip("endc", n0 - 0.4, n1, (
    '<div class="glass end" id="end"><div class="plate lg" id="end-plate"><img src="assets/img/mitc-logo.png" alt="MITC Hotel"/><span class="sheen" id="end-sh"></span></div>'
    f'<div class="end-t" id="end-t">{chars("Tempahan &amp; Pertanyaan")}</div>'
    '<div class="end-row"><span class="cbtn main" id="cb0"><i class="ico">' + ICON["phone"] + '</i>06-233 1551</span>'
    '<span class="cbtn" id="cb1"><i class="ico">' + ICON["web"] + '</i>mitchotel.com.my</span></div>'
    '<div class="end-addr" id="end-addr">Jalan Food City, Pusat Dagangan Antarabangsa Melaka, 75450 Ayer Keroh, Melaka</div>'
    '<div class="end-foot" id="end-foot"><span>DIURUSKAN OLEH</span><span class="wp"><img src="assets/img/mcorp-hotel-logo.png" alt="M\'Corp Hotel"/></span>'
    '<i></i><span>ANAK SYARIKAT</span><span class="wp"><img src="assets/img/mcorp-corporate.png" alt="MCORP"/></span></div></div>'), "", 3)
panel_in(["#end"], n0 - 0.4)
tw("#end-sh", {"xPercent": -150}, {"xPercent": 450, "duration": 1.2, "ease": "power2.inOut"}, n0 + 1.0)
tw("#end-t .ch", {"yPercent": 110, "opacity": 0}, {"yPercent": 0, "opacity": 1, "duration": 0.7, "ease": "expo.out", "stagger": 0.025}, n0 + 0.8)
tw(["#cb0", "#cb1"], {"y": 30, "opacity": 0, "scale": 0.9}, {"y": 0, "opacity": 1, "scale": 1, "duration": 0.7, "ease": "back.out(1.8)", "stagger": 0.14}, n0 + 1.3)
tw("#end-addr", {"opacity": 0}, {"opacity": 1, "duration": 0.7}, n0 + 1.8)
tw("#end-foot", {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0, "duration": 0.7, "ease": "expo.out"}, n0 + 2.1)
tw("#end", {"scale": 1, "transformPerspective": P3}, {"scale": 1.03, "transformPerspective": P3, "duration": round(n1 - n0 - 1.4, 3), "ease": "none"}, n0 + 1.0)
tw("#fadeout", {"opacity": 0}, {"opacity": 1, "duration": 0.7, "ease": "power1.in"}, n1 - 0.7)

# ================================================================ assemble
CSS = open(os.path.join(HF, "..", "style-v4.css")).read()
html = f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="vendor/gsap.min.js"></script>
    <style>
{CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{at(TOTAL)}" data-width="{W}" data-height="{H}">
      {chr(10).join('      ' + c_ for c_ in clips).lstrip()}
      <div id="curw" class="clip fx" data-start="0" data-duration="{at(TOTAL)}" data-track-index="30"><div class="cursor" id="cursor"><span class="cur-ring" id="cur-r"></span><div class="cur-i" id="cur-i"><svg viewBox="0 0 24 24"><path d="M5 3l14 8-6.2 1.6L16 20l-2.6 1.2-3.2-7.4L5 18z"/></svg></div></div></div>
      <div id="fadeout" class="clip fx" data-start="0" data-duration="{at(TOTAL)}" data-track-index="31"></div>
    </div>
    <script>
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
        {chr(10).join('        ' + l for l in tl).lstrip()}
        window.__timelines = window.__timelines || {{}};
        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(os.path.join(HF, "index.html"), "w").write(html)
print("total", TOTAL, "s;", len(clips), "clips;", len(tl), "tweens")
print("app tabs at", round(tF, 2), round(tD, 2), round(tS, 2), round(tB, 2), "exec open", round(xR, 2))
