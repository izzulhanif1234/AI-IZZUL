"""Mix the Islamic score + soft SFX into hf/assets/audio/mix.wav (48k stereo, -14 LUFS, -1.5 dBTP). No VO.
Usage: python3 mix_audio.py
"""
import json
import subprocess
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "hf/assets"
OUT, TMP = A / "audio/mix.wav", A / "audio/mix.premaster.wav"
DURATION = 42.0
# (file, timeline time of the visual moment, file onset offset, volume)
SFX = [  # soft whooshes on the gold light sweeps between sections
    ("whoosh.mp3", 7.6, 0.08, 0.16),
    ("whoosh.mp3", 17.8, 0.08, 0.14),
    ("whoosh.mp3", 23.4, 0.08, 0.14),
    ("whoosh.mp3", 30.2, 0.08, 0.14),
    ("whoosh.mp3", 34.6, 0.08, 0.16),
]


def loudness(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    return json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])


inputs = ["-i", str(A / "audio/music.wav")]
chains, labels = ["[0:a]volume=1.0[m]"], ["[m]"]
for j, (f, t, onset, vol) in enumerate(SFX, start=1):
    inputs += ["-i", str(A / "sfx" / f)]
    chains.append(f"[{j}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={int(max(0, t - onset) * 1000)}:all=1[s{j}]")
    labels.append(f"[s{j}]")
graph = ";".join(chains) + f";{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{DURATION}[mix]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[mix]", "-c:a", "pcm_s24le", str(TMP)], check=True)
m = loudness(TMP)
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(TMP), "-af", f"{ln},aresample=48000", "-c:a", "pcm_s16le", str(OUT)], check=True)
TMP.unlink()
f = loudness(OUT)
print(f"wrote {OUT.name}  I={f['input_i']} LUFS  TP={f['input_tp']} dBTP")
