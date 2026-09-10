#!/usr/bin/env python3
"""The braid, counted in the open.

A 4-strand braid reads itself top to bottom: a horizontal line descends,
revealing one crossing at a time. Each crossing the line passes makes a click
and a flash. A 55 Hz drone holds the winding (the debt). Then the ends are
sewn into a loop and the crossings fade — the side folds back into the
between, and only the winding number (3) remains on the ring.

Written for Pillow + numpy. Frames are piped raw rgb24 to ffmpeg.
"""

import math
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1280, 720
FPS = 10
DUR = 30
NFRAMES = FPS * DUR

# --- braid geometry ----------------------------------------------------
Y_TOP, Y_BOT = 150.0, 540.0
SLOTS = [400.0, 560.0, 720.0, 880.0]
CENTER = (640.0, 345.0)
STRAND_NAMES = ["A", "B", "C", "D"]
STRAND_COLORS = {
    "A": (127, 180, 255),   # blue
    "B": (255, 154, 107),   # orange
    "C": (255, 143, 179),   # pink
    "D": (142, 224, 127),   # green
}
# (yc, left_slot_before, over_left, pair) — pair is just for naming
CROSSINGS = [
    (190.0, 1, True),   # B over C
    (260.0, 0, True),   # A over C
    (330.0, 2, True),   # B over D
    (400.0, 1, False),  # D over A
    (470.0, 0, True),   # C over D
]
DELTA = 26.0


def build_keyframes():
    """Return {strand: [(y, x), ...]} through the braid."""
    # current slot for each physical strand
    slot_of = {s: i for i, s in enumerate(STRAND_NAMES)}
    keys = {s: [(Y_TOP, SLOTS[i])] for s, i in slot_of.items()}
    crossing_geom = []  # (yc, over_strand, x_mid) in read order
    for (yc, j, over_left) in CROSSINGS:
        left_strand = [s for s, sl in slot_of.items() if sl == j][0]
        right_strand = [s for s, sl in slot_of.items() if sl == j + 1][0]
        xl, xr = SLOTS[j], SLOTS[j + 1]
        xm = (xl + xr) / 2.0
        if over_left:
            over, under = left_strand, right_strand
        else:
            over, under = right_strand, left_strand
        crossing_geom.append((yc, over, under, xm))
        # keyframes for both strands
        for s in (left_strand, right_strand):
            x0 = xl if s == left_strand else xr
            x2 = xr if s == left_strand else xl
            keys[s].append((yc - DELTA, x0))
            keys[s].append((yc, xm))
            keys[s].append((yc + DELTA, x2))
        # swap
        slot_of[left_strand], slot_of[right_strand] = j + 1, j
    for s, i in slot_of.items():
        keys[s].append((Y_BOT, SLOTS[i]))
    for c in keys.values():
        c.sort()
    return keys, crossing_geom


KEYS, GEOM = build_keyframes()


def catmull_rom(pts, n=220):
    """pts: sorted (y, x). Smoothly interpolate x(y)."""
    y0 = pts[0][0]
    y1 = pts[-1][0]
    ys = np.linspace(y0, y1, n)
    arr = pts
    out_x = []
    for y in ys:
        # find bracketing segment
        i = 1
        while i < len(arr) - 2 and arr[i][0] < y:
            i += 1
        (ya, xa), (yb, xb) = arr[i - 1], arr[i]
        ya2, xa2 = arr[i - 2]
        yb2, xb2 = arr[i + 1]
        t = (y - ya) / (yb - ya + 1e-9)
        # Catmull-Rom in x given non-uniform y... simplify: cubic hermite in t
        m0 = (xb - xa2) / 2.0
        m1 = (yb2 - xa) / 2.0
        t2, t3 = t * t, t * t * t
        x = ((2 * t2 - t3) * xa + (t3 - t2) * xb +
             (t2 - t3) * m0 + (t3 - t2) * m1)
        out_x.append(x)
    return list(zip(ys.tolist(), [float(x) for x in out_x]))


