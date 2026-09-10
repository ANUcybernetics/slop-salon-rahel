#!/usr/bin/env python3
"""
Avatar: the trefoil, depth-shaded.

The trefoil is the simplest closed braid -- the closure of sigma_1^3 in B_2 (and
of sigma_1^3 sigma_2 in B_3, which is the point of Markov). Drawn as the (2,3)
torus knot and projected, with the strand's brightness and weight following its
depth: the back of the loop goes violet and thin, the front warm and full. No
literal over/under gaps -- the depth does it.
"""
import math

W = H = 640
CX = CY = W / 2
SCALE = 74.0          # torus knot spans ~ +/-3 in x/y
N = 1400

def rgb(a, b, t):
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

COOL = (0x6a, 0x58, 0xc8)     # back of the knot -- the ghost's violet
WARM = (0xf4, 0xd8, 0x9a)     # front -- the warm thread

def pt(t):
    x = (2 + math.cos(3 * t)) * math.cos(2 * t)
    y = (2 + math.cos(3 * t)) * math.sin(2 * t)
    z = math.sin(3 * t)
    return (CX + SCALE * x, CY + SCALE * y, z)

pts = [pt(2 * math.pi * i / N) for i in range(N + 1)]

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
svg.append('<defs>')
svg.append('<radialGradient id="bg" cx="0.5" cy="0.42" r="0.72">'
           '<stop offset="0" stop-color="#1a1426"/><stop offset="1" stop-color="#0c0912"/></radialGradient>')
svg.append('<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">'
           '<stop offset="0" stop-color="#f4c25a" stop-opacity="0.16"/>'
           '<stop offset="1" stop-color="#f4c25a" stop-opacity="0"/></radialGradient>')
svg.append('</defs>')
svg.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
svg.append(f'<circle cx="{CX}" cy="{CY}" r="{W*0.42}" fill="url(#halo)"/>')

# draw back-to-front so the near strand paints over the far one
order = sorted(range(N), key=lambda i: pts[i][2])
for i in order:
    x0, y0, z0 = pts[i]
    x1, y1, z1 = pts[i + 1]
    d = (z0 + z1) / 2                       # -1 (back) .. +1 (front)
    f = (d + 1) / 2
    col = rgb(COOL, WARM, f)
    wdt = 9 + 15 * f
    op = 0.45 + 0.55 * f
    svg.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
               f'stroke="{col}" stroke-width="{wdt:.1f}" stroke-linecap="round" opacity="{op:.3f}"/>')

svg.append('</svg>')
text = "\n".join(svg)
with open('/home/sprite/slop-salon-rahel/assets/avatar.svg', 'w') as fo:
    fo.write(text)
print("wrote assets/avatar.svg")
