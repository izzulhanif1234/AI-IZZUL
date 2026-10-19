import type React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  Interactive,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { AwarenessRibbon, Sparkles } from "../fx";
import { C, FONT, HALF_WIPE } from "../theme";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const pop = Easing.bezier(0.16, 1, 0.3, 1);

const CalendarIcon: React.FC<{ readonly t: number }> = ({ t }) => (
  <svg width={64} height={64} viewBox="0 0 24 24" fill="none">
    <rect x="3" y="5" width="18" height="16" rx="3" fill={C.magenta} />
    <rect x="3" y="5" width="18" height="5" rx="2" fill={C.maroon} />
    <rect x="7" y="2.5" width="2" height="5" rx="1" fill={C.maroon} />
    <rect x="15" y="2.5" width="2" height="5" rx="1" fill={C.maroon} />
    {[0, 1, 2].map((r) =>
      [0, 1, 2].map((c) => (
        <rect
          key={`${r}${c}`}
          x={6.5 + c * 4}
          y={12 + r * 2.8}
          width="2.4"
          height="1.8"
          rx="0.4"
          fill={C.white}
          opacity={interpolate(t, [r * 3 + c, r * 3 + c + 2], [0, 1], clamp)}
        />
      )),
    )}
  </svg>
);

const ClockIcon: React.FC<{ readonly t: number }> = ({ t }) => {
  const spin = interpolate(t, [0, 16], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <svg width={64} height={64} viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10" fill={C.magenta} />
      <circle cx="12" cy="12" r="7.6" fill={C.white} />
      <line
        x1="12"
        y1="12"
        x2="12"
        y2="7.6"
        stroke={C.maroon}
        strokeWidth="2"
        strokeLinecap="round"
        transform={`rotate(${spin * 150} 12 12)`}
      />
      <line
        x1="12"
        y1="12"
        x2="12"
        y2="5.6"
        stroke={C.magenta}
        strokeWidth="1.5"
        strokeLinecap="round"
        transform={`rotate(${spin * 720} 12 12)`}
      />
      <circle cx="12" cy="12" r="1.2" fill={C.maroon} />
    </svg>
  );
};

const PinIcon: React.FC<{ readonly t: number }> = ({ t }) => (
  <svg
    width={64}
    height={64}
    viewBox="0 0 24 24"
    fill="none"
    style={{
      translate: interpolate(t, [0, 6, 9, 12], ["0px -60px", "0px 4px", "0px -6px", "0px 0px"], clamp),
    }}
  >
    <path
      d="M12 22s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12z"
      fill={C.magenta}
    />
    <circle cx="12" cy="10" r="2.8" fill={C.white} />
  </svg>
);

type CardProps = {
  readonly f: number;
  readonly at: number;
  readonly glowAt: number;
  readonly icon: React.ReactNode;
  readonly label: string;
  readonly big: string;
  readonly sub?: string;
  readonly note?: string;
  readonly left: number;
  readonly width: number;
};

const Card: React.FC<CardProps> = ({ f, at, glowAt, icon, label, big, sub, note, left, width }) => {
  const glow = interpolate(f, [glowAt, glowAt + 3, glowAt + 14], [0, 1, 0], clamp);
  return (
    <div
      style={{
        position: "absolute",
        top: 690,
        left,
        width,
        height: 290,
        borderRadius: 28,
        background: `linear-gradient(160deg, rgba(122,15,46,0.96) 0%, rgba(62,6,24,0.96) 100%)`,
        border: `4px solid ${C.hotPink}`,
        boxShadow: `0 24px 60px rgba(0,0,0,0.5), 0 0 ${30 + glow * 50}px rgba(255,63,164,${0.45 + glow * 0.5})`,
        overflow: "hidden",
        opacity: interpolate(f, [at, at + 2], [0, 1], clamp),
        translate: interpolate(
          f,
          [at, at + 8, at + 12],
          ["1500px 0px", "-28px 0px", "0px 0px"],
          { ...clamp, easing: pop },
        ),
        rotate: interpolate(f, [at, at + 8], ["9deg", "0deg"], { ...clamp, easing: pop }),
        scale: `${1 + glow * 0.04}`,
      }}
    >
      {/* shine sweep */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "linear-gradient(110deg, transparent 35%, rgba(255,255,255,0.28) 50%, transparent 65%)",
          translate: `${interpolate(f, [112, 128], [-120, 120], clamp)}% 0`,
        }}
      />
      <div style={{ display: "flex", alignItems: "center", gap: 18, padding: "24px 34px 0" }}>
        <div
          style={{
            width: 80,
            height: 80,
            borderRadius: 40,
            backgroundColor: C.white,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: `0 0 0 5px rgba(255,63,164,0.35)`,
          }}
        >
          <div style={{ scale: "0.8", display: "flex" }}>{icon}</div>
        </div>
        <div
          style={{
            fontFamily: FONT.body,
            fontWeight: 800,
            fontSize: 38,
            letterSpacing: 4,
            color: C.hotPink,
          }}
        >
          {label}
        </div>
      </div>
      <div style={{ padding: "10px 36px 0" }}>
        <div
          style={{
            fontFamily: FONT.display,
            fontWeight: 900,
            fontStyle: "italic",
            fontSize: 88,
            lineHeight: 1,
            color: C.white,
            whiteSpace: "nowrap",
            transformOrigin: "0% 60%",
            scale: interpolate(f, [at + 8, at + 11, at + 15], [1.3, 0.96, 1], {
              ...clamp,
              output: "perceptual-scale",
            }),
            opacity: interpolate(f, [at + 7, at + 8], [0, 1], clamp),
            textShadow: `0 6px 0 ${C.magenta}`,
          }}
        >
          {big}
        </div>
        <div
          style={{
            marginTop: 10,
            fontFamily: FONT.display,
            fontWeight: 800,
            fontStyle: "italic",
            fontSize: 46,
            lineHeight: 1,
            color: C.white,
            opacity: interpolate(f, [at + 10, at + 13], [0, 1], clamp),
            translate: interpolate(f, [at + 10, at + 14], ["0px 24px", "0px 0px"], {
              ...clamp,
              easing: pop,
            }),
          }}
        >
          {sub}
          {note ? <span style={{ color: C.hotPink }}>{note}</span> : null}
        </div>
      </div>
    </div>
  );
};

