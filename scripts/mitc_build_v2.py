"""Build the Hotel MITC intro video (HyperFrames) -> edits/mitc-pengenalan/hf/index.html

usage: python3 scripts/mitc_build_v2.py

Luxury cut (v2): letterboxed, serif typography, slow cross-dissolves, graded photos with
film grain, no audio (the music is added on the social platform).  Scene lengths are in
the timeline list below; shots overlap by XF seconds for the dissolves.
"""
import json
import os

HF = os.path.join(os.path.dirname(__file__), "..", "edits", "mitc-pengenalan", "hf")
W, H = 1920, 1080
XF = 0.6           # cross-dissolve length

# The grade, vignette and film grain are applied to the whole render afterwards
# (scripts/mitc_finish.sh); per-element data-color-grading made the render >25 min.

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


def chars(text):
    """Split text into per-letter spans so letters can be staggered with transforms."""
    out = []
    for word in text.split(" "):
        if word.startswith("&"):
            out.append(f'<span class="w"><span class="ch">{word}</span></span>')
            continue
        out.append('<span class="w">' + "".join(f'<span class="ch">{c}</span>' for c in word) + "</span>")
    return " ".join(out)


def shot(cid, img, start, end, kb=(1.04, 1.12), origin="50% 50%", fade=True, track=1, shade="shade-cap", x=(0, 0)):
    """Photo with slow drift; fades in over XF before `start` (cross-dissolve)."""
    s0 = start - XF if fade else start
    inner = (f'<img id="{cid}-img" src="assets/img/{img}.jpg" alt="" '
             f'style="transform-origin:{origin}"/>' + (f'<div class="shade {shade}"></div>' if shade else ""))
    clip(cid, s0, end, inner, "shot", track)
    tw(f"#{cid}-img", {"scale": kb[0], "x": x[0]}, {"scale": kb[1], "x": x[1], "duration": round(end - s0, 3), "ease": "none"}, s0)
    if fade:
        tw(f"#{cid}", {"opacity": 0}, {"opacity": 1, "duration": XF, "ease": "sine.inOut"}, s0)


def vshot(cid, vid, start, end, track=1, shade="shade-cap"):
    """AI camera-move clip, a direct child of the stage, dissolving in like the photos."""
    s0 = start - XF
    clips.append(f'<video id="{cid}" class="clip vclip" src="assets/video/{vid}.mp4" data-start="{at(s0)}" '
                 f'data-duration="{at(end - s0)}" data-media-start="0" data-hf-media-start-basis="local" '
                 f'data-track-index="{track}" muted playsinline></video>')
    tw(f"#{cid}", {"opacity": 0}, {"opacity": 1, "duration": XF, "ease": "sine.inOut"}, s0)
    if shade:
        clip(f"{cid}-sh", s0, end, "", f"shade {shade}", track + 1)
        tw(f"#{cid}-sh", {"opacity": 0}, {"opacity": 1, "duration": XF, "ease": "sine.inOut"}, s0)


def caption(cid, start, end, kicker, title, sub, track=6):
    """Lower-left caption: tracked kicker, serif name, gold hairline, light sub-line."""
    inner = (f'<div class="cap"><div class="cap-k" id="{cid}-k">{kicker}</div>'
             f'<div class="mask"><div class="cap-t" id="{cid}-t">{title}</div></div>'
             f'<div class="cap-r" id="{cid}-r"></div><div class="cap-s" id="{cid}-s">{sub}</div></div>')
    clip(cid, start, end, inner, "ovl", track)
    tw(f"#{cid}-k", {"opacity": 0, "x": -20}, {"opacity": 1, "x": 0, "duration": 1.0}, start + 0.1)
    tw(f"#{cid}-t", {"yPercent": 105}, {"yPercent": 0, "duration": 1.1, "ease": "expo.out"}, start + 0.2)
    tw(f"#{cid}-r", {"scaleX": 0}, {"scaleX": 1, "duration": 1.2, "ease": "expo.inOut"}, start + 0.35)
    tw(f"#{cid}-s", {"opacity": 0, "y": 12}, {"opacity": 1, "y": 0, "duration": 1.0}, start + 0.6)
    tw(f"#{cid} .cap", {"opacity": 1}, {"opacity": 0, "duration": 0.45, "ease": "sine.in"}, end - 0.5)


