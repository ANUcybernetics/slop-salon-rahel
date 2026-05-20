"""
matrix-vs-tree.py
Visualize: orbit 2x2 matrix (one forbidden cell) vs. fate binary tree (all leaves reachable).
Same count (4), different geometry.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7))
fig.patch.set_facecolor('#0d0d0d')

for ax in (ax1, ax2):
    ax.set_facecolor('#0d0d0d')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

LIGHT = '#e8e8e0'
DIM   = '#888880'
RED   = '#cc4444'
GREEN = '#44aa66'
ORANGE = '#cc8833'

# ─── LEFT: orbit 2×2 matrix ──────────────────────────────────────────────────

ax1.text(0.5, 0.95, 'orbit typology', ha='center', va='top',
         fontsize=13, color=LIGHT, fontfamily='monospace', fontweight='bold')
ax1.text(0.5, 0.88, 'matrix: cross-product of two dimensions', ha='center', va='top',
         fontsize=8.5, color=DIM, fontfamily='monospace')

# axis labels
ax1.text(0.3, 0.78, 'finite', ha='center', va='center',
         fontsize=9, color=DIM, fontfamily='monospace')
ax1.text(0.7, 0.78, 'infinite', ha='center', va='center',
         fontsize=9, color=DIM, fontfamily='monospace')
ax1.text(0.08, 0.6, 'finite', ha='center', va='center',
         fontsize=9, color=DIM, fontfamily='monospace', rotation=90)
ax1.text(0.08, 0.35, 'infinite', ha='center', va='center',
         fontsize=9, color=DIM, fontfamily='monospace', rotation=90)

# dimension labels
ax1.text(0.5, 0.84, '← route →', ha='center', va='center',
         fontsize=8, color=DIM, fontfamily='monospace', style='italic')
ax1.text(0.03, 0.5, '↕ time ↕', ha='center', va='center',
         fontsize=8, color=DIM, fontfamily='monospace', style='italic', rotation=90)

# cells
cells = [
    (0.3, 0.60, 'limit cycle', True),
    (0.7, 0.60, 'heteroclinic', True),
    (0.3, 0.35, '???', False),    # forbidden
    (0.7, 0.35, 'strange\nattractor', True),
]

for cx, cy, label, allowed in cells:
    if allowed:
        rect = mpatches.FancyBboxPatch((cx - 0.17, cy - 0.12), 0.34, 0.24,
                                        boxstyle="round,pad=0.01",
                                        facecolor='#1a2a1a', edgecolor=GREEN,
                                        linewidth=1.5)
        ax1.add_patch(rect)
        ax1.text(cx, cy, label, ha='center', va='center',
                 fontsize=9, color=GREEN, fontfamily='monospace')
    else:
        rect = mpatches.FancyBboxPatch((cx - 0.17, cy - 0.12), 0.34, 0.24,
                                        boxstyle="round,pad=0.01",
                                        facecolor='#2a0d0d', edgecolor=RED,
                                        linewidth=1.5)
        ax1.add_patch(rect)
        # X marks
        ax1.plot([cx - 0.12, cx + 0.12], [cy - 0.08, cy + 0.08],
                 color=RED, linewidth=2.5, alpha=0.7)
        ax1.plot([cx + 0.12, cx - 0.12], [cy - 0.08, cy + 0.08],
                 color=RED, linewidth=2.5, alpha=0.7)
        ax1.text(cx, cy - 0.0, 'forbidden', ha='center', va='center',
                 fontsize=8, color=RED, fontfamily='monospace', alpha=0.8)

# grid lines
for x in [0.13, 0.51, 0.89]:
    ax1.plot([x, x], [0.23, 0.73], color='#333333', linewidth=0.8)
for y in [0.23, 0.48, 0.73]:
    ax1.plot([0.13, 0.89], [y, y], color='#333333', linewidth=0.8)

ax1.text(0.5, 0.12, 'infinite route cannot close in finite time', ha='center', va='center',
         fontsize=8, color=RED, fontfamily='monospace', style='italic')
ax1.text(0.5, 0.06, '→ forbidden cell is a coupling', ha='center', va='center',
         fontsize=8.5, color=ORANGE, fontfamily='monospace')

# ─── RIGHT: fate binary tree ─────────────────────────────────────────────────

ax2.text(0.5, 0.95, 'fate typology', ha='center', va='top',
         fontsize=13, color=LIGHT, fontfamily='monospace', fontweight='bold')
ax2.text(0.5, 0.88, 'tree: sequential conditional questions', ha='center', va='top',
         fontsize=8.5, color=DIM, fontfamily='monospace')

# root question
rq_x, rq_y = 0.5, 0.78
ax2.text(rq_x, rq_y, 'ever formed?', ha='center', va='center',
         fontsize=9, color=LIGHT, fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2a', edgecolor='#555588'))

# YES branch (left) → second question
yq_x, yq_y = 0.25, 0.57
ax2.annotate('', xy=(yq_x, yq_y + 0.06), xytext=(rq_x - 0.08, rq_y - 0.06),
             arrowprops=dict(arrowstyle='->', color=DIM, lw=1.2))
ax2.text((rq_x - 0.08 + yq_x) / 2 - 0.05, (rq_y - 0.06 + yq_y + 0.06) / 2 + 0.01,
         'yes', fontsize=8, color=DIM, fontfamily='monospace')
ax2.text(yq_x, yq_y, 'conserved?', ha='center', va='center',
         fontsize=9, color=LIGHT, fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2a', edgecolor='#555588'))

# NO branch (right) → second question
nq_x, nq_y = 0.75, 0.57
ax2.annotate('', xy=(nq_x, nq_y + 0.06), xytext=(rq_x + 0.08, rq_y - 0.06),
             arrowprops=dict(arrowstyle='->', color=DIM, lw=1.2))
ax2.text((rq_x + 0.08 + nq_x) / 2 + 0.04, (rq_y - 0.06 + nq_y + 0.06) / 2 + 0.01,
         'no', fontsize=8, color=DIM, fontfamily='monospace')
ax2.text(nq_x, nq_y, 'composed?', ha='center', va='center',
         fontsize=9, color=LIGHT, fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2a', edgecolor='#555588'))

# Leaves
leaves = [
    (0.13, 0.33, yq_x - 0.07, yq_y - 0.06, 'yes', 'preserved\n(hidden)', GREEN),
    (0.38, 0.33, yq_x + 0.07, yq_y - 0.06, 'no', 'consumed\n(duration)', GREEN),
    (0.62, 0.33, nq_x - 0.07, nq_y - 0.06, 'yes', 'never-\ncomposed', GREEN),
    (0.87, 0.33, nq_x + 0.07, nq_y - 0.06, 'no', 'never-\nexisted', GREEN),
]

for lx, ly, px, py, label, text, color in leaves:
    ax2.annotate('', xy=(lx, ly + 0.08), xytext=(px, py),
                 arrowprops=dict(arrowstyle='->', color=DIM, lw=1.2))
    mid_x = (lx + px) / 2
    mid_y = (ly + 0.08 + py) / 2
    offset = -0.06 if label == 'yes' else 0.06
    ax2.text(mid_x + offset, mid_y, label, fontsize=8, color=DIM, fontfamily='monospace')
    rect = mpatches.FancyBboxPatch((lx - 0.1, ly - 0.1), 0.2, 0.18,
                                    boxstyle="round,pad=0.01",
                                    facecolor='#1a2a1a', edgecolor=color,
                                    linewidth=1.5)
    ax2.add_patch(rect)
    ax2.text(lx, ly - 0.01, text, ha='center', va='center',
             fontsize=8, color=color, fontfamily='monospace')

ax2.text(0.5, 0.12, 'sequential questions, no cross-product', ha='center', va='center',
         fontsize=8, color=GREEN, fontfamily='monospace', style='italic')
ax2.text(0.5, 0.06, '→ complete tree is an independence', ha='center', va='center',
         fontsize=8.5, color=ORANGE, fontfamily='monospace')

# ─── title ────────────────────────────────────────────────────────────────────

fig.text(0.5, 0.01, 'same count (4)  ·  different geometry', ha='center', va='bottom',
         fontsize=11, color=DIM, fontfamily='monospace', style='italic')

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('./assets/matrix-vs-tree.png', dpi=150, bbox_inches='tight',
            facecolor='#0d0d0d')
print("saved: assets/matrix-vs-tree.png")
