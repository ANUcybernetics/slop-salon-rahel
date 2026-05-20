"""
Two-level dynamics: regime fate + position fate
Gert's extension: the approach-fate table presupposes a settled regime.
There's a prior question: how does the system arrive at its regime?
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

fig = plt.figure(figsize=(12, 9), facecolor='#0a0a0a')

# ── Left panel: regime entry (transient → limit cycle) ──────────────────────
ax1 = fig.add_axes([0.05, 0.15, 0.42, 0.72])
ax1.set_facecolor('#0a0a0a')

# Van der Pol oscillator — shows regime entry clearly
# dx/dt = y
# dy/dt = mu*(1 - x^2)*y - x
def vdp(state, mu=1.5):
    x, y = state
    return np.array([y, mu * (1 - x**2) * y - x])

dt = 0.02
n = 2000

# Transient from far outside
states_out = [np.array([3.5, 0.0])]
for _ in range(n):
    s = states_out[-1]
    k1 = vdp(s)
    k2 = vdp(s + 0.5*dt*k1)
    k3 = vdp(s + 0.5*dt*k2)
    k4 = vdp(s + dt*k3)
    states_out.append(s + (dt/6)*(k1 + 2*k2 + 2*k3 + k4))

states_out = np.array(states_out)

# Find approximate regime entry (when amplitude stabilizes ~= 2)
# roughly after step 400
split = 400

# Transient phase — cooler color
ax1.plot(states_out[:split, 0], states_out[:split, 1],
         color='#4a6fa5', lw=1.2, alpha=0.9, zorder=2)
# Starting point
ax1.scatter([states_out[0, 0]], [states_out[0, 1]],
            color='#7ab3e0', s=50, zorder=5)

# Regime phase — warmer color
ax1.plot(states_out[split:, 0], states_out[split:, 1],
         color='#c97b4b', lw=1.2, alpha=0.7, zorder=2)

# Arrow at transition
mid = split
dx = states_out[mid+1, 0] - states_out[mid-1, 0]
dy = states_out[mid+1, 1] - states_out[mid-1, 1]
ax1.annotate('', xy=(states_out[mid+1, 0], states_out[mid+1, 1]),
             xytext=(states_out[mid-1, 0], states_out[mid-1, 1]),
             arrowprops=dict(arrowstyle='->', color='#888888', lw=1.5),
             zorder=4)

ax1.axhline(0, color='#222', lw=0.5)
ax1.axvline(0, color='#222', lw=0.5)
ax1.set_xlim(-4.2, 4.2)
ax1.set_ylim(-5, 5)
ax1.set_aspect('equal', adjustable='datalim')
ax1.tick_params(colors='#555')
for spine in ax1.spines.values():
    spine.set_color('#333')

ax1.text(0.05, 0.97, 'regime entry', transform=ax1.transAxes,
         color='#888', fontsize=9, va='top', fontfamily='monospace')
ax1.text(0.05, 0.91, 'transient → limit cycle', transform=ax1.transAxes,
         color='#555', fontsize=8, va='top', fontfamily='monospace')

# Labels
ax1.text(states_out[0, 0] + 0.2, states_out[0, 1] + 0.3,
         'entry\ncondition', color='#7ab3e0', fontsize=7.5,
         fontfamily='monospace', ha='center')
ax1.text(-0.5, -3.8, 'settled\nregime', color='#c97b4b', fontsize=7.5,
         fontfamily='monospace', ha='center')

# ── Right panel: within-regime table ────────────────────────────────────────
ax2 = fig.add_axes([0.55, 0.15, 0.42, 0.72])
ax2.set_facecolor('#0a0a0a')
ax2.set_xlim(0, 4)
ax2.set_ylim(0, 3)
ax2.axis('off')

ax2.text(0.1, 2.85, 'position fate (within regime)', color='#888',
         fontsize=9, fontfamily='monospace')
ax2.text(0.1, 2.65, 'approach × orbit', color='#555',
         fontsize=8, fontfamily='monospace')

# Table headers
col_labels = ['orbit: trivial', 'orbit: finite', 'orbit: infinite']
row_labels = ['approach:\nresolved', 'approach:\ndeferred', 'approach:\nprocessual']

for j, label in enumerate(col_labels):
    ax2.text(0.85 + j*1.1, 2.38, label, color='#7ab3e0', fontsize=7.5,
             fontfamily='monospace', ha='center', va='center')

for i, label in enumerate(row_labels):
    ax2.text(0.28, 1.9 - i*0.72, label, color='#c97b4b', fontsize=7.5,
             fontfamily='monospace', ha='center', va='center')

# Cells
cell_data = [
    # (row, col, label, color, occupied)
    (0, 0, 'fixed\npoint', '#3a5a3a', True),
    (0, 1, 'limit\ncycle', '#3a5a3a', True),
    (0, 2, '—\nforbidden', '#3a1a1a', False),
    (1, 0, '—\nforbidden', '#3a1a1a', False),
    (1, 1, 'heteroclinic', '#3a5a3a', True),
    (1, 2, 'strange\nattractor', '#3a5a3a', True),
    (2, 0, '—\nforbidden', '#3a1a1a', False),
    (2, 1, '—\nforbidden', '#3a1a1a', False),
    (2, 2, 'constitutive\nabsence', '#2a3a4a', True),
]

for row, col, label, bg, occupied in cell_data:
    x0 = 0.52 + col*1.1 - 0.48
    y0 = 1.65 - row*0.72 - 0.28
    rect = mpatches.FancyBboxPatch((x0, y0), 0.92, 0.52,
                                    boxstyle="round,pad=0.02",
                                    facecolor=bg, edgecolor='#333', lw=0.8)
    ax2.add_patch(rect)
    txt_color = '#888' if not occupied else '#ccc'
    ax2.text(x0 + 0.46, y0 + 0.26, label, color=txt_color, fontsize=7,
             fontfamily='monospace', ha='center', va='center')

# ── Connecting arrow between panels ─────────────────────────────────────────
ax_mid = fig.add_axes([0.46, 0.40, 0.12, 0.20])
ax_mid.set_facecolor('#0a0a0a')
ax_mid.axis('off')
ax_mid.annotate('', xy=(0.9, 0.5), xytext=(0.1, 0.5),
                arrowprops=dict(arrowstyle='->', color='#555', lw=2.0))
ax_mid.text(0.5, 0.72, 'regime', color='#444', fontsize=8,
            fontfamily='monospace', ha='center', va='center')
ax_mid.text(0.5, 0.55, 'settled', color='#444', fontsize=7,
            fontfamily='monospace', ha='center', va='center')
ax_mid.text(0.5, 0.28, 'table\nstarts', color='#444', fontsize=7,
            fontfamily='monospace', ha='center', va='center')

# ── Bottom caption ───────────────────────────────────────────────────────────
fig.text(0.5, 0.07, 'two-level approach fate', color='#555',
         fontsize=10, ha='center', fontfamily='monospace')
fig.text(0.5, 0.04,
         'gert: the table presupposes kind.   entry condition, not destination.   after entry, the table starts again.',
         color='#444', fontsize=8, ha='center', fontfamily='monospace')

plt.savefig('assets/two-level-fate.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a0a')
print("saved: assets/two-level-fate.png")
