#!/usr/bin/env python3
"""
Draws the Option 2 floor plans as SVG: the ground floor and the typical upper
floor, with internal walls and furniture. One drawing unit is one centimetre;
y = 0 is the rear boundary and y = 2150 the street.

    python3 option-2/plans.py            # writes plan-ground.svg / plan-typical.svg
    python3 option-2/plans.py --png      # also renders PNGs through headless Chrome

The shell geometry follows the architect's OPTION 2 sheet (10.70 x 21.50 m
plot, three 2.80 m shops on a 1.30 m side corridor, stair at the back, an
L-shaped 66 m2 clinic around a rear lightwell; above, offices of 4.30 / 2.80 /
2.80 m to the street on a 1.20 m corridor and a 45 m2 office at the rear).
Partitions and furniture are this script's proposal, not the architect's.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

W, D = 1070, 2150            # plot
OW, PW, IW = 25, 15, 10      # outer wall, party wall, partition

INK   = "#1c2a33"
FURN  = "#5f7079"
SOFT  = "#aebcc3"
GLASS = "#2f8f9d"
HATCH = "#b7c4ca"
DIM   = "#6f8590"
FONT  = "'IBM Plex Sans','IBM Plex Sans Arabic',-apple-system,'Helvetica Neue',Arial,sans-serif"

LAYERS = ("fill", "wall", "open", "glass", "door", "furn", "text", "dim")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


class Plan:
    def __init__(self):
        self.L = {k: [] for k in LAYERS}

    def add(self, layer, s):
        self.L[layer].append(s)

    # ---- walls -------------------------------------------------------------
    def wall(self, x0, y0, x1, y1):
        self.add("wall", f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}"/>')

    def hwall(self, x0, x1, y, t):
        self.wall(x0, y, x1, y + t)

    def vwall(self, x, y0, y1, t):
        self.wall(x, y0, x + t, y1)

    def opening(self, x0, y0, x1, y1):
        self.add("open", f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}"/>')

    # ---- doors -------------------------------------------------------------
    def door_h(self, x, y0, y1, w=90, hinge="l", swing="d"):
        """Door in a horizontal wall occupying y0..y1. Opening x..x+w."""
        self.opening(x, y0 - 1, x + w, y1 + 1)
        hx = x if hinge == "l" else x + w
        dx = 1 if hinge == "l" else -1
        ym = y1 if swing == "d" else y0
        dy = 1 if swing == "d" else -1
        lx, ly = hx, ym + dy * w
        ex, ey = hx + dx * w, ym
        sweep = 1 if (hinge == "r") != (swing == "u") else 0
        self.add("door", f'<line x1="{hx}" y1="{ym}" x2="{lx}" y2="{ly}"/>'
                         f'<path d="M{lx} {ly} A{w} {w} 0 0 {sweep} {ex} {ey}"/>')

    def door_v(self, x0, x1, y, w=90, hinge="t", swing="r"):
        """Door in a vertical wall occupying x0..x1. Opening y..y+w."""
        self.opening(x0 - 1, y, x1 + 1, y + w)
        hy = y if hinge == "t" else y + w
        dy = 1 if hinge == "t" else -1
        xm = x1 if swing == "r" else x0
        dx = 1 if swing == "r" else -1
        lx, ly = xm + dx * w, hy
        ex, ey = xm, hy + dy * w
        sweep = 1 if (hinge == "t") == (swing == "r") else 0
        self.add("door", f'<line x1="{xm}" y1="{hy}" x2="{lx}" y2="{ly}"/>'
                         f'<path d="M{lx} {ly} A{w} {w} 0 0 {sweep} {ex} {ey}"/>')

    # ---- glazing -----------------------------------------------------------
    def glass_h(self, x0, x1, y0, y1):
        self.opening(x0, y0 - 1, x1, y1 + 1)
        ym = (y0 + y1) / 2
        self.add("glass", f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}"/>'
                          f'<line x1="{x0}" y1="{ym}" x2="{x1}" y2="{ym}"/>'
                          f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}"/>')

    def glass_v(self, x0, x1, y0, y1):
        self.opening(x0 - 1, y0, x1 + 1, y1)
        xm = (x0 + x1) / 2
        self.add("glass", f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}"/>'
                          f'<line x1="{xm}" y1="{y0}" x2="{xm}" y2="{y1}"/>'
                          f'<line x1="{x1}" y1="{y0}" x2="{x1}" y2="{y1}"/>')

    def glass_partition_h(self, x0, x1, y):
        self.add("glass", f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke-width="4"/>')

    def glass_partition_v(self, x, y0, y1):
        self.add("glass", f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke-width="4"/>')

    # ---- hatch / fills -----------------------------------------------------
    def hatch(self, x0, y0, x1, y1, kind="terrace"):
        self.add("fill", f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="url(#{kind})"/>')

    def void(self, x0, y0, x1, y1):
        self.add("fill", f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#fff" '
                         f'stroke="{INK}" stroke-width="3" stroke-dasharray="18 10"/>'
                         f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{SOFT}" stroke-width="2"/>'
                         f'<line x1="{x1}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{SOFT}" stroke-width="2"/>')

    # ---- furniture ---------------------------------------------------------
    def f(self, s):
        self.add("furn", s)

    def rect(self, x, y, w, h, rx=0, extra=""):
        self.f(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" {extra}/>')

    def chair(self, cx, cy, rot=0):
        # 45 x 45 seat with a back on its top edge; rot in degrees (back faces up at 0)
        self.f(f'<g transform="translate({cx} {cy}) rotate({rot})">'
               f'<rect x="-22" y="-20" width="44" height="42" rx="8"/>'
               f'<line x1="-22" y1="-20" x2="22" y2="-20" stroke-width="5"/></g>')

    def desk(self, x, y, w, h, chair="b"):
        """Desk with one chair on the side given: t/b/l/r (the chair's back faces away)."""
        self.rect(x, y, w, h)
        if chair == "b":
            self.chair(x + w / 2, y + h + 32, 180)
        elif chair == "t":
            self.chair(x + w / 2, y - 32, 0)
        elif chair == "l":
            self.chair(x - 32, y + h / 2, 270)
        elif chair == "r":
            self.chair(x + w + 32, y + h / 2, 90)

    def table(self, cx, cy, w, h, top=2, bottom=2, left=0, right=0):
        self.rect(cx - w / 2, cy - h / 2, w, h, rx=6)
        for i in range(top):
            self.chair(cx - w / 2 + (i + 0.5) * w / top, cy - h / 2 - 32, 0)
        for i in range(bottom):
            self.chair(cx - w / 2 + (i + 0.5) * w / bottom, cy + h / 2 + 32, 180)
        for i in range(left):
            self.chair(cx - w / 2 - 32, cy - h / 2 + (i + 0.5) * h / left, 270)
        for i in range(right):
            self.chair(cx + w / 2 + 32, cy - h / 2 + (i + 0.5) * h / right, 90)

    def sofa(self, x, y, w, h, back="t"):
        self.rect(x, y, w, h, rx=10)
        if back in ("t", "b"):
            by = y + 14 if back == "t" else y + h - 14
            self.f(f'<line x1="{x+4}" y1="{by}" x2="{x+w-4}" y2="{by}"/>')
            n = max(1, round(w / 65))
            for i in range(1, n):
                self.f(f'<line x1="{x + i*w/n}" y1="{y+16}" x2="{x + i*w/n}" y2="{y+h-4}"/>')
        else:
            bx = x + 14 if back == "l" else x + w - 14
            self.f(f'<line x1="{bx}" y1="{y+4}" x2="{bx}" y2="{y+h-4}"/>')
            n = max(1, round(h / 65))
            for i in range(1, n):
                self.f(f'<line x1="{x+16}" y1="{y + i*h/n}" x2="{x+w-4}" y2="{y + i*h/n}"/>')

    def bed(self, x, y, w=70, h=190, pillow="t"):
        self.rect(x, y, w, h, rx=6)
        if pillow == "t":
            self.rect(x + 8, y + 8, w - 16, 30, rx=6)
        else:
            self.rect(x + 8, y + h - 38, w - 16, 30, rx=6)

    def toilet(self, cx, cy, rot=0):
        self.f(f'<g transform="translate({cx} {cy}) rotate({rot})">'
               f'<rect x="-25" y="-38" width="50" height="18" rx="3"/>'
               f'<ellipse cx="0" cy="8" rx="19" ry="26"/></g>')

    def basin(self, cx, cy, rot=0):
        self.f(f'<g transform="translate({cx} {cy}) rotate({rot})">'
               f'<rect x="-27" y="-18" width="54" height="36" rx="4"/>'
               f'<circle cx="0" cy="2" r="11"/></g>')

    def shelf(self, x, y, w, h):
        self.rect(x, y, w, h)
        if w >= h:
            step = 40
            for i in range(1, int(w // step)):
                self.f(f'<line x1="{x+i*step}" y1="{y}" x2="{x+i*step}" y2="{y+h}" stroke="{SOFT}"/>')
        else:
            step = 40
            for i in range(1, int(h // step)):
                self.f(f'<line x1="{x}" y1="{y+i*step}" x2="{x+w}" y2="{y+i*step}" stroke="{SOFT}"/>')

    def counter(self, x, y, w, h):
        self.rect(x, y, w, h)
        self.rect(x + 6, y + 6, w - 12, h - 12, extra=f'stroke="{SOFT}"')

    def plant(self, cx, cy, r=22):
        self.f(f'<circle cx="{cx}" cy="{cy}" r="{r}"/><circle cx="{cx}" cy="{cy}" r="{r*0.45}" stroke="{SOFT}"/>')

    def stair(self, x, y, w, h, land=120, hall=120, tread=27):
        """Dog-leg stair in a well x..x+w, y..y+h: landing at the top (rear),
        two flights side by side, hall at the bottom."""
        fw = (w - 10) / 2
        y0, y1 = y + land, y + h - hall
        n = int((y1 - y0) // tread)
        for k in (0, 1):
            fx = x + k * (fw + 10)
            self.f(f'<rect x="{fx}" y="{y0}" width="{fw}" height="{y1-y0}" fill="none"/>')
            for i in range(1, n + 1):
                yy = y0 + i * tread
                if yy < y1:
                    self.f(f'<line x1="{fx}" y1="{yy}" x2="{fx+fw}" y2="{yy}"/>')
        # landing edge and the well between flights
        self.f(f'<line x1="{x}" y1="{y0}" x2="{x+w}" y2="{y0}"/>')
        self.f(f'<rect x="{x+fw}" y="{y0}" width="10" height="{y1-y0}" fill="{INK}"/>')
        # up arrow on the first flight (right-hand flight, walking up from the hall)
        ax = x + fw + 10 + fw / 2
        self.f(f'<line x1="{ax}" y1="{y1+40}" x2="{ax}" y2="{y0+30}" stroke-width="3"/>'
               f'<path d="M{ax-12} {y0+52} L{ax} {y0+30} L{ax+12} {y0+52}" fill="none" stroke-width="3"/>')

    # ---- text --------------------------------------------------------------
    def label(self, x, y, s, size=30, weight=500, anchor="middle", color=INK, rot=0, cls=""):
        tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
        self.add("text", f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
                         f'text-anchor="{anchor}" fill="{color}"{tr}>{esc(s)}</text>')

    def room(self, x, y, ar, en=None, size=26):
        """Arabic name with a smaller English gloss underneath."""
        self.label(x, y, ar, size=size, weight=500)
        if en:
            self.label(x, y + size * 0.85, en, size=size * 0.7, weight=400, color=FURN)

    def unit(self, x, y, ar, area, en=None):
        self.label(x, y, ar, size=34, weight=600)
        self.label(x, y + 36, area, size=30, weight=500)
        if en:
            self.label(x, y + 64, en, size=22, weight=400, color=FURN)

    # ---- dimensions --------------------------------------------------------
    def dim_h(self, x0, x1, y, text, size=24):
        self.add("dim", f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}"/>'
                        f'<line x1="{x0}" y1="{y-10}" x2="{x0}" y2="{y+10}"/>'
                        f'<line x1="{x1}" y1="{y-10}" x2="{x1}" y2="{y+10}"/>'
                        f'<text x="{(x0+x1)/2}" y="{y-8}" font-size="{size}" text-anchor="middle">{esc(text)}</text>')

    def dim_v(self, x, y0, y1, text, size=24):
        self.add("dim", f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}"/>'
                        f'<line x1="{x-10}" y1="{y0}" x2="{x+10}" y2="{y0}"/>'
                        f'<line x1="{x-10}" y1="{y1}" x2="{x+10}" y2="{y1}"/>'
                        f'<text x="{x-10}" y="{(y0+y1)/2}" font-size="{size}" text-anchor="middle" '
                        f'transform="rotate(-90 {x-10} {(y0+y1)/2})">{esc(text)}</text>')

    # ---- output ------------------------------------------------------------
    def svg(self, title):
        vb = (-170, -90, 1420, 2400)
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" '
               f'width="{vb[2]}" height="{vb[3]}" font-family="{FONT}">',
               f'<title>{esc(title)}</title>',
               '<defs>',
               f'<pattern id="terrace" width="28" height="28" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
               f'<line x1="0" y1="0" x2="0" y2="28" stroke="{HATCH}" stroke-width="2"/></pattern>',
               f'<pattern id="well" width="20" height="20" patternUnits="userSpaceOnUse">'
               f'<line x1="0" y1="10" x2="20" y2="10" stroke="{HATCH}" stroke-width="1.5"/>'
               f'<line x1="10" y1="0" x2="10" y2="20" stroke="{HATCH}" stroke-width="1.5"/></pattern>',
               '</defs>',
               f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="#fff"/>']
        style = {
            "fill":  "",
            "wall":  f'fill="{INK}"',
            "open":  'fill="#fff"',
            "glass": f'fill="none" stroke="{GLASS}" stroke-width="2.5"',
            "door":  f'fill="none" stroke="{INK}" stroke-width="2.5"',
            "furn":  f'fill="#fff" stroke="{FURN}" stroke-width="2.2" stroke-linejoin="round"',
            "text":  "",
            "dim":   f'fill="{DIM}" stroke="{DIM}" stroke-width="1.5"',
        }
        for k in LAYERS:
            if self.L[k]:
                out.append(f'<g id="{k}" {style[k]}>')
                out.extend(self.L[k])
                out.append('</g>')
        # street label, as on the site's plans
        out.append(f'<text x="{W/2}" y="{D+70}" font-size="30" font-weight="500" text-anchor="middle" '
                   f'fill="{DIM}" letter-spacing="4">STREET · الشارع</text>')
        out.append('</svg>')
        return "\n".join(out)


# =============================================================================
def ground():
    p = Plan()

    # ---- envelope ---------------------------------------------------------
    p.vwall(0, 0, D, OW)
    p.vwall(W - OW, 0, D, OW)
    p.hwall(0, W, 0, OW)

    # rear lightwell, walled on two sides; open to sky
    p.vwall(540, 0, 455, 25)
    p.hwall(0, 565, 430, 25)
    p.hatch(25, 25, 540, 430, "well")

    # stair / clinic wall, shops' back wall
    p.vwall(245, 430, 950, PW)
    p.hwall(160, W, 950, 20)                                   # open to the corridor at the stair hall

    # side corridor and the three shops
    p.vwall(160, 970, D, PW)
    p.vwall(455, 970, D, PW)
    p.vwall(750, 970, D, PW)

    # front: corridor entrance door, three glazed shopfronts with a door each
    p.hwall(25, 160, 2135, 15)
    p.door_h(40, 2135, 2150, 110, "l", "u")
    for a, b in ((175, 455), (470, 750), (765, 1045)):
        m = (a + b) // 2
        p.hwall(a, b, 2135, 15)
        p.glass_h(a, m - 50, 2135, 2150)
        p.glass_h(m + 50, b, 2135, 2150)
        p.door_h(m - 50, 2135, 2150, 100, "l", "u")

    # ---- stair --------------------------------------------------------------
    p.stair(25, 455, 220, 495)
    p.room(135, 900, "درج", "Stair", 24)

    # ---- clinic -------------------------------------------------------------
    p.door_v(245, 260, 850, 90, "b", "r")                     # from the stair hall
    # waiting | consulting 1
    p.vwall(620, 640, 950, IW)
    p.door_v(620, 630, 830, 90, "b", "r")
    # cross partition with the WC, an open hall and a store behind it
    p.hwall(260, 1045, 630, IW)
    p.vwall(420, 455, 630, IW)                                 # WC
    p.door_h(300, 630, 640, 80, "l", "u")
    p.opening(450, 629, 600, 641)                              # open to the hall
    p.vwall(790, 455, 630, IW)                                 # store
    p.door_h(830, 630, 640, 80, "l", "u")
    # wing: second consulting room, lit from the lightwell
    p.hwall(565, 1045, 445, IW)
    p.door_h(600, 445, 455, 90, "l", "u")
    p.glass_v(540, 565, 150, 380)

    # furniture
    p.counter(430, 655, 180, 60);      p.chair(520, 745, 180)
    p.sofa(270, 650, 60, 190, "l")
    p.sofa(400, 880, 200, 60, "b")
    p.rect(350, 780, 60, 60, rx=6)                             # coffee table
    p.desk(800, 700, 160, 80, "t");   p.chair(840, 810, 0);  p.chair(920, 810, 0)
    p.bed(960, 770, 70, 170, "b")
    p.basin(665, 918, 0)
    p.f(f'<line x1="930" y1="760" x2="930" y2="945" stroke-dasharray="10 8"/>')   # curtain
    p.toilet(300, 500, 0);  p.basin(390, 600, 90)
    p.shelf(805, 460, 235, 40)
    p.desk(600, 300, 160, 80, "b");   p.chair(640, 250, 180); p.chair(720, 250, 180)
    p.bed(960, 60, 70, 170, "t")
    p.basin(600, 60, 180)
    p.f(f'<line x1="930" y1="40" x2="930" y2="250" stroke-dasharray="10 8"/>')

    p.unit(650, 545, "عيادة", "66 m²", "Clinic")
    p.room(440, 815, "انتظار", "Waiting", 24)
    p.room(760, 880, "فحص ١", "Consulting 1", 24)
    p.room(850, 400, "فحص ٢", "Consulting 2", 24)
    p.room(340, 560, "حمام", "WC", 22)
    p.room(920, 560, "مخزن", "Store", 22)
    p.room(280, 235, "منور", "Lightwell · open to sky", 26)

    # ---- shops --------------------------------------------------------------
    for i, (a, b) in enumerate(((175, 455), (470, 750), (765, 1045))):
        m = (a + b) // 2
        p.hwall(a, b, 1200, IW)                                 # back-of-house
        p.vwall(a + 120, 970, 1200, IW)                         # WC | store
        p.door_h(a + 20, 1200, 1210, 80, "l", "u")
        p.door_h(b - 110, 1200, 1210, 90, "r", "u")
        p.toilet(a + 60, 1010, 0);  p.basin(a + 60, 1165, 180)
        p.shelf(a + 140, 975, b - a - 150, 40)
        p.shelf(a + 5, 1240, 40, 720)
        p.shelf(b - 45, 1240, 40, 260)
        p.counter(b - 75, 1560, 65, 220);  p.chair(b - 105, 1670, 90)
        p.rect(m - 50, 1780, 100, 170, rx=6)                    # display table
        p.plant(a + 45, 2100)
        p.unit(m, 1420, f"محل {'١٢٣'[i]}", "38.4 m²", f"Shop {i+1}")
        p.room(a + 60, 1090, "حمام", None, 20)
        p.room(m + 60, 1090, "مستودع", "Store", 20)

    p.room(92, 1560, "ممر", "Corridor 1.30", 24)

    # ---- dimensions -------------------------------------------------------
    y = D + 130
    p.dim_h(0, W, y + 60, "10.70")
    p.dim_h(25, 160, y, "1.30");  p.dim_h(175, 455, y, "2.80")
    p.dim_h(470, 750, y, "2.80"); p.dim_h(765, 1045, y, "2.80")
    x = W + 80
    p.dim_v(x + 60, 0, D, "21.50")
    p.dim_v(x, 0, 430, "4.30");  p.dim_v(x, 455, 950, "4.95");  p.dim_v(x, 970, D, "11.80")
    return p


def typical():
    p = Plan()

    # ---- envelope: built part 17.20 m deep, terrace on the rear 4.30 m ------
    p.vwall(0, 430, D, OW)
    p.vwall(W - OW, 430, D, OW)
    p.hwall(0, W, 430, 25)
    # terrace parapet on the plot boundary
    p.vwall(0, 0, 430, 8); p.vwall(W - 8, 0, 430, 8); p.hwall(0, W, 0, 8)
    p.hatch(8, 8, W - 8, 430, "terrace")
    p.void(25, 25, 530, 220)

    # stair, rear office, corridor, three street offices
    p.vwall(245, 455, 965, PW)
    p.hwall(245, 760, 965, PW)
    p.hwall(0, 760, 1100, PW)
    p.vwall(455, 1115, D, PW)
    p.vwall(750, 980, D, PW)

    # front wall with windows
    p.hwall(0, W, 2125, 25)
    for x0, x1 in ((60, 200), (280, 420), (500, 720), (795, 1015)):
        p.glass_h(x0, x1, 2125, 2150)
    # rear wall: windows and a terrace door for the rear office
    p.glass_h(300, 650, 430, 455)
    p.glass_h(830, 1000, 430, 455)
    p.door_h(700, 430, 455, 100, "l", "u")

    # ---- stair --------------------------------------------------------------
    p.stair(25, 455, 220, 510)
    p.room(135, 920, "درج", "Stair", 24)
    p.room(390, 1052, "ممر", "Corridor 1.20", 22)

    # ---- rear office (45 m2) --------------------------------------------
    p.door_v(245, 260, 860, 90, "b", "r")
    p.glass_partition_v(570, 455, 730); p.glass_partition_h(260, 570, 730)
    p.door_h(280, 727, 733, 90, "l", "d")
    p.table(415, 615, 220, 100, 3, 3)
    p.vwall(890, 455, 620, IW); p.hwall(890, 1045, 620, IW)      # WC
    p.door_h(930, 620, 630, 80, "l", "u")
    p.toilet(1010, 500, 0);  p.basin(920, 590, 270)
    p.vwall(730, 455, 620, IW); p.hwall(730, 890, 620, IW)       # pantry
    p.door_h(760, 620, 630, 80, "l", "u")
    p.counter(745, 460, 140, 55)
    p.desk(600, 660, 140, 70, "t"); p.desk(760, 660, 140, 70, "t")
    p.desk(600, 750, 140, 70, "b"); p.desk(760, 750, 140, 70, "b")
    p.desk(380, 790, 160, 70, "t"); p.chair(420, 895, 0); p.chair(500, 895, 0)
    p.plant(1010, 930)
    p.unit(920, 880, "مكتب خلفي", "45 m²", "Rear office")
    p.room(415, 488, "اجتماعات", "Meeting", 22)
    p.room(970, 560, "حمام", None, 20)
    p.room(810, 585, "مطبخ", "Pantry", 20)
    p.room(790, 330, "تراس", "Terrace", 26)
    p.room(280, 120, "منور", "Void · lightwell", 24)

    # ---- office A (48 m2, 4.30 wide) --------------------------------------
    p.door_h(60, 1100, 1115, 90, "l", "d")
    p.vwall(295, 1115, 1270, IW); p.hwall(295, 455, 1270, IW)   # WC
    p.door_h(330, 1270, 1280, 80, "l", "u")
    p.toilet(410, 1160, 0); p.basin(340, 1250, 270)
    p.counter(120, 1190, 170, 60); p.chair(205, 1290, 0)
    p.desk(60, 1350, 140, 70, "t");  p.desk(230, 1350, 140, 70, "t")
    p.desk(60, 1440, 140, 70, "b");  p.desk(230, 1440, 140, 70, "b")
    p.table(200, 1650, 200, 100, 3, 3)
    p.hwall(25, 455, 1790, IW)
    p.door_h(60, 1790, 1800, 90, "l", "d")
    p.desk(200, 1950, 160, 80, "b"); p.chair(240, 1905, 180); p.chair(320, 1905, 180)
    p.sofa(390, 1830, 60, 180, "r")
    p.shelf(30, 1820, 40, 220)
    p.plant(420, 2090)
    p.unit(240, 1560, "مكتب أ", "48 m²", "Office A")
    p.room(200, 1870, "مدير", "Manager", 22)
    p.room(375, 1200, "حمام", None, 20)

    # ---- office B (34 m2, 2.80 wide) --------------------------------------
    p.door_h(500, 1100, 1115, 90, "l", "d")
    p.vwall(630, 1115, 1250, IW); p.hwall(630, 750, 1250, IW)   # WC
    p.door_h(655, 1250, 1260, 80, "l", "u")
    p.toilet(705, 1160, 0); p.basin(670, 1235, 270)
    for yy in (1330, 1500, 1670):
        p.desk(480, yy, 70, 140, "r")
    p.shelf(705, 1300, 40, 420)
    p.table(610, 1980, 130, 90, 2, 2)
    p.plant(720, 1830)
    p.unit(610, 1440, "مكتب ب", "34 m²", "Office B")
    p.room(690, 1200, "حمام", None, 20)

    # ---- office C (38 m2, 2.80 wide, longer) ------------------------------
    p.door_v(750, 765, 985, 90, "t", "r")
    p.vwall(925, 980, 1120, IW); p.hwall(925, 1045, 1120, IW)   # WC
    p.door_h(955, 1120, 1130, 80, "l", "u")
    p.toilet(1000, 1025, 0); p.basin(965, 1105, 270)
    for yy in (1200, 1370, 1540):
        p.desk(965, yy, 70, 140, "l")
    p.shelf(770, 1180, 40, 420)
    p.table(905, 1980, 130, 90, 2, 2)
    p.plant(1015, 1830)
    p.unit(905, 1440, "مكتب ج", "38 m²", "Office C")
    p.room(985, 1060, "حمام", None, 20)

    # ---- dimensions -------------------------------------------------------
    y = D + 130
    p.dim_h(0, W, y + 60, "10.70")
    p.dim_h(25, 455, y, "4.30"); p.dim_h(470, 750, y, "2.80"); p.dim_h(765, 1045, y, "2.80")
    x = W + 80
    p.dim_v(x + 60, 0, D, "21.50")
    p.dim_v(x, 0, 430, "4.30"); p.dim_v(x, 455, 965, "5.10")
    p.dim_v(x, 980, 1100, "1.20"); p.dim_v(x, 1115, D, "10.35")
    return p


def export_png(svg_path, png_path, scale=1.5):
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if not os.path.exists(chrome):
        print("Chrome not found; skipping PNG export"); return
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", "--window-size=1420,2400",
                    f"--screenshot={png_path}", "file://" + os.path.abspath(svg_path)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("wrote", png_path)


if __name__ == "__main__":
    for name, fn, title in (("plan-ground", ground, "Option 2 — ground floor"),
                            ("plan-typical", typical, "Option 2 — typical upper floor")):
        path = os.path.join(HERE, name + ".svg")
        with open(path, "w") as f:
            f.write(fn().svg(title))
        print("wrote", path)
        if "--png" in sys.argv:
            export_png(path, os.path.join(HERE, name + ".png"))
