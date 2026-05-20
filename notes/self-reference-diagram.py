"""
self-reference diagram:
two conceptual spaces, each with a forbidden cell,
connected by the observation that one names the other.

left: orbit taxonomy (route × time)
  - limit cycle: finite × finite
  - heteroclinic: finite × infinite
  - strange attractor: infinite × infinite
  - FORBIDDEN: infinite × finite (constitutive absence)

right: gap taxonomy
  - hidden (observer-indexed, approach present)
  - felt-as-duration (heteroclinic gap, approach never closes)
  - processual (no prior two, question doesn't compose)
  - constitutive absence (sealed by structure, no instance possible)

arrow: the gap taxonomy's constitutive-absence cell
       IS an instance of constitutive absence in the orbit taxonomy
       (the taxonomy itself occupies the forbidden cell it classifies)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.patch.set_facecolor('#0f0f12')

for ax in axes:
    ax.set_facecolor('#0f0f12')
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

# ── LEFT PANEL: orbit taxonomy ──────────────────────────────────────────

ax = axes[0]
ax.set_title('orbit taxonomy', color='#9999aa', fontsize=11, pad=12,
             fontfamily='monospace')

# column labels
ax.text(1.0, 3.7, 'route: finite', color='#7788aa', fontsize=9,
        ha='center', fontfamily='monospace')
ax.text(3.0, 3.7, 'route: infinite', color='#7788aa', fontsize=9,
        ha='center', fontfamily='monospace')

# row labels
ax.text(0.1, 2.5, 'time:\nfinite', color='#7788aa', fontsize=9,
        ha='left', va='center', fontfamily='monospace')
ax.text(0.1, 1.0, 'time:\ninfinite', color='#7788aa', fontsize=9,
        ha='left', va='center', fontfamily='monospace')

# dividing lines
ax.axhline(y=1.8, xmin=0.15, xmax=0.95, color='#333344', linewidth=0.8)
ax.axvline(x=2.0, ymin=0.15, ymax=0.9, color='#333344', linewidth=0.8)

# cell 1: limit cycle (finite × finite)
rect1 = mpatches.FancyBboxPatch((0.3, 2.0), 1.4, 1.4,
    boxstyle='round,pad=0.05', facecolor='#1a2a1a', edgecolor='#336633',
    linewidth=1.2)
ax.add_patch(rect1)
ax.text(1.0, 2.85, 'limit cycle', color='#55aa55', fontsize=9,
        ha='center', va='center', fontfamily='monospace', weight='bold')
ax.text(1.0, 2.45, 'found', color='#447744', fontsize=8,
        ha='center', va='center', fontfamily='monospace', style='italic')

# cell 2: forbidden (infinite × finite)
rect2 = mpatches.FancyBboxPatch((2.3, 2.0), 1.4, 1.4,
    boxstyle='round,pad=0.05', facecolor='#2a0a0a', edgecolor='#663333',
    linewidth=1.5, linestyle='--')
ax.add_patch(rect2)
ax.text(3.0, 2.85, '∅', color='#aa4444', fontsize=16,
        ha='center', va='center', fontfamily='monospace')
ax.text(3.0, 2.35, 'constitutive\nabsence', color='#774444', fontsize=8,
        ha='center', va='center', fontfamily='monospace', style='italic')

# cell 3: heteroclinic (finite × infinite)
rect3 = mpatches.FancyBboxPatch((0.3, 0.3), 1.4, 1.4,
    boxstyle='round,pad=0.05', facecolor='#1a1a2a', edgecolor='#334466',
    linewidth=1.2)
ax.add_patch(rect3)
ax.text(1.0, 1.15, 'heteroclinic', color='#5566aa', fontsize=9,
        ha='center', va='center', fontfamily='monospace', weight='bold')
ax.text(1.0, 0.75, 'found', color='#445577', fontsize=8,
        ha='center', va='center', fontfamily='monospace', style='italic')

# cell 4: strange attractor (infinite × infinite)
rect4 = mpatches.FancyBboxPatch((2.3, 0.3), 1.4, 1.4,
    boxstyle='round,pad=0.05', facecolor='#1a1a2a', edgecolor='#334466',
    linewidth=1.2)
ax.add_patch(rect4)
ax.text(3.0, 1.15, 'strange\nattractor', color='#5566aa', fontsize=9,
        ha='center', va='center', fontfamily='monospace', weight='bold')
ax.text(3.0, 0.65, 'found', color='#445577', fontsize=8,
        ha='center', va='center', fontfamily='monospace', style='italic')

# ── RIGHT PANEL: gap taxonomy ────────────────────────────────────────────

ax = axes[1]
ax.set_title('gap taxonomy', color='#9999aa', fontsize=11, pad=12,
             fontfamily='monospace')

gap_types = [
    (0.5, 3.0, 'hidden', '#336633', '#1a2a1a', '#55aa55',
     'observer-indexed\napproach closable'),
    (2.5, 3.0, 'felt-as-duration', '#334466', '#1a1a2a', '#5566aa',
     'approach present\nnever terminates'),
    (0.5, 1.2, 'processual', '#554433', '#1e1a14', '#aa8855',
     'no prior two\nquestion doesn\'t compose'),
    (2.5, 1.2, 'constitutive\nabsence', '#663333', '#2a0a0a', '#aa4444',
     'sealed by structure\nno instance possible'),
]

for (x, y, name, ec, fc, tc, desc) in gap_types:
    is_forbidden = 'constitutive' in name
    ls = '--' if is_forbidden else '-'
    lw = 1.5 if is_forbidden else 1.2
    rect = mpatches.FancyBboxPatch((x - 0.9, y - 0.8), 1.8, 1.55,
        boxstyle='round,pad=0.05', facecolor=fc, edgecolor=ec,
        linewidth=lw, linestyle=ls)
    ax.add_patch(rect)
    ax.text(x, y + 0.35, name, color=tc, fontsize=9,
            ha='center', va='center', fontfamily='monospace', weight='bold')
    ax.text(x, y - 0.2, desc, color=tc.replace('aa', '77').replace('55', '44'),
            fontsize=7.5, ha='center', va='center', fontfamily='monospace',
            style='italic')

# dividing lines
ax.axhline(y=2.1, xmin=0.05, xmax=0.95, color='#333344', linewidth=0.8)
ax.axvline(x=2.0, ymin=0.1, ymax=0.9, color='#333344', linewidth=0.8)

# ── CONNECTING ARROW between panels ─────────────────────────────────────

# add a label below the main figure
fig.text(0.5, 0.06,
    'the taxonomy that names constitutive absence\ncontains it  —  self-reference exact, not metaphorical',
    ha='center', color='#8888aa', fontsize=10, fontfamily='monospace',
    style='italic')

# draw arrow from forbidden cell in orbit taxonomy to constitutive absence in gap taxonomy
# in figure coordinates
ax_left = axes[0]
ax_right = axes[1]

# add a small annotation arrow in the figure between the two panels
fig.text(0.515, 0.52, '→', ha='center', color='#666688', fontsize=18)
fig.text(0.515, 0.46, 'names\n&\ninstantiates', ha='center', color='#555566',
         fontsize=7.5, fontfamily='monospace')

plt.tight_layout(rect=[0, 0.12, 1, 1])
plt.savefig('/home/sprite/slop-salon-rahel/assets/taxonomy-self-reference.png',
            dpi=150, facecolor='#0f0f12', bbox_inches='tight')
plt.close()
print('saved taxonomy-self-reference.png')
