"""
Lorenz attractor — form is real, orbit never settles.

The attractor can be characterized (orbit, variance, time-average).
No trajectory ever repeats or arrives.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Lorenz system parameters
sigma, rho, beta = 10.0, 28.0, 8.0/3.0

def lorenz_step(x, y, z, dt=0.005):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return x + dx*dt, y + dy*dt, z + dz*dt

# Integrate
n = 40000
xs, ys, zs = np.zeros(n), np.zeros(n), np.zeros(n)
xs[0], ys[0], zs[0] = 0.1, 0.0, 0.0
for i in range(1, n):
    xs[i], ys[i], zs[i] = lorenz_step(xs[i-1], ys[i-1], zs[i-1])

# Discard transient
skip = 2000
xs, ys, zs = xs[skip:], ys[skip:], zs[skip:]
n = len(xs)

fig, ax = plt.subplots(figsize=(10, 7), facecolor='#0a0a0a')
ax.set_facecolor('#0a0a0a')

# Color by time — blue (early) to amber (late)
# Use segments colored by position in time
from matplotlib.collections import LineCollection

# XZ projection (classic butterfly view)
points = np.array([xs, zs]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Color: cool blue early, warm amber late
t = np.linspace(0, 1, n-1)
colors = plt.cm.plasma(t * 0.75 + 0.1)  # plasma: dark purple → amber

lc = LineCollection(segments, colors=colors, linewidth=0.4, alpha=0.7)
ax.add_collection(lc)

ax.set_xlim(xs.min() - 2, xs.max() + 2)
ax.set_ylim(zs.min() - 2, zs.max() + 2)
ax.set_aspect('equal')
ax.axis('off')

# Minimal caption
fig.text(0.5, 0.04,
    "the attractor is real. no trajectory repeats. no point is home.",
    ha='center', va='bottom',
    color='#888888', fontsize=11,
    fontfamily='monospace')

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig('assets/lorenz.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a0a', edgecolor='none')
plt.close()
print("saved assets/lorenz.png")
