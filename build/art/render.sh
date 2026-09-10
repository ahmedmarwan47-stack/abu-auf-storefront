#!/usr/bin/env bash
# Rasterise a stand-in 3D icon from this directory to the PNG the site
# references, then trim it to its own alpha bounds.
#
#   build/art/render.sh flash-sale-3d
#
# Headless Chromium is the renderer because it is the engine that paints the
# site, and --default-background-color=00000000 keeps the alpha the icon set
# relies on. The window is deliberately 4x the artwork: Chromium captures the
# WINDOW, and a window the same size as the art clips it (that cost a round -
# the first flash-sale icon shipped with its bottom third missing). crop.py cuts
# the art back out, which also trims it to its content the way the client's own
# 3D icons are trimmed.
#
# Scale factor 1 is deliberate: the icon paints into a 22px box, so the ~230px
# crop is already ~3x a retina phone's need and a 2x render only quadrupled the
# file for pixels nothing displays.
#
# CHROME can point at any Chromium/Chrome binary.
set -euo pipefail
name="${1:?usage: render.sh <svg basename, no extension>}"
here="$(cd "$(dirname "$0")" && pwd)"
out="$here/../../static-export/images/abuauf/icons/$name.png"
CHROME="${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
"$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --default-background-color=00000000 \
  --window-size=1024,1024 --screenshot="$tmp/out.png" "file://$here/$name.svg" >/dev/null 2>&1
python3 "$here/crop.py" "$tmp/out.png" "$out"