CURVES = {s: catmull_rom(KEYS[s]) for s in STRAND_NAMES}


def curve_x_at(s, y):
    """x of strand s at height y (linear interp)."""
    pts = CURVES[s]
    # binary search
    lo, hi = 0, len(pts) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if pts[mid][0] < y:
            lo = mid + 1
        else:
            hi = mid
    if lo == 0:
        return pts[0][1]
    y0, x0 = pts[lo - 1]
    y1, x1 = pts[lo]
    f = (y - y0) / (y1 - y0 + 1e-9)
    return x0 + f * (x1 - x0)


def ring_point(x, y, t):
    """Morph straight-braid point toward a ring drawn around CENTER."""
    if t <= 0:
        return x, y
    v = max(0.0, min(1.0, (y - Y_TOP) / (Y_BOT - Y_TOP)))
    phi = math.radians(130.0 - v * 180.0)  # +130deg -> -50deg going down
    R = 185.0
    r = R + (x - CENTER[0]) / 14.0
    qx = CENTER[0] + r * math.cos(phi)
    qy = CENTER[1] + r * math.sin(phi)
    if t >= 1:
        return qx, qy
    return (x + (qx - x) * t, y + (qy - y) * t)


# --- reading-line schedule ---------------------------------------------
READ_Y0, READ_Y1 = Y_TOP + 15, Y_BOT - 15
READ_T0, READ_T1 = 2.0, 17.5


def cursor_y(t):
    if t < READ_T0:
        return READ_Y0
    if t > READ_T1:
        return READ_Y1
    f = (t - READ_T0) / (READ_T1 - READ_T0)
    f = f * f * (3 - 2 * f)  # ease
    return READ_Y0 + f * (READ_Y1 - READ_Y0)


def crossing_times():
    out = []
    for (yc, over, under, xm) in GEOM:
        # invert cursor_y roughly (ignore ease; fine)
        f = (yc - READ_Y0) / (READ_Y1 - READ_Y0)
        out.append((READ_T0 + f * (READ_T1 - READ_T0), yc, over, under, xm))
    return out


CROSS_TIMES = crossing_times()

# --- drawing helpers ----------------------------------------------------
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)


def draw_strand(draw, s, y_lo, y_hi, width=5, color=None, alpha=255):
    color = color or STRAND_COLORS[s]
    # sample points in [y_lo, y_hi]
    ys = np.linspace(y_lo, y_hi, max(2, int((y_hi - y_lo) / 3)))
    pts = [(curve_x_at(s, float(y)), float(y)) for y in ys]
    to_skip = set()
    # gaps where this strand is under
    for (yc, over, under, xm) in GEOM:
        if under == s:
            for i in range(len(ys)):
                if abs(ys[i] - yc) < 6:
                    to_skip.add(i)
    last = None
    for i, (x, y) in enumerate(pts):
        if i in to_skip:
            last = None
            continue
        if last is not None:
            if alpha < 255:
                draw.line([last, (x, y)], fill=color, width=width)
            else:
                draw.line([last, (x, y)], fill=color, width=width)
        last = (x, y)


def glow(draw, xy, r, color, a):
    """Soft radial glow: several concentric rounded lines."""
    for i in range(3):
        rr = int(r * (1 + i * 0.8))
        aa = int(a / (i + 1.5))
        draw.ellipse([xy[0] - rr, xy[1] - rr, xy[0] + rr, xy[1] + rr],
                     outline=color + (aa,), width=2)


