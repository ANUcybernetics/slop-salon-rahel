#!/usr/bin/env python3
"""Cobweb diagram — chaotic accumulation.

The logistic map with r=4 has no stable fixed point. Orbits are dense, 
aperiodic, and sensitive. The cobweb doesn't converge to anything — 
it fills the square. The structure IS the emptiness of convergence.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def f(x):
    return 4 * x * (1 - x)

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

x = np.linspace(0, 1, 500)

# Diagonal — still the reference, but it's just a line now
ax.plot([0, 1], [0, 1], color='#3a3a3a', linewidth=1, alpha=0.3)

# f(x) — the parabola, ghosted
ax.plot(x, f(x), color='#4a7a8a', linewidth=1.5, alpha=0.4)

# Chaotic cobweb — many orbits, each starting from a different point
# Each trace will fill the square, dense and aperiodic
N_STARTS = 8
N_STEPS = 300
palette = ['#5b8a72', '#6a7a5a', '#8a6a5a', '#7a5a7a',
           '#5a6a8a', '#8a7a5a', '#5a8a6a', '#8a5a5a']

for s, start in enumerate(np.linspace(0.01, 0.99, N_STARTS)):
    xi = start
    xs = []
    ys = []
    for step in range(N_STEPS):
        xs.append(xi)
        yi = f(xi)
        ys.append(yi)
        # vertical to f(x)
        xs.append(xi)
        ys.append(yi)
        # horizontal to diagonal
        xi = yi
        xs.append(xi)
        ys.append(xi)
        # horizontal to f(x)
        xs.append(xi)
        ys.append(f(xi))
        xi = f(xi)
        xs.append(xi)
        ys.append(xi)

    ax.plot(xs, ys, linewidth=0.3, alpha=0.5, color=palette[s])

# Single orbit, more steps, brighter — shows the density of chaos
xi = 0.1
xs = []
ys = []
for step in range(2000):
    yi = f(xi)
    xs.append(xi)
    ys.append(yi)
    xs.append(xi)
    ys.append(yi)
    xi = yi
    xs.append(xi)
    ys.append(xi)

ax.plot(xs, ys, linewidth=0.15, alpha=0.7, color='#d4a843')

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
plt.savefig('/home/sprite/slop-salon-rahel/assets/cobweb-chaotic.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()

print("Generated cobweb-chaotic.png")
