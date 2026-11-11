"""Build the SPD GREEN explainer (edits/spd-green/hf): compositions/*.html + index.html.

Timing comes from the voice-over: every scene lists the VO lines it carries; the scene length is the
VO length plus lead-in/tail, and every on-screen beat is placed on a spoken word (S.w(line, word)).
Lines whose audio is not recorded yet get an estimated word timing (marked "est") so the film can be
built and previewed before the VO is complete.

usage: python3 scripts/spd_build.py [scene ids to build only, e.g. s06 s07]   (all when omitted)
"""
import json
import os
import re
import subprocess
import sys

ROOT = "/home/user/AI-IZZUL"
HF = f"{ROOT}/edits/spd-green/hf"
sys.path.insert(0, f"{ROOT}/scripts")
import spd_storyboard as SB  # noqa: E402  (reuses the doodle icons, leaf, SPD mark, SPD 2.0 homepage)

SCRIPT = {l["id"]: l["text"] for l in json.load(open(f"{ROOT}/edits/spd-green/vo-script.json"))}


# ----------------------------------------------------------------------------- VO timing
def _syl(w):
    return max(1, len(re.findall(r"[aeiou]+", w.lower())))


SPEED = 1.1  # VO is planned ~10% faster than the raw Charon read (atempo at mix time) to land the film on 4:00


class Line:
    def __init__(self, lid):
        self.id = lid
        mp3, js = f"{HF}/assets/vo/{lid}.mp3", f"{HF}/assets/vo/{lid}.json"
        if os.path.exists(mp3) and os.path.exists(js):
            self.words = json.load(open(js))
            self.dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3],
                                            capture_output=True, text=True).stdout)
            self.real = True
            self.words = [{**w, "start": round(w["start"] / SPEED, 3), "end": round(w["end"] / SPEED, 3)} for w in self.words]
            self.dur = round(self.dur / SPEED, 3)
        else:  # estimate: ~4.3 syllables/s, pauses at punctuation
            t, ws = 0.05, []
            for w in SCRIPT[lid].split():
                d = _syl(w) / 5.6
                ws.append({"start": round(t, 3), "end": round(t + d, 3), "word": w})
                t += d + (0.3 if w[-1] in ".,?" else 0.03)
            ws = [{**w, "start": round(w["start"] / SPEED, 3), "end": round(w["end"] / SPEED, 3)} for w in ws]
            self.words, self.dur, self.real = ws, round((t + 0.2) / SPEED, 3), False

    def t(self, word, nth=1):
        """start time of the nth word that starts with `word` (case/punctuation-insensitive)"""
        for alt in word.split("|"):  # "Kini|Hari": first form found wins (script versions differ)
            key = re.sub(r"[^a-z0-9]", "", alt.lower())
            n = 0
            for w in self.words:
                if re.sub(r"[^a-z0-9]", "", w["word"].lower()).startswith(key):
                    n += 1
                    if n == nth:
                        return w["start"]
        raise KeyError(f"{self.id}: '{word}' #{nth} not in {SCRIPT[self.id]}")

    def end(self):
        return self.words[-1]["end"]


# ----------------------------------------------------------------------------- scene context
class Scene:
    def __init__(self, sid, lines, pre=0.4, post=0.7, extra=0.0, fixed=None):
        self.id, self.pre, self.post = sid, pre, post
        self.lines = [(Line(l), None) for l in lines]
        t = pre
        placed = []
        for ln, _ in self.lines:
            placed.append((ln, round(t, 3)))
            t += ln.dur + 0.25
        self.lines = placed
        self.D = round(fixed if fixed else (t - 0.25 + post + extra), 3)

    def w(self, lid, word, nth=1):
        for ln, at in self.lines:
            if ln.id == lid:
                return round(at + ln.t(word, nth), 3)
        raise KeyError(lid)

    def at(self, lid):
        for ln, at in self.lines:
            if ln.id == lid:
                return at
        raise KeyError(lid)

    def vend(self, lid):
        for ln, at in self.lines:
            if ln.id == lid:
                return round(at + ln.end(), 3)
        raise KeyError(lid)


# ----------------------------------------------------------------------------- html helpers
CURSOR = ('<svg class="cur" id="{id}" viewBox="0 0 60 80"><path d="M5 5 L5 65 L20 50 L32 75 L42 70 L30 46 L52 46Z" '
          'fill="#fff" stroke="#111" stroke-width="3"/></svg><div class="cring" id="{id}-r"></div>')


def cursor(cid):
    return CURSOR.format(id=cid)


def browser(bid, x, y, w, url, pages, extra="", style=""):
    """pages: list of (img id, src). Images are full-width in the viewport (1920x912 source)."""
    vh = round(w * 912 / 1920)
    imgs = "".join(f'<img class="pg" id="{pid}" src="{src}" style="opacity:{1 if i == 0 else 0}">' for i, (pid, src) in enumerate(pages))
    return (f'<div class="bw" id="{bid}" style="left:{x}px;top:{y}px;width:{w}px;height:{vh + 52}px;{style}">'
            f'<div class="bw-bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i>'
            f'<div class="bw-url">🔒 <span id="{bid}-url">{url}</span></div></div>'
            f'<div class="bw-view" id="{bid}-v">{imgs}{extra}</div></div>')


def region(rid, k, x0, y0, x1, y1, pad=10, cls="hl"):
    """highlight box over a screenshot region (source px) inside a viewport scaled by k"""
    return (f'<div class="{cls}" id="{rid}" style="left:{x0 * k - pad:.0f}px;top:{y0 * k - pad:.0f}px;'
            f'width:{(x1 - x0) * k + 2 * pad:.0f}px;height:{(y1 - y0) * k + 2 * pad:.0f}px"></div>')


def crop(cid, src, x0, y0, x1, y1, w, style=""):
    """div showing a source-px crop of a 1920x912 screenshot at width w"""
    s = w / (x1 - x0)
    return (f'<div id="{cid}" style="position:absolute;width:{w:.0f}px;height:{(y1 - y0) * s:.0f}px;border-radius:14px;'
            f'background:url({src}) -{x0 * s:.0f}px -{y0 * s:.0f}px/{1920 * s:.0f}px {912 * s:.0f}px no-repeat;'
            f'box-shadow:0 30px 70px rgba(0,0,0,.55),0 0 0 3px #b6d973;{style}"></div>')


def odo(to, frm=None, cls="", style=""):
    """Odometer markup: digit columns roll from frm's digit to to's digit (+1 full turn when counting up)."""
    frm = frm if frm is not None else re.sub(r"\d", "0", to)
    assert len(frm) == len(to), (frm, to)
    out = []
    for a, b in zip(frm, to):
        if b.isdigit():
            da, db = int(a) if a.isdigit() else 0, int(b)
            s0, e0 = 10 + da, (20 + db if db >= da else db)  # up: forward a full cycle; down: roll back
            if da == db and a == b and frm != to:
                e0 = s0
            lines = "".join(f"<b>{k % 10}</b>" for k in range(30))
            out.append(f'<span class="odo-c"><span class="odo-s" data-s="{s0}" data-e="{e0}">{lines}</span></span>')
        else:
            out.append(f'<span class="odo-x">{b}</span>')
    return f'<span class="odo {cls}" style="{style}">{"".join(out)}</span>'


def kw(text, cls=""):
    """kinetic words: each word in a mask"""
    return " ".join(f'<span class="kw {cls}"><span>{w}</span></span>' for w in text.split())


def sb(html):
    """storyboard frame html -> hf asset paths"""
    return html.replace("assets/", "assets/sb/")


UI = "assets/ui"
IMG = "assets/img"


# ============================================================================= SCENES
SCENES = {}


def scene(fn):
    SCENES[fn.__name__] = fn
    return fn


# --------------------------------------------------------------------------- S01 cold open
MONTAGE = 8.567
CUTS = [0, 1.5, 2.7, 4.3, 5.755]


@scene
def s01(S):
    v = S.at("v01")
    html = f"""
<div class="F" style="background:#000">
  <div id="s01-vw" class="abs" style="inset:0">
    <video id="s01-vid" class="clip" src="assets/video/s01_montage.mp4" data-start="0" data-duration="{MONTAGE}" data-track-index="0"
      muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"></video>
  </div>
  <img id="s01-fr" src="{IMG}/s01_freeze.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0">
  <div id="s01-flash" class="abs" style="inset:0;background:#fff;opacity:0"></div>
  <div id="s01-dim" class="abs" style="inset:0;background:linear-gradient(90deg,rgba(4,20,14,.85),rgba(4,20,14,.25) 60%,rgba(4,20,14,.6));opacity:0"></div>
  <svg id="s01-chalk" viewBox="0 0 1920 1080" class="abs" style="inset:0;filter:url(#s01-cf)" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round" stroke-linejoin="round">
    <defs><filter id="s01-cf"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="5" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -1.6 1.3" result="m"/>
      <feComposite in="SourceGraphic" in2="m" operator="in" result="c"/><feDisplacementMap in="c" in2="n" scale="4"/></filter></defs>
    <path class="s01-d" d="M470 150 C760 140 880 290 850 420 C820 560 560 640 300 600 C110 570 70 420 120 300 C170 190 330 145 520 160"/>
    <path class="s01-d" d="M1000 175 C930 190 900 210 860 250 M860 250 l12 -50 M860 250 l50 -8"/>
    <circle class="s01-d" cx="1580" cy="900" r="80"/><path class="s01-d" d="M1580 900 v-54 M1580 900 l40 24"/>
  </svg>
  <div id="s01-q" class="doodle abs" style="left:1010px;top:80px;font-size:110px;color:#fff;transform:rotate(-6deg);opacity:0">Fail mana?!</div>
  <div class="abs" style="left:120px;top:620px;width:1000px">
    <div class="h1" style="font-size:96px">{kw("Fail fizikal.", "s01-a")}</div>
    <div class="h1" style="font-size:96px;color:var(--lime)">{kw("Carian manual.", "s01-b")}</div>
    <div style="font:600 40px 'Plus Jakarta Sans';margin-top:22px;color:#e6efe9">{kw("Masa yang terbuang, setiap hari.", "s01-c")}</div>
  </div>
  <div class="vign"></div>
</div>"""
    # immediateRender:false everywhere: otherwise the LAST-authored from-values (white flash .35) sit on the first shot
    punches = "".join(f'tl.fromTo("#s01-vw",{{scale:1.09}},{{scale:1,duration:0.45,ease:"expo.out",immediateRender:false}},{c});'
                      f'tl.fromTo("#s01-flash",{{opacity:0.18}},{{opacity:0,duration:0.25,ease:"power2.out",immediateRender:false}},{c});' for c in CUTS[1:])
    js = f"""
{punches}
tl.fromTo("#s01-vw",{{scale:1}},{{scale:1.06,duration:{MONTAGE - CUTS[-1]},ease:"none",immediateRender:false}},{CUTS[-1] + 0.45});
// freeze: flash, hold, slow push + desaturate, chalk doodles draw
tl.set("#s01-fr",{{opacity:1}},{MONTAGE});
tl.fromTo("#s01-flash",{{opacity:0.35}},{{opacity:0,duration:0.35,immediateRender:false}},{MONTAGE});
tl.fromTo("#s01-fr",{{scale:1.06,filter:"grayscale(0) brightness(1)"}},{{scale:1.16,filter:"grayscale(.7) brightness(.75)",duration:{S.D - MONTAGE},ease:"none"}},{MONTAGE});
tl.to("#s01-dim",{{opacity:1,duration:0.6}},{MONTAGE + 0.15});
FX.draw(tl,".s01-d",{MONTAGE + 0.1},0.5,0.18);
tl.fromTo("#s01-q",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{MONTAGE + 0.3});
FX.words(tl,".s01-a > span",{S.w("v01", "Fail") - 0.05});
FX.words(tl,".s01-b > span",{S.w("v01", "Carian") - 0.05});
FX.words(tl,".s01-c > span",{S.w("v01", "Masa") - 0.05},0.07);
"""
    return html, js


# --------------------------------------------------------------------------- S02 title
@scene
def s02(S):
    import random
    r = random.Random(4)
    sheets = ""
    for i in range(30):
        x, y = r.randint(-200, 1900), r.randint(-100, 1000)
        w = r.randint(110, 280)
        z = r.randint(-1600, 400)
        sheets += (f'<div class="s02-sh" data-z="{z}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{w * 1.41:.0f}px;'
                   f'background:#fff;background-image:repeating-linear-gradient(#fff 0 22px,#dfe8e3 22px 24px);'
                   f'box-shadow:0 20px 40px rgba(0,0,0,.35);transform:translateZ({z}px) rotateY({r.randint(-70, 70)}deg) rotate({r.randint(-60, 60)}deg)"></div>')
    t_mem = S.w("v02", "Memperkenalkan")
    t_spd = S.w("v02", "SPD")
    t_ino = S.w("v02", "Inovasi")
    html = f"""
<div class="F gdark">
  <div id="s02-cam" class="abs" style="inset:0;perspective:1100px;transform-style:preserve-3d">
    <div id="s02-sw" class="abs" style="inset:0;transform-style:preserve-3d">{sheets}</div>
  </div>
  <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 52%,rgba(11,46,34,.92) 0 28%,rgba(11,46,34,0) 62%)"></div>
  <div id="s02-k" class="kicker abs" style="left:0;right:0;top:250px;text-align:center;font-size:26px;letter-spacing:.34em;opacity:0">PERBADANAN MELAKA (MCORP)</div>
  <div id="s02-mark" class="abs" style="left:0;right:0;top:330px;display:flex;justify-content:center">{SB.spd_mark(260)}</div>
  <div class="abs h1" style="left:0;right:0;top:648px;text-align:center;font-size:52px;font-weight:700">{kw("Sistem Pengurusan Data Bersepadu", "s02-t")}</div>
  <div class="abs" style="left:0;right:0;top:728px;text-align:center;font:600 italic 36px 'Plus Jakarta Sans';color:var(--gold)">{kw("Inovasi digital ke arah pengurusan hijau dan lestari", "s02-s")}</div>
  <div id="s02-sweep" class="abs" style="left:-600px;top:300px;width:300px;height:340px;background:linear-gradient(90deg,transparent,rgba(255,240,200,.55),transparent);transform:skewX(-20deg);mix-blend-mode:overlay;opacity:0"></div>
  <div class="vign"></div>
</div>"""
    js = f"""
// camera dolly through the paper swarm
tl.fromTo("#s02-sw",{{z:-900,rotationY:-14}},{{z:700,rotationY:10,duration:{S.D},ease:"power1.inOut"}},0);
tl.fromTo(".s02-sh",{{opacity:0.95}},{{opacity:0,duration:0.8,stagger:0.03}},{t_spd - 1.0});
tl.fromTo("#s02-k",{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:0.9,ease:"expo.out"}},{max(0.2, t_mem - 0.3)});
tl.fromTo("#s02-mark",{{opacity:0,scale:1.6,filter:"blur(20px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.7,ease:"expo.out"}},{t_spd - 0.15});
tl.fromTo("#s02-mark svg",{{rotation:-140,scale:0}},{{rotation:28,scale:1,duration:0.8,ease:"back.out(2)"}},{t_spd + 0.1});
FX.words(tl,".s02-t > span",{t_mem + 0.2},0.07);
FX.words(tl,".s02-s > span",{t_ino - 0.05},0.05);
tl.fromTo("#s02-sweep",{{x:0,opacity:0.9}},{{x:2600,opacity:0.9,duration:1.1,ease:"power2.inOut"}},{t_spd + 0.4});
tl.to("#s02-cam",{{scale:1.3,opacity:0,duration:0.5,ease:"power2.in"}},{S.D - 0.5});
tl.to(["#s02-mark","#s02-k",".s02-t",".s02-s"],{{opacity:0,y:-30,duration:0.4,ease:"power2.in"}},{S.D - 0.45});
"""
    return html, js


