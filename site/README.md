# Khan Murjan — Latakia

Project site for Khan Murjan: shops along a covered passage, clinics above.

Static — no build step. Open `index.html`, or serve the folder.

## Stack

| | |
|---|---|
| [GSAP + ScrollTrigger](https://github.com/greensock/GSAP) | scroll timelines, reveals, counters |
| [Lenis](https://github.com/darkroomengineering/lenis) | smooth scrolling, driven off the GSAP ticker |
| [Three.js](https://github.com/mrdoob/three.js) | the 3D model, built from the measured drawing |

All three load from CDN, so there is nothing to install.

## Layout

```
index.html        markup and copy
css/site.css      one stylesheet, custom properties at the top
js/site.js        scroll work, then the Three.js model
assets/           day and night views, five detail crops
```

## The model

`js/site.js` builds the facade as an extruded shape with the openings cut as real
holes, at the dimensions taken off the plans:

- 10.70 m frontage, 21.50 m depth, 12.00 m to the parapet
- ground floor 5.00 m, upper floors 3.00 m each
- shopfronts 3.70 m, passage 2.50 m clear, piers 0.20 m
- four windows per upper floor at 2.675 m centres, 1.05 × 1.90 openings

Change a constant at the top of the model block and the geometry follows.

## Deploying

Any static host. On GitHub Pages, push and enable Pages for the branch.

## One thing to remember

`css/site.css` and `js/site.js` are referenced with a `?v=` query in `index.html`.
GitHub Pages serves them with a long cache lifetime, so a returning visitor keeps
the old file until that number changes. **Bump `?v=` whenever you edit either file** —
otherwise your change is live but nobody sees it.
