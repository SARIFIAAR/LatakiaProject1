#!/usr/bin/env python3
"""
Recommended layout ("Option 3"): Option 2's side-corridor parti with its
weak points fixed. Same plot, same envelope, same lightwell and terrace.

  Ground   corridor 1.50 m (was 1.30); two shops of 4.20 x 11.80 m instead of
           three of 2.80 (same net shop area, one party wall fewer); mezzanine
           in each shop under the 5.00 m ground floor; the stair hall glazed
           onto the lightwell; the dental clinic as drawn for Option 2.
  Typical  three suites instead of four: two street suites of about 53 and
           58 m2, each with two treatment rooms, and the 45 m2 rear suite with
           its terrace; the corridor is 3 m long instead of 8; the stair is
           daylit from the open lightwell on every floor.

    python3 option-3/plans.py --png
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "option-2"))
from plans import Plan, W, D, OW, PW, IW, INK, FURN, export_png   # noqa: E402


def shell_ground(p):
    p.vwall(0, 0, D, OW); p.vwall(W - OW, 0, D, OW); p.hwall(0, W, 0, OW)
    p.vwall(540, 0, 455, 25); p.hwall(0, 565, 430, 25)
    p.hatch(25, 25, 540, 430, "well")
    p.rect(45, 45, 475, 40, rx=4); p.rect(45, 345, 475, 40, rx=4)
    for cx, cy, r in ((90, 65, 26), (170, 65, 22), (250, 65, 28), (330, 65, 22), (410, 65, 27), (480, 65, 22),
                      (90, 365, 24), (170, 365, 28), (250, 365, 22), (330, 365, 27), (410, 365, 23), (480, 365, 26),
                      (70, 150, 30), (70, 260, 34), (500, 150, 32), (500, 260, 30)):
        p.plant(cx, cy, r)
    p.tree(285, 215); p.rect(200, 190, 60, 50, rx=8); p.rect(310, 190, 60, 50, rx=8)
    p.room(285, 315, "منور مزروع", "Planted lightwell", 24)


def clinic(p, cross=False):
    """The Option 2 dental clinic. With cross=True a corridor 1.35 m deep is cut
    off its front edge between the stair hall and the passage, and the entrance
    moves to the axis."""
    """The Option 2 dental clinic, unchanged: it already works."""
    if cross:
        p.vwall(245, 430, 830, PW)
        p.hwall(245, 610, 815, 15); p.door_slide_h(480, 815, 830, 110)
        p.vwall(610, 830, 950, 15)
    else:
        p.vwall(245, 430, 950, PW)
        p.door_v(245, 260, 850, 90, "b", "r")
    p.vwall(700, 640, 950, IW); p.door_v(700, 710, 830, 90, "b", "r")
    p.hwall(260, 1045, 630, IW)
    p.vwall(420, 455, 630, IW); p.door_h(300, 630, 640, 80, "l", "u")
    p.vwall(600, 455, 630, IW); p.door_h(480, 630, 640, 80, "l", "u")
    p.door_h(615, 630, 640, 85, "l", "u")
    p.vwall(790, 455, 630, IW); p.door_h(830, 630, 640, 80, "l", "u")
    p.hwall(565, 1045, 445, IW); p.door_h(600, 445, 455, 90, "l", "u")
    p.glass_v(540, 565, 25, 430)
    if cross:
        p.counter(430, 700, 180, 60); p.chair(520, 670, 0)
        p.sofa(270, 650, 60, 150, "l"); p.rect(350, 720, 60, 60, rx=6); p.sofa(635, 650, 60, 150, "r")
        p.label(430, 795, "عيادة أسنان", size=26, weight=600, anchor="end")
        p.label(450, 795, "61 m²", size=24, weight=600, anchor="start")
        p.label(520, 812, "Dental clinic", size=15, color=FURN)
    else:
        p.counter(430, 655, 180, 60); p.chair(520, 745, 180)
        p.sofa(270, 650, 60, 190, "l"); p.rect(350, 780, 60, 60, rx=6); p.sofa(400, 880, 200, 60, "b")
        p.unit(560, 800, "عيادة أسنان", "66 m²", "Dental clinic")
    p.counter(830, 890, 200, 55); p.basin(930, 917, 0); p.dental_chair(860, 760, 90)
    p.toilet(300, 500, 0); p.basin(390, 600, 90)
    p.counter(435, 460, 160, 55); p.basin(470, 487, 0); p.rect(545, 465, 45, 45, rx=4)
    p.shelf(805, 460, 235, 40); p.shelf(1000, 505, 40, 120)
    p.counter(985, 40, 55, 250); p.basin(1012, 120, 90); p.dental_chair(800, 250)
    p.rect(590, 380, 50, 50, rx=4); p.label(615, 448, "X-ray", size=14, color=FURN)
    p.room(660, 900, "انتظار", "Waiting", 22)
    p.room(765, 680, "علاج ١", "Treatment 1", 22); p.room(700, 410, "علاج ٢", "Treatment 2", 22)
    p.room(340, 560, "حمام", "WC", 22); p.room(515, 540, "تعقيم", "Sterilisation", 18)
    p.room(920, 580, "مخزن", "Store", 22); p.room(700, 525, "ممر", None, 20)


def ground():
    p = Plan()
    shell_ground(p)
    clinic(p)
    # stair, hall glazed onto the lightwell
    p.glass_h(40, 230, 430, 455)
    p.stair(25, 455, 220, 495)
    p.room(135, 900, "درج", "Stair · daylit", 22)
    # shops' back wall, open at the corridor
    p.hwall(175, W, 950, 20)
    # corridor 1.50 and two shops of 4.20
    p.vwall(175, 970, D, PW); p.vwall(610, 970, D, PW)
    p.hwall(25, 175, 2135, 15); p.door_h(45, 2135, 2150, 110, "l", "u")
    for i, (a, b) in enumerate(((190, 610), (625, 1045))):
        m = (a + b) // 2
        p.hwall(a, b, 2135, 15)
        p.glass_h(a, m - 55, 2135, 2150); p.glass_h(m + 55, b, 2135, 2150)
        p.door_h(m - 55, 2135, 2150, 110, "l", "u")
        # back of house: WC and store under the mezzanine
        p.hwall(a, b, 1200, IW); p.vwall(a + 120, 970, 1200, IW)
        p.door_h(a + 20, 1200, 1210, 80, "l", "u"); p.door_h(b - 110, 1200, 1210, 90, "r", "u")
        p.toilet(a + 60, 1010, 0); p.basin(a + 60, 1165, 180)
        p.shelf(a + 140, 975, b - a - 150, 40)
        # mezzanine over the back 4.8 m, reached by a straight stair on the party wall
        p.f(f'<rect x="{a}" y="970" width="{b-a}" height="480" fill="none" stroke-dasharray="14 10"/>')
        p.f(f'<rect x="{b-95}" y="1220" width="90" height="300" fill="none"/>')
        for k in range(1, 12):
            p.f(f'<line x1="{b-95}" y1="{1220+k*25}" x2="{b-5}" y2="{1220+k*25}"/>')
        p.f(f'<line x1="{b-50}" y1="1560" x2="{b-50}" y2="1245" stroke-width="3"/>'
            f'<path d="M{b-62} 1265 L{b-50} 1245 L{b-38} 1265" fill="none" stroke-width="3"/>')
        p.room(m, 1330, "ميزانين فوق", "Mezzanine over", 20)
        # sales floor
        p.shelf(a + 5, 1470, 40, 560); p.shelf(b - 45, 1600, 40, 430)
        p.counter(a + 60, 1480, 200, 65); p.chair(a + 160, 1435, 0)
        p.rect(m - 60, 1750, 120, 200, rx=6); p.rect(m - 160, 1750, 70, 200, rx=6); p.rect(m + 90, 1750, 70, 200, rx=6)
        p.plant(a + 45, 2095); p.plant(b - 45, 2095)
        p.unit(m, 1640, f"محل {'١٢'[i]}", "49.6 m²", f"Shop {i+1} · 4.20 × 11.80")
        p.room(a + 60, 1090, "حمام", None, 20); p.room(m + 60, 1090, "مستودع", "Store", 20)
    p.room(100, 1560, "ممر", "Corridor 1.50", 22)
    y = D + 130
    p.dim_h(0, W, y + 60, "10.70")
    p.dim_h(25, 175, y, "1.50"); p.dim_h(190, 610, y, "4.20"); p.dim_h(625, 1045, y, "4.20")
    x = W + 80
    p.dim_v(x + 60, 0, D, "21.50")
    p.dim_v(x, 0, 430, "4.30"); p.dim_v(x, 455, 950, "4.95"); p.dim_v(x, 970, D, "11.80")
    return p


def shop(p, a, b, ytop, i, area, dims):
    """One shop between party walls a..b from its back wall at ytop to the street,
    with WC and store under a mezzanine at the back."""
    m = (a + b) // 2
    p.hwall(a, b, 2135, 15)
    p.glass_h(a, m - 55, 2135, 2150); p.glass_h(m + 55, b, 2135, 2150)
    p.door_h(m - 55, 2135, 2150, 110, "l", "u")
    p.hwall(a, b, ytop + 230, IW); p.vwall(a + 120, ytop, ytop + 230, IW)
    p.door_h(a + 20, ytop + 230, ytop + 240, 80, "l", "u"); p.door_h(b - 110, ytop + 230, ytop + 240, 90, "r", "u")
    p.toilet(a + 60, ytop + 40, 0); p.basin(a + 60, ytop + 195, 180)
    p.shelf(a + 140, ytop + 5, b - a - 150, 40)
    p.f(f'<rect x="{a}" y="{ytop}" width="{b-a}" height="480" fill="none" stroke-dasharray="14 10"/>')
    p.f(f'<rect x="{b-95}" y="{ytop+250}" width="90" height="300" fill="none"/>')
    for k in range(1, 12):
        p.f(f'<line x1="{b-95}" y1="{ytop+250+k*25}" x2="{b-5}" y2="{ytop+250+k*25}"/>')
    p.f(f'<line x1="{b-50}" y1="{ytop+590}" x2="{b-50}" y2="{ytop+275}" stroke-width="3"/>'
        f'<path d="M{b-62} {ytop+295} L{b-50} {ytop+275} L{b-38} {ytop+295}" fill="none" stroke-width="3"/>')
    p.room(m, ytop + 360, "ميزانين فوق", "Mezzanine over", 20)
    p.shelf(a + 5, ytop + 500, 40, 2030 - ytop - 500); p.shelf(b - 45, ytop + 630, 40, 2030 - ytop - 630)
    p.counter(a + 60, ytop + 510, 200, 65); p.chair(a + 160, ytop + 465, 0)
    ty = max(1750, ytop + 700)
    p.rect(m - 60, ty, 120, 200, rx=6); p.rect(m - 160, ty, 70, 200, rx=6); p.rect(m + 90, ty, 70, 200, rx=6)
    p.plant(a + 45, 2095); p.plant(b - 45, 2095)
    p.unit(m, ytop + 620, f"محل {'١٢'[i]}", area, f"Shop {i+1} · {dims}")
    p.room(a + 60, ytop + 120, "حمام", None, 20); p.room(m + 60, ytop + 120, "مستودع", "Store", 20)


def ground_central():
    """The passage on the facade's axis; at its end a corridor 1.35 m deep, cut
    from the clinic's front edge, turns left to the stair. The clinic is
    entered from the axis. Both shops keep their full depth."""
    p = Plan()
    shell_ground(p)
    clinic(p, cross=True)
    p.glass_h(40, 230, 430, 455)
    p.stair(25, 455, 220, 495)
    p.room(135, 900, "درج", "Stair · daylit", 22)
    p.hwall(25, 445, 950, 20); p.hwall(625, W, 950, 20)        # the shops' back walls
    p.vwall(445, 950, D, PW); p.vwall(610, 950, D, PW)          # the passage
    p.hwall(460, 610, 2135, 15); p.door_h(470, 2135, 2150, 130, "l", "u")
    shop(p, 25, 445, 970, 0, "49.6 m²", "4.20 × 11.80")
    shop(p, 625, 1045, 970, 1, "49.6 m²", "4.20 × 11.80")
    p.room(535, 1560, "ممر", "Passage 1.50", 22)
    p.room(400, 895, "ممر", None, 18)
    y = D + 130
    p.dim_h(0, W, y + 60, "10.70")
    p.dim_h(25, 445, y, "4.20"); p.dim_h(460, 610, y, "1.50"); p.dim_h(625, 1045, y, "4.20")
    x = W + 80
    p.dim_v(x + 60, 0, D, "21.50")
    p.dim_v(x, 0, 430, "4.30"); p.dim_v(x, 455, 950, "4.95"); p.dim_v(x, 970, D, "11.80")
    return p


def suite_dental(p, a, b, ytop, door, name_ar, area, name_en):
    """Street suite a..b from the corridor wall at ytop: waiting with reception,
    WC and sterilisation by the door, two treatment rooms at the window."""
    w = b - a
    # WC and sterilisation in the top-right corner
    p.vwall(b - 300, ytop, ytop + 150, IW); p.hwall(b - 300, b, ytop + 150, IW); p.vwall(b - 150, ytop, ytop + 150, IW)
    p.door_h(b - 265, ytop + 150, ytop + 160, 80, "l", "u"); p.door_h(b - 115, ytop + 150, ytop + 160, 80, "l", "u")
    p.counter(b - 295, ytop + 5, 140, 50); p.basin(b - 250, ytop + 30, 0); p.rect(b - 200, ytop + 8, 42, 42, rx=4)
    p.toilet(b - 45, ytop + 45, 0); p.basin(b - 120, ytop + 120, 270)
    p.room(b - 225, ytop + 110, "تعقيم", None, 16); p.room(b - 112, ytop + 60, "حمام", None, 16)
    # waiting
    if door == "top":
        p.counter(a + 15, ytop + 110, 150, 55); p.chair(a + 90, ytop + 195, 0)
    else:
        p.counter(a + 15, ytop + 120, 150, 55); p.chair(a + 90, ytop + 205, 0)
    p.sofa(a + 15, ytop + 250, 60, 260, "l")
    p.sofa(a + 100, D - 640, 240, 60, "b")
    p.plant(b - 40, ytop + 200)
    # two treatment rooms at the street
    ys = D - 560
    p.hwall(a, b, ys, IW); m = a + w // 2; p.vwall(m - 5, ys, D, IW)
    p.door_h(a + 25, ys, ys + IW, 85, "l", "d"); p.door_h(m + 20, ys, ys + IW, 85, "l", "d")
    for ra, rb in ((a, m - 5), (m + 5, b)):
        rm = (ra + rb) // 2
        p.dental_chair(rm + 10, ys + 300)
        p.counter(ra + 10, D - 80, rb - ra - 20, 50); p.basin(rm, D - 55, 0)
    p.room(a + (3 * w) // 8 + 20, ys + 52, "علاج ١", "Treatment 1", 18); p.room(m + 5 + (3 * w) // 8 + 20, ys + 52, "علاج ٢", "Treatment 2", 18)
    p.unit((a + b) // 2, ytop + 330 if door == "top" else ytop + 380, name_ar, area, name_en)


def typical():
    p = Plan()
    p.vwall(0, 430, D, OW); p.vwall(W - OW, 430, D, OW); p.hwall(0, W, 430, 25)
    p.vwall(0, 0, 430, 8); p.vwall(W - 8, 0, 430, 8); p.hwall(0, W, 0, 8)
    p.vwall(540, 0, 455, 25); p.void(25, 25, 540, 430); p.hatch(565, 8, W - 8, 430, "terrace")
    p.glass_h(40, 230, 430, 455)                      # stair hall daylit from the void
    p.glass_h(440, 530, 430, 455); p.glass_h(760, 830, 430, 455)
    p.door_h(850, 430, 455, 100, "l", "u"); p.glass_h(970, 1030, 430, 455)
    # stair, rear suite, short corridor, two street suites
    p.vwall(245, 455, 965, PW)
    p.hwall(245, 550, 965, PW)
    p.hwall(0, 550, 1100, PW)
    p.vwall(535, 980, D, PW)
    p.hwall(0, W, 2125, 25)
    for x0, x1 in ((60, 240), (320, 500), (590, 770), (850, 1020)):
        p.glass_h(x0, x1, 2125, 2150)
    p.stair(25, 455, 220, 510)
    p.room(135, 920, "درج", "Stair · daylit", 22)
    p.room(390, 1052, "ممر", "Corridor 1.20", 20)

    # rear suite (45 m2), as in Option 2
    p.door_v(245, 260, 860, 90, "b", "r")
    p.vwall(420, 455, 600, IW); p.hwall(260, 430, 600, IW); p.door_h(320, 600, 610, 80, "l", "u"); p.shelf(265, 460, 150, 40)
    p.vwall(570, 455, 965, IW); p.hwall(570, 730, 620, IW); p.door_v(570, 580, 800, 90, "b", "r")
    p.vwall(730, 455, 620, IW); p.door_v(730, 740, 470, 80, "t", "l")
    p.toilet(655, 500, 0); p.basin(700, 590, 90)
    p.sofa(270, 640, 60, 240, "l"); p.counter(400, 640, 160, 60); p.chair(480, 730, 0); p.plant(540, 930)
    p.dental_chair(830, 780, 90); p.counter(800, 900, 230, 50); p.basin(915, 925, 0)
    p.unit(430, 790, "عيادة خلفية", "45 m²", "Rear suite")
    p.room(340, 540, "مخزن", "Store", 18); p.room(655, 470, "حمام", None, 18)
    p.room(805, 330, "تراس", "Terrace", 26); p.room(282, 240, "منور", "Lightwell · open", 26)

    # street suites
    p.door_h(300, 1100, 1115, 90, "l", "d")
    suite_dental(p, 25, 535, 1115, "top", "عيادة أ", "53 m²", "Suite A · 5.10 × 10.35")
    p.door_v(535, 550, 990, 90, "t", "r")
    suite_dental(p, 550, 1045, 980, "left", "عيادة ب", "58 m²", "Suite B · 4.95 × 11.70")

    y = D + 130
    p.dim_h(0, W, y + 60, "10.70")
    p.dim_h(25, 535, y, "5.10"); p.dim_h(550, 1045, y, "4.95")
    x = W + 80
    p.dim_v(x + 60, 0, D, "21.50")
    p.dim_v(x, 0, 430, "4.30"); p.dim_v(x, 455, 965, "5.10")
    p.dim_v(x, 980, 1100, "1.20"); p.dim_v(x, 1115, D, "10.35")
    return p


if __name__ == "__main__":
    for name, fn, title in (("plan-ground", ground_central, "Recommended — ground floor"),
                            ("plan-ground-side", ground, "Recommended — ground floor, side-corridor variant"),
                            ("plan-typical", typical, "Recommended — typical upper floor")):
        path = os.path.join(HERE, name + ".svg")
        with open(path, "w") as f:
            f.write(fn().svg(title))
        print("wrote", path)
        if "--png" in sys.argv:
            export_png(path, os.path.join(HERE, name + ".png"))