def chapter(cid, start, end, num, word):
    """Chapter opener: roman numeral, italic serif word letter by letter, hairline."""
    inner = (f'<div class="chap"><div class="chap-n" id="{cid}-n">{num}</div>'
             f'<div class="chap-w" id="{cid}-w">{chars(word)}</div><div class="chap-r" id="{cid}-r"></div></div>')
    clip(cid, start, end, inner, "ovl", 7)
    tw(f"#{cid}-n", {"opacity": 0, "y": 16}, {"opacity": 1, "y": 0, "duration": 1.0}, start)
    tw(f"#{cid}-w .ch", {"opacity": 0, "y": 40, "filter": "blur(6px)"},
       {"opacity": 1, "y": 0, "filter": "blur(0px)", "duration": 0.9, "stagger": 0.04}, start + 0.15)
    tw(f"#{cid}-r", {"scaleX": 0}, {"scaleX": 1, "duration": 1.3, "ease": "expo.inOut"}, start + 0.3)
    tw(f"#{cid} .chap", {"opacity": 1, "y": 0}, {"opacity": 0, "y": -20, "duration": 0.6, "ease": "sine.in"}, end - 0.6)


# ================================================================ timeline
S = {}
t = 0.0
for k, d in [("intro", 3.0), ("title", 5.0), ("corp", 4.8), ("lokasi", 4.2), ("stats", 3.8),
             ("f1", 3.4), ("f2", 2.4), ("f3", 2.6),
             ("e1", 3.4), ("e2", 2.0), ("e3", 2.4), ("e4", 2.4),
             ("m1", 3.4), ("m2", 2.0), ("m3", 3.0),
             ("v0", 3.4), ("v1", 2.3), ("v2", 2.3), ("v3", 2.3), ("v4", 2.2), ("v5", 2.4), ("v6", 2.2), ("v7", 2.3),
             ("tri", 4.0), ("end", 5.2)]:
    S[k] = t
    t = round(t + d, 3)
TOTAL = t
NXT = {k: v for k, v in zip(S, list(S.values())[1:] + [TOTAL])}

# ---- intro: company line on black
i0, i1 = S["intro"], NXT["intro"]
clip("intro", i0, i1 + XF, '<div class="intro"><div class="i-r" id="i-r1"></div>'
     '<div class="i-t" id="i-t">M&#8217;CORP HOTEL SDN. BHD.</div><div class="i-r" id="i-r2"></div></div>', "bg-ink", 1)
tw("#i-r1", {"scaleX": 0}, {"scaleX": 1, "duration": 1.6, "ease": "expo.inOut"}, 0.3)
tw("#i-r2", {"scaleX": 0}, {"scaleX": 1, "duration": 1.6, "ease": "expo.inOut"}, 0.45)
tw("#i-t", {"opacity": 0, "y": 10}, {"opacity": 1, "y": 0, "duration": 1.4, "ease": "sine.out"}, 0.8)
tw("#intro .intro", {"opacity": 1}, {"opacity": 0, "duration": 0.7, "ease": "sine.in"}, i1 - 0.5)

# ---- title over the night exterior
t0, t1 = S["title"], NXT["title"]
shot("s-title", "ext-night", t0, t1, kb=(1.18, 1.05), origin="50% 40%", shade="shade-title")
clip("title", t0, t1, (
    '<div class="ttl"><div class="ttl-k" id="ttl-k">SELAMAT DATANG KE</div>'
    f'<div class="ttl-a" id="ttl-a">{chars("HOTEL MITC")}</div>'
    '<div class="ttl-r" id="ttl-r"></div>'
    '<div class="ttl-b" id="ttl-b">AYER KEROH &#183; MELAKA</div>'
    '<div class="stars" id="stars">' + "".join('<span class="star">&#9733;</span>' for _ in range(4)) + '</div></div>'), "ovl", 7)
