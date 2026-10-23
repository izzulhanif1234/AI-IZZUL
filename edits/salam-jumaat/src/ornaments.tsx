import React from 'react';
import {AbsoluteFill, interpolate, random, useCurrentFrame, Easing} from 'remotion';
import {C, H, W} from './theme';

const ease = Easing.bezier(0.45, 0, 0.2, 1);

// Points of an eight-pointed star (Rub el Hizb: two overlapping squares).
export const starPoints = (cx: number, cy: number, R: number, rot = 0) => {
  const r = R * 0.7654; // inner vertices where the two squares cross
  const pts: [number, number][] = [];
  for (let i = 0; i < 16; i++) {
    const rad = i % 2 === 0 ? R : r;
    const a = ((i * 22.5 - 90 + rot) * Math.PI) / 180;
    pts.push([cx + rad * Math.cos(a), cy + rad * Math.sin(a)]);
  }
  return pts;
};

export const starPath = (cx: number, cy: number, R: number, rot = 0) =>
  'M' + starPoints(cx, cy, R, rot).map((p) => p.map((v) => v.toFixed(2)).join(',')).join('L') + 'Z';

const squarePath = (cx: number, cy: number, R: number, rot: number) => {
  const pts = [0, 1, 2, 3].map((i) => {
    const a = ((rot + i * 90 - 90) * Math.PI) / 180;
    return `${(cx + R * Math.cos(a)).toFixed(2)},${(cy + R * Math.sin(a)).toFixed(2)}`;
  });
  return `M${pts.join('L')}Z`;
};

// Pointed (mihrab) arch inside the box x,y,w,h. `s` is the depth of the arched part.
export const archPath = (x: number, y: number, w: number, h: number, s = w * 0.62) =>
  [
    `M${x},${y + h}`,
    `L${x},${y + s}`,
    `C${x},${y + s * 0.42} ${x + w * 0.3},${y + s * 0.14} ${x + w / 2},${y}`,
    `C${x + w * 0.7},${y + s * 0.14} ${x + w},${y + s * 0.42} ${x + w},${y + s}`,
    `L${x + w},${y + h}`,
    'Z',
  ].join(' ');

const drawOn = (frame: number, start: number, dur: number) =>
  interpolate(frame, [start, start + dur], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: ease,
  });

/** Tiled star-and-cross lattice, very faint, drifting slowly. */
export const PatternBg: React.FC<{opacity?: number; tile?: number}> = ({opacity = 0.11, tile = 150}) => {
  const frame = useCurrentFrame();
  const drift = (frame * 0.35) % tile;
  const t = tile;
  return (
    <AbsoluteFill style={{opacity}}>
      <svg width={W} height={H}>
        <defs>
          <pattern id="girih" width={t} height={t} patternUnits="userSpaceOnUse" patternTransform={`translate(0 ${-drift})`}>
            <g fill="none" stroke={C.gold} strokeWidth={1.3}>
              <path d={starPath(t / 2, t / 2, t * 0.36)} />
              <circle cx={t / 2} cy={t / 2} r={t * 0.12} />
              {[0, t].map((x) => [0, t].map((y) => <path key={`${x}${y}`} d={starPath(x, y, t * 0.2, 22.5)} />))}
              <path d={`M${t / 2 - t * 0.36},${t / 2}H0M${t / 2 + t * 0.36},${t / 2}H${t}M${t / 2},${t / 2 - t * 0.36}V0M${t / 2},${t / 2 + t * 0.36}V${t}`} />
            </g>
          </pattern>
        </defs>
        <rect width={W} height={H} fill="url(#girih)" />
      </svg>
    </AbsoluteFill>
  );
};

