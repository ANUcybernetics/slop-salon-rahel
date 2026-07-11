"""Transition function as mineral grain shear.

A single continuous mineral texture covers the whole plane.
The transition function is a spatially-varying rotation of the gradient field
in the overlap region — like the grain twisting.
The mineral itself is continuous; what changes is the structure (the direction
of the grain/flow), which is what the transition function does.

Think of it as: the rock is the same, but the cleavage planes twist
as you cross from one local chart to another.
"""

import numpy as np
from PIL import Image

N = 512
x = np.linspace(-5, 5, N)
y = np.linspace(-5, 5, N)
X, Y = np.meshgrid(x, y)

# --- Generate a continuous mineral texture ---
def mineral_terrain(X, Y):
    """Multi-frequency mineral noise — layered crystalline structure."""
    # Layer 1: large-scale mineral structure
    r1 = np.sqrt((X + 1.5)**2 + (Y + 0.8)**2)
    t1 = np.exp(-0.15 * r1) * np.sin(2.0 * r1 * np.pi / 3.0)

    # Layer 2: finer crystalline structure
    r2 = np.sqrt((X - 1.5)**2 + (Y - 0.5)**2)
    t2 = np.exp(-0.2 * r2) * np.sin(4.0 * r2 * np.pi / 2.5)

    # Layer 3: background crystalline noise
    theta1 = np.arctan2(Y, X)
    t3 = np.sin(6 * theta1) * np.exp(-0.1 * np.sqrt(X**2 + Y**2)) * 0.3

    # Layer 4: microstructure
    r4 = np.sqrt(X**2 + Y**2)
    t4 = np.sin(12 * r4 + 3 * np.sin(5 * theta1)) * np.exp(-0.3 * r4) * 0.2

    return t1 + t2 + t3 + t4

terrain = mineral_terrain(X, Y)

# --- The transition function: spatial rotation of the gradient ---
# Compute gradient of the terrain
grad_x = np.gradient(terrain, axis=1)
grad_y = np.gradient(terrain, axis=0)

# Transition: a twist field centered between the two patches
# For a circle bundle, g_UV: U∩V → S^1 — a phase function
# Use angular position relative to overlap center
overlap_center_x = 0.0
overlap_center_y = 0.0
r_over = np.sqrt((X - overlap_center_x)**2 + (Y - overlap_center_y)**2)
theta_over = np.arctan2(Y - overlap_center_y, X - overlap_center_x)

# The transition angle: a function supported in the overlap region
# Smooth bump that tapers to zero at the boundary
max_overlap_r = 2.2
bump_r = np.clip(1.0 - r_over / max_overlap_r, 0, 1)
bump_smooth = bump_r**3 * (10 - 15 * bump_r + 6 * bump_r**2)  # smooth symmetric bump

# The actual transition function: phase that winds around the overlap
# For a non-trivial bundle, the transition has non-zero winding
# Try winding number 1: theta_over (winds once around the origin)
n_winding = 1
transition_phase = theta_over * bump_smooth * n_winding

# --- Apply the rotation to the gradient in the overlap ---
c = np.cos(transition_phase)
s = np.sin(transition_phase)

# Rotate the gradient field
grad_x_rot = c * grad_x - s * grad_y
grad_y_rot = s * grad_x + c * grad_y

# Smoothly blend between unrotated and rotated
blend = bump_smooth
grad_x_final = (1 - blend) * grad_x + blend * grad_x_rot
grad_y_final = (1 - blend) * grad_y + blend * grad_y_rot

# --- Render: show the gradient flow as mineral direction ---
# Compute flow-aligned magnitude
mag = np.sqrt(grad_x_final**2 + grad_y_final**2)

# Color by direction + magnitude
direction = np.arctan2(grad_y_final, grad_x_final) / np.pi  # [-1, 1]

# Mineral palette: dark background, flow shows as bright grain
# Brightness from magnitude
brightness = np.log1p(mag) * 0.5
brightness = np.clip(brightness, 0, 1)

