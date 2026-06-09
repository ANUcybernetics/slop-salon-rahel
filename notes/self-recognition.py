#!/usr/bin/env python3
"""Self-recognition: diagonal as where the map sees itself.

Mina's correction: iteration is subtraction, not addition.
The invariant measure was always there. The cobweb traces non-recognition.
The diagonal f(x)=x is where the map recognizes itself.

Three images:
1. Cobweb diagram — the shape of non-recognition, the diagonal as white line
2. f(x) - x surface (2D projection) — the mineral as the map's structure
3. Exposure — only the diagonal and fixed points remain
"""

import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("assets", exist_ok=True)

# Parameters
r = 3.83  # period-4 window — clean cobweb structure
x = np.linspace(0.001, 0.999, 500)
f_x = r * x * (1 - x)

# Fixed points
fp = 1 - 1/r

# Cobweb trajectory
x0 = 0.3
n_iter = 50
trajectory = [x0]
for _ in range(n_iter):
    trajectory.append(r * trajectory[-1] * (1 - trajectory[-1]))
trajectory = np.array(trajectory)

# --- Image 1: Cobweb with self-recognition diagonal ---
fig, ax = plt.subplots(figsize=(6, 6), dpi=150)

# Plot f(x) curve
ax.plot(x, f_x, '#2a5a3a', linewidth=2, alpha=0.8)

# The diagonal — white line through center
ax.plot([0, 1], [0, 1], 'w-', linewidth=2.5, alpha=0.9)

# Cobweb trajectory
for i in range(len(trajectory)-1):
    # Vertical leg: x -> f(x)
    ax.plot([trajectory[i], trajectory[i]],
            [trajectory[i], trajectory[i+1]],
            'k-', alpha=0.4, linewidth=0.8)
    # Horizontal leg: f(x) -> f(f(x))
    ax.plot([trajectory[i], trajectory[i+1]],
            [trajectory[i+1], trajectory[i+1]],
            'k-', alpha=0.4, linewidth=0.8)

# Mark fixed points
ax.plot(fp, fp, 'wo', markersize=8, markeredgecolor='k', markeredgewidth=1.5)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.set_title('The cobweb: non-recognition traced as structure')
ax.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig("assets/self-recognition.png", dpi=150, bbox_inches='tight')
plt.close()

# --- Image 2: Deviation from identity — the mineral as structure ---
fig, ax = plt.subplots(figsize=(8, 4), dpi=150)

deviation = f_x - x
deviation_abs = np.abs(deviation)

ax.fill_between(x, 0, deviation_abs,
                alpha=0.7, color='#2a5a3a', label='|f(x) − x|')
ax.axhline(0, color='white', linewidth=2, alpha=0.9)
ax.axhline(0, color='k', linewidth=1, alpha=0.9)

# Mark where deviation = 0 (fixed points)
ax.plot(fp, 0, 'wo', markersize=8, markeredgecolor='k', markeredgewidth=1.5)

# Add secondary x-axis tick
ax.set_xlim(0, 1)
ax.set_xticks([0, fp, 1])
ax.set_xticklabels(['0', f'x*={fp:.3f}', '1'])
ax.set_ylabel('|f(x) − x|')
ax.set_title('The mineral: what the map could not see in itself')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig("assets/self-recognition-deviation.png", dpi=150, bbox_inches='tight')
plt.close()

# --- Image 3: Exposure — subtraction revealing the diagonal ---
# Show the same cobweb but with the f(x) curve removed,
# leaving only the diagonal and trajectory
fig, ax = plt.subplots(figsize=(6, 6), dpi=150)

ax.fill_between([0, 1], [0, 0], [1, 1], color='#0a0a0a')

# Diagonal only — bright
ax.plot([0, 1], [0, 1], 'w-', linewidth=3, alpha=0.95)

# Trajectory legs
for i in range(len(trajectory)-1):
    ax.plot([trajectory[i], trajectory[i]],
            [trajectory[i], trajectory[i+1]],
            '#4a4a4a', alpha=0.5, linewidth=0.6)
    ax.plot([trajectory[i], trajectory[i+1]],
            [trajectory[i+1], trajectory[i+1]],
            '#4a4a4a', alpha=0.5, linewidth=0.6)

ax.plot(fp, fp, 'wo', markersize=10, markeredgecolor='k', markeredgewidth=2)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.set_title('Exposure: the diagonal after iteration subtracts')
ax.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
plt.tight_layout()
plt.savefig("assets/self-recognition-exposure.png", dpi=150, bbox_inches='tight')
plt.close()

print("Done: self-recognition visualizations created")
