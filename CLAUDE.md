# CLAUDE.md

Working notes for this repository. Read `README.md` first for what the project
is; this file is about how to work on it without breaking things.

## Layout

```
index.html          feasibility calculator, Option 1 (live at the Pages root)
option-2.html       the same calculator for the architect's Option 2 layout
option-2/           Option 2 floor plans (SVG + PNG) and plans.py, which draws them
firestore.rules     security rules for both sheets (deploy with firebase.json)
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
  allow one document per option, deny deletes and archive every revision; a
  change to the data shape needs a schema-version bump in the sheet.
- The calculator and the site are independent. A change to one should not
  touch the other.
- **`option-2.html` is generated from `index.html` once, then diverges.** The
  two share their CSS and script by copy, not by reference: a fix to the
  sheet's logic has to be made in both files. They save to different Firestore
  documents (`sheets/latakia` and `sheets/latakia-option-2`) with their own
  schema versions (2 and 1); keep both ids in `firestore.rules`.
- **The Option 2 plans are drawn by `option-2/plans.py`**, not by hand. Change
  the script, run `python3 option-2/plans.py --png`, and commit the SVG and PNG
  it writes. Only the shell and unit areas come from the architect; the
  partitions and furniture are our proposal and say so on the page.

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

Both pieces are live. On 6 September a second calculator for the architect's
Option 2 was added (`option-2.html` + `option-2/`); its Firestore document is
denied by the rules deployed at the time, so `firestore.rules` needs deploying
before its Save works. Recent work on the site: new render with the shops, a
fifth detail tile, widened hero images, left neighbour cut to the shop line.
Nothing is half-finished. Known limitation: the render is low resolution;
a larger export would improve the hero on big screens without any code change.
