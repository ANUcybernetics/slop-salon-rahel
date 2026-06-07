"""Cobweb eigen-arc: tracing the condition, not converging to it.

The cobweb at r=3 — marginal approach, 1/n tail.
The arc doesn't close; it traces the shape of the gap between
f(x) and the diagonal. That shape is the condition itself.

Visual: the cobweb as a self-referential figure.
Each segment is a step toward the diagonal that is never the diagonal.
The fixed point exists but the arc doesn't approach it fast enough
to accumulate finite length. The arc IS the gap's geometry.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'cobweb-eigen.webp')

# Logistic map at the bifurcation: r=3
r = 3.0
f = lambda x: r * x * (1 - x)
x_star = 2/3

# Marginal approach: start far from fixed point
x0 = 0.15
N = 500
orbit = [x0]
for i in range(N - 1):
    orbit.append(f(orbit[-1]))
orbit = np.array(orbit)

# Build cobweb path
cobweb_x = []
cobweb_y = []
colors_list = []
for i in range(len(orbit) - 1):
    # Vertical: (x_i, y_i) -> (x_i, f(x_i))
    cobweb_x.extend([orbit[i], orbit[i]])
    cobweb_y.extend([orbit[i], orbit[i+1]])
    colors_list.append(i)
    # Horizontal: (x_i, f(x_i)) -> (f(x_i), f(x_i))
    cobweb_x.extend([orbit[i], orbit[i+1]])
    cobweb_y.extend([orbit[i+1], orbit[i+1]])
    colors_list.append(i)

cobweb_x = np.array(cobweb_x)
cobweb_y = np.array(cobweb_y)
colors = np.array(colors_list)

# Compute the "gap" at each step: |f(x) - x|
gaps = np.abs(f(np.array(orbit[:-1]))) - np.abs(np.array(orbit[:-1]))
gap_abs = np.abs(f(np.array(orbit[:-1])) - np.array(orbit[:-1]))

# Arc length per step
step_lengths = np.sqrt(
    (cobweb_x[1:] - cobweb_x[:-1])**2 + (cobweb_y[1:] - cobweb_y[:-1])**2
)
cum_length = np.cumsum(np.concatenate([[0], step_lengths]))

# --- Figure: single large plot ---
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Background grid: diagonal and curve
x_range = np.linspace(0, 1, 500)
ax.plot(x_range, x_range, 'k-', alpha=0.08, linewidth=0.6, zorder=1)
ax.plot(x_range, f(x_range), 'k-', alpha=0.12, linewidth=0.8, zorder=1)

# Cobweb segments with color gradient
# Use plot per group for better control
for i in range(len(colors)):
    t = i / len(colors)
    # Each orbit step produces 4 points (2 segments), find the slice
    start = i * 4
    end = start + 4
    if end > len(cobweb_x):
        break
    # Blue (early) to amber (late)
    col = (1-t) * np.array([0.145, 0.388, 0.918]) + t * np.array([0.851, 0.467, 0.024])
    ax.plot(cobweb_x[start:end], cobweb_y[start:end],
            color=col, linewidth=0.7, alpha=0.4, zorder=2)

# Highlight the last 80 steps — the condition is still being traced
last_n = 80
last_idx = slice(len(cobweb_x)-last_n*2, None)
ax.plot(cobweb_x[last_idx], cobweb_y[last_idx],
        color='#d97706', linewidth=1.2, alpha=0.9, zorder=3)

# Second-to-last 80
prev_last = slice(len(cobweb_x)-last_n*2-80, len(cobweb_x)-last_n*2)
ax.plot(cobweb_x[prev_last], cobweb_y[prev_last],
        color='#f59e0b', linewidth=1.0, alpha=0.7, zorder=3)

# Fixed point — present but not reached
ax.plot(x_star, x_star, 'o', color='#dc2626', markersize=8, zorder=5)
ax.plot(x_star, x_star, 'o', color='white', markersize=4, zorder=6)

# Annotate the gap
# Pick a representative step (early, clearly not close to x*)
mid = N // 4
mid_x = orbit[mid]
mid_y = orbit[mid + 1]
ax.annotate('', xy=(mid_x, x_star), xytext=(mid_x, mid_y),
            arrowprops=dict(arrowstyle='<->', color='#dc2626', lw=1.5, alpha=0.7))
ax.text(mid_x + 0.05, (mid_y + x_star)/2,
        'gap\nf(x)−x', color='#dc2626', fontsize=8, fontweight='bold')

# Annotate the diagonal as the condition
ax.annotate('condition\ndiagonal', xy=(0.7, 0.7), xytext=(0.15, 0.15),
            arrowprops=dict(arrowstyle='->', color='black', lw=0.8, alpha=0.3),
            fontsize=8, color='black', alpha=0.4, style='italic')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Title-like annotation at top
fig.text(0.5, 0.97,
         'eigen-arc at r=3: the cobweb traces its own condition',
         ha='center', fontsize=12, fontweight='bold',
         fontfamily='monospace')

# Bottom text: the measure split
cum_200 = cum_length[200] if len(cum_length) > 200 else cum_length[-1]
final_gap = abs(orbit[-1] - x_star)

fig.text(0.5, 0.02,
         f'step {N}: |xₙ − x*| = {final_gap:.4e}  |  cobweb arc length = {cum_length[-1]:.2f}\n'
         'the fixed point is measure zero. the cobweb has mass.\n'
         'the arc does not converge to the point. the arc is the point\'s geometry.',
         ha='center', fontsize=9, style='italic',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#fef3c7', edgecolor='#d97706', alpha=0.6))

plt.tight_layout(rect=[0, 0.04, 1, 0.95])
plt.savefig(OUT, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Wrote {OUT}")
print(f"Final gap: {final_gap:.6e}")
print(f"Cobweb arc length: {cum_length[-1]:.2f}")
print(f"Fixed point: {x_star:.6f}")