# --------------------------------------------------------------------------- S03 apa itu SPD
@scene
def s03(S):
    items = [("Tanah", "tanah"), ("Bangunan", "bangunan"), ("Penyewaan", "penyewaan"), ("Penilaian Aset", "penilaian"), ("Dokumen Hak Milik", "dokumen")]
    tiles = "".join(
        f'<div class="abs s03-t" id="s03-t{i}" style="left:0;top:0;width:340px;height:120px;margin:-60px 0 0 -170px">'
        f'<div class="s03-ti" id="s03-ti{i}" style="width:100%;height:100%;border-radius:22px;display:flex;align-items:center;justify-content:center;'
        f'font:700 34px \'Plus Jakarta Sans\';color:#fff;opacity:0;background:linear-gradient(160deg,rgba(47,138,102,.84) 0%,rgba(27,97,72,.80) 55%,rgba(18,70,52,.82) 100%);'
        f'border:1.5px solid rgba(140,214,170,.75);text-shadow:0 2px 8px rgba(0,0,0,.55);'
        f'box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 24px 60px rgba(0,0,0,.45),0 0 34px rgba(182,217,115,.2)">{lab}</div></div>' for i, (lab, _) in enumerate(items))
    dots = "".join(f'<i class="abs s03-p" style="left:0;top:0;width:10px;height:10px;margin:-5px 0 0 -5px;border-radius:50%;background:#d9ffb0;'
                   f'box-shadow:0 0 14px #b6d973;display:block"></i>' for _ in range(28))
    word_t = [S.w("v03", w) for _, w in items]
    t_sat = S.w("v03", "satu")
    t_buk = S.w("v03", "bukan")
    t_hij = S.w("v03", "hijau")
    html = f"""
<div class="F gdark">
  <div id="s03-st" class="abs" style="inset:0">
    <div class="abs" style="left:960px;top:560px;width:1520px;height:700px;margin:-350px 0 0 -760px;border-radius:50%;
      border:2px solid rgba(182,217,115,.45);box-shadow:0 0 40px rgba(182,217,115,.25),inset 0 0 40px rgba(182,217,115,.15)"></div>
    <div class="abs" style="left:960px;top:560px;width:1860px;height:860px;margin:-430px 0 0 -930px;border-radius:50%;
      border:1px solid rgba(255,255,255,.12)"></div>
    {dots}
    <div id="s03-core" class="abs" style="left:960px;top:470px;width:360px;height:360px;margin:-180px 0 0 -180px;z-index:3">
      <div class="abs" style="inset:-170px;border-radius:50%;background:radial-gradient(closest-side,rgba(182,217,115,.32),rgba(182,217,115,.08) 60%,transparent)"></div>
      <div id="s03-glow" class="abs" style="inset:-300px;border-radius:50%;opacity:0;background:radial-gradient(closest-side,rgba(214,255,170,.62),rgba(182,217,115,.22) 45%,rgba(182,217,115,.06) 72%,transparent)"></div>
      <div id="s03-halo" class="abs" style="inset:-26px;border-radius:50%;background:conic-gradient(from 0deg,transparent 0 55%,rgba(217,255,176,.95) 70%,transparent 85%);
        -webkit-mask-image:radial-gradient(circle,transparent 62%,#000 63%,#000 66%,transparent 67%)"></div>
      <div id="s03-ball" class="abs" style="inset:0;border-radius:50%;background:radial-gradient(circle at 35% 30%,#7fe0b0 0%,#26745a 45%,#0b2e22 100%);
        box-shadow:inset -20px -30px 60px rgba(0,0,0,.45),inset 20px 20px 50px rgba(255,255,255,.18),0 30px 80px rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center">
        {SB.spd_mark(110)}</div>
      <div class="abs" style="left:60px;top:30px;width:140px;height:70px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,255,255,.45),transparent 70%);transform:rotate(-25deg)"></div>
    </div>
    {tiles}
  </div>
  <div id="s03-lab" class="mono abs" style="left:0;right:0;top:700px;text-align:center;font-size:26px;color:#d9f0c0;opacity:0">SATU PLATFORM BERPUSAT</div>
  <div class="abs" style="left:0;right:0;top:880px;display:flex;justify-content:center;gap:40px;font:800 56px 'Plus Jakarta Sans'">
    <span id="s03-b1" style="opacity:0">Lebih cekap.</span><span id="s03-b2" style="opacity:0;color:var(--lime)">Lebih hijau.</span></div>
  <div class="vign"></div>
</div>"""
    js = f"""
const tiles=[...document.querySelectorAll(".s03-t")], dots=[...document.querySelectorAll(".s03-p")];
const st={{a:0.35,r:1}};
const cx=960, cy=560, RX=760, RY=350;   // back of the orbit passes ABOVE the sphere, never behind it
function place(){{
  tiles.forEach((t,i)=>{{
    const th=st.a+i*2*Math.PI/5, d=(Math.sin(th)+1)/2;          // d: 0 back .. 1 front
    const x=cx+RX*st.r*Math.cos(th), y=cy+RY*st.r*Math.sin(th);
    t.style.transform=`translate(${{x.toFixed(1)}}px,${{y.toFixed(1)}}px) scale(${{(0.68+0.42*d).toFixed(3)}})`;
    t.style.zIndex=String(d>0.5?6:1); t.style.filter=`brightness(${{(0.72+0.28*d).toFixed(2)}})`;   // solid tiles: depth by shade + size, never transparency
  }});
  dots.forEach((p,i)=>{{
    const th=-st.a*1.6+i*2*Math.PI/dots.length, d=(Math.sin(th)+1)/2;
    p.style.transform=`translate(${{(cx+RX*Math.cos(th)).toFixed(1)}}px,${{(cy+RY*Math.sin(th)).toFixed(1)}}px) scale(${{(0.4+0.9*d).toFixed(2)}})`;
    p.style.opacity=(0.25+0.75*d).toFixed(2);
  }});
}}
place();
tl.to(st,{{a:0.35+1.6,duration:{S.D},ease:"none",onUpdate:place}},0);
tl.fromTo("#s03-core",{{scale:0.2,opacity:0}},{{scale:1,opacity:1,duration:0.9,ease:"back.out(1.5)"}},0.15);
tl.fromTo("#s03-halo",{{rotation:0}},{{rotation:540,duration:{S.D},ease:"none"}},0);
{"".join(f'tl.fromTo("#s03-ti{i}",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.6,ease:"back.out(1.8)"}},{t - 0.12:.2f});' for i, t in enumerate(word_t))}
tl.to(st,{{r:0.12,duration:0.9,ease:"power3.in",onUpdate:place}},{t_sat - 0.2});
tl.to(".s03-ti",{{opacity:0,scale:0.4,duration:0.42,ease:"power2.in"}},{t_sat + 0.05});
tl.fromTo("#s03-glow",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.7,ease:"expo.out"}},{t_sat + 0.55});
tl.fromTo("#s03-core",{{scale:1}},{{scale:1.18,duration:0.6,ease:"expo.out",immediateRender:false}},{t_sat + 0.6});
tl.fromTo("#s03-lab",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5}},{t_sat + 0.7});
tl.fromTo("#s03-b1",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.5,ease:"expo.out"}},{t_buk - 0.05});
tl.fromTo("#s03-b2",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.5,ease:"expo.out"}},{t_hij - 0.3});
tl.to("#s03-ball",{{background:"radial-gradient(circle at 35% 30%,#e6ffc4 0%,#b6d973 45%,#4f8a2c 100%)",duration:0.6}},{t_hij - 0.3});
tl.to("#s03-st",{{scale:1.5,opacity:0,duration:0.5,ease:"power2.in"}},{S.D - 0.5});
"""
    return html, js


