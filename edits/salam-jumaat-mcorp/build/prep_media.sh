#!/usr/bin/env bash
# Grade the drone clip + photos for the Salam Jumaat motion poster. Outputs hf/assets/footage (git-ignored).
# Usage: build/prep_media.sh <dir with the dji_fly_* files>
set -euo pipefail
SRC=${1:?raw dir}
OUT="$(cd "$(dirname "$0")/.." && pwd)/hf/assets/footage"
mkdir -p "$OUT"
LOOK="eq=contrast=1.08:saturation=1.1,curves=all='0/0 0.25/0.22 0.5/0.5 0.75/0.77 1/0.98',colorbalance=rs=-0.02:gs=0.01:bs=0.02:rh=0.02:bh=-0.02,unsharp=5:5:0.3"
# Drone pull-back from the MCORP sign (4K60): keep 60fps for a smooth 0.5x slow-motion.
ffmpeg -v error -y -i "$SRC"/dji_fly_*_video.mp4 -map 0:v:0 -vf "format=yuv444p10le,$LOOK,scale=2400:1350:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset fast -crf 15 -g 30 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart -an "$OUT/drone.mp4"
# Hazy photos: extra contrast (light dehaze) on top of the shared look.
i=1
for f in $(ls "$SRC"/dji_fly_*_photo.jpg | sort); do
  ffmpeg -v error -y -i "$f" -vf "scale=2400:-2:flags=lanczos,eq=contrast=1.12:gamma=0.96:saturation=1.08,$LOOK" -q:v 2 "$OUT/f$i.jpg"
  i=$((i+1))
done
echo "media ready"
# 30fps copy for 1:1 playback in the 30fps render (no slow motion, no duplicated frames)
ffmpeg -v error -y -i "$OUT/drone.mp4" -vf fps=30 -c:v libx264 -preset fast -crf 15 -g 15 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart -an "$OUT/drone30.mp4"
