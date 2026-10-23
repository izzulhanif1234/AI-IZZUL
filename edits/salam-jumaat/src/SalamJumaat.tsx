import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, staticFile} from 'remotion';
import {StarReveal} from './effects';
import {loadFonts} from './fonts';
import {Ayat, Doa1, Doa2, End, Intro} from './scenes';
import type {Props} from './schema';
import {C, SCENES, TOTAL} from './theme';

loadFonts();

const Sfx: React.FC<{at: number; src: string; volume?: number}> = ({at, src, volume = 0.5}) => (
  <Sequence from={at} layout="none">
    <Audio src={staticFile(src)} volume={volume} />
  </Sequence>
);

export const SalamJumaat: React.FC<Props> = (p) => {
  const {intro, ayat, doa1, doa2, end} = SCENES;
  return (
    <AbsoluteFill style={{background: C.night}}>
      <Sequence from={intro.from} durationInFrames={intro.dur}>
        <Intro p={p} dur={intro.dur} />
      </Sequence>
      <Sequence from={ayat.from} durationInFrames={ayat.dur}>
        <StarReveal>
          <Ayat p={p} dur={ayat.dur} />
        </StarReveal>
      </Sequence>
      <Sequence from={doa1.from} durationInFrames={doa1.dur}>
        <StarReveal>
          <Doa1 p={p} dur={doa1.dur} />
        </StarReveal>
      </Sequence>
      <Sequence from={doa2.from} durationInFrames={doa2.dur}>
        <StarReveal>
          <Doa2 p={p} dur={doa2.dur} />
        </StarReveal>
      </Sequence>
      <Sequence from={end.from} durationInFrames={end.dur}>
        <StarReveal>
          <End p={p} dur={end.dur} />
        </StarReveal>
      </Sequence>

      <Soundtrack muzik={p.muzik} />
    </AbsoluteFill>
  );
};

/** Music bed + SFX, shared by both designs (same scene timings). */
export const Soundtrack: React.FC<{muzik: boolean}> = ({muzik}) => {
  const {ayat, doa1, doa2, end} = SCENES;
  return (
    <>
        {muzik && (
          <Audio
            src={staticFile('music/bed.wav')}
            volume={(f) => interpolate(f, [0, 30, TOTAL - 50, TOTAL], [0, 0.6, 0.6, 0], {extrapolateRight: 'clamp'})}
          />
        )}
        <Sfx at={30} src="sfx/sparkle.mp3" volume={0.35} />
        {[ayat.from, doa1.from, doa2.from, end.from].map((t) => (
          <Sfx key={t} at={t - 4} src="sfx/whoosh-short.mp3" volume={0.45} />
        ))}
        {[34, 82, 130].map((t) => (
          <Sfx key={t} at={doa2.from + t} src="sfx/chime.mp3" volume={0.16} />
        ))}
        <Sfx at={end.from + 28} src="sfx/sparkle.mp3" volume={0.35} />
    </>
  );
};
