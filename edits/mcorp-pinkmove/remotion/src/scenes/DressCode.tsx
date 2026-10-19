import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  Interactive,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { shakeAt, Sparkles, Streaks } from "../fx";
import { C, FONT, HALF_WIPE } from "../theme";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const pop = Easing.bezier(0.16, 1, 0.3, 1);

const slideUp = (f: number, at: number) => ({
  opacity: interpolate(f, [at, at + 3], [0, 1], clamp),
  translate: interpolate(f, [at, at + 6], ["0px 50px", "0px 0px"], { ...clamp, easing: pop }),
});

// 11-13 s: dress code on the poster's light-pink card. The maroon
// TeamSync Retreat tee drops in; the pink tudung example pops on the right.
const DressCodeInner: React.FC = () => {
  const f = useCurrentFrame() - HALF_WIPE;
  const shake = shakeAt(f, [
    [9, 10],
    [28, 8],
  ]);

  return (
    <>
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 80% 90% at 40% 40%, ${C.white} 0%, ${C.blush} 40%, ${C.pinkSoft} 100%)`,
        }}
      />
      <AbsoluteFill
        style={{
          backgroundImage: "radial-gradient(circle, rgba(230,0,126,0.22) 2px, transparent 2.6px)",
          backgroundSize: "22px 22px",
          maskImage: "linear-gradient(120deg, black 0%, transparent 45%, transparent 60%, black 100%)",
        }}
      />
      <Streaks name="Streaks" color={C.hotPink} seed={4} />

      <AbsoluteFill style={shake}>
        {/* Shirt drop */}
        <div
          style={{
            position: "absolute",
            left: 640 - 300,
            top: 700,
            width: 600,
            height: 60,
            borderRadius: "50%",
            background: "radial-gradient(ellipse, rgba(62,6,24,0.35), transparent 70%)",
            scale: interpolate(f, [0, 9], [0.3, 1], clamp),
          }}
        />
        <Img
          src={staticFile("img/shirt.png")}
          style={{
            position: "absolute",
            left: 640 - 360,
            top: 46,
            width: 720,
            filter: "drop-shadow(0 26px 30px rgba(62,6,24,0.35))",
            translate: interpolate(f, [-2, 9, 13], ["0px -900px", "0px 18px", "0px 0px"], {
              ...clamp,
              easing: Easing.in(Easing.quad),
            }),
            rotate: interpolate(f, [-2, 9, 15], ["-14deg", "2deg", "0deg"], clamp),
          }}
        />

        {/* Pakaian text */}
        <div style={{ position: "absolute", left: 80, top: 760, width: 1120, textAlign: "center" }}>
          <div
            style={{
              display: "inline-block",
              padding: "8px 28px",
              borderRadius: 999,
              backgroundColor: C.magenta,
              color: C.white,
              fontFamily: FONT.body,
              fontWeight: 900,
              fontSize: 40,
              letterSpacing: 4,
              ...slideUp(f, 5),
            }}
          >
            PAKAIAN
          </div>
          <div
            style={{
              marginTop: 14,
              fontFamily: FONT.display,
              fontWeight: 900,
              fontStyle: "italic",
              fontSize: 76,
              lineHeight: 1.02,
              color: C.maroon,
              ...slideUp(f, 8),
            }}
          >
            T-SHIRT MAROON PROGRAM
          </div>
          <div
            style={{
              fontFamily: FONT.display,
              fontWeight: 900,
              fontStyle: "italic",
              fontSize: 76,
              lineHeight: 1.02,
              color: C.maroon,
              ...slideUp(f, 11),
            }}
          >
            MCORP TEAMSYNC RETREAT
          </div>
        </div>

        {/* Divider */}
        <div
          style={{
            position: "absolute",
            left: 1236,
            top: 140,
            width: 6,
            height: 800,
            borderRadius: 3,
            backgroundColor: C.magenta,
            opacity: 0.6,
            scale: `1 ${interpolate(f, [2, 14], [0, 1], { ...clamp, easing: pop })}`,
          }}
        />

        {/* Perempuan: tudung pink */}
        <div style={{ position: "absolute", left: 1290, top: 110, width: 560, textAlign: "center" }}>
          <div
            style={{
              margin: "0 auto",
              width: 430,
              height: 430,
              borderRadius: "50%",
              padding: 12,
              background: `conic-gradient(from ${f * 6}deg, ${C.magenta}, ${C.hotPink}, ${C.maroon}, ${C.magenta})`,
              boxShadow: "0 24px 50px rgba(62,6,24,0.35)",
              scale: interpolate(f, [18, 24, 28], [0, 1.12, 1], { ...clamp, output: "perceptual-scale" }),
              rotate: interpolate(f, [18, 28], ["-20deg", "0deg"], { ...clamp, easing: pop }),
            }}
          >
            <Img
              src={staticFile("img/woman.jpg")}
              style={{
                width: "100%",
                height: "100%",
                borderRadius: "50%",
                objectFit: "cover",
                border: `8px solid ${C.white}`,
                boxSizing: "border-box",
              }}
            />
          </div>
          <div
            style={{
              marginTop: 40,
              fontFamily: FONT.body,
              fontWeight: 900,
              fontSize: 46,
              letterSpacing: 4,
              color: C.magenta,
              ...slideUp(f, 24),
            }}
          >
            PEREMPUAN
          </div>
          <div
            style={{
              fontFamily: FONT.display,
              fontWeight: 900,
              fontStyle: "italic",
              fontSize: 112,
              lineHeight: 1,
              color: C.maroon,
              opacity: interpolate(f, [27, 28], [0, 1], clamp),
              scale: interpolate(f, [27, 30, 34], [2, 0.95, 1], { ...clamp, output: "perceptual-scale" }),
            }}
          >
            TUDUNG
            <br />
            <span
              style={{
                fontSize: 128,
                color: C.magenta,
                WebkitTextStroke: `4px ${C.white}`,
                paintOrder: "stroke fill",
              }}
            >
              PINK
            </span>
          </div>
        </div>
      </AbsoluteFill>

      <Sparkles name="Sparkles" count={14} color={C.magenta} seed={4} />
    </>
  );
};

export const DressCode = Interactive.create({
  Component: DressCodeInner,
  layout: "absolute-fill",
});
