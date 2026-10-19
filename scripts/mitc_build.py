"""Build the Hotel MITC intro video (HyperFrames) -> edits/mitc-pengenalan/hf/index.html

usage: python3 scripts/mitc_build.py

v3, corporate hypermotion: whip / zoom-through transitions with motion blur, diagonal
chapter wipes, 3D kinetic type, rolling digits, 3D photo gallery, slat and mosaic
reveals, a chapter progress HUD, a cursor that hovers / clicks like a UI, gold particles,
and AI depth camera moves on every full-screen photo (assets/video, scripts/mitc_room3d.py).
Silent (music is added on the platform).  Styles: edits/mitc-pengenalan/style-v3.css
(v2 luxury cut: scripts/mitc_build_v2.py).
"""
import json
import os

HF = os.path.join(os.path.dirname(__file__), "..", "edits", "mitc-pengenalan", "hf")
W, H = 1920, 1080

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


def clip(cid, start, end, inner, cls="", track=1):
    clips.append(f'<div id="{cid}" class="clip {cls}" data-start="{at(start)}" '
                 f'data-duration="{at(end - start)}" data-track-index="{track}">{inner}</div>')


def chars(text, cls="ch"):
    out = []
    for word in text.split(" "):
        if word.startswith("&"):
            out.append(f'<span class="w"><span class="{cls}">{word}</span></span>')
            continue
        out.append('<span class="w">' + "".join(f'<span class="{cls}">{c}</span>' for c in word) + "</span>")
    return " ".join(out)


def roll(cid, text, start, stagger=0.08, dur=1.4):
    """Slot-machine digits: every digit spins through two cycles and lands on its value."""
    html = []
    k = 0
    for c in text:
        if c.isdigit():
            stack = "".join(f"<span>{n % 10}</span>" for n in range(20))
            html.append(f'<span class="roll"><span class="roll-s" id="{cid}-d{k}">{stack}</span></span>')
            land = -(10 + int(c)) / 20 * 100
            tw(f"#{cid}-d{k}", {"yPercent": 0}, {"yPercent": land, "duration": dur + k * 0.06, "ease": "expo.out"}, start + k * stagger)
            k += 1
        else:
            html.append(f'<span class="roll-c">{c}</span>')
    return "".join(html)


_seed = [7]


def rnd():
    _seed[0] = (_seed[0] * 1103515245 + 12345) % 2147483648
    return _seed[0] / 2147483648


def particles(pid, start, end, n=18):
    """Soft gold / white bokeh drifting upwards (deterministic positions)."""
    spans = []
    for i in range(n):
        size = 6 + rnd() * 26
        x, y = rnd() * 1920, rnd() * 1080
        op = 0.15 + rnd() * 0.45
        cls = "pt gold" if rnd() > 0.4 else "pt"
        spans.append(f'<span class="{cls}" id="{pid}{i}" style="left:{x:.0f}px;top:{y:.0f}px;width:{size:.0f}px;height:{size:.0f}px;opacity:{op:.2f}"></span>')
        tw(f"#{pid}{i}", {"y": 0, "x": 0}, {"y": -(60 + rnd() * 160), "x": (rnd() - 0.5) * 80, "duration": round(end - start, 3), "ease": "none"}, start)
    return '<div class="pts">' + "".join(spans) + "</div>"


CURSOR_SVG = '<svg viewBox="0 0 24 24"><path d="M5 3l14 8-6.2 1.6L16 20l-2.6 1.2-3.2-7.4L5 18z"/></svg>'


def cursor(cid, path, clicks=()):
    """UI cursor: path = [(t, x, y), ...] absolute stage coordinates; clicks = [t, ...]."""
    t0, x0, y0 = path[0]
    tw(f"#{cid}", {"x": x0, "y": y0, "opacity": 0}, {"x": x0, "y": y0, "opacity": 1, "duration": 0.3, "ease": "none"}, t0)
    for (ta, xa, ya), (tb, xb, yb) in zip(path, path[1:]):
        tw(f"#{cid}", {"x": xa, "y": ya}, {"x": xb, "y": yb, "duration": round(tb - ta, 3), "ease": "power3.inOut"}, ta)
    for tc in clicks:
        tw(f"#{cid}-i", {"scale": 1}, {"scale": 0.8, "duration": 0.1, "ease": "power2.out"}, tc)
        tw(f"#{cid}-i", {"scale": 0.8}, {"scale": 1, "duration": 0.2, "ease": "power2.out"}, tc + 0.1)
        tw(f"#{cid}-r", {"scale": 0, "opacity": 0.8}, {"scale": 3.5, "opacity": 0, "duration": 0.6, "ease": "power2.out"}, tc)
    return f'<div class="cursor" id="{cid}"><span class="cur-ring" id="{cid}-r"></span><div class="cur-i" id="{cid}-i">{CURSOR_SVG}</div></div>'


# ---------------------------------------------------------------- shots + transitions
def shot(cid, img, start, end, kb=(1.18, 1.04), origin="50% 50%", track=1, shade="shade-lt"):
    """Still photo with a speed-ramped push.  #cid-kb carries the transitions."""
    inner = (f'<div class="kb" id="{cid}-kb"><img id="{cid}-img" src="assets/img/{img}.jpg" alt="" '
             f'style="transform-origin:{origin}"/></div>' + (f'<div class="shade {shade}"></div>' if shade else ""))
    clip(cid, start, end, inner, "shot", track)
    tw(f"#{cid}-img", {"scale": kb[0]}, {"scale": kb[1], "duration": round(end - start, 3), "ease": "power2.out"}, start)
    return f"#{cid}-kb"


