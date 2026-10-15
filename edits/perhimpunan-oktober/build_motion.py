"""Add motion-graphic elements, entrance animations and transitions to the
MCORP monthly-assembly deck.

    python3 build_motion.py <unpacked_dir>

Edits ppt/slides/slideN.xml in place. Two kinds of slide:
  * poster slides (one full-bleed image): slow Ken Burns zoom, light streaks,
    floating sparkles and a periodic shine sweep.
  * segment slides (speaker photo + title): spinning halo rings and a pulsing
    glow behind the speaker, light streaks, particles, an "ATURCARA 0N" tag
    and a staged entrance for photo, title, name and the logo strip.
"""
import random
import re
import sys
from pathlib import Path

EMU = 914400
SLIDE_W, SLIDE_H = 20.0, 11.25  # inches

NAVY = "182F55"
RED = "D7263D"
GOLD = "F6C445"
GOLD_LIGHT = "FFE38A"


def emu(v):
    return int(round(v * EMU))


class Ids:
    def __init__(self, start):
        self.n = start

    def __call__(self):
        self.n += 1
        return self.n


# --------------------------------------------------------------- shapes ----

def sp(sid, name, x, y, w, h, geom, fill, ln="<a:ln><a:noFill/></a:ln>", rot=0,
       effect="", txbody=""):
    rot_attr = f' rot="{int(rot * 60000) % 21600000}"' if rot else ""
    body = txbody or (
        '<p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/>'
        '<a:p><a:endParaRPr lang="en-US"/></a:p></p:txBody>')
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm{rot_attr}><a:off x="{emu(x)}" y="{emu(y)}"/>'
        f'<a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
        f'<a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>{fill}{ln}{effect}</p:spPr>'
        f'{body}</p:sp>')


def solid(color, alpha=100):
    a = f'<a:alpha val="{alpha * 1000}"/>' if alpha < 100 else ""
    return f'<a:solidFill><a:srgbClr val="{color}">{a}</a:srgbClr></a:solidFill>'


def grad_lin(stops, ang=0):
    gs = "".join(
        f'<a:gs pos="{p * 1000}"><a:srgbClr val="{c}"><a:alpha val="{a * 1000}"/></a:srgbClr></a:gs>'
        for p, c, a in stops)
    return f'<a:gradFill rotWithShape="1"><a:gsLst>{gs}</a:gsLst><a:lin ang="{ang * 60000}" scaled="0"/></a:gradFill>'


def grad_radial(stops):
    gs = "".join(
        f'<a:gs pos="{p * 1000}"><a:srgbClr val="{c}"><a:alpha val="{a * 1000}"/></a:srgbClr></a:gs>'
        for p, c, a in stops)
    return (f'<a:gradFill rotWithShape="1"><a:gsLst>{gs}</a:gsLst>'
            '<a:path path="circle"><a:fillToRect l="50000" t="50000" r="50000" b="50000"/></a:path>'
            '</a:gradFill>')


def ring_line(color, width_pt, dash, alpha=100):
    a = f'<a:alpha val="{alpha * 1000}"/>' if alpha < 100 else ""
    return (f'<a:ln w="{int(width_pt * 12700)}" cap="rnd"><a:solidFill><a:srgbClr val="{color}">{a}'
            f'</a:srgbClr></a:solidFill><a:prstDash val="{dash}"/><a:round/></a:ln>')


def glow(color, rad_pt, alpha):
    return (f'<a:effectLst><a:glow rad="{int(rad_pt * 12700)}"><a:srgbClr val="{color}">'
            f'<a:alpha val="{alpha * 1000}"/></a:srgbClr></a:glow></a:effectLst>')


# ----------------------------------------------------------- animations ----

