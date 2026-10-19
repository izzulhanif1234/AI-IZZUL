import { lightLeak } from "@remotion/effects/light-leak";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  Interactive,
  Solid,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {
  AwarenessRibbon,
  Backdrop,
  flashAt,
  RibbonTie,
  shakeAt,
  Sparkles,
  Streaks,
} from "../fx";
import { C, FONT } from "../theme";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const pop = Easing.bezier(0.16, 1, 0.3, 1);

// 0-3 s: pink ribbon crosses the screen, then MCORP / PINK MOVE / 2026
// punch in on the beats (frames 15, 30, 45) with a small camera shake.
const OpeningInner: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const shake = shakeAt(frame, [
    [15, 28],
    [30, 10],
    [34, 10],
    [45, 18],
  ]);
  const beat = frame >= 45 ? (frame - 45) % 15 : 99;
  // Ordinary ribbon ties into the awareness loop (0-10), turns into the
  // official pink ribbon (8-11), then flies beside 2026 on the bass hit.
  const tie = interpolate(frame, [0, 10], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const morph = interpolate(frame, [8, 11], [0, 1], clamp);
  const land = interpolate(frame, [15, 27], [0, 1], { ...clamp, easing: pop });

  return (
    <>
      <Backdrop name="Backdrop" variant="burst" />
      <Streaks name="Streaks" color={C.magenta} seed={1} />

      <AbsoluteFill
        style={{
          ...shake,
          scale: interpolate(frame, [15, 95], [1, 1.06], clamp),
        }}
      >
        <RibbonTie progress={tie} x={776} y={285} scale={1.5} style={{ opacity: 1 - morph }} />
        <AwarenessRibbon
          size={interpolate(land, [0, 1], [368, 170])}
          style={{
            position: "absolute",
            left: interpolate(land, [0, 1], [776, 1665]),
            top: interpolate(land, [0, 1], [285, 640]),
            opacity: morph,
            rotate: `${interpolate(land, [0, 1], [0, 10])}deg`,
            filter: `brightness(${interpolate(frame, [8, 10, 14], [1, 1.7, 1], clamp)}) drop-shadow(0 18px 26px rgba(62,6,24,0.45))`,
          }}
        />

        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
            scale: interpolate(beat, [0, 2, 9], [1.025, 1.025, 1], clamp),
          }}
        >
          <div style={{ position: "relative", width: 1500, height: 820 }}>
            {/* MCORP */}
            <div
              style={{
                position: "absolute",
                top: 20,
                width: "100%",
                textAlign: "center",
                fontFamily: FONT.display,
                fontWeight: 900,
                fontStyle: "italic",
                fontSize: 300,
                lineHeight: 1,
                letterSpacing: -6,
                color: C.maroonDeep,
                WebkitTextStroke: `14px ${C.white}`,
                paintOrder: "stroke fill",
                textShadow: `0 18px 40px rgba(62,6,24,0.45), 0 0 60px ${C.hotPink}`,
                opacity: interpolate(frame, [13, 14], [0, 1], clamp),
                scale: interpolate(frame, [13, 15, 19, 24], [3.2, 0.92, 1.04, 1], {
                  ...clamp,
                  output: "perceptual-scale",
                }),
                filter: `blur(${interpolate(frame, [13, 15], [14, 0], clamp)}px)`,
              }}
            >
              MCORP
              {/* glint sweeping across the letters */}
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  WebkitTextStroke: "0px transparent",
                  color: "transparent",
                  backgroundImage: `linear-gradient(105deg, transparent 40%, rgba(255,255,255,0.9) 50%, transparent 60%)`,
                  backgroundSize: "300% 100%",
                  backgroundPosition: `${interpolate(frame, [58, 78], [100, -50], clamp)}% 0`,
                  WebkitBackgroundClip: "text",
                  backgroundClip: "text",
                  textShadow: "none",
                }}
              >
                MCORP
              </div>
            </div>

            {/* Maroon brush swath behind MOVE 2026, as on the poster */}
            <svg
              width={980}
              height={460}
              viewBox="0 0 980 460"
              style={{
                position: "absolute",
                top: 350,
                left: 600,
                overflow: "visible",
                clipPath: `inset(0 ${interpolate(frame, [28, 34], [100, 0], { ...clamp, easing: pop })}% 0 0)`,
              }}
            >
              <defs>
                <filter id="swathRough" x="-5%" y="-10%" width="110%" height="120%">
                  <feTurbulence type="fractalNoise" baseFrequency="0.02 0.11" numOctaves={4} seed={11} />
                  <feDisplacementMap in="SourceGraphic" scale={80} />
                </filter>
              </defs>
              <g filter="url(#swathRough)" transform="rotate(-9 490 230)">
                <path d="M10 170 C 120 110, 700 80, 960 70 L 930 270 C 640 280, 260 300, 70 290 Z" fill={C.maroonDeep} />
                <path d="M170 300 C 380 250, 700 240, 900 250 L 870 410 C 640 400, 400 420, 220 400 Z" fill={C.maroon} />
              </g>
            </svg>

            {/* PINK: the poster's own brush lettering */}
            <Img
              src={staticFile("img/title-pink.png")}
              style={{
                position: "absolute",
                top: 285,
                left: 10,
                width: 820,
                filter: "drop-shadow(0 0 3px rgba(255,255,255,0.9)) drop-shadow(0 14px 22px rgba(62,6,24,0.45))",
                opacity: interpolate(frame, [26, 27], [0, 1], clamp),
                translate: interpolate(
                  frame,
                  [26, 31, 35],
                  ["-1300px 0px", "40px 0px", "0px 0px"],
                  { ...clamp, easing: pop },
                ),
              }}
            />

            {/* MOVE */}
            <Img
              src={staticFile("img/title-move.png")}
              style={{
                position: "absolute",
                top: 395,
                left: 800,
                width: 700,
                filter: "drop-shadow(0 12px 18px rgba(36,2,14,0.5))",
                opacity: interpolate(frame, [30, 31], [0, 1], clamp),
                translate: interpolate(
                  frame,
                  [30, 35, 39],
                  ["1300px 0px", "-40px 0px", "0px 0px"],
                  { ...clamp, easing: pop },
                ),
              }}
            />

            {/* 2026 */}
            <Img
              src={staticFile("img/title-2026.png")}
              style={{
                position: "absolute",
                top: 615,
                left: 1030,
                width: 410,
                filter: `drop-shadow(0 12px 18px rgba(36,2,14,0.5)) drop-shadow(0 0 22px ${C.hotPink})`,
                opacity: interpolate(frame, [41, 43], [0, 1], clamp),
                rotate: interpolate(frame, [41, 47], ["-10deg", "0deg"], { ...clamp, easing: pop }),
                scale: interpolate(frame, [41, 45, 49, 53], [2.8, 0.9, 1.05, 1], {
                  ...clamp,
                  output: "perceptual-scale",
                }),
              }}
            />

          </div>
        </AbsoluteFill>
      </AbsoluteFill>

      {/* Logo plate top left, as on the poster */}
      <div
        style={{
          position: "absolute",
          top: 60,
          left: 80,
          padding: "14px 22px",
          borderRadius: 18,
          backgroundColor: "rgba(255,255,255,0.92)",
          boxShadow: "0 10px 30px rgba(62,6,24,0.25)",
          opacity: interpolate(frame, [52, 60], [0, 1], clamp),
          translate: interpolate(frame, [52, 60], ["0px -30px", "0px 0px"], {
            ...clamp,
            easing: pop,
          }),
        }}
      >
        <Img src={staticFile("img/logo.png")} style={{ height: 96, display: "block" }} />
      </div>

      {/* Pink light leak blooming after the title lands */}
      <Solid
        width={width}
        height={height}
        style={{ position: "absolute", inset: 0, mixBlendMode: "screen", opacity: 0.45 }}
        effects={[
          lightLeak({
            seed: 3,
            hueShift: 70,
            progress: interpolate(frame, [44, 95], [0, 0.4], clamp),
          }),
        ]}
      />

      <Sparkles name="Sparkles" count={18} color={C.white} seed={1} />

      <AbsoluteFill
        style={{
          backgroundColor: C.white,
          opacity: Math.max(flashAt(frame, 15, 7) * 0.7, flashAt(frame, 45, 6) * 0.45),
        }}
      />
    </>
  );
};

export const Opening = Interactive.create({
  Component: OpeningInner,
  layout: "absolute-fill",
});
