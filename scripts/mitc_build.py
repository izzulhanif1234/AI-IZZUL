"""Build the Hotel MITC intro video (HyperFrames) -> edits/mitc-pengenalan/hf/index.html

usage: python3 scripts/mitc_build.py

All scene timings come from SCENES below (seconds); every cut is snapped to the
nearest beat of the music bed listed in assets/bgm/beats.json when that file exists.
"""
import json
import os
import subprocess

HF = os.path.join(os.path.dirname(__file__), "..", "edits", "mitc-pengenalan", "hf")
W, H = 1920, 1080

# ---------------------------------------------------------------- beat grid
BEATS = []
_bp = os.path.join(HF, "assets", "bgm", "beats.json")
if os.path.exists(_bp):
    BEATS = json.load(open(_bp))["beats"]


def snap(t):
    if not BEATS:
        return round(t, 3)
    return round(min(BEATS, key=lambda b: abs(b - t)), 3)


def dur_of(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True).stdout.strip()
    return round(float(out), 3)


# ---------------------------------------------------------------- storyboard
# Rough cut points (s); snapped to beats.  Each value is the START of that block.
DROP, BEAT = 14.4, 0.4926     # music drop lands on the stats scene; see scripts/mitc_music.py


def B(bar, beat=0):
    """Film time of a bar line (counted from the drop) plus beats."""
    return DROP + (4 * bar + beat) * BEAT


RAW = {
    "intro": 0.0,
    "title": 2.4,
    "corp": 6.6,
    "lokasi": 10.8,
    "stats": DROP,
    "fas": B(2), "fas2": B(3, 1), "fas3": B(4), "fas4": B(5),
    "dewan": B(6), "dewan2": B(7, 1), "dewan3": B(8), "dewan4": B(9),
    "makan": B(10), "makan2": B(11, 1), "makan3": B(12), "makan4": B(13),
    "bilik": B(14), "bilik2": B(16), "bilik3": B(17), "bilik4": B(18), "bilik5": B(19),
    "bilik6": B(20), "bilik7": B(21), "bilik8": B(22),
    "recap": B(23),
    "end": B(25),
    "fin": 68.4,
}
T = {k: (v if k in ("intro", "fin") else snap(v)) for k, v in RAW.items()}
TOTAL = T["fin"]

# ---------------------------------------------------------------- html helpers
clips = []      # timed DOM (visual)
tl = []         # gsap lines for the root timeline
audio = []      # (src, start, vol)


def at(t):
    return f"{t:.3f}"


def clip(cid, start, end, inner, cls="", track=1, style=""):
    clips.append(
        f'<div id="{cid}" class="clip {cls}" data-start="{at(start)}" data-duration="{at(end - start)}" '
        f'data-track-index="{track}"{f" style=\"{style}\"" if style else ""}>{inner}</div>')


def tw(sel, frm, to, start):
    """fromTo tween on the root timeline (immediateRender off, seek-safe)."""
    to = dict(to)
    to.setdefault("ease", "power3.out")
    to["immediateRender"] = False
    tl.append(f'tl.fromTo({json.dumps(sel)}, {js(frm)}, {js(to)}, {at(start)});')


def js(d):
    parts = []
    for k, v in d.items():
        if isinstance(v, str) and v.startswith("@"):
            parts.append(f"{k}: {v[1:]}")
        else:
            parts.append(f"{k}: {json.dumps(v)}")
    return "{ " + ", ".join(parts) + " }"


def sfx(name, start, vol, offset=0.0, maxlen=None):
    audio.append((f"assets/sfx/{name}.mp3", round(max(0.0, start), 3), vol, offset, maxlen))


def shot(cid, img, start, end, kb=(1.06, 1.16), origin="50% 50%", punch=True, track=1, shade="", extra=""):
    """Full-frame photo with Ken Burns drift; optional zoom-blur punch-in on the cut."""
    inner = (f'<div class="kb" id="{cid}-kb"><img id="{cid}-img" src="assets/img/{img}.jpg" alt="" '
             f'style="transform-origin:{origin}"/></div>'
             + (f'<div class="shade {shade}"></div>' if shade else "") + extra)
    clip(cid, start, end, inner, "shot", track)
    tw(f"#{cid}-img", {"scale": kb[0]}, {"scale": kb[1], "duration": round(end - start, 3), "ease": "none"}, start)
    if punch:
        tw(f"#{cid}-kb", {"scale": 1.22, "filter": "blur(16px)"},
           {"scale": 1, "filter": "blur(0px)", "duration": 0.55, "ease": "expo.out"}, start)


