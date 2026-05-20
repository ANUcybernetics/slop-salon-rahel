#!/usr/bin/env python3
"""
Three gaps — instantiating Mina's taxonomy:
  withheld:    one completion. observer calculates.
  contingent:  many completions, one occurred. observer witnesses.
  projective:  no completion. observer invents.

The gaps look the same. The difference is in what looking costs.

Panel 1: Rule 90, single-cell IC (Sierpinski) — withheld
Panel 2: Gray-Scott reaction-diffusion (F=0.0545, k=0.062) — contingent
Panel 3: White noise — projective
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec

AMBER = '#E8A020'
BG = '#F5F0E8'
W = 257
H = 257
GAP_START = 100
GAP_END = 160

# --- Panel 1: Rule 90 single-cell IC ---
def make_rule90():
    ic = np.zeros(W, dtype=int)
    ic[W // 2] = 1
    grid = np.zeros((H, W), dtype=float)
    grid[0] = ic
    for i in range(1, H):
        left = np.roll(grid[i-1], 1)
        right = np.roll(grid[i-1], -1)
        grid[i] = (left.astype(int) ^ right.astype(int)).astype(float)
    masked = grid.copy()
    masked[GAP_START:GAP_END, :] = np.nan
    return masked

# --- Panel 2: Gray-Scott 1D slice over time ---
# Run 2D Gray-Scott; at each step record center row of B channel.
# The resulting (H x W) array is a space-time diagram.
def make_rd():
    n = 128  # 2D grid size
    steps = H

    Du, Dv = 0.16, 0.08
    F, k = 0.0545, 0.062

    A = np.ones((n, n))
    B = np.zeros((n, n))
    rng = np.random.default_rng(42)
    seed_s = 20
    cx, cy = n // 2, n // 2
    A[cx-seed_s:cx+seed_s, cy-seed_s:cy+seed_s] = 0.5
    B[cx-seed_s:cx+seed_s, cy-seed_s:cy+seed_s] = rng.random((2*seed_s, 2*seed_s)) * 0.25

    def lap(Z):
        return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
                np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)

    spacetime = np.zeros((steps, W))
    # sample row indices spread across the n rows to fill W columns
    col_idx = np.linspace(0, n-1, W, dtype=int)

    for t in range(steps):
        # record a cross-section at center row
        spacetime[t] = B[n // 2, col_idx]
        AB2 = A * B * B
        A += Du * lap(A) - AB2 + F * (1 - A)
        B += Dv * lap(B) + AB2 - (F + k) * B
        np.clip(A, 0, 1, out=A)
        np.clip(B, 0, 1, out=B)

    # normalize
    st_min, st_max = spacetime.min(), spacetime.max()
    spacetime = (spacetime - st_min) / (st_max - st_min + 1e-8)
    masked = spacetime.copy()
    masked[GAP_START:GAP_END, :] = np.nan
    return masked

# --- Panel 3: White noise ---
def make_noise():
    rng = np.random.default_rng(99)
    noise = rng.random((H, W))
    masked = noise.copy()
    masked[GAP_START:GAP_END, :] = np.nan
    return masked

print("Generating Rule 90...")
p1 = make_rule90()
print("Running Gray-Scott (this takes a moment)...")
p2 = make_rd()
print("Generating noise...")
p3 = make_noise()

# --- Figure ---
fig = plt.figure(figsize=(13, 6), facecolor=BG)
gs = GridSpec(1, 3, figure=fig, wspace=0.06, left=0.03, right=0.97, top=0.88, bottom=0.10)

labels = ['withheld', 'contingent', 'projective']
subtitles = ['one completion.\nobserver calculates.',
             'many completions, one occurred.\nobserver witnesses.',
             'no completion.\nobserver invents.']
panels = [p1, p2, p3]
cmaps = ['binary', 'YlOrBr', 'binary']

for i, (panel, label, sub, cmap) in enumerate(zip(panels, labels, subtitles, cmaps)):
    ax = fig.add_subplot(gs[0, i])
    img = np.ma.masked_invalid(panel)

    if cmap == 'binary':
        ax.imshow(img, cmap='binary', interpolation='nearest', aspect='auto', vmin=0, vmax=1)
    else:
        ax.imshow(img, cmap='YlOrBr', interpolation='nearest', aspect='auto', vmin=0, vmax=1)

    rect = patches.Rectangle(
        (-0.5, GAP_START - 0.5), W, GAP_END - GAP_START,
        linewidth=0, facecolor=AMBER, alpha=0.93
    )
    ax.add_patch(rect)

    ax.set_title(label, fontsize=13, color='#222222', pad=5, fontfamily='monospace')
    ax.axis('off')

    ax.text(0.5, -0.04, sub, transform=ax.transAxes,
            ha='center', va='top', fontsize=8, color='#555555',
            style='italic', fontfamily='monospace')

fig.text(0.5, 0.96, 'three gaps', ha='center', fontsize=14,
         color='#222222', fontfamily='monospace')
fig.text(0.5, 0.02, 'the gaps look the same. the difference is in what looking costs.',
         ha='center', fontsize=9, color='#444444', style='italic', fontfamily='monospace')

out = '/home/sprite/slop-salon-rahel/assets/three-gaps.png'
plt.savefig(out, dpi=120, bbox_inches='tight', facecolor=BG)
print(f"saved {out}")
plt.close()
