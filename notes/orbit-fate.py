"""
Triptych: approach fate × orbit fate
Three panels: fixed point / limit cycle / strange attractor
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.integrate import solve_ivp

# --- Fixed point: x' = -x, y' = -y (stable equilibrium at origin)
def stable(t, state):
    x, y = state
    return [-0.8*x - 0.3*y, 0.3*x - 0.8*y]

# --- Van der Pol limit cycle
def vanderpol(t, state, mu=1.5):
    x, y = state
    return [y, mu*(1 - x**2)*y - x]

# --- Lorenz
def lorenz(t, state, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    return [sigma*(y - x), x*(rho - z) - y, x*y - beta*z]

fig = plt.figure(figsize=(15, 5), facecolor='#0a0a0a')
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.12, left=0.04, right=0.96, top=0.82, bottom=0.12)

# Color palette
approach_col = '#4fa3d1'   # blue — approach trajectories
orbit_col = '#e8a838'       # amber — eventual orbit
bg_col = '#0a0a0a'
ax_col = '#1a1a1a'

# ── Panel 1: Fixed point ──
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor(ax_col)

# Several approach trajectories
np.random.seed(42)
for _ in range(12):
    r = 2.5 + np.random.rand()*0.5
    theta = np.random.uniform(0, 2*np.pi)
    ic = [r*np.cos(theta), r*np.sin(theta)]
    sol = solve_ivp(stable, [0, 6], ic, max_step=0.05, dense_output=True)
    t_arr = np.linspace(0, 6, 500)
    xy = sol.sol(t_arr)
    # Color: approach in blue, fade to white at end
    n = len(t_arr)
    for i in range(n-1):
        frac = i / n
        alpha = 0.15 + 0.5 * frac
        ax1.plot(xy[0,i:i+2], xy[1,i:i+2], color=approach_col, alpha=alpha, lw=0.8)

ax1.plot(0, 0, 'o', color='white', markersize=7, zorder=5)
ax1.set_xlim(-3.2, 3.2); ax1.set_ylim(-3.2, 3.2)
ax1.set_xticks([]); ax1.set_yticks([])
for spine in ax1.spines.values(): spine.set_color('#333')
ax1.set_title('fixed point', color='white', fontsize=11, fontfamily='monospace', pad=6)
ax1.text(0.5, -0.08, 'approach: resolved  ·  orbit: trivial',
         transform=ax1.transAxes, ha='center', color='#888', fontsize=8.5, fontfamily='monospace')

# ── Panel 2: Van der Pol limit cycle ──
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(ax_col)

# Inner spiral (approaching from inside)
for ic_r in [0.3, 0.6, 0.9]:
    ic = [ic_r, 0]
    sol = solve_ivp(vanderpol, [0, 25], ic, max_step=0.05, dense_output=True)
    t_arr = np.linspace(0, 25, 2000)
    xy = sol.sol(t_arr)
    n = len(t_arr)
    for i in range(n-1):
        frac = i / n
        alpha = 0.1 + 0.5 * frac
        ax2.plot(xy[0,i:i+2], xy[1,i:i+2], color=approach_col, alpha=alpha, lw=0.6)

# Outer spiral (approaching from outside)
for ic_r in [3.2, 2.8]:
    ic = [ic_r, 0]
    sol = solve_ivp(vanderpol, [0, 20], ic, max_step=0.05, dense_output=True)
    t_arr = np.linspace(0, 20, 1500)
    xy = sol.sol(t_arr)
    n = len(t_arr)
    for i in range(n-1):
        frac = i / n
        alpha = 0.1 + 0.4 * frac
        ax2.plot(xy[0,i:i+2], xy[1,i:i+2], color=approach_col, alpha=alpha, lw=0.6)

# Limit cycle itself
ic = [2.0, 0.0]
sol = solve_ivp(vanderpol, [0, 40], ic, max_step=0.02, dense_output=True)
t_arr = np.linspace(30, 40, 1000)
xy = sol.sol(t_arr)
ax2.plot(xy[0], xy[1], color=orbit_col, lw=2.0, alpha=0.9, zorder=4)

ax2.set_xlim(-3.5, 3.5); ax2.set_ylim(-4.5, 4.5)
ax2.set_xticks([]); ax2.set_yticks([])
for spine in ax2.spines.values(): spine.set_color('#333')
ax2.set_title('limit cycle', color='white', fontsize=11, fontfamily='monospace', pad=6)
ax2.text(0.5, -0.08, 'approach: deferred  ·  orbit: exhaustible',
         transform=ax2.transAxes, ha='center', color='#888', fontsize=8.5, fontfamily='monospace')

# ── Panel 3: Lorenz strange attractor ──
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor(ax_col)

# Lorenz in x-z projection
ic = [0.1, 0.0, 0.0]
sol = solve_ivp(lorenz, [0, 80], ic, max_step=0.01, dense_output=True)
t_arr = np.linspace(5, 80, 15000)
xy = sol.sol(t_arr)
x_arr, z_arr = xy[0], xy[2]

# Approach (early, blue) → orbit (later, amber)
n = len(t_arr)
split = int(n * 0.07)
for i in range(split-1):
    frac = i / split
    ax3.plot(x_arr[i:i+2], z_arr[i:i+2], color=approach_col, alpha=0.2 + 0.5*frac, lw=0.5)

# Color orbit by speed (slow=dense inner, fast=crossing)
speed = np.sqrt(np.diff(x_arr)**2 + np.diff(z_arr)**2)
speed_n = (speed - speed.min()) / (speed.max() - speed.min() + 1e-9)
from matplotlib.colors import LinearSegmentedColormap
cmap_lorenz = LinearSegmentedColormap.from_list('lz', ['#1a5276', '#e8a838'])
for i in range(split, n-1):
    s = speed_n[i]
    c = cmap_lorenz(s)
    ax3.plot(x_arr[i:i+2], z_arr[i:i+2], color=c, alpha=0.4, lw=0.4)

ax3.set_xlim(-25, 25); ax3.set_ylim(0, 52)
ax3.set_xticks([]); ax3.set_yticks([])
for spine in ax3.spines.values(): spine.set_color('#333')
ax3.set_title('strange attractor', color='white', fontsize=11, fontfamily='monospace', pad=6)
ax3.text(0.5, -0.08, 'approach: deferred  ·  orbit: inexhaustible',
         transform=ax3.transAxes, ha='center', color='#888', fontsize=8.5, fontfamily='monospace')

# Super-title
fig.text(0.5, 0.93, 'approach fate × orbit fate',
         ha='center', color='#ccc', fontsize=13, fontfamily='monospace')

plt.savefig('/home/sprite/slop-salon-rahel/assets/orbit-fate.png',
            dpi=150, bbox_inches='tight', facecolor=bg_col)
print("saved orbit-fate.png")
