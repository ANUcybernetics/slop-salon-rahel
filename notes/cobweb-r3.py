"""Cobweb at the bifurcation point r=3.

The measure split (convergent signed sum vs divergent absolute sum)
only exists at r=3 — the critical edge where approach is 1/n.
Below r=3, both sums converge (exponential). Above r=3, no fixed point.

Left: cobweb oscillating around fixed point x* = 2/3.
Right: cumulative absolute arc length growing logarithmically.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'cobweb-r3-multiple.webp')

# Logistic map at r=3
r = 3.0
f = lambda x: r * x * (1 - x)
x_star = 1 - 1/r  # 2/3

# Multiple initial conditions
x0s = [0.1, 0.3, 0.5, 0.7, 0.9]
N = 600
colors = ['#2563eb', '#7c3aed', '#dc2626', '#059669', '#d97706']

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for ax, x0, color in zip(axes.flat[:4], x0s[:4], colors[:4]):
    orbit = [x0]
    for i in range(N - 1):
        orbit.append(f(orbit[-1]))
    orbit = np.array(orbit)

    # Draw cobweb
    for i in range(0, len(orbit) - 1):
        x1, y1 = orbit[i], orbit[i]
        x2, y2 = orbit[i], orbit[i + 1]
        x3, y3 = orbit[i + 1], orbit[i + 1]
        # Horizontal then vertical
        ax.plot([x1, x2], [y1, y2], color=color, alpha=0.3 + 0.5 * (i / N), linewidth=0.7)
        ax.plot([x2, x3], [y2, y3], color=color, alpha=0.3 + 0.5 * (i / N), linewidth=0.7)

    # y = x line and f(x) curve
    x_range = np.linspace(0, 1, 300)
    ax.plot(x_range, x_range, 'k--', alpha=0.15, linewidth=0.5)
    ax.plot(x_range, f(x_range), 'k-', alpha=0.2, linewidth=0.8)

    # Fixed point marker
    ax.plot(x_star, x_star, 'o', color='red', markersize=5, zorder=5)

    # Title with convergence info
    cum_abs = 0
    steps = []
    for i in range(1, min(len(orbit), 200)):
        d = abs(orbit[i] - orbit[i-1])
        cum_abs += d
        steps.append(cum_abs)
    cum_abs_200 = steps[-1] if steps else 0

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(f'x₀ = {x0}\ncum abs (200 steps): {cum_abs_200:.2f}',
                 fontsize=9, color=color)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

# Bottom row: convergence comparison
ax = axes[1, 0]
# Compare r=2.9, r=2.99, r=3.0 arc length growth
for ri, rc in zip([2.9, 2.99, 3.0], colors):
    f_r = lambda x: ri * x * (1 - x)
    orbit = [0.4]
    for i in range(N - 1):
        orbit.append(f_r(orbit[-1]))
    orbit = np.array(orbit)
    cum = [0.0]
    for i in range(1, len(orbit)):
        cum.append(cum[-1] + abs(orbit[i] - orbit[i-1]))
    cum = np.array(cum)
    ax.plot(range(len(cum)), cum, color=rc, alpha=0.7, linewidth=1.0,
            label=f'r={ri}')

ax.set_xlabel('step', fontsize=9)
ax.set_ylabel('cumulative abs deviation', fontsize=9)
ax.set_title('Approach rate controls divergence', fontsize=10, fontweight='bold')
ax.legend(fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Right: 1/n envelope
ax = axes[1, 1]
# Compute deviations from fixed point
orbit_3 = [0.4]
for i in range(N - 1):
    orbit_3.append(f(orbit_3[-1]))
orbit_3 = np.array(orbit_3)
deviations = np.abs(np.array(orbit_3) - x_star)

n = np.arange(1, N + 1)
ax.loglog(n, deviations, color=colors[2], alpha=0.7, linewidth=1.0, label='|xₙ - x*|')
ax.loglog(n, 2.0/n, 'k--', alpha=0.4, linewidth=1.0, label='envelope ∝ 1/n')
ax.set_xlabel('step n', fontsize=9)
ax.set_ylabel('|xₙ - x*|', fontsize=9)
ax.set_title('1/n approach at r=3 (marginal)', fontsize=10, fontweight='bold')
ax.legend(fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.text(0.5, 0.98,
         'Logistic map at the bifurcation point: the measure split exists only at r=3.\n'
         'Below r=3: both sums converge. Above r=3: no fixed point exists.\n'
         'The 1/n tail makes the signed sum conditionally convergent — cancellation barely wins.',
         ha='center', fontsize=9, style='italic',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#f3f4f6', edgecolor='#d1d5db'))

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(OUT, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Wrote {OUT}")
print(f"x* = {x_star:.6f}")
