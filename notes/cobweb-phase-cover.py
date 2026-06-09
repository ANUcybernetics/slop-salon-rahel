#!/usr/bin/env python3
"""Cover image for cobweb phase transition audio piece."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as Gridspec
import numpy as np

fig = plt.figure(figsize=(12, 10), dpi=100)
gs = Gridspec.GridSpec(3, 1, hspace=0.4, height_ratios=[1, 1, 0.3])

colors = ['#4a9e4a', '#c4a435', '#c44a3a']  # green (order), amber (period-4), red (chaos)
r_values = [3.2, 3.5, 3.9]
labels = ['r = 3.2 · period-2', 'r = 3.5 · period-4', 'r = 3.9 · chaotic']

for idx, (r, label, color) in enumerate(zip(r_values, labels, colors)):
    ax = plt.subplot(gs[idx])

    # Cobweb plot
    x = 0.3
    N = 400
    xs = [x]
    for i in range(N):
        x = r * x * (1 - x)
        xs.append(x)

    # Draw cobweb
    for i in range(0, len(xs) - 1, 1):
        # Vertical: x → f(x)
        ax.plot([xs[i], xs[i]], [xs[i], xs[i+1]], color=color, alpha=0.15, linewidth=0.5)
        # Horizontal: f(x) → f(x) (diagonal copy)
        ax.plot([xs[i], xs[i+1]], [xs[i+1], xs[i+1]], color=color, alpha=0.15, linewidth=0.5)

    # Diagonal f(x) = x
    ax.plot([0, 1], [0, 1], 'k-', linewidth=0.5, alpha=0.3)

    # Plot trajectory values
    ax.plot(xs, 'w-', alpha=0.3, linewidth=0.3)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(label, fontsize=12, fontweight='bold', color=color, pad=15)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

# Bottom: simple phase label
ax_bottom = plt.subplot(gs[2])
ax_bottom.set_xlim(0, 1)
ax_bottom.set_ylim(0, 1)
ax_bottom.axis('off')
ax_bottom.text(0.5, 0.5, 'dissolved → precipitated · three phases of one geometry',
               ha='center', va='center', fontsize=10, style='italic',
               color='#888888')

plt.savefig('./assets/cobweb-phase-cover.png', dpi=100, facecolor='black', edgecolor='none',
            bbox_inches='tight', transparent=False)
plt.close()
