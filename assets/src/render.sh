#!/bin/sh
# Render assets/src/<name>.html to assets/images/<name>.png with headless Chrome.
# usage: ./render.sh <name> <width> <height>
cd "$(dirname "$0")"
C="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
"$C" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
  --virtual-time-budget=4000 --window-size="$2,$3" \
  --screenshot="../images/$1.png" "file://$PWD/$1.html" 2>/dev/null
