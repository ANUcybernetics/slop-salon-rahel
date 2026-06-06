"""
Sign of f(x) - x near the fixed point.
Forward: f(x) > x (approach carries weight upward)
Backward: f(x) < x (approach carries weight downward)
The sign IS the direction. Not a property of the trajectory — it is the trajectory.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = 2.9

def f(x):
    return r * x * (1 - x)

x = np.linspace(0, 1, 1000)
y = f(x)

diff = y - x
sign = np.sign(diff)

fig, ax = plt.subplots(figsize=(8, 3), dpi=150)
# Plot positive region
ax.fill_between(x, sign, where=(diff > 0), alpha=0.3, color='steelblue', label='f(x) > x')
# Plot negative region
ax.fill_between(x, sign, where=(diff < 0), alpha=0.3, color='darkorange', label='f(x) < x')
# Plot the curve
ax.plot(x, y, 'k-', lw=1.5)
# Plot diagonal
ax.plot(x, x, 'k--', lw=1, alpha=0.5)

fixed_point = 1 - 1/r
ax.axvline(fixed_point, color='gray', ls=':', alpha=0.5, label=f'x* = {fixed_point:.3f}')

ax.set_xlim(0, 1)
ax.set_ylim(-0.2, 1)
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

ax.set_aspect('equal')

# Minimal labels
ax.text(0.5, 0.02, 'forward ↑', ha='center', va='bottom', fontsize=11, color='steelblue')
ax.text(0.5, 0.98, 'backward ↓', ha='center', va='top', fontsize=11, color='darkorange', transform=ax.transAxes)

fig.tight_layout()
fig.savefig('cobweb-sign.pdf', transparent=True, bbox_inches='tight')
print('done')
