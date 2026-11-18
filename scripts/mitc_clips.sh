#!/usr/bin/env bash
# Cut the MITC TikTok b-roll (@mitcmelaka1) into 1080x1920 H.264 clips for edits/mitc-promo/hf/assets/clips.
# usage: scripts/mitc_clips.sh SRC_DIR   (SRC_DIR holds <tiktok-id>.mp4, fetched with
#   yt-dlp -S "res,codec:h264" -o "%(id)s.%(ext)s" https://www.tiktok.com/@mitcmelaka1/video/<id>)
# Every in/out point was picked frame by frame to skip on-screen captions, title cards and presenters,
# and placed on the sharpest window of each shot (Laplacian variance, scripts kept out of the repo).
# Only 720p+ sources that hold up at 1080x1920; the 576p uploads were dropped as too soft.
set -euo pipefail
SRC=$1
OUT=$(dirname "$0")/../edits/mitc-promo/hf/assets/clips
mkdir -p "$OUT"
V="scale=1080:1920:flags=lanczos,setsar=1,fps=30"
cut() { # name id start dur [extra filter before scale]
  local pre=${5:+$5,}
  ffmpeg -nostdin -v error -y -ss "$3" -t "$4" -i "$SRC/$2.mp4" -an -vf "${pre}$V" \
    -c:v libx264 -crf 19 -preset slow -g 15 -keyint_min 15 -pix_fmt yuv420p -movflags +faststart "$OUT/$1.mp4"
  echo "$1 <- $2 @ $3 +$4"
}
cut hook-stage    7507840908549688594 26.8 2.4   # gala prep: LED stage (Konica Minolta dinner, Hall B)
cut hook-star     7507840908549688594 6.6  1.8   # gala prep: star arch + red carpet
cut grand-ballroom 7510414709900774663 35.8 2.7  # Grand Ballroom wedding set-up
cut maharani-hall 7383175657573928199 2.3  2.7   # Maharani Ballroom, wide
cut ev-ht-gate    7378734633376091410 31.6 1.5   # Pameran Hang Tuah (4K): gateway
cut ev-ht-ship    7378734633376091410 37.3 1.5   # Pameran Hang Tuah (4K): ship
cut ev-tables     7507840908549688594 9.0  1.5   # gala dinner tables, Hall B
cut ev-pelamin    7383175657573928199 6.9  1.5   # Maharani Ballroom pelamin
cut ev-akad       7383175657573928199 22.1 1.5   # Maharani Ballroom akad set-up
cut prep-hall     7507840908549688594 32.7 2.7   # hall set-up down the red carpet to the stage
# v4: more hall footage (GoTravel Expo, Karnival Kerjaya TVET, Hang Tuah, Grand Ballroom)
cut hall-expo     7520491843235171591 6.0  2.7   # expo in the exhibition hall (sakura installation)
cut hall-booths   7520491843235171591 28.3 2.7   # busy exhibitor booths
cut hall-robot    7514607342432898322 36.1 2.7   # technology exhibit, robot arm cell
cut hall-seminar  7514607342432898322 42.3 2.7   # seminar set-up, round tables
cut hall-stage    7514607342432898322 15.7 2.7   # stage + seating for an opening ceremony
cut ev-ht-houses  7378734633376091410 36.0 2.7   # Pameran Hang Tuah (4K): Melaka 1477 models
cut grand-2       7510414709900774663 37.0 2.7   # Grand Ballroom, second angle
cut logo-bg       7515280572890107154 61.0 5.3   # stage + crowd, used blurred behind the logo reveal