/** Rub el Hizb medallion that draws itself in. */
export const StarMedallion: React.FC<{
  cx: number;
  cy: number;
  R: number;
  start?: number;
  spin?: number;
}> = ({cx, cy, R, start = 0, spin = 0.12}) => {
  const frame = useCurrentFrame();
  const f = frame - start;
  const rot = f * spin;
  const dotsIn = interpolate(f, [34, 56], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const glow = interpolate(f, [40, 70], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
      <defs>
        <radialGradient id="medGlow">
          <stop offset="0%" stopColor={C.gold} stopOpacity={0.32} />
          <stop offset="70%" stopColor={C.gold} stopOpacity={0.04} />
          <stop offset="100%" stopColor={C.gold} stopOpacity={0} />
        </radialGradient>
        <linearGradient id="medStroke" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor={C.goldLight} />
          <stop offset="50%" stopColor={C.gold} />
          <stop offset="100%" stopColor={C.goldDeep} />
        </linearGradient>
      </defs>
      <circle cx={cx} cy={cy} r={R * 1.6} fill="url(#medGlow)" opacity={glow} />
      <g fill="none" stroke="url(#medStroke)" strokeLinejoin="miter">
        <g transform={`rotate(${rot} ${cx} ${cy})`}>
          <path d={squarePath(cx, cy, R, 0)} pathLength={1} strokeDasharray="1 1" strokeDashoffset={drawOn(f, 0, 30)} strokeWidth={4} />
          <path d={squarePath(cx, cy, R, 45)} pathLength={1} strokeDasharray="1 1" strokeDashoffset={drawOn(f, 10, 30)} strokeWidth={4} />
          <path d={starPath(cx, cy, R * 0.86)} pathLength={1} strokeDasharray="1 1" strokeDashoffset={drawOn(f, 22, 30)} strokeWidth={1.5} opacity={0.8} />
        </g>
        <circle cx={cx} cy={cy} r={R * 0.62} pathLength={1} strokeDasharray="1 1" strokeDashoffset={drawOn(f, 18, 34)} strokeWidth={2.5} transform={`rotate(-90 ${cx} ${cy})`} />
        <circle cx={cx} cy={cy} r={R * 0.56} pathLength={1} strokeDasharray="1 1" strokeDashoffset={drawOn(f, 26, 34)} strokeWidth={1} transform={`rotate(-90 ${cx} ${cy})`} opacity={0.7} />
        <circle cx={cx} cy={cy} r={R * 1.18} pathLength={1} strokeDasharray="1 1" strokeDashoffset={drawOn(f, 30, 40)} strokeWidth={1} opacity={0.5} transform={`rotate(-90 ${cx} ${cy})`} />
      </g>
      <g transform={`rotate(${-rot * 0.6} ${cx} ${cy})`}>
        {new Array(16).fill(0).map((_, i) => {
          const a = (i * 22.5 * Math.PI) / 180;
          const k = interpolate(dotsIn, [i / 20, i / 20 + 0.25], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return (
            <path
              key={i}
              d={starPath(cx + R * 1.18 * Math.cos(a), cy + R * 1.18 * Math.sin(a), (i % 2 ? 6 : 10) * k)}
              fill={C.gold}
              opacity={k}
            />
          );
        })}
      </g>
    </svg>
  );
};

/** Gold mihrab arch outline that draws from the base up to the apex. */
export const ArchFrame: React.FC<{
  x: number;
  y: number;
  w: number;
  h: number;
  start?: number;
  dur?: number;
}> = ({x, y, w, h, start = 0, dur = 36}) => {
  const frame = useCurrentFrame();
  const f = frame - start;
  const o = drawOn(f, 0, dur);
  const pad = 16;
  const finial = interpolate(f, [dur * 0.8, dur + 12], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.back(2))});
  // Draw each side from the base up: split into two half paths.
  const half = (px: number, py: number, pw: number, ph: number, side: 1 | -1) => {
    const s = pw * 0.62;
    const xs = side === 1 ? px : px + pw;
    const xm = px + pw / 2;
    const c1 = side === 1 ? px + pw * 0.3 : px + pw * 0.7;
    return `M${xs},${py + ph} L${xs},${py + s} C${xs},${py + s * 0.42} ${c1},${py + s * 0.14} ${xm},${py}`;
  };
  return (
    <svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
      <g fill="none" stroke={C.gold} strokeLinecap="round">
        {[1, -1].map((side) => (
          <React.Fragment key={side}>
            <path d={half(x - pad, y - pad * 1.6, w + pad * 2, h + pad * 1.6, side as 1 | -1)} pathLength={1} strokeDasharray="1 1" strokeDashoffset={o} strokeWidth={3} />
            <path d={half(x, y, w, h, side as 1 | -1)} pathLength={1} strokeDasharray="1 1" strokeDashoffset={o} strokeWidth={1.2} opacity={0.85} />
            <path d={half(x - pad * 2.1, y - pad * 3.3, w + pad * 4.2, h + pad * 3.3, side as 1 | -1)} pathLength={1} strokeDasharray="0.004 0.012" strokeDashoffset={0} strokeWidth={3} opacity={0.6 * (1 - o)} />
          </React.Fragment>
        ))}
      </g>
      <g transform={`translate(${x + w / 2} ${y - pad * 1.6 - 34}) scale(${finial})`} opacity={finial}>
        <line x1={0} y1={34} x2={0} y2={14} stroke={C.gold} strokeWidth={2} />
        <path d={starPath(0, 0, 15)} fill={C.gold} />
        <circle cx={0} cy={0} r={5} fill={C.night} />
      </g>
    </svg>
  );
};

