#!/usr/bin/env bash
# Fetch the real MITC photos used in the promo from the official site (site.mitc.org.my media library)
# and grade them consistently. Outputs hf/assets/photos/<name>.jpg (git-ignored).
# Usage: build/prep_photos.sh
set -euo pipefail
OUT="$(cd "$(dirname "$0")/.." && pwd)/hf/assets/photos"
TMP=$(mktemp -d); mkdir -p "$OUT"
BASE=https://site.mitc.org.my/wp-content/uploads
# name | path under /wp-content/uploads | extra grade filters
PHOTOS=(
"building|2025/07/ETE00496-scaled.jpg|"
"facade|2025/09/ETE00462-scaled.jpg|"
"aerial|2026/09/IMG_8353.JPG.jpeg|"
"stage1|2025/10/WhatsApp-Image-2025-10-30-at-5.19.26-PM-1.jpeg|"
"stage2|2025/10/WhatsApp-Image-2025-10-30-at-5.19.25-PM-1.jpeg|"
"gala1|2025/09/TYT-11-scaled.jpg|"
"gala2|2025/09/TYT-16-1-scaled.jpg|"
"gala3|2025/08/TYT-6-1-scaled.jpg|"
"show|2025/08/36641801_1821950504515537_2764391610568409088_n.jpg|"
"hallempty|2025/03/5.jpg|"
"expo|2025/09/WhatsApp-Image-2025-09-02-at-12.36.55-PM.jpeg|"
"expo2|2025/09/WhatsApp-Image-2025-09-02-at-12.15.24-PM-2.jpeg|"
"auditorium|2025/11/WhatsApp-Image-2025-11-20-at-9.24.02-AM-2.jpeg|"
"ballroom|2025/09/WhatsApp-Image-2025-09-02-at-5.19.09-PM-1.jpeg|colorbalance=rm=-0.03:bm=0.03"
"meeting|2025/08/ETE00949-scaled.jpg|"
"boardroom|2025/03/photo_19_2025-03-21_12-20-46.jpg|colorbalance=rm=-0.06:gm=-0.01:bm=0.05"
"banquet|2025/09/WhatsApp-Image-2025-09-02-at-10.47.07-AM-1.jpeg|colorbalance=rm=-0.03:bm=0.03"
"grandhall|2025/09/WhatsApp-Image-2025-09-02-at-4.10.52-PM-1.jpeg|"
)
LOOK="eq=contrast=1.06:saturation=1.08,curves=all='0/0 0.25/0.23 0.5/0.5 0.75/0.77 1/0.99',colorbalance=rs=-0.015:bs=0.02:rh=0.01:bh=-0.01,unsharp=5:5:0.4"
for e in "${PHOTOS[@]}"; do
  IFS='|' read -r name path extra <<< "$e"
  curl -sS -A "Mozilla/5.0" --max-time 120 -o "$TMP/src" "$BASE/$path"
  ffmpeg -v error -y -i "$TMP/src" -vf "scale='min(2560,iw)':-2:flags=lanczos,${extra:+$extra,}$LOOK" -q:v 2 "$OUT/$name.jpg"
  echo "ok $name"
done
rm -rf "$TMP"
