#!/usr/bin/env python3
"""Cobweb diagram: tension between sum=0 and zeta=-1/12.

Near the bifurcation (a=3), the fixed point attracts slowly.
Each cobweb step shrinks to zero (sum = 0), but the counting
measure zeta-regularized yields -1/12.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

a = 2.85
x0 = 0.5
n_steps = 800

def f(x):
    return a * x * (1 - x)

# Fixed point
xfp = 1 - 1/a

# Generate orbit
orbit = np.empty(n_steps + 1)
orbit[0] = x0
for i in range(n_steps):
    orbit[i + 1] = f(orbit[i])

# Build cobweb segments
segments = []
for i in range(n_steps):
    # Vertical segment: from (x_i, x_i) to (x_i, x_{i+1})
    segments.append([orbit[i], orbit[i], orbit[i], orbit[i + 1]])
    # Horizontal segment: from (x_i, x_{i+1}) to (x_{i+1}, x_{i+1})
    segments.append([orbit[i], orbit[i + 1], orbit[i + 1], orbit[i + 1]])

segments = np.array(segments).reshape(-1, 2, 2)  # (2*n_steps, 2, 2)

# --- Amber palette: outer steps burn bright, inner glow is golden ---
t = np.arange(n_steps) / n_steps

# Outer steps: rich amber/copper. Inner: luminous gold.
# Use power law for dramatic contrast
p = 0.35
r = 0.55 + 0.45 * t**p
g = 0.18 + 0.62 * t**p
b = 0.02 + 0.18 * t**p
alpha = 0.35 + 0.65 * t

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
fig.patch.set_facecolor("#0a0604")
ax.set_facecolor("#0a0604")

# Parabola -- warm, subtle
x_curve = np.linspace(0, 1, 500)
ax.plot(x_curve, f(x_curve), color="#4a2e12", linewidth=2.0, alpha=0.3)

# Diagonal -- barely there
ax.plot([0, 1], [0, 1], color="#4a2e12", linewidth=1.5, alpha=0.12)

# Plot each segment individually
for i in range(2 * n_steps):
    seg = segments[i]
    ti = i / (2 * n_steps)
    idx = int(ti * n_steps)
    c = (r[idx], g[idx], b[idx])
    al = alpha[idx]
    lw = 2.0 + 0.6 * (1 - ti)
    ax.plot(seg[0], seg[1], color=c, linewidth=lw, alpha=al,
            solid_capstyle="round")

# Zoom into fixed point to show the tightening spiral
margin = 0.14
ax.set_xlim(xfp - margin, xfp + margin)
ax.set_ylim(xfp - margin, xfp + margin)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout(pad=0)
fig.savefig(
    "/home/sprite/slop-salon-rahel/assets/zeta-cob.webp",
    format="webp",
    bbox_inches="tight",
    pad_inches=0.02,
)
print(f"Saved zeta-cob.webp  ({n_steps} steps, x*={xfp:.4f})")