def vshot(cid, vid, start, end, track=1, media_start=0.0, shade="shade-lt"):
    """AI depth camera-move clip (direct child of the stage) plus its own shade layer."""
    clips.append(f'<video id="{cid}" class="clip vclip" src="assets/video/{vid}.mp4" data-start="{at(start)}" '
                 f'data-duration="{at(end - start)}" data-media-start="{media_start}" data-hf-media-start-basis="local" '
                 f'data-track-index="{track}" muted playsinline></video>')
    if shade:
        clip(f"{cid}-sh", start, end, "", f"shade {shade}", track + 1)
    return f"#{cid}"


OUT = {
    "whip":  ({"x": 0, "filter": "blur(0px)"}, {"x": -620, "filter": "blur(30px)"}),
    "whipr": ({"x": 0, "filter": "blur(0px)"}, {"x": 620, "filter": "blur(30px)"}),
    "whipv": ({"y": 0, "filter": "blur(0px)"}, {"y": -460, "filter": "blur(30px)"}),
    "zoom":  ({"scale": 1, "filter": "blur(0px)"}, {"scale": 1.7, "filter": "blur(26px)"}),
    "spin":  ({"scale": 1, "rotation": 0, "filter": "blur(0px)"}, {"scale": 1.4, "rotation": 8, "filter": "blur(24px)"}),
}
IN = {
    "whip":  ({"x": 620, "filter": "blur(30px)"}, {"x": 0, "filter": "blur(0px)"}),
    "whipr": ({"x": -620, "filter": "blur(30px)"}, {"x": 0, "filter": "blur(0px)"}),
    "whipv": ({"y": 460, "filter": "blur(30px)"}, {"y": 0, "filter": "blur(0px)"}),
    "zoom":  ({"scale": 0.55, "filter": "blur(26px)"}, {"scale": 1, "filter": "blur(0px)"}),
    "spin":  ({"scale": 1.4, "rotation": -8, "filter": "blur(24px)"}, {"scale": 1, "rotation": 0, "filter": "blur(0px)"}),
}


def cut(a, b, T, kind="whip"):
    """Hypermotion cut at T from a to b (selector or list of selectors)."""
    f, t = OUT[kind]
    tw(a, f, dict(t, duration=0.28, ease="power2.in"), T - 0.28)
    f, t = IN[kind]
    tw(b, f, dict(t, duration=0.65, ease="expo.out"), T)
    if kind in ("whip", "whipr"):
        x0, x1 = (2300, -700) if kind == "whip" else (-700, 2300)
        tw("#streak", {"x": x0}, {"x": x1, "duration": 0.38, "ease": "none"}, T - 0.2)


# ---------------------------------------------------------------- overlays
def lower_third(cid, start, end, kicker, title, sub, chips=(), track=6):
    chip_html = "".join(f'<span class="chip" id="{cid}-c{i}"><i></i>{c}</span>' for i, c in enumerate(chips))
    inner = (f'<div class="lt" id="{cid}-lt"><div class="lt-in" id="{cid}-in">'
             f'<div class="m"><div class="lt-k" id="{cid}-k">{kicker}</div></div>'
             f'<div class="m" id="{cid}-bm"><div class="lt-box" id="{cid}-b"><span class="lt-bar"></span>{title}'
             f'<span class="sheen" id="{cid}-sh"></span></div></div>'
             f'<div class="m" id="{cid}-sm"><div class="lt-s" id="{cid}-s">{sub}</div></div>'
             + (f'<div class="chips">{chip_html}</div>' if chips else "") + "</div></div>")
    clip(cid, start, end, inner, "ovl", track)
    tw(f"#{cid}-k", {"yPercent": 110}, {"yPercent": 0, "duration": 0.6, "ease": "expo.out"}, start)
    tw(f"#{cid}-bm", {"xPercent": -101}, {"xPercent": 0, "duration": 0.75, "ease": "expo.inOut"}, start + 0.05)
    tw(f"#{cid}-b", {"xPercent": 101}, {"xPercent": 0, "duration": 0.75, "ease": "expo.inOut"}, start + 0.05)
    tw(f"#{cid}-sm", {"xPercent": -101}, {"xPercent": 0, "duration": 0.75, "ease": "expo.inOut"}, start + 0.25)
    tw(f"#{cid}-s", {"xPercent": 101}, {"xPercent": 0, "duration": 0.75, "ease": "expo.inOut"}, start + 0.25)
    tw(f"#{cid}-sh", {"xPercent": -150}, {"xPercent": 450, "duration": 0.9, "ease": "power2.inOut"}, start + 0.8)
    for i in range(len(chips)):
        tw(f"#{cid}-c{i}", {"scale": 0, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.5, "ease": "back.out(2)"}, start + 0.55 + i * 0.14)
    tw(f"#{cid}-in", {"x": 0}, {"x": 16, "duration": round(end - start, 3), "ease": "none"}, start)   # slow drift keeps it alive
    tw(f"#{cid}-lt", {"x": 0, "opacity": 1}, {"x": -90, "opacity": 0, "duration": 0.3, "ease": "power2.in"}, end - 0.32)


