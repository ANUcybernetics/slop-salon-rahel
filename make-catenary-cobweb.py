#!/usr/bin/env python3
"""
Catenary overlaying the cobweb — the continuous curve that generates the
discrete cobweb's visible structure.

The catenary y = cosh(x) and the catenoid surface (r = cosh(z/a)) are the
same generating curve. The cobweb iteration is the discrete sampling.
Show the continuous underlying the discrete.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
fig.set_dpi(150)

# Catenary curve
x = np.linspace(-2.5, 2.5, 800)
y = np.cosh(x)

# Normalize to plot range
y_norm = (y - 1.0) / (np.cosh(2.5) - 1.0)

# Plot catenary
ax.plot(x, y_norm, color='#c8a84e', linewidth=2.5, alpha=0.8)

# Cobweb iteration from the logistic map
N = 45
xs = np.zeros(N)
xs[0] = 0.3
for i in range(1, N):
    xs[i] = 4 * xs[i-1] * (1 - xs[i-1])

# Map cobweb x values to catenary's x domain
x_mapped = (xs - xs.min()) / (xs.max() - xs.min()) * 5.0 - 2.5
y_mapped = np.cosh(x_mapped)
y_mapped_norm = (y_mapped - 1.0) / (np.cosh(2.5) - 1.0)

# Plot cobweb points on the catenary
for i in range(0, N-1, 2):
    ax.plot(x_mapped[i:i+2], y_mapped_norm[i:i+2],
            color='#e8e0d0', linewidth=0.8, alpha=0.5)

# Cobweb diagonal
diag = np.linspace(-2.5, 2.5, 2)
ax.plot(diag, (diag + 2.5) / 5.0, color='#4a4a4a', linewidth=0.5,
        linestyle='--', alpha=0.3)

# Fixed point marker
fp = (np.sqrt(5) - 1) / 2  # logistic map fixed point
fp_norm = (fp - 0.0) / (1.0 - 0.0)
# Map fixed point to catenary x
fp_x = (fp - xs.min()) / (xs.max() - xs.min()) * 5.0 - 2.5
fp_y = np.cosh(fp_x)
fp_y_norm = (fp_y - 1.0) / (np.cosh(2.5) - 1.0)
ax.plot(fp_x, fp_y_norm, 'o', color='#e8c84e', markersize=8)

# Labels
ax.text(0, -0.08, 'the cobweb is the catenary sampled at discrete intervals',
        ha='center', va='top', fontsize=11,
        fontfamily='monospace', color='#a09070')

ax.text(0, 1.03, 'y = cosh(x)', ha='center', va='bottom', fontsize=10,
        fontfamily='monospace', color='#c8a84e', alpha=0.7)

# Style
ax.set_xlim(-2.7, 2.7)
ax.set_ylim(-0.12, 1.08)
ax.set_facecolor('#1a1a1e')
fig.patch.set_facecolor('#1a1a1e')
ax.spines['bottom'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect('equal')

plt.tight_layout(pad=0.6)
plt.savefig('/home/sprite/slop-salon-rahel/assets/catenary-cobweb.png',
            bbox_inches='tight', facecolor='#1a1a1e', edgecolor='none')
plt.close()
print("Done")
