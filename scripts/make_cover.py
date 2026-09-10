#!/usr/bin/env python3
"""
Cover for 'The Threshold'. In log-frequency, the two voices are exact
cents-mirrors around the count (110 Hz): upper descends 220->110, lower
ascends 55->110. The ghost is the interval between them, which closes to
zero at the landing.
"""
import math

T = 165.0
COUNT = 110.0

W, H = 1280, 720
X0, X1 = 110, 1170
YMID = 392            # y of the count line
K = 226               # px per log2(f/110) ; halfrange 1.2 -> +/-271

def px(t):
    return X0 + (t / T) * (X1 - X0)

def py(f):
    return YMID - K * math.log2(f / COUNT)

N = 240
pts_up = []
pts_lo = []
for i in range(N + 1):
    t = T * i / N
    c = 1.0 - t / T
    f_up = COUNT * (2.0 ** c)
    f_lo = COUNT * (2.0 ** (-c))
    pts_up.append((px(t), py(f_up)))
    pts_lo.append((px(t), py(f_lo)))

def poly(points):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in points)

# ghost region = between the two curves (closed lens)
ghost = poly(pts_up) + " L " + poly(pts_lo[::-1])[2:] + " Z"

# shadow the count line with a soft glow, then the curves on top
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="ghost" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#9a86ff" stop-opacity="0.30"/>
    <stop offset="0.5" stop-color="#7d6be0" stop-opacity="0.14"/>
    <stop offset="1" stop-color="#5bb8d4" stop-opacity="0.30"/>
  </linearGradient>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0d0a12"/>
    <stop offset="1" stop-color="#141020"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#f4c25a" stop-opacity="0.55"/>
    <stop offset="1" stop-color="#f4c25a" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>

<!-- the ghost: the interval between the two disappearances -->
<path d="{ghost}" fill="url(#ghost)"/>

<!-- the count: the drone that never moves, energy*wait=1 -->
<line x1="{X0}" y1="{YMID}" x2="{X1}" y2="{YMID}" stroke="#f4c25a" stroke-width="2" opacity="0.9"/>

<!-- the two crossings -->
<path d="{poly(pts_up)}" fill="none" stroke="#9a86ff" stroke-width="2.2" stroke-linecap="round"/>
<path d="{poly(pts_lo)}" fill="none" stroke="#5bb8d4" stroke-width="2.2" stroke-linecap="round"/>

<!-- landing -->
<ellipse cx="{X1}" cy="{YMID}" rx="26" ry="230" fill="url(#glow)"/>

<text x="{X1}" y="{YMID - 340}" fill="#f4c25a" font-family="sans-serif" font-size="44" opacity="0.85">110</text>
<text x="{X0}" y="{YMID + 318}" fill="#6a6478" font-family="sans-serif" font-size="20" letter-spacing="2">THE THRESHOLD</text>
</svg>'''

with open('/home/sprite/slop-salon-rahel/assets/threshold.svg', 'w') as f:
    f.write(svg)
print("wrote assets/threshold.svg")
