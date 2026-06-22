#!/usr/bin/env python3
"""Cobweb diagram rendered as standing wave / crystal structure.
The diagonal IS the nodal line — axis of zero amplitude.
Iteration paths trace mineral growth along resonant eigenmodes."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Logistic map: f(x) = r*x*(1-x)
def f(x, r):
    return r * x * (1 - x)

# Create cobweb for several r values simultaneously
# Each r gives a different eigenmode-like convergence pattern
rs = [2.8, 3.2, 3.5, 3.7]
colors = ['#4a90d9', '#5bb8a0', '#d4a843', '#c94c4c']
labels = ['r=2.8', 'r=3.2', 'r=3.5', 'r=3.7']

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Draw diagonal (the nodal line — the axis)
x = np.linspace(0, 1, 500)
ax.plot(x, x, 'k-', linewidth=1.5, alpha=0.3, label='diagonal = nodal line')

# Draw f(x) curves
for r, color, label in zip(rs, colors, labels):
    ax.plot(x, f(x, r), linewidth=1.5, alpha=0.5, color=color, label=label)

# Draw cobweb paths
N_STEPS = 80
for r, color in zip(rs, colors):
    x0 = 0.3
    xi = x0
    xs = [xi]
    ys = [xi]
    for _ in range(N_STEPS):
        # vertical to f(x)
        yi = f(xi, r)
        xs.extend([xi, xi])
        ys.extend([yi, yi])
        # horizontal to diagonal
        xi = yi
        xs.extend([xi, xi])
        ys.extend([yi, yi])
        if xi < 0.01 or xi > 0.99:
            break
    ax.plot(xs, ys, linewidth=0.5, alpha=0.6, color=color)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel('xₙ', fontsize=14)
ax.set_ylabel('f(xₙ)', fontsize=14)
ax.set_title('cobweb — diagonal as nodal line', fontsize=16, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.grid(False)
ax.set_facecolor('#f8f6f0')
fig.patch.set_facecolor('#f8f6f0')

# Remove ticks for cleaner look
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-rahel/assets/cobweb-resonance-canvas.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()

print("Generated cobweb-resonance-canvas.png")
