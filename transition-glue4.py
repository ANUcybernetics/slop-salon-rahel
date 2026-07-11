"""Transition functions as cleavage in mineral.

A single crystalline field, split into two charts by a seam.
In the overlap (the seam region), the crystal orientation shifts —
this is the transition function. The shift is a rotation of the crystal
lattice, rendered as a visible twist in the cleavage planes.

The crystalline structure is the same underlying field;
the transition is what you see where the crystal grain shears.
"""

import numpy as np
from PIL import Image, ImageFilter

N = 512
x = np.linspace(-3, 3, N)
y = np.linspace(-3, 3, N)
X, Y = np.meshgrid(x, y)

# Sharp crystalline structure using intersecting planes
def crystal_planes(X, Y, angle=0, freq=1.0, line_width=0.04):
    """Sharp mineral crystalline planes at a given angle."""
    # Rotate coordinates
    xr = X * np.cos(angle) - Y * np.sin(angle)
    yr = X * np.sin(angle) + Y * np.cos(angle)

    # Three families of planes (6-fold crystalline)
    planes = 0
    for a in [0, np.pi/3, 2*np.pi/3]:
        pa = xr * np.cos(a) + yr * np.sin(a)
        # Use sinc-like function for sharp planes
        phase = np.pi * freq * pa
        plane = np.abs(np.sin(phase))
        # Sharp edges
        plane = np.exp(-plane / line_width)
        planes += plane

    return 1.0 / (1.0 + planes)

# Generate the same underlying crystal in two different orientations
# U: zero rotation
# V: small rotation (the transition/glu)
angle_v = np.pi / 8  # 22.5° twist — the transition function value

crystal_u = crystal_planes(X, Y, angle=0, freq=1.5, line_width=0.03)
crystal_v = crystal_planes(X, Y, angle=angle_v, freq=1.5, line_width=0.03)

# Patch geometry: two overlapping circular regions
cx_u, cy_u = -1.0, 0.0
cx_v, cy_v = 1.0, 0.0

r_u = np.sqrt((X - cx_u)**2 + (Y - cy_u)**2)
r_v = np.sqrt((X - cx_v)**2 + (Y - cy_v)**2)

# Smooth patch boundaries
def patch_bump(r, center, width=2.5):
    t = np.clip(1.0 - (r - center * 0.1) / width, 0, 1)
    return t**2 * (3 - 2*t)

chi_u = patch_bump(r_u, cx_u)
chi_v = patch_bump(r_v, cx_v)

# The transition function: rotation applied in the overlap region
# The overlap is where both chi values are high
overlap = chi_u * chi_v

# Smooth step for transition region
t_step = np.clip(1.0 - np.abs(chi_u - chi_v) / 0.5, 0, 1)
t_step = t_step ** 2

# The transition angle varies spatially: 0 → angle_v across the overlap
# This is the visual representation of g_UV(x): SO(2) at each point
# Map from left chart to right chart
local_angle = np.arctan2(Y, X)
transition_angle = local_angle * t_step * np.sin(angle_v) * 0.3

# Render: dark background, sharp crystal planes
# Crystal color: quartz/mineral (warm, slightly translucent)
def crystal_to_rgb(crystal, brightness=1.0):
    # Mineral color: warm white-gray with slight amber tint
    q = np.clip(crystal, 0, 1)
    r = (0.04 + 0.55 * q) * brightness
    g = (0.035 + 0.45 * q) * brightness
    b = (0.03 + 0.40 * q) * brightness
    return np.stack([r, g, b], axis=-1)

img = np.zeros((N, N, 3))

# Background (dark stone)
img[:] = [0.02, 0.018, 0.015]

# Crystal U (left side)
img += crystal_to_rgb(crystal_u * chi_u) * 0.8

# Crystal V (right side)
img += crystal_to_rgb(crystal_v * chi_v) * 0.8

# Transition region: twist in the crystal planes
# The twist creates an interference pattern — different orientation
# means the planes don't align perfectly
twist_crystal = crystal_planes(X, Y, angle=transition_angle, freq=1.5, line_width=0.03)
twist_brightness = twist_crystal * overlap * 1.5

