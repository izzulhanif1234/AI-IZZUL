import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {C, FONT, W} from './theme';
import {ArchFrame, archPath, Backdrop, Divider, Frieze, GoldDust, PatternBg, starPath, StarMedallion} from './ornaments';
import {GoldText, KenBurns, SmallCaps, useFade, Words} from './effects';
import type {Props} from './schema';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const outCubic = Easing.out(Easing.cubic);

const center: React.CSSProperties = {position: 'absolute', left: 0, width: W, textAlign: 'center'};

/** Media clipped to a mihrab arch, opening with a gentle zoom. */
const ArchWindow: React.FC<{x: number; y: number; w: number; h: number; start?: number; children: React.ReactNode}> = ({
  x,
  y,
  w,
  h,
  start = 0,
  children,
}) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame - start, [0, 26], [0, 1], clamp);
  const s = interpolate(frame - start, [0, 60], [1.18, 1], {...clamp, easing: outCubic});
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, clipPath: `path('${archPath(0, 0, w, h)}')`, opacity: o}}>
      <AbsoluteFill style={{transform: `scale(${s})`}}>{children}</AbsoluteFill>
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 80% 70% at 50% 45%, transparent 55%, rgba(6,21,18,0.55) 100%), linear-gradient(to bottom, transparent 70%, rgba(6,21,18,0.45) 100%)`,
        }}
      />
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* 1. SALAM JUMAAT                                                     */
/* ------------------------------------------------------------------ */

export const Intro: React.FC<{p: Props; dur: number}> = ({p, dur}) => {
  const frame = useCurrentFrame();
  const fadeIn = interpolate(frame, [0, 14], [0, 1], clamp);
  const exit = interpolate(frame, [dur - 34, dur], [1, 1.07], {...clamp, easing: Easing.in(Easing.quad)});
  const arabicIn = interpolate(frame, [44, 66], [0, 1], clamp);
  const [line1, ...rest] = p.salam.split(' ');
  const line2 = rest.join(' ');
  return (
    <AbsoluteFill style={{opacity: fadeIn}}>
      <Backdrop glowY={0.4} />
      <PatternBg opacity={interpolate(frame, [10, 50], [0, 0.1], clamp)} />
      <Frieze y={170} start={20} />
      <Frieze y={1640} start={26} />
      <AbsoluteFill style={{transform: `scale(${exit})`}}>
        <StarMedallion cx={W / 2} cy={760} R={190} start={6} />
        <div
          style={{
            ...center,
            top: 760 - 92,
            fontFamily: FONT.arabic,
            fontWeight: 700,
            fontSize: 62,
            lineHeight: 1.18,
            direction: 'rtl',
            opacity: arabicIn,
            transform: `scale(${0.85 + 0.15 * arabicIn})`,
          }}
        >
          <GoldText shineAt={70}>
            جمعة
            <br />
            مباركة
          </GoldText>
        </div>
        <div style={{...center, top: 1060, fontFamily: FONT.display, fontWeight: 500, fontSize: 60, letterSpacing: '0.55em', paddingLeft: '0.55em', color: C.ivory}}>
          {line1.split('').map((ch, i) => {
            const f = frame - 52 - i * 3;
            return (
              <span key={i} style={{display: 'inline-block', opacity: interpolate(f, [0, 12], [0, 1], clamp), transform: `translateY(${interpolate(f, [0, 16], [26, 0], {...clamp, easing: outCubic})}px)`}}>
                {ch}
              </span>
            );
          })}
        </div>
        <div style={{...center, top: 1135, fontFamily: FONT.display, fontWeight: 700, fontSize: 170, letterSpacing: '0.04em', lineHeight: 1}}>
          {line2.split('').map((ch, i) => {
            const f = frame - 62 - i * 4;
            return (
              <span
                key={i}
                style={{
                  display: 'inline-block',
                  opacity: interpolate(f, [0, 14], [0, 1], clamp),
                  transform: `translateY(${interpolate(f, [0, 20], [60, 0], {...clamp, easing: outCubic})}px) scale(${interpolate(f, [0, 20], [1.25, 1], {...clamp, easing: outCubic})})`,
                  filter: `blur(${interpolate(f, [0, 14], [10, 0], clamp)}px)`,
                }}
              >
                <GoldText shineAt={100 - 62 + i * 4}>{ch}</GoldText>
              </span>
            );
          })}
        </div>
        <Divider y={1365} width={520} start={96} />
      </AbsoluteFill>
      <GoldDust seed="intro" opacity={interpolate(frame, [20, 60], [0, 1], clamp)} />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* 2. AYAT                                                             */
/* ------------------------------------------------------------------ */

export const Ayat: React.FC<{p: Props; dur: number}> = ({p}) => {
  const frame = useCurrentFrame();
  const arch = {x: 140, y: 280, w: 800, h: 740};
  const reveal = interpolate(frame, [38, 88], [100, 0], {...clamp, easing: Easing.inOut(Easing.quad)});
  const refIn = interpolate(frame, [168, 186], [0, 1], clamp);
  return (
    <AbsoluteFill>
      <Backdrop glowY={0.3} />
      <PatternBg opacity={0.08} />
      <Frieze y={170} />
      <ArchWindow {...arch} start={4}>
        <OffthreadVideo src={staticFile('media/drone_logo.mp4')} muted playbackRate={0.9} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </ArchWindow>
      <ArchFrame {...arch} start={6} dur={40} />
      <div
        style={{
          ...center,
          top: 1068,
          fontFamily: FONT.arabic,
          fontWeight: 700,
          fontSize: 82,
          lineHeight: 1.5,
          direction: 'rtl',
          clipPath: `inset(-20% 0 -20% ${reveal}%)`,
        }}
      >
        <GoldText shineAt={95}>{p.ayat}</GoldText>
      </div>
      <Words
        text={`“${p.terjemahan}”`}
        start={98}
        stagger={3}
        style={{...center, top: 1232, padding: '0 90px', boxSizing: 'border-box', fontFamily: FONT.serif, fontStyle: 'italic', fontWeight: 500, fontSize: 52, lineHeight: 1.22, color: C.ivory}}
      />
      <Divider y={1470} width={360} start={158} />
      <SmallCaps style={{...center, top: 1505, opacity: refIn, transform: `translateY(${(1 - refIn) * 12}px)`}}>{p.rujukan}</SmallCaps>
      <GoldDust seed="ayat" count={30} opacity={0.8} />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* 3. DOA (1) - full-bleed montage                                     */
/* ------------------------------------------------------------------ */

const Clip: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
  const o = useFade(dur, 12, 12);
  return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};

const MEDIA_H = 1110;

export const Doa1: React.FC<{p: Props; dur: number}> = ({p, dur}) => {
  const frame = useCurrentFrame();
  const [head, ...body] = p.doa1.split(',');
  return (
    <AbsoluteFill style={{background: C.night}}>
      <AbsoluteFill style={{height: MEDIA_H}}>
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
          <KenBurns src="media/drone8.jpg" dur={dur - 164} from={1.06} to={1.14} y={[0, 2]} />
        </Clip>
      </Sequence>
      <AbsoluteFill
        style={{
          background: `linear-gradient(to bottom, rgba(6,21,18,0.5) 0%, rgba(6,21,18,0) 22%, rgba(6,21,18,0) 62%, ${C.night} 100%)`,
        }}
      />
      </AbsoluteFill>
      <AbsoluteFill style={{top: MEDIA_H - 2, background: `radial-gradient(ellipse 80% 60% at 50% 0%, ${C.deep} 0%, ${C.night} 100%)`}} />
      <PatternBg opacity={0.06} />
      <ArchFrame x={70} y={150} w={940} h={1660} start={4} dur={44} />
      <div style={{...center, top: 1120, fontFamily: FONT.display, fontWeight: 700, fontSize: 80, opacity: interpolate(frame, [18, 34], [0, 1], clamp)}}>
        <GoldText shineAt={30}>{head.trim()},</GoldText>
      </div>
      <Words
        text={body.join(',').trim()}
        start={34}
        stagger={4}
        gold={['Melaka']}
        style={{...center, top: 1238, padding: '0 90px', boxSizing: 'border-box', fontFamily: FONT.serif, fontWeight: 600, fontSize: 62, lineHeight: 1.22, color: C.ivory}}
      />
      <GoldDust seed="doa1" count={22} opacity={0.6} />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* 4. DOA (2) - three keywords                                         */
/* ------------------------------------------------------------------ */

const KEY_AT = [34, 82, 130];

const Keyword: React.FC<{text: string; at: number; top: number}> = ({text, at, top}) => {
  const frame = useCurrentFrame();
  const f = frame - at;
  const o = interpolate(f, [0, 10], [0, 1], clamp);
  const s = interpolate(f, [0, 18], [1.35, 1], {...clamp, easing: outCubic});
  const blur = interpolate(f, [0, 12], [14, 0], clamp);
  const spark = interpolate(f, [4, 16, 34], [0, 1, 0.55], clamp);
  return (
    <div style={{...center, top, height: 110}}>
      <div style={{fontFamily: FONT.display, fontWeight: 700, fontSize: 88, letterSpacing: '0.03em', lineHeight: '110px', opacity: o, transform: `scale(${s})`, filter: `blur(${blur}px)`}}>
        <GoldText shineAt={at + 6}>{text}</GoldText>
      </div>
      <svg width={W} height={110} style={{position: 'absolute', inset: 0, opacity: spark}}>
        <path d={starPath(70, 55, 12 * spark)} fill={C.goldLight} />
        <path d={starPath(W - 70, 55, 12 * spark)} fill={C.goldLight} />
      </svg>
    </div>
  );
};

export const Doa2: React.FC<{p: Props; dur: number}> = ({p, dur}) => {
  const frame = useCurrentFrame();
  const [k1, k2, k3] = p.doa2Kata;
  const flash = KEY_AT.reduce((a, t) => a + interpolate(frame - t, [-2, 2, 18], [0, 0.32, 0], clamp), 0);
  const bgs: {src: string; from: number; to: number; x: [number, number]; y?: [number, number]}[] = [
    {src: 'media/drone7.jpg', from: 0, to: KEY_AT[1] + 4, x: [-4, -6], y: [3, -1]},
    {src: 'media/drone2.jpg', from: KEY_AT[1] - 6, to: KEY_AT[2] + 4, x: [-26, -30]},
    {src: 'media/drone9.jpg', from: KEY_AT[2] - 6, to: dur, x: [24, 20]},
  ];
  const lineIn = (at: number) => interpolate(frame - at, [0, 14], [0, 1], clamp);
  return (
    <AbsoluteFill style={{background: C.night}}>
      {bgs.map((b, i) => (
        <Sequence key={i} from={b.from} durationInFrames={b.to - b.from + 6}>
          <Clip dur={b.to - b.from + 6}>
            <KenBurns src={b.src} dur={b.to - b.from} from={1.1} to={1.2} x={b.x} y={b.y} style={{filter: 'blur(2px)'}} />
          </Clip>
        </Sequence>
      ))}
      <AbsoluteFill style={{background: 'rgba(6,21,18,0.58)'}} />
      <AbsoluteFill style={{background: `radial-gradient(ellipse 75% 34% at 50% 45%, rgba(6,21,18,0.6) 0%, rgba(6,21,18,0.3) 60%, rgba(6,21,18,0) 100%), radial-gradient(ellipse 120% 80% at 50% 50%, transparent 50%, rgba(6,21,18,0.85) 100%)`}} />
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% 46%, ${C.goldLight} 0%, transparent 55%)`, opacity: flash, mixBlendMode: 'screen'}} />
      <PatternBg opacity={0.06} />
      <Frieze y={170} />
      <div style={{...center, top: 560, fontFamily: FONT.serif, fontStyle: 'italic', fontWeight: 500, fontSize: 64, color: C.ivory, opacity: lineIn(12), transform: `translateY(${(1 - lineIn(12)) * 18}px)`}}>
        {p.doa2Pembuka}
      </div>
      <Keyword text={`${k1.toUpperCase()},`} at={KEY_AT[0]} top={660} />
      <Keyword text={k2.toUpperCase()} at={KEY_AT[1]} top={780} />
      <div style={{...center, top: 902, fontFamily: FONT.serif, fontStyle: 'italic', fontWeight: 500, fontSize: 52, color: C.ivoryDim, opacity: lineIn(KEY_AT[2] - 8)}}>dan</div>
      <Keyword text={k3.toUpperCase()} at={KEY_AT[2]} top={968} />
      <Words
        text={p.doa2Penutup}
        start={172}
        stagger={4}
        style={{...center, top: 1112, fontFamily: FONT.serif, fontStyle: 'italic', fontWeight: 500, fontSize: 60, color: C.ivory}}
      />
      <Divider y={1240} width={420} start={186} />
      <GoldDust seed="doa2" count={34} />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* 5. End card                                                         */
