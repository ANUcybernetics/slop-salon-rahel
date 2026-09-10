#!/usr/bin/env python3
"""
'closure spends the route and keeps the crossings' -- the loop, in motion.

A 3-strand braid runs across a dark field, free ends at both sides. Three arcs
reach from the right-hand ends, sweep below the weave, and sew shut onto the
left-hand ends. When the last arc lands, the braid is a single closed curve: a
travelling light runs the whole loop and finds no start. The crossing glows keep
their sign (warm = +, cool = -); the word is spent, the crossings stay.

The word's permutation is a 3-cycle, so the closure is ONE component -- one
unbroken loop, which is what lets a light run it whole without ever branching.
"""
import math, os, subprocess, shutil

W, H = 1600, 900
YMID = 345
DY = 58
N = 3
X0, XB = 300, 1300

word = [
    (0, +1), (1, +1), (0, +1),
    (1, -1), (0, -1), (1, -1),
    (0, +1), (1, +1), (0, -1), (1, +1),
    (0, +1), (1, -1), (0, -1), (1, +1),
]
L = len(word)
CW = (XB - X0) / L

# ---- slot tracking -------------------------------------------------------
order = list(range(N))
rec = [order[:]]
for (sl, _s) in word:
    order[sl], order[sl + 1] = order[sl + 1], order[sl]
    rec.append(order[:])

def slot_of(b, p):
    return rec[b].index(p)

def y_of(x, p):
    """y of strand p at x. No dissolve: free ends at both sides."""
    if x <= X0:
        return YMID + (slot_of(0, p) - 1) * DY
    if x >= XB:
        return YMID + (slot_of(L, p) - 1) * DY
    k = min(int((x - X0) / CW), L - 1)
    bs, as_ = slot_of(k, p), slot_of(k + 1, p)
    if bs == as_:
        return YMID + (bs - 1) * DY
    t = (x - (X0 + k * CW)) / CW
    return YMID + ((bs + (as_ - bs) * t) - 1) * DY

# ---- crossings (over/under) ----------------------------------------------
over_under = []
for k, (sl, sgn) in enumerate(word):
    upper = slot_of(k, sl)
    lower = slot_of(k, sl + 1)
    over = upper if k % 2 == 0 else lower
    under = lower if over == upper else upper
    xc = X0 + (k + 0.5) * CW
    yc = YMID + (sl - 0.5) * DY
    over_under.append((k, over, under, xc, yc, sgn))

STROKE_W = 21
GAP = STROKE_W + 4

def is_under_gap(p, x):
    for (_k, _ov, und, xc, _yc, _s) in over_under:
        if und == p and abs(x - xc) < GAP / 2:
            return True
    return False

# ---- arcs (the closure) ---------------------------------------------------
def arc_pts(i, M=160):
    """Cubic from right end (XB,y_i) sweeping below to left end (X0,y_i).

    Same R and D for every i, so arc_i is exactly arc_0 translated down by i*DY:
    the three closure arcs nest without ever crossing each other.
    """
    yi = YMID + (i - 1) * DY
    R = 170
    D = 330
    P0 = (XB, yi); P1 = (XB + R, yi + D); P2 = (X0 - R, yi + D); P3 = (X0, yi)
    pts = []
    for j in range(M + 1):
        t = j / M
        mt = 1 - t
        x = mt**3*P0[0] + 3*mt*mt*t*P1[0] + 3*mt*t*t*P2[0] + t**3*P3[0]
        y = mt**3*P0[1] + 3*mt*mt*t*P1[1] + 3*mt*t*t*P2[1] + t**3*P3[1]
        pts.append((x, y))
    return pts

ARCS = [arc_pts(i) for i in range(N)]

def poly_len(pts):
    s = 0.0
    for a, b in zip(pts, pts[1:]):
        s += math.hypot(b[0]-a[0], b[1]-a[1])
    return s

ARC_LEN = [poly_len(a) for a in ARCS]

def poly_d(pts):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for (x, y) in pts)

# ---- the single closed loop, for the travelling light ---------------------
def strand_pts(p, M=260):
    return [(X0 + (XB - X0) * j / M, y_of(X0 + (XB - X0) * j / M, p)) for j in range(M + 1)]

# follow the permutation: left position -> strand -> right position -> arc -> left
loop = []
pos = 0
for _ in range(N):
    p = rec[0][pos]                     # strand sitting at left position pos
    loop.extend(strand_pts(p, 200))     # left -> right
    i = slot_of(L, p)                   # its right position
    loop.extend(ARCS[i])                # arc right -> left (at position i)
    pos = i
LOOP_LEN = poly_len(loop)

def point_at(pts, s):
    """point at fraction s of arclength along pts"""
    total = poly_len(pts)
    target = s * total
    d = 0.0
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0]-a[0], b[1]-a[1])
        if d + seg >= target and seg > 0:
            t = (target - d) / seg
            return (a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t)
        d += seg
    return pts[-1]

def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))

