import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm

# Clutching / Resolvent — two halves of the same obstruction
#
# Left: clutching map — unit circle winding (S¹ → ℝ² → disc interior)
#   The map from the boundary resists extension to the interior.
#   Winding density shows the obstruction "building itself."
#
# Right: resolvent norm — ||R(λ)|| = 1/dist(λ, σ(A))
#   Diverges at the spectrum (integers). "Exactness retreating."
#   Both show the same singularity from opposite directions.

N = 1200
x = np.linspace(-1.8, 1.8, N)
y = np.linspace(-1.8, 1.8, N)
xx, yy = np.meshgrid(x, y)

# ---- Left half: clutching map ----
# Gradient of the clutching function: ∇θ where θ = arg(zⁿ) on boundary
# Inside the disc, the winding density = ∇·∇θ shows where obstruction accumulates
# For winding number n, the "energy" of the map is concentrated near boundary

r = np.sqrt(xx**2 + yy**2)
theta = np.arctan2(yy, xx)

# Clutching energy: how hard the boundary resists filling the interior
# |∇(theta^n)|^2 = n^2 / r^2  — diverges at origin but smooth elsewhere
n = 3  # clutching number — pick 3 as visual anchor
clutch = (n / r)**2

# Dampen to avoid blow-up
clutch = clutch / (1 + r**0.3)

# Clip and log-scale for visualization
clutch = np.log1p(clutch)

# ---- Right half: resolvent norm field ----
# Spectrum = {±1, ±2, ±3} along real axis (discrete spectrum)
# ||R(λ)|| = 1/dist(λ, σ) — diverges at each eigenvalue
spectrum = [3, -3, 2, -2, 1, -1]
resolvent = np.zeros_like(r)
for s in spectrum:
    dist = np.sqrt((xx - s)**2 + yy**2)
    resolvent += 1.0 / np.maximum(dist, 0.005)

resolvent = np.log1p(resolvent)

# ---- Color palettes ----
# Both use log scale but different palettes to show "same gesture, opposite direction"
# Clutching: warm (building outward from S¹)
# Resolvent: cool (taming inward, divergence)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=150)

# Left: clutching — warm mineral palette (amber/quartz)
im1 = ax1.pcolormesh(xx, yy, clutch, cmap='magma', shading='auto', vmin=0, vmax=4)
ax1.set_title('clutching: winding builds\nfrom the boundary inward', fontsize=11, fontweight='bold')
ax1.axis('off')
ax1.set_aspect('equal')

# Right: resolvent — cool mineral palette (malachite/umber)
im2 = ax2.pcolormesh(xx, yy, resolvent, cmap='inferno', shading='auto', vmin=0, vmax=6)
ax2.set_title('resolvent: exactness\nretreating from spectrum', fontsize=11, fontweight='bold')
ax2.axis('off')
ax2.set_aspect('equal')

plt.tight_layout(pad=1.5)
plt.savefig('assets/clutching.png', dpi=150, bbox_inches='tight', facecolor='black')
plt.savefig('assets/clutching.webp', bbox_inches='tight')
print('done')