CH_IN, CH_OUT = 0.5, 1.25     # panel covers at c+CH_IN (scene changes there), leaves at c+CH_OUT


def chapter(cid, c, num, word):
    """Diagonal navy panel (gold leading edge) wipes across with a kinetic chapter title."""
    inner = (f'<div class="chp-gold" id="{cid}-g"></div><div class="chp-navy" id="{cid}-p"></div>'
             f'<div class="chp-num" id="{cid}-n">{num}</div>'
             f'<div class="chp-txt"><div class="chp-k" id="{cid}-k">BAHAGIAN {num}</div>'
             f'<div class="chp-w" id="{cid}-w">{chars(word)}</div></div>')
    clip(cid, c, c + CH_OUT + 0.55, inner, "ovl chpc", 9)
    tw(f"#{cid}-g", {"x": 2250}, {"x": -470, "duration": CH_IN, "ease": "expo.inOut"}, c - 0.04)
    tw(f"#{cid}-p", {"x": 2400}, {"x": -330, "duration": CH_IN, "ease": "expo.inOut"}, c)
    tw(f"#{cid}-n", {"x": 500, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 1.0, "ease": "expo.out"}, c + 0.25)
    tw(f"#{cid}-k", {"x": 120, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.7, "ease": "expo.out"}, c + 0.3)
    tw(f"#{cid}-w .ch", {"x": 260, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.7, "ease": "expo.out", "stagger": 0.03}, c + 0.33)
    tw([f"#{cid}-n", f"#{cid} .chp-txt"], {"x": 0, "opacity": 1}, {"x": -420, "opacity": 0, "duration": 0.42, "ease": "expo.in"}, c + CH_OUT - 0.05)
    tw(f"#{cid}-p", {"x": -330}, {"x": -3250, "duration": 0.5, "ease": "expo.inOut"}, c + CH_OUT)
    tw(f"#{cid}-g", {"x": -470}, {"x": -3400, "duration": 0.5, "ease": "expo.inOut"}, c + CH_OUT + 0.04)


def brackets(cid, start, end, track=8):
    clip(cid, start, end, "".join(f'<span class="brk brk-{p}" id="{cid}-{p}"></span>' for p in ("tl", "tr", "bl", "br")), "ovl", track)
    for p, (dx, dy) in {"tl": (-40, -40), "tr": (40, -40), "bl": (-40, 40), "br": (40, 40)}.items():
        tw(f"#{cid}-{p}", {"x": dx, "y": dy, "opacity": 0}, {"x": 0, "y": 0, "opacity": 1, "duration": 0.8, "ease": "expo.out"}, start + 0.1)


# ================================================================ TIMELINE (slower than the first v3 cut)
T = dict(open=0.0, title=4.2, corp=10.0, lok=15.6, stats=21.0,
         ch1=25.8, ch2=35.4, ch3=47.4, ch4=55.9, recap=75.7, end=79.7, fin=86.0)
TOTAL = T["fin"]
SW = {k: T[k] + CH_IN for k in ("ch1", "ch2", "ch3", "ch4")}    # scene switch under each chapter wipe

# ---- 1. opening on navy
o1 = T["title"]
clip("open", 0, o1, (
    '<div class="grid" id="op-grid"></div>' + particles("p0-", 0, o1) +
    '<div class="op" id="op"><div class="op-line" id="op-line"></div>'
    f'<div class="m"><div class="op-t" id="op-t">{chars("M’CORP HOTEL SDN. BHD.")}</div></div>'
    '<div class="m"><div class="op-s" id="op-s">PENGENDALI HOTEL MITC &#183; MELAKA</div></div></div>'), "bg-navy", 1)
tw("#op-grid", {"opacity": 0, "scale": 1.15}, {"opacity": 1, "scale": 1, "duration": 3.0, "ease": "power2.out"}, 0)
tw("#op-line", {"scaleX": 0}, {"scaleX": 1, "duration": 1.0, "ease": "expo.inOut"}, 0.25)
tw("#op-t .ch", {"yPercent": 120}, {"yPercent": 0, "duration": 0.8, "ease": "expo.out", "stagger": 0.03}, 0.85)
tw("#op-s", {"yPercent": -120}, {"yPercent": 0, "duration": 0.8, "ease": "expo.out"}, 1.6)
tw("#op", {"scale": 1}, {"scale": 1.05, "duration": round(o1 - 1.0, 3), "ease": "none"}, 0.6)
tw("#op .m", {"opacity": 1}, {"opacity": 0, "duration": 0.3, "ease": "power2.in"}, o1 - 0.45)
for i, cls in enumerate(["sw-blue", "sw-gold", "sw-navy"]):
    clip(f"sweep{i}", o1 - 0.55, o1 + 0.6, f'<div class="sweep {cls}" id="sw{i}"></div>', "ovl swc", 10 + i)
    tw(f"#sw{i}", {"x": 2400}, {"x": -3000, "duration": 1.0, "ease": "expo.inOut"}, o1 - 0.55 + i * 0.08)

