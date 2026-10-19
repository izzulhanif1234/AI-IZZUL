import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  Interactive,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { Backdrop, flashAt, shakeAt, Sparkles, Streaks } from "../fx";
import { C, FONT, HALF_WIPE } from "../theme";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const pop = Easing.bezier(0.16, 1, 0.3, 1);

const Word: React.FC<{ readonly at: number; readonly f: number; readonly children: string }> = ({
  at,
  f,
  children,
}) => (
  <span
    style={{
      display: "inline-block",
      opacity: interpolate(f, [at - 1, at], [0, 1], clamp),
      scale: interpolate(f, [at - 1, at + 3, at + 7], [2.4, 0.94, 1], {
        ...clamp,
        output: "perceptual-scale",
      }),
      filter: `blur(${interpolate(f, [at - 1, at + 3], [10, 0], clamp)}px)`,
      textShadow: `0 0 ${interpolate(f, [at, at + 10], [40, 0], clamp)}px ${C.white}`,
    }}
  >
    {children}
  </span>
);

const Dot: React.FC<{ readonly at: number; readonly f: number }> = ({ at, f }) => (
  <span
    style={{
      display: "inline-block",
      width: 24,
      height: 24,
      borderRadius: 12,
      backgroundColor: C.hotPink,
      boxShadow: `0 0 18px ${C.hotPink}`,
      margin: "0 34px",
      verticalAlign: "middle",
      scale: interpolate(f, [at, at + 4, at + 7], [0, 1.5, 1], clamp),
    }}
  />
);

// 3-6 s: ZUMBA • FITNESS • AWARENESS land one per beat, then the
// tagline writes on. Participants rise in from below.
const TaglineInner: React.FC = () => {
  const f = useCurrentFrame() - HALF_WIPE;
  const shake = shakeAt(f, [
    [0, 9],
    [15, 9],
    [30, 12],
  ]);

  return (
    <>
      <Backdrop name="Backdrop" variant="dark" />
      <Streaks name="Streaks" color={C.magenta} seed={2} />

      {/* Outlined marquee behind the people */}
      <div
        style={{
          position: "absolute",
          top: 470,
          left: 0,
          whiteSpace: "nowrap",
          fontFamily: FONT.display,
          fontWeight: 900,
          fontStyle: "italic",
          fontSize: 300,
          lineHeight: 1,
          color: "transparent",
          WebkitTextStroke: `3px ${C.hotPink}`,
          opacity: 0.35,
          translate: `${-200 - f * 9}px 0px`,
        }}
      >
        PINK MOVE • PINK MOVE • PINK MOVE • PINK MOVE
      </div>

      <AbsoluteFill style={shake}>
        {/* Participants */}
        <div
          style={{
            position: "absolute",
            left: 960 - 760,
            top: 360,
            width: 1520,
            height: 850,
            translate: interpolate(f, [-4, 10], ["0px 420px", "0px 0px"], {
              ...clamp,
              easing: pop,
            }),
            scale: interpolate(f, [10, 95], [1, 1.07], clamp),
          }}
        >
          <div
            style={{
              position: "absolute",
              inset: "10% 12% 0 12%",
              background: `radial-gradient(ellipse at 50% 60%, ${C.magenta} 0%, transparent 65%)`,
              opacity: 0.7,
              filter: "blur(30px)",
            }}
          />
          <Img
            src={staticFile("img/people-cut.png")}
            style={{
              position: "absolute",
              width: "100%",
              height: "100%",
              objectFit: "contain",
              objectPosition: "50% 0%",
              filter: "drop-shadow(0 20px 40px rgba(36,2,14,0.6))",
              maskImage: "linear-gradient(to bottom, black 70%, transparent 96%)",
            }}
          />
        </div>

        {/* Pill bar with the three words */}
        <div
          style={{
            position: "absolute",
            top: 110,
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
          }}
        >
          <div
            style={{
              padding: "26px 60px",
              borderRadius: 999,
              background: `linear-gradient(90deg, ${C.maroonDeep}, ${C.maroon}, ${C.maroonDeep})`,
              border: `4px solid ${C.hotPink}`,
              boxShadow: `0 0 40px rgba(230,0,126,0.55), 0 20px 50px rgba(0,0,0,0.45)`,
              fontFamily: FONT.body,
              fontWeight: 900,
              fontSize: 84,
              lineHeight: 1,
              letterSpacing: 6,
              color: C.white,
              whiteSpace: "nowrap",
              scale: interpolate(f, [-3, 2], [0, 1], { ...clamp, easing: pop }),
            }}
          >
            <Word at={0} f={f}>
              ZUMBA
            </Word>
            <Dot at={13} f={f} />
            <Word at={15} f={f}>
              FITNESS
            </Word>
            <Dot at={28} f={f} />
            <Word at={30} f={f}>
              AWARENESS
            </Word>
          </div>
        </div>

        {/* Tagline */}
        <div
          style={{
            position: "absolute",
            top: 262,
            left: 0,
            right: 0,
            textAlign: "center",
            fontFamily: FONT.script,
            fontSize: 112,
            lineHeight: 1.2,
            color: C.white,
            textShadow: `0 6px 0 ${C.magenta}, 0 14px 30px rgba(0,0,0,0.5)`,
            clipPath: `inset(-20% ${interpolate(f, [45, 63], [100, 0], {
              ...clamp,
              easing: Easing.inOut(Easing.quad),
            })}% -20% 0)`,
            scale: interpolate(f, [60, 62, 70, 75, 77, 85], [1, 1.04, 1, 1, 1.03, 1], clamp),
          }}
        >
          ~ Satu Rentak, Seribu Semangat ~
        </div>
      </AbsoluteFill>

      <Sparkles name="Sparkles" count={22} color={C.pinkSoft} seed={2} />

      <AbsoluteFill
        style={{
          backgroundColor: C.white,
          opacity: Math.max(flashAt(f, 0, 5) * 0.5, flashAt(f, 15, 5) * 0.35, flashAt(f, 30, 5) * 0.35),
        }}
      />
    </>
  );
};

export const Tagline = Interactive.create({
  Component: TaglineInner,
  layout: "absolute-fill",
});
