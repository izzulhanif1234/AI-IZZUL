#!/usr/bin/env bash
# Finish the Hotel MITC render: warm/muted grade, soft vignette, fine film grain, no audio.
# usage: scripts/mitc_finish.sh RAW.mp4 OUT.mp4 [END_CARD_START]
# The vignette stops when the ivory end card fades in (default 70.6 s) so it stays clean.
# Grain makes CRF encodes huge (~55 Mbit/s), so this is a two-pass 9.5 Mbit/s encode (~90 MB).
set -euo pipefail
RAW="$1"; OUT="$2"; END="${3:-70.6}"
VF="colortemperature=temperature=5600:mix=0.45,eq=contrast=1.06:saturation=0.9:gamma=0.985,\
curves=all='0/0.02 0.5/0.49 1/0.99',vignette=angle=PI/7:enable='lt(t,$END)',noise=c0s=5:c0f=t+u,format=yuv420p"
LOG="$(mktemp -d)/pass"
ffmpeg -y -loglevel error -i "$RAW" -an -vf "$VF" -c:v libx264 -preset medium -b:v 9500k -pass 1 -passlogfile "$LOG" -f mp4 /dev/null
ffmpeg -y -loglevel error -i "$RAW" -an -vf "$VF" -c:v libx264 -preset medium -b:v 9500k -maxrate 14M -bufsize 20M \
  -pass 2 -passlogfile "$LOG" -movflags +faststart "$OUT"