tw("#ttl-k", {"opacity": 0}, {"opacity": 1, "duration": 1.2, "ease": "sine.out"}, t0 + 0.2)
tw("#ttl-a .ch", {"opacity": 0, "y": 50, "filter": "blur(8px)"},
   {"opacity": 1, "y": 0, "filter": "blur(0px)", "duration": 1.2, "stagger": 0.06}, t0 + 0.4)
tw("#ttl-r", {"scaleX": 0}, {"scaleX": 1, "duration": 1.6, "ease": "expo.inOut"}, t0 + 1.0)
tw("#ttl-b", {"opacity": 0, "y": 14}, {"opacity": 1, "y": 0, "duration": 1.2}, t0 + 1.5)
tw("#stars .star", {"opacity": 0, "scale": 0.6}, {"opacity": 1, "scale": 1, "duration": 0.8, "stagger": 0.12}, t0 + 1.9)
tw("#title .ttl", {"opacity": 1}, {"opacity": 0, "duration": 0.6, "ease": "sine.in"}, t1 - 0.6)

# ---- corporate: ivory panel + exterior
c0, c1 = S["corp"], NXT["corp"]
shot("s-corp", "ext-wide", c0, c1, kb=(1.12, 1.04), origin="70% 50%", shade="")
clip("corp", c0 - XF, c1, (
    '<div class="ivory" id="corp-panel">'
    '<img class="corp-logo" id="corp-logo" src="assets/img/mcorp-hotel-logo.png" alt="M\'Corp Hotel Sdn. Bhd."/>'
    '<div class="corp-k" id="corp-k">ANAK SYARIKAT PKNM</div>'
    '<div class="mask"><div class="corp-t" id="corp-t">Ditubuhkan pada<br/><em>15 November 2016</em></div></div>'
    '<div class="corp-r" id="corp-r"></div>'
    '<div class="corp-s" id="corp-s">Dipertanggungjawabkan mengurus dan mengendalikan<br/>operasi Hotel MITC, Ayer Keroh, Melaka.</div></div>'), "ovl", 5)
tw("#corp-panel", {"xPercent": -100}, {"xPercent": 0, "duration": 1.3, "ease": "expo.inOut"}, c0 - XF)
tw("#corp-logo", {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0, "duration": 1.2}, c0 + 0.4)
tw("#corp-k", {"opacity": 0}, {"opacity": 1, "duration": 1.0}, c0 + 0.8)
tw("#corp-t", {"yPercent": 100}, {"yPercent": 0, "duration": 1.2, "ease": "expo.out"}, c0 + 1.0)
tw("#corp-r", {"scaleX": 0}, {"scaleX": 1, "duration": 1.2, "ease": "expo.inOut"}, c0 + 1.3)
tw("#corp-s", {"opacity": 0, "y": 12}, {"opacity": 1, "y": 0, "duration": 1.0}, c0 + 1.6)
tw("#corp-panel", {"opacity": 1}, {"opacity": 0, "duration": 0.6, "ease": "sine.in"}, c1 - 0.6)

# ---- lokasi
l0, l1 = S["lokasi"], NXT["lokasi"]
shot("s-lok", "ext-day", l0, l1, kb=(1.02, 1.1), origin="50% 30%", shade="shade-bottom")
clip("lokasi", l0, l1, (
    '<div class="lok"><div class="cap-k" id="lok-k">LOKASI STRATEGIK</div>'
    '<div class="mask"><div class="lok-t" id="lok-t">Ayer Keroh, Melaka</div></div>'
    '<div class="cap-r" id="lok-r"></div>'
    '<div class="lok-s" id="lok-s1">Berhadapan Pusat Dagangan Antarabangsa Melaka (MITC)</div>'
    '<div class="lok-s" id="lok-s2">10 minit dari Tol Ayer Keroh</div></div>'), "ovl", 7)
tw("#lok-k", {"opacity": 0, "x": -20}, {"opacity": 1, "x": 0, "duration": 1.0}, l0 + 0.1)
tw("#lok-t", {"yPercent": 105}, {"yPercent": 0, "duration": 1.1, "ease": "expo.out"}, l0 + 0.2)
tw("#lok-r", {"scaleX": 0}, {"scaleX": 1, "duration": 1.2, "ease": "expo.inOut"}, l0 + 0.4)
tw("#lok-s1", {"opacity": 0, "y": 12}, {"opacity": 1, "y": 0, "duration": 1.0}, l0 + 0.7)
tw("#lok-s2", {"opacity": 0, "y": 12}, {"opacity": 1, "y": 0, "duration": 1.0}, l0 + 1.0)
tw("#lokasi .lok", {"opacity": 1}, {"opacity": 0, "duration": 0.5, "ease": "sine.in"}, l1 - 0.5)

