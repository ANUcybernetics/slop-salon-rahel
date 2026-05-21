#!/usr/bin/env python3
"""Two periodic windows side by side.

The main cascade (period-1 → period-2 → ...) and the period-3 window,
each showing bifurcation diagram above and Lyapunov exponent below.

The same fold structure at two scales. Lou's observation: "each zero in
the staircase is a fold." The zeros are periodic windows; the rises are
cascades. Each cascade is the same fold repeated."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def compute_lyap(rs, n_burn=500, n_iter=1000):
    lyaps = np.zeros(len(rs))
    for i, r in enumerate(rs):
        x = 0.3
        lam = 0.0
        for j in range(n_burn + n_iter):
            x = r * x * (1 - x)
            if x <= 0 or x >= 1:
                lyaps[i] = np.nan
                break
            dx = abs(2 * r * x - r)
            if dx > 1e-15:
                lam += np.log(dx)
        else:
            lyaps[i] = lam / (n_burn + n_iter)
    return lyaps

def plot_bifurcation(ax, rs, color='#e8c170', alpha=0.25, n_burn=500):
    for r in rs[::8]:
        x = 0.3
        for _ in range(n_burn):
            x = r * x * (1 - x)
        xs = []
        for _ in range(200):
            x = r * x * (1 - x)
            xs.append(x)
        ax.plot([r] * len(xs), xs, '.', color=color, alpha=alpha,
                 markersize=0.3, rasterized=True)

# Figure
fig, axes = plt.subplots(2, 2, figsize=(12, 9),
                         gridspec_kw={'height_ratios': [1, 0.5],
                                      'hspace': 0.08, 'wspace': 0.2})
fig.patch.set_facecolor('#0a0a0f')

# --- Main cascade ---
r1 = np.linspace(3.0, 3.6, 600)
l1 = compute_lyap(r1)

ax_bif1 = axes[0, 0]
ax_bif1.set_facecolor('#0a0a0f')
plot_bifurcation(ax_bif1, r1, color='#e8c170')
for rv, lb in zip([3.0, 3.449, 3.544, 3.564, 3.5699],
                   ['P1', 'P2', 'P4', 'P8', 'r∞']):
    ax_bif1.axvline(rv, color='#5566aa', alpha=0.25, linewidth=0.5)
    ax_bif1.text(rv + 0.003, 0.05, lb, color='#5566aa', fontsize=7, alpha=0.6)
ax_bif1.set_xlim(3.0, 3.6)
ax_bif1.set_ylim(0, 1)
ax_bif1.set_title('Main Cascade', color='#ccc', fontsize=11, pad=10)
ax_bif1.tick_params(colors='#666', labelsize=8)
for s in ax_bif1.spines.values(): s.set_color('#333')

ax_lyap1 = axes[1, 0]
ax_lyap1.set_facecolor('#0a0a0f')
from scipy.ndimage import median_filter
l1s = median_filter(l1, size=3)
ax_lyap1.plot(r1, l1s, color='#e8c170', linewidth=0.6, alpha=0.7)
ax_lyap1.axhline(0, color='#5566aa', alpha=0.2, linewidth=0.5)
for rv in [3.0, 3.449, 3.544, 3.564, 3.5699]:
    ax_lyap1.axvline(rv, color='#5566aa', alpha=0.15, linewidth=0.5)
ax_lyap1.set_xlim(3.0, 3.6)
ax_lyap1.set_xlabel('r', color='#888', fontsize=9)
ax_lyap1.tick_params(colors='#666', labelsize=8)
for s in ax_lyap1.spines.values(): s.set_color('#333')

# --- Period-3 window ---
r2 = np.linspace(3.8284, 3.99, 600)
l2 = compute_lyap(r2)

ax_bif2 = axes[0, 1]
ax_bif2.set_facecolor('#0a0a0f')
plot_bifurcation(ax_bif2, r2, color='#aa6644')
ax_bif2.set_xlim(3.8284, 3.99)
ax_bif2.set_ylim(0, 1)
ax_bif2.set_title('Period-3 Window', color='#ccc', fontsize=11, pad=10)
ax_bif2.tick_params(colors='#666', labelsize=8)
for s in ax_bif2.spines.values(): s.set_color('#333')

ax_lyap2 = axes[1, 1]
ax_lyap2.set_facecolor('#0a0a0f')
l2s = median_filter(l2, size=3)
ax_lyap2.plot(r2, l2s, color='#aa6644', linewidth=0.6, alpha=0.7)
ax_lyap2.axhline(0, color='#aa6644', alpha=0.2, linewidth=0.5)
ax_lyap2.set_xlim(3.8284, 3.99)
ax_lyap2.set_xlabel('r', color='#888', fontsize=9)
ax_lyap2.tick_params(colors='#666', labelsize=8)
for s in ax_lyap2.spines.values(): s.set_color('#333')

plt.savefig('assets/periodic-windows.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
print("Saved assets/periodic-windows.png")
