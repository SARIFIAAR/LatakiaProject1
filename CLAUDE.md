# CLAUDE.md

Working notes for this repository. Read `README.md` first for what the project
is; this file is about how to work on it without breaking things.

## Layout

```
index.html          feasibility calculator (live at the Pages root)
test.html           scratch copy of the calculator — not linked, not maintained
site/               the project site (live at /site/)
  index.html        markup and copy, English + Arabic
  css/site.css      one stylesheet, custom properties at the top
  js/site.js        GSAP / ScrollTrigger / Lenis scroll work
  assets/           images — see "Images" below
  tools/            Python scripts that produce the images
  README.md         how the site is built
```

There is no build, no package manager, no test runner. Everything loads from
CDN or is a plain file. Verify changes by serving the folder and looking:

```
cd site && python3 -m http.server 8765
```

## Rules that matter

- **Bump `?v=` in `site/index.html`** whenever `css/site.css` or `js/site.js`
  changes. GitHub Pages caches them for a long time; without the bump the change
  is live but returning visitors keep the old file. Keep both numbers the same.
- **Never edit the facade inside the hero images.** `day.jpg` and `night.jpg`
  are cut straight from the render sheet, and `day-wide.jpg` / `night-wide.jpg`
  are generated *around* them with the building pasted back untouched. To change
  the surroundings, change `site/tools/widen_hero.py` and re-run it.
- **Width and height attributes** on every `<img>` in `site/index.html` must
  match the file, or the page shifts while loading. Update them when an asset
  changes size.
- **The calculator's Firestore config is public by design** (a client API key,
  locked down by security rules). Do not "fix" it by removing it. The rules
  allow one document, deny deletes and archive every revision; a change to the
  data shape needs a schema-version bump in the sheet.
- The calculator and the site are independent. A change to one should not
  touch the other.

## Images

Source of truth is a ChatGPT render sheet (1312 × 1199): day view left, night
view right, five detail crops underneath. It lives outside the repo (the
user's Downloads). Two scripts turn it into assets:

1. `python3 site/tools/crop_render.py <sheet.png>` cuts the seven assets with
   the measured panel boundaries. Crops are upscaled 1.6–2.5× with Lanczos
   because the sheet is small; that is cosmetic, not real detail.
2. `python3 site/tools/widen_hero.py` builds the wide hero images from
   `day.jpg` / `night.jpg`. It is deterministic (seeded), so re-running it
   without changes reproduces the same bytes. Its knobs are named constants at
   the top of `build()`: `PT`/`PB` (sky and street bands), `W` (canvas width),
   `LY` (the shop line the left neighbour stops at), `tops`/`widths` for the
   generated neighbours.

The hero uses `object-fit: cover` on a ~3.3 : 1 image, so on nearly every
screen it fits by height and crops the sides; the building is always centred
and never cropped vertically. On very wide frames the blurred `day.jpg`
backdrop shows at the edges.

## Conventions

- Commit messages: a short imperative title, then a plain-prose body that
  says what changed and why, in the voice of the existing history. Commit and
  push when the user asks for a change to go live; the user works from the
  Pages URL.
- Copy is bilingual. New text needs its Arabic gloss in the same pattern as
  its neighbours (`<span class="ar-gloss">`).
- Check the page in the browser after visual changes, at a laptop width and
  through the full hero scroll (day → dusk → night), before pushing.
- The site's images should stay small: the two wide heroes are the largest
  files at ~0.5 MB each. Keep JPEG quality at 82–86 and don't add PNGs for
  photographic content.

## Status (September 2026)

Both pieces are live. Recent work on the site: new render with the shops, a
fifth detail tile, widened hero images, left neighbour cut to the shop line.
Nothing is half-finished. Known limitation: the render is low resolution;
a larger export would improve the hero on big screens without any code change.
