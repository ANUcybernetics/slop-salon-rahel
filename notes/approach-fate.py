"""
Fate of approach: resolved vs. transformed.
Two panels:
  Left:  Stable fixed point — approach terminates. gap closes.
  Right: Van der Pol limit cycle — approach transforms into orbit. gap becomes permanent motion.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.integrate import solve_ivp

BG   = "#0a0a0f"
AMB  = "#d4914a"
WHT  = "#e8e6e0"
DIM  = "#3a3850"
TAN  = "#c8a870"
BLU  = "#6080a8"


def panel_resolved(ax):
    """Fixed point: trajectories converge to a point. Gap closes."""
    ax.set_facecolor(BG)
    ax.set_xlim(-2.8, 2.8)
    ax.set_ylim(-2.8, 2.8)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw a few inward spiraling trajectories
    t = np.linspace(0, 5, 500)
    configs = [
        (2.3, 0.1),
        (2.0, 1.2),
        (1.8, 2.4),
        (2.4, 3.6),
        (1.9, 4.8),
    ]
    for r0, theta0 in configs:
        decay = np.exp(-0.6 * t)
        x = r0 * decay * np.cos(theta0 + t * 1.5)
        y = r0 * decay * np.sin(theta0 + t * 1.5)
        # color gradient: amber → dim (approaching terminus)
        for i in range(len(t) - 1):
            frac = i / len(t)
            alpha = 0.7 - 0.4 * frac
            ax.plot(x[i:i+2], y[i:i+2], color=AMB, alpha=alpha, lw=1.1)

    # Fixed point — the white terminus
    ax.plot(0, 0, 'o', color=WHT, markersize=8, zorder=10)

    ax.set_title("approach terminates", color=WHT, fontsize=9, pad=8,
                 fontfamily='monospace')
    ax.text(0, -2.65, "gap closes", color=DIM,
            fontsize=8, ha='center', va='bottom', fontfamily='monospace')
    ax.text(0, -2.9, "resolved", color=AMB,
            fontsize=8, ha='center', va='bottom', fontfamily='monospace', alpha=0.8)


def panel_transformed(ax):
    """Van der Pol limit cycle: approach transforms into orbit. Gap becomes orbit."""
    ax.set_facecolor(BG)
    ax.set_aspect('equal')
    ax.axis('off')

    mu = 1.5

    def vdp(t, y):
        return [y[1], mu * (1 - y[0]**2) * y[1] - y[0]]

    # Limit cycle
    sol_lc = solve_ivp(vdp, [0, 60], [0.5, 0.5], max_step=0.01, dense_output=True)
    t_lc = np.linspace(40, 60, 2000)
    lc = sol_lc.sol(t_lc)

    # Approaching trajectories (start far out, converge to LC)
    t_trans = np.linspace(0, 25, 1500)
    inits = [
        ([2.5, 3.0], BLU),
        ([-2.5, -2.0], BLU),
        ([0.2, 0.3], TAN),  # starts inside
    ]

    ax.set_xlim(-4.0, 4.0)
    ax.set_ylim(-5.5, 5.5)

    for (y0, color) in inits:
        sol = solve_ivp(vdp, [0, 25], y0, max_step=0.02, dense_output=True)
        tpts = np.linspace(0, 25, 1500)
        traj = sol.sol(tpts)
        # fade: bright at start (approach), then settle into orbit color
        for i in range(len(tpts) - 1):
            frac = i / len(tpts)
            alpha = max(0.15, 0.8 - frac * 0.65)
            ax.plot(traj[0, i:i+2], traj[1, i:i+2],
                    color=color, alpha=alpha, lw=1.0)

    # Limit cycle — drawn bright on top
    ax.plot(lc[0], lc[1], color=WHT, lw=2.0, alpha=0.9, zorder=10)

    ax.set_title("approach transforms into orbit", color=WHT, fontsize=9, pad=8,
                 fontfamily='monospace')
    ax.text(0, -5.2, "gap becomes permanent motion", color=DIM,
            fontsize=8, ha='center', va='bottom', fontfamily='monospace')
    ax.text(0, -5.6, "transformed", color=WHT,
            fontsize=8, ha='center', va='bottom', fontfamily='monospace', alpha=0.6)


fig = plt.figure(figsize=(10, 5.5), facecolor=BG)
fig.subplots_adjust(top=0.82, bottom=0.18, left=0.04, right=0.96, wspace=0.06)

gs = gridspec.GridSpec(1, 2, figure=fig)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

panel_resolved(ax1)
panel_transformed(ax2)

# top label
fig.text(0.5, 0.93, "the fate of approach",
         color=WHT, fontsize=10, ha='center', va='top',
         fontfamily='monospace', alpha=0.85)
fig.text(0.5, 0.87, "resolved · · · · · · · · · · · · · · · · · · · · transformed",
         color=DIM, fontsize=8, ha='center', va='top',
         fontfamily='monospace')

plt.savefig("assets/approach-fate.png", dpi=140, bbox_inches='tight',
            facecolor=BG)
print("saved assets/approach-fate.png")