def vshot(cid, vid, start, end, punch=True, track=1, shade="", media_start=0.3):
    """Full-frame AI camera-move clip (muted).  The <video> is a direct child of the stage
    (a timed wrapper would desync the frame extractor); the shade is its own layer."""
    clips.append(
        f'<video id="{cid}" class="clip vclip" src="assets/video/{vid}.mp4" data-start="{at(start)}" '
        f'data-duration="{at(end - start)}" data-media-start="{media_start}" data-hf-media-start-basis="local" '
        f'data-track-index="{track}" muted playsinline></video>')
    if shade:
        clip(f"{cid}-sh", start, end, "", f"shade {shade}", track + 1)
    if punch:
        tw(f"#{cid}", {"scale": 1.22, "filter": "blur(16px)"},
           {"scale": 1, "filter": "blur(0px)", "duration": 0.55, "ease": "expo.out"}, start)


STAR = ('<svg viewBox="0 0 24 24"><path d="M12 1.8l3.1 6.6 7.2.9-5.3 5 1.4 7.1L12 17.9 5.6 21.4 7 14.3 1.7 9.3l7.2-.9z"/></svg>')
ICON = {
    "pin": '<svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.6A2.6 2.6 0 1 1 12 6.4a2.6 2.6 0 0 1 0 5.2z"/></svg>',
    "car": '<svg viewBox="0 0 24 24"><path d="M18.9 6c-.2-.6-.8-1-1.4-1H6.5c-.7 0-1.2.4-1.4 1L3 12v8c0 .6.4 1 1 1h1c.6 0 1-.4 1-1v-1h12v1c0 .6.4 1 1 1h1c.6 0 1-.4 1-1v-8l-2.1-6zM6.5 16a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm11 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zM5 11l1.5-4.5h11L19 11H5z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>',
    "web": '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm6.9 6h-3a15.6 15.6 0 0 0-1.4-3.6A8 8 0 0 1 18.9 8zM12 4c.8 1.2 1.5 2.5 1.9 4h-3.8c.4-1.4 1.1-2.8 1.9-4zM4.3 14a8.2 8.2 0 0 1 0-4h3.4a16.5 16.5 0 0 0 0 4H4.3zm.8 2h3c.3 1.3.8 2.5 1.4 3.6A8 8 0 0 1 5.1 16zm3-8h-3a8 8 0 0 1 4.4-3.6C8.9 5.5 8.4 6.7 8.1 8zM12 20c-.8-1.2-1.5-2.5-1.9-4h3.8c-.4 1.4-1.1 2.8-1.9 4zm2.3-6H9.7a14.7 14.7 0 0 1 0-4h4.6a14.7 14.7 0 0 1 0 4zm.3 5.6c.6-1.1 1.1-2.3 1.4-3.6h3a8 8 0 0 1-4.4 3.6zm1.7-5.6a16.5 16.5 0 0 0 0-4h3.4a8.2 8.2 0 0 1 0 4h-3.4z"/></svg>',
}


def flash(t, peak=0.85, d=0.4):
    tw("#flash", {"opacity": peak}, {"opacity": 0, "duration": d, "ease": "power2.out"}, t)


def leak(t, d=1.4):
    tw("#leak", {"xPercent": -60, "opacity": 0}, {"keyframes": "@[{opacity:0.9,duration:0.35},{opacity:0,duration:" + str(d - 0.35) + "}]",
                                                    "xPercent": 60, "duration": d, "ease": "power1.inOut"}, t)