# --------------------------------------------------------------------------- S04 problems (doodle)
@scene
def s04(S):
    names = [("01", "Penggunaan kertas tinggi", "paper", "Penggunaan"), ("02", "Ruang simpanan fizikal besar", "cabinet", "Ruang"),
             ("03", "Pertindihan data", "dup", "Pertindihan"), ("04", "Carian maklumat lambat", "hourglass", "Carian"),
             ("05", "Risiko kehilangan dokumen", "lost", "Risiko"), ("06", "Kos operasi tinggi", "cost", "kos")]
    cells, js_c = "", ""
    for i, (n, t, k, word) in enumerate(names):
        x, y = 150 + (i % 3) * 560, 200 + (i // 3) * 420
        icon = SB.doodle_icon(k).replace('style="width:330px;height:300px;filter:url(#rough)"',
                                         f'class="s04-ic" id="s04-i{i}" style="width:330px;height:300px"')
        cells += (f'<div class="abs s04-cell" id="s04-c{i}" style="left:{x}px;top:{y}px;width:520px;height:400px;text-align:center">'
                  f'<div class="doodle abs" id="s04-n{i}" style="left:10px;top:-10px;font-size:80px;color:#D62839">{n}</div>'
                  f'<div style="margin-top:10px">{icon}</div>'
                  f'<div class="doodle" id="s04-l{i}" style="font-size:46px;color:#22302A;margin-top:-6px">{t}</div></div>')
        tt = S.w("v04", word, 2 if word == "Penggunaan" and False else 1)
        js_c += (f'FX.draw(tl,"#s04-i{i} path, #s04-i{i} rect, #s04-i{i} circle",{tt - 0.1},0.55,0.05);'
                 f'tl.fromTo("#s04-i{i} [fill=\'#B6D973\'], #s04-i{i} text",{{opacity:0}},{{opacity:1,duration:0.3}},{tt + 0.3});'
                 f'tl.fromTo("#s04-n{i}",{{opacity:0,scale:2,rotation:-20}},{{opacity:1,scale:1,rotation:0,duration:0.35,ease:"back.out(2)"}},{tt - 0.15});'
                 f'tl.fromTo("#s04-l{i}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{tt + 0.1});')
    filt = "".join(f'<filter id="s04-r{k}"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="{k * 7 + 3}"/>'
                   f'<feDisplacementMap in="SourceGraphic" scale="7"/></filter>' for k in range(3))
    html = f"""
<div class="F" style="background:radial-gradient(ellipse at 50% 45%,#efe9da,#cfc6b0)">
<div class="F paperbg" id="s04-pg" style="box-shadow:0 30px 80px rgba(0,0,0,.35)">
  <svg width="0" height="0" class="abs"><defs>{filt}</defs></svg>
  <div id="s04-in" class="abs" style="inset:0">
    <div class="doodle abs" id="s04-h" style="left:150px;top:62px;font-size:92px;color:#165A44">Sebelum SPD…</div>
    <svg viewBox="0 0 1920 1080" class="abs" style="inset:0;filter:url(#s04-r0)"><path id="s04-u" d="M150 168 C400 152 600 178 720 160" stroke="#B6D973" stroke-width="16" fill="none" stroke-linecap="round"/></svg>
    <div class="doodle abs" id="s04-six" style="left:1220px;top:70px;font-size:70px;color:#D62839;transform:rotate(-4deg)">6 cabaran</div>
    {cells}
  </div>
</div>
</div>"""
    t0 = S.w("v04", "Sebelum")
    js = f"""
tl.fromTo("#s04-h",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.8,ease:"power2.inOut"}},{t0 - 0.2});
FX.draw(tl,"#s04-u",{t0 + 0.4},0.5);
tl.fromTo("#s04-six",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{S.w("v04", "enam") - 0.05});
{js_c}
FX.boil(tl,".s04-ic",["s04-r0","s04-r1","s04-r2"],0,{S.D});
tl.fromTo("#s04-in",{{scale:1.04}},{{scale:1,duration:{S.D},ease:"none"}},0);
// crumple: page folds into a ball and flies at the camera
tl.to("#s04-pg",{{scale:0.16,rotation:-200,borderRadius:"50%",duration:0.75,ease:"power3.in"}},{S.D - 0.85});
tl.to("#s04-pg",{{scale:3,opacity:0,duration:0.1,ease:"power2.in"}},{S.D - 0.1});
"""
    return html, js


# --------------------------------------------------------------------------- S05 before -> after, into the system
@scene
def s05(S):
    t_hari = S.w("v05", "Kini|Hari")
    t_ber = S.w("v05", "berpusat")
    t_ata = S.w("v05", "Atas")
    t_cek = S.w("v05", "cekap")
    html = f"""
<div class="F" style="background:#f3eedf">
  <div id="s05-split" class="abs" style="inset:0;opacity:0">
    <div id="s05-l" class="abs" style="inset:0;clip-path:polygon(0 0,58% 0,42% 100%,0 100%)">
      <img src="{IMG}/fail-rak.jpg" style="position:absolute;left:-720px;top:0;width:1920px;height:1080px;object-fit:cover;filter:grayscale(1) contrast(1.1) brightness(.85)"></div>
    <div id="s05-r" class="abs" style="inset:0;clip-path:polygon(58% 0,100% 0,100% 100%,42% 100%);background:#0b2e22">
      {browser("s05-b", 1010, 200, 860, "spd.pknm.gov.my", [("s05-p", f"{UI}/s77.jpg")])}</div>
    <div id="s05-seam" class="abs" style="inset:0;background:linear-gradient(115deg,transparent 46%,rgba(182,217,115,.9) 49.6%,#fff 50%,rgba(182,217,115,.9) 50.4%,transparent 54%)"></div>
    <div class="mono abs" id="s05-tb" style="left:80px;top:90px;font-size:28px;color:#fff;background:rgba(0,0,0,.6);padding:10px 18px;border-radius:8px">SEBELUM · FAIL FIZIKAL</div>
    <div class="mono abs" id="s05-ta" style="right:230px;top:90px;font-size:28px;color:#0b2e22;background:var(--lime);padding:10px 18px;border-radius:8px">SELEPAS · SPD</div>
    <div class="abs" style="left:0;right:0;bottom:70px;display:flex;justify-content:center;gap:28px">
      <div class="pill" id="s05-p1">BERPUSAT</div><div class="pill" id="s05-p2">ATAS TALIAN</div><div class="pill" id="s05-p3">LEBIH CEKAP</div></div>
  </div>
  <div id="s05-ball" class="abs" style="left:845px;top:425px;width:230px;height:230px;border-radius:50%;
    background:radial-gradient(circle at 35% 30%,#fff,#e2dccb 55%,#a9a28f);box-shadow:0 30px 60px rgba(0,0,0,.45)"></div>
  <div id="s05-wh" class="abs" style="inset:0;background:#fff;opacity:0"></div>
</div>"""
    js = f"""
tl.fromTo("#s05-ball",{{scale:0.3,rotation:0}},{{scale:9,rotation:160,duration:0.9,ease:"power3.in"}},0);
tl.to("#s05-wh",{{opacity:1,duration:0.2}},0.75);
tl.set("#s05-split",{{opacity:1}},0.95); tl.set("#s05-ball",{{opacity:0}},0.95);
tl.to("#s05-wh",{{opacity:0,duration:0.4}},0.95);
tl.fromTo("#s05-l",{{x:-200}},{{x:0,duration:1.0,ease:"expo.out"}},0.95);
tl.fromTo("#s05-r",{{x:200}},{{x:0,duration:1.0,ease:"expo.out"}},0.95);
tl.fromTo("#s05-b",{{rotationY:-25,transformPerspective:1400,scale:0.9}},{{rotationY:-8,scale:1,duration:1.4,ease:"expo.out"}},1.0);
tl.fromTo(["#s05-tb","#s05-ta"],{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.4,stagger:0.15}},{t_hari});
tl.fromTo("#s05-p1",{{opacity:0,y:60,scale:0.8}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(2)"}},{t_ber - 0.1});
tl.fromTo("#s05-p2",{{opacity:0,y:60,scale:0.8}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(2)"}},{t_ata - 0.1});
tl.fromTo("#s05-p3",{{opacity:0,y:60,scale:0.8}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(2)"}},{t_cek - 0.3});
// push into the SPD screen -> next scene
tl.to("#s05-l",{{x:-1100,duration:0.6,ease:"power3.in"}},{S.D - 0.6});
tl.to(["#s05-seam","#s05-tb","#s05-ta","#s05-i .pill"],{{opacity:0,duration:0.3}},{S.D - 0.6});
tl.to("#s05-r",{{clipPath:"polygon(0% 0,100% 0,100% 100%,0% 100%)",duration:0.6,ease:"power3.in"}},{S.D - 0.6});
tl.to("#s05-b",{{x:-800,y:-90,scale:{1500/860:.4f},transformOrigin:"0 0",rotationY:0,duration:0.6,ease:"power3.inOut"}},{S.D - 0.6});
"""
    return html, js


# --------------------------------------------------------------------------- S06 demo: Laman Utama
BWX, BWY, BWW = 80, 106, 1760
K = BWW / 1920  # screenshot px -> viewport px


@scene
def s06(S):
    t_tab = S.w("v06", "taburan")
    t_rin = S.w("v06", "ringkasan")
    t_aa = S.w("v06", "aset", 1)
    t_ata = S.w("v06", "aset", 2)
    t_sew = S.w("v06", "sewaan")
    t_sto = S.w("v06", "stor")
    t_sat = S.w("v06", "satu")
    extra = (region("s06-hmap", K, 44, 260, 1856, 766) + region("s06-haa", K, 30, 160, 1240, 450) +
             region("s06-hata", K, 1280, 150, 1880, 860) + region("s06-hsew", K, 30, 168, 1260, 688) +
             cursor("s06-c"))
    pages = [("s06-p77", f"{UI}/s77.jpg"), ("s06-p78", f"{UI}/s78.jpg"), ("s06-p80", f"{UI}/s80.jpg")]
    html = f"""
<div class="F demo-bg">
  <div id="s06-cam" class="abs" style="inset:0;perspective:2200px">
    {browser("s06-b", BWX, BWY, BWW, "spd.pknm.gov.my", pages, extra)}
  </div>
  {crop("s06-stor", f"{UI}/s79.jpg", 1290, 408, 1870, 888, 520, "left:1330px;top:330px;opacity:0")}
  <div class="callout" id="s06-k1" style="left:90px;top:860px;opacity:0"><div class="k">LAMAN UTAMA</div><div class="t">Taburan premis & tanah milik MCORP</div></div>
  <div class="callout" id="s06-k2" style="left:90px;top:860px;opacity:0"><div class="k">RINGKASAN</div><div class="t">Aset alih · Aset tak alih · Sewaan · Stor</div></div>
  {crop("s06-cm", f"{UI}/s77.jpg", 44, 260, 1856, 766, 560, "left:80px;top:90px;opacity:0")}
  {crop("s06-ca", f"{UI}/s78.jpg", 30, 160, 1240, 450, 520, "left:90px;top:640px;opacity:0")}
  {crop("s06-cs", f"{UI}/s80.jpg", 30, 168, 1260, 688, 470, "left:1360px;top:640px;opacity:0")}
  <div class="callout" id="s06-k3" style="left:660px;top:900px;opacity:0"><div class="k">SATU PAPARAN</div><div class="t">Semua aset dalam satu sistem</div></div>
  <div class="vign"></div>
</div>"""
    js = f"""
const B="#s06-b";
tl.fromTo(B,{{rotationX:1.5,rotationY:-1.5,scale:1}},{{rotationX:0,rotationY:1,duration:{t_sat - 0.45},ease:"sine.inOut"}},0);
FX.cursor(tl,document.getElementById("s06-c"),[[0,1400,700],[{t_tab - 0.4},760,420],[{t_rin},700,520],[{t_aa},500,250],[{t_ata},1240,300],[{t_sew},600,320],[{t_sto},1150,560]],[],null);
// zoom into the map
tl.to(B,{{scale:1.18,transformOrigin:"50% 52%",duration:0.8,ease:"power3.inOut"}},{t_tab - 0.35});
FX.ring(tl,"#s06-hmap",{t_tab + 0.2},{t_rin - t_tab - 0.6:.2f});
tl.fromTo("#s06-k1",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.45,ease:"expo.out"}},{t_tab});
tl.to("#s06-k1",{{opacity:0,duration:0.25}},{t_rin - 0.3});
tl.to(B,{{scale:1,duration:0.7,ease:"power3.inOut"}},{t_rin - 0.6});
// scroll 77 -> 78
tl.to("#s06-p77",{{y:-500,opacity:0,filter:"blur(6px)",duration:0.55,ease:"power3.in"}},{t_rin - 0.2});
tl.fromTo("#s06-p78",{{y:500,opacity:0,filter:"blur(6px)"}},{{y:0,opacity:1,filter:"blur(0px)",duration:0.6,ease:"power3.out"}},{t_rin + 0.2});
tl.fromTo("#s06-k2",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.45,ease:"expo.out"}},{t_rin + 0.1});
FX.ring(tl,"#s06-haa",{t_aa - 0.05},{t_ata - t_aa:.2f});
FX.ring(tl,"#s06-hata",{t_ata - 0.05},{t_sew - t_ata - 0.3:.2f});
// scroll 78 -> 80 (sewaan)
tl.to("#s06-p78",{{y:-500,opacity:0,filter:"blur(6px)",duration:0.5,ease:"power3.in"}},{t_sew - 0.5});
tl.fromTo("#s06-p80",{{y:500,opacity:0,filter:"blur(6px)"}},{{y:0,opacity:1,filter:"blur(0px)",duration:0.55,ease:"power3.out"}},{t_sew - 0.1});
FX.ring(tl,"#s06-hsew",{t_sew + 0.3},{t_sat - t_sew - 0.6:.2f});
// stor card pops out of the page
tl.fromTo("#s06-stor",{{opacity:0,scale:0.4,rotationY:-40,transformPerspective:1200}},{{opacity:1,scale:1,rotationY:-12,duration:0.6,ease:"back.out(1.6)"}},{t_sto - 0.1});
// "dalam satu paparan": pull back, tilt, title
tl.to("#s06-k2",{{opacity:0,duration:0.25}},{t_sat - 0.5});
tl.to(B,{{scale:0.72,rotationY:-16,rotationX:8,duration:0.9,ease:"power3.inOut"}},{t_sat - 0.4});
tl.to("#s06-stor",{{x:-40,y:-200,scale:0.82,duration:0.9,ease:"power3.inOut"}},{t_sat - 0.4});
tl.fromTo(["#s06-cm","#s06-ca","#s06-cs"],{{opacity:0,scale:0.4,x:(i)=>[620,600,-560][i],y:(i)=>[260,-260,-260][i],rotationY:(i)=>[30,30,-30][i],transformPerspective:1400}},
  {{opacity:1,scale:1,x:0,y:0,rotationY:(i)=>[14,14,-14][i],duration:0.8,stagger:0.08,ease:"expo.out"}},{t_sat - 0.1});
tl.fromTo("#s06-k3",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.5,ease:"expo.out"}},{t_sat + 0.2});
tl.to(["#s06-cm","#s06-ca","#s06-cs","#s06-stor","#s06-k3"],{{opacity:0,scale:0.9,duration:0.3}},{S.D - 0.35});
tl.to(B,{{scale:1,rotationY:0,rotationX:0,duration:0.5,ease:"power3.inOut"}},{S.D - 0.5});
"""
    return html, js


# --------------------------------------------------------------------------- S07 demo: Aset Tak Alih
@scene
def s07(S):
    t_taip = S.w("v07", "menaip|taip")
    t_rek = S.w("v07", "Rekod")
    t_lot = S.w("v07", "lot")
    t_sta = S.w("v07", "status")
    t_koo = S.w("v07", "koordinat")
    t_pet = S.w("v07", "peta")
    t_dok = S.w("v07", "dokumen")
    # unhurried search: type on "pengguna", list opens ~"menaip", cursor glides to ELKAY and rests, clicks on "Rekod",
    # page loads, slow zoom-out, cursor waits before moving on
    t_pen = S.w("v07", "pengguna")
    t_type = t_pen + 0.3
    t_drop = t_type + 0.85
    t_hov = t_drop + 1.1
    t_pick = max(t_hov + 0.3, t_rek - 0.05)
    sx, sy = 1300, 62   # search box (source px)
    ix, iy = 760, 422   # dropdown item "PLOT 10"
    gx, gy = 1720, 572  # Google pin button on s86
    extra = (f'<div id="s07-sbox" class="abs" style="left:{1140 * K:.0f}px;top:{40 * K:.0f}px;width:{320 * K:.0f}px;height:{44 * K:.0f}px;background:#fff;'
             f'border:2px solid #b6d973;border-radius:22px;padding:4px 14px;font:600 20px \'Plus Jakarta Sans\';color:#111;display:flex;align-items:center;opacity:0">'
             f'<span id="s07-txt"></span><i id="s07-car" style="width:2px;height:22px;background:#8e1b33;display:block;margin-left:2px"></i></div>' +
             region("s07-hitem", K, 500, 404, 1120, 440, 6) +
             region("s07-hprem", K, 860, 320, 1345, 430) + region("s07-hlot", K, 1380, 330, 1870, 420) +
             region("s07-hsta", K, 860, 545, 1345, 615) + region("s07-hkoo", K, 1380, 440, 1870, 530) +
             region("s07-hpin", K, 1690, 545, 1790, 600, 6) +
             region("s07-hd1", K, 250, 426, 520, 776) + region("s07-hd2", K, 1060, 426, 1330, 776) +
             cursor("s07-c"))
    pages = [("s07-p83", f"{UI}/s83.jpg"), ("s07-p84", f"{UI}/s84.jpg"), ("s07-p86", f"{UI}/s86.jpg"), ("s07-p89", f"{UI}/s89.jpg")]
    gmap = browser("s07-g", 0, 0, 900, "google.com/maps", [("s07-pg", f"{UI}/s87.jpg")],
                   '<div id="s07-pin" class="abs" style="left:430px;top:190px;width:80px;height:80px;border-radius:50%;border:5px solid #ea4335;opacity:0"></div>')
    html = f"""
<div class="F demo-bg">
  <div id="s07-cam" class="abs" style="inset:0;perspective:2200px">
    <div id="s07-in" class="abs" style="inset:0;transform-style:preserve-3d">{browser("s07-b", BWX, BWY, BWW, "spd.pknm.gov.my/asettakalih", pages, extra)}</div>
  </div>
  <div id="s07-gw" class="abs" style="left:880px;top:300px;width:900px;height:{round(900 * 912 / 1920) + 52}px;opacity:0">{gmap}</div>
  <div class="callout" id="s07-k1" style="left:90px;top:860px;opacity:0"><div class="k">ASET TAK ALIH · CARIAN</div><div class="t">Taip nama lokasi</div></div>
  <div class="callout" id="s07-k2" style="left:90px;top:860px;opacity:0"><div class="k">MAKLUMAT PREMIS</div><div class="t">Premis · Lot · Hak milik · Koordinat</div></div>
  <div class="callout" id="s07-k3" style="left:90px;top:860px;opacity:0"><div class="k">HAK MILIK DIGITAL</div><div class="t">Dokumen terus dalam sistem</div></div>
  <div class="vign"></div>
</div>"""
    js = f"""
const B="#s07-b", K={K};
tl.fromTo("#s07-in",{{opacity:0,x:700,rotationY:-30,filter:"blur(14px)"}},{{opacity:1,x:0,rotationY:0,filter:"blur(0px)",duration:0.55,ease:"expo.out"}},0);
tl.fromTo(B,{{rotationY:1.5,rotationX:1,x:20}},{{rotationY:-1,rotationX:0,x:0,duration:{S.D - 0.45},ease:"sine.inOut"}},0);
FX.cursor(tl,document.getElementById("s07-c"),[[0,{900 * K},{600 * K}],[{t_pen - 0.15},{sx * K},{sy * K}],[{t_drop + 0.35},{sx * K},{sy * K}],
  [{t_hov},{ix * K},{iy * K}],[{t_pick + 0.7},{ix * K},{iy * K}],[{t_pick + 1.6},{1100 * K},{380 * K}],[{t_pet - 0.5},{gx * K},{gy * K}],[{t_dok - 0.6},{700 * K},{600 * K}]],
  [[{t_pen},{sx * K},{sy * K}],[{t_pick},{ix * K},{iy * K}],[{t_pet - 0.35},{gx * K},{gy * K}]],document.getElementById("s07-c-r"));
tl.fromTo("#s07-k1",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.45,ease:"expo.out"}},{t_pen - 0.3});
tl.to("#s07-k1",{{opacity:0,duration:0.3}},{t_pick + 0.15});
// zoom to the search box, type ELKAY
tl.to(B,{{scale:1.22,transformOrigin:"78% 8%",duration:0.7,ease:"power2.inOut"}},{t_pen - 0.55});
tl.set("#s07-sbox",{{opacity:1}},{t_pen + 0.05});
FX.type(tl,document.getElementById("s07-txt"),"ELKAY",{t_type},0.6,document.getElementById("s07-car"));
// dropdown (s84) wipes down
tl.set("#s07-sbox",{{opacity:0}},{t_drop});
tl.fromTo("#s07-p84",{{opacity:1,clipPath:"inset(0 0 100% 0)"}},{{opacity:1,clipPath:"inset(0 0 0% 0)",duration:0.6,ease:"power2.out"}},{t_drop});
// ease the camera out a little while the list opens, so the list and the cursor stay in view
tl.to(B,{{scale:1.12,duration:0.9,ease:"power2.inOut"}},{t_drop + 0.1});
FX.ring(tl,"#s07-hitem",{t_hov - 0.1},{t_pick - t_hov + 0.2:.2f});
// click -> premis page, then a slow zoom-out
tl.fromTo("#s07-p86",{{opacity:0,scale:1.03,filter:"blur(6px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.6,ease:"power2.out"}},{t_pick + 0.15});
tl.to(B,{{scale:1,duration:1.0,ease:"power2.inOut"}},{t_pick + 0.25});
tl.fromTo("#s07-k2",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.45,ease:"expo.out"}},{t_pick + 0.5});
FX.ring(tl,"#s07-hprem",{t_pick + 0.8},{t_pet - t_pick - 1.2:.2f});
FX.ring(tl,"#s07-hlot",{t_lot},{t_pet - t_lot - 0.4:.2f});
FX.ring(tl,"#s07-hsta",{t_sta},{t_pet - t_sta - 0.4:.2f});
FX.ring(tl,"#s07-hkoo",{t_koo},{t_pet - t_koo - 0.4:.2f});
tl.to("#s07-k2",{{opacity:0,duration:0.25}},{t_pet - 0.4});
FX.ring(tl,"#s07-hpin",{t_pet - 0.6},0.6);
// Google map window pops out of the pin button
tl.fromTo("#s07-gw",{{opacity:0,scale:0.1,x:500,y:120,rotationY:-30,transformPerspective:1600}},{{opacity:1,scale:1,x:0,y:0,rotationY:-10,duration:0.6,ease:"back.out(1.4)"}},{t_pet - 0.2});
tl.fromTo("#s07-pin",{{opacity:1,scale:0.3}},{{opacity:0,scale:2.2,duration:0.8,repeat:2,ease:"power2.out"}},{t_pet + 0.3});
tl.to("#s07-gw",{{opacity:0,scale:0.1,x:500,y:120,rotationY:-30,duration:0.45,ease:"power3.in"}},{max(t_pet + 0.7, t_dok - 0.7)});
// documents (s89)
tl.fromTo("#s07-p89",{{opacity:0,y:400,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.55,ease:"power3.out"}},{t_dok - 0.5});
tl.to(B,{{scale:1.12,transformOrigin:"35% 70%",duration:0.8,ease:"power3.inOut"}},{t_dok - 0.2});
tl.fromTo("#s07-k3",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.45,ease:"expo.out"}},{t_dok});
FX.ring(tl,"#s07-hd1",{t_dok + 0.1},0);
FX.ring(tl,"#s07-hd2",{t_dok + 0.3},0);
tl.to(["#s07-k3","#s07-hd1","#s07-hd2"],{{opacity:0,duration:0.3}},{S.D - 0.4});
tl.to(B,{{scale:0.9,opacity:0,rotationY:-30,x:-500,filter:"blur(10px)",duration:0.4,ease:"power3.in"}},{S.D - 0.4});
"""
    return html, js


# --------------------------------------------------------------------------- S08 demo: other modules (3D carousel)
@scene
def s08(S):
    t_aa = S.w("v08", "aset")
    t_bar = S.w("v08", "barcode")
    t_sto = S.w("v08", "Pengurusan")
    t_baki = S.w("v08", "baki")
    t_mi = S.w("v08", "Modal")
    t_lat = S.w("v08", "kakitangan|latihan")
    t_pen = S.w("v08", "pentadbiran")
    t_cap = S.w("v08", "capaian")
    W = BWW
    k8 = W / 1920
    vh = round(W * 912 / 1920)
    pent = region("s08-hsys", k8, 20, 505, 300, 555, 6) + region("s08-hacc", k8, 1500, 8, 1905, 62, 6) + cursor("s08-cur")
    laser = ('<div id="s08-laser" class="abs" style="left:0;right:0;top:0;height:8px;background:#44ff88;'
             'box-shadow:0 0 30px 10px rgba(68,255,136,.6),0 0 80px 30px rgba(68,255,136,.25);opacity:0"></div>')
    panels = [("s08-a", "spd.pknm.gov.my/asetalih", [("s08-a1", f"{UI}/s90.jpg"), ("s08-a2", f"{UI}/s92.jpg")], laser),
              ("s08-b", "spd.pknm.gov.my/stor", [("s08-b1", f"{UI}/s93.jpg"), ("s08-b2", f"{UI}/s94.jpg")], ""),
              ("s08-c", "spd.pknm.gov.my/modalinsan", [("s08-c1", f"{UI}/s98.jpg"), ("s08-c2", f"{UI}/s95.jpg")], ""),
              ("s08-d", "spd.pknm.gov.my/sistem", [("s08-d1", f"{UI}/s83.jpg")], pent)]
    ph = "".join(f'<div class="abs s08-pn" id="{pid}-w" style="left:0;top:0;width:1920px;height:1080px;opacity:{1 if i == 0 else 0}">'
                 f'{browser(pid, BWX, BWY, W, url, pages, extra)}</div>' for i, (pid, url, pages, extra) in enumerate(panels))
    labels = [("01", "ASET ALIH", "Rekod & pemeriksaan barcode"), ("02", "PENGURUSAN STOR", "Permohonan serta baki stok"),
              ("03", "MODAL INSAN", "Cuti dan rekod berkaitan"), ("04", "PENTADBIRAN", "Pengurusan capaian sistem")]
    lab = "".join(f'<div class="callout s08-lb" id="s08-l{i}" style="left:70px;top:900px;opacity:0"><div class="k">{n} · {a}</div><div class="t">{b}</div></div>'
                  for i, (n, a, b) in enumerate(labels))
    html = f"""
<div class="F demo-bg">
  {ph}
  {lab}
  <div id="s08-eco" class="abs h1" style="left:0;right:0;top:960px;text-align:center;font-size:58px;opacity:0">Lima modul. <span style="color:var(--lime)">Satu ekosistem.</span></div>
  <div class="vign"></div>
</div>"""
    turns = [(t_sto - 0.35, "#s08-a-w", "#s08-b-w"), (t_mi - 0.35, "#s08-b-w", "#s08-c-w"), (t_pen - 0.35, "#s08-c-w", "#s08-d-w")]
    js_turn = "".join(f'FX.whipOut(tl,"{o}",{t:.2f},-1);FX.whipIn(tl,"{n}",{t + 0.18:.2f},1);' for t, o, n in turns)
    cx, cy = BWX + W / 2, BWY + (vh + 52) / 2
    grid = [(500, 300), (1420, 300), (500, 690), (1420, 690)]
    tg = S.D - 1.9
    js_grid = "".join(f'tl.to("{pid}-w",{{opacity:1,x:{gx - cx:.0f},y:{gy - cy:.0f},scale:0.44,skewX:0,filter:"blur(0px)",duration:0.9,ease:"expo.inOut"}},{tg + i * 0.06:.2f});'
                      for i, ((pid, *_), (gx, gy)) in enumerate(zip([("#s08-a",), ("#s08-b",), ("#s08-c",), ("#s08-d",)], grid)))
    js = f"""
tl.fromTo("#s08-a-w",{{opacity:0,x:500,filter:"blur(12px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:0.6,ease:"expo.out"}},0.05);
{js_turn}
tl.fromTo("#s08-l0",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.4,ease:"expo.out"}},{t_aa});
tl.to("#s08-l0",{{opacity:0,duration:0.2}},{t_sto - 0.35});
tl.fromTo("#s08-l1",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.4,ease:"expo.out"}},{t_sto + 0.2});
tl.to("#s08-l1",{{opacity:0,duration:0.2}},{t_mi - 0.35});
tl.fromTo("#s08-l2",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.4,ease:"expo.out"}},{t_mi + 0.2});
tl.to("#s08-l2",{{opacity:0,duration:0.2}},{t_pen - 0.35});
tl.fromTo("#s08-l3",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.4,ease:"expo.out"}},{t_pen + 0.2});
FX.scroll(tl,"#s08-a1",0,-300,{t_aa + 0.6},0.7);
tl.to("#s08-a1",{{opacity:0,duration:0.2}},{t_aa + 1.1});
tl.fromTo("#s08-a2",{{opacity:0,y:200}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{t_aa + 1.0});
tl.fromTo("#s08-laser",{{opacity:1,y:0}},{{opacity:1,y:{vh},duration:0.9,ease:"power1.inOut",yoyo:true,repeat:1}},{t_bar - 0.3});
tl.to("#s08-laser",{{opacity:0,duration:0.2}},{min(t_bar + 1.6, t_sto - 0.4)});
FX.scroll(tl,"#s08-b1",0,-280,{t_baki - 0.4},0.6);
tl.to("#s08-b1",{{opacity:0,duration:0.2}},{t_baki});
tl.fromTo("#s08-b2",{{opacity:0,y:200}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{t_baki - 0.1});
tl.fromTo("#s08-c2",{{opacity:0,x:300}},{{opacity:1,x:0,duration:0.5,ease:"power3.out"}},{t_lat - 0.2});
FX.cursor(tl,document.getElementById("s08-cur"),[[0,{700 * k8},{500 * k8}],[{t_pen + 0.2},{160 * k8},{530 * k8}],[{t_cap - 0.1},{1700 * k8},{36 * k8}]],
  [[{t_pen + 0.35},{160 * k8},{530 * k8}]],document.getElementById("s08-cur-r"));
FX.ring(tl,"#s08-hsys",{t_pen + 0.3},{max(0.4, t_cap - t_pen - 0.5):.2f});
FX.ring(tl,"#s08-hacc",{t_cap - 0.1},1.2);
tl.to("#s08-l3",{{opacity:0,duration:0.25}},{tg - 0.1});
{js_grid}
tl.fromTo("#s08-eco",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.5,ease:"expo.out"}},{tg + 0.5});
"""
    return html, js


# --------------------------------------------------------------------------- S09 lima komponen hijau
@scene
def s09(S):
    # slide 5: "Lima modul dalam satu ekosistem SPD" (wording from the slide)
    mods = [("Aset Alih", "Rekod & pemeriksaan barcode", f"{UI}/s90.jpg", "Kurang dokumen fizikal", ("dokumen", 1)),
            ("Aset Tak Alih", "Carian, cukai, hak milik, laporan", f"{UI}/s86.jpg", "Kurang fail hak milik fizikal", ("fail", 1)),
            ("Modal Insan", "Cuti dan rekod berkaitan", f"{UI}/s98.jpg", "Kurang cetakan borang", ("cetakan", 1)),
            ("Pengurusan Stor", "Permohonan serta baki stok", f"{UI}/s93.jpg", "Permohonan tanpa kertas", ("fail", 1)),
            ("Pentadbiran", "Pengurusan capaian sistem", f"{UI}/s77.jpg", "Kurang ruang arkib", ("arkib", 1))]
    cards, js_c = "", ""
    for i, (a, b, img, c, (word, nth)) in enumerate(mods):
        x = 90 + i * 352
        cards += (f'<div class="abs s09-cd" id="s09-c{i}" style="left:{x}px;top:270px;width:330px;height:620px;background:#fff;border-radius:24px;overflow:hidden;'
                  f'box-shadow:0 20px 50px rgba(11,46,34,.18);color:#0b2e22">'
                  f'<div style="height:170px;background:url({img}) left top/{330 * 1.9:.0f}px auto no-repeat;border-bottom:6px solid #165A44"></div>'
                  f'<div style="padding:22px 24px">'
                  f'<div class="mono" style="font-size:22px;color:#26745A;letter-spacing:.1em">0{i + 1}</div>'
                  f'<div style="font:800 34px/1.1 Plus Jakarta Sans;margin-top:8px;height:76px;display:flex;align-items:flex-end">{a}</div>'
                  f'<div style="font:500 25px/1.35 Plus Jakarta Sans;color:#4c5a53;margin-top:12px">{b}</div></div>'
                  f'<div id="s09-g{i}" class="abs" style="left:18px;right:18px;bottom:22px;height:92px;display:flex;align-items:center;background:#E9F2E7;border-radius:16px;padding:0 14px 0 70px;'
                  f'font:700 22px/1.3 Plus Jakarta Sans;color:#165A44">{SB.leaf("position:absolute;left:14px;top:50%;transform:translateY(-50%) rotate(20deg);width:44px;height:44px", "#7DB544")}{c}</div></div>')
        t = S.w("v09", word, nth) + (0.25 if i == 3 else 0)
        js_c += f'tl.fromTo("#s09-g{i}",{{opacity:0,scale:0.6,y:30}},{{opacity:1,scale:1,y:0,duration:0.45,ease:"back.out(2)"}},{t - 0.1});'
    t0 = S.w("v09", "Setiap")
    html = f"""
<div class="F" style="background:linear-gradient(#F5F2EA,#E9F2E7)">
  <div class="kicker abs" id="s09-k" style="left:90px;top:84px;color:#26745A">IDEA · EKOSISTEM SPD</div>
  <div class="abs h1" style="left:90px;top:124px;font-size:76px;color:#0B2E22">{kw("Lima modul dalam satu ekosistem SPD", "s09-h")}</div>
  <svg viewBox="0 0 1920 1080" class="abs" style="inset:0"><path id="s09-v" d="M60 990 C400 930 600 1040 960 980 S1600 930 1880 990" stroke="#7DB544" stroke-width="8" fill="none"/></svg>
  {cards}
</div>"""
    js = f"""
tl.fromTo("#s09-k",{{opacity:0}},{{opacity:1,duration:0.4}},0.1);
FX.words(tl,".s09-h > span",0.15,0.06);
tl.fromTo(".s09-cd",{{opacity:0,y:200,rotationX:-40,transformPerspective:1200}},{{opacity:1,y:0,rotationX:0,duration:0.7,stagger:0.12,ease:"expo.out"}},{max(0.3, t0 - 0.6)});
FX.draw(tl,"#s09-v",{t0},{S.D - t0 - 0.6:.2f});
{js_c}
tl.to(".s09-cd",{{y:-60,opacity:0,stagger:0.05,duration:0.35,ease:"power2.in"}},{S.D - 0.5});
"""
    return html, js


# --------------------------------------------------------------------------- S10 chapter IMPAK SPD
@scene
def s10(S):
    t_imp = S.w("v10", "impak")
    layers = "".join(f'<div class="abs s10-ly" style="left:0;right:0;top:{380 + i * 3}px;text-align:center;font:800 290px/1 \'Plus Jakarta Sans\';'
                     f'letter-spacing:-.04em;color:{"#06261c" if i < 14 else "#fff"};transform:translateX({i * 2}px)">IMPAK SPD</div>' for i in range(15))
    import random
    r = random.Random(12)
    parts = "".join(f'<i class="abs s10-p" style="left:{r.randint(0, 1900)}px;top:{r.randint(200, 1080)}px;width:{w}px;height:{w}px;border-radius:50%;'
                    f'background:rgba(217,255,176,{r.uniform(.25, .7):.2f});box-shadow:0 0 12px rgba(182,217,115,.8);display:block" data-dy="{r.randint(250, 600)}"></i>'
                    for w in [r.randint(4, 12) for _ in range(40)])
    rings = "".join(f'<div class="abs s10-rg" style="left:960px;top:540px;width:{d}px;height:{d}px;margin:-{d // 2}px 0 0 -{d // 2}px;border-radius:50%;'
                    f'border:2px solid rgba(182,217,115,{.32 - i * .05:.2f})"></div>' for i, d in enumerate([520, 820, 1160, 1560, 2000]))
    html = f"""
<div class="F gdark">
  <div id="s10-glow" class="abs" style="left:960px;top:540px;width:1400px;height:1400px;margin:-700px 0 0 -700px;border-radius:50%;
    background:radial-gradient(circle,rgba(63,208,142,.45),rgba(63,208,142,.08) 45%,transparent 65%)"></div>
  {rings}{parts}
  <div id="s10-sw" class="abs" style="left:-700px;top:-100px;width:420px;height:1300px;background:linear-gradient(90deg,transparent,rgba(220,255,235,.35),transparent);transform:skewX(-20deg)"></div>
  <div id="s10-t" class="abs" style="inset:0;transform:perspective(1200px) rotateX(10deg)">{layers}</div>
  <div class="mono abs" id="s10-b" style="left:0;right:0;top:740px;text-align:center;font-size:30px;letter-spacing:.5em;color:var(--lime)">BAB 03 · HASIL</div>
  <div class="vign"></div>
</div>"""
    js = f"""
tl.fromTo("#s10-glow",{{scale:0.7,opacity:0.6}},{{scale:1.25,opacity:1,duration:{S.D},ease:"sine.inOut"}},0);
tl.fromTo(".s10-rg",{{scale:0.6,opacity:0}},{{scale:1.35,opacity:1,duration:{S.D},ease:"power1.out",stagger:0.12}},0);
tl.fromTo(".s10-p",{{y:0,opacity:0}},{{y:(i,e)=>-(+e.dataset.dy),opacity:1,duration:{S.D},ease:"none"}},0);
tl.fromTo("#s10-sw",{{x:0}},{{x:3000,duration:1.4,ease:"power2.inOut"}},{max(0.1, t_imp - 0.3)});
tl.fromTo("#s10-t",{{scale:2.4,opacity:0,filter:"blur(16px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:0.45,ease:"expo.out"}},{max(0.05, t_imp - 0.2)});
tl.fromTo("#s10-t",{{scale:1}},{{scale:1.08,duration:{S.D - t_imp},ease:"none",immediateRender:false}},{t_imp + 0.25});
tl.fromTo("#s10-b",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.6}},{t_imp + 0.35});
"""
    return html, js


# --------------------------------------------------------------------------- S11 kecekapan sumber
@scene
def s11(S):
    t_car = S.w("v11", "Carian")
    t_kep = S.w("v11", "Keperluan")
    t_18 = S.w("v11", "lapan")
    t_9 = S.w("v11", "sembilan")
    people = "".join(f'<div class="s11-p" id="s11-p{j}" style="display:inline-block">{SB.person("#d9ae52" if j < 9 else "#d9ae52")}</div>' for j in range(18))
    cols = [("MASA", "Carian & semakan rekod lebih pantas", 520, 200), ("TENAGA KERJA", "Anggaran keperluan kakitangan", 700, 740),
            ("RUANG & BAHAN", "Dimanfaatkan semula", 450, 1280)]
    html_c = ""
    for i, (a, b, h, x) in enumerate(cols):
        inner = ""
        if i == 0:
            inner = ('<svg viewBox="0 0 200 200" style="width:190px;height:190px;margin-top:26px"><circle cx="100" cy="110" r="78" stroke="#b6d973" stroke-width="12" fill="none"/>'
                     '<rect x="88" y="14" width="24" height="18" rx="4" fill="#b6d973"/><line id="s11-hand" x1="100" y1="110" x2="100" y2="52" stroke="#fff" stroke-width="10" stroke-linecap="round" style="transform-origin:100px 110px"/></svg>')
        if i == 1:
            inner = (f'<div id="s11-cnt" class="h1" style="font-size:150px;color:#fff;margin-top:10px">18</div>'
                     f'<div style="width:380px;margin-top:6px;line-height:0">{people}</div>')
        html_c += (f'<div class="abs s11-col" id="s11-c{i}" style="left:{x}px;bottom:0;width:440px;height:{h}px;background:linear-gradient(#26745A,#165A44);'
                   f'border-radius:26px 26px 0 0;padding:40px 30px;box-shadow:0 -10px 60px rgba(0,0,0,.35)">'
                   f'<div style="font:800 46px Plus Jakarta Sans;color:#fff">{a}</div><div style="font:500 28px/1.35 Plus Jakarta Sans;color:#d8ecdf;margin-top:12px">{b}</div>{inner}</div>')
    html = f"""
<div class="F gdark">
  <div class="kicker abs" style="left:200px;top:96px">HASIL · SUMBER ORGANISASI</div>
  <div class="abs h1" style="left:200px;top:136px;font-size:74px">{kw("Kecekapan sumber organisasi", "s11-h")}</div>
  {html_c}
  <div class="vign"></div>
</div>"""
    js = f"""
FX.words(tl,".s11-h > span",0.1,0.06);
tl.fromTo("#s11-c0",{{y:800}},{{y:0,duration:0.8,ease:"expo.out"}},{t_car - 0.2});
tl.to("#s11-hand",{{rotation:720,duration:2.4,ease:"power2.inOut"}},{t_car});
tl.fromTo("#s11-c1",{{y:900}},{{y:0,duration:0.8,ease:"expo.out"}},{t_kep - 0.2});
tl.fromTo(".s11-p",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:0.3,stagger:0.03,ease:"back.out(2)"}},{t_kep + 0.3});
tl.fromTo("#s11-cnt",{{scale:1.3}},{{scale:1,duration:0.4,ease:"back.out(2)"}},{t_18});
FX.count(tl,document.getElementById("s11-cnt"),18,9,{t_9 - 0.6},0.8,(v)=>String(Math.round(v)),"power2.inOut");
tl.to(".s11-p:nth-child(n+10)",{{opacity:0.15,scale:0.85,duration:0.35,stagger:0.04}},{t_9 - 0.6});
tl.fromTo("#s11-c2",{{y:800}},{{y:0,duration:0.8,ease:"expo.out"}},{t_9 + 0.2});
tl.to(".s11-col",{{y:900,duration:0.5,stagger:0.08,ease:"power3.in"}},{S.D - 0.65});
"""
    return html, js


# --------------------------------------------------------------------------- S12 kurang pencemaran (chalk)
@scene
def s12(S):
    t_sis = S.w("v12", "Sisa")
    t_dok = S.w("v12", "Dokumen")
    t_meja = S.w("v12", "meja", 2)
    t_ruang = S.w("v12", "ruang")
    t_pro = S.w("v12", "produktif")
    html = f"""
<div class="F chalkbg">
  <svg viewBox="0 0 1920 1080" class="abs" style="inset:0" fill="none" stroke="#f1f5ee" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">
    <defs><filter id="s12-cf"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="5" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -1.6 1.3" result="m"/>
      <feComposite in="SourceGraphic" in2="m" operator="in" result="c"/><feDisplacementMap in="c" in2="n" scale="4"/></filter></defs>
    <g filter="url(#s12-cf)">
      <g id="s12-a"><path class="s12-d1" d="M200 420 h240 l-28 320 h-184z M180 420 h280 M285 388 h70"/><path class="s12-d1" d="M260 470 l18 230 M320 470 v230 M380 470 l-18 230"/>
        <path class="s12-d1" d="M120 300 c30 -40 70 -40 90 0 M140 260 c20 -30 50 -30 70 0" stroke-width="6"/></g>
      <g id="s12-ar"><path class="s12-d1b" d="M490 580 h80 M545 552 l28 28 l-28 28" stroke="#b6d973"/><path class="s12-d1b" d="M610 600 h110 l-12 140 h-86z M600 600 h130"/></g>
      <g id="s12-b"><path class="s12-d2" d="M820 640 h160 M840 640 v100 M960 640 v100 M1320 640 h160 M1340 640 v100 M1460 640 v100"/>
        <path class="s12-d2" d="M900 610 c100 -230 330 -230 480 0" stroke-dasharray="4 26"/><path class="s12-d2" d="M1130 430 h60 v74 h-60z M1142 450 h36 M1142 468 h36"/></g>
      <path id="s12-x" class="s12-d2b" d="M1060 380 l200 180 M1260 380 l-200 180" stroke="#ff8a8a" stroke-width="13"/>
      <g id="s12-c"><path class="s12-d3" d="M1560 400 h260 v300 h-260z M1590 440 h70 v100 h-70z M1690 440 h70 v100 h-70z"/></g>
      <g id="s12-c2"><path class="s12-d3b" d="M1560 400 h260 v300 h-260z" stroke="#b6d973"/><path class="s12-d3b" d="M1600 610 h180 M1630 610 v70 M1750 610 v70" stroke="#b6d973"/>
        <circle class="s12-d3b" cx="1640" cy="560" r="22" stroke="#b6d973"/><circle class="s12-d3b" cx="1740" cy="560" r="22" stroke="#b6d973"/></g>
    </g>
  </svg>
  <div class="doodle abs" id="s12-t" style="left:150px;top:80px;font-size:92px;color:#fff">Kurang pencemaran, lebih produktif</div>
  <div class="doodle abs s12-lb" id="s12-l1" style="left:170px;top:800px;font-size:52px;color:#e9f0e4">sisa kertas ↓</div>
  <div class="doodle abs s12-lb" id="s12-l2" style="left:930px;top:800px;font-size:52px;color:#e9f0e4">tiada lagi meja ke meja</div>
  <div class="doodle abs s12-lb" id="s12-l3" style="left:1500px;top:800px;font-size:52px;color:#e9f0e4">ruang lebih produktif</div>
</div>"""
    js = f"""
tl.fromTo("#s12-t",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.9,ease:"power2.inOut"}},0.15);
FX.draw(tl,".s12-d1",{t_sis - 0.1},0.6,0.12);
FX.draw(tl,".s12-d1b",{t_sis + 0.6},0.4,0.1);
tl.fromTo("#s12-l1",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{t_sis + 0.4});
FX.draw(tl,".s12-d2",{t_dok - 0.1},0.7,0.12);
FX.draw(tl,".s12-d2b",{t_meja},0.35,0.1);
tl.fromTo("#s12-l2",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{t_meja});
FX.draw(tl,".s12-d3",{t_ruang - 0.1},0.6,0.1);
tl.to("#s12-c",{{opacity:0,duration:0.3}},{t_pro - 0.6});
FX.draw(tl,".s12-d3b",{t_pro - 0.5},0.5,0.08);
tl.fromTo("#s12-l3",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{t_pro - 0.3});
tl.to("#s12-i .chalkbg",{{opacity:0,duration:0.35}},{S.D - 0.35});
"""
    return html, js


# --------------------------------------------------------------------------- S13 sewaan 14 -> 3
@scene
def s13(S):
    t_pro = S.w("v13", "proses|Proses")
    t_14 = S.w("v13", "empat")
    t_3 = S.w("v13", "tiga")
    t_11 = S.w("v13", "sebelas|Sebelas")
    leaves = "".join(SB.leaf(f"position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{w}px;opacity:0", "#7DB544").replace("<svg ", f'<svg class="s13-lf" ', 1)
                     for x, y, w in [(1560, 640, 54), (1700, 520, 40), (1760, 780, 34), (260, 700, 36), (180, 520, 28)])
    days = "".join(f'<i class="s13-d" id="s13-d{i}" style="display:block;width:52px;height:52px;border-radius:12px;'
                   f'background:{"#B6D973" if i < 3 else "rgba(255,255,255,.16)"};border:1.5px solid rgba(255,255,255,.22);transform-origin:50% 100%"></i>' for i in range(14))
    html = f"""
<div class="F gdark">
  <div class="kicker abs" id="s13-k" style="left:0;right:0;top:150px;text-align:center">PRODUKTIVITI · PROSES PERMOHONAN SEWAAN</div>
  <div class="abs" style="left:0;right:0;top:250px;display:flex;justify-content:center;align-items:center;gap:110px">
    <div id="s13-a" style="text-align:center">
      <div class="mono" style="font-size:24px;color:rgba(255,255,255,.55)">SEBELUM</div>
      <div style="position:relative;display:inline-block;font:800 240px 'Plus Jakarta Sans';letter-spacing:-.04em;color:rgba(255,255,255,.34)">{odo("14")}
        <i id="s13-strike" style="position:absolute;left:-10px;right:-10px;top:50%;height:10px;border-radius:5px;background:#ff5a5a;display:block;transform-origin:0 50%;box-shadow:0 0 20px rgba(255,90,90,.5)"></i></div>
      <div style="font:700 40px 'Plus Jakarta Sans';letter-spacing:.12em;color:rgba(255,255,255,.5)">HARI</div></div>
    <svg id="s13-ar" viewBox="0 0 100 40" style="width:140px"><path id="s13-arp" d="M0 20h86M70 6l16 14-16 14" stroke="#b6d973" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <div id="s13-b" style="text-align:center;position:relative">
      <div class="bloom" id="s13-bl" style="left:-180px;right:-180px;top:-120px;bottom:-120px"></div>
      <div class="mono" style="font-size:24px;color:var(--lime);position:relative">SELEPAS SPD</div>
      <div style="position:relative;display:inline-block;font:800 320px 'Plus Jakarta Sans';letter-spacing:-.04em;color:var(--lime);text-shadow:0 0 60px rgba(182,217,115,.35)">{odo("3")}</div>
      <div style="position:relative;font:700 48px 'Plus Jakarta Sans';letter-spacing:.12em">HARI</div></div>
  </div>
  <div id="s13-days" class="abs" style="left:0;right:0;top:790px;display:flex;justify-content:center;gap:16px">{days}</div>
  <div class="abs" style="left:0;right:0;top:900px;display:flex;justify-content:center">
    <div id="s13-badge" style="display:flex;align-items:center;gap:16px;font:800 44px 'Plus Jakarta Sans';color:#0B2E22;background:#B6D973;padding:14px 44px;border-radius:60px;box-shadow:0 20px 50px rgba(0,0,0,.35);clip-path:inset(0 50% 0 50% round 60px);opacity:0">
      {odo("11")}<span>HARI DIJIMATKAN</span></div></div>
  {leaves}
  <div class="vign"></div>
</div>"""
    js = f"""
tl.fromTo("#s13-k",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.6,ease:"expo.out"}},{max(0.1, t_pro - 0.2)});
tl.fromTo("#s13-a",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.7,ease:"expo.out"}},{t_14 - 0.25});
FX.odo(tl,"#s13-a",{t_14 - 0.2},1.1);
tl.fromTo(".s13-d",{{opacity:0,scaleY:0}},{{opacity:1,scaleY:1,duration:0.5,stagger:0.035,ease:"expo.out"}},{t_14 - 0.1});
tl.fromTo("#s13-strike",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"expo.inOut"}},{t_3 - 0.45});
FX.draw(tl,"#s13-arp",{t_3 - 0.35},0.45,0);
tl.fromTo("#s13-b",{{opacity:0,y:50}},{{opacity:1,y:0,duration:0.7,ease:"expo.out"}},{t_3 - 0.1});
FX.odo(tl,"#s13-b",{t_3 - 0.1},1.2);
FX.bloom(tl,"#s13-bl",{t_3 + 0.2},1);
tl.to("{", ".join(f"#s13-d{i}" for i in range(3, 14))}",{{opacity:0.18,y:14,duration:0.5,stagger:{{each:0.035,from:"end"}},ease:"power3.inOut"}},{t_3 + 0.1});
tl.fromTo(["#s13-d0","#s13-d1","#s13-d2"],{{boxShadow:"0 0 0px rgba(182,217,115,0)"}},{{boxShadow:"0 0 26px rgba(182,217,115,.8)",duration:0.5,stagger:0.08}},{t_3 + 0.5});
tl.fromTo(".s13-lf",{{opacity:0,y:100,rotation:0}},{{opacity:0.75,y:-70,rotation:120,duration:2.4,stagger:0.12,ease:"power1.out"}},{t_3 + 0.2});
tl.fromTo("#s13-badge",{{clipPath:"inset(0 50% 0 50% round 60px)",opacity:0}},{{clipPath:"inset(0 0% 0 0% round 60px)",opacity:1,duration:0.8,ease:"expo.inOut"}},{t_11 - 0.35});
FX.odo(tl,"#s13-badge",{t_11 - 0.15},1.0);
tl.to(["#s13-k","#s13-a","#s13-ar","#s13-b","#s13-days","#s13-badge"],{{y:-50,opacity:0,duration:0.4,stagger:0.03,ease:"power3.in"}},{S.D - 0.5});
"""
    return html, js


# --------------------------------------------------------------------------- S14 semakan aset 20 -> 2
@scene
def s14(S):
    t_sem = S.w("v14", "Semakan")
    t_20 = S.w("v14", "dua", 1)
    t_kini = S.w("v14", "Kini|Hari")
    t_2 = S.w("v14", "dua", 2)
    t_ims = S.w("v14", "imbasan")
    html = f"""
<div class="F" style="background:#081310">
  <div class="kicker abs" style="left:120px;top:90px">PRODUKTIVITI · SEMAKAN ASET ALIH</div>
  <div class="shot" id="s14-m" style="left:120px;top:170px;width:560px;height:452px;transform:rotate(-4deg)"><img src="{IMG}/manual-check.jpg" style="filter:grayscale(1) brightness(.85)"></div>
  <div class="shot" id="s14-b" style="left:720px;top:190px;width:620px;height:500px;transform:rotate(2deg)"><img src="{IMG}/barcode.jpg">
    <div id="s14-las" class="abs" style="left:0;right:0;top:0;height:8px;background:#44ff88;box-shadow:0 0 30px 10px rgba(68,255,136,.6),0 0 80px 30px rgba(68,255,136,.25)"></div></div>
  <div class="shot" id="s14-r" style="left:1380px;top:250px;width:450px;height:330px;transform:perspective(900px) rotateY(-18deg)"><img src="{IMG}/spd-record.jpg"></div>
  <div class="abs" style="left:150px;top:730px;display:flex;align-items:flex-end;gap:46px">
    <div id="s14-old" class="h1" style="font-size:150px;color:rgba(255,255,255,.38);position:relative">{odo("20")}
      <i id="s14-strike" style="position:absolute;left:-8px;right:-8px;top:50%;height:10px;border-radius:5px;background:#ff5a5a;display:block;transform-origin:0 50%;box-shadow:0 0 18px rgba(255,90,90,.5)"></i>
      <div class="mono" style="position:absolute;left:4px;top:-34px;font-size:20px;color:rgba(255,255,255,.5)">MANUAL</div></div>
    <svg id="s14-arw" viewBox="0 0 100 40" style="width:110px;margin-bottom:62px"><path id="s14-arp" d="M0 20h86M70 6l16 14-16 14" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <div id="s14-new" class="h1" style="font-size:200px;color:#44ff88;position:relative;display:flex;align-items:flex-end;gap:22px">
      <div class="bloom" id="s14-bl" style="left:-160px;right:-60px;top:-100px;bottom:-100px;background:radial-gradient(closest-side,rgba(68,255,136,.35),rgba(68,255,136,.08) 55%,transparent)"></div>
      <span style="position:relative;text-shadow:0 0 50px rgba(68,255,136,.35)">{odo("2")}</span><span style="position:relative;font-size:76px;margin-bottom:34px">HARI</span>
      <div class="mono" style="position:absolute;left:6px;top:-34px;font-size:20px;color:#44ff88">SPD · BARCODE</div>
      <i class="uline" id="s14-ul" style="bottom:4px;background:linear-gradient(90deg,rgba(68,255,136,0),#44ff88 30%,#c8ffd9)"></i></div>
  </div>
  <div id="s14-sv" class="abs" style="left:1080px;top:860px;display:flex;align-items:center;gap:14px;font:600 38px Plus Jakarta Sans;color:#cfe">
    <span style="width:12px;height:12px;border-radius:50%;background:#44ff88;box-shadow:0 0 14px #44ff88"></span>
    <b style="color:#fff;font-size:46px">{odo("18")}</b><span>hari dijimatkan</span></div>
  <div class="vign"></div>
</div>"""
    js = f"""
tl.fromTo("#s14-m",{{opacity:0,x:-300,rotation:-14}},{{opacity:1,x:0,rotation:-4,duration:0.7,ease:"expo.out"}},{max(0.1, t_sem - 0.2)});
tl.fromTo("#s14-old",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.6,ease:"expo.out"}},{t_20 - 0.2});
FX.odo(tl,"#s14-old",{t_20 - 0.15},1.0);
tl.fromTo("#s14-b",{{opacity:0,y:300,rotation:10}},{{opacity:1,y:0,rotation:2,duration:0.7,ease:"expo.out"}},{t_kini - 0.3});
tl.fromTo("#s14-las",{{y:0}},{{y:490,duration:0.8,yoyo:true,repeat:1,ease:"power1.inOut"}},{t_ims - 0.2});
tl.fromTo("#s14-strike",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"expo.inOut"}},{t_2 - 0.4});
FX.draw(tl,"#s14-arp",{t_2 - 0.3},0.4,0);
tl.fromTo("#s14-new",{{opacity:0,y:50}},{{opacity:1,y:0,duration:0.7,ease:"expo.out"}},{t_2 - 0.1});
FX.odo(tl,"#s14-new",{t_2 - 0.1},1.1);
FX.bloom(tl,"#s14-bl",{t_2 + 0.2},1);
FX.uline(tl,"#s14-ul",{t_2 + 0.35});
tl.fromTo("#s14-r",{{opacity:0,x:300}},{{opacity:1,x:0,duration:0.6,ease:"expo.out"}},{t_ims + 0.6});
tl.fromTo("#s14-sv",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.6,ease:"expo.out"}},{t_ims + 0.9});
FX.odo(tl,"#s14-sv",{t_ims + 0.95},1.0);
tl.to(["#s14-m","#s14-b","#s14-r"],{{y:-700,duration:0.5,stagger:0.05,ease:"power3.in"}},{S.D - 0.55});
tl.to(["#s14-old","#s14-arw","#s14-new","#s14-sv"],{{opacity:0,y:-30,duration:0.4,stagger:0.03,ease:"power3.in"}},{S.D - 0.5});
"""
    return html, js


# --------------------------------------------------------------------------- S15 penjimatan kos
@scene
def s15(S):
    t_ang = S.w("v15", "Anggaran")
    t_dua = S.w("v15", "dua")
    t_rgt = S.w("v15", "ringgit")
    t_set = S.w("v15", "setahun")
    # each digit of RM217,836 locks as the VO says it: dua ratus | tujuh belas ribu | lapan ratus | tiga puluh | enam
    t_bel, t_lap, t_tig, t_ena = S.w("v15", "belas"), S.w("v15", "lapan"), S.w("v15", "puluh"), S.w("v15", "enam")
    lock = [t_dua + 0.35, t_bel + 0.05, t_bel + 0.2, t_lap + 0.3, t_tig + 0.1, t_ena + 0.3]
    people = "".join(f'<div class="s15-p" style="display:inline-block">{SB.person("#D9AE52")}</div>' for j in range(18))
    html = f"""
<div class="F gdark">
  <div class="kicker abs" style="left:130px;top:120px">PENJIMATAN KOS TENAGA KERJA</div>
  <div class="abs" style="left:130px;top:190px;width:640px;line-height:0">{people}</div>
  <div class="abs" id="s15-pp" style="left:130px;top:420px;font:700 36px Plus Jakarta Sans">18 orang → <span style="color:#D9AE52">9 orang</span></div>
  <table class="abs" id="s15-tb" style="left:130px;top:510px;width:720px;border-collapse:separate;border-spacing:0 14px;font:700 34px Plus Jakarta Sans;color:#fff">
    <tr style="color:#B6D973;font-size:24px;letter-spacing:.14em"><td>UKURAN</td><td>SEBELUM</td><td>SELEPAS</td></tr>
    <tr class="s15-r"><td>Kos bulanan</td><td style="opacity:.55">RM36,306</td><td>RM18,153</td></tr>
    <tr class="s15-r"><td>Kos tahunan</td><td style="opacity:.55">RM435,672</td><td>RM217,836</td></tr></table>
  <div class="abs" style="right:120px;top:330px;text-align:right">
    <div class="mono" style="font-size:30px;color:#D9AE52">ANGGARAN PENJIMATAN TAHUNAN</div>
    <div id="s15-n" class="h1" style="position:relative;font-size:158px;margin-top:10px">
      <div class="bloom" id="s15-bl" style="left:-120px;right:-120px;top:-110px;bottom:-110px;background:radial-gradient(closest-side,rgba(217,174,82,.32),rgba(217,174,82,.08) 55%,transparent)"></div>
      <span style="position:relative">{odo("RM217,836", cls="odo-gold")}</span>
      <i class="uline" id="s15-ul" style="bottom:-6px;background:linear-gradient(90deg,rgba(217,174,82,0),#D9AE52 35%,#fff3c8);box-shadow:0 0 18px rgba(217,174,82,.6)"></i></div>
    <div id="s15-s" style="font:600 34px Plus Jakarta Sans;color:#cfe3d6">setahun · kaedah anggaran kos upah</div>
  </div>
  <div class="vign"></div>
</div>"""
    js = f"""
tl.fromTo(".s15-p",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.3,stagger:0.03}},{max(0.1, t_ang - 0.2)});
tl.to(".s15-p:nth-child(n+10)",{{opacity:0.15,duration:0.3,stagger:0.03}},{t_ang + 0.8});
tl.fromTo("#s15-pp",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.4}},{t_ang + 0.9});
tl.fromTo(".s15-r",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.45,stagger:0.25,ease:"expo.out"}},{t_ang + 1.3});
tl.fromTo("#s15-n",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.7,ease:"expo.out"}},{t_dua - 0.45});
FX.odo(tl,"#s15-n",{t_dua - 0.3},0,{{lock:{json.dumps([round(x, 3) for x in lock])},ease:"power3.out"}});
FX.bloom(tl,"#s15-bl",{t_ena},1);
FX.uline(tl,"#s15-ul",{t_ena + 0.15});
tl.fromTo("#s15-s",{{opacity:0}},{{opacity:1,duration:0.4}},{t_set - 0.1});
tl.to("#s15-i .gdark > *",{{opacity:0,duration:0.35}},{S.D - 0.4});
"""
    return html, js


# --------------------------------------------------------------------------- S16 kertas A4 & dakwat
@scene
def s16(S):
    t_ant = S.w("v16", "Bagi|Antara")
    t_ber = S.w("v16", "menurun|berkurang")
    t_25 = S.w("v16", "dua", 5)
    t_dak = S.w("v16", "dakwat")
    t_39 = S.w("v16", "tiga")

    def chart(cid, x, title, a, b, mx, pct, unit):
        ha, hb = a / mx * 440, b / mx * 440
        return (f'<div class="abs" style="left:{x}px;top:170px;width:700px">'
                f'<div class="h1" style="font-size:42px;color:#0B2E22">{title}</div>'
                f'<div class="abs" style="top:120px;left:40px;width:620px;height:500px;border-bottom:4px solid #22302A">'
                f'<div id="{cid}-a" class="abs" style="bottom:0;left:60px;width:200px;height:{ha:.0f}px;background:linear-gradient(90deg,#5f7d8c,#3d5866);border-radius:10px 10px 0 0;box-shadow:16px -8px 0 #2b414c;transform-origin:50% 100%"></div>'
                f'<div id="{cid}-an" class="abs" style="bottom:{ha + 12:.0f}px;left:60px;width:200px;text-align:center;font:800 46px Plus Jakarta Sans;color:#22302A">{a:,}</div>'
                f'<div id="{cid}-b" class="abs" style="bottom:0;left:360px;width:200px;height:{ha:.0f}px;background:linear-gradient(90deg,#3fa877,#26745A);border-radius:10px 10px 0 0;box-shadow:16px -8px 0 #1a5a43;transform-origin:50% 100%"></div>'
                f'<div id="{cid}-bn" class="abs" style="bottom:{ha + 12:.0f}px;left:330px;width:260px;height:52px;text-align:center;font:800 46px Plus Jakarta Sans;color:#165A44">'
                f'<span id="{cid}-bo" class="abs" style="left:0;right:0;top:0;font-variant-numeric:tabular-nums">{a:,}</span>'
                f'<span id="{cid}-bv" class="abs" style="left:0;right:0;top:-4px;opacity:0">{odo(f"{b:,}", f"{a:,}" if len(f"{a:,}") == len(f"{b:,}") else None)}</span></div>'
                f'<div class="abs mono" style="bottom:-54px;left:60px;width:200px;text-align:center;font-size:28px;color:#22302A;letter-spacing:0">2021</div>'
                f'<div class="abs mono" style="bottom:-54px;left:360px;width:200px;text-align:center;font-size:28px;color:#22302A;letter-spacing:0">2025</div></div>'
                f'<div id="{cid}-p" class="abs" style="top:96px;right:0;display:flex;align-items:center;gap:12px;font:800 64px Plus Jakarta Sans;color:#fff;'
                f'background:linear-gradient(135deg,#e0364a,#a3172b);padding:8px 28px 8px 22px;border-radius:18px;box-shadow:0 18px 40px rgba(163,23,43,.35);clip-path:inset(0 100% 0 0 round 18px)">'
                f'<svg viewBox="0 0 20 20" style="width:34px"><path d="M10 18 L2 6 H18 Z" fill="#fff"/></svg>{odo(pct.lstrip("−"))}</div>'
                f'<div id="{cid}-u" class="abs" style="top:705px;left:40px;font:600 30px Plus Jakarta Sans;color:#3b4842">{unit}</div></div>'), hb / ha
    c1, r1 = chart("s16-x", 140, "Permohonan kertas A4", 1242, 926, 1300, "−25.4%", "Berkurang 316 unit")
    c2, r2 = chart("s16-y", 1040, "Permohonan dakwat pencetak", 174, 105, 182, "−39.7%", "Berkurang 69 unit")
    html = f"""
<div class="F paperbg">
  {c1}{c2}
  <svg viewBox="0 0 1920 1080" class="abs" style="inset:0"><path id="s16-dv" d="M960 200 v700" stroke="#22302A" stroke-width="5" stroke-dasharray="10 20"/></svg>
</div>"""

    def anim(cid, t0, tb, tp, r, a, b):
        return (f'tl.fromTo(["#{cid}-a","#{cid}-b"],{{scaleY:0}},{{scaleY:1,duration:0.7,stagger:0.1,ease:"expo.out"}},{t0});'
                f'tl.fromTo(["#{cid}-an","#{cid}-bn"],{{opacity:0}},{{opacity:1,duration:0.3}},{t0 + 0.4});'
                f'tl.to("#{cid}-b",{{scaleY:{r:.4f},duration:0.8,ease:"power3.inOut"}},{tb});'
                f'tl.to("#{cid}-bn",{{y:{(1 - r) * 440 * (1 if a > 500 else 440 / 440):.0f},duration:0.8,ease:"power3.inOut"}},{tb});'
                f'tl.to("#{cid}-bo",{{opacity:0,y:-26,duration:0.3,ease:"power2.in"}},{tb});'
                f'tl.fromTo("#{cid}-bv",{{opacity:0}},{{opacity:1,duration:0.25}},{tb + 0.15});'
                f'FX.odo(tl,"#{cid}-bv",{tb + 0.1},1.0,{{ease:"power3.out"}});'
                f'tl.fromTo("#{cid}-p",{{clipPath:"inset(0 100% 0 0 round 18px)"}},{{clipPath:"inset(0 0% 0 0 round 18px)",duration:0.7,ease:"expo.inOut"}},{tp - 0.2});'
                f'FX.odo(tl,"#{cid}-p",{tp},1.1);'
                f'tl.fromTo("#{cid}-u",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{tp + 0.3});')
    js = f"""
{anim("s16-x", max(0.1, t_ant - 0.2), t_ber - 0.2, t_25 - 0.1, r1, 1242, 926)}
{anim("s16-y", t_dak - 0.5, t_dak + 0.3, t_39 - 0.1, r2, 174, 105)}
tl.to("#s16-i .paperbg",{{x:-1920,duration:0.5,ease:"power3.in"}},{S.D - 0.5});
"""
    return html, js


# --------------------------------------------------------------------------- S17 digitalisasi & bukti
@scene
def s17(S):
    t_fail = S.w("v17", "Fail")
    t_dig = S.w("v17", "digantikan")
    t_buk = S.w("v17", "bukti|Buktinya")
    t_stok = S.w("v17", "stok")
    t_per = S.w("v17", "pemeriksaan")
    import random
    r = random.Random(9)
    parts = ""
    for i in range(160):
        x, y, sz = r.randint(140, 760), r.randint(260, 760), r.randint(5, 16)
        c = r.choice(["#e8e1cf", "#f6f1e3", "#B6D973", "#ffffff", "#c9c1ad"])
        parts += (f'<i class="s17-pt" data-tx="{r.randint(1180, 1800) - x}" data-ty="{r.randint(260, 760) - y}" '
                  f'style="position:absolute;left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;background:{c};display:block;opacity:0;transform:rotate({r.randint(0, 90)}deg)"></i>')
    pol = [("manual-stock1.jpg", "Manual: permohonan stok", 140, 230, -8, True), ("spd-stock.jpg", "SPD: permohonan stok", 600, 170, 4, False),
           ("manual-check.jpg", "Manual: pemeriksaan aset", 1060, 250, -3, True), ("barcode.jpg", "SPD: imbas barcode", 1420, 150, 7, False)]
    pols = "".join(
        f'<div class="abs s17-pol" id="s17-po{i}" style="left:{x}px;top:{y}px;width:420px;background:#fff;padding:20px 20px 70px;transform:rotate({rr}deg);box-shadow:0 30px 60px rgba(0,0,0,.45);opacity:0">'
        f'<img src="{IMG}/{f}" style="width:380px;height:330px;object-fit:cover;display:block;{"filter:grayscale(1)" if g else ""}">'
        f'<div class="doodle abs" style="left:20px;bottom:12px;font-size:38px;color:#22302A">{t}</div></div>'
        for i, (f, t, x, y, rr, g) in enumerate(pol))
    html = f"""
<div class="F gdark">
  <div id="s17-a" class="abs" style="inset:0">
    <div class="shot" id="s17-f" style="left:130px;top:250px;width:640px;height:520px;transform:perspective(1000px) rotateY(18deg)"><img src="{IMG}/fail-gantung.jpg"></div>
    {parts}
    <div class="shot" id="s17-d" style="left:1170px;top:250px;width:640px;height:520px;transform:perspective(1000px) rotateY(-18deg);box-shadow:0 0 0 3px #B6D973,0 40px 90px rgba(0,0,0,.6)">
      <img src="{IMG}/spd-record.jpg" style="object-fit:contain;background:#fff"></div>
    <div id="s17-t" class="abs h1" style="left:0;right:0;top:850px;text-align:center;font-size:100px;letter-spacing:.12em">DIGITALISASI</div>
  </div>
  <div id="s17-b" class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 40%,#7a5a3c,#3b2a1b 80%);opacity:0">{pols}
    <div class="mono abs" style="left:140px;top:930px;font-size:26px;color:#F3E3B5">BUKTI PELAKSANAAN · SEBELUM &amp; SELEPAS</div></div>
  <div class="vign"></div>
</div>"""
    js = f"""
tl.fromTo("#s17-f",{{opacity:0,x:-200}},{{opacity:1,x:0,duration:0.6,ease:"expo.out"}},{max(0.05, t_fail - 0.3)});
tl.to("#s17-f",{{opacity:0.15,filter:"blur(4px)",duration:0.9}},{t_dig - 0.2});
tl.fromTo(".s17-pt",{{opacity:0,x:0,y:0}},{{opacity:1,duration:0.2,stagger:0.004}},{t_dig - 0.3});
tl.to(".s17-pt",{{x:(i,e)=>+e.dataset.tx,y:(i,e)=>+e.dataset.ty,rotation:180,duration:1.0,stagger:0.004,ease:"power2.inOut"}},{t_dig - 0.1});
tl.to(".s17-pt",{{opacity:0,duration:0.3,stagger:0.003}},{t_dig + 0.8});
tl.fromTo("#s17-d",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.6,ease:"back.out(1.6)"}},{t_dig + 0.6});
tl.fromTo("#s17-t",{{opacity:0,scale:1.3}},{{opacity:1,scale:1,duration:0.5,ease:"expo.out"}},{t_dig + 0.7});
tl.to("#s17-a",{{opacity:0,scale:1.1,duration:0.35}},{t_buk - 0.3});
tl.to("#s17-b",{{opacity:1,duration:0.35}},{t_buk - 0.3});
tl.fromTo(["#s17-po0","#s17-po1"],{{opacity:0,y:-500,rotation:-30}},{{opacity:1,y:0,rotation:(i)=>[-8,4][i],duration:0.55,stagger:0.25,ease:"back.out(1.4)"}},{t_buk});
tl.fromTo(["#s17-po2","#s17-po3"],{{opacity:0,y:-500,rotation:30}},{{opacity:1,y:0,rotation:(i)=>[-3,7][i],duration:0.55,stagger:0.25,ease:"back.out(1.4)"}},{t_per - 0.2});
tl.to("#s17-b",{{x:-200,opacity:0,duration:0.4,ease:"power3.in"}},{S.D - 0.4});
"""
    return html, js


# --------------------------------------------------------------------------- S18 pengiktirafan
@scene
def s18(S):
    t_iki = S.w("v18", "pengiktirafan|diiktiraf")
    t_2020 = S.w("v18", "dua")
    t_plat = S.w("v18", "platform")
    html = f"""
<div class="F" style="background:linear-gradient(120deg,#F5F2EA,#E9F2E7)">
  <div class="shot" id="s18-c" style="left:200px;top:120px;width:560px;height:762px;border-radius:6px"><img src="{IMG}/copyright.png" style="object-fit:contain;background:#fff"></div>
  <div id="s18-seal" class="abs" style="left:600px;top:700px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#d43a3a,#8E1B33 70%);
    box-shadow:0 20px 40px rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center;text-align:center;font:800 30px/1.2 'JetBrains Mono';color:#ffd9d9">HAK<br>CIPTA</div>
  <div class="abs" style="left:960px;top:250px;width:820px;color:#0B2E22">
    <div class="kicker" style="color:#26745A">KELANGSUNGAN · PENGIKTIRAFAN</div>
    <div class="h1" style="font-size:84px;margin-top:16px">{kw("Diiktiraf. Diguna pakai sepenuhnya.", "s18-h")}</div>
    <div id="s18-a" style="margin-top:40px;background:#fff;border-left:10px solid #165A44;border-radius:16px;padding:26px 30px;font:600 32px/1.35 'Plus Jakarta Sans';color:#2b3a33">
      Sijil Pemberitahuan Hak Cipta<br><b style="color:#165A44">2 Mac 2020</b></div>
    <div id="s18-b" style="margin-top:20px;background:#fff;border-left:10px solid #B6D973;border-radius:16px;padding:26px 30px;font:600 32px/1.35 'Plus Jakarta Sans';color:#2b3a33">
      Platform utama pengurusan data MCORP</div>
  </div>
</div>"""
    js = f"""
tl.fromTo("#s18-c",{{opacity:0,x:-500,rotation:-25}},{{opacity:1,x:0,rotation:-5,duration:0.8,ease:"expo.out"}},0.15);
FX.words(tl,".s18-h > span",{t_iki - 0.2},0.07);
tl.fromTo("#s18-seal",{{opacity:0,scale:3,rotation:-60}},{{opacity:1,scale:1,rotation:-12,duration:0.3,ease:"power4.in"}},{t_iki + 0.1});
tl.fromTo("#s18-c",{{x:0}},{{x:6,duration:0.05,yoyo:true,repeat:3,immediateRender:false}},{t_iki + 0.4});
tl.fromTo("#s18-a",{{opacity:0,x:80}},{{opacity:1,x:0,duration:0.5,ease:"expo.out"}},{t_2020 - 0.3});
tl.fromTo("#s18-b",{{opacity:0,x:80}},{{opacity:1,x:0,duration:0.5,ease:"expo.out"}},{t_plat - 0.2});
tl.to("#s18-i .F > *",{{opacity:0,duration:0.4}},{S.D - 0.4});
"""
    return html, js


# --------------------------------------------------------------------------- S19 akan datang: SPD 2.0 + Green Dashboard
@scene
def s19(S):
    t_dan = S.w("v19", "Dan")
    t_aka = S.w("v19", "Akan")
    t_spd = S.w("v19", "SPD")
    t_ber = S.w("v19", "bersama")
    t_set = S.w("v19", "Setiap")
    t_ker = S.w("v19", "Kertas")
    t_dak = S.w("v19", "Dakwat")
    t_mas = S.w("v19", "Masa")
    t_ten = S.w("v19", "Tenaga")
    t_kos = S.w("v19", "kos", 2)  # 1st match is "kosong" (dua point kosong)
    t_kar = S.w("v19", "Kerana")
    t_uru = S.w("v19", "diurus")
    page = sb(SB.spd2_homepage(full=True))
    page = page.replace('<div style="transform:translateY(-0px)">', '<div id="s19-page">', 1)
    page = re.sub(r'<div style="height:96px;background:#fff;display:flex;align-items:center;padding:0 34px;gap:26px;.*?PEGAWAI SPD ▾</div></div>',
                  '<div style="height:96px;position:relative;z-index:3;background:url(assets/ui/s77.jpg) 0 0/1920px auto;box-shadow:0 2px 8px rgba(0,0,0,.06)">'
                  '<span style="position:absolute;left:750px;top:30px;background:#165A44;color:#fff;padding:2px 12px;border-radius:8px;font:800 24px Plus Jakarta Sans">2.0</span></div>',
                  page, count=1, flags=re.S)
    page = page.replace('<div style="width:300px;background:#8E1B33;min-height:2000px;padding-top:20px">',
                        '<div id="s19-side" style="width:300px;background:#8E1B33;min-height:2000px;padding-top:20px;position:relative;z-index:2">', 1)
    for i, v in enumerate(["−25.4%", "−39.7%", "−79%", "−90%", "−50%", "RM217,836"]):
        page = re.sub(r'(margin-top:8px">)' + re.escape(v) + "</div>", lambda m, i=i, v=v: m.group(1) + f'<span class="s19-kv" id="s19-k{i}" style="display:inline-block">{odo(v)}</span></div>', page, count=1)
    page = page.replace('stroke="url(#gg)"', 'id="s19-g" stroke="url(#gg)"', 1)
    page = page.replace('font-size="76" fill="#0B2E22">82</text>', 'font-size="76" fill="#0B2E22" id="s19-gt">0</text>', 1)
    page = page.replace('<div style="margin-top:24px;background:linear-gradient(90deg,#0B2E22,#165A44);border-radius:14px;padding:14px 10px;display:flex;align-items:center">',
                        '<div id="s19-meter" style="margin-top:24px;background:linear-gradient(90deg,#0B2E22,#165A44);border-radius:14px;padding:14px 10px;display:flex;align-items:center">', 1)
    rings = "".join(f'<div class="abs s19-rg" style="left:50%;top:50%;width:{w}px;height:{w}px;margin:-{w // 2}px 0 0 -{w // 2}px;border-radius:50%;'
                    f'border:{3 + i}px solid rgba(182,217,115,{0.15 + i * 0.07:.2f})"></div>' for i, w in enumerate([300, 600, 900, 1300, 1800, 2400]))
    circ = 2 * 3.14159 * 110
    html = f"""
<div class="F" style="background:#03100b">
  <div id="s19-tun" class="abs" style="inset:0">{rings}</div>
  <div id="s19-soon" class="abs" style="left:0;right:0;top:330px;text-align:center">
    <div class="mono" id="s19-k" style="display:inline-block;font-size:30px;color:#0B2E22;background:#B6D973;padding:10px 22px;border-radius:8px">AKAN DATANG</div>
    <div class="h1" id="s19-big" style="font-size:210px;margin-top:20px">SPD <span style="color:var(--lime)">2.0</span></div>
    <div id="s19-gd" style="font:700 54px 'Plus Jakarta Sans';color:#cfe3d6">+ Green Dashboard</div>
  </div>
  <div id="s19-win" class="abs" style="left:0;top:0;width:1920px;height:1080px;transform-origin:50% 50%;opacity:0;border-radius:22px;overflow:hidden;box-shadow:0 60px 160px rgba(0,0,0,.7),0 0 0 2px rgba(182,217,115,.4)">{page}</div>
  <div id="s19-tag" class="mono abs" style="left:60px;top:40px;font-size:24px;color:#0B2E22;background:#B6D973;padding:8px 16px;border-radius:6px;opacity:0;z-index:5">AKAN DATANG · PRATONTON</div>
  <div id="s19-end" class="abs h1" style="left:0;right:0;top:470px;text-align:center;font-size:84px;opacity:0;text-shadow:0 10px 40px rgba(0,0,0,.7)">Apa yang diukur, <span style="color:var(--lime)">dapat diurus.</span></div>
  <div class="vign"></div>
</div>"""
    kv = [(0, t_ker), (1, t_dak), (2, t_mas), (3, t_mas + 0.25), (4, t_ten), (5, t_kos)]
    js_kv = "".join(f'tl.fromTo("#s19-k{i}",{{opacity:0.12,y:10}},{{opacity:1,y:0,duration:0.5,ease:"expo.out"}},{t - 0.1:.2f});'
                    f'FX.odo(tl,"#s19-k{i}",{t - 0.1:.2f},0.9,{{stagger:0.05}});' for i, t in kv)
    js = f"""
tl.fromTo(".s19-rg",{{scale:0.2,opacity:0}},{{scale:2.2,opacity:1,duration:2.2,stagger:0.12,ease:"power2.in"}},0);
tl.fromTo("#s19-k",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{t_aka - 0.1});
tl.fromTo("#s19-big",{{opacity:0,scale:1.6,filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.6,ease:"expo.out"}},{t_spd - 0.1});
tl.fromTo("#s19-gd",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.5,ease:"expo.out"}},{t_ber});
tl.to("#s19-soon",{{scale:0.6,opacity:0,duration:0.5,ease:"power3.in"}},{t_set - 0.9});
tl.to("#s19-tun",{{opacity:0,duration:0.6}},{t_set - 0.8});
// SPD 2.0 homepage window
tl.set(".s19-kv",{{opacity:0.12}},0);
tl.fromTo("#s19-win",{{opacity:0,scale:0.5,rotationX:30,y:200,transformPerspective:2000}},{{opacity:1,scale:0.86,rotationX:6,y:0,duration:0.9,ease:"expo.out"}},{t_set - 0.7});
tl.fromTo("#s19-tag",{{opacity:0}},{{opacity:1,duration:0.4}},{t_set - 0.3});
// scroll down to the Green Dashboard section (sidebar stays put)
tl.fromTo("#s19-page",{{y:0}},{{y:-560,duration:1.1,ease:"power3.inOut"}},{t_set + 0.1});
tl.fromTo("#s19-side",{{y:0}},{{y:560,duration:1.1,ease:"power3.inOut"}},{t_set + 0.1});
tl.to("#s19-win",{{scale:0.9,rotationX:0,duration:1.5,ease:"power2.inOut"}},{t_set + 0.1});
tl.fromTo("#s19-g",{{strokeDasharray:"0 {circ:.0f}"}},{{strokeDasharray:"{circ * 0.82:.0f} {circ:.0f}",duration:1.6,ease:"power3.out"}},{t_set + 1.0});
FX.count(tl,document.getElementById("s19-gt"),0,82,{t_set + 1.0},1.6,(v)=>String(Math.round(v)),"power3.out");
document.getElementById("s19-gt").style.fontVariantNumeric="tabular-nums";
{js_kv}
tl.fromTo("#s19-meter",{{opacity:0.2}},{{opacity:1,duration:0.5}},{t_kos + 0.3});
tl.to("#s19-win",{{scale:1.0,y:-40,duration:2.0,ease:"power1.inOut"}},{t_kar - 0.8});
tl.to("#s19-win",{{filter:"brightness(0.3) blur(3px)",duration:0.6}},{t_uru - 1.0});
tl.fromTo("#s19-end",{{opacity:0,scale:1.15}},{{opacity:1,scale:1,duration:0.6,ease:"expo.out"}},{t_uru - 0.9});
tl.to(["#s19-win","#s19-end","#s19-tag"],{{opacity:0,duration:0.45}},{S.D - 0.45});
"""
    return html, js


# --------------------------------------------------------------------------- S20 penutup
@scene
def s20(S):
    t_spd = S.w("v20", "SPD")
    t_m1 = S.w("v20", "Mendigitalkan")
    t_m2 = S.w("v20", "Mengoptimumkan")
    t_m3 = S.w("v20", "Mempercepat")
    t_ke = S.w("v20", "Ke")
    tiles = "".join(f'<div class="abs s20-ti" style="left:{x}px;top:{y}px;width:220px;height:130px;border-radius:16px;background:rgba(255,255,255,.08);'
                    f'border:2px solid rgba(182,217,115,.5);display:flex;align-items:center;justify-content:center;font:800 40px Plus Jakarta Sans;color:#b6d973">{v}</div>'
                    for x, y, v in [(80, 120, "−25.4%"), (1620, 140, "−39.7%"), (60, 820, "−79%"), (1640, 840, "−90%"), (820, -40, "−50%"), (800, 980, "RM217k")])
    html = f"""
<div class="F" style="background:#0B2E22">
  <div class="abs" style="left:0;top:0;bottom:0;width:22px;background:#B6D973"></div>
  <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 40%,rgba(182,217,115,.22),transparent 60%)"></div>
  {tiles}
  <div id="s20-mark" class="abs" style="left:0;right:0;top:200px;display:flex;justify-content:center">{SB.spd_mark(230, "#B6D973", "#B6D973")}</div>
  <div class="abs" style="left:0;right:0;top:520px;text-align:center;font:800 56px/1.2 'Plus Jakarta Sans'">{kw("INOVASI DIGITAL KE ARAH", "s20-h1")}<br>{kw("PENGURUSAN HIJAU DAN LESTARI", "s20-h2")}</div>
  <div class="abs" style="left:0;right:0;top:704px;text-align:center;font:600 32px 'Plus Jakarta Sans';color:#cfe3d6">
    <span id="s20-a">Mendigitalkan proses</span> <span style="color:#B6D973">•</span> <span id="s20-b">Mengoptimumkan sumber</span> <span style="color:#B6D973">•</span> <span id="s20-c">Mempercepat penyampaian</span></div>
  <div id="s20-slo" class="abs" style="left:0;right:0;top:786px;text-align:center;font:600 italic 36px 'Plus Jakarta Sans';color:#D9AE52">Less Paper. Smarter Assets. Greener Future.</div>
  <div id="s20-org" class="mono abs" style="left:0;right:0;top:930px;text-align:center;font-size:26px;color:#B6D973">PERBADANAN MELAKA (MCORP) | 2026</div>
  <div id="s20-blk" class="abs" style="inset:0;background:#000;opacity:0"></div>
</div>"""
    js = f"""
tl.fromTo(".s20-ti",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.4,stagger:0.05}},0);
tl.to(".s20-ti",{{x:(i)=>[770,-770,790,-790,30,50][i],y:(i)=>[150,130,-550,-570,310,-710][i],scale:0.2,opacity:0,duration:0.8,stagger:0.04,ease:"power3.in"}},{max(0.5, t_spd - 0.7)});
tl.fromTo("#s20-mark",{{opacity:0,scale:0.4,filter:"blur(14px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.6,ease:"expo.out"}},{t_spd - 0.05});
tl.fromTo("#s20-mark svg",{{rotation:-180,scale:0}},{{rotation:28,scale:1,duration:0.8,ease:"back.out(2)"}},{t_spd + 0.15});
FX.words(tl,".s20-h1 > span",{t_spd + 0.3},0.06);
FX.words(tl,".s20-h2 > span",{t_spd + 0.5},0.06);
tl.fromTo("#s20-a",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{t_m1 - 0.05});
tl.fromTo("#s20-b",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{t_m2 - 0.05});
tl.fromTo("#s20-c",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{t_m3 - 0.05});
tl.fromTo("#s20-slo",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.6}},{t_ke + 0.2});
tl.fromTo("#s20-org",{{opacity:0}},{{opacity:1,duration:0.6}},{t_ke + 0.8});
tl.to("#s20-blk",{{opacity:1,duration:1.0,ease:"power1.in"}},{S.D - 1.0});
"""
    return html, js


# ============================================================================= FILM PLAN
XFADE = 0.6
PLAN = [  # (scene id, VO lines, kwargs)  -- v4: s11, s12, s17 cut as duplicates (functions kept)
    ("s01", ["v01"], dict(pre=MONTAGE + 0.2, post=0.9)),
    ("s02", ["v02"], dict(pre=0.5, post=0.9)),
    ("s03", ["v03"], dict(pre=0.5, post=1.1)),
    ("s04", ["v04"], dict(pre=0.5, post=1.1)),
    ("s05", ["v05"], dict(pre=1.2, post=0.9)),
    ("s06", ["v06"], dict(pre=0.5, post=1.4)),
    ("s07", ["v07"], dict(pre=0.5, post=1.2)),
    ("s08", ["v08"], dict(pre=0.5, post=2.4)),
    ("s09", ["v09"], dict(pre=0.7, post=1.0)),
    ("s10", ["v10"], dict(pre=0.5, post=1.4)),
    ("s13", ["v13"], dict(pre=0.5, post=1.2)),
    ("s14", ["v14"], dict(pre=0.5, post=1.0)),
    ("s15", ["v15"], dict(pre=0.5, post=1.4)),
    ("s16", ["v16"], dict(pre=0.5, post=1.1)),
    ("s18", ["v18"], dict(pre=0.5, post=1.0)),
    ("s19", ["v19"], dict(pre=0.7, post=2.4)),
    ("s20", ["v20"], dict(pre=1.0, post=2.4)),
]

TEMPLATE = """<!doctype html>
<html lang="ms">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <div id="root" data-composition-id="{id}" data-width="1920" data-height="1080" style="position:absolute;inset:0;overflow:hidden">
      <div id="{id}-o" style="position:absolute;inset:0"><div id="{id}-i" style="position:absolute;inset:0">
{html}
      </div></div>
      </div>
      <script>
        (function () {{
          const tl = gsap.timeline({{ paused: true }});
          const FX = window.SPDFX;
{js}
          // camera: crossfade in over the previous scene + slow breathing push (no blur-in)
{cam}
          tl.set({{}}, {{}}, {D});
          window.__timelines = window.__timelines || {{}};
          window.__timelines["{id}"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""

CAM = """          tl.fromTo("#{id}-o", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power1.inOut" }}, 0);
          tl.fromTo("#{id}-i", {{ scale: 1 }}, {{ scale: 1.03, duration: {D}, ease: "none", transformOrigin: "50% 50%" }}, 0);"""
# s01 opens the film on full-resolution footage: no fade from black, no upscaling push (both soften the first shot)
CAM_OPEN = """          tl.set("#{id}-o", {{ opacity: 1 }}, 0);"""


def build(only=None, write=True):
    built = []
    t = 0.0
    for sid, lines, kw_ in PLAN:
        S = Scene(sid, lines, **kw_)
        S.start = round(t, 3)
        t += S.D - XFADE  # next scene starts XFADE before this one ends and fades in on top
        built.append(S)
        if not write or (only and sid not in only):
            continue
        html, js = SCENES[sid](S)
        open(f"{HF}/compositions/{sid}.html", "w").write(TEMPLATE.format(id=sid, html=html, js=js, D=S.D, cam=(CAM_OPEN if sid == "s01" else CAM).format(id=sid, D=S.D)))
    return built, round(t + XFADE, 3)


BADGE = """<!doctype html>
<html lang="ms">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <div id="root" data-composition-id="badge" data-width="1920" data-height="1080" style="position:absolute;inset:0;pointer-events:none">
        <div id="bd-stage" style="position:absolute;right:36px;top:26px;width:132px;height:88px;perspective:700px">
          <div id="bd-card" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;transform-style:preserve-3d">
            <img src="assets/img/logo-pptx.png" alt="MCORP Perbadanan Melaka" style="width:132px;height:88px;display:block;
              filter:drop-shadow(0 0 1.5px #fff) drop-shadow(0 0 1.5px #fff) drop-shadow(0 0 1px #fff) drop-shadow(0 6px 10px rgba(0,0,0,.45))" />
          </div>
        </div>
      </div>
      <script>
        (function () {{
          const D = {D};
          const card = document.getElementById("bd-card");
          const stage = document.getElementById("bd-stage");
          const SWING = 28, PERIOD = 4.2; // swings left-right, never a full spin
          function render(t) {{
            const ph = (2 * Math.PI * t) / PERIOD;
            card.style.transform = `rotateY(${{(SWING * Math.sin(ph)).toFixed(2)}}deg) rotateX(${{(6 * Math.sin(ph * 0.5 + 1.2)).toFixed(2)}}deg)`;
            stage.style.opacity = Math.min(1, t / 0.6).toFixed(3);
          }}
          const clock = {{ t: 0 }};
          const tl = gsap.timeline({{ paused: true }});
          tl.to(clock, {{ t: D, duration: D, ease: "none", onUpdate: () => render(clock.t) }}, 0);
          render(0);
          window.__timelines = window.__timelines || {{}};
          window.__timelines["badge"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""

FXC = """<!doctype html>
<html lang="ms">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <div id="root" data-composition-id="fx" data-width="1920" data-height="1080" style="position:absolute;inset:0;pointer-events:none;overflow:hidden">
        <div id="fx-sweep" style="position:absolute;top:-200px;left:0;width:520px;height:1480px;opacity:0;mix-blend-mode:screen;
          background:linear-gradient(90deg,transparent,rgba(200,255,225,.18),rgba(255,255,255,.28),rgba(200,255,225,.18),transparent);transform:skewX(-18deg);filter:blur(6px)"></div>
        <div id="fx-bloom" style="position:absolute;inset:0;opacity:0;background:radial-gradient(60% 60% at 50% 50%,rgba(220,255,235,.35),transparent 70%);mix-blend-mode:screen"></div>
        <div id="fx-grain" style="position:absolute;inset:-60px;background:url(assets/img/grain.png);opacity:.07;mix-blend-mode:overlay"></div>
        <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,transparent 62%,rgba(0,0,0,.28) 100%)"></div>
      </div>
      <script>
        (function () {{
          const tl = gsap.timeline({{ paused: true }});
          const cuts = {cuts};
          cuts.forEach((t) => {{
            tl.fromTo("#fx-sweep", {{ x: -700, opacity: 0.0 }}, {{ x: 2300, opacity: 1, duration: 0.6, ease: "power2.inOut", immediateRender: false }}, t - 0.3);
            tl.to("#fx-sweep", {{ opacity: 0, duration: 0.15 }}, t + 0.3);
          }});
          const g = document.getElementById("fx-grain");
          let k = 0;
          for (let t = 0; t < {D}; t += 1 / 12) {{
            const x = ((k * 73) % 60), y = ((k * 131) % 60);
            tl.set(g, {{ x: -x, y: -y }}, t);
            k++;
          }}
          tl.set({{}}, {{}}, {D});
          window.__timelines = window.__timelines || {{}};
          window.__timelines["fx"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""


INDEX = """<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="vendor/gsap.min.js"></script>
    <script src="vendor/spdfx.js"></script>
    <link rel="stylesheet" href="vendor/spd.css" />
    <style>
{fonts}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #04140e; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #04140e; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1920" data-height="1080">
{mounts}
      <div id="m-fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{D}" data-track-index="7" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <div id="m-badge" data-composition-id="badge" data-composition-src="compositions/badge.html" data-start="0" data-duration="{D}" data-track-index="8" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
{audio}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def write_index(scenes, total, audio_extra=""):
    fonts = open(f"{HF}/assets/fonts/fonts.css").read()
    mounts, audio = [], []
    for n, S in enumerate(scenes):
        mounts.append(f'      <div id="m-{S.id}" data-composition-id="{S.id}" data-composition-src="compositions/{S.id}.html" data-start="{S.start}" '
                      f'data-duration="{S.D}" data-track-index="{1 + n % 2}" data-track-kind="graphics" data-width="1920" data-height="1080"></div>')
        for k, (ln, at) in enumerate(S.lines):
            if ln.real and os.environ.get("SPD_VO"):
                audio.append(f'      <audio id="vo-{ln.id}" src="assets/vo/{ln.id}.mp3" data-start="{round(S.start + at, 3)}" data-duration="{ln.dur:.3f}" '
                             f'data-track-index="{20 + k % 2}" data-volume="1" data-fade-out="0.12"></audio>')
    open(f"{HF}/compositions/badge.html", "w").write(BADGE.format(D=total))
    cuts = [S.start + 0.3 for S in scenes[1:] if S.id not in ("s05", "s13")]  # scenes with their own flash/ball/slam skip the sweep
    open(f"{HF}/compositions/fx.html", "w").write(FXC.format(D=total, cuts=json.dumps(cuts)))
    open(f"{HF}/index.html", "w").write(INDEX.format(fonts=fonts, D=total, mounts="\n".join(mounts), audio="\n".join(audio) + audio_extra))


def dialogue(scenes):
    s01 = next(S for S in scenes if S.id == "s01")
    return (f'\n      <audio id="dlg-s01" src="assets/vo/dlg_s01.wav" data-start="{round(s01.start + CUTS[-1], 3)}" data-duration="5.2" '
            f'data-track-index="22" data-volume="1" data-fade-in="0.08" data-fade-out="0.2"></audio>')


if __name__ == "__main__":
    only = sys.argv[1:] or None
    scenes, total = build(only)
    write_index(scenes, total)
    for S in scenes:
        est = [ln.id for ln, _ in S.lines if not ln.real]
        print(f"{S.id} {S.start:7.2f} +{S.D:6.2f}  {'EST ' + ','.join(est) if est else ''}")
    print("total", total)
    json.dump([{"id": S.id, "start": S.start, "dur": S.D, "vo": [(ln.id, round(S.start + at, 3), ln.real) for ln, at in S.lines]} for S in scenes],
              open(f"{ROOT}/edits/spd-green/plan.json", "w"), indent=1)
