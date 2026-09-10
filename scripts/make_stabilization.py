#!/usr/bin/env python3
"""
'the word grows a strand; the link does not move.'

Markov stabilization, made visible. Two open words hang above one closed link:

    sigma1^3         in B_2   -- two strands, three crossings
    sigma1^3 sigma2  in B_3   -- three strands, four crossings (one strand more)

Both close to the trefoil: the added strand carries exactly one crossing, and in
the closure that crossing is idle, so the link cannot tell the word was ever
stabilized. The link is drawn complete at frame 0 and never animates (only a
light runs it at the end); the words above are what move -- and the right-hand
word grows its third strand mid-piece.

Reuses the closure engine's tricks: track each strand's slot per crossing, split
every strand wherever it passes UNDER a crossing so over/under reads, and walk
the closed loop by arclength for the travelling light.
"""
import math, os, subprocess, shutil, sys

W, H = 1600, 900
INK = "#f2e7c9"
COPPER = "#f4c25a"
VIOLET = "#9a86ff"


def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


class Braid:
    """A braid word drawn along x (strand slots are y-positions)."""

    def __init__(self, word, n, x0, xb, ymid, dy, stroke=20.0):
        self.word, self.n, self.x0, self.xb = word, n, x0, xb
        self.ymid, self.dy, self.stroke = ymid, dy, stroke
        self.L = len(word)
        self.cw = (xb - x0) / self.L if self.L else 0.0
        self.gap = stroke + 4
        order = list(range(n))
        rec = [order[:]]
        for (sl, _s) in word:
            order[sl], order[sl + 1] = order[sl + 1], order[sl]
            rec.append(order[:])
        self.rec = rec
        self.crossings = []
        for k, (sl, sgn) in enumerate(word):
            upper, lower = rec[k][sl], rec[k][sl + 1]
            over = upper if k % 2 == 0 else lower
            under = lower if over == upper else upper
            xc = x0 + (k + 0.5) * self.cw
            yc = ymid + (sl - (n - 1) / 2) * dy
            self.crossings.append((k, over, under, xc, yc, sgn))

    def slotpos(self, s):
        return self.ymid + (s - (self.n - 1) / 2) * self.dy

    def y_of(self, x, p):
        if x <= self.x0:
            return self.slotpos(self.rec[0].index(p))
        if x >= self.xb:
            return self.slotpos(self.rec[self.L].index(p))
        k = min(int((x - self.x0) / self.cw), self.L - 1)
        bs, a = self.rec[k].index(p), self.rec[k + 1].index(p)
        if bs == a:
            return self.slotpos(bs)
        t = (x - (self.x0 + k * self.cw)) / self.cw
        return self.slotpos(bs + (a - bs) * t)

    def is_under(self, p, x):
        for (_k, _ov, und, xc, _yc, _s) in self.crossings:
            if und == p and abs(x - xc) < self.gap / 2:
                return True
        return False

    def strand_segments(self, p, yoff=0.0, M=900):
        segs, cur = [], []
        for j in range(M + 1):
            x = self.x0 + (self.xb - self.x0) * j / M
            if self.is_under(p, x):
                if len(cur) >= 2:
                    segs.append(cur)
                cur = []
            else:
                cur.append((x, self.y_of(x, p) + yoff))
        if len(cur) >= 2:
            segs.append(cur)
        return segs

    def strand_pts(self, p, M=240):
        return [(self.x0 + (self.xb - self.x0) * j / M,
                 self.y_of(self.x0 + (self.xb - self.x0) * j / M, p))
                for j in range(M + 1)]


def poly_d(pts):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for (x, y) in pts)


def poly_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def point_at(pts, s):
    total = poly_len(pts)
    target = s * total
    d = 0.0
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if seg > 0 and d + seg >= target:
            t = (target - d) / seg
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        d += seg
    return pts[-1]