// 6-11 s: Tarikh, Masa, Tempat cards slide in one by one over the
// MCORP building; the date lands with the ding.
const InfoInner: React.FC = () => {
  const f = useCurrentFrame() - HALF_WIPE;

  return (
    <>
      <AbsoluteFill style={{ backgroundColor: C.maroonDeep, overflow: "hidden" }}>
        <Img
          src={staticFile("img/building.jpg")}
          style={{
            position: "absolute",
            left: -96,
            top: -300,
            width: 2112,
            height: 1188,
            objectFit: "cover",
            scale: interpolate(f, [-5, 155], [1.0, 1.1], clamp),
            translate: interpolate(f, [-5, 155], ["0px 0px", "-40px 20px"], clamp),
          }}
        />
        <AbsoluteFill
          style={{
            background: `linear-gradient(180deg, rgba(62,6,24,0) 0%, rgba(122,15,46,0.15) 45%, rgba(62,6,24,0.85) 70%, ${C.ink} 100%)`,
          }}
        />
        <AbsoluteFill
          style={{ backgroundColor: C.magenta, mixBlendMode: "soft-light", opacity: 0.3 }}
        />
      </AbsoluteFill>

      {/* Heading lockup */}
      <div
        style={{
          position: "absolute",
          top: 70,
          left: 80,
          display: "flex",
          alignItems: "center",
          gap: 26,
          opacity: interpolate(f, [0, 6], [0, 1], clamp),
          translate: interpolate(f, [0, 8], ["-60px 0px", "0px 0px"], { ...clamp, easing: pop }),
        }}
      >
        <div
          style={{
            padding: "12px 20px",
            borderRadius: 16,
            backgroundColor: "rgba(255,255,255,0.94)",
          }}
        >
          <Img src={staticFile("img/logo.png")} style={{ height: 80, display: "block" }} />
        </div>
        <div
          style={{
            display: "flex",
            alignItems: "flex-end",
            gap: 14,
            filter: "drop-shadow(0 8px 14px rgba(36,2,14,0.55))",
          }}
        >
          <Img src={staticFile("img/title-pink.png")} style={{ height: 96 }} />
          <Img src={staticFile("img/title-move.png")} style={{ height: 64 }} />
          <Img src={staticFile("img/title-2026.png")} style={{ height: 58 }} />
          <AwarenessRibbon size={46} />
        </div>
      </div>

      <Card
        f={f}
        at={4}
        glowAt={66}
        left={100}
        width={560}
        icon={<CalendarIcon t={f - 8} />}
        label="TARIKH"
        big="27/10/2026"
        note="(SELASA)"
      />
      <Card
        f={f}
        at={26}
        glowAt={81}
        left={700}
        width={540}
        icon={<ClockIcon t={f - 30} />}
        label="MASA"
        big="5.00"
        sub="PETANG"
      />
      <Card
        f={f}
        at={48}
        glowAt={96}
        left={1280}
        width={540}
        icon={<PinIcon t={f - 54} />}
        label="TEMPAT"
        big="LOBI"
        sub="MCORP"
      />

      <Sparkles name="Sparkles" count={16} color={C.pinkSoft} seed={3} />
    </>
  );
};

export const Info = Interactive.create({
  Component: InfoInner,
  layout: "absolute-fill",
});
