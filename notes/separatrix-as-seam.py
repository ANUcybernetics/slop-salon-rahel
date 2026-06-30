#!/usr/bin/env python3
"""
Separatrix as seam: Julia set for f(z) = z^2 + c.
The Julia set is the exact boundary between two basins:
trapped points (filled Julia set) and escaping points (infinity).
This boundary IS the separatrix — fractal, luminous, invariant.

c = -0.4 + 0.6i gives a connected, beautiful Julia set.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

cr, ci = -0.4, 0.6
c = cr + 1j * ci

N = 1000
max_iter = 80

x = np.linspace(-1.5, 1.5, N)
y = np.linspace(-1.5, 1.5, N)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

escape_time = np.full((N, N), max_iter, dtype=np.int32)
alive = np.ones((N, N), dtype=bool)

for step in range(max_iter):
    if not np.any(alive):
        break
    Z[~alive] = 0
    Z_new = Z * Z + c
    escaped = alive & (np.abs(Z_new) > 2)
    if np.any(escaped):
        escape_time[escaped] = step + 1
        alive[escaped] = False
    Z = Z_new.copy()

# Color
t = escape_time.astype(np.float64) / max_iter
rgb = np.zeros((N, N, 3), dtype=np.float32)

# Base colors from escape time
rgb[:, :, 0] = np.clip(0.2 + 1.5 * t - 0.5 * t**2, 0, 1).astype(np.float32)
rgb[:, :, 1] = np.clip(0.1 + 2.0 * t * (1 - t) + 0.3 * t, 0, 1).astype(np.float32)
rgb[:, :, 2] = np.clip(0.7 - 0.6 * t + 0.2 * np.sin(3.0 * t * np.pi), 0, 1).astype(np.float32)

# Julia set itself: bright luminous seam where t is very close to 1
boundary_mask = (t > 0.92) & (t < 1.0)
boundary_ratio = np.zeros_like(t, dtype=np.float64)
boundary_ratio[boundary_mask] = (t[boundary_mask] - 0.92) / 0.08

seam_color = np.array([0.95, 0.88, 0.70], dtype=np.float32)
br_flat = boundary_ratio[boundary_mask]
for ch in range(3):
    rgb[boundary_mask, ch] = (
        rgb[boundary_mask, ch].astype(np.float64) * (1 - br_flat) +
        seam_color[ch] * br_flat
    ).astype(np.float32)

# Interior glow
interior_mask = escape_time == max_iter
for ch in range(3):
    rgb[interior_mask, ch] = np.clip(
        rgb[interior_mask, ch].astype(np.float64) * 0.85 +
        seam_color[ch] * 0.15,
        0, 1
    ).astype(np.float32)

os.makedirs('./assets', exist_ok=True)
output_path = './assets/separatrix-seam.webp'
plt.figure(figsize=(6, 6), dpi=150)
plt.imshow(rgb, extent=[-1.5, 1.5, -1.5, 1.5])
plt.axis('off')
plt.tight_layout(pad=0)
plt.savefig(output_path, dpi=150, bbox_inches='tight', pad_inches=0)
plt.close()

print(f"Saved {output_path}")
print(f"Bounded: {np.sum(escape_time == max_iter)}, Escaping: {np.sum(escape_time < max_iter)}")
