import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Mina's insight: exhaustion implies a clock. density is a ratio; exhaustion is a rate.
# Three clocks showing the same constraint at different speeds:
# 1. Cobweb iteration — error decay per iteration (eigenvalue clock)
# 2. Phyllotaxis — primordium number (geometric clock)
# 3. Amber — layer deposition time (temporal clock)

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.suptitle('exhaustion implies a clock', fontsize=16, fontweight='bold')

# --- 1. Cobweb: iteration count as clock ---
ax = axes[0]
r = 3.1
x0 = 0.5
x = x0
errors = []
for i in range(50):
    y = r * x * (1 - x)
    errors.append(abs(y - x))
    x = y

ax.plot(errors, 'b-', lw=2, alpha=0.8)
ax.axhline(0, color='k', lw=0.5, alpha=0.3)
ax.set_yscale('log')
ax.set_xlabel('iteration n (the clock)')
ax.set_ylabel('|f(x) − x|  (distance to diagonal)')
ax.set_title('cobweb: error per tick\n(eigenvalue clock, |f\'| = 0.9)')
ax.grid(alpha=0.3)

# Mark where error drops below different thresholds
thresholds = [0.1, 0.01, 0.001, 1e-4]
for t in thresholds:
    idx = np.where(np.array(errors) < t)[0]
    if len(idx) > 0:
        ax.annotate('', xy=(idx[0], t*5), xytext=(idx[0]-3, t*5),
                    arrowprops=dict(arrowstyle='<->', color='orange', lw=0.8))
        ax.text(idx[0]-3, t*0.3, f'n={idx[0]}', fontsize=6, color='orange')

# --- 2. Phyllotaxis: primordium number as clock ---
ax = axes[1]
angle = 137.508 * np.pi / 180  # golden angle in radians
r_cart = 0.15  # base spacing
primordia = list(range(1, 201))
x_coords = []
y_coords = []
for p in primordia:
    x_coords.append(r_cart * np.sqrt(p) * np.cos(p * angle))
    y_coords.append(r_cart * np.sqrt(p) * np.sin(p * angle))

ax.scatter(x_coords, y_coords, s=8, c='goldenrod', edgecolors='sandybrown', linewidths=0.3)
ax.set_aspect(1)
ax.set_xlabel('primordium number n (the clock)')
ax.set_ylabel('position')
ax.set_title('phyllotaxis: position per primordium\ngolden angle clock, 137.5°')
ax.set_xlim(-0.8, 0.8)
ax.set_ylim(-0.8, 0.8)

# Mark the "exhaustion" — when the spiral resolves into radial lines
ax.axhline(0, color='k', lw=0.3, alpha=0.2)
ax.axvline(0, color='k', lw=0.3, alpha=0.2)

# --- 3. Amber: layer number as clock (coarse visualization of solidification) ---
ax = axes[2]
# Concentric hexagonal layers, each representing a deposition event
# Layer k has circumference ~ k, so each layer needs k deposits
n_layers = 40
colors = []
positions_x, positions_y = [], []

for layer in range(n_layers):
    radius = layer * 0.025
    n_sectors = max(3, int(2 * np.pi * radius / 0.02))
    angles = np.linspace(0, 2*np.pi, n_sectors + 1)
    for a in angles[:-1]:
        positions_x.append(radius * np.cos(a))
        positions_y.append(radius * np.sin(a))
        # Color by "deposition time" (layer number → intensity)
        colors.append(layer / n_layers)

scatter = ax.scatter(positions_x, positions_y, c=colors, cmap='YlOrBr',
                     s=6, edgecolors='none', alpha=0.8)
ax.set_aspect(1)
ax.set_xlabel('layer number n (the clock)')
ax.set_ylabel('position')
ax.set_title('amber: layer per deposition\n(solidification clock)')
ax.set_xlim(-1.0, 1.0)
ax.set_ylim(-1.0, 1.0)
ax.axis('off')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-rahel/assets/clock-as-ratio.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print('done — clock-as-ratio.png')
