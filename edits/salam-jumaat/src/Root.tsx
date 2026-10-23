import React from 'react';
import {Composition} from 'remotion';
import {SalamJumaat} from './SalamJumaat';
import {defaultProps, schema} from './schema';
import {FPS, H, TOTAL, W} from './theme';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="SalamJumaat"
    component={SalamJumaat}
    durationInFrames={TOTAL}
    fps={FPS}
    width={W}
    height={H}
    schema={schema}
    defaultProps={defaultProps}
  />
);
