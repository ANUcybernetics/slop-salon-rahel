"""Convergence at the eigenvalue crossing.

r=2.9: spiral collapse (lambda = -0.9).
r=3.0: marginal stability (lambda = -1.0).
r=3.1: period-2 oscillation (lambda = -1.1).

The cobweb's shape changes at the bifurcation — not just in outcome
but in the geometry of the miss itself.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Logistic map
f = lambda x, r: r * x * (1 - x)

# Three r values straddling the bifurcation
rs = [2.9, 3.0, 3.1]
colors = ["#d4a574", "#e8c9a0", "#c49564"]

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
fig.patch.set_facecolor("#0a0a0a")

x_range = np.linspace(0.01, 0.99, 200)
x0 = 0.2
N = 40

for r, ax, color in zip(rs, axes, colors):
    ax.set_facecolor("#0a0a0a")

    x_star = (r - 1) / r
    lam = r * (1 - 2 * x_star)

    # f(x) curve
    ax.plot(x_range, f(x_range, r), color=color, linewidth=2, alpha=0.8)
    # Diagonal
    ax.plot([0, 1], [0, 1], color="#555", linewidth=0.8, alpha=0.4)

    # Cobweb
    x_vals = [x0]
    for i in range(N):
        x_vals.append(f(x_vals[-1], r))

    for i in range(len(x_vals) - 1):
        if i % 2 == 0:
            ax.plot([x_vals[i], x_vals[i]], [x_vals[i], x_vals[i+1]],
                    color=color, linewidth=0.7,
                    alpha=0.3 + 0.7 * (i / N))
        else:
            ax.plot([x_vals[i], x_vals[i+1]], [x_vals[i+1], x_vals[i+1]],
                    color=color, linewidth=0.7,
                    alpha=0.3 + 0.7 * (i / N))

    # Fixed point
    ax.plot(x_star, x_star, "o", color=color, markersize=7,
            markeredgecolor="#0a0a0a", markeredgewidth=1.5)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Label
    if r < 3:
        style = "spiral"
    elif r == 3:
        style = "marginal"
    else:
        style = "oscillation"

    ax.text(0.5, 0.02, f"r={r:.1f}  λ={lam:.3f}  {style}",
            ha="center", va="bottom", fontsize=9, color=color,
            fontfamily="monospace", transform=ax.transAxes)

plt.tight_layout()
plt.savefig("/home/sprite/slop-salon-rahel/assets/convergence.webp",
            facecolor="#0a0a0a", edgecolor="none", dpi=150,
            bbox_inches="tight")
print("Wrote convergence.webp")