# ---- 2. title (AI dolly on the night exterior)
t0, t1 = T["title"], T["corp"]
vt = vshot("s-title", "ext-night", t0, t1, shade="shade-title")
clip("title", t0, t1, (
    particles("p1-", t0, t1, 14) +
    '<div class="ttl" id="ttl"><div class="ttl-k" id="ttl-k">HOTEL</div>'
    f'<div class="ttl-a" id="ttl-a">{chars("MITC", "ch3")}</div>'
    '<div class="ttl-bar" id="ttl-bar"></div>'
    f'<div class="ttl-b" id="ttl-b">{chars("AYER KEROH · MELAKA")}</div>'
    '<div class="stars">' + "".join(f'<span class="star" id="st{i}">&#9733;</span>' for i in range(4)) + "</div></div>"), "ovl", 7)
brackets("brk1", t0 + 0.3, t1 - 0.35)
tw("#ttl-k", {"y": -40, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.7, "ease": "expo.out"}, t0 + 0.4)
tw("#ttl-a .ch3", {"z": -1400, "rotationX": 80, "opacity": 0}, {"z": 0, "rotationX": 0, "opacity": 1, "duration": 1.2, "ease": "expo.out", "stagger": 0.11}, t0 + 0.5)
tw("#ttl-bar", {"scaleX": 0}, {"scaleX": 1, "duration": 1.0, "ease": "expo.inOut"}, t0 + 1.3)
tw("#ttl-b .ch", {"x": -30, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.6, "ease": "expo.out", "stagger": 0.025}, t0 + 1.7)
for i in range(4):
    tw(f"#st{i}", {"scale": 0, "rotation": -180}, {"scale": 1, "rotation": 0, "duration": 0.7, "ease": "back.out(2)"}, t0 + 2.3 + i * 0.12)
tw("#ttl", {"scale": 1}, {"scale": 1.06, "duration": round(t1 - t0 - 0.5, 3), "ease": "none"}, t0)
tw("#ttl", {"opacity": 1, "filter": "blur(0px)"}, {"opacity": 0, "filter": "blur(14px)", "duration": 0.45, "ease": "power2.in"}, t1 - 0.45)
tw(vt, {"scale": 1, "filter": "blur(0px)"}, {"scale": 1.5, "filter": "blur(20px)", "duration": 0.45, "ease": "power2.in"}, t1 - 0.45)

# ---- 3. corporate (light)
c0, c1 = T["corp"], T["lok"]
clip("corp", c0, c1, (
    '<div class="grid dark" id="cp-grid"></div>'
    '<div class="cp-photo" id="cp-photo"><div class="cp-photo-in" id="cp-pin"><img src="assets/img/ext-wide.jpg" alt=""/></div></div>'
    '<div class="cp-left">'
    '<div class="cp-card" id="cp-card"><img src="assets/img/mcorp-hotel-logo.png" alt="M\'Corp Hotel Sdn. Bhd."/><span class="sheen" id="cp-sh"></span></div>'
    '<div class="m"><div class="cp-k" id="cp-k">ANAK SYARIKAT PKNM &#183; DITUBUHKAN</div></div>'
    f'<div class="cp-date" id="cp-date">{roll("cpd", "15.11.2016", c0 + 1.3)}</div>'
    '<div class="m"><div class="cp-s" id="cp-s">Mengurus &amp; mengendalikan operasi<br/><b>Hotel MITC, Ayer Keroh, Melaka</b></div></div></div>'), "bg-light", 1)
tw("#corp", {"scale": 0.8, "filter": "blur(16px)"}, {"scale": 1, "filter": "blur(0px)", "duration": 0.7, "ease": "expo.out"}, c0)
tw("#cp-photo", {"xPercent": 110}, {"xPercent": 0, "duration": 1.0, "ease": "expo.inOut"}, c0 + 0.15)
tw("#cp-pin", {"scale": 1.35}, {"scale": 1.05, "duration": round(c1 - c0, 3), "ease": "power2.out"}, c0 + 0.15)
tw("#cp-card", {"rotationY": -90, "opacity": 0}, {"rotationY": 0, "opacity": 1, "duration": 1.0, "ease": "expo.out"}, c0 + 0.5)
tw("#cp-sh", {"xPercent": -150}, {"xPercent": 450, "duration": 1.0, "ease": "power2.inOut"}, c0 + 1.4)
tw("#cp-k", {"yPercent": 110}, {"yPercent": 0, "duration": 0.7, "ease": "expo.out"}, c0 + 1.1)
tw("#cp-date", {"opacity": 0}, {"opacity": 1, "duration": 0.2}, c0 + 1.25)
tw("#cp-s", {"yPercent": 110}, {"yPercent": 0, "duration": 0.8, "ease": "expo.out"}, c0 + 2.4)
tw(".cp-left", {"y": 0}, {"y": -14, "duration": round(c1 - c0, 3), "ease": "none"}, c0)

# ---- 4. lokasi (AI crane on the day exterior + map graphics)
l0, l1 = T["lok"], T["stats"]
vl = vshot("s-lokbg", "ext-day", l0, l1, shade="shade-navy")
clip("lok", l0, l1, (
    '<div class="grid" id="lok-grid"></div>' + particles("p2-", l0, l1, 12) +
    '<div class="pin-wrap"><div class="ring" id="rg0"></div><div class="ring" id="rg1"></div><div class="ring" id="rg2"></div>'
    '<div class="pin" id="pin"><svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.6A2.6 2.6 0 1 1 12 6.4a2.6 2.6 0 0 1 0 5.2z"/></svg></div>'
    '<div class="tline tline1" id="tl1"></div><div class="tline tline2" id="tl2"></div>'
    '<div class="tag tag1" id="tag1"><b>MITC</b><span>Bertentangan Pusat Dagangan<br/>Antarabangsa Melaka</span></div>'
    '<div class="tag tag2" id="tag2"><b>10 MINIT</b><span>dari Tol Ayer Keroh</span></div></div>'
    '<div class="lok-left"><div class="m"><div class="lk-k" id="lk-k">LOKASI STRATEGIK</div></div>'
    f'<div class="lk-t" id="lk-t">{chars("AYER KEROH,")}<br/>{chars("MELAKA")}</div>'
    f'<div class="lk-c" id="lk-c">{chars("2.27° U  ·  102.28° T")}</div></div>'), "", 3)
