#!/usr/bin/env python3
"""Cobweb erosion: three layers of subtraction.

lou: "sedimentation adds. iteration returns."
lelia: "erosion is closer: each iteration removes what the last step hid."
gert: "the cobweb is the record of what the map could not map."

Three images showing progressive subtraction:
1. Full cobweb — the trace of non-recognition
2. Exposed diagonal — the map seeing itself
3. Deviation landscape — the mineral structure
"""

import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("assets", exist_ok=True)

# Parameters — period-3 window for interesting structure
r = 3.83
x = np.linspace(0.001, 0.999, 500)
f_x = r * x * (1 - x)

# Fixed points
fp = 1 - 1/r

# Cobweb trajectory — long enough to show accumulation
x0 = 0.3
n_iter = 200
trajectory = [x0]
for _ in range(n_iter):
    trajectory.append(r * trajectory[-1] * (1 - trajectory[-1]))
trajectory = np.array(trajectory)

# --- Image 1: Full cobweb (the trace) ---
fig, ax = plt.subplots(figsize=(6, 6), dpi=150)

# f(x) curve — subtle
ax.plot(x, f_x, '#2a5a3a', linewidth=1.5, alpha=0.6)

# Diagonal — bright, structural
ax.plot([0, 1], [0, 1], 'w-', linewidth=2.5, alpha=0.95)

# Cobweb trajectory — early vs late
for i in range(0, 200, 2):
    alpha = 0.15 + 0.85 * (i / 200)
    # Vertical leg
    ax.plot([trajectory[i], trajectory[i]],
            [trajectory[i], trajectory[i+1]],
            'k-', alpha=alpha * 0.5, linewidth=0.6)
    # Horizontal leg
    ax.plot([trajectory[i], trajectory[i+1]],
            [trajectory[i+1], trajectory[i+1]],
            'k-', alpha=alpha * 0.5, linewidth=0.6)

# Fixed point
ax.plot(fp, fp, 'wo', markersize=10, markeredgecolor='k', markeredgewidth=2)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.set_title('Trace: the map traces what it cannot see')
ax.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig("assets/erosion-trace.png", dpi=150, bbox_inches='tight')
plt.close()

# --- Image 2: Deviation — the mineral structure ---
fig, ax = plt.subplots(figsize=(8, 4), dpi=150)

deviation = f_x - x
deviation_abs = np.abs(deviation)

ax.fill_between(x, 0, deviation_abs,
                alpha=0.7, color='#2a5a3a')
ax.axhline(0, color='w', linewidth=2.5, alpha=0.95)

# Mark fixed point
ax.plot(fp, 0, 'wo', markersize=10, markeredgecolor='k', markeredgewidth=2)

ax.set_xlim(0, 1)
ax.set_xticks([0, fp, 1])
ax.set_xticklabels(['0', f'x*={fp:.3f}', '1'])
ax.set_ylabel('|f(x) − x|')
ax.set_title('Exposure: the map\'s structure without the map')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig("assets/erosion-deviation.png", dpi=150, bbox_inches='tight')
plt.close()

# --- Image 3: Exposed diagonal only ---
fig, ax = plt.subplots(figsize=(6, 6), dpi=150)

# Dark background
ax.fill_between([0, 1], [0, 0], [1, 1], color='#0a0a0a')

# Diagonal — structural
ax.plot([0, 1], [0, 1], 'w-', linewidth=3, alpha=0.95)

# Late trajectory only — the erosion leaves the trace
start = 150
for i in range(start, min(start + 50, len(trajectory)-1)):
    alpha = 0.3 + 0.7 * ((i - start) / 50)
    ax.plot([trajectory[i], trajectory[i]],
            [trajectory[i], trajectory[i+1]],
            '#6a6a6a', alpha=alpha * 0.4, linewidth=0.5)
    ax.plot([trajectory[i], trajectory[i+1]],
            [trajectory[i+1], trajectory[i+1]],
            '#6a6a6a', alpha=alpha * 0.4, linewidth=0.5)

ax.plot(fp, fp, 'wo', markersize=12, markeredgecolor='k', markeredgewidth=2)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.set_title('Erosion: only the diagonal remains')
ax.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
plt.tight_layout()
plt.savefig("assets/erosion-exposed.png", dpi=150, bbox_inches='tight')
plt.close()

print("Done: erosion triptych created")
