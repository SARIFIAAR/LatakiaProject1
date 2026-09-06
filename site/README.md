# Khan Murjan — Latakia · project site

One page: a pinned hero that turns from day to night as you scroll, a
statement, the key figures, the passage, the shops, five detail tiles, the two
floor plans and a WhatsApp enquiry. English and Arabic throughout.

Static — no build step. Open `index.html`, or serve the folder:

```
python3 -m http.server 8765
```

Live at https://sarifiaar.github.io/LatakiaProject1/site/

## Stack

| | |
|---|---|
| [GSAP + ScrollTrigger](https://github.com/greensock/GSAP) | the pinned hero, reveals, counters, parallax |
| [Lenis](https://github.com/darkroomengineering/lenis) | smooth scrolling, driven off the GSAP ticker |

Both load from CDN, so there is nothing to install. (An earlier version had a
Three.js model of the facade; it was dropped in favour of the render.)

## Layout

```
index.html        markup and copy
css/site.css      one stylesheet, custom properties at the top
js/site.js        scroll work: hero timeline, intro, reveals, counters, plans
assets/           images (below)
tools/            the two scripts that make the images
```

## The hero

Two images sit in a frame that is pinned for about two screens of scrolling.
Phase one scales the frame until it meets the edges of the hero; phase two
fades the night view in over the day view while the veil deepens and the
title lifts away. The label in the corner reads Day / Dusk / Night.

The images are wide (about 3.3 : 1) and use `object-fit: cover`, so the
building is centred and the street, neighbours and sky fill whatever frame the
viewport gives. Only on a frame wider than 3.3 : 1 does the blurred backdrop
show at the sides.

## Images

Everything comes from one ChatGPT render sheet — day view, night view, and a
strip of five detail crops. The sheet lives outside the repo.

| File | What it is |
|---|---|
| `day.jpg`, `night.jpg` | the facade, cut from the sheet, 2× upscaled; used for the share preview and the blurred backdrop |
| `day-wide.jpg`, `night-wide.jpg` | the hero images, generated around the facade (see below) |
| `shop.jpg` | the Atelier front with the passage beside it, from the day view |
| `d-sign.jpg`, `d-window.jpg`, `d-entrance.jpg`, `d-parapet.jpg`, `d-material.jpg` | the detail tiles; the entrance is also the full-width Passage image |
| `plan-ground.png`, `plan-typical.png` | the floor plans |

Rebuilding from a new sheet:

```
python3 tools/crop_render.py "/path/to/sheet.png"   # the seven crops
python3 tools/widen_hero.py                          # the two wide heroes
```

`widen_hero.py` never touches the facade. It brings `day.jpg` / `night.jpg`
back to their native 650 × 831, then paints around them: a sky gradient
matched to the render at the seam with fractal-noise cotton clouds; low-rise
neighbours to each side, blurred more the further they are from the building;
pavement and cobbles tiled outward and continued below. On the left the wall
in the render was cut down to the ground-floor cornice, with the tree in front
kept against the sky, and the generated run beyond it stays at that height. On
the right the neighbour wall already in the render continues, then steps down.
The script is seeded, so re-running it reproduces the same bytes.

If an asset changes size, update its `width` and `height` attributes in
`index.html`.

## Deploying

Push to `main`; GitHub Pages serves the repository, and this folder is at
`/site/`.

## One thing to remember

`css/site.css` and `js/site.js` are referenced with a `?v=` query in `index.html`.
GitHub Pages serves them with a long cache lifetime, so a returning visitor keeps
the old file until that number changes. **Bump `?v=` whenever you edit either file** —
otherwise your change is live but nobody sees it.

## Progress

- 5 Sep 2026 — site built: markup, stylesheet, scroll work, floor plans.
  Hero reworked to show the whole building; shops added; 3D model dropped.
  Hero pinned so day turning to night is watched, not glimpsed. Arabic added
  throughout; email replaced with WhatsApp.
- 6 Sep 2026 — new render with the shop names over their arches; all assets
  re-cut; fifth detail tile (shop sign). Hero images widened to fill the frame.
  Left neighbour brought down to the shop line.
- Open — a higher-resolution export of the render would sharpen the hero on
  large screens; no code change needed.
