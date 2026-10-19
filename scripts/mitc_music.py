"""Music bed for the Hotel MITC intro from a MusicGen take (epicB, ~121.8 bpm).

usage: python3 scripts/mitc_music.py SRC.wav HF_DIR

- starts the take so its drop (17.168 s in the take) lands on the stats scene (14.4 s in the film)
- the take breaks up after ~49 s, so from a bar line at 46.724 s it jumps back 12 bars
  (same beat phase) to keep the driving section going until the end
- writes HF_DIR/assets/bgm/bed.wav (48 kHz stereo, -14 LUFS) and beats.json (film-time beat grid)
"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

SRC, HF = sys.argv[1], sys.argv[2]
DROP, FILM_DROP = 17.168, 14.4
BEAT = 0.4926
BAR = 4 * BEAT
JOIN = DROP + 15 * BAR          # 46.724 s in the take
BACK = 12 * BAR
LENGTH = 68.5                    # film seconds (a little past the end)
XF = 0.03

y, sr = sf.read(SRC, dtype="float32")
off = DROP - FILM_DROP
a = y[int(off * sr):int(JOIN * sr)]
b = y[int((JOIN - BACK) * sr):int((JOIN - BACK + LENGTH) * sr)]
n = int(XF * sr)
fade = np.linspace(0, 1, n, dtype=np.float32)
a[-n:] = a[-n:] * (1 - fade) + b[:n] * fade
bed = np.concatenate([a, b[n:]])[:int(LENGTH * sr)]

os.makedirs(os.path.join(HF, "assets", "bgm"), exist_ok=True)
tmp = os.path.join(HF, "assets", "bgm", "_raw.wav")
sf.write(tmp, bed, sr)
out = os.path.join(HF, "assets", "bgm", "bed.wav")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                "-ar", "48000", "-ac", "2", out], check=True)
os.remove(tmp)

beats = [round(FILM_DROP + k * BEAT, 3) for k in range(-29, 120) if 0 < FILM_DROP + k * BEAT < LENGTH]
json.dump({"bpm": round(60 / BEAT, 2), "drop": FILM_DROP, "join": round(JOIN - off, 3), "beats": beats},
          open(os.path.join(HF, "assets", "bgm", "beats.json"), "w"), indent=1)
print("bed", len(bed) / sr, "s; join at film", round(JOIN - off, 3))
