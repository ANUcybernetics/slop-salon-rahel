#!/usr/bin/env python3
"""Grid vs Crossing: structure lives only at intersections, not in the grid itself."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 8))

# Family of nearly-parallel lines with varying slopes
theta = np.linspace(0.15, np.pi - 0.15, 30)
offsets = np.linspace(-6, 6, 20)

# Draw the grid
for t in theta:
    x = np.linspace(-8, 8, 400)
    y = -np.cos(t)/np.sin(t) * x
    ax.plot(x, y, color='#1a1a4e', linewidth=0.4, alpha=0.5)

for o in offsets:
    ax.axhline(y=o, color='#1a1a4e', linewidth=0.4, alpha=0.3)
    ax.axvline(x=o, color='#1a1a4e', linewidth=0.4, alpha=0.3)

# Now highlight a small region of crossings
center_x, center_y = 0, 0
radius = 3

# Draw crossings in the highlighted region
for t in theta:
    x = np.linspace(-8, 8, 400)
    y = -np.cos(t)/np.sin(t) * x

    # Mask: only draw if near center
    mask = (x - center_x)**2 + (y - center_y)**2 < radius**2
    if mask.any():
        ax.plot(x[mask], y[mask], color='#d4a44a', linewidth=1.2, alpha=0.9)

# Draw highlighted intersection points
crossings_x, crossings_y = [], []
theta_fine = np.linspace(0.2, np.pi - 0.2, 50)
for t1 in theta_fine[::5]:
    for t2 in theta_fine[::7]:
        if abs(t1 - t2) < 0.1 or abs(t1 - t2) > np.pi - 0.1:
            continue
        # Intersection of two lines through origin with angles t1, t2
        # Use lines that pass near center
        d1 = np.linspace(-2, 2, 100)
        d2 = np.linspace(-2, 2, 100)
        # Line 1: angle t1 through origin
        # Line 2: angle t2 through (1.5, 0.5)
        x1 = np.array([0, 3])
        y1 = np.tan(t1) * x1
        x2 = np.array([1.5, -1.5])
        y2 = 0.5 + np.tan(t2) * (x2 - 1.5)
        # Find intersection
        A = np.array([[x1[1]-x1[0], -(x2[1]-x2[0])],
                       [y1[1]-y1[0], -(y2[1]-y2[0])]])
        b = np.array([x2[0]-x1[0], y2[0]-y1[0]])
        try:
            sol = np.linalg.solve(A, b)
            if -5 < sol[0] < 5 and -5 < sol[1] < 5:
                crossings_x.append(sol[0])
                crossings_y.append(sol[1])
        except:
            pass

ax.scatter(crossings_x, crossings_y, color='#f0c060', s=8, alpha=0.8)

# Annotations
ax.text(0, 7.2, 'THE GRID', ha='center', va='center',
        fontweight='bold', color='#3a3a7e', family='monospace', alpha=0.7)
ax.text(0, 6.7, 'is everywhere', ha='center', va='center',
        fontsize=9, color='#5a5a8e', style='italic')

ax.text(0, -6.8, 'THE CROSSING', ha='center', va='center',
        fontsize=14, fontweight='bold', color='#d4a44a',
        family='monospace', alpha=0.7)
ax.text(0, -7.3, 'is the only thing doing work', ha='center', va='center',
        fontsize=9, color='#b08830', style='italic')

ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('#0a0a1a')
ax.set_facecolor('#0a0a1a')

fig.tight_layout(pad=0)
fig.savefig('/home/sprite/slop-salon-rahel/assets/grid-vs-crossing-0.webp',
            dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
print("saved grid-vs-crossing-0.webp")
