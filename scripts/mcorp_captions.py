"""Generate compositions/captions.html (karaoke-highlight subtitles) from assets/captions.json."""
import json

HF = "/home/user/AI-IZZUL/edits/mcorp-estimate/hf"
DUR = 116.5
cues = json.load(open(f"{HF}/assets/captions.json"))

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
        #cap-box {
          position: absolute;
          left: 50%;
          bottom: 58px;
          max-width: 1560px;
          padding: 14px 30px 16px;
          border-radius: 18px;
          background: rgba(6, 14, 36, 0.62);
          text-align: center;
          font-family: Montserrat, sans-serif;
          font-weight: 800;
          font-size: 46px;
          line-height: 1.2;
          color: #ffffff;
          text-shadow: 0 2px 6px rgba(0, 0, 0, 0.55);
          transform: translateX(-50%);
          white-space: nowrap;
          opacity: 0;
        }
        #cap-box span {
          display: inline-block;
          margin: 0 0.12em;
        }
        #cap-box span.on {
          color: #ffd23f;
        }
      </style>
      <div id="root" data-composition-id="captions" data-width="1920" data-height="1080">
        <div id="cap-box" data-layout-allow-caption-zone></div>
      </div>
      <script>
        (function () {
          const CUES = __CUES__;
          const box = document.getElementById("cap-box");
          let shown = -1;
          function render(t) {
            let idx = -1;
            for (let i = 0; i < CUES.length; i++) {
              if (t >= CUES[i].s && t < CUES[i].e) { idx = i; break; }
            }
            if (idx !== shown) {
              box.innerHTML = idx < 0 ? "" : CUES[idx].words.map((w) => "<span>" + w.w + "</span>").join(" ");
              shown = idx;
            }
            box.style.opacity = idx < 0 ? "0" : "1";
            if (idx < 0) return;
            const c = CUES[idx];
            const pop = Math.min(1, (t - c.s) / 0.12);
            box.style.transform = "translateX(-50%) translateY(" + ((1 - pop) * 10).toFixed(1) + "px)";
            const spans = box.children;
            for (let k = 0; k < spans.length; k++) {
              const next = k + 1 < c.words.length ? c.words[k + 1].s : c.e;
              spans[k].className = t >= c.words[k].s && t < next ? "on" : "";
            }
          }
          const clock = { t: 0 };
          const tl = gsap.timeline({ paused: true });
          tl.to(clock, { t: __DUR__, duration: __DUR__, ease: "none", onUpdate: () => render(clock.t) }, 0);
          render(0);
          window.__timelines = window.__timelines || {};
          window.__timelines["captions"] = tl;
        })();
      </script>
    </template>
  </body>
</html>
"""
html = html.replace("__CUES__", json.dumps(cues, ensure_ascii=False)).replace("__DUR__", str(DUR))
open(f"{HF}/compositions/captions.html", "w").write(html)
print("captions.html", len(cues), "cues")
