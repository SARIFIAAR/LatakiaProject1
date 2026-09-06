# Khan Murjan — Latakia

A mixed-use building in Latakia: shops along a covered passage at street level,
clinics on the two floors above. This repository holds the two web pieces of the
project, both static, both served by GitHub Pages.

| | Where | Live |
|---|---|---|
| **Feasibility calculator** | `index.html` (and `test.html`, a scratch copy) | https://sarifiaar.github.io/LatakiaProject1/ |
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

**Open** — the contact number in the footer is the live one; nothing else is
placeholder. A higher-resolution export of the facade render would sharpen the
hero on large screens, since the current one is upscaled from about 650 px.
