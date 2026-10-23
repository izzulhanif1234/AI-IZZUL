import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {FONT, H, W, WIPE} from '../theme';
import {Divider, GoldDust, PatternBg} from '../ornaments';
import {GoldText, KenBurns, SmallCaps, useFade, Words} from '../effects';
import type {Props} from '../schema';
import {ogeePath, OgeeFrame, Pal, Skyline, Sky, TopArcade, valancePath} from './ornamentsB';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const outCubic = Easing.out(Easing.cubic);
const center: React.CSSProperties = {position: 'absolute', left: 0, width: W, textAlign: 'center'};
const RUQAA = "'Aref Ruqaa', serif";
const PLAYFAIR = "'Playfair Display', serif";

type SceneProps = {p: Props; P: Pal; dur: number};

/** Scene transition: the new scene opens through a growing ogee arch. */
export const ArchIris: React.FC<{P: Pal; children: React.ReactNode}> = ({P, children}) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [0, WIPE], [0, 1], {...clamp, easing: Easing.bezier(0.65, 0, 0.25, 1)});
  if (t >= 1) return <AbsoluteFill>{children}</AbsoluteFill>;
  const w = 60 + t * 3600;
  const h = w * 1.5;
  const d = ogeePath(W / 2 - w / 2, 1150 - h * 0.6, w, h);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{clipPath: `path('${d}')`}}>{children}</AbsoluteFill>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <path d={d} fill="none" stroke={P.accent} strokeWidth={14} opacity={1 - t * 0.5} />
        <path d={d} fill="none" stroke={P.goldLight} strokeWidth={4} opacity={1 - t * 0.4} />
      </svg>
    </AbsoluteFill>
  );
};

/** Media clipped to an ogee arch. */
const OgeeWindow: React.FC<{x: number; y: number; w: number; h: number; P: Pal; start?: number; children: React.ReactNode}> = ({
  x,
  y,
  w,
  h,
  P,
  start = 0,
  children,
}) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame - start, [0, 24], [0, 1], clamp);
  const s = interpolate(frame - start, [0, 60], [1.16, 1], {...clamp, easing: outCubic});
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, clipPath: `path('${ogeePath(0, 0, w, h)}')`, opacity: o, background: P.ink}}>
      <AbsoluteFill style={{transform: `scale(${s})`}}>{children}</AbsoluteFill>
      <AbsoluteFill style={{background: `linear-gradient(to bottom, transparent 72%, ${P.ink}88 100%)`}} />
    </div>
  );
};

const Panel: React.FC<{P: Pal; top: number; height: number; start?: number}> = ({P, top, height, start = 0}) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame - start, [0, 20], [0, 1], clamp);
  return (
    <div
      style={{
        position: 'absolute',
        left: 60,
        width: W - 120,
        top,
        height,
        borderRadius: 28,
        background: P.panel,
        border: `2px solid ${P.gold}`,
        boxShadow: `inset 0 0 0 8px ${P.panel}, inset 0 0 0 10px ${P.accent}99, 0 24px 60px rgba(0,0,0,0.35)`,
        opacity: o,
        transform: `translateY(${(1 - o) * 30}px)`,
      }}
    />
  );
};

/* 1. Pembuka ------------------------------------------------------- */

export const IntroB: React.FC<SceneProps> = ({p, P, dur}) => {
  const frame = useCurrentFrame();
  const exit = interpolate(frame, [dur - 34, dur], [1, 1.06], {...clamp, easing: Easing.in(Easing.quad)});
  const calli = interpolate(frame, [22, 66], [100, 0], {...clamp, easing: Easing.inOut(Easing.quad)});
  const salamIn = interpolate(frame, [62, 80], [0, 1], clamp);
  const [line1, ...rest] = p.salam.split(' ');
  const line2 = rest.join(' ');
  return (
    <AbsoluteFill style={{opacity: interpolate(frame, [0, 12], [0, 1], clamp)}}>
      <Sky P={P} dawn={interpolate(frame, [0, dur], [0.15, 0.45])} />
      <PatternBg opacity={0.06} />
      <Skyline P={P} start={8} y={170} />
      <TopArcade P={P} start={6} />
      <AbsoluteFill style={{transform: `scale(${exit})`}}>
        <div style={{...center, top: 520, fontFamily: RUQAA, fontWeight: 700, fontSize: 150, lineHeight: 1.4, direction: 'rtl', clipPath: `inset(-30% 0 -30% ${calli}%)`}}>
          <GoldText shineAt={80}>جمعة مباركة</GoldText>
        </div>
        <Divider y={830} width={460} start={58} />
        <div style={{...center, top: 870, fontFamily: PLAYFAIR, fontStyle: 'italic', fontWeight: 500, fontSize: 84, color: P.ivory, opacity: salamIn, transform: `translateY(${(1 - salamIn) * 24}px)`}}>
          {line1.charAt(0) + line1.slice(1).toLowerCase()}
        </div>
        <div style={{...center, top: 975, fontFamily: PLAYFAIR, fontWeight: 700, fontSize: 168, letterSpacing: '0.06em', lineHeight: 1}}>
          {line2.split('').map((ch, i) => {
            const f = frame - 72 - i * 4;
            return (
              <span
                key={i}
                style={{
                  display: 'inline-block',
                  opacity: interpolate(f, [0, 12], [0, 1], clamp),
                  transform: `translateY(${interpolate(f, [0, 18], [50, 0], {...clamp, easing: outCubic})}px)`,
                  filter: `blur(${interpolate(f, [0, 12], [8, 0], clamp)}px)`,
                }}
              >
                <GoldText shineAt={108 - 72 + i * 4}>{ch}</GoldText>
              </span>
            );
          })}
        </div>
      </AbsoluteFill>
      <GoldDust seed="bintro" count={34} opacity={interpolate(frame, [20, 60], [0, 0.8], clamp)} />
    </AbsoluteFill>
  );
};

