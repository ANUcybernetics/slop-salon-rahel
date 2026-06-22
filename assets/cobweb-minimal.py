#!/usr/bin/env python3
"""Minimal cobweb — single trajectory, clean geometry.
Diagonal as cleavage plane. Single path as crystal growth trace."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def f(x, r):
    return r * x * (1 - x)

fig, ax = plt.subplots(1, 1, figsize=(8, 8))

r = 3.5

# Draw diagonal (cleavage plane)
ax.plot([0, 1], [0, 1], color='#1a1a2e', linewidth=2, alpha=0.4)

# Draw f(x) curve
x = np.linspace(0, 1, 500)
ax.plot(x, f(x, r), color='#1a1a2e', linewidth=2, alpha=0.5)

# Cobweb path — colored by iteration depth
x0 = 0.35
xi = x0

for step in range(150):
    yi = f(xi, r)
    if xi < 0.01 or xi > 0.99 or yi < 0 or yi > 1:
        break
    alpha = 0.8 * (1 - step / 150)
    # Vertical line: (xi, xi) -> (xi, yi)
    ax.plot([xi, xi], [xi, yi], color='#2d6a9f', linewidth=1.2, alpha=alpha)
    # Horizontal line: (xi, yi) -> (yi, yi)
    ax.plot([xi, yi], [yi, yi], color='#2d6a9f', linewidth=1.2, alpha=alpha)
    xi = yi

# Mark limit cycle points
test_x = 0.5
for _ in range(1000):
    test_x = f(test_x, r)
for _ in range(200):
    test_x = f(test_x, r)
    ax.plot(test_x, test_x, 'o', color='#c94c4c', markersize=4, alpha=0.6)

ax.set_xlim(-0.05, 1.15)
ax.set_ylim(-0.05, 1.15)
ax.set_xticks([])
ax.set_yticks([])
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.set_aspect('equal')

ax.set_facecolor('#faf8f2')
fig.patch.set_facecolor('#faf8f2')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-rahel/assets/cobweb-resonance-minimal.png',
            dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(),
            edgecolor='none')
plt.close()

print("Done")