/* ------------------------------------------------------------------ */

export const End: React.FC<{p: Props; dur: number}> = ({p, dur}) => {
  const frame = useCurrentFrame();
  const arch = {x: 200, y: 300, w: 680, h: 640};
  const plaque = interpolate(frame, [26, 46], [0, 1], {...clamp, easing: outCubic});
  const title = interpolate(frame, [44, 62], [0, 1], clamp);
  return (
    <AbsoluteFill>
      <Backdrop glowY={0.36} />
      <PatternBg opacity={0.09} />
      <Frieze y={170} />
      <Frieze y={1640} />
      <ArchWindow {...arch} start={2}>
        <KenBurns src="media/bangunan.jpg" dur={dur} from={1.0} to={1.1} x={[4, 4]} />
      </ArchWindow>
      <ArchFrame {...arch} start={4} dur={36} />
      <div
        style={{
          position: 'absolute',
          left: W / 2 - 230,
          top: 1010,
          width: 460,
          height: 210,
          borderRadius: 26,
          background: `linear-gradient(160deg, #fffaf0 0%, ${C.ivory} 60%, #efe3c4 100%)`,
          boxShadow: `0 0 0 2px ${C.gold}, 0 0 0 9px rgba(214,178,94,0.18), 0 22px 60px rgba(0,0,0,0.45)`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          opacity: plaque,
          transform: `translateY(${(1 - plaque) * 40}px) scale(${0.92 + 0.08 * plaque})`,
        }}
      >
        <Img src={staticFile('media/logo.png')} style={{height: 150}} />
      </div>
      <div style={{...center, top: 1290, fontFamily: FONT.display, fontWeight: 700, fontSize: 80, letterSpacing: '0.06em', opacity: title, transform: `translateY(${(1 - title) * 20}px)`}}>
        <GoldText shineAt={70}>{p.salam}</GoldText>
      </div>
      <div style={{...center, top: 1395, fontFamily: FONT.arabic, fontWeight: 700, fontSize: 54, direction: 'rtl', opacity: interpolate(frame, [58, 76], [0, 1], clamp)}}>
        <GoldText shineAt={84}>جمعة مباركة</GoldText>
      </div>
      <GoldDust seed="end" count={40} />
    </AbsoluteFill>
  );
};

