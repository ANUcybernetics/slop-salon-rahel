"""Hénon map attractor — density rendering as golden mineral structure."""
import numpy as np
from PIL import Image

a, b = 1.4, 0.3
n = 100_000
x = np.zeros(n)
y = np.zeros(n)
x[0], y[0] = 0.1, 0.1

for i in range(1, n):
    x[i] = 1 - a * x[i-1]**2 + y[i-1]
    y[i] = b * x[i-1]

ax, ay = x[100:], y[100:]

# Density grid
gs = 512
gx = np.clip(((ax - ax.min()) / (ax.max() - ax.min()) * (gs - 1)).astype(int), 0, gs-1)
gy = np.clip(((ay - ay.min()) / (ay.max() - ay.min()) * (gs - 1)).astype(int), 0, gs-1)

grid = np.zeros((gs, gs), dtype=np.int32)
for xi, yi in zip(gx, gy):
    grid[xi, yi] += 1

density = np.log1p(grid).astype(np.float64)
density /= density.max() or 1

# Box blur via slicing
blurred = (density[0:-2, 0:-2] + density[0:-2, 1:-1] + density[0:-2, 2:]
         + density[1:-1, 0:-2] + density[1:-1, 1:-1] + density[1:-1, 2:]
         + density[2:,   0:-2] + density[2:,   1:-1] + density[2:,   2:]) / 9.0
blurred /= blurred.max() or 1

# Golden color function
def gold(t):
    """t in [0,1] -> (r, g, b)"""
    r = min(255, 128 + 127 * t)
    g = min(255, 64 + 180 * np.power(t, 0.5))
    bl = min(255, 10 + 240 * np.power(t, 0.3))
    return int(r), int(g), int(bl)

# Render
size = 1024
img = Image.new('RGB', (size, size), (0, 0, 0))
pix = img.load()

ys, xs = np.nonzero(blurred > 0.02)
for idx in range(len(xs)):
    gx_i, gy_i = xs[idx], ys[idx]
    t = blurred[gx_i, gy_i]
    r, g, bl = gold(t)
    px = int(gx_i / (gs-1) * (size-1))
    py = int((gs - 1 - gy_i) / (gs-1) * (size-1))
    pix[px, py] = (r, g, bl)

img.save('assets/henon-attractor.png')
print("Done. Attractor points:", len(ax), "Rendered to assets/henon-attractor.png")
