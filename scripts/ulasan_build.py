"""Build the MCORP Estimate user-testimonial video (edits/mcorp-ulasan/hf).

Generates index.html, compositions/fx.html (from edits/mcorp-ulasan/fx.tpl.html),
compositions/captions.html and compositions/badge.html.
All times below are seconds; src times come from media/sistem-full/transcripts.
"""
import json
import re

ROOT = "/home/user/AI-IZZUL"
HF = f"{ROOT}/edits/mcorp-ulasan/hf"

# (name, source, src_in, src_out) -- cut points checked on the cleaned audio
# order: title card -> Puan Rahimah -> YB Datuk -> outro
CLIPS = [
    ("RI", "rahimah3", 7.93, 11.92),
    ("RM", "rahimah3", 16.88, 37.02),
    ("H", "helmy3", 0.55, 28.40),
    ("C", "helmy3", 28.70, 31.95),
    ("D", "helmy3", 37.80, 51.40),
]
TITLE_LEN = 3.0
OUTRO_LEN = 4.0

T0 = {}
t = TITLE_LEN
for name, src, a, b in CLIPS:
    T0[name] = round(t, 3)
    t += b - a
OUT0 = round(t, 3)
TOTAL = round(OUT0 + OUTRO_LEN, 3)
CLIP = {c[0]: c for c in CLIPS}


def at(name, src_t):
    """root time of a source timestamp inside clip `name`"""
    return round(T0[name] + src_t - CLIP[name][2], 3)


T = {
    "TTL1": TITLE_LEN, "RI0": T0["RI"], "RM0": T0["RM"], "H0": T0["H"], "C0": T0["C"], "D0": T0["D"], "OUT0": OUT0,
    # Puan Rahimah
    "RM500": at("RM", 20.94), "BR1": at("RM", 23.67), "TIADA": at("RM", 25.08), "BR1_OUT": at("RM", 26.70),
    "CH2": at("RM", 26.82), "GALAK": at("RM", 28.64), "BR2": at("RM", 30.25), "BR2_OUT": at("RM", 33.85),
    "NET": at("RM", 34.64),
    # YB Datuk
    "CHIP1": at("H", 4.22), "CHIP2": at("H", 5.02), "CHIP3": at("H", 5.60), "PERTIKAI": at("H", 6.76),
    "RM50": at("H", 7.72), "RM20": at("H", 9.60), "Q_OUT": at("H", 11.05),
    "TEN": at("H", 15.22), "TEN_OUT": at("H", 17.55),
    "CH4": at("H", 19.30), "BQ_IN": at("H", 20.62), "MAHAL": at("H", 24.28), "MURAH": at("H", 25.26),
    "BQ_OUT": round(T0["C"] - 0.27, 3),
    "PQ1": at("C", 29.10), "PQ2": at("C", 30.0), "PQ3": at("C", 30.5),
    "TECH1": at("D", 42.32), "TECH2": at("D", 44.24), "SALING": at("D", 45.00),
    "BR3": at("D", 45.60), "BR3_OUT": at("D", 47.30), "MANFAAT": at("D", 47.42), "MELUAS": at("D", 49.90),
}

FACE_H = "56% 30%"
FACE_R = "52% 30%"
LEFT_FREE_H = "0% 32%"   # pushes YB to the right third, frees the left for graphics
RIGHT_FREE_R = "100% 30%"  # pushes Puan Rahimah left, frees the right


