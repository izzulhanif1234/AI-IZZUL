import { Audio } from "@remotion/media";
import { linearTiming, TransitionSeries } from "@remotion/transitions";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Finish, pinkSlash } from "./fx";
import { DressCode } from "./scenes/DressCode";
import { Info } from "./scenes/Info";
import { Mandatory } from "./scenes/Mandatory";
import { Opening } from "./scenes/Opening";
import { Tagline } from "./scenes/Tagline";
import { C, HALF_WIPE, WIPE } from "./theme";

const wipe = linearTiming({
  durationInFrames: WIPE,
  easing: Easing.bezier(0.7, 0, 0.3, 1),
});

const sfx = (name: string) => staticFile(`audio/${name}.wav`);

// 15 s, 16:9 teaser. Scene cuts at 3, 6, 11 and 13 s sit on the music's
// beat grid; each wipe is centred on its cut, so every middle scene
// carries HALF_WIPE extra frames on both sides.
export const PinkMoveTeaser: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: C.maroonDeep }}>
      <TransitionSeries name="Scenes">
        <TransitionSeries.Sequence name="1 Opening" durationInFrames={3 * fps + HALF_WIPE}>
          <Opening name="Opening" />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={pinkSlash({ direction: "right" })} timing={wipe} />
        <TransitionSeries.Sequence name="2 Tagline" durationInFrames={3 * fps + WIPE}>
          <Tagline name="Tagline" />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={pinkSlash({ direction: "left" })} timing={wipe} />
        <TransitionSeries.Sequence name="3 Info" durationInFrames={5 * fps + WIPE}>
          <Info name="Info" />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={pinkSlash({ direction: "right" })} timing={wipe} />
        <TransitionSeries.Sequence name="4 Dress code" durationInFrames={2 * fps + WIPE}>
          <DressCode name="Dress code" />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={pinkSlash({ direction: "left" })} timing={wipe} />
        <TransitionSeries.Sequence name="5 Mandatory" durationInFrames={2 * fps + HALF_WIPE}>
          <Mandatory name="Mandatory" />
        </TransitionSeries.Sequence>
      </TransitionSeries>

      <Finish name="Grain + vignette" />

      {/* Music: 120 BPM bed, dips for a breath before the final stamp. */}
      <Audio
        name="Music"
        src={staticFile("audio/music.wav")}
        volume={interpolate(
          frame,
          [0, 2, 396, 398, 404, 405, 436, 450],
          [0, 0.9, 0.9, 0.12, 0.12, 0.9, 0.9, 0],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
        )}
      />

      {/* Scene 1: ribbon swoosh, riser into the title, bass hits */}
      <Audio name="Ribbon whoosh" from={0} src={sfx("whoosh")} volume={0.8} />
      <Audio name="Ribbon swoosh" from={0} src={sfx("swoosh")} volume={0.6} />
      <Audio name="Riser" from={0} src={sfx("riser")} volume={0.45} />
      <Audio name="Bass hit MCORP" from={0.5 * fps} src={sfx("bass-hit")} volume={1} />
      <Audio name="Whip PINK" from={1 * fps} src={sfx("whip")} volume={0.45} />
      <Audio name="Whip MOVE" from={1 * fps + 4} src={sfx("whip")} volume={0.45} />
      <Audio name="Bass hit 2026" from={1.5 * fps} src={sfx("bass-hit")} volume={0.7} />

      {/* Swoosh on every transition, peaking on the cut */}
      <Audio name="Swoosh 3s" from={3 * fps - 7} src={sfx("swoosh")} volume={0.9} />
      <Audio name="Whoosh 3s" from={3 * fps - 3} src={sfx("whoosh")} volume={0.6} />
      <Audio name="Swoosh 6s" from={6 * fps - 7} src={sfx("swoosh")} volume={0.9} />
      <Audio name="Whoosh 6s" from={6 * fps - 3} src={sfx("whoosh")} volume={0.6} />
      <Audio name="Swoosh 11s" from={11 * fps - 7} src={sfx("swoosh")} volume={0.9} />
      <Audio name="Whoosh 11s" from={11 * fps - 3} src={sfx("whoosh")} volume={0.6} />
      <Audio name="Swoosh 13s" from={13 * fps - 7} src={sfx("swoosh")} volume={0.9} />
      <Audio name="Whoosh 13s" from={13 * fps - 3} src={sfx("whoosh")} volume={0.6} />

      {/* Scene 2: a tick per word, soft swoosh under the tagline */}
      <Audio name="Whip ZUMBA" from={3 * fps} src={sfx("whip")} volume={0.4} />
      <Audio name="Whip FITNESS" from={3.5 * fps} src={sfx("whip")} volume={0.4} />
      <Audio name="Whip AWARENESS" from={4 * fps} src={sfx("whip")} volume={0.4} />
      <Audio name="Swoosh tagline" from={4.5 * fps} src={sfx("swoosh")} volume={0.35} />

      {/* Scene 3: ding when the date lands, whips for the other cards */}
      <Audio name="Ding date" from={6 * fps + 12} src={sfx("ding")} volume={0.9} />
      <Audio name="Whip time card" from={6 * fps + 26} src={sfx("whip")} volume={0.5} />
      <Audio name="Whip place card" from={6 * fps + 48} src={sfx("whip")} volume={0.5} />

      {/* Scene 4: shirt lands, tudung pops */}
      <Audio name="Shirt thump" from={11 * fps + 9} src={sfx("bass-hit")} volume={0.35} />
      <Audio name="Whip tudung" from={11 * fps + 18} src={sfx("whip")} volume={0.5} />

      {/* Scene 5: logo pop, riser into the DIWAJIBKAN stamp */}
      <Audio name="Whip logo" from={13 * fps - 2} src={sfx("whip")} volume={0.5} />
      <Audio name="Riser stamp" from={13 * fps} src={sfx("riser")} volume={0.55} />
      <Audio name="Bass hit stamp" from={13.5 * fps} src={sfx("bass-hit")} volume={1} />
    </AbsoluteFill>
  );
};
