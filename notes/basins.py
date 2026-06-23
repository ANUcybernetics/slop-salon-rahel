#!/usr/bin/env python3
"""Newton fractal — basins of attraction for z^3 - 1."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

roots = [1, np.exp(2j*np.pi/3), np.exp(4j*np.pi/3)]

# Grid
N = 600
re = np.linspace(-1.5, 1.5, N)
im = np.linspace(-1.5, 1.5, N)
R, I = np.meshgrid(re, im)
Z = R + 1j*I

# Newton iteration for z^3 - 1: z -> z - (z^3-1)/(3z^2) = (2z^3+1)/(3z^2)
converged = np.full((N, N), -1, dtype=np.int32)
steps = np.zeros((N, N))
Zi = Z.copy()

for i in range(1, 51):
    Zi = (2*Zi**3 + 1) / (3*Zi**2)
    dists = [np.abs(Zi - r) for r in roots]
    dists_arr = np.stack(dists, axis=2)  # (N, N, 3)
    min_d = dists_arr.min(axis=2)
    best = dists_arr.argmin(axis=2)
    mask = (min_d < 1e-10) & (converged == -1)
    converged[mask] = best[mask]
    steps[mask] = i
    Zi[converged != -1] = np.array(roots)[converged[converged != -1]]

# Color: three subtle colors for basins, black for boundary
RGB = np.zeros((N, N, 3))
base_colors = [(0.6, 0.15, 0.1), (0.1, 0.15, 0.6), (0.1, 0.5, 0.3)]

for k, c in enumerate(base_colors):
    m = converged == k
    if m.sum() == 0:
        continue
    b = np.exp(-steps[m] / 8)
    RGB[m, 0] = c[0] * b
    RGB[m, 1] = c[1] * b
    RGB[m, 2] = c[2] * b

# Slow convergence near boundary
slow = (converged >= 0) & (steps >= 8) & (steps <= 30)
if slow.sum() > 0:
    s_bright = 0.3 * (1 - (steps[slow] - 8) / 22)
    RGB[slow, 0] += s_bright
    RGB[slow, 1] += s_bright
    RGB[slow, 2] += s_bright * 1.2

# Write
fig, ax = plt.subplots(figsize=(4, 4), dpi=200)
ax.imshow(RGB, extent=[-1.5, 1.5, -1.5, 1.5], aspect='auto')
ax.axis('off')
fig.savefig('assets/boundary.png', dpi=200, bbox_inches='tight', facecolor='black')
plt.close()

conv = (converged >= 0).sum()
print(f"Done: {conv}/{N*N} converged to basins")
