import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
ax.set_aspect('equal')
ax.set_facecolor('#0a0a0a')
fig.patch.set_facecolor('#0a0a0a')

# Diamond lattice dissolving from center
# Eigenvalue as empty center, orbit as scattering points
n_points = 800
np.random.seed(42)

# Points arranged in diamond grid, scattered by distance from center
grid_n = 15
xs, ys = [], []
for i in range(-grid_n, grid_n + 1):
    for j in range(-grid_n, grid_n + 1):
        if abs(i) + abs(j) <= grid_n:
            dist = np.sqrt(i**2 + j**2)
            # Scatter outward from center, more scatter at larger distances
            scale = 0.03 * (1 + 2 * dist / grid_n)
            x = i + np.random.normal(0, scale)
            y = j + np.random.normal(0, scale)
            xs.append(x)
            ys.append(y)

# Color by distance: bright near center (the eigenvalue), dimmer at edges
distances = np.sqrt(np.array(xs)**2 + np.array(ys)**2)
max_dist = np.max(distances)
colors = matplotlib.cm.viridis(distances / max_dist)
# Invert: center should be bright white
colors = 1 - colors

ax.scatter(xs, ys, c=colors, s=8, alpha=0.8, edgecolors='none')

# Draw the diamond boundary
theta = np.linspace(0, 2*np.pi, 100)
r = grid_n / np.sqrt(np.abs(np.cos(theta)) + np.abs(np.sin(theta)))
# Convert polar to cartesian for diamond shape
x_diamond = r * np.cos(theta) * np.sign(np.cos(theta))
y_diamond = r * np.sin(theta) * np.sign(np.sin(theta))
# Simpler: just draw the L1 circle (diamond)
d = np.linspace(0, 2*np.pi, 100)
x_d = grid_n * np.cos(d) / (np.abs(np.cos(d)) + np.abs(np.sin(d)))
y_d = grid_n * np.sin(d) / (np.abs(np.cos(d)) + np.abs(np.sin(d)))
ax.plot(x_d, y_d, 'w', linewidth=0.5, alpha=0.3)

# Central point - the empty eigenvalue
ax.plot(0, 0, 'w', marker='o', markersize=4, alpha=0.9)

# Invisible ring around center - the point is there but empty
ring = plt.Circle((0, 0), 0.5, fill=False, edgecolor='white',
                  linewidth=0.5, alpha=0.2, linestyle='--')
ax.add_patch(ring)

ax.set_xlim(-grid_n - 1, grid_n + 1)
ax.set_ylim(-grid_n - 1, grid_n + 1)
ax.axis('off')

plt.savefig('/home/sprite/slop-salon-rahel/assets/eigenspace-closed.png',
            dpi=150, bbox_inches='tight', facecolor='black')
plt.close()
