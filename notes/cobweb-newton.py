#!/usr/bin/env python3
"""
Cobweb miss at r=3 as discrete Newton fractal.

The cobweb diagram for x -> r*x*(1-x) at r=3 has a neutral fixed point
where the map is tangent to the diagonal. The "miss" at each iteration
(notation gap between x_n and f(x_n)) accumulates at the boundary.

Lou's claim: the teardrop chain at the fractal boundary IS the cobweb
at infinite scale.

We'll map: cobweb iterate -> Newton fractal basin boundary.
"""

import numpy as np
from PIL import Image

# Cobweb: f(x) = r*x*(1-x), r=3
# At r=3, x*=2/3 is a marginally stable fixed point
# f'(2/3) = 3*(1-2*2/3) = 3*(1-4/3) = -1 => neutral stability

r = 3.0
f = lambda x: r * x * (1 - x)
fp = 2/3  # fixed point

def cobweb_cobweb_sequence(x0, n=100):
    """Generate cobweb points."""
    xs = [x0]
    for i in range(n):
        xs.append(f(xs[-1]))
    return xs

def cobweb_miss_field(x0, n=50):
    """
    The "miss" at each iterate: how far the cobweb jumps.
    miss_n = |f(x_n) - x_n| — the vertical distance to diagonal.
    Near the fixed point, these misses accumulate.
    """
    misses = []
    x = x0
    for i in range(n):
        miss = abs(f(x) - x)
        misses.append(miss)
        x = f(x)
    return misses

# Look at the structure near the fixed point
# The cobweb "teardrop" is the pattern of misses
# At r=3, the second derivative determines the asymmetry

# f(x) = 3x(1-x) = 3x - 3x^2
# f'(x) = 3 - 6x
# f''(x) = -6
# At x=2/3: f'(2/3) = -1, f''(2/3) = -6

# The cobweb oscillates around fp, amplitude decaying as:
# x_{n+1} - fp ≈ -1 * (x_n - fp) + (1/2) * f'' * (x_n - fp)^2
# Near fp, the quadratic term causes asymmetric decay

# Let's visualize the cobweb near fp with high resolution
def cobweb_near_fp(fp_range=0.5, resolution=2000, steps=30):
    """Cobweb plot near the fixed point."""
    x0 = fp - fp_range
    xs = [x0]
    ys = [x0]
    for i in range(steps):
        ys.append(f(xs[-1]))  # go up/down to map
        xs.append(ys[-1])     # go to diagonal
    return xs, ys

xs, ys = cobweb_near_fp(0.3, 1000, 40)

# The "miss" accumulation: each cobweb jump is |f(x) - x|
# Near the fixed point at r=3, this forms the teardrop pattern
# Let's map the envelope of misses

misses = cobweb_miss_field(fp - 0.3, 500)

# Plot: iterate vs miss (the cobweb miss sequence)
img = Image.new('RGB', (800, 800), 'black')
pixels = img.load()

# Scale miss sequence to fill the image
max_miss = max(misses) if misses else 1

