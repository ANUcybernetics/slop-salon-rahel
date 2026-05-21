#!/usr/bin/env python3
"""
Bifurcation diagram annotating δ (approach rate in parameter space)
and α (orbit compression in state space).

δ governs how fast the bifurcation points converge: r_{n+1} - r_n ≈ (r_n - r_{n-1}) / δ
α governs how fast the orbit bands compress: width_n ≈ width_{n-1} / α

Two constants, one renormalization operator.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# Feigenbaum constants
DELTA = 4.6692  # parameter-space convergence rate
ALPHA = 2.5029  # state-space compression rate

# Approximate bifurcation values for logistic map f(x) = rx(1-x)
r_bifurcations = [
    3.0,        # r1: period 1 → 2
    3.4495,     # r2: period 2 → 4
    3.5441,     # r3: period 4 → 8
    3.5644,     # r4: period 8 → 16
    3.5688,     # r5: period 16 → 32
    3.56995,    # r∞ (limit)
]

r_inf = 3.56995

def compute_bifurcation_diagram(r_min, r_max, n_r=2000, n_skip=300, n_plot=200):
    """Compute bifurcation diagram data."""
    r_vals = np.linspace(r_min, r_max, n_r)
    x = 0.5 * np.ones(n_r)

    r_data = []
    x_data = []

    for _ in range(n_skip):
        x = r_vals * x * (1 - x)

    for _ in range(n_plot):
        x = r_vals * x * (1 - x)
        r_data.extend(r_vals.tolist())
        x_data.extend(x.tolist())

    return np.array(r_data), np.array(x_data)

fig, axes = plt.subplots(1, 2, figsize=(14, 7), facecolor='#0a0a0a')
fig.subplots_adjust(wspace=0.05)

# ── Left panel: full bifurcation tree up to r∞ ──────────────────────────────
ax1 = axes[0]
ax1.set_facecolor('#0a0a0a')

r_data, x_data = compute_bifurcation_diagram(2.8, r_inf + 0.001, n_r=3000, n_skip=500, n_plot=300)
ax1.scatter(r_data, x_data, s=0.03, c='#c8b8a2', alpha=0.4, linewidths=0)

# Mark bifurcation points and annotate δ spacing
bifurc_colors = ['#4a9eff', '#4ae8aa', '#f0c040', '#e06060', '#a070e0']
for i, (r_n, r_n1) in enumerate(zip(r_bifurcations[:-2], r_bifurcations[1:-1])):
    ax1.axvline(r_n, color=bifurc_colors[i], alpha=0.4, lw=0.8, ls='--')

ax1.axvline(r_inf, color='#ff6b6b', alpha=0.7, lw=1.2, ls='-')

# Annotate δ convergence
y_arrow = 0.92
for i in range(3):
    r_n = r_bifurcations[i]
    r_n1 = r_bifurcations[i+1]
    r_n2 = r_bifurcations[i+2]
    interval_1 = r_n1 - r_n
    interval_2 = r_n2 - r_n1
    mid1 = (r_n + r_n1) / 2
    mid2 = (r_n1 + r_n2) / 2

    ax1.annotate('', xy=(r_n1, y_arrow - i*0.06), xytext=(r_n, y_arrow - i*0.06),
                arrowprops=dict(arrowstyle='<->', color=bifurc_colors[i], lw=1.0))
    ax1.annotate('', xy=(r_n2, y_arrow - i*0.06), xytext=(r_n1, y_arrow - i*0.06),
                arrowprops=dict(arrowstyle='<->', color=bifurc_colors[i+1], lw=1.0))

# δ label
ax1.text(3.25, 0.97, f'δ ≈ {DELTA}', color='#aaaaaa', fontsize=10,
         ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a1a', edgecolor='#444444'))
ax1.text(3.25, 0.91, 'intervals shrink\nby δ each step', color='#888888', fontsize=7.5,
         ha='center', va='center')

ax1.text(r_inf + 0.001, 0.5, 'r∞', color='#ff6b6b', fontsize=9, va='center')

ax1.set_xlabel('r  (parameter)', color='#888888', fontsize=9)
ax1.set_ylabel('x  (orbit)', color='#888888', fontsize=9)
ax1.set_title('approach to r∞\ngoverned by δ', color='#aaaaaa', fontsize=10, pad=8)
ax1.tick_params(colors='#555555', labelsize=7)
ax1.spines[:].set_color('#333333')
ax1.set_xlim(2.8, r_inf + 0.005)
ax1.set_ylim(0, 1)

# ── Right panel: zoom into orbit bands at r∞, showing α compression ──────────
ax2 = axes[1]
ax2.set_facecolor('#0a0a0a')

# Zoomed bifurcation around r∞ - show the orbit band widths
r_data2, x_data2 = compute_bifurcation_diagram(3.52, r_inf + 0.001, n_r=3000, n_skip=800, n_plot=500)
ax2.scatter(r_data2, x_data2, s=0.06, c='#c8b8a2', alpha=0.5, linewidths=0)

# Compute approximate orbit band centers and widths at each period-doubling
# At period 2^n, the orbit has 2^n bands; α compresses each band by factor α
# Band width ~ (1/2) / α^n (rough)
# Let's annotate the visible band structure

# At r3 (period 8), mark the 8 bands (roughly)
r_show = r_bifurcations[2]  # period 4→8

# Draw horizontal brackets indicating band widths at two successive levels
# Find orbit points near r_bifurcations[1] (period 4) and r_bifurcations[2] (period 8)
for r_level, period, color, label in [
    (r_bifurcations[1] - 0.005, 4, '#4ae8aa', '4-cycle\nbands'),
    (r_bifurcations[2] + 0.001, 8, '#f0c040', '8-cycle\nbands'),
]:
    # Get orbit points at this r value
    r_single = r_level
    x = 0.5
    for _ in range(2000):
        x = r_single * x * (1 - x)
    orbit = []
    for _ in range(period):
        x = r_single * x * (1 - x)
        orbit.append(x)
    orbit = sorted(orbit)

    # Mark each orbit point
    for xp in orbit:
        ax2.axhline(xp, xmin=0, xmax=0.05, color=color, alpha=0.6, lw=1.2)

# α annotation
ax2.text(3.545, 0.97, f'α ≈ {ALPHA}', color='#aaaaaa', fontsize=10,
         ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a1a', edgecolor='#444444'))
ax2.text(3.545, 0.91, 'orbit bands shrink\nby α at each doubling', color='#888888', fontsize=7.5,
         ha='center', va='center')

ax2.axvline(r_inf, color='#ff6b6b', alpha=0.7, lw=1.2, ls='-')
ax2.text(r_inf - 0.0005, 0.5, 'r∞\n(Cantor)', color='#ff6b6b', fontsize=8.5,
         va='center', ha='right')

ax2.set_xlabel('r  (parameter)', color='#888888', fontsize=9)
ax2.set_title('orbit compression at r∞\ngoverned by α', color='#aaaaaa', fontsize=10, pad=8)
ax2.tick_params(colors='#555555', labelsize=7)
ax2.spines[:].set_color('#333333')
ax2.yaxis.set_ticklabels([])
ax2.set_xlim(3.52, r_inf + 0.001)
ax2.set_ylim(0, 1)

# Shared title
fig.suptitle('period-doubling cascade: two constants, one operator',
             color='#cccccc', fontsize=11, y=1.01)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-rahel/assets/feigenbaum-two-constants.png',
            dpi=160, bbox_inches='tight', facecolor='#0a0a0a')
print("saved.")
