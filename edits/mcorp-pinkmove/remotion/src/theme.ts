import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Poster palette: pink magenta, maroon, white.
export const C = {
  magenta: "#E6007E",
  hotPink: "#FF3FA4",
  pinkSoft: "#FFC4E1",
  blush: "#FFE6F2",
  maroon: "#7A0F2E",
  maroonDeep: "#3E0618",
  ink: "#24020E",
  white: "#FFFFFF",
};

// Google Fonts (latin subset) bundled in public/fonts so renders do not
// depend on fonts.gstatic.com being reachable from headless Chrome.
const local = (family: string, file: string, weight = "400", style = "normal") =>
  loadFont({ family, url: staticFile(`fonts/${file}.woff2`), weight, style });

local("Kanit", "Kanit-800i", "800", "italic");
local("Kanit", "Kanit-900i", "900", "italic");
local("Kaushan Script", "KaushanScript");
local("Montserrat", "Montserrat-700", "700");
local("Montserrat", "Montserrat-800", "800");
local("Montserrat", "Montserrat-900", "900");

export const FONT = {
  // Heavy sporty italic for MCORP and headlines.
  display: "Kanit",
  // Hand-written tagline.
  script: "Kaushan Script",
  body: "Montserrat",
};

// Music is mastered to exactly 120 BPM with a downbeat on frame 0,
// so one beat is 15 frames at 30 fps and every scene cut lands on a beat.
export const BEAT = 15;

// Transition length; each wipe is centred on the scene boundary.
export const WIPE = 10;
export const HALF_WIPE = WIPE / 2;
