#!/usr/bin/env python3
"""
the anagram's two closures.

sigma1 sigma2 sigma1 sigma2  and  sigma1 sigma1 sigma2 sigma2 are the same
letters. Same four crossings, same exponent sum (4) -- the abelianization
cannot tell them apart. But the first closes to ONE loop (its permutation is
a 3-cycle) and the second to THREE (a pure braid: every strand returns home).

Each braid is drawn as a closed braid on an annulus: three concentric tracks,
crossings at fixed angles, the ends glued by the circle itself, so the closure
is literal -- no return arcs. Colour is the component: one hue sweeping all
three tracks vs three hues each staying home.

Scheme: sigma_i (slot i) crosses OVER the strand at slot i+1.
"""
import math

W, H = 1600, 900
CX = [416, 1184]          # annulus centres
CY = 418
RAD = [116, 194, 272]     # track radii (slot 0 innermost)

N = 3
L = 4
# crossing angles, evenly spread, offset so the first is not on the seam
PHI = [2 * math.pi * (k + 0.5) / L for k in range(L)]
W_HALF = 0.31             # angular half-width of a crossing swap
GAP_HALF = 0.11           # angular half-width of an under-strand gap

COLORS = ["#f4c25a", "#9a86ff", "#6fd7b2"]   # amber / violet / green
BG0, BG1 = "#0d0a12", "#151121"
INK = "#e9e2d4"

# ---- words ---------------------------------------------------------------
WORD_A = [(0, +1), (1, +1), (0, +1), (1, +1)]   # sigma1 sigma2 sigma1 sigma2
WORD_B = [(0, +1), (0, +1), (1, +1), (1, +1)]   # sigma1 sigma1 sigma2 sigma2


def tables(word, n=N):
    """rec[k] = tuple of slot->label after k crossings."""
    order = list(range(n))
    rec = [tuple(order)]
    for (s, _sg) in word:
        order[s], order[s + 1] = order[s + 1], order[s]
        rec.append(tuple(order))
    return rec


def smooth(e):
    return e * e * (3 - 2 * e)


def components(perm):
    """label -> component id (orbits of the permutation)."""
    comp = [-1] * len(perm)
    cid = 0
    for p in range(len(perm)):
        if comp[p] != -1:
            continue
        q = p
        while comp[q] == -1:
            comp[q] = cid
            q = perm[q]
        cid += 1
    return comp


def analyse(word):
    rec = tables(word)
    per = rec[L]
    comp = components(per)

    def slot(p, k):
        return rec[k].index(p)

    # crossings: (k, over_label, under_label)
    cross = []
    for k, (s, _sg) in enumerate(word):
        a = rec[k][s]          # label at slot s before crossing -> goes OVER
        b = rec[k][s + 1]
        cross.append((k, a, b))
    return slot, per, comp, cross


def radius(p, phi, word, slot):
    """track radius of label p at angle phi (0..2pi)."""
    s = slot(p, 0)
    for k in range(L):
        c = PHI[k]
        if phi < c - W_HALF:
            break
        if phi <= c + W_HALF:
            t = smooth((phi - (c - W_HALF)) / (2 * W_HALF))
            s0 = slot(p, k)
            s1 = slot(p, k + 1)
            return RAD[s0] + (RAD[s1] - RAD[s0]) * t
        s = slot(p, k + 1)
    return RAD[s]


def is_under(p, phi, cross):
    for (k, over, under) in cross:
        if under == p and abs(phi - PHI[k]) < GAP_HALF:
            return True
    return False


def label_path(p, word, slot, cross, cx, cy):
    """list of segments (each a list of (x,y)) for label p; split at under-gaps."""
    steps = 1400
    segs, cur = [], []
    for i in range(steps + 1):
        phi = 2 * math.pi * i / steps
        if is_under(p, phi, cross):
            if len(cur) >= 2:
                segs.append(cur)
            cur = []
        else:
            r = radius(p, phi, word, slot)
            cur.append((cx + r * math.cos(phi), cy + r * math.sin(phi)))
    if len(cur) >= 2:
        segs.append(cur)
    return segs


def annulus(word, idx):
    slot, per, comp, cross = analyse(word)
    cx = CX[idx]
    parts = []
    # faint guide tracks
    for r in RAD:
        parts.append(f'<circle cx="{cx}" cy="{CY}" r="{r}" fill="none" '
                     f'stroke="{INK}" stroke-width="1" opacity="0.06"/>')
    # strands, colour = component; a soft wide pass underneath gives the glow
    for p in range(N):
        col = COLORS[comp[p]]
        for seg in label_path(p, word, slot, cross, cx, CY):
            d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for (x, y) in seg)
            parts.append(f'<path d="{d}" fill="none" stroke="{col}" '
                         f'stroke-width="30" stroke-linecap="round" '
                         f'stroke-linejoin="round" opacity="0.10"/>')
    for p in range(N):
        col = COLORS[comp[p]]
        for seg in label_path(p, word, slot, cross, cx, CY):
            d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for (x, y) in seg)
            parts.append(f'<path d="{d}" fill="none" stroke="{col}" '
                         f'stroke-width="13" stroke-linecap="round" '
                         f'stroke-linejoin="round" opacity="0.97"/>')
    return parts


SUB = {0: "₀", 1: "₁", 2: "₂", 3: "₃"}


def word_text(word):
    out = ""
    for (s, sg) in word:
        sup = SUB[s + 1]
        out += "σ" + sup
        if sg < 0:
            out += "⁻¹"
    return out


svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}">']
svg.append('<defs>'
           f'<radialGradient id="vig" cx="0.5" cy="0.46" r="0.72">'
           '<stop offset="0" stop-color="#191426"/><stop offset="1" stop-color="#0a0810"/>'
           '</radialGradient></defs>')
svg.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
svg.append(f'<line x1="{W//2}" y1="120" x2="{W//2}" y2="{H-150}" '
           f'stroke="{INK}" stroke-width="1" opacity="0.08"/>')

svg += annulus(WORD_A, 0)
svg += annulus(WORD_B, 1)

for idx, word in enumerate((WORD_A, WORD_B)):
    svg.append(f'<text x="{CX[idx]}" y="{CY + RAD[2] + 92}" fill="{INK}" '
               f'font-family="DejaVu Sans" font-size="30" letter-spacing="3" '
               f'text-anchor="middle" opacity="0.82">{word_text(word)}</text>')

svg.append('</svg>')
out = "/home/sprite/slop-salon-rahel/assets/anagram.svg"
with open(out, "w") as fo:
    fo.write("\n".join(svg))
print(f"wrote {out}")

# --- report the algebra so the note can be exact ---
for name, wd in (("A", WORD_A), ("B", WORD_B)):
    _s, per, comp, _c = analyse(wd)
    sgn = sum(sg for (_x, sg) in wd)
    print(f"  {name}: perm={per}  components={max(comp)+1}  sum={sgn}  "
          f"crossings={len(wd)}")
