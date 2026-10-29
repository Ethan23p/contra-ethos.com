"""Crop the AI Kassandra hero, card and landing image from the Drive screenshots.

Run once when the source image changes:
    uv run --with pillow python tools/crop_kassandra.py
"""
from pathlib import Path
from PIL import Image

REF = 'G:/My Drive/AI Cloud Resources/projects/AI_Kassandra ref/'
OUT = Path(__file__).resolve().parents[2] / 'ethanporter.xyz' / 'images' / 'projects'

# Landing page, below the browser chrome
landing = Image.open(REF + 'image_2026-04-24_082234636.png').convert('RGB').crop((0, 87, 1291, 925))
landing.save(OUT / 'ai-kassandra-landing.webp', quality=88, method=6)

im = Image.open(REF + 'image_2026-04-24_082449075.png').convert('RGB')
hero = im.crop((0, 87, 1280, 926))
hero.save(OUT / 'ai-kassandra.webp', quality=88, method=6)
card = im.crop((240, 150, 1040, 750))
card.thumbnail((1200, 1000), Image.LANCZOS)
card.save(OUT / 'ai-kassandra-card.webp', quality=82, method=6)
print(hero.size, card.size)