class Timeline:
    """Collects effects that all start automatically when the slide opens."""

    def __init__(self):
        self.n = 4  # 1 root, 2 main sequence, 3 click group, 4 inner group
        self.effects = []
        self.build = {}  # spid -> has text

    def id(self):
        self.n += 1
        return self.n

    def _tgt(self, spid):
        return f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'

    def _effect(self, spid, preset, cls, sub, delay, children, extra="", text=False):
        self.build.setdefault(spid, text)
        self.effects.append(
            f'<p:par><p:cTn id="{self.id()}" presetID="{preset}" presetClass="{cls}" '
            f'presetSubtype="{sub}"{extra} fill="hold" nodeType="withEffect">'
            f'<p:stCondLst><p:cond delay="{delay}"/></p:stCondLst>'
            f'<p:childTnLst>{children}</p:childTnLst></p:cTn></p:par>')

    def _show(self, spid):
        return (f'<p:set><p:cBhvr><p:cTn id="{self.id()}" dur="1" fill="hold">'
                f'<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>{self._tgt(spid)}'
                '<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
                '</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>')

    def _anim(self, spid, attr, frm, to, dur, ease=""):
        return (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr additive="base">'
                f'<p:cTn id="{self.id()}" dur="{dur}" fill="hold"{ease}/>{self._tgt(spid)}'
                f'<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst></p:cBhvr>'
                f'<p:tavLst><p:tav tm="0"><p:val><p:strVal val="{frm}"/></p:val></p:tav>'
                f'<p:tav tm="100000"><p:val><p:strVal val="{to}"/></p:val></p:tav></p:tavLst></p:anim>')

    def _fade(self, spid, dur):
        return (f'<p:animEffect transition="in" filter="fade"><p:cBhvr>'
                f'<p:cTn id="{self.id()}" dur="{dur}"/>{self._tgt(spid)}</p:cBhvr></p:animEffect>')

    # entrance -------------------------------------------------------------
    def fade_in(self, spid, delay, dur=500, text=False):
        self._effect(spid, 10, "entr", 0, delay, self._show(spid) + self._fade(spid, dur), text=text)

    def float_in(self, spid, delay, dx=0.0, dy=0.0, dur=800, text=False):
        """Fade in while sliding from an offset (fractions of the slide)."""
        ease = ' decel="100000"'
        kids = self._show(spid) + self._fade(spid, dur)
        kids += self._anim(spid, "ppt_x", f"#ppt_x{dx:+.3f}", "#ppt_x", dur, ease)
        kids += self._anim(spid, "ppt_y", f"#ppt_y{dy:+.3f}", "#ppt_y", dur, ease)
        self._effect(spid, 42, "entr", 0, delay, kids, text=text)

    def zoom_in(self, spid, delay, dur=600, text=False):
        ease = ' decel="100000"'
        kids = self._show(spid) + self._fade(spid, dur)
        kids += self._anim(spid, "ppt_w", "#ppt_w*0.3", "#ppt_w", dur, ease)
        kids += self._anim(spid, "ppt_h", "#ppt_h*0.3", "#ppt_h", dur, ease)
        self._effect(spid, 53, "entr", 16, delay, kids, text=text)

    def wipe_in(self, spid, delay, dur=500, text=False):
        kids = self._show(spid) + (
            f'<p:animEffect transition="in" filter="wipe(left)"><p:cBhvr>'
            f'<p:cTn id="{self.id()}" dur="{dur}"/>{self._tgt(spid)}</p:cBhvr></p:animEffect>')
        self._effect(spid, 22, "entr", 8, delay, kids, text=text)

    # emphasis / loops -----------------------------------------------------
    def spin(self, spid, delay, period, clockwise=True):
        by = 21600000 if clockwise else -21600000
        kids = (f'<p:animRot by="{by}"><p:cBhvr><p:cTn id="{self.id()}" dur="{period}" fill="hold"/>'
                f'{self._tgt(spid)}<p:attrNameLst><p:attrName>r</p:attrName></p:attrNameLst>'
                '</p:cBhvr></p:animRot>')
        self._effect(spid, 8, "emph", 0, delay, kids, extra=' repeatCount="indefinite"')

    def breathe(self, spid, delay, period, pct=106):
        """Grow/Shrink that reverses forever: Ken Burns or a pulse."""
        kids = (f'<p:animScale><p:cBhvr><p:cTn id="{self.id()}" dur="{period}" fill="hold"/>'
                f'{self._tgt(spid)}</p:cBhvr><p:by x="{pct * 1000}" y="{pct * 1000}"/></p:animScale>')
        self._effect(spid, 6, "emph", 0, delay, kids,
                     extra=' repeatCount="indefinite" autoRev="1"')

    def path(self, spid, delay, dx_in, dy_in, dur, autorev=False, accel=False):
        """Looping straight motion path; offsets given in inches."""
        dx, dy = dx_in / SLIDE_W, dy_in / SLIDE_H
        ease = ' accel="50000" decel="50000"' if accel else ""
        kids = (f'<p:animMotion origin="layout" path="M 0 0 L {dx:.4f} {dy:.4f} E" '
                f'pathEditMode="relative" ptsTypes="AA"><p:cBhvr>'
                f'<p:cTn id="{self.id()}" dur="{dur}" fill="hold"{ease}/>{self._tgt(spid)}'
                '<p:attrNameLst><p:attrName>ppt_x</p:attrName><p:attrName>ppt_y</p:attrName>'
                '</p:attrNameLst></p:cBhvr></p:animMotion>')
        extra = ' repeatCount="indefinite"' + (' autoRev="1"' if autorev else "")
        self._effect(spid, 0, "path", 0, delay, kids, extra=extra)

    def xml(self):
        bg_attr = ' animBg="1"'
        bld = "".join(
            f'<p:bldP spid="{s}" grpId="0"{"" if t else bg_attr}/>'
            for s, t in self.build.items())
        return (
            '<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
            '<p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq">'
            '<p:childTnLst><p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>'
            '<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
            '<p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            + "".join(self.effects) +
            '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn>'
            '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
            '</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>'
            f'<p:bldLst>{bld}</p:bldLst></p:timing>')


