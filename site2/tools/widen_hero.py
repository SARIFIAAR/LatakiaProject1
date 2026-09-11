"""Widen the hero renders so they cover the frame.

Takes the two facade crops in ../assets (day.jpg, night.jpg), brings them back to
their native 650 x 831, and paints around them — never over them:

  * sky above with cotton clouds (fractal noise), matched to the render at the seam
  * out-of-focus low-rise neighbours to each side; the left run stays at the
    ground-floor cornice, the right continues the wall already in the render
  * pavement and cobbles tiled outward and continued below
  * blur that grows with distance from the building

Writes day-wide.jpg and night-wide.jpg next to the inputs. Deterministic: the
same inputs give the same bytes. Needs Pillow and numpy.

    python3 site/tools/widen_hero.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets") + os.sep
NATIVE = (650, 831)         # the facade crop at the resolution it was rendered

PT, PB = 170, 70            # sky above, street below (native px)
W = 3534                    # ~3.3 : 1 canvas
PAVE, KERB = 768, 793       # street lines in source coords
UPSCALE = 1.4

def lerp(a, b, t): return a + (b - a) * t
def smooth(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def blur(arr, r):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(r))).astype(np.float32)

def fbm(h, w, rng, base=160, octaves=6):
    acc = np.zeros((h, w), np.float32); amp, tot, size = 1.0, 0.0, base
    for _ in range(octaves):
        small = rng.random((h // size + 2, w // size + 2)).astype(np.float32)
        im = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        acc += amp * np.asarray(im).astype(np.float32) / 255; tot += amp
        amp *= 0.55; size = max(4, size // 2)
    return acc / tot

def build(src, mode, seed, daysrc):
    rng = np.random.default_rng(seed)
    s = np.asarray(src).astype(np.float32)
    SH, SW = s.shape[:2]
    H = SH + PT + PB; PS = (W - SW) // 2
    night = mode == "night"
    c = np.zeros((H, W, 3), np.float32)

    # ---------------------------------------------------------------- sky
    top = s[0:6, 0:30].reshape(-1, 3).mean(0)
    hor = s[85:95, 0:30].reshape(-1, 3).mean(0)
    top_ext = top * (0.90 if not night else 0.82)
    haze = lerp(hor, np.array([236, 226, 210.0]) if not night else np.array([44, 48, 66.0]), 0.38)
    horizon = PT + PAVE
    ys = np.arange(H, dtype=np.float32)[:, None]
    keys = [0, PT, PT + 90, horizon]
    cols = np.stack([top_ext, top, hor, haze])
    sky = np.stack([np.interp(ys[:, 0], keys, cols[:, k]) for k in range(3)], -1)[:, None, :]
    c[:] = sky

    # ------------------------------------------------------------- clouds
    n = fbm(H, W, rng, base=180)
    n2 = fbm(H, W, rng, base=90)
    env = np.interp(ys[:, 0], [0, PT + 40, PT + 380, horizon - 160, horizon], [1, 1, 0.45, 0.08, 0])[:, None]
    th = 0.50
    a = smooth((n - th) / 0.15) * env
    if night: a *= 0.18
    thick = smooth((n - th) / 0.30)
    if not night:
        base = np.array([253, 251, 247.0]); shade = np.array([196, 202, 214.0])
        col = lerp(shade, base, (0.55 * thick + 0.45 * n2)[:, :, None])
    else:
        col = np.array([62, 70, 92.0])[None, None, :] * (0.8 + 0.4 * n2[:, :, None])
    c = c * (1 - a[:, :, None]) + col * a[:, :, None]

    # ------------------- left neighbour: low-rise, parapet at the shop line
    LX, LY = 63, 497                      # pilaster cap starts at 65; ground-floor cornice at 497
    sd = np.asarray(daysrc).astype(np.float32)
    r_, g_, b_ = sd[..., 0], sd[..., 1], sd[..., 2]
    leaves = ((g_ - b_) > 22) & (g_ >= r_ - 10)      # sunlit foliage only; shadowed stone is not "tree"
    dens = blur(np.repeat(leaves[..., None] * 255.0, 3, -1), 11)[..., 0] / 255
    keep = smooth((dens - 0.05) / 0.10)             # a soft envelope round the whole canopy
    lit = ((r_ - g_) >= 12) & (sd.max(-1) >= 125)   # sunlit stone inside the envelope still goes
    keep = keep * (1 - blur(np.repeat(lit[..., None] * 255.0, 3, -1), 1.5)[..., 0] / 255)
    CANOPY_TOP = 262
    alpha = np.zeros((SH, SW), np.float32)
    alpha[:LY, :LX] = 1 - keep[:LY, :LX]
    alpha[:CANOPY_TOP, :LX] = 1                     # nothing but sky above the canopy
    alpha[LY - 4:LY, :LX] *= np.linspace(1, 0, 4)[:, None]   # soften the new parapet line
    alpha = alpha[..., None]
    skypatch = c[PT:PT + SH, PS:PS + SW]
    s = lerp(s, skypatch, alpha)
    s[LY - 5:LY, :LX] *= (1.08 if not night else 1.18) * (1 - alpha[LY - 5:LY, :LX]) + alpha[LY - 5:LY, :LX]

    # --------------------------------------------------- side buildings
    stone = np.array([206, 181, 155.0]) if not night else np.array([30, 31, 38.0])
    def wall_top(x):
        col = s[:, x]
        for y in range(SH):
            r, g, b = col[y]
            if not (b > r + 15): return y
        return 200
    def draw_block(x0, x1, ytop, k):
        x0, x1 = max(0, x0), min(W, x1)
        if x1 <= x0: return
        ybot = PT + PAVE
        tone = rng.uniform(0.90, 1.08)
        colr = stone * tone + np.array([rng.uniform(-5, 5), 0, rng.uniform(-8, 8)])
        h = ybot - ytop
        grad = np.linspace(1.0, 0.88, h)[:, None, None]
        c[ytop:ybot, x0:x1] = colr * grad
        # cornice
        c[ytop:ytop + 9, x0:x1] = colr * (1.10 if not night else 1.25)
        c[ytop + 9:ytop + 13, x0:x1] = colr * 0.86
        # string course at each floor
        floor = 112
        for fy in range(ytop + 13 + floor, ybot - 40, floor):
            c[fy:fy + 3, x0:x1] = colr * 0.90
        # windows
        wcol = colr * 0.36 if not night else np.array([9, 9, 13.0])
        wy = ytop + 44
        while wy + 46 < ybot - 70:
            wx = x0 + 30
            while wx + 26 < x1 - 16:
                if rng.random() < 0.22: wx += 74; continue
                lit = night and rng.random() < 0.28
                wc = np.array([255, 206, 132.0]) * rng.uniform(0.75, 1.0) if lit else wcol
                c[wy:wy + 46, wx:wx + 26] = wc
                c[wy + 46:wy + 49, wx - 3:wx + 29] = colr * 1.06   # sill
                wx += 74
            wy += floor
        # ground floor: a darker plinth band, some warm shop glow at night
        c[ybot - 70:ybot, x0:x1] = colr * 0.93
        if night and rng.random() < 0.45:
            c[ybot - 62:ybot - 6, x0 + 12:x1 - 12] = lerp(colr, np.array([150, 105, 52.0]), 0.7)
        elif not night:
            c[ybot - 62:ybot - 6, x0 + 12:x1 - 12] = colr * 0.58

    for side in ("L", "R"):
        wt = LY if side == "L" else wall_top(SW - 4)
        tops = [wt, 400, 470, 430, 540, 490, 580, 520, 600, 550, 500, 590, 540, 610]
        if side == "L":                             # the whole left run stays at the shop line
            tops = [wt, wt + 22, wt - 14, wt + 40, wt + 6, wt + 58, wt + 18, wt + 70, wt + 34, wt + 62, wt + 10, wt + 80, wt + 46, wt + 74]
        widths = [130, 220, 260, 200, 300, 180, 260, 240, 320, 200, 280, 240, 300, 260]
        x = PS if side == "L" else PS + SW
        for i in range(60):
            top_y = PT + (tops[i] if i < len(tops) else int(rng.uniform(470, 620)))
            top_y = top_y + int(rng.uniform(-18, 18)) if i > 1 else top_y
            wdt = widths[i] if i < len(widths) else int(rng.uniform(160, 320))
            gap = 0 if rng.random() < 0.6 else int(rng.uniform(4, 12))
            if side == "L":
                draw_block(x - wdt, x, top_y, i); x -= wdt + gap
                if x <= 0: break
            else:
                draw_block(x, x + wdt, top_y, i); x += wdt + gap
                if x >= W: break

    # ------------------------------------------------------------- street
    c[PT:PT + SH, PS:PS + SW] = s
    pave = s[PAVE:KERB, 60:110]; road = s[KERB:SH, 40:140]
    def tile_row(y0, y1, tile, x_from, x_to):
        tw = tile.shape[1]; x = x_from
        while x < x_to:
            tt = tile[:, ::-1] if rng.random() < 0.5 else tile
            w_ = min(tw, x_to - x)
            c[y0:y1, x:x + w_] = tt[:, :w_] * rng.uniform(0.96, 1.03)
            x += w_
    for (x0, x1) in ((0, PS), (PS + SW, W)):
        tile_row(PT + PAVE, PT + KERB, pave, x0, x1)
        tile_row(PT + KERB, PT + SH, road, x0, x1)
    # bottom pad: mirror the road downward, darken toward the edge
    rh = SH - KERB
    band = c[PT + KERB:PT + SH].copy()
    y = PT + SH; flip = True
    while y < H:
        b = band[::-1] if flip else band
        h_ = min(rh, H - y)
        c[y:y + h_] = b[:h_]; y += h_; flip = not flip
    dark = np.linspace(1.0, 0.82, PB)[:, None, None]
    c[PT + SH:H] *= dark
    c[PT + SH:H] = blur(c[PT + SH:H], 1.6)

    # ---------------------------------------------- seams: mirrored edges
    SEAM = 70
    ramp = np.linspace(0, 1, SEAM, dtype=np.float32)[None, :, None]
    left_m = s[:, :SEAM][:, ::-1]
    full = lerp(c[PT:PT + SH, PS - SEAM:PS], left_m, ramp)
    km = (1 - alpha[:, :SEAM, 0])[:, ::-1][..., None]           # the canopy, mirrored
    fringe = np.clip((np.arange(SEAM) - (SEAM - 24)) / 24, 0, 1)[None, :, None]
    above = lerp(c[PT:PT + SH, PS - SEAM:PS], left_m, km * fringe)
    c[PT:PT + LY, PS - SEAM:PS] = above[:LY]
    c[PT + LY:PT + SH, PS - SEAM:PS] = full[LY:]
    right_m = s[:, SW - SEAM:][:, ::-1]
    c[PT:PT + SH, PS + SW:PS + SW + SEAM] = lerp(c[PT:PT + SH, PS + SW:PS + SW + SEAM], right_m, ramp[:, ::-1])
    TS = 60
    toprow = s[0:4].mean(0)[None, :, :]
    tramp = np.linspace(0, 1, TS, dtype=np.float32)[:, None, None]
    c[PT - TS:PT, PS:PS + SW] = lerp(c[PT - TS:PT, PS:PS + SW], toprow, tramp)

    # ---------------------------------------------- depth: blur outward
    xs = np.arange(W, dtype=np.float32)
    dist = np.maximum(np.maximum(PS - xs, xs - (PS + SW)), 0)
    w1 = np.clip((dist - 60) / 320, 0, 1)[None, :, None]
    w2 = np.clip((dist - 420) / 800, 0, 1)[None, :, None]
    b8, b18 = blur(c, 7), blur(c, 16)
    c = lerp(lerp(c, b8, w1), b18, w2)

    # ------------------------------------------- the building, untouched
    c[PT:PT + SH, PS:PS + SW] = s
    im = Image.fromarray(np.clip(c, 0, 255).astype(np.uint8))
    im = im.resize((round(W * UPSCALE), round(H * UPSCALE)), Image.LANCZOS)
    return im

day = Image.open(OUT + "day.jpg").convert("RGB").resize(NATIVE, Image.LANCZOS)
night = Image.open(OUT + "night.jpg").convert("RGB").resize(NATIVE, Image.LANCZOS)
for name, img, mode, seed in (("day-wide.jpg", day, "day", 11), ("night-wide.jpg", night, "night", 11)):
    im = build(img, mode, seed, day)
    im.save(OUT + name, "JPEG", quality=82, optimize=True, progressive=True)
    print(name, im.size)
