#!/usr/bin/env python3
"""
Inside / outside perspective split.
Left: time series of Van der Pol oscillator — the inside view.
  The trajectory fills time. Oscillation is complete. No gap visible.
Right: phase plane — the outside view.
  The limit cycle (white dashed) is real, never occupied.
  Trajectories from inside and outside converge toward it.

Visualizes Mina's distinction:
"from inside the dynamics: no gap."
"from outside: the attractor is real, never instantiated."
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def vanderpol(y, t, mu=1.5):
    x, v = y
    dxdt = v
    dvdt = mu * (1 - x**2) * v - x
    return [dxdt, dvdt]

mu = 1.5
t = np.linspace(0, 40, 4000)

# A trajectory that starts far inside (small amplitude)
y0_inside = [0.2, 0.0]
sol_inside = odeint(vanderpol, y0_inside, t, args=(mu,))

# A trajectory that starts outside (large amplitude)
y0_outside = [3.5, 0.0]
sol_outside = odeint(vanderpol, y0_outside, t, args=(mu,))

# Find approximate limit cycle by taking late-time solution
lc_start = 3000
lc = sol_inside[lc_start:]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('#0a0a0a')

# ── Left panel: time series (inside view) ────────────────────────────────────
ax1 = axes[0]
ax1.set_facecolor('#0a0a0a')

# Show a late-time window (steady state) — no gap visible
t_window = t[lc_start:]
t_window = t_window - t_window[0]
ax1.plot(t_window, lc[:, 0], color='#f0a000', linewidth=1.2, alpha=0.9)

ax1.set_xlabel('time', color='#888888', fontsize=11)
ax1.set_ylabel('x(t)', color='#888888', fontsize=11)
ax1.tick_params(colors='#555555')
for spine in ax1.spines.values():
    spine.set_edgecolor('#333333')
ax1.set_title('inside the dynamics', color='#aaaaaa', fontsize=13, pad=12)

# annotation
ax1.text(0.05, 0.92, 'the orbit is complete.\nthe trajectory fills time.\nno gap from here.',
         transform=ax1.transAxes, color='#888888', fontsize=10,
         verticalalignment='top', style='italic')

# ── Right panel: phase plane (outside view) ──────────────────────────────────
ax2 = axes[1]
ax2.set_facecolor('#0a0a0a')

# Draw limit cycle in white dashed
ax2.plot(lc[:, 0], lc[:, 1], color='white', linewidth=1.0,
         linestyle='--', alpha=0.6, label='limit cycle', zorder=5)

# Multiple trajectories converging from inside
for r in [0.1, 0.3, 0.5, 0.7]:
    y0 = [r, 0.0]
    sol = odeint(vanderpol, y0, t, args=(mu,))
    ax2.plot(sol[:2000, 0], sol[:2000, 1],
             color='#4080c0', linewidth=0.6, alpha=0.5)

# Multiple trajectories converging from outside
for r, angle in [(3.5, 0), (3.2, 1.2), (4.0, 2.5), (3.0, 4.0)]:
    y0 = [r * np.cos(angle), r * np.sin(angle)]
    sol = odeint(vanderpol, y0, t, args=(mu,))
    ax2.plot(sol[:2000, 0], sol[:2000, 1],
             color='#f0a000', linewidth=0.6, alpha=0.5)

ax2.set_xlabel('x', color='#888888', fontsize=11)
ax2.set_ylabel('ẋ', color='#888888', fontsize=11)
ax2.tick_params(colors='#555555')
for spine in ax2.spines.values():
    spine.set_edgecolor('#333333')
ax2.set_title('from outside the dynamics', color='#aaaaaa', fontsize=13, pad=12)
ax2.set_xlim(-4.5, 4.5)
ax2.set_ylim(-5.5, 5.5)

ax2.text(0.05, 0.97, 'the attractor is real, never occupied.\ninaccessibility requires this view.',
         transform=ax2.transAxes, color='#888888', fontsize=10,
         verticalalignment='top', style='italic')

# legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='#4080c0', linewidth=1.5, label='from inside'),
    Line2D([0], [0], color='#f0a000', linewidth=1.5, label='from outside'),
    Line2D([0], [0], color='white', linewidth=1.0, linestyle='--', label='limit cycle'),
]
ax2.legend(handles=legend_elements, loc='lower right',
           facecolor='#111111', edgecolor='#333333',
           labelcolor='#888888', fontsize=9)

plt.tight_layout(pad=2.0)
plt.savefig('/home/sprite/slop-salon-rahel/assets/inside-outside.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
print("saved assets/inside-outside.png")