# camera moves per clip: (clip, t_from, t_to, scale_from, scale_to, origin)
def shots():
    S = []
    S += [("RI", T["RI0"], T["RM0"], 1.0, 1.06, FACE_R)]
    r1 = T["RM500"] - 0.4
    S += [("RM", T["RM0"], r1, 1.15, 1.19, FACE_R), ("RM", r1, T["BR1"], 1.22, 1.26, RIGHT_FREE_R),
          ("RM", T["BR1"], T["CH2"], 1.0, 1.03, FACE_R), ("RM", T["CH2"], T["BR2"], 1.12, 1.17, FACE_R),
          ("RM", T["BR2"], T["NET"] - 0.3, 1.0, 1.03, FACE_R), ("RM", T["NET"] - 0.3, T["H0"], 1.18, 1.24, FACE_R)]
    h = lambda x: at("H", x)
    bq = T["BQ_IN"]
    S += [("H", T["H0"], h(2.98), 1.0, 1.04, FACE_H), ("H", h(2.98), h(5.92), 1.2, 1.25, LEFT_FREE_H),
          ("H", h(5.92), h(7.37), 1.0, 1.03, FACE_H),
          ("H", h(7.37), h(9.30), 1.30, 1.36, FACE_H), ("H", h(9.30), h(11.20), 1.5, 1.56, FACE_H),
          ("H", h(11.20), h(12.78), 1.18, 1.22, FACE_H), ("H", h(12.78), h(14.50), 1.0, 1.03, FACE_H),
          ("H", h(14.50), h(17.70), 1.22, 1.28, LEFT_FREE_H), ("H", h(17.70), T["CH4"], 1.0, 1.03, FACE_H),
          ("H", T["CH4"], bq, 1.2, 1.23, FACE_H), ("H", bq, T["C0"], 1.28, 1.33, LEFT_FREE_H)]
    S += [("C", T["C0"], T["D0"], 1.38, 1.47, LEFT_FREE_H)]
    d1 = at("D", 41.82)
    S += [("D", T["D0"], d1, 1.0, 1.04, FACE_H), ("D", d1, T["BR3"], 1.22, 1.26, LEFT_FREE_H),
          ("D", T["BR3"], T["MANFAAT"] - 0.1, 1.0, 1.02, FACE_H), ("D", T["MANFAAT"] - 0.1, T["MELUAS"] - 0.1, 1.25, 1.29, LEFT_FREE_H),
          ("D", T["MELUAS"] - 0.1, T["OUT0"], 1.4, 1.46, LEFT_FREE_H)]
    return S


# b-roll cutaways (dialogue keeps running underneath)
BROLL = [
    ("ttl", "rahimah2", 0.0, TITLE_LEN, 4.0),
    ("br1", "rahimah1", T["BR1"], T["BR1_OUT"] - T["BR1"], 1.2),
    ("br2", "rahimah2", T["BR2"], T["BR2_OUT"] - T["BR2"], 7.0),
    ("br3", "helmy1", T["BR3"], T["BR3_OUT"] - T["BR3"], 2.5),
]

SFX = [
    (0.15, "whoosh-cinematic", 0.4), (0.33, "impact-bass-2", 0.55), (0.58, "impact-bass-1", 0.4), (1.1, "sparkle", 0.3),
    (T["RI0"] - 0.2, "whoosh", 0.45),
    (T["RM500"] - 0.38, "whoosh-short", 0.35), (T["RM500"] + 0.8, "notification", 0.25),
    (T["BR1"] - 0.05, "whoosh-short", 0.3), (T["TIADA"] + 0.18, "chime", 0.3),
    (T["CH2"] - 0.05, "whoosh-short", 0.35), (T["GALAK"] - 0.05, "impact-bass-2", 0.45),
    (T["BR2"] - 0.05, "whoosh-short", 0.3),
    (T["H0"] - 0.22, "whoosh", 0.5),
    (T["CHIP1"] - 0.02, "pop", 0.3), (T["CHIP2"] - 0.02, "pop", 0.3), (T["CHIP3"] - 0.02, "pop", 0.3),
    (T["PERTIKAI"] - 0.05, "impact-bass-1", 0.4),
    (T["RM50"] - 0.1, "pop", 0.35), (T["RM20"] - 0.1, "pop", 0.35), (T["Q_OUT"] - 0.1, "whoosh-short", 0.3),
    (T["TEN"] - 0.22, "whoosh-short", 0.35), (T["TEN"] - 0.1, "typing", 0.22),
    (T["CH4"] - 0.05, "whoosh-short", 0.35), (T["BQ_IN"] - 0.05, "whoosh", 0.4),
    (T["MAHAL"] - 0.02, "ping", 0.3), (T["MURAH"] - 0.02, "ping", 0.3),
    (T["C0"] - 0.1, "whoosh-cinematic", 0.3), (T["PQ2"] - 0.02, "impact-bass-1", 0.3), (T["PQ3"] - 0.02, "impact-bass-2", 0.3),
    (T["D0"] - 0.12, "whoosh", 0.4),
    (T["TECH1"] - 0.02, "pop", 0.3), (T["TECH2"] - 0.02, "pop", 0.3), (T["SALING"] - 0.1, "chime", 0.25),
    (T["BR3"] - 0.05, "whoosh-short", 0.3),
    (T["MANFAAT"] - 0.05, "impact-bass-1", 0.3), (T["MANFAAT"] + 0.1, "sparkle", 0.35),
    (T["MELUAS"] - 0.05, "whoosh-cinematic", 0.3),
    (T["OUT0"] - 0.3, "whoosh", 0.5), (T["OUT0"] + 1.1, "chime", 0.35),
]
SFX_LEN = {"chime": 2.544, "click": 0.366, "glitch-1": 2.638, "impact-bass-1": 2.116, "impact-bass-2": 2.592,
           "key-press": 0.432, "notification": 2.456, "ping": 1.32, "pop": 0.72, "riser": 10.032, "sparkle": 1.802,
           "typing": 1.541, "whoosh-cinematic": 5.544, "whoosh-short": 0.575, "whoosh": 0.575}