/** Thin divider: line - diamond star - line. */
export const Divider: React.FC<{y: number; width?: number; start?: number; color?: string}> = ({y, width = 420, start = 0, color = C.gold}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame - start, [0, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
  const cx = W / 2;
  const half = (width / 2 - 26) * p;
  return (
    <svg width={W} height={60} style={{position: 'absolute', left: 0, top: y - 30}}>
      <g stroke={color} strokeWidth={1.5} opacity={p}>
        <line x1={cx - 26 - half} y1={30} x2={cx - 26} y2={30} />
        <line x1={cx + 26} y1={30} x2={cx + 26 + half} y2={30} />
        <circle cx={cx - 30 - half} cy={30} r={2.5} fill={color} />
        <circle cx={cx + 30 + half} cy={30} r={2.5} fill={color} />
      </g>
      <g transform={`translate(${cx} 30) rotate(${(1 - p) * 90}) scale(${p})`}>
        <path d={starPath(0, 0, 14)} fill="none" stroke={color} strokeWidth={1.5} />
        <path d={starPath(0, 0, 6, 22.5)} fill={color} />
      </g>
    </svg>
  );
};

/** Repeating star frieze band (top / bottom border). */
export const Frieze: React.FC<{y: number; start?: number; opacity?: number}> = ({y, start = 0, opacity = 0.55}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame - start, [0, 30], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
  const step = 60;
  const n = Math.ceil(W / step) + 2;
  const shift = (frame * 0.4) % step;
  return (
    <svg width={W} height={40} style={{position: 'absolute', left: 0, top: y - 20, opacity: opacity * p}}>
      <g stroke={C.gold} fill="none" strokeWidth={1}>
        <line x1={0} y1={6} x2={W} y2={6} />
        <line x1={0} y1={34} x2={W} y2={34} />
        <g transform={`translate(${-shift} 0)`}>
          {new Array(n).fill(0).map((_, i) => (
            <React.Fragment key={i}>
              <path d={starPath(i * step, 20, 9)} />
              <path d={`M${i * step + 12},20 L${i * step + 30},10 L${i * step + 48},20 L${i * step + 30},30 Z`} opacity={0.6} />
            </React.Fragment>
          ))}
        </g>
      </g>
    </svg>
  );
};

/** Floating gold dust. Deterministic per seed. */
export const GoldDust: React.FC<{count?: number; seed?: string; opacity?: number}> = ({count = 46, seed = 'dust', opacity = 1}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none', opacity}}>
      {new Array(count).fill(0).map((_, i) => {
        const x0 = random(`${seed}x${i}`) * W;
        const speed = 0.4 + random(`${seed}s${i}`) * 1.1;
        const size = 2 + random(`${seed}r${i}`) * 4.5;
        const y = (((random(`${seed}y${i}`) * (H + 200) - frame * speed) % (H + 200)) + H + 200) % (H + 200) - 100;
        const x = x0 + Math.sin(frame / 40 + i) * 18;
        const tw = 0.35 + 0.65 * Math.abs(Math.sin(frame / (14 + (i % 7) * 3) + i));
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x,
              top: y,
              width: size,
              height: size,
              borderRadius: '50%',
              background: C.goldLight,
              boxShadow: `0 0 ${size * 3}px ${size}px rgba(214,178,94,0.45)`,
              opacity: tw * 0.75,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

/** Dark emerald backdrop with soft centre light. */
export const Backdrop: React.FC<{glowY?: number}> = ({glowY = 0.42}) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(ellipse 85% 55% at 50% ${glowY * 100}%, ${C.jade} 0%, ${C.emerald} 32%, ${C.deep} 62%, ${C.night} 100%)`,
    }}
  />
);
