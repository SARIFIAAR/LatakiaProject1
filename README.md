# Khan Murjan — Latakia

A mixed-use building in Latakia: shops along a covered passage at street level,
clinics on the two floors above. This repository holds the two web pieces of the
project, both static, both served by GitHub Pages.

| | Where | Live |
|---|---|---|
| **Feasibility calculator — Option 1** | `index.html` (and `test.html`, a scratch copy) | https://sarifiaar.github.io/LatakiaProject1/ |
| **Feasibility calculator — Option 2** | `option-2.html`, plans in `option-2/` | https://sarifiaar.github.io/LatakiaProject1/option-2.html |
| **Project site** | `site/` | https://sarifiaar.github.io/LatakiaProject1/site/ |

No build step anywhere. Open the file, or serve the folder.

## The feasibility calculator

A single-page sheet for the numbers: sales value per unit, allocation of units
between the parties, project costs and the net result. English and Arabic side by
side. Figures save to a Firestore document in the `latakia-feasibility` Firebase
project, which exists for this sheet alone; every save is archived as an
immutable revision and a second browser loads the latest one.

Current shape of the sheet (September 2026):

- Ground floor: shops on the street and along the passage.
- First and second floor: four separately priced units each — street 49 m²,
  street corner 40 m², back corner 44 m², back 44 m² — with a saleable-area
  loading of 192 / 177 per floor.
- Three parties in unit allocation: the two owners and the supervising engineer.
- Saved figures carry a schema version, so a sheet stored under an older layout
  prompts for a re-save instead of being misread.

### Option 2

`option-2.html` is the same sheet for the architect's second layout (the
"OPTION 2" sheet of 6 September): three 2.80 m shops facing the street on a
1.30 m side corridor, the stair at the back and an L-shaped 66 m² clinic around
a rear lightwell; above, offices of 48, 34 and 38 m² to the street and a 45 m²
office at the rear with a terrace. Twelve units in allocation. It saves to its
own document (`sheets/latakia-option-2`) so the two options never overwrite
each other; a switch at the top of both pages moves between them. Prices and
rates start as copies of the Option 1 figures so the comparison is like for
like.

The Option 2 plans shown on that page (`option-2/plan-*.svg`, PNG copies
beside them) are drawn by `option-2/plans.py` — shell and unit areas from the
architect's sheet, internal walls and furniture as a proposal. Edit the script
and re-run it (`--png` also re-renders the PNGs through headless Chrome).

`firestore.rules` holds the security rules both sheets need; see the comment
at its top before deploying.

## The project site

A one-page presentation site: a scroll-pinned hero that turns from day to night,
a statement, the key figures, the passage, the shops, five detail tiles, the two
floor plans and a WhatsApp enquiry. Bilingual throughout. See `site/README.md`
for how it is put together and how the images are produced.

## Progress

**Calculator** — built first, in the first week of September 2026: the sheet,
the bilingual hints, the Firestore save with shared storage, the third party
in allocation, then the split of each upper floor into four units.

**Site** — built 5 September: markup, stylesheet, scroll work, floor plans;
then the hero was reworked so the whole building shows, the shops were added
and the 3D model was dropped; the hero was pinned so day turning to night is
something you watch; Arabic was added throughout and the email replaced by
WhatsApp.

**Site, 6 September** — the facade render was replaced with the one that
names the shops (Atelier, Nomad) over their arches; all seven image assets are
cut from that sheet, and a fifth detail tile for the backlit shop sign was
added. The hero images were then widened so the render fills the frame instead
of sitting between blurred bands: sky with clouds above, cobbles below,
out-of-focus low-rise neighbours to either side. Finally the wall to the left
of the building was cut down to the shop line, so that side reads as low-rise.

**Calculator, 6 September (evening)** — a second sheet for the architect's
Option 2, with its own Firestore document, an option switch on both pages,
and furnished floor plans drawn from the Option 2 sheet.

**Open** — the contact number in the footer is the live one; nothing else is
placeholder. A higher-resolution export of the facade render would sharpen the
hero on large screens, since the current one is upscaled from about 650 px.
