"""Transition functions as gluing — two mineral patches, rotation in overlap.

Visual: two mineral textures (each a radial field with decay+ringing),
centered at different points. In their overlap, show the transition
function as a spatial rotation — the glue that identifies the charts.

Not a diagram. Not Newton basins. The rotation is the visual language.
"""

import numpy as np
from PIL import Image

N = 512
x = np.linspace(-4, 4, N)
y = np.linspace(-4, 4, N)
X, Y = np.meshgrid(x, y)

# Two patch centers
cx_u, cy_u = -1.0, 0.0
cx_v, cy_v = 1.0, 0.0

r_u = np.sqrt((X - cx_u)**2 + (Y - cy_u)**2)
r_v = np.sqrt((X - cx_v)**2 + (Y - cy_v)**2)

# Mineral field: exponential decay with sinusoidal ringing
def mineral(r, freq=5.0, decay=0.6):
    return np.exp(-decay * r) * np.sin(freq * r * np.pi)

u_raw = mineral(r_u, freq=5.0, decay=0.6)
v_raw = mineral(r_v, freq=4.5, decay=0.55)

# Smooth partition of unity
def bump(r, center=0, width=1.8):
    t = np.clip(1.0 - (r - center) / width, 0, 1)
    return t**2 * (3 - 2*t)

chi_u = bump(r_u)
chi_v = bump(r_v)

# Transition function: a phase rotation supported in the overlap
# g_UV(x) ∈ SO(2) — an angle field, zero outside overlap
overlap = chi_u * chi_v

# The angle varies with position — use angular offset from midpoint
theta_raw = np.arctan2(Y, X)
# Dampen: zero far from overlap
theta = theta_raw * overlap * 2.5

# Color field: base mineral field, darkened in overlap
# In the overlap, show rotation via color shift (hue)
field = u_raw * chi_u + v_raw * chi_v
hue_field = theta / (2 * np.pi) + 0.5  # normalize to [0,1]

# Two renderings:
# v1: mineral palette with overlap rotation as subtle color shift
# v2: higher contrast — dark background, bright mineral, rotation as hue wheel

# --- v1: mineral palette ---
def field_to_rgb(field, hue=None, sat_mult=1.0, bright=1.0):
    """Map scalar field to deep mineral colors."""
    f = np.clip(field, -1, 1)
    abs_f = np.abs(f)
    # Base: dark mineral
    base = 0.08 + 0.5 * abs_f
    if hue is not None:
        # Modulate with hue
        h = (hue * 6) % 1.0
        # Simple RGB from hue
        r = base * (0.5 + 0.5 * np.sin(h * 2 * np.pi + 0.0))
        g = base * (0.5 + 0.5 * np.sin(h * 2 * np.pi + 2.094))
        b = base * (0.5 + 0.5 * np.sin(h * 2 * np.pi + 4.189))
    else:
        # Amethyst-ish: purple-dominant
        r = base * (0.4 + 0.3 * f)
        g = base * 0.15
        b = base * (0.3 + 0.5 * (1 - abs_f))
    # Desaturate the non-overlap region to keep it mineral-like
    # In overlap, increase saturation via hue
    if hue is not None:
        non_overlap_sat = 1.0 - overlap
        r = r * non_overlap_sat + r * overlap * sat_mult
        g = g * non_overlap_sat + g * overlap * sat_mult + base * overlap * 0.15
        b = b * non_overlap_sat + b * overlap * sat_mult
    return np.clip(np.stack([r, g, b], axis=-1) * bright, 0, 1)

img = field_to_rgb(field, hue=hue_field, sat_mult=2.0, bright=1.5)
img = (img * 255).astype(np.uint8)

img_out = Image.fromarray(img, mode='RGB')
img_out.save('assets/transition-glue.png', 'png')
print(f"Saved transition-glue.png  {img.shape}  overlap stats: min={overlap.min():.3f} max={overlap.max():.3f} mean={overlap.mean():.4f}")

# --- v2: higher contrast with dark background ---
img2 = np.zeros((N, N, 3), dtype=float)
# Dark background
img2 += 0.02
# Add mineral fields
mineral_rgb = field_to_rgb(field, sat_mult=0.5)
img2 += mineral_rgb * 0.4 * (1 - overlap)[..., None]
# In the overlap, add the hue wheel on dark background
h = hue_field
h6 = (h * 6) % 1.0
r_h = 0.3 + 0.7 * np.maximum(0, np.sin(h6 * 2 * np.pi))
g_h = 0.3 + 0.7 * np.maximum(0, np.sin((h6 - 0.33) * 2 * np.pi))
b_h = 0.3 + 0.7 * np.maximum(0, np.sin((h6 - 0.66) * 2 * np.pi))
overlap_rgb = np.stack([r_h, g_h, b_h], axis=-1) * overlap[..., None] * 0.6
img2 += overlap_rgb
img2 = np.clip(img2, 0, 1)
img2 = (img2 * 255).astype(np.uint8)

img2_out = Image.fromarray(img2, mode='RGB')
img2_out.save('assets/transition-glue-v2.png', 'png')
print(f"Saved transition-glue-v2.png  {img2.shape}")
