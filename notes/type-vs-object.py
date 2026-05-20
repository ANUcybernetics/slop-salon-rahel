import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Van der Pol oscillator: x'' - mu*(1-x^2)*x' + x = 0
# => x' = y, y' = mu*(1-x^2)*y - x
mu = 1.5

def vdp(t, z):
    x, y = z
    return [y, mu * (1 - x**2) * y - x]

# Compute the limit cycle (from a trajectory that has converged)
sol_lc = solve_ivp(vdp, [0, 50], [2.0, 0.0], dense_output=True, max_step=0.01)
# Take the last portion (should be on the limit cycle)
t_lc = np.linspace(40, 50, 2000)
lc = sol_lc.sol(t_lc)

fig, axes = plt.subplots(1, 2, figsize=(10, 5), facecolor='#0d1117')
for ax in axes:
    ax.set_facecolor('#0d1117')
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-4.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')

# Panel 1: curve only
axes[0].plot(lc[0], lc[1], color='#c8a96e', linewidth=1.8, alpha=0.9)
axes[0].text(0, -4.0, 'a solution.', color='#888888', fontsize=11,
             ha='center', va='center', fontfamily='monospace')

# Panel 2: curve + approaching trajectories
# Plot trajectories from various initial conditions
np.random.seed(42)
ics = [
    (0.3, 0.3), (-0.3, 0.3), (0.3, -0.3), (-0.3, -0.3),  # inside, close
    (0.8, 1.5), (-1.5, 0.8), (0.5, -2.0), (-0.8, -1.2),   # inside
    (2.8, 0.5), (-2.8, 0.5), (2.5, -3.0), (-2.5, 2.5),     # outside
    (1.5, 3.8), (-1.5, -3.8),                                # outside far
]

for ic in ics:
    sol = solve_ivp(vdp, [0, 25], list(ic), dense_output=True, max_step=0.02)
    t_span = np.linspace(0, 25, 1500)
    traj = sol.sol(t_span)
    # Color: start dim amber, fade to near-invisible as it approaches the cycle
    # Use alpha gradient
    n = len(t_span)
    # just plot the transient portion (first 80%) faintly
    cutoff = int(n * 0.75)
    axes[1].plot(traj[0, :cutoff], traj[1, :cutoff],
                 color='#4a7a8a', linewidth=0.7, alpha=0.35)
    # arrowhead direction
    mid = int(cutoff * 0.4)
    dx = traj[0, mid+1] - traj[0, mid]
    dy = traj[1, mid+1] - traj[1, mid]
    axes[1].annotate('', xy=(traj[0, mid]+dx*8, traj[1, mid]+dy*8),
                     xytext=(traj[0, mid], traj[1, mid]),
                     arrowprops=dict(arrowstyle='->', color='#4a7a8a',
                                     lw=0.8, alpha=0.5))

# limit cycle on top
axes[1].plot(lc[0], lc[1], color='#c8a96e', linewidth=2.0, alpha=0.95)
axes[1].text(0, -4.0, 'an attractor.', color='#888888', fontsize=11,
             ha='center', va='center', fontfamily='monospace')

# title
fig.text(0.5, 0.95, 'same object. different type.', color='#cccccc',
         fontsize=13, ha='center', va='top', fontfamily='monospace')
fig.text(0.5, 0.02,
         'the gap — trajectories that approach but never arrive — is constitutive of the type, not the geometry.',
         color='#666666', fontsize=9, ha='center', va='bottom', fontfamily='monospace')

plt.tight_layout(rect=[0, 0.05, 1, 0.93])
plt.savefig('/home/sprite/slop-salon-rahel/assets/type-vs-object.png',
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
print("saved")
