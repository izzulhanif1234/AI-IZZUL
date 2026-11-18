      (function () {
        const C = /*CFG*/;
        const { B, BAR, DROP, F, END, OV, S } = C;
        const tl = gsap.timeline({ paused: true });
        const T2 = 2 * OV;

        // ---------------- hypermotion transitions (on untimed wrappers) ----------------
        function tIn(type, w, t) {
          const a = t - OV, o = { duration: T2, immediateRender: false };
          if (type === "zoom") tl.fromTo(w, { scale: 1.4, opacity: 0, filter: "blur(16px)" }, { ...o, scale: 1, opacity: 1, filter: "blur(0px)", ease: "power3.out" }, a);
          if (type === "whipL") tl.fromTo(w, { x: 1080, filter: "blur(22px)" }, { ...o, x: 0, filter: "blur(0px)", ease: "power3.inOut" }, a);
          if (type === "whipU") tl.fromTo(w, { y: 1920, filter: "blur(22px)" }, { ...o, y: 0, filter: "blur(0px)", ease: "power3.inOut" }, a);
          if (type === "spin") tl.fromTo(w, { rotation: -30, scale: 1.7, opacity: 0, filter: "blur(12px)" }, { ...o, rotation: 0, scale: 1, opacity: 1, filter: "blur(0px)", ease: "power3.out" }, a);
          if (type === "push3d") tl.fromTo(w, { rotationY: 75, x: 520, opacity: 0, transformPerspective: 1400 }, { ...o, rotationY: 0, x: 0, opacity: 1, ease: "power3.out" }, a);
        }
        function tOut(type, w, t) {
          const a = t - OV, o = { duration: T2 };
          if (type === "zoom") tl.to(w, { ...o, scale: 2.4, opacity: 0, filter: "blur(18px)", ease: "power3.in" }, a);
          if (type === "whipL") tl.to(w, { ...o, x: -1080, filter: "blur(22px)", ease: "power3.inOut" }, a);
          if (type === "whipU") tl.to(w, { ...o, y: -1920, filter: "blur(22px)", ease: "power3.inOut" }, a);
          if (type === "spin") tl.to(w, { ...o, rotation: 30, scale: 1.7, opacity: 0, filter: "blur(12px)", ease: "power3.in" }, a);
          if (type === "push3d") tl.to(w, { ...o, rotationY: -75, x: -520, opacity: 0, transformPerspective: 1400, ease: "power3.in" }, a);
        }
        function cut(type, wOut, wIn, t) {
          if (wOut) tOut(type, wOut, t);
          if (wIn) tIn(type, wIn, t);
        }
        // media motion inside a shot: punch-in then a slow push (speed-ramp feel)
        function drift(sel, t0, t1, pan) {
          const x0 = pan ? pan[0] : 0, x1 = pan ? pan[1] : 0;
          const s1 = pan ? pan[3] : 1.07;
          tl.fromTo(sel, { x: x0, scale: 1.14, transformOrigin: "50% 50%" }, { x: x0 + (x1 - x0) * 0.25, scale: 1.0, duration: 0.45, ease: "expo.out", immediateRender: false }, t0 - OV);
          tl.fromTo(sel, { x: x0 + (x1 - x0) * 0.25, scale: 1.0 }, { x: x1, scale: s1, duration: t1 - t0 + T2 - 0.45, ease: "none", immediateRender: false }, t0 - OV + 0.45);
        }
        function leak(t) {
          tl.fromTo("#leak", { opacity: 0, x: -200 }, { opacity: 0.7, x: 0, duration: 0.25, ease: "power2.out", immediateRender: false }, t - 0.1);
          tl.to("#leak", { opacity: 0, x: 200, duration: 0.6, ease: "power2.in" }, t + 0.15);
        }
        function flash(t, peak) {
          tl.fromTo("#flash", { opacity: 0 }, { opacity: peak || 0.9, duration: 0.05, ease: "none", immediateRender: false }, t - 0.05);
          tl.to("#flash", { opacity: 0, duration: 0.45, ease: "power2.out" }, t);
        }
        const fmt = (n) => Math.round(n).toLocaleString("en-US");

        // ================= INTRO =================
        // I-A 0-2.4: dark, blurred exterior + light streak
        tl.fromTo("#x1", { x: -1150, scale: 1.4, filter: "blur(24px) brightness(0.45)", transformOrigin: "50% 50%" }, { x: -1200, scale: 1.25, filter: "blur(18px) brightness(0.55)", duration: 2 * B * 2, ease: "none", immediateRender: false }, 0);
        tl.fromTo("#streak", { scaleX: 0, opacity: 1 }, { scaleX: 1, duration: 0.7, ease: "expo.out", immediateRender: false }, 0.05);
        tl.to("#streak", { opacity: 0, scaleY: 6, duration: 0.5, ease: "power2.in" }, 1.6);
        tl.from("#i-k1", { y: 40, opacity: 0, scale: 1.3, duration: 0.6, ease: "expo.out" }, B);
        tl.from("#i-k2", { y: 30, opacity: 0, duration: 0.5, ease: "power3.out" }, 2 * B);
        tl.to(["#i-k1", "#i-k2"], { y: -60, opacity: 0, filter: "blur(10px)", duration: 0.25, ease: "power2.in" }, BAR - 0.25);
        // I-B 2.4-4.8: sharp reveal + name, one word per beat
        tl.to("#x1", { filter: "blur(0px) brightness(1)", scale: 1.12, x: -1250, duration: 0.6, ease: "expo.out" }, BAR);
        tl.to("#x1", { scale: 1.02, x: -1320, duration: BAR - 0.6 + OV, ease: "none" }, BAR + 0.6);
        flash(BAR, 0.5);
        ["#it1", "#it2", "#it3"].forEach((s, i) => {
          tl.from(s, { yPercent: 90, opacity: 0, skewY: 8, scale: 1.25, duration: 0.5, ease: "expo.out" }, BAR + i * B);
        });
        tl.from("#it-bar", { scaleX: 0, duration: 0.5, ease: "expo.out" }, BAR + 3 * B);
        tl.to("#i-title", { y: -120, opacity: 0, filter: "blur(14px)", duration: 0.25, ease: "power2.in" }, 2 * BAR - 0.25);
        // I-C 4.8-7.2: aerial + stats
        cut("whipU", "#w-x1", "#w-x2", 2 * BAR);
        tl.fromTo("#x2", { x: -1000, scale: 1.12, transformOrigin: "50% 50%" }, { x: -1650, scale: 1.0, duration: 2 * BAR, ease: "none", immediateRender: false }, 2 * BAR - OV);
        const c1 = { v: 0 }, c2 = { v: 0 };
        tl.from("#i-stat1", { scale: 0.5, opacity: 0, duration: 0.5, ease: "back.out(1.8)" }, 2 * BAR + 0.1);
        tl.to(c1, { v: 3.1, duration: 0.7, ease: "power2.out", onUpdate: () => (document.getElementById("n1").textContent = c1.v.toFixed(1)) }, 2 * BAR + 0.15);
        tl.from("#i-stat2", { scale: 0.5, opacity: 0, duration: 0.5, ease: "back.out(1.8)" }, 2 * BAR + 2 * B);
        tl.to(c2, { v: 13090, duration: 0.6, ease: "power2.out", onUpdate: () => (document.getElementById("n2").textContent = fmt(c2.v)) }, 2 * BAR + 2 * B + 0.05);
        tl.to(["#i-stat1", "#i-stat2"], { y: -80, opacity: 0, filter: "blur(12px)", duration: 0.22, ease: "power2.in", stagger: 0.05 }, 3 * BAR - 0.3);
        // I-D 7.2-9.6: three strips, one per beat
        ["#st1", "#st2", "#st3"].forEach((s, i) => {
          tl.fromTo(s, { yPercent: 100 }, { yPercent: 0, duration: 0.5, ease: "power4.out", immediateRender: false }, 3 * BAR + i * B);
          tl.fromTo(s + " .clip", { scale: 1.3 }, { scale: 1.0, duration: BAR, ease: "power2.out", immediateRender: false }, 3 * BAR + i * B);
          tl.from("#lab" + (i + 1), { y: 80, opacity: 0, duration: 0.4, ease: "expo.out" }, 3 * BAR + i * B + 0.15);
        });
        tl.set(["#st1", "#st2", "#st3"], { yPercent: 100 }, 0);
        tl.to(["#lab1", "#lab2", "#lab3"], { opacity: 0, y: -60, duration: 0.2, ease: "power2.in" }, 4 * BAR - 0.2);
        // I-E 9.6-12.0: accelerating zoom into the MITC sign + THINK MICE, THINK MITC
        cut("zoom", "#w-strips", "#w-x3", 4 * BAR);
        tl.fromTo("#x3", { x: -1542, y: -52, scale: 1.0, transformOrigin: "2082px 1012px", filter: "blur(0px)" }, { scale: 7.5, duration: BAR, ease: "expo.in", immediateRender: false }, 4 * BAR);
        tl.to("#x3", { filter: "blur(10px)", duration: 0.35, ease: "power2.in" }, DROP - 0.35);
        tl.from("#think1", { scale: 1.8, opacity: 0, filter: "blur(10px)", duration: 0.4, ease: "expo.out" }, 4 * BAR + 0.02);
        tl.from("#think2", { scale: 1.8, opacity: 0, filter: "blur(10px)", duration: 0.4, ease: "expo.out" }, 4 * BAR + 2 * B);
        tl.to(["#think1", "#think2"], { scale: 1.5, opacity: 0, filter: "blur(16px)", duration: 0.3, ease: "power2.in" }, DROP - 0.3);
        flash(DROP, 1);
        leak(DROP);

        // ================= LOGO (drop) =================
        tl.fromTo("#lgv", { scale: 1.25 }, { scale: 1.05, duration: 2 * BAR, ease: "none", immediateRender: false }, DROP);
        tl.fromTo("#rays", { rotation: 0, opacity: 0 }, { rotation: 50, opacity: 1, duration: 2 * BAR, ease: "none", immediateRender: false }, DROP);
        tl.from("#lg", { rotationY: -540, scale: 0.2, opacity: 0, transformPerspective: 1600, duration: 1.1, ease: "expo.out" }, DROP + 0.02);
        tl.to("#lg", { y: -14, duration: 1.2, yoyo: true, repeat: 2, ease: "sine.inOut" }, DROP + 1.2);
        tl.from("#lg-head .t", { y: 80, opacity: 0, scale: 1.15, duration: 0.5, ease: "expo.out" }, DROP + 2 * B);
        tl.from("#lg-head .en", { y: 40, opacity: 0, duration: 0.45, ease: "power3.out" }, DROP + 3 * B);
        tl.from("#lg-head .pill", { scale: 0.4, opacity: 0, duration: 0.45, ease: "back.out(2)" }, DROP + 4 * B);
        tl.to(["#lg", "#lg-head", "#rays"], { scale: 1.6, opacity: 0, filter: "blur(14px)", duration: T2, ease: "power3.in" }, S.sa - OV);

        // ================= MONTAGE =================
        const shots = C.shots;
        tOut(shots[0].trans, "#w-lg", shots[0].t0);
        shots.forEach((sh, i) => {
          tIn(sh.trans, "#w-" + sh.id, sh.t0);
          const next = shots[i + 1];
          if (next && Math.abs(next.t0 - sh.t1) < 0.01) tOut(next.trans, "#w-" + sh.id, sh.t1);
          drift("#m-" + sh.id, sh.t0, sh.t1, sh.pan);
        });
        // sections: title slam, captions per shot, light leak on entry
        C.sections.forEach(([id, t0, t1]) => {
          const s = "#t-" + id + " ";
          leak(t0);
          tl.from(s + ".num", { x: -160, opacity: 0, duration: 0.45, ease: "expo.out" }, t0 + 0.02);
          tl.from(s + ".en", { x: 80, opacity: 0, duration: 0.4, ease: "power3.out" }, t0 + 0.12);
          tl.from(s + ".ttl", { y: 120, opacity: 0, scale: 1.3, skewX: -8, duration: 0.5, ease: "expo.out" }, t0 + 0.18);
          tl.from(s + ".sub", { scaleX: 0, transformOrigin: "0% 50%", duration: 0.45, ease: "expo.out" }, t0 + 0.45);
          tl.to(s + ".sec", { y: -60, opacity: 0, filter: "blur(10px)", duration: 0.2, ease: "power2.in" }, t1 - 0.22);
          shots.filter((sh) => sh.t0 >= t0 - 0.01 && sh.t0 < t1 - 0.01).forEach((sh) => {
            tl.fromTo("#cap-" + sh.id, { x: -80, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: "expo.out", immediateRender: false }, sh.t0 + 0.12);
            tl.to("#cap-" + sh.id, { x: 60, opacity: 0, duration: 0.14, ease: "power2.in" }, sh.t1 - 0.16);
            tl.set("#cap-" + sh.id, { opacity: 0 }, 0);
          });
        });
        document.querySelectorAll("#t-sd .chip").forEach((el, i) => {
          tl.from(el, { y: 40, scale: 0.5, opacity: 0, duration: 0.32, ease: "back.out(2.2)" }, S.sd + 0.9 + i * B);
          tl.to(el, { backgroundColor: "#f7c731", borderColor: "#f7c731", color: "#1c2747", duration: 0.12, ease: "none" }, S.sd + 0.9 + i * B);
        });
        // HUD
        tl.from(".br", { scale: 0, opacity: 0, duration: 0.4, ease: "back.out(2)", stagger: 0.05 }, S.sa);
        tl.from(["#hud-l", "#hud-r"], { opacity: 0, y: -20, duration: 0.4, ease: "power3.out" }, S.sa + 0.2);
        tl.fromTo("#hud-fill", { scaleX: 0 }, { scaleX: 1, duration: S.aw - S.sa, ease: "none", immediateRender: false }, S.sa);

        // ================= AWARDS =================
        const lastMont = shots.filter((sh) => sh.t1 <= S.aw + 0.01).pop();
        tOut("zoom", "#w-" + lastMont.id, S.aw);
        flash(S.aw, 0.8);
        tl.from("#aw-title .k", { y: -30, opacity: 0, duration: 0.3, ease: "power3.out" }, S.aw + 0.03);
        tl.from("#aw-title .t", { scale: 1.8, opacity: 0, filter: "blur(14px)", duration: 0.45, ease: "expo.out" }, S.aw + 0.08);
        tl.from("#v-aw", { y: 140, rotationX: 30, opacity: 0, transformPerspective: 1400, duration: 0.6, ease: "expo.out" }, S.aw + 0.2);
        ["#bd1", "#bd2", "#bd3", "#bd4"].forEach((s, i) => tl.from(s, { scale: 0, rotation: -60, duration: 0.45, ease: "back.out(2)" }, S.aw + (2 + i) * B));
        tl.from("#al1", { y: 30, opacity: 0, duration: 0.35, ease: "power3.out" }, S.aw + 3 * B + 0.1);
        tl.from("#al2", { y: 30, opacity: 0, duration: 0.35, ease: "power3.out" }, S.aw + 4 * B + 0.1);
        tl.from("#al3", { y: 30, opacity: 0, duration: 0.35, ease: "power3.out" }, S.aw + 5 * B + 0.1);
        tl.to(["#bd1", "#bd2", "#bd3", "#bd4"], { scale: 1.08, duration: 0.18, yoyo: true, repeat: 1, ease: "sine.inOut", stagger: 0.1 }, S.aw + 6 * B);
        tl.to(["#t-aw > *", "#v-aw", "#aw-bg"], { scale: 1.3, opacity: 0, filter: "blur(12px)", duration: T2, ease: "power3.in" }, S.recap - OV);

        // ================= RECAP (one beat per shot) =================
        flash(S.recap, 0.6);
        tl.from("#rc1", { scale: 1.8, opacity: 0, filter: "blur(10px)", duration: 0.35, ease: "expo.out" }, S.recap + 0.02);
        tl.to("#rc1", { opacity: 0, duration: 0.1 }, S.recap + 2 * B - 0.1);
        tl.from("#rc2", { scale: 1.8, opacity: 0, filter: "blur(10px)", duration: 0.35, ease: "expo.out" }, S.recap + 2 * B);
        tl.to("#rc2", { scale: 1.4, opacity: 0, filter: "blur(14px)", duration: T2, ease: "power3.in" }, S.close - OV);
        const lastRecap = shots[shots.length - 1];
        tOut("zoom", "#w-" + lastRecap.id, S.close);

        // ================= CLOSE (soft ending) =================
        tIn("zoom", "#w-cl", S.close);
        tl.fromTo("#cl", { x: -1250, scale: 1.25, transformOrigin: "50% 50%", filter: "brightness(0.85) saturate(1.1)" }, { x: -1150, scale: 1.04, duration: F - S.close + T2, ease: "power1.out", immediateRender: false }, S.close - OV);
        tl.from("#cl-t", { y: 80, opacity: 0, duration: 0.6, ease: "expo.out" }, S.close + 0.25);
        tl.from("#cl-s", { y: 30, opacity: 0, duration: 0.5, ease: "power3.out" }, S.close + 1.1);
        tl.to(["#cl-t", "#cl-s"], { opacity: 0, y: -40, duration: 0.2, ease: "power2.in" }, F - 0.2);

        // ================= OUTRO (final chord) =================
        flash(F, 0.9);
        tl.fromTo("#ob", { x: -1100, scale: 1.05, transformOrigin: "50% 50%" }, { x: -1300, scale: 1.12, duration: END - F, ease: "none", immediateRender: false }, F);
        tl.from("#out-logo", { rotationY: 360, scale: 0.3, opacity: 0, transformPerspective: 1400, duration: 0.9, ease: "expo.out" }, F + 0.02);
        tl.from("#out-name", { y: 40, opacity: 0, duration: 0.45, ease: "power3.out" }, F + 0.4);
        tl.from("#out-cta", { scale: 0.4, opacity: 0, duration: 0.45, ease: "back.out(2.2)" }, F + 0.8);
        tl.from("#out-contact", { y: 80, opacity: 0, duration: 0.5, ease: "expo.out" }, F + 1.1);
        tl.from("#out-contact .ct", { x: -40, opacity: 0, duration: 0.35, ease: "power3.out", stagger: 0.12 }, F + 1.25);
        tl.from("#out-addr", { opacity: 0, duration: 0.4 }, F + 1.7);
        tl.to("#out-cta", { scale: 1.05, duration: 0.35, yoyo: true, repeat: 3, ease: "sine.inOut" }, F + 1.9);
        tl.to("#fade", { opacity: 1, duration: 0.6, ease: "power1.in" }, END - 0.6);

        window.__timelines = window.__timelines || {};
        window.__timelines["main"] = tl;
      })();
