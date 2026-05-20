"""
Spectrum from extrinsic to intrinsic gap.
Three panels:
  Left:   Stable fixed point — object predates approach (gap = distance only)
  Center: Van der Pol limit cycle — object survives, type requires gap (extrinsic)
  Right:  RD processual — no object without approach (intrinsic)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.integrate import solve_ivp

# ── color palette ──────────────────────────────────────────
BG   = "#0a0a0f"
AMB  = "#d4914a"
WHT  = "#e8e6e0"
DIM  = "#4a4860"
GRID = "#1a1a2a"

# ── Panel 1: Stable fixed point ────────────────────────────
def panel_fixed_point(ax):
    ax.set_facecolor(BG)
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Phase field: dx/dt = -x, dy/dt = -y (simple stable origin)
    X, Y = np.meshgrid(np.linspace(-2.3, 2.3, 14), np.linspace(-2.3, 2.3, 14))
    U = -X * 0.6
    V = -Y * 0.6
    speed = np.sqrt(U**2 + V**2)
    U /= (speed + 0.01)
    V /= (speed + 0.01)
    ax.quiver(X, Y, U, V, color=DIM, alpha=0.4, scale=20, width=0.003)

    # A few trajectories spiraling in
    t = np.linspace(0, 4, 200)
    for r0, theta0 in [(2.0, 0), (1.8, np.pi/2), (1.5, np.pi), (2.2, 3*np.pi/4), (1.9, 5*np.pi/4)]:
        x = r0 * np.exp(-t) * np.cos(theta0 + t * 0.3)
        y = r0 * np.exp(-t) * np.sin(theta0 + t * 0.3)
        ax.plot(x, y, color=AMB, alpha=0.5, lw=1.0)

    # Fixed point
    ax.plot(0, 0, 'o', color=WHT, markersize=8, zorder=10)

    ax.set_title("stable fixed point", color=WHT, fontsize=9, pad=6,
                 fontfamily='monospace')

    # Label
    ax.text(0, -2.3, "object predates gap\napproach = distance", color=DIM,
            fontsize=7, ha='center', va='bottom', fontfamily='monospace',
            linespacing=1.6)


# ── Panel 2: Van der Pol limit cycle (no approaching trajectories) ──
def panel_limit_cycle(ax):
    ax.set_facecolor(BG)
    ax.set_aspect('equal')
    ax.axis('off')

    mu = 1.5

    def vdp(t, y):
        return [y[1], mu * (1 - y[0]**2) * y[1] - y[0]]

    # Find the limit cycle by integrating past transients
    sol = solve_ivp(vdp, [0, 60], [0.5, 0.5], max_step=0.01, dense_output=True)
    t_lc = np.linspace(40, 60, 2000)
    lc = sol.sol(t_lc)

    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-4.5, 4.5)

    # Draw only the limit cycle — no approach, no field
    ax.plot(lc[0], lc[1], color=WHT, lw=1.8, alpha=0.85, zorder=5)

    # Label the "solution" nature
    ax.text(0, 3.8, "a solution", color=DIM, fontsize=7.5,
            ha='center', va='center', fontfamily='monospace', style='italic')
    ax.annotate("", xy=(0.8, 2.5), xytext=(0, 3.6),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=0.8))

    ax.set_title("Van der Pol limit cycle", color=WHT, fontsize=9, pad=6,
                 fontfamily='monospace')
    ax.text(0, -4.2, "object survives removal of approach\ngap constitutes type, not form",
            color=DIM, fontsize=7, ha='center', va='bottom',
            fontfamily='monospace', linespacing=1.6)


# ── Panel 3: RD processual — form requires approach ────────
def panel_processual(ax):
    ax.set_facecolor(BG)
    ax.axis('off')

    N = 60
    rng = np.random.default_rng(42)

    # Gray-Scott parameters: processual regime
    F, k = 0.022, 0.050
    Du, Dv = 0.16, 0.08
    dt = 1.0

    u = np.ones((N, N))
    v = np.zeros((N, N))
    # small random seed
    cx, cy = N//2, N//2
    u[cx-5:cx+5, cy-5:cy+5] = 0.5
    v[cx-5:cx+5, cy-5:cy+5] = 0.25
    u += rng.normal(0, 0.02, (N, N))
    v += rng.normal(0, 0.02, (N, N))
    u = np.clip(u, 0, 1)
    v = np.clip(v, 0, 1)

    def laplacian(Z):
        return (np.roll(Z,1,0)+np.roll(Z,-1,0)+np.roll(Z,1,1)+np.roll(Z,-1,1) - 4*Z)

    # Run for a moderate number of steps — still evolving, not settled
    for _ in range(6000):
        uvv = u * v * v
        u += dt * (Du * laplacian(u) - uvv + F*(1-u))
        v += dt * (Dv * laplacian(v) + uvv - (F+k)*v)
        u = np.clip(u, 0, 1)
        v = np.clip(v, 0, 1)

    im = ax.imshow(v, cmap='inferno', vmin=0, vmax=0.35,
                   interpolation='bilinear', aspect='equal')

    # Indicate still in motion
    ax.text(0.5, 0.97, "step 6,000 of ∞", transform=ax.transAxes,
            color=DIM, fontsize=7, ha='center', va='top',
            fontfamily='monospace')

    ax.set_title("RD processual", color=WHT, fontsize=9, pad=6,
                 fontfamily='monospace')
    ax.text(0.5, -0.06, "no form prior to approach\ngap is intrinsic — remove it, remove the form",
            transform=ax.transAxes, color=DIM, fontsize=7,
            ha='center', va='top', fontfamily='monospace', linespacing=1.6)


# ── Compose ────────────────────────────────────────────────
fig = plt.figure(figsize=(12, 5), facecolor=BG)
fig.subplots_adjust(top=0.82, bottom=0.16, left=0.04, right=0.96, wspace=0.08)

gs = gridspec.GridSpec(1, 3, figure=fig)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])

panel_fixed_point(ax1)
panel_limit_cycle(ax2)
panel_processual(ax3)

# Spectrum arrow across top
fig.text(0.5, 0.93, "extrinsic  ←────────────────────────────→  intrinsic",
         color=WHT, fontsize=9, ha='center', va='top',
         fontfamily='monospace', alpha=0.7)

fig.text(0.5, 0.88, "gap is: incidental       constitutive of type       constitutive of form",
         color=DIM, fontsize=8, ha='center', va='top',
         fontfamily='monospace')

plt.savefig("assets/gap-spectrum.png", dpi=140, bbox_inches='tight',
            facecolor=BG)
print("saved assets/gap-spectrum.png")
