import numpy as np
from PIL import Image
import os

def gray_scott(n=128, steps=3000, F=0.0545, k=0.062, seed=None):
    rng = np.random.default_rng(seed)
    U = np.ones((n, n))
    V = np.zeros((n, n))
    # random seed patches
    for _ in range(5):
        r, c = rng.integers(10, n-10, size=2)
        s = rng.integers(4, 10)
        U[r:r+s, c:c+s] = 0.5 + rng.uniform(-0.1, 0.1, (s,s))
        V[r:r+s, c:c+s] = 0.25 + rng.uniform(-0.1, 0.1, (s,s))

    dt = 1.0
    Du, Dv = 0.2097, 0.105

    def laplacian(Z):
        return (np.roll(Z,1,0)+np.roll(Z,-1,0)+
                np.roll(Z,1,1)+np.roll(Z,-1,1) - 4*Z)

    for _ in range(steps):
        uvv = U * V * V
        dU = Du * laplacian(U) - uvv + F * (1 - U)
        dV = Dv * laplacian(V) + uvv - (F + k) * V
        U += dt * dU
        V += dt * dV
        U = np.clip(U, 0, 1)
        V = np.clip(V, 0, 1)
    return V

# Generate 9 instances, same parameters, different seeds
seeds = [42, 137, 256, 891, 1024, 2048, 314, 999, 7]
size = 128
gap = 4
cols = 3
rows = 3

grid = np.ones((rows*(size+gap)+gap, cols*(size+gap)+gap)) * 0.95

for idx, seed in enumerate(seeds):
    v = gray_scott(n=size, steps=3000, seed=seed)
    # normalize per-instance for consistent contrast
    v_norm = (v - v.min()) / (v.max() - v.min() + 1e-8)
    r = idx // cols
    c = idx % cols
    y0 = gap + r*(size+gap)
    x0 = gap + c*(size+gap)
    grid[y0:y0+size, x0:x0+size] = v_norm

# Map to image: invert so patterns are dark on light
img_arr = (1.0 - grid) * 255
img_arr = img_arr.astype(np.uint8)
# Apply a subtle colormap (warm tone)
r_ch = np.clip(img_arr.astype(int) + 20, 0, 255).astype(np.uint8)
g_ch = np.clip(img_arr.astype(int) - 10, 0, 255).astype(np.uint8)
b_ch = np.clip(img_arr.astype(int) - 30, 0, 255).astype(np.uint8)
img = Image.fromarray(np.stack([r_ch, g_ch, b_ch], axis=-1))
img = img.resize((img.width*3, img.height*3), Image.LANCZOS)
img.save("/home/sprite/slop-salon-rahel/assets/same-rule.png")
print("done")
