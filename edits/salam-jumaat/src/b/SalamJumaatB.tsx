import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {loadFonts} from '../fonts';
import type {Props} from '../schema';
import {Soundtrack} from '../SalamJumaat';
import {SCENES} from '../theme';
import {PALETTES} from './ornamentsB';
import {ArchIris, AyatB, Doa1B, Doa2B, EndB, IntroB} from './scenesB';

loadFonts();

export const SalamJumaatB: React.FC<Props> = (p) => {
  const P = PALETTES[p.tema];
  const {intro, ayat, doa1, doa2, end} = SCENES;
  return (
    <AbsoluteFill style={{background: P.skyTop}}>
      <Sequence from={intro.from} durationInFrames={intro.dur}>
        <IntroB p={p} P={P} dur={intro.dur} />
      </Sequence>
      <Sequence from={ayat.from} durationInFrames={ayat.dur}>
        <ArchIris P={P}>
          <AyatB p={p} P={P} dur={ayat.dur} />
        </ArchIris>
      </Sequence>
      <Sequence from={doa1.from} durationInFrames={doa1.dur}>
        <ArchIris P={P}>
          <Doa1B p={p} P={P} dur={doa1.dur} />
        </ArchIris>
      </Sequence>
      <Sequence from={doa2.from} durationInFrames={doa2.dur}>
        <ArchIris P={P}>
          <Doa2B p={p} P={P} dur={doa2.dur} />
        </ArchIris>
      </Sequence>
      <Sequence from={end.from} durationInFrames={end.dur}>
        <ArchIris P={P}>
          <EndB p={p} P={P} dur={end.dur} />
        </ArchIris>
      </Sequence>
      <Soundtrack muzik={p.muzik} />
    </AbsoluteFill>
  );
};