# Direction modulates color
hue = (direction + 1) * 0.5  # [0, 1]

# Color mapping: earth tones
r = 0.05 + 0.6 * brightness * (0.7 + 0.3 * np.sin(hue * 2 * np.pi + 0.5))
g = 0.04 + 0.5 * brightness * (0.6 + 0.4 * np.sin(hue * 2 * np.pi - 0.5))
b = 0.06 + 0.55 * brightness * (0.5 + 0.5 * np.sin(hue * 2 * np.pi + 1.5))

img = np.clip(np.stack([r, g, b], axis=-1), 0, 1)
img = (img * 255).astype(np.uint8)

img_out = Image.fromarray(img, mode='RGB')
img_out.save('assets/transition-grain.png', 'png')
print(f"Saved transition-grain.png")

# v2: show the terrain itself, with the twist visible as structural
# The terrain is the "rock", the rotation of the gradient is the twist
# Render terrain brightness + twist phase overlaid
terrain_norm = np.clip(terrain / (np.max(np.abs(terrain)) + 1e-10), -1, 1)
terrain_bright = 0.08 + 0.7 * (terrain_norm * 0.5 + 0.5)

# Dark rock color
img2 = np.zeros((N, N, 3), dtype=float)
img2[:, :, 0] = terrain_bright * 0.5   # slight warm
img2[:, :, 1] = terrain_bright * 0.4
img2[:, :, 2] = terrain_bright * 0.35

# Overlay the twist phase as a subtle color shift in the overlap
# Where the transition is active, the grain direction shifts
twist_brightness = bump_smooth * 0.3
hue_twist = theta_over / (2 * np.pi)
r_twist = twist_brightness * np.maximum(0, np.sin(hue_twist * 2 * np.pi))
g_twist = twist_brightness * np.maximum(0, np.sin((hue_twist - 0.33) * 2 * np.pi))
b_twist = twist_brightness * np.maximum(0, np.sin((hue_twist - 0.66) * 2 * np.pi))
img2 = img2 + np.stack([r_twist, g_twist, b_twist], axis=-1)

img2 = np.clip(img2, 0, 1)
img2 = (img2 * 255).astype(np.uint8)
img2_out = Image.fromarray(img2, mode='RGB')
img2_out.save('assets/transition-grain-v2.png', 'png')
print(f"Saved transition-grain-v2.png")

# v3: focus on the twist angle as the subject
# A field of arrows / flow lines, but rendered as mineral
# Brightness = strength of transition, color = angle of rotation
twist_strength = np.abs(transition_phase)
twist_dir = transition_phase  # signed angle

# Normalize
twist_strength = np.clip(twist_strength / np.max(twist_strength), 0, 1)
twist_dir_norm = (twist_dir / np.pi + 1) * 0.5  # [0, 1]

img3 = np.zeros((N, N, 3), dtype=float)
# Dark background
img3[:, :, 0] = 0.02
img3[:, :, 1] = 0.015
img3[:, :, 2] = 0.025

# Twist as colored mineral
h = twist_dir_norm
r_s = 0.08 + 0.5 * twist_strength * np.maximum(0, np.sin(h * 2 * np.pi))
g_s = 0.06 + 0.45 * twist_strength * np.maximum(0, np.sin((h - 0.33) * 2 * np.pi))
b_s = 0.05 + 0.5 * twist_strength * np.maximum(0, np.sin((h - 0.66) * 2 * np.pi))
img3 = img3 + np.stack([r_s, g_s, b_s], axis=-1)

# Add terrain texture
img3 = img3 + terrain_bright[..., None] * 0.15

img3 = np.clip(img3, 0, 1)
img3 = (img3 * 255).astype(np.uint8)
img3_out = Image.fromarray(img3, mode='RGB')
img3_out.save('assets/transition-grain-v3.png', 'png')
print(f"Saved transition-grain-v3.png")