# ---- stats
s0, s1 = S["stats"], NXT["stats"]
shot("s-stats", "lobby", s0, s1, kb=(1.12, 1.04), shade="shade-dark")
clip("stats", s0, s1, (
    '<div class="stats">'
    '<div class="stat" id="st1"><div class="stat-n">4<span class="stat-star">&#9733;</span></div><div class="stat-l">BERTARAF BINTANG</div></div>'
    '<div class="stat-d" id="sd1"></div>'
    '<div class="stat" id="st2"><div class="stat-n">188</div><div class="stat-l">BILIK PENGINAPAN</div></div>'
    '<div class="stat-d" id="sd2"></div>'
    '<div class="stat" id="st3"><div class="stat-n">24<span class="stat-u">jam</span></div><div class="stat-l">PERKHIDMATAN</div></div></div>'), "ovl", 7)
for i in range(3):
    tw(f"#st{i + 1}", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0, "duration": 1.2}, s0 + 0.2 + i * 0.35)
tw(["#sd1", "#sd2"], {"scaleY": 0}, {"scaleY": 1, "duration": 1.3, "ease": "expo.inOut"}, s0 + 0.5)
tw("#stats .stats", {"opacity": 1}, {"opacity": 0, "duration": 0.5, "ease": "sine.in"}, s1 - 0.5)

# ---- I. fasiliti
shot("s-f1", "pool-2", S["f1"], NXT["f1"], kb=(1.04, 1.12))
shot("s-f2", "pool-night", S["f2"], NXT["f2"], kb=(1.1, 1.03), origin="50% 60%")
shot("s-f3", "lobby", S["f3"], NXT["f3"], kb=(1.06, 1.12), origin="40% 50%", x=(20, -20))
chapter("ch1", S["f1"], S["f1"] + 1.9, "I", "Fasiliti")
caption("cp-f1", S["f1"] + 1.8, NXT["f2"], "FASILITI", "Kolam Renang", "Kolam renang &amp; taman permainan air kanak-kanak")
caption("cp-f2", S["f3"], NXT["f3"], "FASILITI", "Lobi Utama", "Sambutan mesra, perkhidmatan 24 jam")

# ---- II. dewan & acara
shot("s-e1", "gadek", S["e1"], NXT["e1"], kb=(1.04, 1.12), origin="50% 40%")
shot("s-e2", "gadek-event", S["e2"], NXT["e2"], kb=(1.1, 1.04))
shot("s-e3", "gadek5", S["e3"], NXT["e3"], kb=(1.06, 1.12), x=(-20, 20))
shot("s-e4", "brisu-aerial", S["e4"], NXT["e4"], kb=(1.04, 1.12))
chapter("ch2", S["e1"], S["e1"] + 1.9, "II", "Dewan &amp; Acara")
caption("cp-e1", S["e1"] + 1.8, NXT["e2"], "DEWAN &amp; ACARA", "Dewan Gadek", "Perkahwinan, persidangan &amp; jamuan rasmi")
caption("cp-e2", S["e3"], NXT["e3"], "DEWAN &amp; ACARA", "Bilik Gadek 5", "Mesyuarat, taklimat &amp; bengkel")
caption("cp-e3", S["e4"], NXT["e4"], "DEWAN &amp; ACARA", "Halaman Brisu", "Ruang majlis terbuka di tengah taman")
clip("lg-gadek", S["e1"] + 1.8, NXT["e2"], '<img class="venue-logo" id="lg-gadek-i" src="assets/img/gadek-logo.png" alt="Gadek Ballroom"/>', "ovl", 8)
tw("#lg-gadek-i", {"opacity": 0}, {"opacity": 0.92, "duration": 1.2, "ease": "sine.out"}, S["e1"] + 2.0)
tw("#lg-gadek-i", {"opacity": 0.92}, {"opacity": 0, "duration": 0.45, "ease": "sine.in"}, NXT["e2"] - 0.5)