def card(cid, start, end, kicker, title, sub, track=6):
    inner = (f'<div class="card"><div class="card-bar" id="{cid}-bar"></div>'
             f'<div class="card-k" id="{cid}-k">{kicker}</div>'
             f'<div class="card-t-mask"><div class="card-t" id="{cid}-t">{title}</div></div>'
             f'<div class="card-s" id="{cid}-s">{sub}</div></div>')
    clip(cid, start, end, inner, "ovl", track)
    tw(f"#{cid}-bar", {"scaleY": 0}, {"scaleY": 1, "duration": 0.45, "ease": "expo.out"}, start + 0.05)
    tw(f"#{cid}-k", {"x": -40, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.5}, start + 0.12)
    tw(f"#{cid}-t", {"yPercent": 110}, {"yPercent": 0, "duration": 0.6, "ease": "expo.out"}, start + 0.18)
    tw(f"#{cid}-s", {"y": 20, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.5}, start + 0.38)
    tw(f"#{cid} .card", {"opacity": 1, "x": 0}, {"opacity": 0, "x": -60, "duration": 0.25, "ease": "power2.in"}, end - 0.27)
    sfx("whoosh-short", start + 0.05, 0.28)


def slam(cid, start, end, num, word):
    """Section opener: outlined number + giant word, then it clears for the card."""
    inner = (f'<div class="slam"><div class="slam-n" id="{cid}-n">{num}</div>'
             f'<div class="slam-w" id="{cid}-w">{word}</div><div class="slam-line" id="{cid}-l"></div></div>')
    clip(cid, start, end, inner, "ovl", 7)
    tw(f"#{cid}-w", {"scale": 1.5, "opacity": 0, "filter": "blur(20px)"},
       {"scale": 1, "opacity": 1, "filter": "blur(0px)", "duration": 0.6, "ease": "expo.out"}, start + 0.02)
    tw(f"#{cid}-n", {"y": 50, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.5}, start + 0.15)
    tw(f"#{cid}-l", {"scaleX": 0}, {"scaleX": 1, "duration": 0.7, "ease": "expo.out"}, start + 0.25)
    tw(f"#{cid} .slam", {"opacity": 1, "y": 0}, {"opacity": 0, "y": -80, "duration": 0.3, "ease": "power2.in"}, end - 0.3)
    flash(start, 0.9, 0.45)
    leak(start)
    sfx("whoosh", max(0, start - 0.25), 0.5)
    sfx("impact-bass-1", start, 0.5)


# ================================================================ SCENES
# ---- 1. intro + title
i0, i1 = T["intro"], T["title"]
clip("intro", i0, i1, (
    '<div class="intro"><div class="i-top" id="i-top">M&#8217;CORP HOTEL SDN. BHD.</div>'
    '<div class="i-line" id="i-line"></div><div class="i-bot" id="i-bot">MEMPERSEMBAHKAN</div></div>'), "bg-ink", 1)
tw("#i-line", {"scaleX": 0}, {"scaleX": 1, "duration": 1.0, "ease": "expo.inOut"}, 0.15)
tw("#i-top", {"y": 30, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 1.1}, 0.55)
tw("#i-bot", {"y": -24, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.9}, 0.85)
tw("#intro .intro", {"opacity": 1, "scale": 1}, {"opacity": 0, "scale": 1.08, "duration": 0.35, "ease": "power2.in"}, i1 - 0.4)
sfx("riser", 0.0, 0.4, offset=round(10.03 - T["title"], 3))
sfx("sparkle", 0.6, 0.25)

t0, t1 = T["title"], T["corp"]
shot("s-title", "ext-night", t0, t1, kb=(1.28, 1.08), origin="50% 40%", punch=False, shade="shade-full")
clip("title", t0, t1, (
    '<div class="ttl"><div class="ttl-mask"><div class="ttl-a" id="ttl-a">HOTEL MITC</div></div>'
    '<div class="ttl-b" id="ttl-b">MELAKA</div>'
    '<div class="stars">' + "".join(f'<span class="star" id="st{i}">{STAR}</span>' for i in range(4)) + '</div>'
    '<div class="ttl-c" id="ttl-c">HOTEL BERTARAF 4 BINTANG &#183; AYER KEROH</div>'
    '<div class="sheen" id="ttl-sheen"></div></div>'), "ovl", 7)
