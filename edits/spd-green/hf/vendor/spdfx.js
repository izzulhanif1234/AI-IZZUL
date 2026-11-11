/* SPD GREEN shared motion helpers. Every helper only ADDS tweens to a paused GSAP timeline,
   so the whole film stays seekable frame by frame (no timers, no Math.random at runtime). */
(function () {
  const FX = {};

  // deterministic pseudo-random
  FX.rand = function (seed) {
    let s = seed >>> 0;
    return function () {
      s = (s * 1664525 + 1013904223) >>> 0;
      return s / 4294967296;
    };
  };

  // type text into an element (textContent) between t and t + dur; optional caret element
  FX.type = function (tl, el, text, t, dur, caret) {
    const o = { n: 0 };
    el.textContent = "";
    tl.to(o, {
      n: text.length, duration: dur, ease: "none",
      onUpdate: () => { el.textContent = text.slice(0, Math.round(o.n)); }
    }, t);
    if (caret) {
      for (let k = 0; k < 40; k++) tl.set(caret, { opacity: k % 2 ? 0 : 1 }, t - 0.6 + k * 0.45);
    }
  };

  // count a number up, formatted
  FX.count = function (tl, el, from, to, t, dur, fmt, ease) {
    const o = { v: from };
    const f = fmt || ((v) => Math.round(v).toLocaleString("en-US"));
    el.textContent = f(from);
    tl.to(o, { v: to, duration: dur, ease: ease || "power3.out", onUpdate: () => { el.textContent = f(o.v); } }, t);
  };

  // draw SVG strokes (paths/lines/circles/rects) with dash offset
  FX.draw = function (tl, sel, t, dur, stagger) {
    const els = typeof sel === "string" ? document.querySelectorAll(sel) : (sel.length !== undefined ? sel : [sel]);
    els.forEach((p, i) => {
      const L = (p.getTotalLength ? p.getTotalLength() : 1000) + 2;
      p.style.strokeDasharray = L;
      p.style.strokeDashoffset = L;
      tl.to(p, { strokeDashoffset: 0, duration: dur, ease: "power2.inOut" }, t + (stagger || 0) * i);
    });
  };

  // hand-drawn "line boil": switch an element between filters at 12 fps
  FX.boil = function (tl, sel, ids, t0, t1) {
    let k = 0;
    for (let t = t0; t < t1; t += 1 / 12) {
      tl.set(sel, { filter: `url(#${ids[k % ids.length]})` }, t);
      k++;
    }
  };

  // move a cursor element along waypoints [[t, x, y], ...]; clicks = [[t, x, y], ...] (ring flashes there)
  FX.cursor = function (tl, cur, pts, clicks, ring) {
    tl.set(cur, { x: pts[0][1], y: pts[0][2], opacity: 1 }, 0);
    for (let i = 1; i < pts.length; i++) {
      const [t, x, y] = pts[i];
      const d = Math.max(0.05, t - pts[i - 1][0]);
      tl.to(cur, { x, y, duration: d, ease: "power3.inOut" }, pts[i - 1][0]);
    }
    (clicks || []).forEach(([t, x, y]) => {
      tl.to(cur, { scale: 0.8, duration: 0.07, ease: "power2.in" }, t);
      tl.to(cur, { scale: 1, duration: 0.2, ease: "back.out(3)" }, t + 0.07);
      if (ring) {
        tl.set(ring, { x, y }, t);
        tl.fromTo(ring, { opacity: 0.95, scale: 0.2 }, { opacity: 0, scale: 1.7, duration: 0.6, ease: "power2.out", immediateRender: false }, t);
      }
    });
  };

  // fast "scroll" of a page image: translate + motion blur
  FX.scroll = function (tl, el, y0, y1, t, dur) {
    tl.fromTo(el, { y: y0 }, { y: y1, duration: dur, ease: "power3.inOut" }, t);
    tl.fromTo(el, { filter: "blur(0px)" }, { filter: "blur(5px)", duration: dur * 0.4, ease: "power2.in", yoyo: true, repeat: 1 }, t);
  };

  // whip transition helper: blur + skew + slide
  FX.whipOut = function (tl, el, t, dir) {
    tl.to(el, { x: (dir || -1) * 900, skewX: (dir || -1) * 12, filter: "blur(18px)", opacity: 0, duration: 0.32, ease: "power3.in" }, t);
  };
  FX.whipIn = function (tl, el, t, dir) {
    tl.fromTo(el, { x: (dir || 1) * 900, skewX: (dir || 1) * 12, filter: "blur(18px)", opacity: 0 },
      { x: 0, skewX: 0, filter: "blur(0px)", opacity: 1, duration: 0.42, ease: "expo.out" }, t);
  };

  // highlight ring (absolutely positioned div) pop
  FX.ring = function (tl, el, t, hold) {
    tl.fromTo(el, { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, t);
    if (hold) tl.to(el, { opacity: 0, duration: 0.25 }, t + hold);
  };

  // kinetic word reveal (mask slide up) for elements with .kw > span

  // premium odometer: every digit is a masked column (0-9 x3) that rolls to its value; static characters
  // (RM , . % −) rise in. o.lock = per-column landing times (digits lock left->right as the VO speaks them).
  FX.odo = function (tl, root, t, dur, o) {
    o = o || {};
    const el = typeof root === "string" ? document.querySelector(root) : root;
    const strips = [...el.querySelectorAll(".odo-s")], n = strips.length;
    strips.forEach((s, i) => {
      const a = +s.dataset.s, e = +s.dataset.e;
      const k = o.ltr ? i : n - 1 - i;
      const t0 = o.lock ? t : t + (o.stagger === undefined ? 0.07 : o.stagger) * k;
      const d = o.lock ? Math.max(0.3, o.lock[i] - t) : dur;
      tl.fromTo(s, { yPercent: -a * 100 / 30 }, { yPercent: -e * 100 / 30, duration: d, ease: o.ease || "expo.out" }, t0);
    });
    const xs = el.querySelectorAll(".odo-x");
    if (xs.length) tl.fromTo(xs, { opacity: 0, yPercent: 45 }, { opacity: 1, yPercent: 0, duration: 0.5, ease: "expo.out", stagger: 0.04 }, t);
  };

  // clean reveals used around numbers: underline draw + soft bloom
  FX.uline = function (tl, sel, t) {
    tl.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "expo.inOut" }, t);
  };
  FX.bloom = function (tl, sel, t, peak) {
    tl.fromTo(sel, { opacity: 0, scale: 0.6 }, { opacity: peak || 1, scale: 1, duration: 0.9, ease: "expo.out" }, t);
  };

  FX.words = function (tl, sel, t, stagger) {
    const els = document.querySelectorAll(sel);
    els.forEach((e, i) => {
      tl.fromTo(e, { yPercent: 110, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.55, ease: "expo.out" }, t + i * (stagger || 0.06));
    });
  };

  window.SPDFX = FX;
})();
