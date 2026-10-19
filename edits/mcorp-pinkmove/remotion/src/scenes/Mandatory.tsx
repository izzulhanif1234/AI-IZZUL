import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  Interactive,
  staticFile,
  useCurrentFrame,
} from "remotion";
import {
  AwarenessRibbon,
  Backdrop,
  flashAt,
  RibbonPath,
  shakeAt,
  Sparkles,
  Streaks,
} from "../fx";
import { C, FONT, HALF_WIPE } from "../theme";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const pop = Easing.bezier(0.16, 1, 0.3, 1);

const PeopleIcon: React.FC = () => (
  <svg width={92} height={70} viewBox="0 0 46 35" fill={C.white}>
    <circle cx="23" cy="9" r="7" />
    <path d="M10 35c0-8 6-13 13-13s13 5 13 13z" />
    <circle cx="8" cy="12" r="5" opacity="0.85" />
    <path d="M0 33c0-6 4-10 9-10 2 0 3 .4 4 1-3 2.5-5 6-5 9z" opacity="0.85" />
    <circle cx="38" cy="12" r="5" opacity="0.85" />
    <path d="M46 33c0-6-4-10-9-10-2 0-3 .4-4 1 3 2.5 5 6 5 9z" opacity="0.85" />
  </svg>
);

// 13-15 s: the call to action. Logo pops, line one rises, and
// DIWAJIBKAN lands like a rubber stamp on the beat (frame 15, 13.5 s).
const MandatoryInner: React.FC = () => {
  const f = useCurrentFrame() - HALF_WIPE;
  const shake = shakeAt(f, [
    [0, 8],
    [15, 30],
  ]);

  return (
    <>
      <Backdrop name="Backdrop" variant="dark" />
      <AbsoluteFill
        style={{
          background: `repeating-conic-gradient(from ${f * 0.8}deg at 50% 32%, rgba(230,0,126,0.22) 0deg 7deg, transparent 7deg 15deg)`,
          maskImage: "radial-gradient(ellipse 70% 70% at 50% 32%, black 10%, transparent 75%)",
        }}
      />
      <Streaks name="Streaks" color={C.magenta} seed={5} />

      <AbsoluteFill style={shake}>
        <div style={{ position: "absolute", inset: 0, opacity: 0.85 }}>
          <RibbonPath
            progress={interpolate(f, [16, 36], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) })}
            wave={f * 0.08}
            thickness={90}
          />
        </div>

        {/* Logo plate */}
        <div
          style={{
            position: "absolute",
            top: 90,
            left: 960 - 250,
            width: 500,
            height: 300,
            borderRadius: 36,
            backgroundColor: C.white,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            overflow: "hidden",
            boxShadow: `0 0 0 8px ${C.magenta}, 0 0 60px rgba(255,63,164,0.7), 0 30px 60px rgba(0,0,0,0.5)`,
            scale: interpolate(f, [-2, 4, 8], [0, 1.12, 1], { ...clamp, output: "perceptual-scale" }),
            rotate: interpolate(f, [-2, 8], ["-12deg", "0deg"], { ...clamp, easing: pop }),
          }}
        >
          <Img src={staticFile("img/logo.png")} style={{ width: 410 }} />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background:
                "linear-gradient(110deg, transparent 35%, rgba(255,63,164,0.35) 50%, transparent 65%)",
              translate: `${interpolate(f, [24, 40], [-120, 120], clamp)}% 0`,
            }}
          />
        </div>

        {/* Pink ribbon beside the logo */}
        <AwarenessRibbon
          size={150}
          style={{
            position: "absolute",
            top: 100,
            left: 1250,
            rotate: interpolate(f, [4, 12], ["40deg", "10deg"], { ...clamp, easing: pop }),
            scale: interpolate(f, [4, 9, 12], [0, 1.15, 1], clamp),
            filter: "drop-shadow(0 14px 22px rgba(0,0,0,0.5))",
          }}
        />
        <AwarenessRibbon
          size={150}
          style={{
            position: "absolute",
            top: 100,
            left: 520,
            rotate: interpolate(f, [6, 14], ["-40deg", "-10deg"], { ...clamp, easing: pop }),
            scale: interpolate(f, [6, 11, 14], [0, 1.15, 1], clamp),
            filter: "drop-shadow(0 14px 22px rgba(0,0,0,0.5))",
          }}
        />

        {/* Line one */}
        <div
          style={{
            position: "absolute",
            top: 460,
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 30,
            clipPath: "inset(-10% -5% -10% -5%)",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 30,
              opacity: interpolate(f, [3, 6], [0, 1], clamp),
              translate: interpolate(f, [3, 10], ["0px 90px", "0px 0px"], { ...clamp, easing: pop }),
            }}
          >
            <PeopleIcon />
            <div style={{ width: 4, height: 80, backgroundColor: C.hotPink }} />
            <div
              style={{
                fontFamily: FONT.body,
                fontWeight: 900,
                fontSize: 58,
                letterSpacing: 2,
                color: C.white,
                whiteSpace: "nowrap",
              }}
            >
              KEHADIRAN SEMUA WARGA KERJA MCORP
            </div>
          </div>
        </div>

        {/* Stamp line */}
        <div
          style={{
            position: "absolute",
            top: 590,
            left: 0,
            right: 0,
            textAlign: "center",
            whiteSpace: "nowrap",
            fontFamily: FONT.display,
            fontWeight: 900,
            fontStyle: "italic",
            fontSize: 150,
            lineHeight: 1.1,
            color: C.white,
            opacity: interpolate(f, [12, 13], [0, 1], clamp),
            scale: interpolate(f, [12, 15, 18, 22], [3, 0.92, 1.04, 1], {
              ...clamp,
              output: "perceptual-scale",
            }),
            rotate: interpolate(f, [12, 16], ["-10deg", "-3deg"], { ...clamp, easing: pop }),
            textShadow: "0 18px 40px rgba(0,0,0,0.5)",
          }}
        >
          ADALAH{" "}
          <span
            style={{
              display: "inline-block",
              padding: "0 30px",
              border: `8px solid ${C.hotPink}`,
              borderRadius: 24,
              color: C.magenta,
              WebkitTextStroke: `8px ${C.white}`,
              paintOrder: "stroke fill",
              boxShadow: `0 0 40px rgba(255,63,164,0.6), inset 0 0 30px rgba(255,63,164,0.35)`,
            }}
          >
            DIWAJIBKAN
          </span>
        </div>
      </AbsoluteFill>

      <Sparkles name="Sparkles" count={26} color={C.pinkSoft} seed={5} />

      <AbsoluteFill
        style={{
          backgroundColor: C.white,
          opacity: flashAt(f, 15, 7) * 0.55,
        }}
      />
    </>
  );
};

export const Mandatory = Interactive.create({
  Component: MandatoryInner,
  layout: "absolute-fill",
});
