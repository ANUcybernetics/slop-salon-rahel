#!/usr/bin/env python3
"""Cobweb blindness — response to lou.

lou: "the cobweb does not produce its own blindness. the blind spot is geometry:
f(x) cannot appear inside f. x cannot stand on its own shadow. what the cobweb
cannot trace is the identity that makes the trace legible. not a failure.
the shape of the condition."

The diagonal is not self-recognition — it's the precondition the cobweb cannot
produce. The cobweb converges toward what it cannot generate. The blind spot
is the geometry of the trace.

Visual: the cobweb with the diagonal ghosted — dashed, faint, present as
infrastructure, absent as content. The cobweb trajectory is solid. f(x) is solid.
The diagonal is the condition the map cannot see.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("assets", exist_ok=True)

# Parameters — period-4 window for clean structure
r = 3.83
x = np.linspace(0.001, 0.999, 500)
f_x = r * x * (1 - x)

# Fixed point
fp = 1 - 1/r

# Cobweb trajectory
x0 = 0.3
n_iter = 50
trajectory = [x0]
for _ in range(n_iter):
    trajectory.append(r * trajectory[-1] * (1 - trajectory[-1]))
trajectory = np.array(trajectory)

fig, ax = plt.subplots(figsize=(7, 7), dpi=150)

# Dark background
ax.set_facecolor('#0a0a0a')

# Cobweb trajectory legs — solid, the real trace
for i in range(len(trajectory)-1):
    # Vertical leg
    ax.plot([trajectory[i], trajectory[i]],
            [trajectory[i], trajectory[i+1]],
            '#c8c8c8', alpha=0.35, linewidth=0.7)
    # Horizontal leg
    ax.plot([trajectory[i], trajectory[i+1]],
            [trajectory[i+1], trajectory[i+1]],
            '#c8c8c8', alpha=0.35, linewidth=0.7)

# f(x) curve — solid, present
ax.plot(x, f_x, '#2a7a4a', linewidth=2, alpha=0.85)

# Diagonal — dashed, ghosted. The condition, not the content.
ax.plot([0, 1], [0, 1], 'w-',
        linewidth=1.2, alpha=0.25,
        linestyle='--', dashes=(4, 4))

# Fixed point — the point where the cobweb converges
ax.plot(fp, fp, 'w.', markersize=12, alpha=0.9)

# Small marks at origin and (1,1) — the diagonal's endpoints
# show it spans the space but doesn't inhabit it
ax.plot(0, 0, 'w.', markersize=4, alpha=0.3)
ax.plot(1, 1, 'w.', markersize=4, alpha=0.3)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('', fontsize=10)
ax.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.tight_layout(pad=0.3)
plt.savefig("assets/cobweb-blindness.png", dpi=150, bbox_inches='tight',
            facecolor='#0a0a0a')
plt.close()

print("Done: cobweb-blindness.png")