flash(t0, 1.0, 0.6)
tw("#ttl-a", {"yPercent": 105}, {"yPercent": 0, "duration": 0.8, "ease": "expo.out"}, t0 + 0.1)
tw("#ttl-b", {"opacity": 0}, {"opacity": 1, "duration": 1.0}, t0 + 0.45)
for i in range(4):
    tw(f"#st{i}", {"scale": 0, "rotation": -90, "opacity": 0}, {"scale": 1, "rotation": 0, "opacity": 1, "duration": 0.45, "ease": "back.out(2.4)"}, t0 + 0.9 + i * 0.14)
    sfx("pop", t0 + 0.9 + i * 0.14, 0.22)
tw("#ttl-c", {"y": 20, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6}, t0 + 1.5)
tw("#ttl-sheen", {"xPercent": -120}, {"xPercent": 120, "duration": 1.1, "ease": "power2.inOut"}, t0 + 1.7)
tw("#title .ttl", {"opacity": 1, "scale": 1}, {"opacity": 0, "scale": 0.94, "duration": 0.3, "ease": "power2.in"}, t1 - 0.32)
sfx("impact-bass-2", t0, 0.6)
sfx("whoosh-cinematic", t0 - 0.2, 0.35)
sfx("sparkle", t0 + 1.0, 0.3)

# ---- 2. corporate: anak syarikat
c0, c1 = T["corp"], T["lokasi"]
shot("s-corp", "ext-wide", c0, c1, kb=(1.12, 1.02), origin="70% 40%", punch=False)
clip("corp", c0, c1, (
    '<div class="panel" id="corp-panel"><div class="hex"></div>'
    '<div class="corp-head" id="corp-head"><span class="chev"></span><div>ANAK<br/>SYARIKAT</div></div>'
    '<div class="corp-sub" id="corp-sub">Ditubuhkan oleh PKNM pada</div>'
    '<div class="corp-date" id="corp-date">15 NOVEMBER 2016</div>'
    '<div class="corp-sub2" id="corp-sub2">Mengurus &amp; mengendalikan operasi<br/><b>Hotel MITC, Ayer Keroh, Melaka</b></div></div>'
    '<div class="logo-card" id="corp-logo"><img src="assets/img/mcorp-hotel-logo.png" alt="M\'Corp Hotel Sdn. Bhd."/></div>'), "ovl", 5)
flash(c0, 0.8, 0.4)
tw("#corp-panel", {"xPercent": -100}, {"xPercent": 0, "duration": 0.7, "ease": "expo.out"}, c0)
tw("#corp-head", {"x": -60, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.6}, c0 + 0.35)
tw("#corp-logo", {"y": 60, "opacity": 0, "scale": 0.9}, {"y": 0, "opacity": 1, "scale": 1, "duration": 0.7, "ease": "back.out(1.6)"}, c0 + 0.7)
tw("#corp-sub", {"y": 20, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.5}, c0 + 1.1)
tw("#corp-date", {"y": 30, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.7}, c0 + 1.3)
tw("#corp-sub2", {"y": 20, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6}, c0 + 2.0)
tw(["#corp-panel", "#corp-logo"], {"opacity": 1}, {"opacity": 0, "duration": 0.25, "ease": "power2.in"}, c1 - 0.27)
sfx("whoosh", c0 - 0.15, 0.45)
sfx("chime", c0 + 0.75, 0.3)
sfx("click", c0 + 1.35, 0.3)
sfx("click", c0 + 2.0, 0.25)

# ---- 3. lokasi
l0, l2 = T["lokasi"], T["stats"]
shot("s-lok1", "ext-day", l0, l2, kb=(1.0, 1.12), origin="50% 30%", shade="shade-bottom")
clip("lokasi", l0, l2, (
    '<div class="lok"><div class="kick gold" id="lok-k">LOKASI STRATEGIK</div>'
    '<div class="ttl-mask"><div class="lok-t" id="lok-t">DI JANTUNG AYER KEROH</div></div>'
    '<div class="chips"><div class="chip" id="chip1"><span class="ic">' + ICON["pin"] + '</span>'
    'Bertentangan Pusat Dagangan Antarabangsa Melaka (MITC)</div>'
    '<div class="chip" id="chip2"><span class="ic">' + ICON["car"] + '</span>10 minit dari Tol Ayer Keroh</div></div></div>'), "ovl", 7)