/* 2. Ayat ---------------------------------------------------------- */

export const AyatB: React.FC<SceneProps> = ({p, P}) => {
  const frame = useCurrentFrame();
  const win = {x: 180, y: 300, w: 720, h: 640};
  const reveal = interpolate(frame, [40, 88], [100, 0], {...clamp, easing: Easing.inOut(Easing.quad)});
  const refIn = interpolate(frame, [168, 186], [0, 1], clamp);
  return (
    <AbsoluteFill>
      <Sky P={P} dawn={0.4} />
      <PatternBg opacity={0.06} />
      <Skyline P={P} start={-60} y={190} />
      <TopArcade P={P} start={-60} />
      <OgeeWindow {...win} P={P} start={4}>
        <OffthreadVideo src={staticFile('media/drone_logo.mp4')} muted playbackRate={0.9} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </OgeeWindow>
      <OgeeFrame {...win} P={P} start={6} dur={40} />
      <Panel P={P} top={1010} height={560} start={20} />
      <div style={{...center, top: 1036, fontFamily: FONT.arabic, fontWeight: 700, fontSize: 80, lineHeight: 1.5, direction: 'rtl', clipPath: `inset(-20% 0 -20% ${reveal}%)`}}>
        <GoldText shineAt={95}>{p.ayat}</GoldText>
      </div>
      <Words
        text={`“${p.terjemahan}”`}
        start={98}
        stagger={3}
        style={{...center, top: 1196, padding: '0 110px', boxSizing: 'border-box', fontFamily: FONT.serif, fontStyle: 'italic', fontWeight: 500, fontSize: 50, lineHeight: 1.22, color: P.ivory}}
      />
      <Divider y={1440} width={340} start={158} />
      <SmallCaps style={{...center, top: 1474, color: P.goldLight, opacity: refIn, transform: `translateY(${(1 - refIn) * 12}px)`}}>{p.rujukan}</SmallCaps>
      <GoldDust seed="bayat" count={22} opacity={0.6} />
    </AbsoluteFill>
  );
};

/* 3. Doa (1) ------------------------------------------------------- */

const Clip: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => (
  <AbsoluteFill style={{opacity: useFade(dur, 12, 12)}}>{children}</AbsoluteFill>
);

const BAND = 1000;

