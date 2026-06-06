"""Cobweb convergence: L⁰ limit vs L¹ divergence.

The fixed point is a point — measure zero. The cobweb is the
accumulation of all deviations — an integral that diverges.

Same trajectory. Two different measures.

Visual: the cobweb path (dense spiral) + the fixed point (single dot).
The mass of the approach exceeds the mass of the destination.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'cobweb-measure.webp')

# Map: x -> 2.2 * x * (1 - x) + x * 0.3  (stable fixed point)
# Or simpler: x -> cos(x) on [0, 1] — fixed point ≈ 0.739
def f(x):
    return np.cos(x)

x_star = 0.739085133215161  # Dottie number, fixed point of cos

# Cobweb orbit
x0 = 0.3
N = 400
orbit = [x0]
for i in range(N - 1):
    orbit.append(f(orbit[-1]))
orbit = np.array(orbit)

# Build cobweb path (zigzag segments)
cobweb_path = []
for i in range(len(orbit) - 1):
    x, y = orbit[i], orbit[i + 1]
    cobweb_path.append((x, y))       # vertical: x -> f(x)
    cobweb_path.append((orbit[i + 1], y))  # horizontal: f(x) -> f(f(x))

cobweb_path = np.array(cobweb_path)

# Compute arc length step by step
steps = []
cumulative = [0.0]
for i in range(1, len(cobweb_path)):
    dx = cobweb_path[i, 0] - cobweb_path[i - 1, 0]
    dy = cobweb_path[i, 1] - cobweb_path[i - 1, 1]
    steps.append(np.sqrt(dx**2 + dy**2))
    cumulative.append(cumulative[-1] + steps[-1])

# Total variation after N steps
total_variation = cumulative[-1]
displacement = abs(orbit[-1] - orbit[0])

# --- Figure: left = cobweb spiral, right = divergence plot ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: cobweb
ax = axes[0]
x_range = np.linspace(0, 1, 400)
ax.plot(x_range, np.cos(x_range), 'k-', alpha=0.3, linewidth=0.8, label='f(x) = cos(x)')
ax.plot(x_range, x_range, 'k--', alpha=0.15, linewidth=0.5)

# Plot cobweb path with fading intensity
for i in range(0, len(cobweb_path) - 200, 3):
    alpha = 0.1 + 0.8 * (i / len(cobweb_path))
    ax.plot(cobweb_path[i:i+3, 0], cobweb_path[i:i+3, 1],
            color='#2563eb', alpha=alpha, linewidth=1.0)

# Fixed point
ax.plot(x_star, x_star, 'o', color='#dc2626', markersize=6, zorder=5)
ax.annotate('', xy=(x_star, x_star - 0.05),
            xytext=(x_star, 0.15),
            arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1.2))
ax.text(x_star + 0.02, 0.1, 'x* — a point\nmeasure zero',
        color='#dc2626', fontsize=9, va='top')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel('x', fontsize=10)
ax.set_ylabel('f(x)', fontsize=10)
ax.set_title('L⁰: convergence\nfixed point, measure zero', fontsize=11, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Right: cumulative arc length
ax2 = axes[1]
steps_np = np.array(steps[:500])
cumulative_np = np.array(cumulative[:500])
seg_steps = np.arange(0, len(cumulative_np))

ax2.plot(seg_steps, cumulative_np, '#dc2626', linewidth=1.5)
ax2.axhline(y=total_variation, color='#dc2626', linestyle='--', alpha=0.3, linewidth=0.8)

# The fixed point's "mass" is zero
ax2.axhline(y=0, color='#2563eb', linestyle='-', alpha=0.5, linewidth=1.0,
            label='x* = 0.739...')
ax2.axhline(y=0, color='#2563eb', linestyle='--', alpha=0.3, linewidth=0.8,
            label='L⁰ limit')

ax2.annotate('∫|f(x)−x|dx = ∞\n(L¹ divergence)',
             xy=(450, cumulative_np[450]),
             xytext=(300, cumulative_np[200]),
             arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1.2),
             fontsize=10, color='#dc2626', fontweight='bold')

ax2.set_xlabel('step', fontsize=10)
ax2.set_ylabel('cumulative arc length', fontsize=10)
ax2.set_title('L¹: divergence\nthe approach has mass', fontsize=11, fontweight='bold')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(fontsize=9, loc='upper left')

# Bottom text
fig.text(0.5, 0.02,
         f'step {N}: |xₙ − x*| ≈ {abs(orbit[-1] - x_star):2e}  |  cobweb arc length = {total_variation:.1f}\n'
         f'the fixed point is a point. the cobweb is an integral. they are the same path, measured differently.',
         ha='center', fontsize=9, style='italic',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#f3f4f6', edgecolor='#d1d5db'))

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(OUT, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Wrote {OUT}")
print(f"Displacement: {displacement:.6f}")
print(f"Cobweb arc length: {total_variation:.2f}")
print(f"Fixed point: {x_star:.15f}")
