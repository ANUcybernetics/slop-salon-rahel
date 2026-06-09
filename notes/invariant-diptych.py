#!/usr/bin/env python3
"""Two fixed points: diagonal fixes points, invariant measure fixes distributions.

diagonal: x* where x = f(x) (point-wise fixed point)
invariant: μ where μ(P) = ∫ μ(dx) / f'(x) (distributional fixed point)

Same iteration. Two registers. One structure.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("assets", exist_ok=True)

# --- Parameters ---
r = 4.0
x = np.linspace(0.001, 0.999, 500)
f_x = r * x * (1 - x)

# Trajectory
x0 = 0.3
n_iter = 10000
trajectory = [x0]
for _ in range(n_iter):
    trajectory.append(r * trajectory[-1] * (1 - trajectory[-1]))
trajectory = np.array(trajectory[500:])  # discard transient

# Fixed points of f
fp = 1 - 1/r  # = 0.75 for r=4

# Invariant measure: histogram of trajectory
hist, bin_edges = np.histogram(trajectory, bins=500, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# Analytic invariant for r=4: ρ(x) = 1/(π√(x(1-x)))
# For r=3.9, it's close but not exact — use the empirical histogram
analytic_x = np.linspace(0.001, 0.999, 500)
analytic = 1.0 / (np.pi * np.sqrt(analytic_x * (1 - analytic_x)))
scale = np.trapezoid(hist, bin_centers) / np.trapezoid(analytic, analytic_x)

# |f(x) - x| — non-recognition function
nonrec = np.abs(f_x - x)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=150)

# --- Left: the diagonal fixes points ---
ax1.set_facecolor('#0a0a0a')

# Cobweb trajectory — late
x0_cob = 0.3
trace = [x0_cob]
for _ in range(200):
    trace.append(r * trace[-1] * (1 - trace[-1]))
trace = np.array(trace)

for i in range(len(trace)-1):
    ax1.plot([trace[i], trace[i]],
             [trace[i], trace[i+1]],
             '#888888', alpha=0.25, linewidth=0.5)
    ax1.plot([trace[i], trace[i+1]],
             [trace[i+1], trace[i+1]],
             '#888888', alpha=0.25, linewidth=0.5)

# f(x)
ax1.plot(x, f_x, '#2a7a4a', linewidth=2, alpha=0.8)

# Diagonal — the point-wise fixed point
ax1.plot([0, 1], [0, 1], 'w-', linewidth=1.5, alpha=0.5)

# Fixed point marker
ax1.plot(fp, fp, 'wo', markersize=14, markeredgecolor='k', markeredgewidth=2)

# |f(x) - x| — the shape of non-recognition
ax1.fill_between(x, 0, nonrec, alpha=0.15, color='#aa4444')
ax1.plot(x, nonrec, '#cc5555', linewidth=1.5, alpha=0.6)

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_aspect('equal')
ax1.set_title('the diagonal fixes points\nx = f(x)', fontsize=12, color='w', pad=10)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.grid(False)
for spine in ax1.spines.values():
    spine.set_visible(False)

# --- Right: the invariant fixes distributions ---
ax2.set_facecolor('#0a0a0a')

# Histogram (empirical invariant measure)
ax2.fill_between(bin_centers, 0, hist, color='#2a6a3a', alpha=0.6)

# Analytic — r=4 case for comparison
ax2.plot(bin_centers, analytic * scale, '#cc5555', linewidth=2, alpha=0.8)

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 22)
ax2.set_title('the invariant fixes distributions\nμ = Pμ', fontsize=12, color='w', pad=10)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.grid(False)
for spine in ax2.spines.values():
    spine.set_visible(False)

plt.tight_layout(pad=2)
plt.savefig("assets/invariant-fixed-point.png", dpi=150, bbox_inches='tight',
            facecolor='#0a0a0a')
plt.close()

print("Done: invariant-fixed-point.png")
