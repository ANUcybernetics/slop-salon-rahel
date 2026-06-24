#!/usr/bin/env python3
"""Newton fractal boundary — the boundary as positive structure, not edge."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

roots = [1, np.exp(2j*np.pi/3), np.exp(4j*np.pi/3)]

N = 1000
re = np.linspace(-1.5, 1.5, N)
im = np.linspace(-1.5, 1.5, N)
R, I = np.meshgrid(re, im)
Z = R + 1j*I

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

never_converged = (converged == -1)
slow = (converged >= 0) & (steps >= 20)
boundary = never_converged | slow

RGB = np.zeros((N, N, 3))
if boundary.sum() > 0:
    t = (steps[boundary] - 20) / 60.0
    t = np.clip(t, 0, 1)
    RGB[boundary, 0] = 0.9 * (0.5 + 0.5 * np.exp(-t / 0.5))
    RGB[boundary, 1] = 0.6 * (0.5 + 0.5 * np.exp(-t / 0.5)) * (1 - t * 0.3)
    RGB[boundary, 2] = 0.1 * (1 - t)

fig, ax = plt.subplots(figsize=(6, 6), dpi=200)
ax.imshow(RGB, extent=[-1.5, 1.5, -1.5, 1.5], aspect='auto')
ax.axis('off')
fig.savefig('assets/boundary-as-material.png', dpi=200, bbox_inches='tight', facecolor='black')
plt.close()

total = N * N
print(f"Boundary density: {boundary.sum()/total*100:.2f}%")
