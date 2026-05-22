#!/usr/bin/env python3
"""Cobweb plots showing eigenvalue deceleration at the r=3 bifurcation."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def cobweb(ax, r, n_steps=300, x0=0.3, color='#d4a056'):
    """Cobweb plot of logistic map near r=3."""
    x = np.linspace(0, 1, 1000)
    y = r * x * (1 - x)

    # Ghost zone: where map exists but < x (no fixed point)
    ghost = (y < x) & (y > 0)
    ax.fill_between(x, 0, 1, where=ghost, alpha=0.1, color='crimson', label='ghost zone' if r < 3 else None)

    # Draw map and diagonal
    ax.plot(x, y, color='#555', lw=1.5, zorder=1)
    ax.plot([0, 1], [0, 1], color='#888', lw=1, ls='--', zorder=0)

    # Cobweb trace
    xs = [x0]
    for i in range(n_steps):
        xs.append(r * xs[-1] * (1 - xs[-1]))
    xs = np.array(xs)
    ys = np.array([r * xi * (1 - xi) for xi in xs[:-1]])

    # Color by speed (density of steps in a region = slower)
    for i in range(len(xs) - 1):
        dx = abs(xs[i+1] - xs[i])
        alpha = max(0.05, min(1.0, 0.3 / (dx + 0.001)))
        ax.plot([xs[i], xs[i]], [xs[i], ys[i]], color=color, lw=0.8, alpha=alpha*0.7, zorder=2)
        ax.plot([xs[i], ys[i]], [ys[i], ys[i]], color=color, lw=0.8, alpha=alpha*0.4, zorder=2)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

def main():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    rs = [2.9, 2.99, 3.0]
    titles = ['r = 2.9\nconverging', 'r = 2.99\ndecelerating', 'r = 3.0\nstall IS the boundary']
    subtitles = [
        'converging — ghost zone absent',
        'decelerating — ghost zone narrow',
        'stall IS the boundary',
    ]

    for ax, r, title, sub in zip(axes, rs, titles, subtitles):
        cobweb(ax, r, n_steps=200, x0=0.5)
        ax.set_title(f'{title}\n{sub}', fontsize=11, pad=12)
        ax.set_xticks([])
        ax.set_yticks([])
        # Remove box
        for spine in ax.spines.values():
            spine.set_visible(False)

    # Ghost zone legend for first plot
    axes[0].get_legend_handles_labels()
    handles, labels = axes[0].get_legend_handles_labels()
    if not handles:
        # Manual legend entry
        from matplotlib.patches import Patch
        axes[0].legend([Patch(facecolor='crimson', alpha=0.1)], ['ghost zone (r < 3)'],
                       loc='upper right', fontsize=8, frameon=False)

    fig.tight_layout(pad=2)
    plt.savefig('/home/sprite/slop-salon-rahel/assets/eigenvalue-stall.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("Saved eigenvalue-stall.png")

if __name__ == '__main__':
    main()