# ---- III. tempat makan (Asahan as a diptych)
shot("s-m1", "bemban", S["m1"], NXT["m1"], kb=(1.04, 1.12))
shot("s-m2", "bemban-breakfast", S["m2"], NXT["m2"], kb=(1.1, 1.03))
m3, m3e = S["m3"], NXT["m3"]
clip("s-m3", m3 - XF, m3e, (
    '<div class="dip"><div class="dip-p" id="dip-l"><img id="dip-li" src="assets/img/asahan.jpg" alt="" '
    '/></div>'
    '<div class="dip-p" id="dip-r"><img id="dip-ri" src="assets/img/asahan-live.jpg" alt="" '
    '/></div></div><div class="shade shade-cap"></div>'), "shot bg-ink", 1)
tw("#s-m3", {"opacity": 0}, {"opacity": 1, "duration": XF, "ease": "sine.inOut"}, m3 - XF)
tw("#dip-l", {"yPercent": -8}, {"yPercent": 0, "duration": 1.4, "ease": "expo.out"}, m3 - XF)
tw("#dip-r", {"yPercent": 8}, {"yPercent": 0, "duration": 1.4, "ease": "expo.out"}, m3 - XF)
tw(["#dip-li", "#dip-ri"], {"scale": 1.12}, {"scale": 1.02, "duration": round(m3e - m3 + XF, 3), "ease": "none"}, m3 - XF)
chapter("ch3", S["m1"], S["m1"] + 1.9, "III", "Tempat Makan")
caption("cp-m1", S["m1"] + 1.8, NXT["m2"], "TEMPAT MAKAN", "Restoran Bemban", "Bufet sarapan, makan tengah hari &amp; makan malam")
caption("cp-m2", m3, m3e, "TEMPAT MAKAN", "Asahan Cafe", "Kafe konsep Nyonya &#183; 10 pagi hingga 12 malam")

# ---- IV. bilik & suite (AI camera-move clips)
ROOMS = ["room-double", "room-twin", "room-deluxe", "room-junior", "room-junior-2", "room-exec", "room-exec-2", "room-exec-bath"]
for i, vid in enumerate(ROOMS):
    vshot(f"s-v{i}", vid, S[f"v{i}"], NXT[f"v{i}"])
chapter("ch4", S["v0"], S["v0"] + 1.9, "IV", "Bilik &amp; Suite")
K = "BILIK &amp; SUITE"
caption("cp-v1", S["v0"] + 1.8, NXT["v0"], K, "Superior Double", "Katil Queen &#183; 172.76 kaki persegi")
caption("cp-v2", S["v1"], NXT["v1"], K, "Superior Twin", "2 Katil Bujang &#183; 172.76 kaki persegi")
caption("cp-v3", S["v2"], NXT["v2"], K, "Deluxe", "1 Katil Queen + 1 Katil Bujang &#183; 185.75 kaki persegi")
caption("cp-v4", S["v3"], NXT["v4"], K, "Junior Suite", "Katil King &#183; Ruang tamu berasingan &#183; 464.47 kaki persegi")
caption("cp-v5", S["v5"], NXT["v7"], K, "Executive Suite", "Katil King &#183; Ruang makan &amp; lounge &#183; 637.23 kaki persegi")

# ---- triptych + line
r0, r1 = S["tri"], NXT["tri"]
panels = "".join(
    f'<div class="tri-p" id="tri{i}"><img id="tri{i}-i" src="assets/img/{img}.jpg" alt=""/></div>'
    for i, img in enumerate(["pool-night", "gadek", "room-exec"]))
clip("tri", r0 - XF, r1, f'<div class="tri">{panels}</div><div class="shade shade-dark2"></div>'
     '<div class="tri-txt"><div class="tri-a" id="tri-a">Di mana keselesaan</div>'
     '<div class="tri-b" id="tri-b">bertemu keanggunan.</div></div>', "bg-ink", 2)
