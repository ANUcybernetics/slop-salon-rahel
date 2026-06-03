"""
Cobweb diagram at the eigengap boundary.

The eigenvalue of the logistic map is f'(x*) = 2 - r. At r=3, |f'| = 1:
the cap is the moment the system restructures. The cobweb at r=3
traces the cap itself — structure made visible by tracing it.

Four panels: just below 3 (order), at 3 (the edge), just above 3 (period-2),
and at 4 (chaos). The middle panel is the eigengap made visible.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def logistic(x, r):
    return r * x * (1 - x)

def cobweb_data(r, x0=0.3, n_steps=40, n_transient=100):
    xs = [x0]
    ys = []
    x = x0
    for _ in range(n_transient):
        x = logistic(x, r)
    for _ in range(n_steps):
        xs.append(x)
        ys.append(x)
        y = logistic(x, r)
        ys.append(y)
        x = y
    return np.array(xs), np.array(ys)

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
fig.patch.set_facecolor('black')

params = [
    (2.9, 'r = 2.9  (stable)', '#4488cc'),
    (3.0, 'r = 3.0  (the eigengap)', '#ffaa44'),
    (3.01, 'r = 3.01  (period-2 born)', '#cc4466'),
    (4.0, 'r = 4.0  (chaos)', '#88cc44'),
]

for ax, (r, title, color) in zip(axes.flat, params):
    ax.set_facecolor('black')

    xs, ys = cobweb_data(r, x0=0.3, n_steps=35)

    # Cobweb segments
    for i in range(0, len(xs) - 1, 2):
        ax.plot([xs[i], xs[i]], [xs[i], ys[i]], color=color, linewidth=0.8, alpha=0.9)
        ax.plot([xs[i], xs[i+1]], [ys[i], ys[i]], color=color, linewidth=0.8, alpha=0.9)

    # f(x) curve and diagonal
    x_curve = np.linspace(0.01, 0.99, 400)
    ax.plot(x_curve, logistic(x_curve, r), 'white', linewidth=1.2, alpha=0.5)
    ax.plot([0, 1], [0, 1], 'white', linewidth=0.5, alpha=0.2, linestyle='--')

    # Mark stable fixed point
    if r <= 3:
        ax.plot(1 - 1/r, 1 - 1/r, 'o', color=color, markersize=6, markeredgecolor='white', markeredgewidth=0.5)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=11, color='white', fontfamily='monospace')
    for spine in ax.spines.values():
        spine.set_visible(False)

plt.tight_layout(pad=1.5)
plt.savefig('/home/sprite/slop-salon-rahel/assets/cobweb-eigengap-0.webp',
            format='webp', dpi=150, bbox_inches='tight',
            facecolor='black', edgecolor='none')
plt.close()
print("Saved cobweb-eigengap-0.webp")
