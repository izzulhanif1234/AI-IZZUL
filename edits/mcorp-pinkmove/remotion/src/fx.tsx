import type { TransitionPresentationComponentProps } from "@remotion/transitions";
import type React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  Interactive,
  random,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { C } from "./theme";

const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

// Decaying camera shake from a list of hit frames.
export const shakeAt = (
  frame: number,
  hits: ReadonlyArray<readonly [at: number, amp: number]>,
) => {
  let x = 0;
  let y = 0;
  let r = 0;
  for (const [at, amp] of hits) {
    const t = frame - at;
    if (t < 0 || t > 14) continue;
    const d = amp * Math.exp(-t / 4);
    x += Math.sin(t * 2.9 + at) * d;
    y += Math.cos(t * 3.7 + at * 1.3) * d * 0.7;
    r += Math.sin(t * 2.1 + at * 0.7) * d * 0.04;
  }
  return { translate: `${x}px ${y}px`, rotate: `${r}deg` };
};

// Pink-white burst background like the poster's bright centre,
// or the deep maroon variant.
const BackdropInner: React.FC<{ readonly variant: "burst" | "dark" }> = ({
  variant,
}) => {
  const frame = useCurrentFrame();
  const burst = variant === "burst";
  return (
    <>
      <AbsoluteFill
        style={{
          background: burst
            ? `radial-gradient(ellipse 70% 75% at 50% 48%, ${C.white} 0%, ${C.pinkSoft} 28%, ${C.hotPink} 55%, ${C.magenta} 72%, ${C.maroon} 100%)`
            : `radial-gradient(ellipse 85% 80% at 50% 45%, ${C.maroon} 0%, ${C.maroonDeep} 62%, ${C.ink} 100%)`,
        }}
      />
      <AbsoluteFill
        style={{
          backgroundImage: `radial-gradient(circle, ${burst ? "rgba(122,15,46,0.35)" : "rgba(255,63,164,0.35)"} 2.2px, transparent 2.8px)`,
          backgroundSize: "22px 22px",
          backgroundPosition: `${frame * 0.6}px ${frame * -0.3}px`,
          maskImage:
            "radial-gradient(ellipse 60% 60% at 50% 50%, transparent 35%, black 100%)",
          opacity: 0.9,
        }}
      />
      {/* fine static noise to dither the gradient's 8-bit banding */}
      <svg width="100%" height="100%" style={{ position: "absolute", inset: 0, opacity: burst ? 0.07 : 0.05 }}>
        <filter id="dither">
          <feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves={1} seed={2} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#dither)" />
      </svg>
    </>
  );
};

export const Backdrop = Interactive.create({
  Component: BackdropInner,
  layout: "absolute-fill",
});

// Rough diagonal paint streaks drifting across the frame.
const StreaksInner: React.FC<{ readonly color: string; readonly seed: number }> = ({
  color,
  seed,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const streaks = new Array(7).fill(0).map((_, i) => ({
    y: random(`y${seed}${i}`) * height,
    w: 600 + random(`w${seed}${i}`) * 900,
    h: 10 + random(`h${seed}${i}`) * 46,
    x: random(`x${seed}${i}`) * width,
    speed: 4 + random(`s${seed}${i}`) * 10,
    o: 0.25 + random(`o${seed}${i}`) * 0.55,
  }));
  return (
    <svg
      width={width}
      height={height}
      style={{ position: "absolute", inset: 0, overflow: "visible" }}
    >
      <defs>
        <filter id={`rough${seed}`}>
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.035 0.6"
            numOctaves="2"
            seed={seed}
          />
          <feDisplacementMap in="SourceGraphic" scale="26" />
        </filter>
      </defs>
      <g filter={`url(#rough${seed})`} transform={`rotate(-24 ${width / 2} ${height / 2})`}>
        {streaks.map((s, i) => (
          <rect
            key={i}
            x={((s.x + frame * s.speed) % (width + s.w * 2)) - s.w}
            y={s.y}
            width={s.w}
            height={s.h}
            rx={s.h / 2}
            fill={color}
            opacity={s.o}
          />
        ))}
      </g>
    </svg>
  );
};

export const Streaks = Interactive.create({
  Component: StreaksInner,
  layout: "absolute-fill",
});

// Twinkling four-point sparkles.
const SparklesInner: React.FC<{
  readonly count: number;
  readonly color: string;
  readonly seed: number;
}> = ({ count, color, seed }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  return (
    <>
      {new Array(count).fill(0).map((_, i) => {
        const x = random(`sx${seed}${i}`) * width;
        const y = random(`sy${seed}${i}`) * height;
        const size = 14 + random(`ss${seed}${i}`) * 34;
        const phase = random(`sp${seed}${i}`) * Math.PI * 2;
        const tw = Math.max(0, Math.sin(frame * 0.22 + phase));
        return (
          <svg
            key={i}
            width={size}
            height={size}
            viewBox="-10 -10 20 20"
            style={{
              position: "absolute",
              left: x - size / 2,
              top: y - size / 2 - frame * (0.4 + random(`sv${seed}${i}`)),
              opacity: tw,
              scale: `${0.4 + tw * 0.8}`,
              rotate: `${frame * 2 + i * 40}deg`,
              filter: `drop-shadow(0 0 6px ${color})`,
            }}
          >
            <path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2 Z" fill={color} />
          </svg>
        );
      })}
    </>
  );
};

export const Sparkles = Interactive.create({
  Component: SparklesInner,
  layout: "absolute-fill",
});

type Pt = readonly [number, number];

const cubic = (p0: Pt, p1: Pt, p2: Pt, p3: Pt, t: number): Pt => {
  const u = 1 - t;
  return [
    u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
    u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1],
  ];
};

