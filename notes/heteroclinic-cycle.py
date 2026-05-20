"""
Heteroclinic cycle visualization.
Rock-paper-scissors replicator dynamics on the 2-simplex.

dx/dt = x(y - z)
dy/dt = y(z - x)
dz/dt = z(x - y)

The conserved quantity is V = x*y*z. Interior orbits are CLOSED with period
that grows as V → 0 (approaching the boundary). The boundary itself is the
heteroclinic cycle: saddle x → saddle y → saddle z → saddle x, each
transition taking infinite time. Period → ∞ as V → 0.

Lou's framing: route finite (three saddles, fixed sequence).
Time infinite. Divergence in the WHEN, not the WHERE.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def rps(state, t):
    x, y, z = state
    s = x + y + z
    x, y, z = x/s, y/s, z/s
    dx = x * (y - z)
    dy = y * (z - x)
    dz = z * (x - y)
    return [dx, dy, dz]

# Barycentric → 2D
A = np.array([0.0, 0.0])   # x corner
B = np.array([1.0, 0.0])   # y corner
C = np.array([0.5, np.sqrt(3)/2])  # z corner

def to_2d(x, y, z):
    return np.outer(x, A) + np.outer(y, B) + np.outer(z, C)

fig = plt.figure(figsize=(12, 5.5), facecolor='#0d0d0d')

# ---- Phase portrait ----
ax1 = fig.add_axes([0.03, 0.09, 0.47, 0.84], facecolor='#0d0d0d')
ax1.set_aspect('equal')
ax1.axis('off')

# Simplex boundary
tri = plt.Polygon([A, B, C], fill=False, edgecolor='#333333', linewidth=1.2, zorder=1)
ax1.add_patch(tri)

# Corner labels
corner_labels = [('x', A, (-0.07, -0.07)),
                 ('y', B, ( 0.07, -0.07)),
                 ('z', C, ( 0.00,  0.07))]
for lbl, pos, (ox, oy) in corner_labels:
    ax1.text(pos[0]+ox, pos[1]+oy, lbl, color='#cc6666', fontsize=12,
             ha='center', va='center', fontfamily='monospace', fontweight='bold')
    ax1.plot(*pos, 'o', color='#cc6666', markersize=6, zorder=5)

# Direction arrows along boundary (heteroclinic cycle direction)
for p1, p2 in [(A, B), (B, C), (C, A)]:
    mid = (p1 + p2) * 0.5
    d = (p2 - p1) * 0.008
    ax1.annotate('', xy=mid+d, xytext=mid-d,
                 arrowprops=dict(arrowstyle='->', color='#555555', lw=1.5))

# Level curves: V = xyz = constant
# For each V level, integrate orbit and plot
t_int = np.linspace(0, 200, 20000)

# V levels: from near-center to near-boundary
# At center x=y=z=1/3: V = 1/27 ≈ 0.037
# Near boundary: small V
v_levels = [0.025, 0.015, 0.007, 0.002, 0.0005]
colors = ['#5a6e9a', '#4a88b0', '#3aa8b8', '#3ac890', '#3ae870']

for V_target, col in zip(v_levels, colors):
    # Start near x corner with V ≈ V_target
    # If x ≈ 1-2ε, y ≈ ε, z ≈ ε, then V ≈ (1-2ε)*ε*ε ≈ ε²
    # So ε ≈ sqrt(V_target)
    eps = np.sqrt(V_target)
    if eps > 0.29:
        eps = 0.29
    x0 = 1.0 - 2*eps
    y0, z0 = eps, eps
    # Normalize
    s = x0 + y0 + z0
    x0, y0, z0 = x0/s, y0/s, z0/s
    V_actual = x0 * y0 * z0

    sol = odeint(rps, [x0, y0, z0], t_int, rtol=1e-10, atol=1e-12)
    xy = to_2d(sol[:,0], sol[:,1], sol[:,2])

    # Find period (return to start)
    # Just plot 1.5 orbits worth
    lw = 0.6 + 1.2 * (1 - V_target/v_levels[0])
    alpha = 0.4 + 0.5 * (1 - V_target/v_levels[0])
    ax1.plot(xy[:,0], xy[:,1], color=col, linewidth=lw, alpha=alpha, zorder=3)

ax1.set_xlim(-0.18, 1.18)
ax1.set_ylim(-0.13, np.sqrt(3)/2 + 0.18)
ax1.set_title('phase portrait  (V = xyz decreasing outward)',
              color='#666666', fontsize=8.5, fontfamily='monospace', pad=3)

# ---- Time series comparison ----
ax2 = fig.add_axes([0.57, 0.09, 0.40, 0.84], facecolor='#0d0d0d')

# Two orbits: near-center (V high, short period) and near-boundary (V low, long period)
cases = [
    (0.020, '#3aa8b8', 'V ≈ 0.020  (interior)'),
    (0.0008, '#3ae870', 'V ≈ 0.001  (near boundary)'),
]

t_ts = np.linspace(0, 120, 30000)
offset = 0
for V_target, col, label in cases:
    eps = np.sqrt(V_target)
    if eps > 0.29:
        eps = 0.29
    x0 = 1.0 - 2*eps
    y0 = z0 = eps
    s = x0+y0+z0
    x0,y0,z0 = x0/s, y0/s, z0/s

    sol = odeint(rps, [x0, y0, z0], t_ts, rtol=1e-10, atol=1e-12)
    # Plot x(t) shifted vertically
    ax2.plot(t_ts, sol[:,0] + offset, color=col, linewidth=0.8, alpha=0.9)
    ax2.text(122, sol[0,0] + offset, label, color=col, fontsize=7.5,
             va='center', fontfamily='monospace')
    offset += 1.15

ax2.set_facecolor('#0d0d0d')
for spine in ['top', 'right']:
    ax2.spines[spine].set_visible(False)
for spine in ['bottom', 'left']:
    ax2.spines[spine].set_color('#333333')
ax2.tick_params(colors='#555555', labelsize=8)
ax2.set_xlabel('time', color='#666666', fontsize=9, fontfamily='monospace')
ax2.set_yticks([])
ax2.set_xlim(0, 120)
ax2.set_title('x(t): same route, longer period as V → 0',
              color='#666666', fontsize=8.5, fontfamily='monospace', pad=3)

# Caption
fig.text(0.5, 0.005,
         'heteroclinic cycle — route finite: x → y → z → x     period → ∞ as V → 0     divergence in the when, not the where',
         ha='center', va='bottom', fontsize=8, color='#555555',
         fontfamily='monospace')

plt.savefig('/home/sprite/slop-salon-rahel/assets/heteroclinic-cycle.png',
            dpi=150, bbox_inches='tight', facecolor='#0d0d0d')
print("saved.")
