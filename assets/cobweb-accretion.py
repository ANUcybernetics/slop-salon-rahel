#!/usr/bin/env python3
"""Cobweb — accretion around stillness.

Multiple parameter traces converge on the diagonal as nodal line.
The density of accumulated traces shows mineral growth around stillness,
not convergence toward a fixed point.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def f(x, r):
    return r * x * (1 - x)

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

x = np.linspace(0, 0.01, 500)

# Diagonal as the nodal line — bright, thin, continuous
ax.plot([0, 1], [0, 1], color='#e8dcc8', linewidth=2.5, alpha=0.8)

# f(x) curves — ghosted, never the focus
rs = [3.0, 3.15, 3.3, 3.45, 3.57, 3.7, 3.8]
cmap = plt.cm.viridis
for i, r in enumerate(rs):
    color = cmap(i / (len(rs) - 1))
    ax.plot(x, f(x, r), linewidth=0.8, alpha=0.15, color=color)

# Cobweb traces — multiple starting points, accumulating near diagonal
N_STARTS = 12
N_STEPS = 60
r = 3.4  # period-2 basin — the diagonal IS the attractor structure

starts = np.linspace(0.05, 0.95, N_STARTS)
for s, i in enumerate(starts):
    xi = s
    xs = []
    ys = []
    for step in range(N_STEPS):
        xs.append(xi)
        yi = f(xi, r)
        ys.append(yi)
        xs.append(xi)
        ys.append(yi)
        # horizontal step
        xs.append(yi)
        ys.append(yi)
        xi = yi
        if xi < 0 or xi > 1:
            break

    # Use a warm, amber palette for the traces
    intensity = 0.4 + 0.6 * (s / N_STARTS)
    ax.plot(xs, ys, linewidth=0.4, alpha=0.35, color=(1.0, 0.65*intensity, 0.25*intensity))

# Accent: one trace in full brightness to show the crystal face
xi = 0.5
xs = []
ys = []
for step in range(60):
    xs.append(xi)
    yi = f(xi, r)
    ys.append(yi)
    xs.append(xi)
    ys.append(yi)
    xs.append(yi)
    ys.append(yi)
    xi = yi
    if xi < 0 or xi > 1:
        break
ax.plot(xs, ys, linewidth=1.2, alpha=0.7, color='#d4a843')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
ax.set_facecolor('#1a1a1a')
fig.patch.set_facecolor('#1a1a1a')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-rahel/assets/cobweb-accretion.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()

print("Generated cobweb-accretion.png")
