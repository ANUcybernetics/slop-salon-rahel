"""Cavity as process: dissolution outward.
Each particle starts at a lattice point inside, moves outward,
leaving a trail. The shell is the accumulation of trajectories
that chose to exit. What remains behind is the cavity.
"""

import numpy as np
from PIL import Image, ImageDraw

np.random.seed(42)

W, H = 512, 512
center = (W // 2, H // 2)
radius = 200

def make_field(n=12):
    """Outward radial field with grain boundaries as subtle channels."""
    x = np.linspace(-1, 1, W)
    y = np.linspace(-1, 1, H)
    X, Y = np.meshgrid(x, y)

    R = np.sqrt(X**2 + Y**2) + 0.01
    theta = np.arctan2(Y, X)

    # Radial outward base field
    fx_base = X / R
    fy_base = Y / R

    # Grain centers — well-spaced around the field
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    grain_r = np.linspace(0.15, 0.6, n)
    grain_x = grain_r * np.cos(angles + np.random.randn(n) * 0.1)
    grain_y = grain_r * np.sin(angles + np.random.randn(n) * 0.1)

    # Create grain channels: additive perturbation that steers flow
    fx = fx_base.copy()
    fy = fy_base.copy()

    for gx, gy in zip(grain_x, grain_y):
        dx = X - gx
        dy = Y - gy
        d = np.sqrt(dx**2 + dy**2) + 0.01
        # Channel: slight angular perturbation that decays with distance
        angle_perturb = np.exp(-d**2 / 0.12)
        fx += -np.sin(theta) * angle_perturb * 0.3
        fy += np.cos(theta) * angle_perturb * 0.3

    # Normalize field
    norm = np.sqrt(fx**2 + fy**2) + 1e-10
    fx = fx / norm
    fy = fy / norm

    return fx, fy

fx, fy = make_field(n=10)

# Trace trajectories from random interior points
num_particles = 3000
trails = []

for _ in range(num_particles):
    # Start at random point inside radius
    angle = np.random.uniform(0, 2*np.pi)
    r = np.random.uniform(0, radius / W * 0.9)
    x = W/2 + r * np.cos(angle)
    y = H/2 + r * np.sin(angle)

    trail = [(int(x), int(y))]
    step = 0.8
    for _ in range(200):
        ix = int(np.clip(x, 0, W-1))
        iy = int(np.clip(y, 0, H-1))
        field_x = fx[iy, ix]
        field_y = fy[iy, ix]

        x += field_x * step
        y += field_y * step

        if (x - W/2)**2 + (y - H/2)**2 > (radius - 5)**2:
            # Exited — this trajectory formed the shell
            trail.append((int(x), int(y)))
            break

        if step % 3 == 0:
            trail.append((int(x), int(y)))
        step += 0.02

    trails.append(trail)

# Render: dark background, golden trails
img = Image.new('RGB', (W, H), (8, 8, 12))
draw = ImageDraw.Draw(img)

for trail in trails:
    if len(trail) < 2:
        continue

    # Color based on trail length (proxy for "depth" of origin)
    depth = min(len(trail) / 50, 1.0)
    gold = int(180 + 75 * depth)
    green = int(80 + 40 * depth)
    dim = int(30 + 20 * depth)

    for i in range(1, len(trail)):
        thickness = max(0.3, 1.0 - i / len(trail) * 0.7)
        draw.line(
            [trail[i-1], trail[i]],
            fill=(dim, int(green*0.6), dim),
            width=1
        )

    # Brighter at exit point (shell formation)
    if len(trail) > 5:
        exit_pt = trail[-3:]
        draw.line(
            [exit_pt[0], exit_pt[1], exit_pt[2]],
            fill=(gold, green, dim),
            width=2
        )

# Add subtle shell outline
for angle in np.linspace(0, 2*np.pi, 360):
    r = radius + 3 * np.sin(16 * angle) + 2 * np.cos(23 * angle)
    x = int(W/2 + r * np.cos(angle))
    y = int(H/2 + r * np.sin(angle))
    draw.point([x, y], fill=(gold, green, dim))

img.save('assets/cavity-dissolve-0.webp', 'WEBP', quality=85)
print(f"Saved cavity-dissolve-0.webp — {sum(len(t) for t in trails)} trail points, {num_particles} particles")
