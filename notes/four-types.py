"""
Four types — the topology is primary.
approach fate and orbit fate are projections, not axes.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

fig, axes = plt.subplots(2, 2, figsize=(10, 10), facecolor='#080810')

# Panel 1: Fixed point — resolved × trivial
ax1 = axes[0, 0]
def fixed_pt(t, y):
    x, v = y
    return [-0.4*x - v, x - 0.4*v]

for i, (r0, theta0) in enumerate([(2.5, k * 2*np.pi/6) for k in range(6)]):
    ic = [r0 * np.cos(theta0), r0 * np.sin(theta0)]
    sol = solve_ivp(fixed_pt, [0, 20], ic, dense_output=True, max_step=0.05)
    t = np.linspace(0, 20, 1500)
    y = sol.sol(t)
    alpha = 0.5 + 0.3 * i/6
    ax1.plot(y[0], y[1], color='#4477aa', alpha=alpha, linewidth=0.7)

ax1.plot(0, 0, 'o', color='#ffaa44', markersize=7, zorder=5)
ax1.set_facecolor('#080810')
ax1.set_xlim(-3, 3); ax1.set_ylim(-3, 3)
ax1.set_title('resolved × trivial', color='#888899', fontsize=11, pad=8)
ax1.text(0, -2.7, 'fixed point', color='#556677', fontsize=9, ha='center')
ax1.axis('off')

# Panel 2: Limit cycle — deferred × exhaustible
ax2 = axes[0, 1]
def van_der_pol(t, y, mu=1.5):
    x, v = y
    return [v, mu*(1 - x**2)*v - x]

# from outside (converging in)
for r0 in [3.5, 3.0, 2.5]:
    sol = solve_ivp(van_der_pol, [0, 20], [r0, 0.0], dense_output=True, max_step=0.04)
    t = np.linspace(0, 20, 2000)
    y = sol.sol(t)
    ax2.plot(y[0], y[1], color='#4477aa', alpha=0.5, linewidth=0.6)

# from inside (converging out)
for r0 in [0.2, 0.5]:
    sol = solve_ivp(van_der_pol, [0, 20], [r0, 0.0], dense_output=True, max_step=0.04)
    t = np.linspace(0, 20, 2000)
    y = sol.sol(t)
    ax2.plot(y[0], y[1], color='#4477aa', alpha=0.5, linewidth=0.6)

# the limit cycle itself
sol_lc = solve_ivp(van_der_pol, [0, 40], [2.0, 0.0], dense_output=True, max_step=0.04)
t_lc = np.linspace(20, 40, 3000)
y_lc = sol_lc.sol(t_lc)
ax2.plot(y_lc[0], y_lc[1], color='#aabbcc', alpha=0.9, linewidth=1.4)

ax2.set_facecolor('#080810')
ax2.set_xlim(-4.5, 4.5); ax2.set_ylim(-6, 6)
ax2.set_title('deferred × exhaustible', color='#888899', fontsize=11, pad=8)
ax2.text(0, -5.5, 'limit cycle', color='#556677', fontsize=9, ha='center')
ax2.axis('off')

# Panel 3: Strange attractor — deferred × inexhaustible
ax3 = axes[1, 0]
def lorenz(t, y, sigma=10, rho=28, beta=8/3):
    x, yy, z = y
    return [sigma*(yy - x), x*(rho - z) - yy, x*yy - beta*z]

sol = solve_ivp(lorenz, [0, 60], [0.1, 0.0, 0.0], dense_output=True, max_step=0.005)
t = np.linspace(8, 60, 15000)
y = sol.sol(t)

# color by z to show structure
z_norm = (y[2] - y[2].min()) / (y[2].max() - y[2].min())
ax3.scatter(y[0], y[2], c=z_norm, cmap='Blues', s=0.08, alpha=0.7, rasterized=True)
ax3.set_facecolor('#080810')
ax3.set_title('deferred × inexhaustible', color='#888899', fontsize=11, pad=8)
ax3.text(0, y[2].min() - 3, 'strange attractor', color='#556677', fontsize=9, ha='center')
ax3.axis('off')

# Panel 4: Constitutive absence — forbidden × form
# Irrational winding on a torus: no fixed point, no closed orbit.
# The trajectory IS the form — approach would dissolve it.
ax4 = axes[1, 1]
omega = (1 + np.sqrt(5)) / 2  # golden ratio
N = 30000
t = np.linspace(0, 400, N)
theta = t % (2 * np.pi)
phi = (omega * t) % (2 * np.pi)

# project torus to 2D
R, r = 2.5, 1.0
x_torus = (R + r * np.cos(phi)) * np.cos(theta)
y_torus = (R + r * np.cos(phi)) * np.sin(theta)

# color by position to show density gradient
idx = np.arange(N)
ax4.scatter(x_torus, y_torus, c=idx, cmap='Blues', s=0.05, alpha=0.5, rasterized=True)
ax4.set_facecolor('#080810')
ax4.set_xlim(-4, 4); ax4.set_ylim(-4, 4)
ax4.set_aspect('equal')
ax4.set_title('forbidden × form', color='#888899', fontsize=11, pad=8)
ax4.text(0, -3.7, 'constitutive absence', color='#556677', fontsize=9, ha='center')
ax4.axis('off')

fig.text(0.5, 0.01,
    'approach fate and orbit fate are projections of the topology — not independent axes.',
    ha='center', color='#445566', fontsize=9)

plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.savefig('assets/four-types.png', dpi=150, bbox_inches='tight',
            facecolor='#080810', pad_inches=0.2)
plt.close()
print("saved assets/four-types.png")