# ---------------------------------------------------------------- captions
FIX = {"petikai": "pertikai", "Bintik": "binti"}
DROP = {"So", "Ok,", "Ok"}
KEY = {"RM50,000", "RM20,000", "FAHAM", "PERTIKAI", "10", "KALI", "TERIMA", "MAHAL", "MURAH", "RM500,000", "TEKNIKAL",
       "MEMBANTU", "MENGGALAKKAN", "AGENSI-AGENSI", "BERMANFAAT", "MELUAS", "SALAH", "PECAHAN-PECAHAN"}
NO_CAPS = {"C"}  # the pull-quote already spells these words out


def words_for(name):
    """words of clip `name` grouped by whisper segment (phrase), mapped to root time"""
    _, src, a, b = CLIP[name]
    d = json.load(open(f"{ROOT}/media/sistem-full/transcripts/{src}.json"))
    groups = []
    for s in d["segments"]:
        out = []
        for w in s["words"]:
            txt = w["word"].strip()
            if w["start"] < a - 0.05 or w["end"] > b + 0.1:
                continue
            if (txt.startswith("-") or txt.startswith(",")) and out:
                out[-1]["w"] += txt
                out[-1]["e"] = at(name, w["end"])
                continue
            if txt in DROP:
                continue
            core = txt.rstrip(",.?")
            txt = FIX.get(core, core) + txt[len(core):]
            out.append({"w": txt, "s": at(name, w["start"]), "e": at(name, w["end"])})
        if out:
            groups.append(out)
    return groups


def pages():
    import math
    P = []
    for name, *_ in CLIPS:
        if name in NO_CAPS:
            continue
        for g in words_for(name):
            chars = sum(len(x["w"]) + 1 for x in g)
            k = max(math.ceil(len(g) / 4), math.ceil(chars / 24))
            # split as evenly as possible so no page is left with a lone word
            base, extra = divmod(len(g), k)
            i = 0
            for j in range(k):
                n = base + (1 if j < extra else 0)
                P.append(g[i:i + n])
                i += n
    cues = []
    for i, p in enumerate(P):
        s = max(0.0, p[0]["s"] - 0.06)
        e = p[-1]["e"] + 0.3
        if i + 1 < len(P):
            e = min(e, P[i + 1][0]["s"] - 0.06)
        words = []
        for w in p:
            clean = w["w"].rstrip(",.").upper()
            words.append({"w": clean, "s": round(w["s"], 3), "k": 1 if clean.rstrip("?") in KEY else 0})
        cues.append({"s": round(s, 3), "e": round(e, 3), "words": words})
    return cues


