import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {C, FONT, GOLD_GRADIENT, H, W, WIPE} from './theme';
import {starPath, starPoints} from './ornaments';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/**
 * Opens its children through an eight-pointed star that grows from the
 * centre, with a gold edge riding the outline. Used between scenes.
 */
export const StarReveal: React.FC<{children: React.ReactNode; dur?: number; cy?: number}> = ({
  children,
  dur = WIPE,
  cy = H / 2,
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, dur], [0, 1], {...clamp, easing: Easing.bezier(0.65, 0, 0.25, 1)});
  if (p >= 1) return <AbsoluteFill>{children}</AbsoluteFill>;
  const R = p * 1500;
  const rot = p * 45;
  const poly = starPoints(W / 2, cy, R, rot)
    .map(([x, y]) => `${x.toFixed(1)}px ${y.toFixed(1)}px`)
    .join(',');
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{clipPath: `polygon(${poly})`}}>{children}</AbsoluteFill>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <path d={starPath(W / 2, cy, R, rot)} fill="none" stroke={C.goldLight} strokeWidth={6} opacity={1 - p * 0.6} />
        <path d={starPath(W / 2, cy, R * 1.05, rot)} fill="none" stroke={C.gold} strokeWidth={2} opacity={0.7 - p * 0.5} />
      </svg>
    </AbsoluteFill>
  );
};

/** Gold gradient text with a light sweep at `shineAt`. */
export const GoldText: React.FC<{
  children: React.ReactNode;
  style?: React.CSSProperties;
  shineAt?: number;
}> = ({children, style, shineAt = 0}) => {
  const frame = useCurrentFrame();
  const pos = interpolate(frame, [shineAt, shineAt + 40], [100, 0], {...clamp, easing: Easing.inOut(Easing.quad)});
  return (
    <span
      style={{
        backgroundImage: GOLD_GRADIENT,
        backgroundSize: '300% 100%',
        backgroundPosition: `${pos}% 50%`,
        WebkitBackgroundClip: 'text',
        backgroundClip: 'text',
        color: 'transparent',
        filter: 'drop-shadow(0 2px 10px rgba(0,0,0,0.45))',
        ...style,
      }}
    >
      {children}
    </span>
  );
};

/** Word-by-word reveal. Words listed in `gold` are tinted gold. */
export const Words: React.FC<{
  text: string;
  start: number;
  stagger?: number;
  gold?: string[];
  style?: React.CSSProperties;
  wordStyle?: React.CSSProperties;
}> = ({text, start, stagger = 4, gold = [], style, wordStyle}) => {
  const frame = useCurrentFrame();
  const goldSet = new Set(gold.map((g) => g.toLowerCase()));
  const words = text.split(/\s+/).filter(Boolean);
  return (
    <div style={style}>
      {words.map((w, i) => {
        const f = frame - start - i * stagger;
        const o = interpolate(f, [0, 14], [0, 1], clamp);
        const y = interpolate(f, [0, 16], [22, 0], {...clamp, easing: Easing.out(Easing.cubic)});
        const blur = interpolate(f, [0, 12], [8, 0], clamp);
        const isGold = goldSet.has(w.toLowerCase().replace(/[.,!?]/g, ''));
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              opacity: o,
              transform: `translateY(${y}px)`,
              filter: `blur(${blur}px)`,
              marginRight: '0.26em',
              color: isGold ? C.goldLight : undefined,
              ...wordStyle,
            }}
          >
            {w}
          </span>
        );
      })}
    </div>
  );
};

/**
 * Full-frame photo with a slow push. `x` / `y` pan the crop in percentage
 * points around the centre (object-position), so edges never show.
 */
export const KenBurns: React.FC<{
  src: string;
  dur: number;
  from?: number;
  to?: number;
  x?: [number, number];
  y?: [number, number];
  style?: React.CSSProperties;
}> = ({src, dur, from = 1.08, to = 1.2, x = [0, 0], y = [0, 0], style}) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [0, dur], [0, 1], clamp);
  const s = from + (to - from) * t;
  const tx = x[0] + (x[1] - x[0]) * t;
  const ty = y[0] + (y[1] - y[0]) * t;
  return (
    <AbsoluteFill style={{overflow: 'hidden', ...style}}>
      <Img
        src={staticFile(src)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          objectPosition: `${50 + tx}% ${50 + ty}%`,
          transform: `scale(${s})`,
        }}
      />
    </AbsoluteFill>
  );
};

/** Cross-dissolve helper: opacity envelope for an item living in [0, dur]. */
export const useFade = (dur: number, inF = 12, outF = 12) => {
  const frame = useCurrentFrame();
  return interpolate(frame, [0, inF, dur - outF, dur], [0, 1, 1, 0], clamp);
};

export const SmallCaps: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
  <div
    style={{
      fontFamily: FONT.sans,
      fontWeight: 500,
      fontSize: 26,
      letterSpacing: '0.32em',
      textTransform: 'uppercase',
      color: C.gold,
      ...style,
    }}
  >
    {children}
  </div>
);