# ---------------------------------------------------------- transitions ----

def transition(p14_xml, fallback, dur_ms):
    return (
        '<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
        '<mc:Choice xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" Requires="p14">'
        f'<p:transition spd="slow" p14:dur="{dur_ms}">{p14_xml}</p:transition></mc:Choice>'
        f'<mc:Fallback><p:transition spd="slow">{fallback}</p:transition></mc:Fallback>'
        '</mc:AlternateContent>')


T_OPEN = transition('<p:fade thruBlk="1"/>', '<p:fade thruBlk="1"/>', 1500)
T_POSTER = transition('<p14:gallery dir="l"/>', "<p:fade/>", 1600)
T_SEGMENT = transition('<p14:flythrough hasBounce="1"/>', "<p:zoom/>", 1200)


# -------------------------------------------------------- shared pieces ----

def streak(ids, tl, name, start, end, length, thick, delay, travel_ms, gap_factor, front_alpha=95):
    """A glowing gold streak that shoots along start->end, then waits off-slide.

    The path is stretched by gap_factor so the visible crossing takes
    travel_ms and the rest of each loop is spent off the slide.
    """
    import math
    (x0, y0), (x1, y1) = start, end
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    sid = ids()
    shape = sp(sid, name, x0 - length / 2, y0 - thick / 2, length, thick, "roundRect",
               grad_lin([(0, GOLD_LIGHT, 0), (70, "FFFFFF", front_alpha), (100, GOLD_LIGHT, 0)]),
               rot=ang, effect=glow(GOLD, 6, 55))
    dx, dy = (x1 - x0) * gap_factor, (y1 - y0) * gap_factor
    tl.path(sid, delay, dx, dy, int(travel_ms * gap_factor))
    return shape


def particles(ids, tl, rng, boxes, count, colors):
    out = []
    for i in range(count):
        bx, by, bw, bh = boxes[i % len(boxes)]
        d = rng.uniform(0.08, 0.22)
        x, y = bx + rng.uniform(0, bw), by + rng.uniform(0, bh)
        color, alpha = colors[i % len(colors)]
        sid = ids()
        out.append(sp(sid, f"Particle {i + 1}", x, y, d, d, "ellipse", solid(color, alpha),
                      effect=glow(color, 3, 35)))
        tl.fade_in(sid, 400 + i * 120, 800)
        tl.path(sid, 400 + i * 120, rng.uniform(-0.6, 0.6), -rng.uniform(0.4, 1.1),
                rng.randint(2600, 4800), autorev=True, accel=True)
    return out


def shine(ids, tl, delay, travel_ms=2200, gap_factor=3.2, alpha=45):
    """Tall translucent band that sweeps left to right across the whole slide."""
    sid = ids()
    shape = sp(sid, "Shine Sweep", -4.0, -2.5, 2.6, 16.0, "rect",
               grad_lin([(0, "FFFFFF", 0), (50, "FFFFFF", alpha), (100, "FFFFFF", 0)], ang=0),
               rot=18)
    tl.path(sid, delay, 28.0 * gap_factor, 0.0, int(travel_ms * gap_factor))
    return shape


# --------------------------------------------------------------- slides ----

