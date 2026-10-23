import React from 'react';
import {AbsoluteFill, Easing, interpolate, random, useCurrentFrame} from 'remotion';
import {H, W} from '../theme';

export type Pal = {
  skyTop: string;
  skyMid: string;
  skyLow: string;
  dawn: string;
  dawnLight: string;
  ink: string;
  panel: string;
  accent: string;
  gold: string;
  goldLight: string;
  goldDeep: string;
  ivory: string;
};

const GOLD = {gold: '#e6bb5f', goldLight: '#fde9b4', goldDeep: '#a97a26', ivory: '#fff7e6'};

export const PALETTES: Record<'biru' | 'marun', Pal> = {
  // Biru diraja + fajar: night sky warming to dawn, Iznik turquoise accent.
  biru: {
    skyTop: '#070f2b',
    skyMid: '#132a66',
    skyLow: '#2c4c98',
    dawn: '#f39b55',
    dawnLight: '#ffd9a0',
    ink: '#081230',
    panel: 'rgba(7,15,43,0.74)',
    accent: '#3cc0b8',
    ...GOLD,
  },
  // Merah marun ala bangunan merah Melaka.
  marun: {
    skyTop: '#1c0408',
    skyMid: '#4a0b17',
    skyLow: '#7c1a2a',
    dawn: '#f39a52',
    dawnLight: '#ffd49a',
    ink: '#1f050a',
    panel: 'rgba(31,5,10,0.74)',
    accent: '#3bb3a8',
    ...GOLD,
  },
};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** Ogee (onion) arch inside x,y,w,h. */
export const ogeePath = (x: number, y: number, w: number, h: number, s = w * 0.66) =>
  [
    `M${x},${y + h}`,
    `L${x},${y + s}`,
    `C${x},${y + s * 0.3} ${x + w * 0.45},${y + s * 0.34} ${x + w / 2},${y}`,
    `C${x + w * 0.55},${y + s * 0.34} ${x + w},${y + s * 0.3} ${x + w},${y + s}`,
    `L${x + w},${y + h}`,
    'Z',
  ].join(' ');