# ---- one frame ------------------------------------------------------------
def frame_svg(u):
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    svg.append('<defs>')
    svg.append('<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
               '<stop offset="0" stop-color="#0d0a12"/><stop offset="1" stop-color="#151121"/></linearGradient>')
    svg.append('<radialGradient id="warm" cx="0.5" cy="0.5" r="0.5">'
               '<stop offset="0" stop-color="#f4c25a" stop-opacity="0.75"/>'
               '<stop offset="1" stop-color="#f4c25a" stop-opacity="0"/></radialGradient>')
    svg.append('<radialGradient id="cool" cx="0.5" cy="0.5" r="0.5">'
               '<stop offset="0" stop-color="#9a86ff" stop-opacity="0.7"/>'
               '<stop offset="1" stop-color="#9a86ff" stop-opacity="0"/></radialGradient>')
    svg.append('<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
               '<stop offset="0" stop-color="#fff3d0" stop-opacity="0.95"/>'
               '<stop offset="1" stop-color="#f4c25a" stop-opacity="0"/></radialGradient>')
    svg.append('</defs>')
    svg.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

    # phases
    p_braid = clamp(u / 0.10)                 # braid fades in
    p_close = clamp((u - 0.14) / 0.58)        # arcs sew shut
    p_light = clamp((u - 0.78) / 0.17)        # light runs the loop

    svg.append(f'<g opacity="{p_braid:.3f}">')
    svg.append(f'<ellipse cx="{(X0+XB)/2:.0f}" cy="{YMID+40:.0f}" rx="620" ry="200" fill="url(#warm)" opacity="0.06"/>')

    # crossing glows, gently breathing
    for (k, _over, _under, xc, yc, sgn) in over_under:
        g = "warm" if sgn > 0 else "cool"
        br = 0.55 + 0.22 * math.sin(2 * math.pi * (u * 2.0 + k * 0.13))
        svg.append(f'<ellipse cx="{xc:.1f}" cy="{yc:.1f}" rx="74" ry="60" fill="url(#{g})" opacity="{br:.3f}"/>')

    # strands
    xs = [X0 + (XB - X0) * j / 900 for j in range(901)]
    for p in range(N):
        segs = []; cur = []
        for x in xs:
            if is_under_gap(p, x):
                if len(cur) >= 2: segs.append(cur)
                cur = []
            else:
                cur.append((x, y_of(x, p)))
        if len(cur) >= 2: segs.append(cur)
        col = "#9a86ff" if p == 1 else "#f2e7c9"
        op = 0.72 if p == 1 else 0.96
        for seg in segs:
            svg.append(f'<path d="{poly_d(seg)}" fill="none" stroke="{col}" stroke-width="{STROKE_W}" '
                       f'stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>')
    # end caps (the loose ends) -- they vanish as the arcs take over
    cap_op = 0.95 * (1 - clamp(p_close * 1.6))
    if cap_op > 0.01:
        for p in range(N):
            for xe in (X0, XB):
                svg.append(f'<circle cx="{xe}" cy="{y_of(xe,p):.1f}" r="12.5" fill="#f2e7c9" opacity="{cap_op:.3f}"/>')
    svg.append('</g>')

    # the closing arcs: drawn from the right ends leftward, nested translates
    if p_close > 0:
        for i in range(N):
            off = ARC_LEN[i] * (1 - p_close)
            svg.append(f'<path d="{poly_d(ARCS[i])}" fill="none" stroke="#f2e7c9" stroke-width="{STROKE_W}" '
                       f'stroke-linecap="round" stroke-linejoin="round" opacity="0.9" '
                       f'stroke-dasharray="{ARC_LEN[i]:.1f}" stroke-dashoffset="{off:.1f}"/>')

    # travelling light, once the loop is whole
    if p_light > 0 and p_close >= 0.999:
        s = p_light
        x, y = point_at(loop, s)
        svg.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="86" ry="86" fill="url(#glow)" opacity="0.9"/>')
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="#fff3d0" opacity="0.99"/>')
        # brief trail
        for b in range(1, 16):
            sb = (s - b * 0.005) % 1.0
            xb, yb = point_at(loop, sb)
            svg.append(f'<circle cx="{xb:.1f}" cy="{yb:.1f}" r="{max(1.5, 10-b*0.55):.1f}" '
                       f'fill="#ffe9b0" opacity="{max(0.04, 0.6-b*0.04):.3f}"/>')

    svg.append('</svg>')
    return "\n".join(svg)

# ---- render ---------------------------------------------------------------
OUT = "/home/sprite/slop-salon-rahel/assets/closure_frames"
FRAMES = 144
FPS = 24
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

for f in range(FRAMES):
    u = f / (FRAMES - 1)
    svg = frame_svg(u)
    tmp = f"{OUT}/f{f:04d}.svg"
    with open(tmp, "w") as fo:
        fo.write(svg)
    png = f"{OUT}/f{f:04d}.png"
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), tmp, "-o", png], check=True)
    os.remove(tmp)
    if f % 24 == 0:
        print(f"frame {f}/{FRAMES}")

subprocess.run([
    "ffmpeg", "-y", "-framerate", str(FPS), "-i", f"{OUT}/f%04d.png",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart",
    "/home/sprite/slop-salon-rahel/assets/closure.mp4",
], check=True)
print("wrote assets/closure.mp4")