def shape_ids(xml):
    body = xml.split("</p:grpSpPr>", 1)[1]
    # top-level children only: skip ids that live inside a group
    out, depth, pos = [], 0, 0
    for m in re.finditer(r"<p:grpSp>|</p:grpSp>|<p:cNvPr id=\"(\d+)\" name=\"([^\"]*)\"", body):
        tok = m.group(0)
        if tok == "<p:grpSp>":
            depth += 1
            if depth == 1:
                pos = len(out)
            continue
        if tok == "</p:grpSp>":
            depth -= 1
            continue
        if depth == 0 or (depth == 1 and len(out) == pos):
            out.append((int(m.group(1)), m.group(2)))
    return out


def insert_after_first_shape(xml, fragment):
    i = xml.index("</p:sp>") + len("</p:sp>")
    return xml[:i] + fragment + xml[i:]


def insert_at_end(xml, fragment):
    i = xml.index("</p:spTree>")
    return xml[:i] + fragment + xml[i:]


def add_timing_and_transition(xml, tl, trans):
    xml = re.sub(r"<p:transition.*?</p:transition>|<mc:AlternateContent.*?</mc:AlternateContent>",
                 "", xml, flags=re.S)
    xml = re.sub(r"<p:timing>.*?</p:timing>", "", xml, flags=re.S)
    i = xml.index("</p:clrMapOvr>") + len("</p:clrMapOvr>")
    return xml[:i] + trans + tl.xml() + xml[i:]


def poster_slide(xml, seed, opening):
    rng = random.Random(seed)
    ids = Ids(100)
    tl = Timeline()
    bg = shape_ids(xml)[0][0]
    tl.breathe(bg, 0, 9000, 105)  # Ken Burns

    front = [
        streak(ids, tl, "Light Streak 1", (-3.0, 3.6), (11.0, -2.5), 4.5, 0.07, 600, 1400, 2.6),
        streak(ids, tl, "Light Streak 2", (8.0, 14.5), (24.0, 4.0), 5.0, 0.08, 1500, 1600, 2.2),
        streak(ids, tl, "Light Streak 3", (11.0, 14.0), (25.0, 6.5), 3.5, 0.05, 3200, 1500, 2.4),
    ]
    front += particles(ids, tl, rng, [(0.6, 0.4, 5.5, 2.2), (12.2, 0.4, 2.5, 3.0), (0.6, 7.6, 6.0, 1.3)],
                       12, [(GOLD, 85), (RED, 60), ("FFFFFF", 90), (NAVY, 50)])
    front.append(shine(ids, tl, 2500 if opening else 900))
    xml = insert_at_end(xml, "".join(front))
    return add_timing_and_transition(xml, tl, T_OPEN if opening else T_POSTER)