# ---------------------------------------------------------------- html
def build_index():
    L = []
    L.append(f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="vendor/gsap.min.js"></script>
    <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #07080d;
      }}
      #root {{
        position: relative;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #07080d;
      }}
      .vw {{
        position: absolute;
        inset: 0;
        overflow: hidden;
      }}
      .vw video {{
        position: absolute;
        inset: 0;
        width: 1920px;
        height: 1080px;
        object-fit: cover;
      }}
      .br {{
        position: absolute;
        inset: 0;
      }}
      .br video {{
        position: absolute;
        inset: 0;
        width: 1920px;
        height: 1080px;
        object-fit: cover;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
      <!-- interview cuts (see edits/mcorp-ulasan/NOTES.md) -->""")
    for ci, (name, src, a, b) in enumerate(CLIPS):
        L.append(f'      <div id="w-{name}" class="vw" data-layout-allow-overflow><video id="v-{name}" class="clip" data-hf-media-start-basis="local" '
                 f'src="assets/video/{src}.mp4" data-start="{T0[name]}" data-duration="{round(b - a, 3)}" data-media-start="{a}" '
                 f'data-track-index="{ci % 2}" data-fade-in="0.04" data-fade-out="0.06" playsinline data-has-audio="true"></video></div>')
    L.append("      <!-- b-roll cutaways, muted -->")
    for bid, src, s, d, ms in BROLL:
        L.append(f'      <div id="b-{bid}" class="br" data-layout-allow-overflow><video id="bv-{bid}" class="clip" data-hf-media-start-basis="local" '
                 f'src="assets/video/{src}.mp4" data-start="{round(s, 3)}" data-duration="{round(d, 3)}" data-media-start="{ms}" '
                 f'data-track-index="2" muted playsinline></video></div>')
    L.append(f'      <div id="m-fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1920" data-height="1080"></div>')
    L.append(f'      <div id="m-badge" data-composition-id="badge" data-composition-src="compositions/badge.html" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-track-kind="graphics" data-width="1920" data-height="1080"></div>')
    L.append(f'      <div id="m-captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-track-kind="captions" data-width="1920" data-height="1080"></div>')
    # music: low under speech, up for the title card and outro
    lo, hi = 0.15, 0.6
    pts = [(0, 0), (0.12, hi), (T["RI0"] - 0.1, hi), (T["RI0"] + 0.15, lo),
           (OUT0 - 0.3, lo), (OUT0 + 0.2, hi), (TOTAL - 1.2, hi), (TOTAL, 0)]
    auto = {"version": 1, "lanes": [{"target": "volume", "points": [{"t": round(a, 3), "v": v} for a, v in pts]}]}
    L.append("      <!-- music bed -->")
    L.append(f"""      <audio id="bgm" data-timeline-role="music" src="assets/bgm/bed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-automation='{json.dumps(auto, separators=(",", ":"))}'></audio>""")
    L.append("      <!-- sfx -->")
    ends = []
    for i, (s, f, v) in enumerate(sorted(SFX)):
        s = max(0, round(s, 3))
        d = SFX_LEN[f]
        tr = next((k for k, e in enumerate(ends) if e <= s), None)
        if tr is None:
            ends.append(0)
            tr = len(ends) - 1
        ends[tr] = s + d
        L.append(f'      <audio id="s{i:02d}" src="assets/sfx/{f}.mp3" data-start="{s}" data-duration="{d}" data-track-index="{30 + tr}" data-volume="{v}"></audio>')
    # camera moves
    js = []
    for clip, a, b, s0, s1, o in shots():
        js.append(f'          tl.fromTo("#w-{clip}", {{ scale: {s0}, transformOrigin: "{o}" }}, {{ scale: {s1}, duration: {round(b - a - 0.002, 3)}, ease: "none", immediateRender: false }}, {round(a, 3)});')
    for bid, src, s, d, ms in BROLL:
        js.append(f'          tl.fromTo("#b-{bid}", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {round(d, 3)}, ease: "none", immediateRender: false }}, {round(s, 3)});')
    L.append("""    </div>
    <script>
      (function () {
        const tl = gsap.timeline({ paused: true });
        // hard jump-cut punch-ins at sentence breaks, slow drift inside each shot
""" + "\n".join(x[2:] for x in js) + """
        window.__timelines = window.__timelines || {};
        window.__timelines["main"] = tl;
      })();
    </script>
  </body>
</html>
""")
    open(f"{HF}/index.html", "w").write("\n".join(L))


def build_fx():
    s = open(f"{ROOT}/edits/mcorp-ulasan/fx.tpl.html").read()
    s = s.replace("__TOTAL__", str(TOTAL)).replace("__TIMES__", json.dumps(T))
    open(f"{HF}/compositions/fx.html", "w").write(s)


def build_badge():
    s = open(f"{ROOT}/edits/mcorp-estimate/hf/compositions/badge.html").read()
    s = s.replace("const D = 118.6;", f"const D = {TOTAL};")
    s = s.replace("// corporate MCORP mark stays on for the whole film\n          const HIDE = [];",
                  f"// hidden over the title card and the outro (which carries its own logo)\n          const HIDE = [[-1, {T['TTL1']}], [{OUT0}, {TOTAL + 1}]];")
    open(f"{HF}/compositions/badge.html", "w").write(s)


def build_captions():
    cues = pages()
    json.dump(cues, open(f"{HF}/assets/captions.json", "w"), ensure_ascii=False, indent=1)
    html = """<!doctype html>
<html lang="ms">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
        #root {
          position: absolute;
          inset: 0;
          pointer-events: none;
        }
        #cap {
          position: absolute;
          left: 50%;
          bottom: 64px;
          display: flex;
          gap: 16px;
          align-items: center;
          transform: translateX(-50%);
          white-space: nowrap;
          font-family: Montserrat, sans-serif;
          font-weight: 900;
          font-size: 60px;
          line-height: 1;
          color: #ffffff;
        }
        #cap span {
          display: inline-block;
          padding: 8px 14px 10px;
          border-radius: 12px;
          text-shadow: 0 3px 0 rgba(0, 0, 0, 0.55), 0 0 18px rgba(0, 0, 0, 0.75);
          opacity: 0;
          transform: translateY(18px) scale(0.8);
        }
        #cap span.k {
          color: #ffd23f;
        }
        #cap span.on {
          background: #ffd23f;
          color: #111;
          text-shadow: none;
          box-shadow: 0 10px 26px rgba(0, 0, 0, 0.45);
        }
      </style>
      <div id="root" data-composition-id="captions" data-width="1920" data-height="1080">
        <div id="cap" data-layout-allow-caption-zone></div>
      </div>
      <script>
        (function () {
          const D = __D__;
          const CUES = __CUES__;
          const box = document.getElementById("cap");
          let shown = -1;
          let spans = [];
          function render(t) {
            let idx = -1;
            for (let i = 0; i < CUES.length; i++) {
              if (t >= CUES[i].s && t < CUES[i].e) { idx = i; break; }
            }
            if (idx !== shown) {
              box.innerHTML = idx < 0 ? "" : CUES[idx].words.map((w) => '<span class="' + (w.k ? "k" : "") + '">' + w.w + "</span>").join("");
              spans = Array.from(box.children);
              shown = idx;
            }
            if (idx < 0) return;
            const ws = CUES[idx].words;
            let active = -1;
            ws.forEach((w, i) => { if (t >= w.s - 0.02) active = i; });
            spans.forEach((sp, i) => {
              // each word pops in on its own timestamp
              const k = Math.min(1, Math.max(0, (t - (ws[i].s - 0.08)) / 0.14));
              const e = k < 1 ? 1 - Math.pow(1 - k, 3) : 1;
              const pop = i === active ? 1 + 0.08 * Math.max(0, 1 - (t - ws[i].s) / 0.18) : 1;
              sp.style.opacity = e.toFixed(3);
              sp.style.transform = `translateY(${(18 * (1 - e)).toFixed(1)}px) scale(${((0.8 + 0.2 * e) * pop).toFixed(3)})`;
              sp.classList.toggle("on", i === active);
            });
          }
          const clock = { t: 0 };
          const tl = gsap.timeline({ paused: true });
          tl.to(clock, { t: D, duration: D, ease: "none", onUpdate: () => render(clock.t) }, 0);
          render(0);
          window.__timelines = window.__timelines || {};
          window.__timelines["captions"] = tl;
        })();
      </script>
    </template>
  </body>
</html>
"""
    html = html.replace("__D__", str(TOTAL)).replace("__CUES__", json.dumps(cues, ensure_ascii=False))
    open(f"{HF}/compositions/captions.html", "w").write(html)
    return cues


if __name__ == "__main__":
    build_index()
    build_fx()
    build_badge()
    cues = build_captions()
    print("TOTAL", TOTAL, "OUT0", OUT0)
    print(json.dumps(T))
    for c in cues:
        print(f'{c["s"]:6.2f}-{c["e"]:6.2f} ' + " ".join(("*" if w["k"] else "") + w["w"] for w in c["words"]))
