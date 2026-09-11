"""Cut the site's image assets out of the ChatGPT render sheet.

The sheet is a 1312 x 1199 composite: day view (left), night view (right), and a
strip of five detail crops underneath — shop sign, window, entrance, parapet,
material. The panel boundaries below were measured on the sheet dated
6 Sep 2026; a re-render laid out the same way should cut identically, but check
the edges if the sheet changes.

    python3 site/tools/crop_render.py "/path/to/render sheet.png"

After this, run widen_hero.py to rebuild the wide hero images.
"""
import os
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets") + os.sep

# name, (left, top, right, bottom) on the sheet, upscale factor
CUTS = [
    ("day.jpg",        (2, 2, 652, 833),        2.0),   # 2 px in from the panel edge
    ("night.jpg",      (660, 2, 1310, 833),     2.0),
    ("shop.jpg",       (100, 462, 390, 800),    2.5),   # Atelier front + the passage, from the day panel
    ("d-sign.jpg",     (18, 847, 313, 1047),    1.6),
    ("d-window.jpg",   (328, 847, 525, 1047),   1.6),
    ("d-entrance.jpg", (544, 847, 768, 1047),   2.0),   # also used full-width in the Passage section
    ("d-parapet.jpg",  (788, 847, 1062, 1047),  1.6),
    ("d-material.jpg", (1080, 847, 1293, 1047), 1.6),
]

def main(path):
    sheet = Image.open(path).convert("RGB")
    for name, box, scale in CUTS:
        im = sheet.crop(box)
        if scale != 1:
            im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        im.save(OUT + name, "JPEG", quality=86, optimize=True, progressive=True)
        print(f"{name:16} {im.width} x {im.height}")
    print("now update the width/height attributes in index.html if any size changed")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