flash(l0, 0.7, 0.35)
tw("#lok-k", {"x": -40, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.5}, l0 + 0.1)
tw("#lok-t", {"yPercent": 105}, {"yPercent": 0, "duration": 0.7, "ease": "expo.out"}, l0 + 0.25)
tw("#chip1", {"x": -80, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.6, "ease": "back.out(1.4)"}, l0 + 0.9)
tw("#chip2", {"x": -80, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.6, "ease": "back.out(1.4)"}, l0 + 1.4)
tw("#lokasi .lok", {"opacity": 1}, {"opacity": 0, "duration": 0.25}, l2 - 0.27)
sfx("whoosh", l0 - 0.2, 0.4)
sfx("pop", l0 + 0.9, 0.3)
sfx("pop", l0 + 1.4, 0.3)

# ---- 4. stats
s0, s1 = T["stats"], T["fas"]
shot("s-stats", "lobby", s0, s1, kb=(1.1, 1.2), punch=False, shade="shade-navy")
clip("stats", s0, s1, (
    '<div class="stats">'
    '<div class="stat" id="stat1"><div class="stat-n"><span id="n1">0</span><span class="stat-star">' + STAR + '</span></div><div class="stat-l">BERTARAF<br/>4 BINTANG</div></div>'
    '<div class="stat-div" id="sd1"></div>'
    '<div class="stat" id="stat2"><div class="stat-n"><span id="n2">0</span></div><div class="stat-l">BILIK<br/>PENGINAPAN</div></div>'
    '<div class="stat-div" id="sd2"></div>'
    '<div class="stat" id="stat3"><div class="stat-n"><span id="n3">0</span><span class="stat-u">JAM</span></div><div class="stat-l">PERKHIDMATAN<br/>SETIAP HARI</div></div>'
    '</div>'), "ovl", 7)
flash(s0, 0.8, 0.4)
for i, (sel, target, d) in enumerate([("#n1", 4, 0.6), ("#n2", 188, 1.4), ("#n3", 24, 1.0)]):
    st = s0 + 0.2 + i * 0.55
    tw(f"#stat{i + 1}", {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "expo.out"}, st)
    tl.append(f'tl.fromTo({{v:0}}, {{v:0}}, {{v:{target}, duration:{d}, ease:"power2.out", immediateRender:false, '
              f'onUpdate:function(){{document.querySelector("{sel}").textContent=Math.round(this.targets()[0].v);}}}}, {at(st + 0.1)});')
    sfx("click", st, 0.3)
tw(["#sd1", "#sd2"], {"scaleY": 0}, {"scaleY": 1, "duration": 0.6, "ease": "expo.out"}, s0 + 0.4)
tw("#stats .stats", {"opacity": 1, "scale": 1}, {"opacity": 0, "scale": 1.06, "duration": 0.28, "ease": "power2.in"}, s1 - 0.3)
sfx("whoosh", s0 - 0.2, 0.4)
sfx("impact-bass-2", s0 + 1.4, 0.35)

# ---- 5. 01 fasiliti
f = [T["fas"], T["fas2"], T["fas3"], T["fas4"], T["dewan"]]
shot("s-f1", "pool", f[0], f[1], kb=(1.04, 1.14), punch=False, shade="shade-left")
shot("s-f2", "pool-kids", f[1], f[2], kb=(1.04, 1.12), shade="shade-left")
shot("s-f3", "pool-night", f[2], f[3], kb=(1.04, 1.14), shade="shade-left")
shot("s-f4", "lobby", f[3], f[4], kb=(1.14, 1.04), origin="60% 50%", shade="shade-left")
slam("slam1", f[0], f[0] + 1.35, "01", "FASILITI")
card("card-f1", f[0] + 1.3, f[3], "01 &#183; FASILITI", "KOLAM RENANG", "Kolam &amp; taman permainan air kanak-kanak")
card("card-f2", f[3], f[4], "01 &#183; FASILITI", "LOBI UTAMA", "Perkhidmatan mesra 24 jam")
for t in f[1:3]:
    sfx("whoosh-short", t - 0.05, 0.22)