/** Night-to-dawn sky with twinkling stars. `dawn` 0..1 lifts the warm glow. */
export const Sky: React.FC<{P: Pal; dawn: number}> = ({P, dawn}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{background: `linear-gradient(to bottom, ${P.skyTop} 0%, ${P.skyMid} 46%, ${P.skyLow} 78%, ${P.skyLow} 100%)`}} />
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 95% 38% at 50% 100%, ${P.dawnLight} 0%, ${P.dawn} 30%, rgba(0,0,0,0) 72%)`,
          opacity: 0.35 + 0.65 * dawn,
        }}
      />
      <AbsoluteFill style={{opacity: 1 - dawn * 0.55}}>
        {new Array(70).fill(0).map((_, i) => {
          const x = random(`sx${i}`) * W;
          const y = random(`sy${i}`) * H * 0.55;
          const s = 1.2 + random(`ss${i}`) * 2.6;
          const tw = 0.3 + 0.7 * Math.abs(Math.sin(frame / (18 + (i % 9) * 4) + i * 1.7));
          return (
            <div
              key={i}
              style={{position: 'absolute', left: x, top: y, width: s, height: s, borderRadius: '50%', background: '#fff', opacity: tw * 0.85, boxShadow: `0 0 ${s * 3}px rgba(255,255,255,0.6)`}}
            />
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Mosque skyline silhouette along the bottom edge with a thin gold rim. */
export const Skyline: React.FC<{P: Pal; start?: number; y?: number}> = ({P, start = 0, y = 0}) => {
  const frame = useCurrentFrame();
  const rise = interpolate(frame - start, [0, 40], [260, 0], {...clamp, easing: Easing.out(Easing.cubic)});
  const g = 1770; // ground
  const minaret = (cx: number, top: number) =>
    `M${cx - 22},${g} L${cx - 22},${top + 120} L${cx - 34},${top + 110} L${cx + 34},${top + 110} L${cx + 22},${top + 120} L${cx + 22},${g} Z ` +
    `M${cx - 18},${top + 110} L${cx - 18},${top + 60} L${cx + 18},${top + 60} L${cx + 18},${top + 110} Z ` +
    `M${cx - 24},${top + 60} L${cx},${top} L${cx + 24},${top + 60} Z`;
  const dome = (cx: number, base: number, w: number, hgt: number) =>
    `M${cx - w / 2},${base} C${cx - w / 2},${base - hgt * 0.75} ${cx - w * 0.12},${base - hgt * 0.8} ${cx},${base - hgt} C${cx + w * 0.12},${base - hgt * 0.8} ${cx + w / 2},${base - hgt * 0.75} ${cx + w / 2},${base} Z`;
  const d = [
    dome(540, 1610, 380, 230),
    `M370,1610 L710,1610 L710,${g} L370,${g} Z`,
    dome(265, 1680, 190, 120),
    `M180,1680 L350,1680 L350,${g} L180,${g} Z`,
    dome(815, 1680, 190, 120),
    `M730,1680 L900,1680 L900,${g} L730,${g} Z`,
    minaret(95, 1390),
    minaret(985, 1390),
    `M0,${g} L${W},${g} L${W},${H} L0,${H} Z`,
  ].join(' ');
  return (
    <svg width={W} height={H} style={{position: 'absolute', inset: 0, transform: `translateY(${rise + y}px)`}}>
      <path d={d} fill={P.ink} stroke={P.gold} strokeOpacity={0.55} strokeWidth={2} />
      <line x1={540} y1={1380} x2={540} y2={1335} stroke={P.gold} strokeWidth={3} />
      <circle cx={540} cy={1322} r={10} fill="none" stroke={P.gold} strokeWidth={3} />
      {[440, 490, 540, 590, 640].map((x) => (
        <path key={x} d={`M${x - 12},1700 L${x - 12},1670 Q${x},1650 ${x + 12},1670 L${x + 12},1700 Z`} fill={P.dawn} opacity={0.75} />
      ))}
    </svg>
  );
};

/** Ogee arch border: turquoise tile band between gold rules, beaded outer edge. */
export const OgeeFrame: React.FC<{x: number; y: number; w: number; h: number; P: Pal; start?: number; dur?: number}> = ({
  x,
  y,
  w,
  h,
  P,
  start = 0,
  dur = 36,
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame - start, [0, dur], [0, 1], {...clamp, easing: Easing.bezier(0.45, 0, 0.2, 1)});
  const pad = 14;
  const dash = {pathLength: 1, strokeDasharray: '1 1', strokeDashoffset: 1 - p};
  return (
    <svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
      <path d={ogeePath(x - pad, y - pad * 1.5, w + pad * 2, h + pad * 1.5)} fill="none" stroke={P.accent} strokeWidth={14} {...dash} />
      <path d={ogeePath(x - pad, y - pad * 1.5, w + pad * 2, h + pad * 1.5)} fill="none" stroke={P.goldLight} strokeWidth={2} strokeDasharray="2 12" opacity={p} />
      <path d={ogeePath(x, y, w, h)} fill="none" stroke={P.gold} strokeWidth={3} {...dash} />
      <path d={ogeePath(x - pad * 2, y - pad * 3, w + pad * 4, h + pad * 3)} fill="none" stroke={P.gold} strokeWidth={3} {...dash} />
      <path
        d={ogeePath(x - pad * 3, y - pad * 4.6, w + pad * 6, h + pad * 4.6)}
        fill="none"
        stroke={P.gold}
        strokeWidth={7}
        strokeLinecap="round"
        strokeDasharray="0 22"
        opacity={p}
      />
    </svg>
  );
};

/** Bottom edge of a media band cut as a row of pointed valance scallops. */
export const valancePath = (bandH: number, n = 6, depth = 56) => {
  const seg = W / n;
  let d = `M0,0 L${W},0 L${W},${bandH}`;
  for (let i = n; i > 0; i--) {
    const x = i * seg;
    d += ` Q${x - seg * 0.08},${bandH + depth} ${x - seg / 2},${bandH + depth} Q${x - seg * 0.92},${bandH + depth} ${x - seg},${bandH}`;
  }
  return d + ' Z';
};

/** Row of small ogee arches across the top edge, drawn in one after another. */
export const TopArcade: React.FC<{P: Pal; start?: number; y?: number; n?: number}> = ({P, start = 0, y = 96, n = 7}) => {
  const frame = useCurrentFrame();
  const w = W / n;
  const h = 104;
  return (
    <svg width={W} height={y + h + 40} style={{position: 'absolute', left: 0, top: 0}}>
      <line x1={0} y1={y + h} x2={W} y2={y + h} stroke={P.gold} strokeWidth={2} opacity={interpolate(frame - start, [0, 20], [0, 0.9], clamp)} />
      <line x1={0} y1={y + h + 10} x2={W} y2={y + h + 10} stroke={P.accent} strokeWidth={4} opacity={interpolate(frame - start, [6, 26], [0, 0.8], clamp)} />
      {new Array(n).fill(0).map((_, i) => {
        const mid = Math.abs(i - (n - 1) / 2);
        const p = interpolate(frame - start - mid * 4, [0, 26], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
        const x = i * w;
        return (
          <g key={i} opacity={p}>
            <path d={ogeePath(x + 10, y, w - 20, h, (w - 20) * 0.7)} fill={P.ink} fillOpacity={0.35} stroke={P.gold} strokeWidth={2} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - p} />
            <path d={ogeePath(x + 22, y + 18, w - 44, h - 18, (w - 44) * 0.7)} fill="none" stroke={P.accent} strokeWidth={1.5} opacity={0.8} />
            <circle cx={x + w / 2} cy={y - 10} r={4} fill={P.gold} />
          </g>
        );
      })}
    </svg>
  );
};
