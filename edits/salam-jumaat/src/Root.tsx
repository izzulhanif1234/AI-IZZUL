import React from 'react';
import {Composition} from 'remotion';
import {SalamJumaat} from './SalamJumaat';
import {SalamJumaatB} from './b/SalamJumaatB';
import {defaultProps, schema} from './schema';
import {FPS, H, TOTAL, W} from './theme';

const common = {durationInFrames: TOTAL, fps: FPS, width: W, height: H, schema, defaultProps};

export const RemotionRoot: React.FC = () => (
  <>
    {/* Design A: zamrud + emas, star wipe */}
    <Composition id="SalamJumaat" component={SalamJumaat} {...common} />
    {/* Design B: langit biru diraja / marun + fajar, gerbang ogee, siluet masjid */}
    <Composition id="SalamJumaatB" component={SalamJumaatB} {...common} />
  </>
);
