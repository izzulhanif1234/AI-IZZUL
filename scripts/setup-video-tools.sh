#!/usr/bin/env bash
# Install video editing tools: FFmpeg, HyperFrames (HTML -> video), and helpers.
# Safe to run repeatedly; skips anything already installed.
set -euo pipefail

SUDO=""
if [ "$(id -u)" -ne 0 ] && command -v sudo >/dev/null 2>&1; then SUDO="sudo"; fi

# --- System packages ---------------------------------------------------------
APT_PKGS=(ffmpeg imagemagick sox mediainfo gifsicle webp fonts-noto-core fonts-noto-color-emoji)
missing=()
for p in "${APT_PKGS[@]}"; do
  dpkg -s "$p" >/dev/null 2>&1 || missing+=("$p")
done
if [ ${#missing[@]} -gt 0 ]; then
  echo "[setup] apt install: ${missing[*]}"
  $SUDO apt-get update -qq
  DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -qq "${missing[@]}" >/dev/null
fi

# --- Python libraries --------------------------------------------------------
# audioop-lts: pydub needs it on Python 3.13+ (audioop was removed from stdlib)
PY_PKGS=(moviepy yt-dlp ffmpeg-python pydub audioop-lts opencv-python-headless)
if ! python3 -c "import moviepy, yt_dlp, ffmpeg, pydub, cv2" >/dev/null 2>&1; then
  echo "[setup] pip install: ${PY_PKGS[*]}"
  pip3 install -q --break-system-packages "${PY_PKGS[@]}" 2>/dev/null \
    || pip3 install -q "${PY_PKGS[@]}"
fi

# --- HyperFrames (HeyGen) ----------------------------------------------------
if ! command -v hyperframes >/dev/null 2>&1; then
  echo "[setup] npm install -g hyperframes"
  npm install -g hyperframes --silent
fi
# Headless Chrome used by `hyperframes render`
hyperframes browser ensure >/dev/null 2>&1 || echo "[setup] warning: hyperframes browser ensure failed"

echo "[setup] video tools ready: $(ffmpeg -version | head -1 | cut -d' ' -f1-3), hyperframes $(hyperframes --version)"
