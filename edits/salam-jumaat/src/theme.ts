export const FPS = 30;
export const W = 1080;
export const H = 1920;

export const C = {
  night: '#061512',
  deep: '#0a231e',
  emerald: '#0f3d33',
  jade: '#1d5c4c',
  gold: '#d6b25e',
  goldLight: '#f5e3a8',
  goldDeep: '#9c7629',
  ivory: '#f8f1df',
  ivoryDim: 'rgba(248,241,223,0.78)',
};

export const GOLD_GRADIENT = `linear-gradient(100deg, ${C.goldDeep} 0%, ${C.gold} 22%, ${C.goldLight} 38%, ${C.gold} 52%, ${C.goldDeep} 70%, ${C.gold} 86%, ${C.goldLight} 100%)`;

export const FONT = {
  arabic: "'Amiri', serif",
  display: "'Cinzel', serif",
  serif: "'Cormorant Garamond', serif",
  sans: "'Montserrat', sans-serif",
};

// Scene layout on the root timeline (frames). Scenes overlap so each one can
// open with a star wipe over the tail of the previous scene.
export const WIPE = 24;
export const SCENES = {
  intro: {from: 0, dur: 165},
  ayat: {from: 140, dur: 280},
  doa1: {from: 396, dur: 232},
  doa2: {from: 604, dur: 236},
  end: {from: 816, dur: 144},
};
export const TOTAL = SCENES.end.from + SCENES.end.dur;