def bez(p0, p1, p2, p3, M=80):
    out = []
    for j in range(M + 1):
        t = j / M
        mt = 1 - t
        out.append((mt**3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t**3 * p3[0],
                    mt**3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t**3 * p3[1]))
    return out


# ---- composition ----------------------------------------------------------
# left word: sigma1^3  in B_2
W1 = Braid([(0, +1), (0, +1), (0, +1)], 2, 165, 665, 235, 86)
# right word, two states: sigma1^3 with an idle third strand, and sigma1^3 sigma2.
# The copper part must be *the left word* at g=0, so the sigma2 swap cannot be
# baked in -- interpolate between the two states as the violet strand arrives.
W2A = Braid([(0, +1), (0, +1), (0, +1)], 3, 935, 1435, 278, 86)
W2B = Braid([(0, +1), (0, +1), (0, +1), (1, +1)], 3, 935, 1435, 278, 86)
W2 = W2B  # x-range / stroke / gap / first-three crossings come from here
# the link: closure of sigma1^3 -- one closed loop, centred, drawn once, still
LK = Braid([(0, +1), (0, +1), (0, +1)], 2, 610, 990, 545, 116)


def w2_y(x, p, g):
    return (1 - g) * W2A.y_of(x, p) + g * W2B.y_of(x, p)


def w2_segments(p, g, yoff=0.0, M=900):
    segs, cur = [], []
    for j in range(M + 1):
        x = W2.x0 + (W2.xb - W2.x0) * j / M
        under = False
        for (k, _ov, und, xc, _yc, _s) in W2B.crossings:
            if k == 3 and g < 0.999:
                continue
            if und == p and abs(x - xc) < W2.gap / 2:
                under = True
                break
        if under:
            if len(cur) >= 2:
                segs.append(cur)
            cur = []
        else:
            cur.append((x, w2_y(x, p, g) + yoff))
    if len(cur) >= 2:
        segs.append(cur)
    return segs


def arc_pts(i, R=140, D=210, M=220):
    yi = LK.slotpos(i)
    return bez((LK.xb, yi), (LK.xb + R, yi + D), (LK.x0 - R, yi + D), (LK.x0, yi), M)


ARCS = [arc_pts(i) for i in range(LK.n)]
ARC_LEN = [poly_len(a) for a in ARCS]

loop = []
pos = 0
for _ in range(LK.n):
    p = LK.rec[0][pos]
    loop.extend(LK.strand_pts(p))
    loop.extend(ARCS[LK.rec[LK.L].index(p)])
    pos = LK.rec[LK.L].index(p)

# closure fibres: each loose inner end of each word sews down into the link
LINK_TOP = (800.0, 482.0)


def fibre(xe, y0, bend_x):
    return bez((xe, y0), (xe + bend_x, y0 + 70), (800 - bend_x * 0.4, 395), LINK_TOP, 100)


FIB_L = [fibre(W1.xb, W1.y_of(W1.xb, p), 55) for p in range(W1.n)]
FIB_R = [fibre(W2.x0, w2_y(W2.x0, p, 0.0), -55) for p in range(W2.n)]
FIB_L_LEN = [poly_len(f) for f in FIB_L]
FIB_R_LEN = [poly_len(f) for f in FIB_R]


def strand_paths(b, col, opacity, yoff_map=None, M=900):
    out = []
    for p in range(b.n):
        yo = 0.0 if yoff_map is None else yoff_map.get(p, 0.0)
        op = opacity if yoff_map is None else opacity * yoff_map.get(("op", p), 1.0)
        for seg in b.strand_segments(p, yoff=yo, M=M):
            out.append(f'<path d="{poly_d(seg)}" fill="none" stroke="{col}" stroke-width="{b.stroke}" '
                       f'stroke-linecap="round" stroke-linejoin="round" opacity="{op:.3f}"/>')
    return out


