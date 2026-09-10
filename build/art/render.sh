#!/usr/bin/env bash
# Rasterise the stand-in 3D icons in this directory to the PNGs the site
# references. Headless Chromium is the renderer because it is the same engine
# that paints the site, and --default-background-color=00000000 keeps the alpha
# the icon set relies on (they sit on the beige utility bar and on white cards).
#
#   build/art/render.sh flash-sale-3d
#
# CHROME can point at any Chromium/Chrome binary.
set -euo pipefail
name="${1:?usage: render.sh <svg basename, no extension>}"
here="$(cd "$(dirname "$0")" && pwd)"
out="$here/../../static-export/images/abuauf/icons/$name.png"
CHROME="${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"
tmp="$(mktemp -d)"
"$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --default-background-color=00000000 \
  --window-size=256,256 --screenshot="$tmp/out.png" "file://$here/$name.svg" >/dev/null 2>&1
cp "$tmp/out.png" "$out"
rm -rf "$tmp"
echo "wrote $out"