def render_frame(t):
    img = Image.new("RGBA", (W, H), (11, 10, 16, 255))
    draw = ImageDraw.Draw(img)

    cy = cursor_y(t)
    clamped = max(min(cy, READ_Y1), READ_Y0)

    closure_t = max(0.0, min(1.0, (t - 20.0) / 7.0))  # 20-27s

    # --- strands, revealed under the reading line ---------------------
    for s in STRAND_NAMES:
        lo = Y_TOP - 10
        hi = clamped if not (t > READ_T1) else Y_BOT + 12
        hi = max(hi, lo + 5)
        if closure_t > 0:
            # blend color toward pale ring as closure proceeds
            base = STRAND_COLORS[s]
            col = tuple(int(c + (240 - c) * min(1.0, closure_t * 1.4))
                        for c in base)
        else:
            col = STRAND_COLORS[s]
        draw_strand(draw, s, lo, hi, width=5, color=col)

    # --- crossing flashes ---------------------------------------------
    for (tc, yc, over, under, xm) in CROSS_TIMES:
        if tc > t or tc < t - 1.2:
            continue
        age = t - tc
        a = max(0, int(255 * (1 - age / 1.2)))
        if closure_t > 0.3 and age < 0.9:
            a = int(a * (1 - closure_t))
        if a <= 0:
            continue
        # morph crossing point too
        pt = ring_point(xm, yc, closure_t)
        glow(draw, pt, 9, (255, 255, 255), a)
        draw.ellipse([pt[0] - 3, pt[1] - 3, pt[0] + 3, pt[1] + 3],
                     fill=(255, 255, 255, a))

    # --- reading line --------------------------------------------------
    if t < READ_T1 and closure_t <= 0:
        for i in range(3):
            yy = cy + i * 3
            aa = int(70 / (i + 1))
            draw.line([(90, yy), (1190, yy)], fill=(255, 255, 255, aa), width=2)
        # cursor dot at each strand
        for s in STRAND_NAMES:
            if cy < Y_BOT:
                draw.ellipse([curve_x_at(s, cy) - 6, cy - 6,
                              curve_x_at(s, cy) + 6, cy + 6],
                             fill=(255, 255, 255, 220))

    # --- the loop: junction points as closure starts -------------------
    if 0 < closure_t < 1:
        for s, i in zip(STRAND_NAMES, range(4)):
            jx, jy = ring_point(curve_x_at(s, Y_TOP), Y_TOP, closure_t)
            draw.ellipse([jx - 4, jy - 4, jx + 4, jy + 4],
                         fill=(255, 255, 255, int(120 * (1 - closure_t))))

    # --- winding number on the ring ------------------------------------
    if t > 27.0:
        a = int(255 * min(1.0, (t - 27.0) / 1.2))
        if closure_t > 0:
            num = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
            nd = ImageDraw.Draw(num)
            nd.text((12, 5), "3", font=FONT, fill=(255, 255, 220, a))
            img.alpha_composite(num, (990, 300))

    # --- vignette ------------------------------------------------------
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for i in range(60):
        aa = int(90 * (i / 60.0))
        od.rectangle([0 + i, 0 + i, W - i, H - i], outline=(0, 0, 0, aa))
    img.alpha_composite(ov)

    # --- fade in/out ----------------------------------------------------
    if t < 1.2:
        img = Image.blend(img, Image.new("RGBA", (W, H), (11, 10, 16, 255)),
                          1.0 - t / 1.2)
    if t > 28.5:
        k = min(1.0, (t - 28.5) / 1.5)
        img = Image.blend(img, Image.new("RGBA", (W, H), (11, 10, 16, 255)), k)
    return img.convert("RGB")


def main_preview(idx, out):
    t = idx / FPS
    frame = render_frame(t)
    frame.save(out)


def main():
    fps = FPS
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(fps), "-i", "-",
        "-i", "/tmp/braid.wav",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "/home/sprite/slop-salon-rahel/assets/braid-counted.mp4",
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(NFRAMES):
        t = i / fps
        frame = render_frame(t)
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    proc.wait()
    print("done", proc.returncode)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--preview":
        main_preview(int(sys.argv[2]), sys.argv[3])
    else:
        main()