import { Composition, Folder } from "remotion";
import { PinkMoveTeaser } from "./PinkMoveTeaser";
import { DressCode } from "./scenes/DressCode";
import { Info } from "./scenes/Info";
import { Mandatory } from "./scenes/Mandatory";
import { Opening } from "./scenes/Opening";
import { Tagline } from "./scenes/Tagline";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="PinkMoveTeaser"
        component={PinkMoveTeaser}
        durationInFrames={450}
        fps={30}
        width={1920}
        height={1080}
      />
      <Folder name="Scenes">
        <Composition
          id="Opening"
          component={Opening}
          durationInFrames={95}
          fps={30}
          width={1920}
          height={1080}
        />
        <Composition
          id="Tagline"
          component={Tagline}
          durationInFrames={100}
          fps={30}
          width={1920}
          height={1080}
        />
        <Composition
          id="Info"
          component={Info}
          durationInFrames={160}
          fps={30}
          width={1920}
          height={1080}
        />
        <Composition
          id="DressCode"
          component={DressCode}
          durationInFrames={70}
          fps={30}
          width={1920}
          height={1080}
        />
        <Composition
          id="Mandatory"
          component={Mandatory}
          durationInFrames={65}
          fps={30}
          width={1920}
          height={1080}
        />
      </Folder>
    </>
  );
};