def segment_slide(xml, number, center, seed):
    rng = random.Random(seed)
    ids = Ids(100)
    tl = Timeline()
    top = shape_ids(xml)
    bg = top[0][0]
    texts = [(i, n) for i, n in top if n.startswith("TextBox")]
    title_id, name_id = texts[0][0], texts[1][0]
    role_id = texts[2][0] if len(texts) > 2 else None

    title_xfrm = re.search(
        rf'<p:cNvPr id="{title_id}" .*?<a:off x="(\d+)" y="(\d+)"/>', xml, re.S)
    tx, ty = int(title_xfrm.group(1)) / EMU, int(title_xfrm.group(2)) / EMU

    # classify the remaining top-level shapes by what they are
    photo = band = None
    logos, group = [], None
    for sid, name in top[1:]:
        if name.startswith("TextBox"):
            continue
        if name.startswith("Group"):
            group = sid
            continue
        m = re.search(rf'<p:cNvPr id="{sid}" name="[^"]*"/>.*?<a:off x="(-?\d+)" y="(-?\d+)"/>'
                      rf'<a:ext cx="(\d+)" cy="(\d+)"/>', xml, re.S)
        x, y, w, h = (int(v) / EMU for v in m.groups())
        if h > 6:
            photo = sid
        elif w > 15:
            band = sid
        elif y > 9 or y < 2.5:
            logos.append((x, sid))

    # --- behind the speaker: glow + three halo rings + streaks -------------
    cx, cy = center
    behind = []
    gid = ids()
    behind.append(sp(gid, "Halo Glow", cx - 4.3, cy - 4.3, 8.6, 8.6, "ellipse",
                     grad_radial([(0, GOLD_LIGHT, 70), (45, GOLD, 30), (100, GOLD, 0)])))
    tl.zoom_in(gid, 0, 900)
    tl.breathe(gid, 900, 2400, 110)

    for k, (d, color, wpt, dash, alpha, period, cw) in enumerate([
            (7.6, RED, 3, "sysDash", 85, 26000, False),
            (6.6, GOLD, 7, "lgDash", 100, 18000, True),
            (5.6, NAVY, 2, "dash", 55, 12000, False)]):
        rid = ids()
        behind.append(sp(rid, f"Halo Ring {k + 1}", cx - d / 2, cy - d / 2, d, d, "ellipse",
                         "<a:noFill/>", ln=ring_line(color, wpt, dash, alpha)))
        tl.zoom_in(rid, 150 + k * 150, 800)
        tl.spin(rid, 150 + k * 150, period, cw)

    behind += [
        streak(ids, tl, "Light Streak 1", (4.0, 14.0), (28.0, -1.0), 4.0, 0.07, 1200, 1700, 2.0),
        streak(ids, tl, "Light Streak 2", (2.0, 11.5), (26.0, -3.5), 3.0, 0.05, 2400, 1900, 2.3),
        streak(ids, tl, "Light Streak 3", (6.0, 16.5), (30.0, 1.5), 5.0, 0.08, 3600, 1600, 2.1),
    ]
    xml = insert_after_first_shape(xml, "".join(behind))

    # --- in front: "ATURCARA 0N" tag, particles, one shine sweep ------------
    front = []
    pill = ids()
    pill_txt = (
        '<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>'
        '<a:lstStyle/><a:p><a:pPr algn="ctr"/><a:r><a:rPr lang="ms-MY" sz="2000" b="1" spc="400">'
        '<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:latin typeface="Montserrat Bold"/>'
        '<a:cs typeface="Montserrat Bold"/></a:rPr>'
        f'<a:t>ATURCARA {number:02d}</a:t></a:r></a:p></p:txBody>')
    front.append(sp(pill, "Aturcara Tag", tx, ty - 0.95, 3.6, 0.62, "roundRect",
                    grad_lin([(0, RED, 100), (100, "9E1528", 100)], ang=0),
                    effect='<a:effectLst><a:outerShdw blurRad="152400" dist="38100" dir="5400000" '
                           'algn="t" rotWithShape="0"><a:srgbClr val="9E1528"><a:alpha val="40000"/>'
                           '</a:srgbClr></a:outerShdw></a:effectLst>',
                    txbody=pill_txt))
    front += particles(ids, tl, rng, [(0.8, 0.6, 9.0, 1.6), (0.8, 7.3, 9.0, 1.6), (cx - 4.5, 1.0, 9.0, 1.2)],
                       12, [(GOLD, 90), (RED, 70), (NAVY, 55)])
    front.append(shine(ids, tl, 2600, travel_ms=1600, gap_factor=4.0, alpha=55))
    xml = insert_at_end(xml, "".join(front))

    # --- staged entrance of the original content --------------------------
    tl.breathe(bg, 0, 12000, 104)
    tl.float_in(photo, 250, dx=0.18, dur=1000)
    tl.wipe_in(pill, 750, 550, text=True)
    tl.float_in(title_id, 900, dx=-0.08, dur=800, text=True)
    tl.float_in(name_id, 1300, dy=0.05, dur=700, text=True)
    if role_id:
        tl.fade_in(role_id, 1650, 600, text=True)
    if band:
        tl.float_in(band, 300, dy=0.15, dur=700)
    if group:
        tl.zoom_in(group, 800, 700)
    for k, (_, sid) in enumerate(sorted(logos)):
        tl.zoom_in(sid, 800 + k * 70, 450)

    return add_timing_and_transition(xml, tl, T_SEGMENT)


SEGMENTS = {  # slide -> (agenda number, centre of the speaker's halo in inches)
    3: (1, (15.35, 4.9)),
    5: (2, (15.25, 5.2)),
    8: (3, (15.05, 5.2)),
    10: (4, (15.10, 5.3)),
}


def main(root):
    slides = Path(root) / "ppt" / "slides"
    for n in range(1, 12):
        f = slides / f"slide{n}.xml"
        xml = f.read_text(encoding="utf-8")
        if n in SEGMENTS:
            num, center = SEGMENTS[n]
            xml = segment_slide(xml, num, center, seed=n)
        else:
            xml = poster_slide(xml, seed=n, opening=(n == 1))
        f.write_text(xml, encoding="utf-8")
        print(f"slide{n}: {'segment' if n in SEGMENTS else 'poster'}")


if __name__ == "__main__":
    main(sys.argv[1])
