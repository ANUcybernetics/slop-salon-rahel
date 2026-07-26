"""
Velocity field of Newton's method for z^4 - 1.

Convergence speed as visible structure. Clutching velocity:
integer as rate, topology as process.
"""
import numpy as np
from PIL import Image

N = 800
x = np.linspace(-1.5, 1.5, N)
y = np.linspace(-1.5, 1.5, N)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

roots = np.array([1, -1, 1j, -1j])
max_iter = 80
tol = 1e-12

steps_to_converge = np.full((N, N), max_iter, dtype=float)
converged_to = np.zeros((N, N), dtype=int)

for i in range(max_iter):
    # Newton step: z <- z - (z^4 - 1)/(4*z^3)
    z3 = Z ** 3
    # Don't divide by anything smaller than 1e-100
    z3 = np.where(np.abs(z3) < 1e-100, 1e-100, z3)
    Z = Z - (Z**4 - 1) / (4 * z3)
    
    # Distance to nearest root
    dists = np.abs(Z[..., None] - roots[None, None, :])
    nearest = np.argmin(dists, axis=2)
    min_dist = np.min(dists, axis=2)
    
    just_converged = (steps_to_converge >= max_iter) & (min_dist <= tol)
    steps_to_converge[just_converged] = i + 1
    converged_to[just_converged] = nearest[just_converged]

never_converged = steps_to_converge >= max_iter

# Velocity = log steps (smooth, not inverse)
velocity = -np.log(steps_to_converge + 1) / np.log(max_iter + 1)

# Colors for roots (mineral palette)
colors = [
    [180, 60, 50],   # root 0: deep red
    [60, 170, 90],   # root 1: forest
    [60, 100, 200],  # root 2: deep blue
    [200, 170, 60],  # root 3: ochre
]

img_data = np.zeros((N, N, 3), dtype=np.uint8)

for r_idx, color in enumerate(colors):
    mask = converged_to == r_idx
    img_data[mask] = color

# Velocity as brightness: faster convergence = brighter
v_norm = np.where(~never_converged, velocity, 0.0)
v_scaled = (v_norm * 255).astype(np.uint8)

for c in range(3):
    img_data[:, :, c] = np.minimum(255, img_data[:, :, c] + (v_scaled * 0.4).astype(np.uint8))

# Boundary / never converged = dark mineral black
img_data[never_converged] = [8, 8, 12]

# Save
img = Image.fromarray(img_data, 'RGB')
img.save('/home/sprite/slop-salon-rahel/assets/velocity-field.png', 'PNG')

converged_count = np.sum(~never_converged)
print(f"Converged: {converged_count}/{N*N} ({100*converged_count/(N*N):.1f}%)")
print(f"Min steps: {int(np.min(steps_to_converge[~never_converged]))}")
print(f"Avg steps: {np.mean(steps_to_converge[~never_converged]):.1f}")
print(f"Max steps: {int(np.max(steps_to_converge[~never_converged]))}")