brackets("brk2", l0 + 0.2, l1 - 0.35)
tw("#lk-k", {"yPercent": 110}, {"yPercent": 0, "duration": 0.6, "ease": "expo.out"}, l0 + 0.5)
tw("#lk-t .ch", {"yPercent": 100, "opacity": 0}, {"yPercent": 0, "opacity": 1, "duration": 0.7, "ease": "expo.out", "stagger": 0.035}, l0 + 0.6)
tw("#lk-c .ch", {"opacity": 0}, {"opacity": 1, "duration": 0.05, "ease": "none", "stagger": 0.04}, l0 + 1.5)
tw("#pin", {"y": -500, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.9, "ease": "bounce.out"}, l0 + 0.8)
for i in range(3):
    tw(f"#rg{i}", {"scale": 0.2, "opacity": 0.9}, {"scale": 3.2, "opacity": 0, "duration": 1.8, "ease": "power2.out"}, l0 + 1.6 + i * 0.6)
tw("#tl1", {"scaleX": 0}, {"scaleX": 1, "duration": 0.5, "ease": "expo.out"}, l0 + 1.9)
tw("#tag1", {"x": 40, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.7, "ease": "expo.out"}, l0 + 2.1)
tw("#tl2", {"scaleX": 0}, {"scaleX": 1, "duration": 0.5, "ease": "expo.out"}, l0 + 2.6)
tw("#tag2", {"x": 40, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.7, "ease": "expo.out"}, l0 + 2.8)
cut("#corp", [vl, "#lok"], l0, "whip")

# ---- 5. stats: three cards, a cursor hovers each one
s0, s1 = T["stats"], SW["ch1"]
panels = [("ext-night", "4", "&#9733;", "BERTARAF<br/>4 BINTANG"), ("room-exec", "188", "", "BILIK<br/>PENGINAPAN"),
          ("lobby", "24", "JAM", "PERKHIDMATAN<br/>SETIAP HARI")]
ph = []
for i, (img, n, suf, lab) in enumerate(panels):
    ph.append(f'<div class="sp" id="sp{i}"><img id="sp{i}-i" src="assets/img/{img}.jpg" alt=""/><div class="sp-sh"></div>'
              f'<div class="sp-glow" id="sp{i}-g"></div>'
              f'<div class="sp-n">{roll(f"sn{i}", n, s0 + 0.6 + i * 0.25, dur=1.5)}<span class="sp-suf">{suf}</span></div>'
              f'<div class="sp-bar"></div><div class="sp-l">{lab}</div></div>')
hover = [s0 + 2.2, s0 + 3.0, s0 + 3.8]
cur1 = cursor("cur1", [(s0 + 1.6, 1750, 1000), (hover[0], 470, 700), (hover[1], 1010, 700), (hover[2], 1550, 700), (s1 - 0.1, 1700, 760)])
clip("stats", s0, s1, '<div class="grid" id="st-grid"></div>' + particles("p3-", s0, s1, 14) +
     '<div class="sps">' + "".join(ph) + "</div>" + cur1, "bg-navy", 1)
for i in range(3):
    tw(f"#sp{i}", {"yPercent": 130 if i != 1 else -130, "rotation": 4 if i != 1 else -4},
       {"yPercent": 0, "rotation": 0, "duration": 0.9, "ease": "expo.out"}, s0 + 0.1 + i * 0.12)
    tw(f"#sp{i}-i", {"scale": 1.4}, {"scale": 1.1, "duration": round(s1 - s0, 3), "ease": "power2.out"}, s0)
    h = hover[i]
    tw(f"#sp{i}", {"scale": 1, "y": 0}, {"scale": 1.06, "y": -16, "duration": 0.35, "ease": "power2.out"}, h - 0.1)
    tw(f"#sp{i}-g", {"opacity": 0}, {"opacity": 1, "duration": 0.3, "ease": "power2.out"}, h - 0.1)
    tw(f"#sp{i}", {"scale": 1.06, "y": -16}, {"scale": 1, "y": 0, "duration": 0.4, "ease": "power2.inOut"}, h + 0.55)
    tw(f"#sp{i}-g", {"opacity": 1}, {"opacity": 0, "duration": 0.4, "ease": "power2.inOut"}, h + 0.55)
cut([vl, "#lok"], "#stats", s0, "whipv")