# ---- 6. 02 dewan & acara
e = [T["dewan"], T["dewan2"], T["dewan3"], T["dewan4"], T["makan"]]
shot("s-e1", "gadek", e[0], e[1], kb=(1.04, 1.14), origin="50% 40%", punch=False, shade="shade-left")
shot("s-e2", "gadek-event", e[1], e[2], kb=(1.06, 1.14), shade="shade-left")
shot("s-e3", "gadek5", e[2], e[3], kb=(1.04, 1.12), shade="shade-left")
shot("s-e4", "brisu-aerial", e[3], e[4], kb=(1.04, 1.16), shade="shade-left")
slam("slam2", e[0], e[0] + 1.35, "02", "DEWAN &amp; ACARA")
card("card-e1", e[0] + 1.3, e[2], "02 &#183; DEWAN &amp; ACARA", "DEWAN GADEK", "Perkahwinan, persidangan &amp; jamuan rasmi")
card("card-e2", e[2], e[3], "02 &#183; DEWAN &amp; ACARA", "BILIK GADEK 5", "Mesyuarat, taklimat &amp; bengkel")
card("card-e3", e[3], e[4], "02 &#183; DEWAN &amp; ACARA", "HALAMAN BRISU", "Ruang majlis terbuka di tengah taman")
clip("lg-gadek", e[0] + 1.3, e[2], '<img class="venue-logo" id="lg-gadek-i" src="assets/img/gadek-logo.png" alt="Gadek Ballroom"/>', "ovl", 8)
tw("#lg-gadek-i", {"opacity": 0, "y": -20}, {"opacity": 1, "y": 0, "duration": 0.6}, e[0] + 1.5)
clip("lg-brisu", e[3], e[4], '<img class="venue-logo light" id="lg-brisu-i" src="assets/img/brisu-logo.png" alt="Brisu Courtyard"/>', "ovl", 8)
tw("#lg-brisu-i", {"opacity": 0, "y": -20}, {"opacity": 1, "y": 0, "duration": 0.6}, e[3] + 0.3)
sfx("whoosh-short", e[1] - 0.05, 0.22)

# ---- 7. 03 tempat makan
m = [T["makan"], T["makan2"], T["makan3"], T["makan4"], T["bilik"]]
shot("s-m1", "bemban", m[0], m[1], kb=(1.04, 1.14), punch=False, shade="shade-left")
shot("s-m2", "bemban-breakfast", m[1], m[2], kb=(1.06, 1.16), shade="shade-left")
shot("s-m3", "asahan", m[2], m[3], kb=(1.04, 1.12), origin="70% 50%", shade="shade-left")
shot("s-m4", "asahan-live", m[3], m[4], kb=(1.04, 1.12), origin="60% 50%", shade="shade-left")
slam("slam3", m[0], m[0] + 1.35, "03", "TEMPAT MAKAN")
card("card-m1", m[0] + 1.3, m[2], "03 &#183; TEMPAT MAKAN", "RESTORAN BEMBAN", "Bufet sarapan, makan tengah hari &amp; makan malam")
card("card-m2", m[2], m[4], "03 &#183; TEMPAT MAKAN", "ASAHAN CAFE", "Kafe konsep Nyonya &#183; 10 pagi hingga 12 malam")
for t in (m[1], m[3]):
    sfx("whoosh-short", t - 0.05, 0.22)

# ---- 8. 04 bilik & suite (AI 3D camera moves, assets/video/*.mp4)
rk = ["bilik", "bilik2", "bilik3", "bilik4", "bilik5", "bilik6", "bilik7", "bilik8", "recap"]
rb = [T[k] for k in rk]
ROOMS = ["room-double", "room-twin", "room-deluxe", "room-junior", "room-junior-2", "room-exec", "room-exec-2", "room-exec-bath"]
for i, vid in enumerate(ROOMS):
    vshot(f"s-v{i}", vid, rb[i], rb[i + 1], punch=i > 0, shade="shade-left", media_start=0 if i == 0 else 0.3)
    if i:
        sfx("whoosh-short", rb[i] - 0.05, 0.22)
