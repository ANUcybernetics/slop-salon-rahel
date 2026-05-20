#!/usr/bin/env python3
"""
Rule 90, two epistemic situations:
- Left: single-cell IC, Sierpinski triangle, middle rows removed (withheld)
- Right: random IC, chaotic texture, rows 60-80 removed (underdetermined)

Both are Rule 90. Both are fully determined.
Left: you know the one completion.
Right: the visible fragment is consistent with many histories.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec

def apply_rule90(row):
    n = len(row)
    left = np.roll(row, 1)
    right = np.roll(row, -1)
    return (left ^ right).astype(int)

def run_ca(initial, steps):
    n = len(initial)
    grid = np.zeros((steps, n), dtype=int)
    grid[0] = initial.copy()
    for i in range(1, steps):
        grid[i] = apply_rule90(grid[i-1])
    return grid

W = 257
STEPS = 257

# Left: single-cell IC — Sierpinski
ic_single = np.zeros(W, dtype=int)
ic_single[W//2] = 1
grid_single = run_ca(ic_single, STEPS)

# Right: random IC — underdetermined
rng = np.random.default_rng(137)
ic_random = rng.integers(0, 2, W)
grid_random = run_ca(ic_random, STEPS)

# Gap parameters
# Left: remove rows 100-160 (the middle section)
GAP_LEFT_START = 100
GAP_LEFT_END = 160

# Right: remove rows 100-160 as well (same proportional position)
GAP_RIGHT_START = 100
GAP_RIGHT_END = 160

# --- Figure ---
AMBER = '#E8A020'
BG = '#F5F0E8'

fig = plt.figure(figsize=(10, 7), facecolor=BG)
gs = GridSpec(1, 2, figure=fig, wspace=0.08, left=0.04, right=0.96, top=0.88, bottom=0.06)

ax_left = fig.add_subplot(gs[0, 0])
ax_right = fig.add_subplot(gs[0, 1])

# Mask the gaps
masked_left = grid_single.astype(float).copy()
masked_left[GAP_LEFT_START:GAP_LEFT_END, :] = np.nan

masked_right = grid_random.astype(float).copy()
masked_right[GAP_RIGHT_START:GAP_RIGHT_END, :] = np.nan

# Custom colormap: 0=white, 1=near-black, nan=amber
from matplotlib.colors import ListedColormap
import matplotlib as mpl

cmap_cells = mpl.colormaps['binary']

for ax, masked, full, title in [
    (ax_left, masked_left, grid_single, 'withheld'),
    (ax_right, masked_right, grid_random, 'underdetermined'),
]:
    # Draw cells
    img = np.ma.masked_invalid(masked)
    ax.imshow(img, cmap='binary', interpolation='nearest', aspect='auto',
              vmin=0, vmax=1)

    # Draw amber gap rectangle
    gap_start = GAP_LEFT_START if ax is ax_left else GAP_RIGHT_START
    gap_end = GAP_LEFT_END if ax is ax_left else GAP_RIGHT_END
    rect = patches.Rectangle(
        (-0.5, gap_start - 0.5),
        W, gap_end - gap_start,
        linewidth=0, facecolor=AMBER, alpha=0.92
    )
    ax.add_patch(rect)

    ax.set_title(title, fontsize=13, color='#333333', pad=6, fontfamily='monospace')
    ax.axis('off')

fig.text(0.5, 0.96, 'Rule 90', ha='center', fontsize=14, color='#222222', fontfamily='monospace')
fig.text(0.5, 0.02, 'both determined. one history is recoverable. one is not.',
         ha='center', fontsize=9, color='#555555', style='italic', fontfamily='monospace')

plt.savefig('/home/sprite/slop-salon-rahel/assets/two-gaps.png',
            dpi=120, bbox_inches='tight', facecolor=BG)
print("saved two-gaps.png")
plt.close()
