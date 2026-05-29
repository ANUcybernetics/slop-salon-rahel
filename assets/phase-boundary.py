import numpy as np
from PIL import Image

N = 700
X, Y = np.meshgrid(np.linspace(-3, 3, N), np.linspace(-3, 3, N)[::-1])  # Y flipped for image coords

D = X + Y

# Arches region: D > 0 (upper-left in image)
r = np.sqrt(X**2 + Y**2)
arch_v = (np.cos(r * 5) + 1) / 2

# Strata region: D < 0 (lower-right)
strata_v = (np.sin(Y * 10) + 1) / 2

mask_arch = D > 0.08
mask_strata = D < -0.08
mask_bound = ~mask_arch & ~mask_strata

img = np.zeros((N, N, 3), dtype=np.uint8)

# Arches: gold
img[mask_arch, 0] = (80 + 175 * arch_v[mask_arch]).astype(int)
img[mask_arch, 1] = (40 + 110 * arch_v[mask_arch]).astype(int)
img[mask_arch, 2] = (5 + 20 * arch_v[mask_arch]).astype(int)

# Strata: teal
img[mask_strata, 0] = (5 + 15 * strata_v[mask_strata]).astype(int)
img[mask_strata, 1] = (30 + 90 * strata_v[mask_strata]).astype(int)
img[mask_strata, 2] = (60 + 195 * strata_v[mask_strata]).astype(int)

# Boundary: warm glow
t = (1.0 - np.abs(D[mask_bound]) / 0.08).clip(0, 1)
img[mask_bound, 0] = (10 + 245 * t).astype(int)
img[mask_bound, 1] = (10 + 210 * t).astype(int)
img[mask_bound, 2] = (10 + 130 * t).astype(int)

Image.fromarray(img, 'RGB').save('/home/sprite/slop-salon-rahel/assets/phase-boundary.png')
print("Done")
