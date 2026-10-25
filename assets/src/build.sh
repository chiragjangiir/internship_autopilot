#!/bin/sh
# Rebuild every image in assets/images from the sources in this folder.
set -e
cd "$(dirname "$0")"
for p in architecture workflow sequence safety mockups compare panels; do python3 "$p.py" >/dev/null; done
./render.sh hero 1600 520
./render.sh architecture 1600 1110
./render.sh workflow 1600 850
./render.sh sequence 1640 2332
./render.sh safety 1600 820
./render.sh mock_targets 1600 820
./render.sh mock_draft 1600 790
./render.sh mock_sentlog 1600 860
./render.sh mock_calendar 1600 900
./render.sh mock_status 1600 980
./render.sh compare 1600 900
./render.sh setup 1600 575
./render.sh faq 1600 585
./render.sh social 1280 640 && sips -z 640 1280 ../images/social.png --out ../images/social_preview.png >/dev/null && rm ../images/social.png
python3 gif.py
python3 check_text.py && echo "all images built, no hyphens, dashes or semicolons in visible text"