# ---- 6. 01 fasiliti
c = T["ch1"]
chapter("ch1", c, "01", "FASILITI")
f = [SW["ch1"], 30.3, 33.1, SW["ch2"]]
a = vshot("s-f1", "pool-2", f[0], f[1])
b = vshot("s-f2", "pool-night", f[1], f[2])
d = vshot("s-f3", "lobby", f[2], f[3])
cut(a, b, f[1], "whip")
cut(b, d, f[2], "zoom")
lower_third("lt-f1", c + CH_OUT + 0.25, f[2], "01 &#183; FASILITI", "KOLAM RENANG", "Kolam renang &amp; taman permainan air kanak-kanak")
lower_third("lt-f2", f[2] + 0.35, f[3] - 0.5, "01 &#183; FASILITI", "LOBI UTAMA", "Sambutan mesra, perkhidmatan 24 jam")

# ---- 7. 02 dewan & acara: 3D gallery settles flat, the cursor clicks Dewan Gadek, zoom into it
c = T["ch2"]
chapter("ch2", c, "02", "DEWAN &amp; ACARA")
g0, g1 = SW["ch2"], 39.9
cards = [("gadek", "DEWAN GADEK"), ("gadek5", "BILIK GADEK 5"), ("brisu-aerial", "HALAMAN BRISU")]
gal = "".join(f'<div class="gc" id="gc{i}"><img src="assets/img/{img}.jpg" alt=""/><div class="gc-glow" id="gc{i}-g"></div>'
              f'<div class="gc-l"><span>0{i + 1}</span>{lab}</div></div>' for i, (img, lab) in enumerate(cards))
click_t = g1 - 0.75
cur2 = cursor("cur2", [(g0 + 1.9, 1500, 980), (click_t, 400, 560)], clicks=[click_t])
clip("gal", g0, g1, '<div class="grid" id="gal-grid"></div>' + particles("p4-", g0, g1, 14) +
     f'<div class="gal-stage"><div class="gal-row" id="gal-row">{gal}</div></div>' + cur2, "bg-navy", 2)
tw("#gal-row", {"rotationY": 40, "x": 520, "z": -600}, {"rotationY": 0, "x": 0, "z": 0, "duration": round(click_t - 0.3 - g0, 3), "ease": "power3.inOut"}, g0)
for i in range(3):
    tw(f"#gc{i}", {"y": 200 if i % 2 == 0 else -200, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.9, "ease": "expo.out"}, g0 + 0.8 + i * 0.14)
tw("#gc0", {"scale": 1}, {"scale": 1.08, "duration": 0.3, "ease": "power2.out"}, click_t - 0.3)
tw("#gc0-g", {"opacity": 0}, {"opacity": 1, "duration": 0.3, "ease": "power2.out"}, click_t - 0.3)
e = [g1, 42.7, 45.3, SW["ch3"]]
e1 = vshot("s-e1", "gadek", e[0], e[1])
e2 = vshot("s-e2", "gadek5", e[1], e[2])
e3 = vshot("s-e3", "brisu-aerial", e[2], e[3])
cut("#gal", e1, e[0], "zoom")
cut(e1, e2, e[1], "whip")
cut(e2, e3, e[2], "spin")
lower_third("lt-e1", e[0] + 0.3, e[1], "02 &#183; DEWAN &amp; ACARA", "DEWAN GADEK", "Perkahwinan, persidangan &amp; jamuan rasmi")
lower_third("lt-e2", e[1] + 0.3, e[2], "02 &#183; DEWAN &amp; ACARA", "BILIK GADEK 5", "Mesyuarat, taklimat &amp; bengkel")
lower_third("lt-e3", e[2] + 0.3, e[3] - 0.5, "02 &#183; DEWAN &amp; ACARA", "HALAMAN BRISU", "Ruang majlis terbuka di tengah taman")
clip("lg-gadek", e[0] + 0.35, e[1], '<img class="venue-logo" id="lg-gadek-i" src="assets/img/gadek-logo.png" alt="Gadek Ballroom"/>', "ovl", 8)
tw("#lg-gadek-i", {"scale": 0.6, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.7, "ease": "back.out(1.8)"}, e[0] + 0.6)

# ---- 8. 03 tempat makan: slats slide over Bemban, then part to reveal it
c = T["ch3"]
chapter("ch3", c, "03", "TEMPAT MAKAN")
m0, m1 = SW["ch3"], 51.0
mm = [m1, 53.6, SW["ch4"]]
s_m1 = vshot("s-m1", "bemban", m0, mm[1])             # under the slats
slats = [("bemban", "RESTORAN BEMBAN"), ("bemban-breakfast", "BUFET SARAPAN"), ("asahan", "ASAHAN CAFE")]
sl = "".join(f'<div class="slat" id="sl{i}"><img id="sl{i}-i" src="assets/img/{img}.jpg" alt=""/><div class="slat-l">{lab}</div></div>'
             for i, (img, lab) in enumerate(slats))
clip("slats", m0, m1, f'<div class="slats">{sl}</div>', "", 3)
for i in range(3):
    tw(f"#sl{i}", {"yPercent": -100 if i % 2 == 0 else 100}, {"yPercent": 0, "duration": 0.9, "ease": "expo.inOut"}, m0 + 0.6 + i * 0.12)
    tw(f"#sl{i}-i", {"scale": 1.45}, {"scale": 1.1, "duration": round(m1 - m0, 3), "ease": "power2.out"}, m0 + 0.6)
    tw(f"#sl{i}", {"yPercent": 0}, {"yPercent": 100 if i % 2 == 0 else -100, "duration": 0.55, "ease": "expo.in"}, m1 - 0.55)
