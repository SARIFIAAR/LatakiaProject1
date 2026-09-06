# Khan Murjan — Latakia

A mixed-use building in Latakia: shops along a covered passage at street level,
clinics on the two floors above. This repository holds the two web pieces of the
project, both static, both served by GitHub Pages.

| | Where | Live |
|---|---|---|
| **Feasibility calculator — Option 1** | `index.html` (and `test.html`, a scratch copy) | https://sarifiaar.github.io/LatakiaProject1/ |
| **Feasibility calculator — Option 2** | `option-2.html`, plans in `option-2/` | https://sarifiaar.github.io/LatakiaProject1/option-2.html |
| **Feasibility calculator — Option 3 (recommended)** | `option-3.html`, plans in `option-3/` | https://sarifiaar.github.io/LatakiaProject1/option-3.html |
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
1.30 m side corridor, the stair at the back and an L-shaped 66 m² dental clinic glazed
onto a planted rear lightwell; above, clinic suites of 48, 34 and 38 m² to the street
and a 45 m² suite at the rear with a terrace, the lightwell kept open through
every floor. Twelve units in allocation. It saves to its
own document (`sheets/latakia-option-2`) so the two options never overwrite
each other; a switch at the top of both pages moves between them. Prices and
rates start as copies of the Option 1 figures so the comparison is like for
like.

The Option 2 plans shown on that page (`option-2/plan-*.svg`, PNG copies
beside them) are drawn by `option-2/plans.py` — shell and unit areas from the
architect's sheet, internal walls and furniture as a proposal. Edit the script
and re-run it (`--png` also re-renders the PNGs through headless Chrome).

### Option 3 — the recommended layout

`option-3.html` is our proposal on the Option 2 envelope: a 1.50 m passage
on the axis of the facade with a 4.20 m shop either side. Shop 1 is 11.80 m
deep (49.6 m²); shop 2 runs back to the clinic's door line, 13.20 m deep
(55.4 m²), so the corridor at the end of the passage serves only the stair.
Each shop has a mezzanine under the 5.00 m ground floor. The dental clinic is
entered from the end of the passage and is 48 m² net: waiting room glazed
onto the lightwell, one treatment room at the back beside it, the WC off a
small lobby, and the store in the front block's right-hand room (a second
treatment room was cancelled and merged into that store). The stair hall is
glazed onto the lightwell, and there are three suites per upper floor (53, 58
and 45 m², each with two treatment rooms) instead of four. Eleven units in
allocation, a mezzanine-slab cost row, its own document
`sheets/latakia-option-3` (schema 2). The plans come from
`option-3/plans.py`, which imports the drawing helpers from
`option-2/plans.py`; `plan-ground-side.*` is the earlier side-corridor
variant, kept for comparison and not shown on the page.

Saleable area on this sheet follows a rule the owner set: a shop has its own
street door, so it sells at its net area plus its walls only (the full outer
wall, half of each shared wall) and carries no common area. The passage,
corridor and stair hall serve the clinic and the six suites above, so those
38 m² are shared between the seven units in proportion to size, on top of
each unit's own walls. Option 2 still shares each floor plate across all its
units, shops included, so its shop figures are not on the same basis.

`firestore.rules` holds the security rules all three sheets need. It was deployed
on 6 September (`firebase deploy --only firestore:rules --project
latakia-feasibility`); before that the live rules admitted only the Option 1
document and Save on Option 2 failed.

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
and furnished floor plans drawn from the Option 2 sheet. Later the same
evening the upper floors were redrawn as clinic suites (the office fit-out
read as clutter), the ground clinic got a store in its dead corner, the
lightwell was planted and kept open through the upper floors.

**Calculator, 6 September (late)** — the ground clinic became a dental clinic
and the rules were deployed; then a third sheet, Option 3, for the layout we
recommend, with its own plans and a three-way switch on every sheet.

**Calculator, 6 September (night)** — on Option 3 shop 2 was deepened to the
clinic's door line, the clinic reduced to one treatment room with a merged
store, and the saleable areas re-based so the shops carry their walls only.
The sheet's schema went to 2 and the saved document was re-saved on the new
basis; the plan images gained a version query so browsers drop the old
drawing.

**Open** — the contact number in the footer is the live one; nothing else is
placeholder. A higher-resolution export of the facade render would sharpen the
hero on large screens, since the current one is upscaled from about 650 px.