export const Doa1B: React.FC<SceneProps> = ({p, P, dur}) => {
  const frame = useCurrentFrame();
  const [head, ...body] = p.doa1.split(',');
  const edge = valancePath(BAND);
  return (
    <AbsoluteFill>
      <Sky P={P} dawn={0.55} />
      <PatternBg opacity={0.06} />
      <Skyline P={P} start={-60} y={200} />
      <AbsoluteFill style={{height: BAND + 60, clipPath: `path('${edge}')`, background: P.ink}}>
        <Sequence durationInFrames={96}>
          <Clip dur={96}>
            <AbsoluteFill style={{transform: `scale(${interpolate(frame, [0, 96], [1.04, 1.12])})`}}>
              <OffthreadVideo src={staticFile('media/drone_entrance.mp4')} muted playbackRate={0.85} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
            </AbsoluteFill>
          </Clip>
        </Sequence>
        <Sequence from={84} durationInFrames={92}>
          <Clip dur={92}>
            <KenBurns src="media/drone5.jpg" dur={92} from={1.02} to={1.12} x={[2, -2]} />
          </Clip>
        </Sequence>
        <Sequence from={164} durationInFrames={dur - 164 + 12}>
          <Clip dur={dur - 164 + 12}>
            <KenBurns src="media/drone8.jpg" dur={dur - 164} from={1.06} to={1.14} />
          </Clip>
        </Sequence>
        <AbsoluteFill style={{background: `linear-gradient(to bottom, ${P.ink}aa 0%, transparent 24%, transparent 80%, ${P.ink}66 100%)`}} />
      </AbsoluteFill>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <path d={edge} fill="none" stroke={P.accent} strokeWidth={10} />
        <path d={edge} fill="none" stroke={P.gold} strokeWidth={3} />
      </svg>
      <TopArcade P={P} start={-60} />
      <div style={{...center, top: 1120, fontFamily: PLAYFAIR, fontWeight: 700, fontSize: 84, opacity: interpolate(frame, [18, 34], [0, 1], clamp)}}>
        <GoldText shineAt={30}>{head.trim()},</GoldText>
      </div>
      <Words
        text={body.join(',').trim()}
        start={34}
        stagger={4}
        gold={['Melaka']}
        style={{...center, top: 1238, padding: '0 90px', boxSizing: 'border-box', fontFamily: FONT.serif, fontWeight: 600, fontSize: 62, lineHeight: 1.22, color: P.ivory}}
      />
      <GoldDust seed="bdoa1" count={18} opacity={0.6} />
    </AbsoluteFill>
  );
};

/* 4. Doa (2) ------------------------------------------------------- */

const KEY_AT = [34, 82, 130];

const Medallion: React.FC<{cx: number; cy: number; r: number; src: string; pos: string; at: number; P: Pal}> = ({cx, cy, r, src, pos, at, P}) => {
  const frame = useCurrentFrame();
  const ring = interpolate(frame, [4, 30], [0, 1], {...clamp, easing: outCubic});
  const f = frame - at;
  const on = interpolate(f, [0, 14], [0, 1], clamp);
  const s = interpolate(f, [0, 22], [1.35, 1.05], {...clamp, easing: outCubic}) + interpolate(f, [22, 120], [0, 0.08], clamp);
  const pop = interpolate(f, [0, 8, 20], [1, 1.08, 1], clamp);
  return (
    <div style={{position: 'absolute', left: cx - r, top: cy - r, width: r * 2, height: r * 2, transform: `scale(${(0.85 + 0.15 * ring) * pop})`, opacity: ring}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: '50%', overflow: 'hidden', background: P.ink}}>
        <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: pos, opacity: on, transform: `scale(${s})`}} />
      </div>
      <svg width={r * 2 + 60} height={r * 2 + 60} style={{position: 'absolute', left: -30, top: -30, overflow: 'visible'}}>
        <circle cx={r + 30} cy={r + 30} r={r + 7} fill="none" stroke={P.accent} strokeWidth={10} />
        <circle cx={r + 30} cy={r + 30} r={r + 1} fill="none" stroke={P.gold} strokeWidth={3} />
        <circle cx={r + 30} cy={r + 30} r={r + 14} fill="none" stroke={P.gold} strokeWidth={3} />
        <circle cx={r + 30} cy={r + 30} r={r + 24} fill="none" stroke={P.goldLight} strokeWidth={5} strokeLinecap="round" strokeDasharray="0 17" opacity={0.4 + 0.6 * on} />
      </svg>
      <div style={{position: 'absolute', inset: -40, borderRadius: '50%', boxShadow: `0 0 70px 10px ${P.dawn}`, opacity: interpolate(f, [0, 6, 30], [0, 0.8, 0.25], clamp), pointerEvents: 'none'}} />
    </div>
  );
};

const Keyword: React.FC<{text: string; at: number; top: number}> = ({text, at, top}) => {
  const frame = useCurrentFrame();
  const f = frame - at;
  return (
    <div
      style={{
        ...center,
        top,
        fontFamily: PLAYFAIR,
        fontWeight: 700,
        fontSize: 86,
        letterSpacing: '0.04em',
        lineHeight: '108px',
        opacity: interpolate(f, [0, 10], [0, 1], clamp),
        transform: `scale(${interpolate(f, [0, 18], [1.3, 1], {...clamp, easing: outCubic})})`,
        filter: `blur(${interpolate(f, [0, 12], [12, 0], clamp)}px)`,
      }}
    >
      <GoldText shineAt={at + 6}>{text}</GoldText>
    </div>
  );
};

