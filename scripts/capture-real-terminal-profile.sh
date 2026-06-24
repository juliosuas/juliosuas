#!/usr/bin/env zsh
set -euo pipefail

ROOT="${0:A:h:h}"
RAW="$ROOT/assets/terminal-profile-raw.png"
OUT="$ROOT/assets/terminal-profile.png"
COMMAND="$ROOT/scripts/open-real-terminal-profile.command"

mkdir -p "$ROOT/assets"
chmod +x "$COMMAND"

open -a Terminal "$COMMAND"
sleep 2.0
screencapture -x "$RAW"

python3 - "$RAW" "$OUT" <<'PY'
from pathlib import Path
from PIL import Image, ImageOps
import sys

raw = Path(sys.argv[1])
out = Path(sys.argv[2])
img = Image.open(raw).convert("RGB")

pixels = img.load()
w, h = img.size
xs = []
ys = []
for y in range(h):
    for x in range(w):
        r, g, b = pixels[x, y]
        if g > 115 and r < 130 and b < 130:
            xs.append(x)
            ys.append(y)

if not xs:
    raise SystemExit("no green terminal text found in screenshot")

left = max(min(xs) - 46, 0)
right = min(max(xs) + 86, w)
top = max(min(ys) - 52, 0)
bottom = min(max(ys) + 70, h)
img = img.crop((left, top, right, bottom))

# Keep the crop terminal-black and README-sized without adding fake controls.
w, h = img.size
target_w = 1450
target_h = int(h * (target_w / w))
img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
img.save(out, optimize=True)
print(out)
PY