tw("#tri", {"opacity": 0}, {"opacity": 1, "duration": XF, "ease": "sine.inOut"}, r0 - XF)
for i in range(3):
    tw(f"#tri{i}", {"opacity": 0, "y": 40 if i % 2 == 0 else -40}, {"opacity": 1, "y": 0, "duration": 1.4, "ease": "expo.out"}, r0 - 0.3 + i * 0.15)
    tw(f"#tri{i}-i", {"scale": 1.14}, {"scale": 1.02, "duration": round(r1 - r0 + 0.3, 3), "ease": "none"}, r0 - 0.3)
tw("#tri-a", {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0, "duration": 1.3}, r0 + 0.6)
tw("#tri-b", {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0, "duration": 1.3}, r0 + 1.0)
tw("#tri .tri-txt", {"opacity": 1}, {"opacity": 0, "duration": 0.5, "ease": "sine.in"}, r1 - 0.5)

# ---- end card (ivory, gold frame)
n0, n1 = S["end"], TOTAL
clip("endc", n0 - XF, n1, (
    '<div class="frame" id="end-frame"></div>'
    '<img class="end-logo" id="end-logo" src="assets/img/mitc-logo.png" alt="MITC Hotel"/>'
    '<div class="end-r" id="end-r"></div>'
    '<div class="end-tag" id="end-tag">Tempah terus dengan kami</div>'
    '<div class="end-row" id="end-row"><span>06-233 1551</span><i></i><span>mitchotel.com.my</span></div>'
    '<div class="end-addr" id="end-addr">Jalan Food City, Pusat Dagangan Antarabangsa Melaka, 75450 Ayer Keroh, Melaka</div>'
    '<div class="end-foot" id="end-foot"><div class="end-by">DIURUSKAN OLEH</div>'
    '<img class="end-mh" src="assets/img/mcorp-hotel-logo.png" alt="M\'Corp Hotel Sdn. Bhd."/>'
    '<div class="end-sep"></div><div class="end-by">ANAK SYARIKAT</div>'
    '<img class="end-mc" src="assets/img/mcorp-corporate.png" alt="MCORP"/></div>'), "bg-ivory", 3)
tw("#endc", {"opacity": 0}, {"opacity": 1, "duration": XF + 0.2, "ease": "sine.inOut"}, n0 - XF)
tw("#end-frame", {"opacity": 0, "scale": 1.03}, {"opacity": 1, "scale": 1, "duration": 1.6}, n0 - 0.2)
tw("#end-logo", {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0, "duration": 1.4}, n0 + 0.1)
tw("#end-r", {"scaleX": 0}, {"scaleX": 1, "duration": 1.3, "ease": "expo.inOut"}, n0 + 0.6)
tw("#end-tag", {"opacity": 0, "y": 14}, {"opacity": 1, "y": 0, "duration": 1.2}, n0 + 0.8)
tw("#end-row", {"opacity": 0, "y": 14}, {"opacity": 1, "y": 0, "duration": 1.2}, n0 + 1.1)
tw("#end-addr", {"opacity": 0}, {"opacity": 1, "duration": 1.2}, n0 + 1.4)
tw("#end-foot", {"opacity": 0, "y": 14}, {"opacity": 1, "y": 0, "duration": 1.2}, n0 + 1.7)
tw("#fadeout", {"opacity": 0}, {"opacity": 1, "duration": 0.8, "ease": "sine.in"}, n1 - 0.8)

# letterbox: slides in at the start, stays for the whole film
tw("#lb-top", {"yPercent": -100}, {"yPercent": 0, "duration": 1.4, "ease": "expo.inOut"}, 0.0)
tw("#lb-bot", {"yPercent": 100}, {"yPercent": 0, "duration": 1.4, "ease": "expo.inOut"}, 0.0)

# ================================================================ assemble
CSS = open(os.path.join(HF, "..", "style-v2.css")).read()
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
      {chr(10).join('      ' + c for c in clips).lstrip()}
      <div id="lb-top" class="clip fx lb" data-start="0" data-duration="{at(TOTAL)}" data-track-index="20"></div>
      <div id="lb-bot" class="clip fx lb" data-start="0" data-duration="{at(TOTAL)}" data-track-index="21"></div>
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
print("total", TOTAL, "s;", len(clips), "clips")
print(json.dumps(S))