export const Doa2B: React.FC<SceneProps> = ({p, P, dur}) => {
  const frame = useCurrentFrame();
  const [k1, k2, k3] = p.doa2Kata;
  const lineIn = (at: number) => interpolate(frame - at, [0, 14], [0, 1], clamp);
  return (
    <AbsoluteFill>
      <Sky P={P} dawn={interpolate(frame, [0, dur], [0.6, 0.85])} />
      <PatternBg opacity={0.07} />
      <Skyline P={P} start={-60} y={200} />
      <TopArcade P={P} start={-60} />
      <Medallion cx={196} cy={500} r={130} src="media/drone7.jpg" pos="58% 50%" at={KEY_AT[0]} P={P} />
      <Medallion cx={540} cy={500} r={130} src="media/drone2.jpg" pos="18% 50%" at={KEY_AT[1]} P={P} />
      <Medallion cx={884} cy={500} r={130} src="media/drone9.jpg" pos="76% 50%" at={KEY_AT[2]} P={P} />
      <div style={{...center, top: 700, fontFamily: FONT.serif, fontStyle: 'italic', fontWeight: 500, fontSize: 62, color: P.ivory, opacity: lineIn(12)}}>{p.doa2Pembuka}</div>
      <Keyword text={`${k1.toUpperCase()},`} at={KEY_AT[0]} top={782} />
      <Keyword text={k2.toUpperCase()} at={KEY_AT[1]} top={892} />
      <div style={{...center, top: 1006, fontFamily: FONT.serif, fontStyle: 'italic', fontWeight: 500, fontSize: 52, color: P.ivory, opacity: lineIn(KEY_AT[2] - 8) * 0.85}}>dan</div>
      <Keyword text={k3.toUpperCase()} at={KEY_AT[2]} top={1064} />
      <Words text={p.doa2Penutup} start={172} stagger={4} style={{...center, top: 1196, fontFamily: FONT.serif, fontStyle: 'italic', fontWeight: 500, fontSize: 60, color: P.ivory}} />
      <Divider y={1320} width={420} start={186} />
      <GoldDust seed="bdoa2" count={26} opacity={0.7} />
    </AbsoluteFill>
  );
};

/* 5. Penutup ------------------------------------------------------- */

export const EndB: React.FC<SceneProps> = ({p, P, dur}) => {
  const frame = useCurrentFrame();
  const win = {x: 240, y: 330, w: 600, h: 560};
  const plaque = interpolate(frame, [24, 44], [0, 1], {...clamp, easing: outCubic});
  const title = interpolate(frame, [42, 60], [0, 1], clamp);
  return (
    <AbsoluteFill>
      <Sky P={P} dawn={0.9} />
      <PatternBg opacity={0.07} />
      <Skyline P={P} start={-60} y={150} />
      <TopArcade P={P} start={-60} />
      <OgeeWindow {...win} P={P} start={2}>
        <KenBurns src="media/bangunan.jpg" dur={dur} from={1.0} to={1.1} x={[4, 4]} />
      </OgeeWindow>
      <OgeeFrame {...win} P={P} start={4} dur={34} />
      <div
        style={{
          position: 'absolute',
          left: W / 2 - 220,
          top: 960,
          width: 440,
          height: 196,
          borderRadius: 26,
          background: `linear-gradient(160deg, #ffffff 0%, ${P.ivory} 60%, #f3e6c8 100%)`,
          boxShadow: `0 0 0 3px ${P.gold}, 0 0 0 10px ${P.accent}, 0 0 0 13px ${P.gold}, 0 24px 60px rgba(0,0,0,0.4)`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          opacity: plaque,
          transform: `translateY(${(1 - plaque) * 40}px) scale(${0.92 + 0.08 * plaque})`,
        }}
      >
        <Img src={staticFile('media/logo.png')} style={{height: 142}} />
      </div>
      <div style={{...center, top: 1186, fontFamily: RUQAA, fontWeight: 700, fontSize: 96, lineHeight: 1.4, direction: 'rtl', opacity: title, transform: `translateY(${(1 - title) * 20}px)`}}>
        <GoldText shineAt={70}>جمعة مباركة</GoldText>
      </div>
      <div style={{...center, top: 1340, fontFamily: PLAYFAIR, fontStyle: 'italic', fontWeight: 500, fontSize: 56, color: P.ivory, opacity: interpolate(frame, [56, 74], [0, 1], clamp)}}>
        {p.salam.charAt(0) + p.salam.slice(1).toLowerCase().replace(/ (\w)/g, (_, c) => ' ' + c.toUpperCase())}
      </div>
      <GoldDust seed="bend" count={30} opacity={0.8} />
    </AbsoluteFill>
  );
};