img += crystal_to_rgb(twist_brightness) * 0.7

# Add a bright seam line through the overlap center
seam = np.exp(-((Y - cy_u) / 0.3)**2) * overlap
img[:, :, 0] += seam * 0.15
img[:, :, 1] += seam * 0.08

# Post-process: slight contrast boost
img = np.clip(img, 0, 1)
img = (img * 255).astype(np.uint8)

# Slight blur then sharpen (unsharp mask)
pil = Image.fromarray(img, mode='RGB')
blur = pil.filter(ImageFilter.GaussianBlur(radius=1))
img_blur = np.array(blur).astype(float)
img_sharp = 2 * img.astype(float) - img_blur
img_sharp = np.clip(img_sharp, 0, 255).astype(np.uint8)

pil_sharp = Image.fromarray(img_sharp, mode='RGB')
pil_sharp.save('assets/transition-cleavage.png', 'png')
print(f"Saved transition-cleavage.png")

# v2: more dramatic — show the transition as a visible phase boundary
# Think of it as a fault line in rock where the grain has shifted
img2 = np.zeros((N, N, 3))
img2[:] = [0.015, 0.012, 0.01]

# Crystal with higher contrast
crystal_u_high = np.clip((crystal_u * chi_u - 0.1) * 2, 0, 1)
crystal_v_high = np.clip((crystal_v * chi_v - 0.1) * 2, 0, 1)

img2[:, :, 0] = 0.03 + 0.6 * (crystal_u_high * 0.5 + crystal_v_high * 0.5)
img2[:, :, 1] = 0.02 + 0.5 * (crystal_u_high * 0.45 + crystal_v_high * 0.45)
img2[:, :, 2] = 0.02 + 0.4 * (crystal_u_high * 0.4 + crystal_v_high * 0.4)

# Transition: visible as a bright, complex interference zone
# Use the difference between the two crystal orientations
diff = np.abs(crystal_u - crystal_v) * overlap
# Interference fringes — periodic modulation
fringes = np.sin(np.arctan2(Y, X) * 8) * diff * 2
fringes = np.clip(fringes, 0, 1)

img2[:, :, 0] += fringes * 0.2
img2[:, :, 1] += fringes * 0.12
img2[:, :, 2] += fringes * 0.15

img2 = np.clip(img2, 0, 1)
img2 = (img2 * 255).astype(np.uint8)
pil2 = Image.fromarray(img2, mode='RGB')
pil2.save('assets/transition-cleavage-v2.png', 'png')
print(f"Saved transition-cleavage-v2.png")

# v3: simpler — just show the crystal twist as a continuous deformation
# The crystal rotates smoothly from left to right
# Rotation angle: linear ramp in X, modulated by radial envelope
angle_field = np.linspace(-angle_v/2, angle_v/2, N)
angle_grid = np.broadcast_to(angle_field[None, :], (N, N)).copy()

# Radial envelope (fade at edges)
r_center = np.sqrt(X**2 + Y**2)
envelope = np.exp(-r_center / 3)

# Apply spatially-varying rotation
crystal_twist = crystal_planes(X, Y, angle=angle_grid * envelope, freq=1.5, line_width=0.03)

img3 = np.zeros((N, N, 3))
img3[:] = [0.015, 0.012, 0.01]
c_twist = np.clip((crystal_twist - 0.05) * 2, 0, 1)

# Mineral color: warm stone
img3[:, :, 0] = 0.04 + 0.5 * c_twist
img3[:, :, 1] = 0.03 + 0.4 * c_twist
img3[:, :, 2] = 0.025 + 0.35 * c_twist

img3 = np.clip(img3, 0, 1)
img3 = (img3 * 255).astype(np.uint8)
pil3 = Image.fromarray(img3, mode='RGB')
pil3.save('assets/transition-twist-field.png', 'png')
print(f"Saved transition-twist-field.png")
