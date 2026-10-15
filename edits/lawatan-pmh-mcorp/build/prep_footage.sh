#!/usr/bin/env bash
# Grade the 19 DJI Osmo Pocket 4 clips (4K 10-bit BT.709) into 3200x1800 H.264 edit masters
# (1.67x punch-in headroom at 1080p). Outputs hf/assets/footage/pNN.mp4 (git-ignored).
# Usage: build/prep_footage.sh <dir with the DJI_*_D.MP4 files>
set -euo pipefail
SRC=${1:?raw footage dir}
OUT="$(cd "$(dirname "$0")/.." && pwd)/hf/assets/footage"
mkdir -p "$OUT"
# Look: gentle S-curve with highlight roll-off (white walls), +12% saturation, cool shadows /
# warm mids for depth, light clarity. Skin stays natural; no smoothing.
LOOK="eq=contrast=1.07:saturation=1.12,curves=all='0/0 0.25/0.22 0.5/0.5 0.75/0.77 1/0.985',colorbalance=rs=-0.015:bs=0.025:rm=0.012:bm=-0.008:rh=0.012:bh=-0.018,unsharp=5:5:0.25"
# Per-clip exposure match (EV) from measured mean luma: corridor/lobby and meeting-room shots run under.
declare -A EV=([03]=0.25 [05]=0.2 [08]=0.2 [09]=0.1 [11]=0.15 [14]=0.1 [15]=0.1 [16]=0.1 [18]=0.1)
grade() { # n file ev
  ffmpeg -v error -y -i "$2" -map 0:v:0 \
    -vf "format=yuv444p10le,exposure=exposure=$3,$LOOK,scale=3200:1800:flags=lanczos,fps=30000/1001,format=yuv420p" \
    -c:v libx264 -preset fast -crf 16 -g 15 -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
    -movflags +faststart -an "$OUT/p$1.part.mp4" && mv "$OUT/p$1.part.mp4" "$OUT/p$1.mp4"
  echo "graded p$1 ($(basename "$2"))"
}
export -f grade; export OUT LOOK
# 4 clips in parallel (the 10-bit 4:4:4 grade filters are single-threaded); skips finished clips
i=1
for f in $(ls "$SRC"/DJI_*_D.MP4 | sort); do
  n=$(printf "%02d" $i); i=$((i+1))
  [ -f "$OUT/p$n.mp4" ] && continue
  echo "$n $f ${EV[$n]:-0}"
done | xargs -P 4 -L 1 bash -c 'grade "$@"' _