s_m2 = vshot("s-m2", "asahan-live", mm[1], mm[2])
cut(s_m1, s_m2, mm[1], "whipr")
lower_third("lt-m1", mm[0], mm[1], "03 &#183; TEMPAT MAKAN", "RESTORAN BEMBAN", "Bufet sarapan, makan tengah hari &amp; makan malam")
lower_third("lt-m2", mm[1] + 0.3, mm[2] - 0.5, "03 &#183; TEMPAT MAKAN", "ASAHAN CAFE", "Kafe konsep Nyonya &#183; 10 pagi hingga 12 malam")

# ---- 9. 04 bilik & suite (AI camera-move clips)
c = T["ch4"]
chapter("ch4", c, "04", "BILIK &amp; SUITE")
rb = [SW["ch4"], 59.6, 61.9, 64.2, 66.5, 68.8, 71.1, 73.4, T["recap"]]
ROOMS = ["room-double", "room-twin", "room-deluxe", "room-junior", "room-junior-2", "room-exec", "room-exec-2", "room-exec-bath"]
KINDS = ["whip", "zoom", "whipv", "whip", "spin", "zoom", "whipr"]
sel = [vshot(f"s-v{i}", vid, rb[i], rb[i + 1], media_start=0 if i in (0, 5) else 0.3) for i, vid in enumerate(ROOMS)]
for i in range(1, len(ROOMS)):
    cut(sel[i - 1], sel[i], rb[i], KINDS[i - 1])
K = "04 &#183; BILIK &amp; SUITE"
lower_third("lt-v1", c + CH_OUT + 0.25, rb[1], K, "SUPERIOR DOUBLE", "Selesa untuk urusan kerja &amp; percutian", ("Katil Queen", "172.76 kps"))
lower_third("lt-v2", rb[1] + 0.25, rb[2], K, "SUPERIOR TWIN", "Pilihan ideal untuk peserta seminar", ("2 Katil Bujang", "172.76 kps"))
lower_third("lt-v3", rb[2] + 0.25, rb[3], K, "DELUXE", "Luas untuk seisi keluarga", ("1 Queen + 1 Bujang", "185.75 kps"))
lower_third("lt-v4", rb[3] + 0.25, rb[5], K, "JUNIOR SUITE", "Ruang tamu berasingan dengan sofa bed", ("Katil King", "464.47 kps"))
lower_third("lt-v5", rb[5] + 0.25, rb[8], K, "EXECUTIVE SUITE", "Ruang makan, bilik bacaan &amp; lounge", ("Katil King", "637.23 kps"))

# ---- 10. recap mosaic
r0, r1 = T["recap"], T["end"]
MOS = ["pool-2", "gadek", "bemban", "room-exec", "lobby", "gadek5", "asahan", "room-junior", "ext-night", "brisu-aerial",
       "bemban-breakfast", "room-twin"]
tiles = "".join(f'<div class="mt" id="mt{i}" style="left:{(i % 4) * 480}px;top:{(i // 4) * 360}px">'
                f'<img src="assets/img/{img}.jpg" alt=""/></div>' for i, img in enumerate(MOS))
clip("recap", r0, r1, (
    f'<div class="mos-stage"><div class="mos" id="mos">{tiles}</div></div><div class="shade shade-mos" id="mos-sh"></div>'
    + particles("p5-", r0, r1, 14) +
    f'<div class="mos-txt"><div class="m"><div class="mos-k" id="mos-k">HOTEL MITC MELAKA</div></div>'
    f'<div class="mos-t" id="mos-t">{chars("SEGALANYA DI SATU DESTINASI")}</div></div>'), "bg-navy", 2)
