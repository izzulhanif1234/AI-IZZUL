#!/usr/bin/env bash
# Grade the raw iPhone clips (HLG HDR, BT.2020) into SDR BT.709 masters for the edit,
# and build the speed-ramp clip. Outputs to hf/assets/footage/ (git-ignored).
# Usage: build/prep_footage.sh <dir with IMG_8033.MOV ... IMG_8036.MOV>
set -euo pipefail
SRC=${1:?raw footage dir}
HERE=$(cd "$(dirname "$0")/.." && pwd)
OUT="$HERE/hf/assets/footage"
TMP=$(mktemp -d)
mkdir -p "$OUT"

# HLG -> linear -> BT.709 primaries -> Mobius tone-map (keeps skin tones natural) -> BT.709 SDR.
TONEMAP="zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.5:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
# Light grade: a touch of contrast and warmth, gentle clarity. No skin smoothing, no heavy look.
GRADE="eq=contrast=1.05:saturation=1.05,colorbalance=rm=0.012:bm=-0.012:rh=0.008:bh=-0.008,unsharp=5:5:0.35"
ENC=(-c:v libx264 -preset slow -crf 14 -g 15 -keyint_min 15 -pix_fmt yuv420p
     -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart -an)

grade() { # name extra-filters
  ffmpeg -v error -y -i "$SRC/IMG_$1.MOV" -map 0:v:0 -vf "${2:+$2,}$TONEMAP,$GRADE,fps=30" "${ENC[@]}" "$OUT/c$1.mp4"
  echo "graded c$1.mp4"
}

grade 8033
grade 8035
grade 8036
# 8034 is the speaker close-up we punch in on: stabilise first (slight handheld jitter).
ffmpeg -v error -y -i "$SRC/IMG_8034.MOV" -vf "vidstabdetect=shakiness=4:accuracy=15:result=$TMP/8034.trf" -f null -
grade 8034 "vidstabtransform=input=$TMP/8034.trf:smoothing=30:optzoom=0:zoom=3:interpol=bicubic"

# Speed ramp on the 8033 zoom-out (src 20.5-25.3 -> 1.2s): 2x -> 5x (frame-blended) -> 3.33x.
C="$OUT/c8033.mp4"
ffmpeg -v error -y -i "$C" -filter_complex "
  [0:v]trim=20.5:21.0,setpts=(PTS-STARTPTS)/2[a];
  [0:v]trim=21.0:24.4,setpts=(PTS-STARTPTS)/5,tmix=frames=3[b];
  [0:v]trim=24.4:25.3,setpts=(PTS-STARTPTS)/3.333,tmix=frames=2[c];
  [a][b][c]concat=n=3:v=1:a=0,fps=30,trim=duration=1.2[v]" -map "[v]" "${ENC[@]}" "$OUT/ramp.mp4"
echo "built ramp.mp4"
rm -rf "$TMP"