slam("slam4", rb[0], rb[0] + 1.35, "04", "BILIK &amp; SUITE")
K = "04 &#183; BILIK &amp; SUITE"
card("card-v1", rb[0] + 1.3, rb[1], K, "SUPERIOR DOUBLE", "Katil Queen &#183; 172.76 kaki persegi")
card("card-v2", rb[1], rb[2], K, "SUPERIOR TWIN", "2 Katil Bujang &#183; 172.76 kaki persegi")
card("card-v3", rb[2], rb[3], K, "DELUXE", "1 Katil Queen + 1 Katil Bujang &#183; 185.75 kaki persegi")
card("card-v4", rb[3], rb[5], K, "JUNIOR SUITE", "Katil King &#183; Ruang tamu berasingan &#183; 464.47 kaki persegi")
card("card-v5", rb[5], rb[8], K, "EXECUTIVE SUITE", "Katil King &#183; Ruang makan &amp; lounge &#183; 637.23 kaki persegi")

# ---- 9. recap grid
g0, g1 = T["recap"], T["end"]
TILES = [("pool-2", "Kolam Renang"), ("gadek", "Dewan Gadek"), ("gadek5-2", "Bilik Gadek 5"), ("brisu", "Halaman Brisu"),
         ("bemban", "Restoran Bemban"), ("asahan-2", "Asahan Cafe"), ("room-exec", "188 Bilik Penginapan")]
tiles = []
for i, (img, lab) in enumerate(TILES):
    row, col = (0, i) if i < 4 else (1, i - 4)
    tw_, th_, gap = 380, 262, 22
    left = (W - (4 * tw_ + 3 * gap)) // 2 + col * (tw_ + gap) if row == 0 else (W - (3 * tw_ + 2 * gap)) // 2 + col * (tw_ + gap)
    top = 230 + row * (th_ + gap)
    tiles.append(f'<div class="tile" id="tile{i}" style="left:{left}px;top:{top}px;width:{tw_}px;height:{th_}px">'
                 f'<img src="assets/img/{img}.jpg" alt=""/><div class="tile-l"><span>{i + 1:02d}</span>{lab}</div></div>')
clip("recap", g0, g1, (
    '<div class="hex dark"></div><div class="rc-k" id="rc-k">7 KEMUDAHAN UTAMA</div>'
    '<div class="ttl-mask rc-mask"><div class="rc-t" id="rc-t">SEGALANYA DI SATU DESTINASI</div></div>'
    + "".join(tiles) + '<div class="rc-f" id="rc-f">HOTEL MITC &#183; AYER KEROH &#183; MELAKA</div>'), "bg-navy", 2)
flash(g0, 0.8, 0.4)
tw("#rc-k", {"opacity": 0}, {"opacity": 1, "duration": 0.6}, g0 + 0.05)
tw("#rc-t", {"yPercent": 105}, {"yPercent": 0, "duration": 0.6, "ease": "expo.out"}, g0 + 0.15)
for i in range(len(TILES)):
    st = g0 + 0.35 + i * 0.16
    tw(f"#tile{i}", {"opacity": 0, "scale": 0.6, "rotationX": -70, "y": 40},
       {"opacity": 1, "scale": 1, "rotationX": 0, "y": 0, "duration": 0.6, "ease": "back.out(1.5)"}, st)
    sfx("pop", st, 0.2)
tw("#rc-f", {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0, "duration": 0.5}, g0 + 1.6)
tw("#recap", {"scale": 1}, {"scale": 1.04, "duration": round(g1 - g0, 3), "ease": "none"}, g0)
tw(["#recap .tile", "#rc-t", "#rc-k", "#rc-f"], {"opacity": 1}, {"opacity": 0, "duration": 0.3, "ease": "power2.in"}, g1 - 0.32)
sfx("whoosh", g0 - 0.2, 0.45)