// The sweeping S-curve the ribbon flies along (two cubic segments).
export const ribbonPoint = (width: number, height: number, wave: number, t: number): Pt => {
  const w = Math.sin(wave) * 40;
  const a: Pt = [-260, height * 0.92];
  const b: Pt = [width * 0.18, height * 0.62 + w];
  const c: Pt = [width * 0.36, height * 1.02 - w];
  const m: Pt = [width * 0.55, height * 0.55];
  const d: Pt = [2 * m[0] - c[0], 2 * m[1] - c[1]];
  const e: Pt = [width * 0.84, height * 0.02 + w];
  const z: Pt = [width + 300, height * 0.2];
  return t < 0.5 ? cubic(a, b, c, m, t * 2) : cubic(m, d, e, z, t * 2 - 1);
};

// The flowing pink band left behind by the flying ribbon; drawn up to `progress`.
export const RibbonPath: React.FC<{
  readonly progress: number;
  readonly wave: number;
  readonly thickness?: number;
}> = ({ progress, wave, thickness = 120 }) => {
  const { width, height } = useVideoConfig();
  const steps = 140;
  const pts: Pt[] = [];
  for (let i = 0; i <= steps * progress; i++) {
    pts.push(ribbonPoint(width, height, wave, i / steps));
  }
  pts.push(ribbonPoint(width, height, wave, progress));
  const d = pts.map((p, i) => `${i === 0 ? "M" : "L"}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(" ");
  if (progress <= 0) return null;
  return (
    <svg width={width} height={height} style={{ position: "absolute", inset: 0, overflow: "visible" }}>
      <defs>
        <linearGradient id="ribbonGrad" x1="0" y1="1" x2="1" y2="0">
          <stop offset="0" stopColor={C.maroon} />
          <stop offset="0.35" stopColor={C.magenta} />
          <stop offset="0.6" stopColor={C.hotPink} />
          <stop offset="1" stopColor={C.magenta} />
        </linearGradient>
      </defs>
      <path d={d} fill="none" stroke={C.ink} strokeOpacity={0.35} strokeWidth={thickness} strokeLinejoin="round" transform="translate(14 22)" />
      <path d={d} fill="none" stroke="url(#ribbonGrad)" strokeWidth={thickness} strokeLinejoin="round" />
      <path d={d} fill="none" stroke={C.white} strokeOpacity={0.55} strokeWidth={thickness * 0.12} strokeLinejoin="round" transform={`translate(0 ${-thickness * 0.28})`} />
    </svg>
  );
};

// An ordinary pink ribbon streams in from bottom left and ties itself into
// the awareness-ribbon loop. Points are in the loop's local 245x340 box
// (same framing as pink-ribbon.png), placed at (x, y) and scaled by `scale`.
const LOOP_PATH: ReadonlyArray<readonly [string, ...number[]]> = [
  ["L", 180, 190],
  ["C", 228, 130, 225, 40, 175, 18],
  ["C", 150, 10, 100, 15, 70, 50],
  ["C", 30, 95, 60, 168, 122, 222],
  ["L", 225, 312],
];

export const RibbonTie: React.FC<{
  readonly progress: number;
  readonly x: number;
  readonly y: number;
  readonly scale: number;
  readonly style?: React.CSSProperties;
}> = ({ progress, x, y, scale, style }) => {
  const { width, height } = useVideoConfig();
  const map = (px: number, py: number) => `${(x + px * scale).toFixed(1)} ${(y + py * scale).toFixed(1)}`;
  const tail = [x + 18 * scale, y + 312 * scale];
  const dir = [162 / 202, -122 / 202];
  const lead = `M -260 ${height + 40} C ${width * 0.12} ${height - 20}, ${(tail[0] - dir[0] * 180).toFixed(1)} ${(tail[1] - dir[1] * 180).toFixed(1)}, ${map(18, 312)}`;
  const loop = LOOP_PATH.map(([cmd, ...n]) => {
    const pts: string[] = [];
    for (let i = 0; i < n.length; i += 2) pts.push(map(n[i], n[i + 1]));
    return `${cmd} ${pts.join(", ")}`;
  }).join(" ");
  const d = `${lead} ${loop}`;
  const dash = { strokeDasharray: "1 1", strokeDashoffset: 1 - progress };
  return (
    <svg width={width} height={height} style={{ position: "absolute", inset: 0, overflow: "visible", ...style }}>
      <defs>
        <linearGradient id="tieGrad" x1="0" y1="1" x2="1" y2="0">
          <stop offset="0" stopColor="#DD4E86" />
          <stop offset="0.5" stopColor="#EC6A9C" />
          <stop offset="1" stopColor="#C2185B" />
        </linearGradient>
      </defs>
      <path d={d} pathLength={1} fill="none" stroke={C.ink} strokeOpacity={0.3} strokeWidth={46 * scale} transform="translate(12 18)" style={dash} />
      <path d={d} pathLength={1} fill="none" stroke={C.white} strokeWidth={54 * scale} style={dash} />
      <path d={d} pathLength={1} fill="none" stroke="url(#tieGrad)" strokeWidth={46 * scale} style={dash} />
    </svg>
  );
};

// Pink breast-cancer awareness ribbon supplied by the client (keyed off
// white in public/img/pink-ribbon.png). `size` is the width.
export const AwarenessRibbon: React.FC<{
  readonly size: number;
  readonly style?: React.CSSProperties;
}> = ({ size, style }) => (
  <div style={{ width: size, height: size * 1.383, ...style }}>
    <Img
      src={staticFile("img/pink-ribbon.png")}
      style={{
        width: "100%",
        height: "100%",
        filter: "drop-shadow(0 0 2px #fff) drop-shadow(0 0 1px #fff)",
      }}
    />
  </div>
);

// Film grain plus vignette, laid over the whole video.
const FinishInner: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  return (
    <>
      <svg
        width={width}
        height={height}
        style={{ position: "absolute", inset: 0, opacity: 0.09, mixBlendMode: "overlay" }}
      >
        <filter id="grain">
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.9"
            numOctaves="2"
            seed={frame % 7}
          />
        </filter>
        <rect width={width} height={height} filter="url(#grain)" />
      </svg>
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse 75% 70% at 50% 50%, transparent 55%, rgba(36,2,14,0.55) 100%)",
        }}
      />
    </>
  );
};

export const Finish = Interactive.create({
  Component: FinishInner,
  layout: "absolute-fill",
});

// White flash that decays after a hit.
export const flashAt = (frame: number, at: number, len = 6) =>
  interpolate(frame, [at, at + 1, at + len], [0, 0.85, 0], clamp);

type SlashProps = { direction: "right" | "left" };

// Diagonal maroon/magenta slash that wipes the next scene in.
const PinkSlashPresentation: React.FC<
  TransitionPresentationComponentProps<SlashProps>
> = ({ children, presentationDirection, presentationProgress, passedProps }) => {
  const p = presentationProgress;
  const right = passedProps.direction === "right";
  if (presentationDirection === "exiting") {
    return (
      <AbsoluteFill
        style={{
          scale: interpolate(p, [0, 1], [1, 1.12]),
          translate: `${(right ? -1 : 1) * p * 5}% 0`,
        }}
      >
        {children}
      </AbsoluteFill>
    );
  }
  const e = interpolate(p, [0, 1], [-30, 130]);
  const slab = (a: number, b: number) => {
    const pts = [
      [a + 14, 0],
      [b + 14, 0],
      [b - 14, 100],
      [a - 14, 100],
    ].map(([x, y]) => `${right ? x : 100 - x}% ${y}%`);
    return `polygon(${pts.join(",")})`;
  };
  return (
    <AbsoluteFill>
      <AbsoluteFill
        style={{
          clipPath: slab(-80, e),
          scale: interpolate(p, [0, 1], [1.14, 1], {
            easing: Easing.out(Easing.cubic),
          }),
        }}
      >
        {children}
      </AbsoluteFill>
      <AbsoluteFill style={{ clipPath: slab(e, e + 6), backgroundColor: C.maroon }} />
      <AbsoluteFill style={{ clipPath: slab(e + 6, e + 15), backgroundColor: C.magenta }} />
      <AbsoluteFill style={{ clipPath: slab(e + 15, e + 16.2), backgroundColor: C.white }} />
    </AbsoluteFill>
  );
};

export const pinkSlash = (props: SlashProps) => ({
  component: PinkSlashPresentation,
  props,
});
