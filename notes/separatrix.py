#!/usr/bin/env python3
"""Newton fractal — boundary-only visualization for the separatrix arc.

Shows the set of points that never converge (or converge slowly) as a
positive structure: the boundary IS the geometry, not its absence.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

roots = [1, np.exp(2j*np.pi/3), np.exp(4j*np.pi/3)]

# Grid — zoomed in on a boundary region
N = 800
re = np.linspace(-1.5, 1.5, N)
im = np.linspace(-1.5, 1.5, N)
R, I = np.meshgrid(re, im)
Z = R + 1j*I

# Newton iteration for z^3 - 1
converged = np.full((N, N), -1, dtype=np.int32)
steps = np.zeros((N, N))
Zi = Z.copy()

for i in range(1, 81):
    Zi = (2*Zi**3 + 1) / (3*Zi**2)
    dists = [np.abs(Zi - r) for r in roots]
    dists_arr = np.stack(dists, axis=2)
    min_d = dists_arr.min(axis=2)
    best = dists_arr.argmin(axis=2)
    mask = (min_d < 1e-10) & (converged == -1)
    converged[mask] = best[mask]
    steps[mask] = i
    Zi[converged != -1] = np.array(roots)[converged[converged != -1]]

# Boundary: points that never converged + slowly converging
never_converged = (converged == -1)
slow_converged = (converged >= 0) & (steps >= 15)
boundary = never_converged | slow_converged

# Color the boundary by iteration count (how long it hesitated)
RGB = np.zeros((N, N, 3))
# Black background
if boundary.sum() > 0:
    # Warm colormap: slow -> gold, fast -> deep red
    t = (steps[boundary] - 15) / 65.0
    t = np.clip(t, 0, 1)
    # Heat mapping: gold -> red -> black
    RGB[boundary, 0] = t
    RGB[boundary, 1] = (1 - t**0.5) * 0.15
    RGB[boundary, 2] = (1 - t) * 0.1
    # Boost brightness for middle range
    bright = np.exp(-t / 0.4)
    RGB[boundary, 0] *= 0.5 + 0.5 * bright
    RGB[boundary, 1] *= 0.3 + 0.7 * bright
    RGB[boundary, 2] *= 0.2 + 0.8 * bright

# Write
fig, ax = plt.subplots(figsize=(6, 6), dpi=200)
ax.imshow(RGB, extent=[-1.5, 1.5, -1.5, 1.5], aspect='auto')
ax.axis('off')
fig.savefig('assets/separatrix.png', dpi=200, bbox_inches='tight', facecolor='black')
plt.close()

conv = (converged >= 0).sum()
total = N * N
print(f"Done: {conv}/{total} converged, {(never_converged.sum())} never converged, {(slow_converged.sum())} slow")
print(f"Boundary density: {boundary.sum()/total*100:.2f}%")
