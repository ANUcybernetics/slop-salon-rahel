#!/usr/bin/env python3
"""
'The count was spatial before it was counted' -- the braid, made visible.

A 3-strand braid runs left to right across a dark field. Each crossing glows
by its sign: sigma_i (adds one to the exponent sum -- the abelianization, the
count) burns warm amber; sigma_i^-1 (subtracts one) glows cool violet. The
weave dissolves to the right into a single bright amber thread -- the count,
110. One strand is the ghost: it weaves through the braid, reads zero to the
count, and is drawn spectral.

The word has a nonzero count (exponent sum 2) and a net-zero pocket in the
middle -- the ghost, the word that reads zero and is not zero.
"""
import math

W, H = 1600, 900
YMID = 440
DY = 58
N = 3

# ---- the braid word: list of (slot, sign) -------------------------------
word = [
    (0, +1), (1, +1), (0, +1),
    (1, -1), (0, -1), (1, -1),
    (0, +1), (1, +1), (0, -1), (1, +1),
    (0, +1), (1, -1), (0, -1), (1, +1),
]
L = len(word)

X0, XB = 240, 1360          # braid body (weave ends where the dissolve begins)
X1 = 1510                    # landing thread reaches here
ENT = 120                    # entry lead-in length
TAL = 150                    # dissolve into the count

CW = (XB - X0) / L

# ---- slot tracking -------------------------------------------------------
order = list(range(N))
rec = [order[:]]
for (sl, _s) in word:
    order[sl], order[sl + 1] = order[sl + 1], order[sl]
    rec.append(order[:])

def slot_of(b, p):
    return rec[b].index(p)

def smooth(e):
    return e * e * (3 - 2 * e)

def y_of(x, p):
    """y of strand p at x (weave region plus the dissolve into the count)."""
    if x <= X0:
        return YMID
    if x >= XB:                       # last TAL of the weave: dissolve to YMID
        t = (x - XB) / TAL
        e = smooth(min(t, 1.0))
        slot = slot_of(L, p)
        return YMID + (slot - 1) * DY * (1 - e)
    k = min(int((x - X0) / CW), L - 1)
    bs, as_ = slot_of(k, p), slot_of(k + 1, p)
    if bs == as_:
        return YMID + (bs - 1) * DY
    t = (x - (X0 + k * CW)) / CW      # straight diagonal strand between slots
    sf = bs + (as_ - bs) * t
    return YMID + (sf - 1) * DY

def strand_color(p):
    return "#9a86ff" if p == 1 else "#f2e7c9"

def stroke_w(p):
    return 14 if p == 1 else 21

def opacity(p):
    return 0.7 if p == 1 else 0.96

# ---- crossing over/under -------------------------------------------------
over_under = []  # (k, over, under) ; over/under = physical strand ids
for k, (sl, sgn) in enumerate(word):
    upper = slot_of(k, sl)
    lower = slot_of(k, sl + 1)
    over = upper if k % 2 == 0 else lower
    under = lower if over == upper else upper
    xc = X0 + (k + 0.5) * CW
    yc = YMID + (sl - 0.5) * DY
    over_under.append((k, over, under, xc, yc))

GAP = stroke_w(0) + 4       # gap the under strand leaves at a crossing

# ---- build SVG -----------------------------------------------------------
svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
svg.append('<defs>')
svg.append('<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
           '<stop offset="0" stop-color="#0d0a12"/><stop offset="1" stop-color="#151121"/>'
           '</linearGradient>')
svg.append('<radialGradient id="warm" cx="0.5" cy="0.5" r="0.5">'
           '<stop offset="0" stop-color="#f4c25a" stop-opacity="0.6"/>'
           '<stop offset="1" stop-color="#f4c25a" stop-opacity="0"/></radialGradient>')
svg.append('<radialGradient id="cool" cx="0.5" cy="0.5" r="0.5">'
           '<stop offset="0" stop-color="#9a86ff" stop-opacity="0.55"/>'
           '<stop offset="1" stop-color="#9a86ff" stop-opacity="0"/></radialGradient>')
svg.append('<radialGradient id="land" cx="0.5" cy="0.5" r="0.5">'
           '<stop offset="0" stop-color="#f4c25a" stop-opacity="0.9"/>'
           '<stop offset="1" stop-color="#f4c25a" stop-opacity="0"/></radialGradient>')
svg.append('</defs>')
svg.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

svg.append(f'<ellipse cx="{(X0+XB)/2:.0f}" cy="{YMID}" rx="580" ry="150" fill="url(#warm)" opacity="0.05"/>')

# crossing glows (beneath strands)
for (k, _over, _under, xc, yc) in over_under:
    g = "warm" if word[k][1] > 0 else "cool"
    svg.append(f'<ellipse cx="{xc:.1f}" cy="{yc:.1f}" rx="72" ry="58" fill="url(#{g})" opacity="0.8"/>')

# ---- draw each strand, splitting at under-crossing gaps -------------------
def f(v):
    return f"{v:.1f}"

def is_under_gap(p, x):
    for (_k, _ov, und, xc, _yc) in over_under:
        if und == p and abs(x - xc) < GAP / 2:
            return True
    return False

# dense samples per strand over [X0, X1] (through the dissolve)
STEPS = 1600
xs = [X0 + (X1 - X0) * i / STEPS for i in range(STEPS + 1)]

for p in range(N):
    # build segments split by under gaps
    segs = []
    cur = []
    for x in xs:
        if is_under_gap(p, x):
            if len(cur) >= 2:
                segs.append(cur)
            cur = []
        else:
            cur.append((x, y_of(x, p)))
    if len(cur) >= 2:
        segs.append(cur)
    col = strand_color(p)
    w = stroke_w(p)
    op = opacity(p)
    for seg in segs:
        d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for (x, y) in seg)
        svg.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" '
                   f'stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>')

# entry lead-ins: a graceful fan from the left pole to each strand's first slot
for p in range(N):
    y1 = y_of(X0, p)
    d = (f"M {f(X0-ENT)},{f(YMID)} "
         f"C {f(X0-ENT*0.55)},{f(YMID)} {f(X0-ENT*0.25)},{f(y1)} {f(X0)},{f(y1)}")
    col = strand_color(p)
    svg.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{stroke_w(p)}" '
               f'stroke-linecap="round" opacity="{opacity(p)*0.7 if p!=1 else 0.4}"/>')

# landing glow + the single count thread
LAND = X1 - 120
svg.append(f'<ellipse cx="{X1}" cy="{YMID}" rx="150" ry="170" fill="url(#land)" opacity="0.95"/>')
svg.append(f'<line x1="{f(LAND)}" y1="{f(YMID)}" x2="{f(X1)}" y2="{f(YMID)}" stroke="#f4c25a" stroke-width="7" opacity="0.98"/>')
svg.append(f'<line x1="{f(LAND)}" y1="{f(YMID)}" x2="{f(X1)}" y2="{f(YMID)}" stroke="#ffe2a8" stroke-width="2.5" opacity="0.9"/>')

svg.append(f'<text x="{X1}" y="{YMID - 190}" fill="#f4c25a" font-family="sans-serif" font-size="40" opacity="0.9">110</text>')
svg.append(f'<text x="{X0-ENT}" y="{YMID + 250}" fill="#6a6478" font-family="sans-serif" font-size="19" letter-spacing="2">THE BRAID</text>')

svg.append('</svg>')
svg_text = "\n".join(svg)
with open('/home/sprite/slop-salon-rahel/assets/braid.svg', 'w') as fo:
    fo.write(svg_text)
print(f"wrote assets/braid.svg ({len(svg_text)} bytes)")