for i in range(12):
    dx, dy = ((i % 4) - 1.5) * 300, ((i // 4) - 1) * 300
    tw(f"#mt{i}", {"x": dx, "y": dy, "scale": 0.3, "opacity": 0}, {"x": 0, "y": 0, "scale": 1, "opacity": 1, "duration": 0.8, "ease": "expo.out"},
       r0 + 0.025 * ((i * 7) % 12))
tw("#mos", {"scale": 1.25, "rotationX": 0, "rotation": 0}, {"scale": 0.82, "rotationX": 18, "rotation": -4, "duration": round(r1 - r0, 3), "ease": "power2.inOut"}, r0)
tw("#mos-sh", {"opacity": 0}, {"opacity": 1, "duration": 0.7}, r0 + 0.6)
tw("#mos-k", {"yPercent": 110}, {"yPercent": 0, "duration": 0.6, "ease": "expo.out"}, r0 + 1.0)
tw("#mos-t .ch", {"z": -600, "opacity": 0}, {"z": 0, "opacity": 1, "duration": 0.8, "ease": "expo.out", "stagger": 0.025}, r0 + 1.1)
cut(sel[-1], "#recap", r0, "zoom")

# ---- 11. end card with button click
n0, n1 = r1, TOTAL
cur3 = cursor("cur3", [(n0 + 2.4, 1480, 1000), (n0 + 3.5, 820, 618)], clicks=[n0 + 3.6])
clip("endc", n0, n1, (
    '<div class="grid dark" id="end-grid"></div><div class="end-band" id="end-band"></div>'
    '<div class="end-logo-w" id="end-logo"><img src="assets/img/mitc-logo.png" alt="MITC Hotel"/><span class="sheen" id="end-sh"></span></div>'
    f'<div class="end-tag" id="end-tag">{chars("Tempah terus dengan kami")}</div>'
    '<div class="end-btns"><div class="btn btn-main" id="btn"><span class="ripple" id="ripple"></span>TEMPAH SEKARANG</div>'
    '<div class="btn" id="btn2">06-233 1551</div><div class="btn" id="btn3">mitchotel.com.my</div></div>'
    '<div class="end-addr" id="end-addr">Jalan Food City, Pusat Dagangan Antarabangsa Melaka, 75450 Ayer Keroh, Melaka</div>'
    '<div class="end-foot" id="end-foot"><span>DIURUSKAN OLEH</span><img class="end-mh" src="assets/img/mcorp-hotel-logo.png" alt="M\'Corp Hotel"/>'
    '<i></i><span>ANAK SYARIKAT</span><img class="end-mc" src="assets/img/mcorp-corporate.png" alt="MCORP"/></div>' + cur3), "bg-light", 3)
cut("#recap", "#endc", n0, "zoom")
tw("#end-band", {"xPercent": -120}, {"xPercent": 0, "duration": 0.9, "ease": "expo.inOut"}, n0 + 0.1)
tw("#end-logo", {"scale": 0.3, "opacity": 0, "rotation": -8}, {"scale": 1, "opacity": 1, "rotation": 0, "duration": 1.0, "ease": "back.out(1.6)"}, n0 + 0.35)
tw("#end-sh", {"xPercent": -150}, {"xPercent": 450, "duration": 1.1, "ease": "power2.inOut"}, n0 + 1.4)
tw("#end-tag .ch", {"yPercent": 100, "opacity": 0}, {"yPercent": 0, "opacity": 1, "duration": 0.6, "ease": "expo.out", "stagger": 0.025}, n0 + 0.9)
for i, b_ in enumerate(["#btn", "#btn2", "#btn3"]):
    tw(b_, {"y": 40, "opacity": 0, "scale": 0.9}, {"y": 0, "opacity": 1, "scale": 1, "duration": 0.7, "ease": "back.out(1.8)"}, n0 + 1.4 + i * 0.14)
tw("#end-addr", {"opacity": 0}, {"opacity": 1, "duration": 0.7}, n0 + 1.9)
tw("#end-foot", {"y": 30, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.7, "ease": "expo.out"}, n0 + 2.1)
tw("#btn", {"scale": 1}, {"scale": 0.94, "duration": 0.12, "ease": "power2.out"}, n0 + 3.6)
tw("#btn", {"scale": 0.94}, {"scale": 1.06, "duration": 0.4, "ease": "back.out(3)"}, n0 + 3.72)
tw("#ripple", {"scale": 0, "opacity": 0.7}, {"scale": 6, "opacity": 0, "duration": 0.9, "ease": "power2.out"}, n0 + 3.65)
tw("#fadeout", {"opacity": 0}, {"opacity": 1, "duration": 0.6, "ease": "power1.in"}, n1 - 0.6)

# ---- HUD: brand tags + chapter progress (from the first chapter to the recap)
h0, h1 = SW["ch1"], T["recap"]
LABELS = ["FASILITI", "DEWAN &amp; ACARA", "TEMPAT MAKAN", "BILIK &amp; SUITE"]
segs = "".join(f'<div class="seg" id="seg{i}"><div class="seg-l" id="segl{i}"><b>0{i + 1}</b> {lab}</div>'
               f'<div class="seg-tr"><div class="seg-f" id="segf{i}"></div></div></div>' for i, lab in enumerate(LABELS))
clip("hud", h0, h1, (
    '<div class="hud-tl" id="hud-tl"><span class="dot"></span>HOTEL MITC</div>'
    '<div class="hud-tr" id="hud-tr">AYER KEROH &#183; MELAKA</div>'
    f'<div class="hud-bar" id="hud-bar">{segs}</div>'), "ovl hudc", 15)
tw(["#hud-tl", "#hud-tr"], {"y": -30, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.7, "ease": "expo.out"}, h0 + 0.8)
tw("#hud-bar", {"y": 40, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.7, "ease": "expo.out"}, h0 + 0.8)
bounds = [SW["ch1"], SW["ch2"], SW["ch3"], SW["ch4"], T["recap"]]
for i in range(4):
    tw(f"#segf{i}", {"scaleX": 0}, {"scaleX": 1, "duration": round(bounds[i + 1] - bounds[i], 3), "ease": "none"}, bounds[i])
    tw(f"#segl{i}", {"opacity": 0.45}, {"opacity": 1, "duration": 0.3, "ease": "none"}, bounds[i])
    if i < 3:
        tw(f"#segl{i}", {"opacity": 1}, {"opacity": 0.45, "duration": 0.3, "ease": "none"}, bounds[i + 1])
tw(["#hud-tl", "#hud-tr", "#hud-bar"], {"opacity": 1}, {"opacity": 0, "duration": 0.3}, h1 - 0.3)

# ================================================================ assemble
CSS = open(os.path.join(HF, "..", "style-v3.css")).read()
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
      <div id="streakw" class="clip fx" data-start="0" data-duration="{at(TOTAL)}" data-track-index="20"><div id="streak"></div></div>
      <div id="fadeout" class="clip fx" data-start="0" data-duration="{at(TOTAL)}" data-track-index="22"></div>
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