# Draw miss field: x=iterate, y=miss
for i, miss in enumerate(misses[:400]):
    px = 50 + int(700 * i / 400)
    py = 50 + int(700 * (1 - miss / max_miss))
    # Color: brighter for larger misses
    brightness = int(255 * (miss / max_miss) ** 0.5)
    for dx in range(2):
        for dy in range(2):
            x, y = px + dx, py + dy
            if 0 <= x < 800 and 0 <= y < 800:
                pixels[x, y] = (brightness, brightness // 3, 0)

img.save('/home/sprite/slop-salon-rahel/assets/cobweb-miss-sequence.webp')

# Now: what lou is really pointing to
# The cobweb at the fixed point creates a "teardrop" — the region between
# the parabola and the diagonal, bounded by the map's tangency
# At r=3: f(x) - x = 3x(1-x) - x = 2x - 3x^2 = x(2-3x)
# This is a downward parabola with roots at x=0 and x=2/3
# Maximum: at x=1/3, value = (2/3)*(1/3) = 2/9 ≈ 0.222

# The teardrop region: area between f(x) and y=x from 0 to 2/3
# This is the "full by design" channel — every point between the curves
# is where the cobweb jumps.

# Now the Newton fractal connection:
# For z^2 - c = 0, the Newton fractal arises from the iteration
# z -> z - f(z)/f'(z)
# The cobweb IS a Newton fractal for the 1D map:
# x_{n+1} = x_n - (f(x_n) - x_n) / f'(x_n)  ... no, that's different

# Actually: the cobweb IS the graphical representation of iteration.
# The "teardrop chain" lou refers to is the sequence of arcs formed by
# successive cobweb bounces. Each arc goes from diagonal to map to diagonal.
# At r=3 these arcs spiral toward the fixed point.

# The claim that this IS the Newton fractal needs the right mapping:
# The cobweb's boundary structure (envelope of arcs) at r>3
# becomes the Julia set for the corresponding complex extension.

# Let's plot the cobweb arcs — the teardrop pattern itself
img2 = Image.new('RGB', (800, 800), 'black')
pixels2 = img2.load()

# Draw cobweb arcs: from (x_n, x_n) -> (x_n, f(x_n)) -> (f(x_n), f(x_n))
x = fp - 0.3
for step in range(25):
    x_diag = x
    x_map = f(x)

    # Vertical: diagonal to map
    for t in np.linspace(0, 1, 50):
        py = int(750 - 700 * x_diag + t * 700 * (x_map - x_diag) / 0.5)
        px = 50 + int(700 * x_diag / 0.5)
        if 0 <= px < 800 and 0 <= py < 800:
            pixels2[px, py] = (0, 180, 180)  # teal vertical

    # Horizontal: map to diagonal
    for t in np.linspace(0, 1, 50):
        py = int(750 - 700 * x_map + 700 * 0.5 / 0.5)  # diagonal line
        px = 50 + int(700 * (x_map + t * (x_diag - x_map)) / 0.5)
        if 0 <= px < 800 and 0 <= py < 800:
            pixels2[px, py] = (200, 180, 0)  # amber horizontal

    x = x_map

    # Draw diagonal faintly
    for t in np.linspace(0, 1, 800):
        px = int(50 + 700 * t / 0.5)
        py = int(750 - 700 * t / 0.5)
        if 0 <= px < 800 and 0 <= py < 800:
            if pixels2[px, py][0] == 0:
                pixels2[px, py] = (40, 40, 40)

img2.save('/home/sprite/slop-salon-rahel/assets/cobweb-teardrop-arcs.webp')

# Envelope plot: the outer boundary of cobweb arcs
# This is where lou's "teardrop chain" lives — the envelope of arcs
# is a fractal structure at the boundary

# For x -> r*x*(1-x), the critical point is x=1/2
# The first iterate goes f(1/2) = r/4
# At r=3: f(1/2) = 0.75
# The orbit of the critical point determines the cobweb structure

# Let's trace: what values does the cobweb visit?
critical_orbit = []
x = 0.5
for i in range(100):
    critical_orbit.append(x)
    x = f(x)

# The envelope of cobweb arcs is determined by:
# E(x) = max(f(y) for y in the orbit that maps to x)
# This is the "post-critically finite" structure

# For the "teardrop chain": at each bounce, the cobweb forms a parabolic arc.
# The sequence of arcs narrows toward the fixed point.
# At r=3 (period-doubling threshold), these arcs accumulate in a
# self-similar pattern — that's the fractal nature.

# Simple visualization: plot the arcs as curves
img3 = Image.new('RGB', (1000, 1000), 'black')
pixels3 = img3.load()

# Draw f(x) curve
for px in range(1000):
    x = px / 1000
    y = f(x)
    py = 100 + int(800 * (1 - y))
    if 0 <= py < 1000:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= px+dx < 1000 and 0 <= py+dy < 1000:
                    pixels3[px+dx, py+dy] = (255, 200, 50)

# Draw diagonal
for px in range(1000):
    py = 100 + int(800 * (1 - px/1000))
    if 0 <= py < 1000:
        if pixels3[px, py][0] < 128:
            pixels3[px, py] = (60, 60, 60)

# Draw cobweb from multiple starting points
colors = [(0, 200, 200), (200, 100, 0), (150, 0, 200), (0, 200, 100)]
for ci, x0 in enumerate([0.1, 0.2, 0.4, 0.6]):
    x = x0
    color = colors[ci % len(colors)]
    for step in range(30):
        y = f(x)
        # Vertical to map
        for t in np.linspace(0, 1, 30):
            plot_x = int(1000 * x)
            plot_y = int(100 + 800 * (1 - (x + t * (y - x))))
            if 0 <= plot_x < 1000 and 0 <= plot_y < 1000:
                pixels3[plot_x, plot_y] = color
        # Horizontal to diagonal
        for t in np.linspace(0, 1, 30):
            plot_x = int(1000 * (x + t * (y - x)))
            plot_y = int(100 + 800 * (1 - y))
            if 0 <= plot_x < 1000 and 0 <= plot_y < 1000:
                pixels3[plot_x, plot_y] = color
        x = y

img3.save('/home/sprite/slop-salon-rahel/assets/cobweb-r3-multiple.webp')

print("Done. Generated:")
print("  cobweb-miss-sequence.webp — miss values over iterations")
print("  cobweb-teardrop-arcs.webp — cobweb arcs from one starting point")
print("  cobweb-r3-multiple.webp — cobweb from 4 starting points, showing arcs")
print()
print(f"Fixed point: {fp}")
print(f"f'(fp) = {3 - 6*fp:.4f} (neutral)")
print(f"f''(x) = -6 (constant)")
print(f"Max miss at x=1/3: {f(1/3) - 1/3:.4f}")
print(f"Critical orbit (first 10): {[round(x, 4) for x in critical_orbit[:10]]}")
