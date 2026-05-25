import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Cobweb plot for r=3 (period-2 orbit — diagonal intersects f at two off-diagonal points
# The key insight: at r=3 the cobweb "thickens" to zero at the intersection
# — the distance to diagonal IS the error, and it shrinks to zero
# at the bifurcation point, that distance becomes legible

r = 3.0
x0 = np.linspace(0.01, 0.99, 1000)
f = r * x0 * (1 - x0)

# Fixed point
x_star = 1 - 1/r  # = 2/3 for r=3

fig, axes = plt.subplots(2, 2, figsize=(10, 10))
fig.suptitle(f'r = {r} — the diagonal becomes legible', fontsize=14, fontweight='bold')

# 1. Full cobweb — many iterations
ax = axes[0, 0]
x = 0.3
x_vals = [x]
y_vals = [0]
for i in range(60):
    y = r * x * (1 - x)
    x_vals.extend([x, x])
    y_vals.extend([y, y])
    x = y
    x_vals.append(x)
    y_vals.append(0)

ax.plot(x0, f, 'k-', lw=1.5, label='f(x)')
ax.plot(x0, x0, 'r--', lw=1.0, alpha=0.7, label='diagonal')
ax.plot(x_vals, y_vals, 'b-', lw=0.6, alpha=0.5)
ax.axvline(x_star, color='orange', linestyle=':', alpha=0.5, label=f'x* = {x_star:.3f}')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect(1)
ax.legend(fontsize=7)
ax.set_title('cobweb — 60 iterations')
ax.set_xlabel('xₙ')
ax.set_ylabel('xₙ₊₁')

# 2. Zoom: error = distance to diagonal (the "meter stick")
ax = axes[0, 1]
n_zoom = 20
x = 0.3
errors = []
for i in range(n_zoom):
    y = r * x * (1 - x)
    error = abs(y - x)  # distance to diagonal
    errors.append(error)
    x = y

ax.plot(range(n_zoom), errors, 'b-', lw=1.5, marker='o', markersize=4)
ax.set_xlabel('iteration')
ax.set_ylabel('|f(x) − x|  (distance to diagonal)')
ax.set_title('error decay — the diagonal as meter stick')
ax.set_yscale('log')
ax.grid(alpha=0.3)

# 3. Zoom cobweb around x*
ax = axes[1, 0]
x_start = x_star - 0.1
x_zoom = np.linspace(x_start, x_star + 0.1, 500)
f_zoom = r * x_zoom * (1 - x_zoom)

x_trace = [x_star - 0.08]
for i in range(30):
    y = r * x_trace[-1] * (1 - x_trace[-1])
    x_trace.extend([x_trace[-1], y])
    x_trace.append(y)

ax.plot(x_zoom, f_zoom, 'k-', lw=1.5)
ax.plot(x_zoom, x_zoom, 'r--', lw=1.0, alpha=0.7)
ax.plot(x_trace, x_trace if len(x_trace) == len(f_zoom) else [f_zoom[i] if i < len(f_zoom) else 0 for i in range(len(x_trace))], 'b-', lw=0.8, alpha=0.6)
# Simpler cobweb trace for zoom
ax2 = ax.twinx()
ax2.plot(x_trace, np.array([r * xi * (1 - xi) for xi in x_trace]) if len(x_trace) > 0 else [], 'b-', lw=0.8, alpha=0.6)
ax.set_xlim(x_star - 0.12, x_star + 0.12)
ax.set_ylim(x_star - 0.12, x_star + 0.12)
ax.set_aspect(1)
ax.set_title('zoom around x* — cobweb tightening')
ax.set_xlabel('xₙ')
ax.set_ylabel('xₙ₊₁')

# 4. The cobweb thickness as function of r (near bifurcation)
ax = axes[1, 1]
rs = np.linspace(2.0, 3.5, 300)
x_star_line = 1 - 1/rs
# derivative at fixed point: f'(x*) = 2 - r
deriv = 2 - rs

ax.plot(rs, deriv, 'b-', lw=2)
ax.axhline(0, color='k', lw=0.5)
ax.axvline(3, color='orange', linestyle='--', alpha=0.7, label='bifurcation r=3')
ax.set_xlabel('r')
ax.set_ylabel("f'(x*) at fixed point")
ax.set_title('cobweb thickness → 0 as r → 3')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
ax.set_ylim(-1.5, 1.5)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-rahel/assets/cobweb-legible.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print('done')
