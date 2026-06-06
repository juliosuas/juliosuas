#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "terminal-profile.png"
FONT_PATHS = [
    Path("/Library/Fonts/Monaco.ttf"),
    Path("/System/Library/Fonts/Menlo.ttc"),
]

raw = subprocess.check_output([str(ROOT / "scripts" / "profile-terminal-card.sh")], text=True)
raw = raw.replace("\x1b[0;32m", "").replace("\x1b[0m", "").replace("\x1b[H\x1b[2J\x1b[3J", "")
lines = raw.strip("\n").splitlines()

font_path = next(path for path in FONT_PATHS if path.exists())
font = ImageFont.truetype(str(font_path), 24)
title_font = ImageFont.truetype(str(font_path), 20)

padding_x = 34
padding_y = 34
line_h = 34
chrome_h = 54
width = 1450
height = chrome_h + padding_y * 2 + line_h * len(lines)

img = Image.new("RGB", (width, height), "#050805")
draw = ImageDraw.Draw(img)

draw.rectangle((0, 0, width, chrome_h), fill="#151715")
draw.ellipse((22, 18, 42, 38), fill="#ff5f57")
draw.ellipse((58, 18, 78, 38), fill="#febc2e")
draw.ellipse((94, 18, 114, 38), fill="#28c840")
draw.text((width // 2 - 270, 16), "juliosuas@fsociety: ~ - zsh - 112x42", font=title_font, fill="#8c948c")

green = "#33ff33"
shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow)

y = chrome_h + padding_y
for line in lines:
    shadow_draw.text((padding_x, y), line, font=font, fill=(51, 255, 51, 110))
    y += line_h

blurred = shadow.filter(ImageFilter.GaussianBlur(radius=2))
img = Image.alpha_composite(img.convert("RGBA"), blurred)
draw = ImageDraw.Draw(img)

y = chrome_h + padding_y
for line in lines:
    draw.text((padding_x, y), line, font=font, fill=green)
    y += line_h

img.save(OUTPUT)
print(OUTPUT)