# ---- 10. end card
n0, n1 = T["end"], T["fin"]
clip("endc", n0, n1, (
    '<div class="hex light"></div><div class="end-glow"></div>'
    '<img class="end-logo" id="end-logo" src="assets/img/mitc-logo.png" alt="MITC Hotel"/>'
    '<div class="end-tag" id="end-tag">Tempah terus dengan kami!</div>'
    '<div class="end-row" id="end-row">'
    f'<div class="end-it"><span class="ic">{ICON["phone"]}</span>06-233 1551</div>'
    f'<div class="end-it"><span class="ic">{ICON["web"]}</span>mitchotel.com.my</div></div>'
    f'<div class="end-addr" id="end-addr"><span class="ic">{ICON["pin"]}</span>Jalan Food City, Pusat Dagangan Antarabangsa Melaka, 75450 Ayer Keroh, Melaka</div>'
    '<div class="end-foot" id="end-foot"><div class="end-by">DIURUSKAN OLEH</div>'
    '<img class="end-mh" src="assets/img/mcorp-hotel-logo.png" alt="M\'Corp Hotel Sdn. Bhd."/>'
    '<div class="end-sep"></div><div class="end-by">ANAK SYARIKAT</div>'
    '<img class="end-mc" src="assets/img/mcorp-corporate.png" alt="MCORP"/></div>'), "bg-white", 2)
flash(n0, 1.0, 0.6)
tw("#end-logo", {"scale": 0.6, "opacity": 0, "filter": "blur(12px)"}, {"scale": 1, "opacity": 1, "filter": "blur(0px)", "duration": 0.9, "ease": "expo.out"}, n0 + 0.1)
tw("#end-tag", {"y": 20, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6}, n0 + 0.7)
tw("#end-row", {"y": 30, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6}, n0 + 1.0)
tw("#end-addr", {"opacity": 0}, {"opacity": 1, "duration": 0.6}, n0 + 1.3)
tw("#end-foot", {"y": 30, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.7}, n0 + 1.6)
tw("#end-logo", {"scale": 1}, {"scale": 1.04, "duration": round(n1 - n0 - 1.0, 3), "ease": "sine.inOut"}, n0 + 1.0)
tw("#fadeout", {"opacity": 0}, {"opacity": 1, "duration": 0.6, "ease": "power1.in"}, n1 - 0.6)
sfx("impact-bass-2", n0, 0.55)
sfx("whoosh-cinematic", n0 - 0.4, 0.35)
sfx("chime", n0 + 0.7, 0.35)

# ================================================================ assemble
CSS = open(os.path.join(HF, "..", "style.css")).read()

aud = []
busy = []   # end time per sfx track
for i, (src, start, vol, off, maxlen) in enumerate(sorted(audio, key=lambda a: a[1])):
    d = dur_of(os.path.join(HF, src)) - off
    d = min(d, maxlen or d, TOTAL - start)
    tr = next((k for k, e in enumerate(busy) if e <= start), None)
    if tr is None:
        busy.append(0)
        tr = len(busy) - 1
    busy[tr] = start + d
    media = f' data-media-start="{off}"' if off else ""
    aud.append(f'<audio id="sx{i:02d}" src="{src}" data-start="{at(start)}" data-duration="{at(d)}"{media} '
               f'data-track-index="{30 + tr}" data-volume="{vol}"></audio>')

bgm = ""
if os.path.exists(os.path.join(HF, "assets", "bgm", "bed.wav")):
    auto = {"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0, "v": 0}, {"t": 0.3, "v": 0.85}, {"t": TOTAL - 2.0, "v": 0.85}, {"t": TOTAL, "v": 0}]}]}
    bgm = (f'<audio id="bgm" data-timeline-role="music" src="assets/bgm/bed.wav" data-start="0" '
           f'data-duration="{at(TOTAL)}" data-track-index="10" data-automation=\'{json.dumps(auto)}\'></audio>')

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
      <div id="leak" class="clip fx" data-start="0" data-duration="{at(TOTAL)}" data-track-index="20"></div>
      <div id="vignette" class="clip fx" data-start="0" data-duration="{at(TOTAL)}" data-track-index="21"></div>
      <div id="flash" class="clip fx" data-start="0" data-duration="{at(TOTAL)}" data-track-index="22"></div>
      <div id="fadeout" class="clip fx" data-start="0" data-duration="{at(TOTAL)}" data-track-index="23"></div>
      {bgm}
      {chr(10).join('      ' + a for a in aud).lstrip()}
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
print("total", TOTAL, "s;", len(clips), "clips,", len(aud), "sfx")
print(json.dumps(T))
