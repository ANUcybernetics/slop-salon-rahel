"""Transition function as crystal lattice rotation.

Two crystal lattices (angular, not radial) from different patches.
Their overlap shows the transition as a spatial rotation of the lattice.
The lattice should look like mineral structure — cleavage planes, not waves.
"""

import numpy as np
from PIL import Image

N = 512
x = np.linspace(-4, 4, N)
y = np.linspace(-4, 4, N)
X, Y = np.meshgrid(x, y)

def crystal_lattice(X, Y, rotation=0, scale=1.0, spacing=0.6):
    """Generate a crystal lattice pattern from three sets of parallel lines
    (6-fold symmetry, like a hexagonal/mineral structure)."""
    # Three families of parallel lines at 60° to each other
    lines = 0
    for angle in [0, np.pi/3, 2*np.pi/3]:
        # Rotate coordinates
        xr = X * np.cos(rotation) - Y * np.sin(rotation)
        yr = X * np.sin(rotation) + Y * np.cos(rotation)
        # Project onto direction perpendicular to line family
        nx = np.cos(angle + np.pi/2)
        ny = np.sin(angle + np.pi/2)
        proj = (xr * nx + yr * ny) * scale / spacing
        lines += np.abs(np.sin(np.pi * proj))
    # Lines appear where all three families intersect strongly
    # Use min projection — bright where lines cross
    result = 1.0 / (1.0 + lines**2)
    return result

# Two patches with different crystal orientations
# Patch U: centered left, orientation 0
# Patch V: centered right, orientation π/6 (30° twist = the transition)
cx_u, cy_u = -1.2, 0.0
cx_v, cy_v = 1.2, 0.0

def bump(r, width=2.0):
    t = np.clip(1.0 - r / width, 0, 1)
    return t**2 * (3 - 2*t)

r_u = np.sqrt((X - cx_u)**2 + Y**2)
r_v = np.sqrt((X - cx_v)**2 + Y**2)
chi_u = bump(r_u, width=2.0)
chi_v = bump(r_v, width=2.0)

# Lattice for each patch
lat_u = crystal_lattice(X, Y, rotation=0, scale=0.8)
lat_v = crystal_lattice(X, Y, rotation=np.pi/6, scale=0.8)

# Fade each lattice with its bump function
# Decay the lattice outward from patch center
decay_u = np.exp(-0.3 * r_u)
decay_v = np.exp(-0.3 * r_v)

field_u = lat_u * chi_u * decay_u
field_v = lat_v * chi_v * decay_v

# Transition angle in the overlap
overlap = chi_u * chi_v
# θ goes from 0 to π/6 across the overlap
theta = np.arctan2(Y, (X - cx_u)) * overlap * 0.8

# Color: amber/charcoal for U, green/charcoal for V
# Mineral palette: dark background, bright lattice lines
def lattice_to_rgb(field, hue_family):
    """Map crystal lattice to mineral color."""
    f = np.clip(field, 0, 1)
    # Bright lines, dark matrix
    if hue_family == 'amber':
        r = 0.05 + 0.75 * f
        g = 0.04 + 0.40 * f
        b = 0.03 + 0.25 * f * (1 - f)
    elif hue_family == 'green':
        r = 0.03 + 0.20 * f * (1 - f)
        g = 0.05 + 0.65 * f
        b = 0.03 + 0.30 * f * (1 - f)
    elif hue_family == 'amethyst':
        r = 0.05 + 0.55 * f * (1 - f)
        g = 0.04 + 0.20 * f * (1 - f)
        b = 0.05 + 0.70 * f
    return np.stack([r, g, b], axis=-1)

# Compose
img = np.zeros((N, N, 3))
img += lattice_to_rgb(field_u, 'amethyst') * chi_u[..., None] * 0.8
img += lattice_to_rgb(field_v, 'green') * chi_v[..., None] * 0.8

# Overlap: show the rotation as a color shift + lattice blend
# Use the theta field to drive color
overlap_field = (field_u + field_v) * overlap
# Rotate the color between amethyst and green based on theta
hue_mix = (theta / (np.pi/6) * 0.5 + 0.5) * overlap

# Amber-green blend for overlap
r_over = 0.03 + 0.6 * overlap_field
g_over = 0.03 + 0.55 * overlap_field * (0.5 + 0.5 * np.sin(theta * 3))
b_over = 0.03 + 0.2 * overlap_field * (1 - 0.5 * np.abs(np.sin(theta * 3)))

img += np.stack([r_over, g_over, b_over], axis=-1) * overlap[..., None] * 1.5

# Darken overall
img = np.clip(img * 0.7, 0, 1)
img = (img * 255).astype(np.uint8)

img_out = Image.fromarray(img, mode='RGB')
img_out.save('assets/transition-glue-lattice.png', 'png')
print(f"Saved transition-glue-lattice.png  {img.shape}")

# v2: simpler, single mineral color, rotation as a bright seam
img2 = np.zeros((N, N, 3))
# Dark background
img2[:] = [8, 6, 5]  # very dark warm gray
# Overlay both lattices
lattice_blend = field_u * 0.6 + field_v * 0.6
img2 = img2 + lattice_to_rgb(lattice_blend, 'amber') * 0.5

# Bright seam at the overlap — the gluing
seam_brightness = overlap * (0.3 + 0.4 * np.abs(np.sin(theta * 4)))
img2 = img2 + np.stack([seam_brightness * 0.8, seam_brightness * 0.6, seam_brightness * 0.4], axis=-1)

img2 = np.clip(img2, 0, 1)
img2 = (img2 * 255).astype(np.uint8)
img2_out = Image.fromarray(img2, mode='RGB')
img2_out.save('assets/transition-glue-lattice-v2.png', 'png')
print(f"Saved transition-glue-lattice-v2.png  {img2.shape}")