def frame_svg(u):
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    s.append('<defs>')
    s.append('<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#0d0a12"/><stop offset="1" stop-color="#151121"/></linearGradient>')
    s.append('<radialGradient id="warm" cx="0.5" cy="0.5" r="0.5">'
             '<stop offset="0" stop-color="#f4c25a" stop-opacity="0.75"/>'
             '<stop offset="1" stop-color="#f4c25a" stop-opacity="0"/></radialGradient>')
    s.append('<radialGradient id="cool" cx="0.5" cy="0.5" r="0.5">'
             '<stop offset="0" stop-color="#9a86ff" stop-opacity="0.7"/>'
             '<stop offset="1" stop-color="#9a86ff" stop-opacity="0"/></radialGradient>')
    s.append('<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
             '<stop offset="0" stop-color="#fff3d0" stop-opacity="0.95"/>'
             '<stop offset="1" stop-color="#f4c25a" stop-opacity="0"/></radialGradient>')
    s.append('</defs>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

    # ---- phases ----
    p_left = clamp((u - 0.05) / 0.20)            # left word draws in
    p_right = clamp((u - 0.24) / 0.16)           # right word, two strands
    p_grow = clamp((u - 0.46) / 0.16)            # third strand slides in
    p_fib = clamp((u - 0.34) / 0.30)             # closure fibres reach the link
    p_light = clamp((u - 0.76) / 0.24)           # light runs the still link

    # ---- the link: present from frame 0, still ----
    s.append(f'<ellipse cx="{W/2:.0f}" cy="{LK.ymid+80:.0f}" rx="360" ry="190" fill="url(#warm)" opacity="0.05"/>')
    for (k, _ov, _un, xc, yc, _sg) in LK.crossings:
        br = 0.40 + 0.09 * math.sin(2 * math.pi * (u * 1.2 + k * 0.2))
        s.append(f'<ellipse cx="{xc:.1f}" cy="{yc:.1f}" rx="70" ry="62" fill="url(#warm)" opacity="{br:.3f}"/>')
    for p in range(LK.n):
        for seg in LK.strand_segments(p):
            s.append(f'<path d="{poly_d(seg)}" fill="none" stroke="{INK}" stroke-width="{LK.stroke}" '
                     f'stroke-linecap="round" stroke-linejoin="round" opacity="0.92"/>')
    for a in ARCS:
        s.append(f'<path d="{poly_d(a)}" fill="none" stroke="{INK}" stroke-width="{LK.stroke}" '
                 f'stroke-linecap="round" stroke-linejoin="round" opacity="0.92"/>')

    # ---- closure fibres: each loose word-end sews down into the link ----
    if p_fib > 0:
        for i, (fib, ln) in enumerate(zip(FIB_L, FIB_L_LEN)):
            pp = clamp(p_fib - i * 0.08)
            if pp <= 0:
                continue
            s.append(f'<path d="{poly_d(fib)}" fill="none" stroke="{COPPER}" stroke-width="6" '
                     f'stroke-linecap="round" opacity="0.30" '
                     f'stroke-dasharray="{ln:.1f}" stroke-dashoffset="{ln*(1-pp):.1f}"/>')
        for i, (fib, ln) in enumerate(zip(FIB_R, FIB_R_LEN)):
            gate = p_grow if i == 2 else 1.0
            col = VIOLET if i == 2 else COPPER
            pp = clamp(p_fib - 0.12 - i * 0.08) * gate
            if pp <= 0:
                continue
            s.append(f'<path d="{poly_d(fib)}" fill="none" stroke="{col}" stroke-width="6" '
                     f'stroke-linecap="round" opacity="0.30" '
                     f'stroke-dasharray="{ln:.1f}" stroke-dashoffset="{ln*(1-pp):.1f}"/>')

    # ---- left word: sigma1^3, in copper ----
    s.append(f'<g opacity="{p_left:.3f}">')
    for (k, _ov, _un, xc, yc, _sg) in W1.crossings:
        s.append(f'<ellipse cx="{xc:.1f}" cy="{yc:.1f}" rx="64" ry="56" fill="url(#warm)" opacity="0.28"/>')
    s.extend(strand_paths(W1, COPPER, 0.95))
    for p in range(W1.n):
        for xe in (W1.x0, W1.xb):
            s.append(f'<circle cx="{xe}" cy="{W1.y_of(xe,p):.1f}" r="11" fill="{COPPER}" opacity="0.95"/>')
    s.append('</g>')

    # ---- right word: the same copper word, one violet strand added ----
    g = p_grow
    s.append(f'<g opacity="{p_right:.3f}">')
    for (k, _ov, _un, xc, yc, _sg) in W2B.crossings:
        if k < 3:
            s.append(f'<ellipse cx="{xc:.1f}" cy="{yc:.1f}" rx="60" ry="52" fill="url(#warm)" opacity="0.28"/>')
        else:
            s.append(f'<ellipse cx="{xc:.1f}" cy="{yc:.1f}" rx="60" ry="52" fill="url(#cool)" opacity="{0.38*g:.3f}"/>')
    for p in (0, 1):
        for seg in w2_segments(p, g):
            s.append(f'<path d="{poly_d(seg)}" fill="none" stroke="{COPPER}" stroke-width="{W2.stroke}" '
                     f'stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>')
    yoff = (1 - g) * W2.dy * 0.7
    for seg in w2_segments(2, g, yoff=yoff):
        s.append(f'<path d="{poly_d(seg)}" fill="none" stroke="{VIOLET}" stroke-width="{W2.stroke}" '
                 f'stroke-linecap="round" stroke-linejoin="round" opacity="{0.95*g:.3f}"/>')
    for p in (0, 1):
        for xe in (W2.x0, W2.xb):
            s.append(f'<circle cx="{xe}" cy="{w2_y(xe,p,g):.1f}" r="11" fill="{COPPER}" opacity="0.95"/>')
    for xe in (W2.x0, W2.xb):
        s.append(f'<circle cx="{xe}" cy="{w2_y(xe,2,g)+yoff:.1f}" r="11" fill="{VIOLET}" opacity="{0.95*g:.3f}"/>')
    s.append('</g>')

    # ---- light runs the still link ----
    if p_light > 0:
        x, y = point_at(loop, p_light)
        s.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="80" ry="80" fill="url(#glow)" opacity="0.9"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="#fff3d0" opacity="0.99"/>')
        for b in range(1, 16):
            sb = (p_light - b * 0.005) % 1.0
            xb, yb = point_at(loop, sb)
            s.append(f'<circle cx="{xb:.1f}" cy="{yb:.1f}" r="{max(1.5, 10-b*0.55):.1f}" '
                     f'fill="#ffe9b0" opacity="{max(0.04, 0.6-b*0.04):.3f}"/>')

    s.append('</svg>')
    return "\n".join(s)


# ---- render ---------------------------------------------------------------
OUT = "/home/sprite/slop-salon-rahel/assets/stabilization_frames"
FRAMES, FPS = 168, 24
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

probe = len(sys.argv) > 1
for f in range(FRAMES):
    if probe and f % 20 != 0:
        continue
    u = f / (FRAMES - 1)
    svg = frame_svg(u)
    tmp = f"{OUT}/f{f:04d}.svg"
    with open(tmp, "w") as fo:
        fo.write(svg)
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), tmp,
                    "-o", f"{OUT}/f{f:04d}.png"], check=True)
    os.remove(tmp)
    if f % 24 == 0:
        print(f"frame {f}/{FRAMES}")

if not probe:
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", f"{OUT}/f%04d.png",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart",
        "/home/sprite/slop-salon-rahel/assets/stabilization.mp4",
    ], check=True)
    print("wrote assets/stabilization.mp4")
