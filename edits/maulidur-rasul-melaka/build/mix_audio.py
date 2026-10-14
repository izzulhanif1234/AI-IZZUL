"""Mix dialogue + music + SFX into hf/assets/audio/mix.wav (48k stereo, -14 LUFS, -1.5 dBTP).

Dialogue is the camera audio of the stadium PA: high-pass, gentle de-noise, de-box and presence EQ,
light compression, each bite matched to -18 LUFS before the master. Music is ducked under speech
by the gain automation in edl.MUSIC_GAIN.
Usage: python3 mix_audio.py <raw footage dir>
"""
import json
import subprocess
import sys
from pathlib import Path

import edl

RAW = Path(sys.argv[1])
HERE = Path(__file__).resolve().parent.parent
A = HERE / "hf/assets"
OUT = A / "audio/mix.wav"
TMP = OUT.with_suffix(".premaster.wav")

VOICE_FX = (
    "highpass=f=95,lowpass=f=11000,afftdn=nr=10:nf=-38,"
    "equalizer=f=280:t=q:w=1.2:g=-2.5,equalizer=f=3200:t=q:w=1.0:g=2.5,"
    "acompressor=threshold=-22dB:ratio=2.5:attack=8:release=180:makeup=2"
)


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    j = r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1]
    return json.loads(j)


inputs, chains, labels = [], [], []
# dialogue bites
for i, (clip, a, b, t, fo) in enumerate(edl.SPEECH):
    inputs += ["-i", str(RAW / f"{clip}.MOV")]
    chains.append(
        f"[{i}:a:0]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,{VOICE_FX},"
        f"afade=t=in:d=0.04,afade=t=out:st={round(b - a - fo, 3)}:d={fo},"
        f"loudnorm=I=-18:TP=-3:LRA=7:linear=true,aresample=48000,adelay={int(t * 1000)}:all=1[d{i}]"
    )
    labels.append(f"[d{i}]")
n = len(edl.SPEECH)

# music with gain automation (piecewise-linear in dB)
inputs += ["-i", str(A / "audio/music.wav")]
pts = edl.MUSIC_GAIN
expr = str(pts[-1][1])
for (t0, g0), (t1, g1) in reversed(list(zip(pts, pts[1:]))):
    seg = f"({g0}+({g1}-({g0}))*(t-{t0})/{max(t1 - t0, 1e-3)})"
    expr = f"if(lt(t,{t1}),{seg},{expr})"
chains.append(f"[{n}:a]volume='pow(10,({expr})/20)':eval=frame,volume=-3dB[m]")
labels.append("[m]")

# sfx
for j, (f, t, onset, vol) in enumerate(edl.SFX):
    k = n + 1 + j
    inputs += ["-i", str(A / "sfx" / f)]
    start = max(0, t - onset)
    chains.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={int(start * 1000)}:all=1[s{j}]")
    labels.append(f"[s{j}]")

graph = ";".join(chains) + f";{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{edl.DURATION}[mix]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[mix]", "-ar", "48000", "-c:a", "pcm_s24le", str(TMP)], check=True)

# master: two-pass loudnorm to -14 LUFS integrated, true peak -1.5 dBTP
m = loudness(TMP)
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(TMP), "-af", f"{ln},aresample=48000", "-c:a", "pcm_s16le", str(OUT)], check=True)
TMP.unlink()
f = loudness(OUT)
print(f"wrote {OUT.relative_to(HERE)}  I={f['input_i']} LUFS  TP={f['input_tp']} dBTP  LRA={f['input_lra']}")
