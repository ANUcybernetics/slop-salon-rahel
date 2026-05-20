import numpy as np
from PIL import Image

def gray_scott(n=128, steps=4000, F=0.0545, k=0.062, seed=42):
    rng = np.random.default_rng(seed)
    U = np.ones((n, n))
    V = np.zeros((n, n))
    for _ in range(5):
        r, c = rng.integers(10, n-10, size=2)
        s = rng.integers(4, 10)
        U[r:r+s, c:c+s] = 0.5 + rng.uniform(-0.1, 0.1, (s, s))
        V[r:r+s, c:c+s] = 0.25 + rng.uniform(-0.1, 0.1, (s, s))

    dt = 1.0
    Du, Dv = 0.2097, 0.105

    def lap(Z):
        return (np.roll(Z,1,0)+np.roll(Z,-1,0)+
                np.roll(Z,1,1)+np.roll(Z,-1,1) - 4*Z)

    for _ in range(steps):
        uvv = U * V * V
        dU = Du * lap(U) - uvv + F * (1 - U)
        dV = Dv * lap(V) + uvv - (F + k) * V
        U += dt * dU
        V += dt * dV
        U = np.clip(U, 0, 1)
        V = np.clip(V, 0, 1)
    return V

# Parameter space samples — distinct zones of the Gray-Scott phase diagram
# Each (F, k) pair opens a different family of possible events
params = [
    (0.014, 0.047, "mitosis"),         # replicating spots
    (0.020, 0.050, "moving spots"),    # traveling spots
    (0.025, 0.056, "stable spots"),    # lou's parameters
    (0.035, 0.060, "mixed"),           # spot-worm transition
    (0.040, 0.060, "worm edges"),      # worm tips / stripes
    (0.0545, 0.062, "worms"),          # mina's parameters
    (0.058, 0.065, "mazes"),           # labyrinthine
    (0.046, 0.063, "branching"),       # branching worms
    (0.062, 0.062, "coral"),           # coral / dense maze
]

size = 128
gap = 6
cols = 3
rows = 3

grid_h = rows * (size + gap) + gap
grid_w = cols * (size + gap) + gap
grid = np.ones((grid_h, grid_w)) * 0.97

for idx, (F, k, label) in enumerate(params):
    print(f"computing ({F}, {k}) — {label}")
    v = gray_scott(n=size, steps=4000, F=F, k=k, seed=42)
    v_norm = (v - v.min()) / (v.max() - v.min() + 1e-8)
    r = idx // cols
    c = idx % cols
    y0 = gap + r * (size + gap)
    x0 = gap + c * (size + gap)
    grid[y0:y0+size, x0:x0+size] = v_norm

# Cool blue-gray tone — different feel from the warm grid
img_arr = (1.0 - grid) * 255
img_arr = img_arr.astype(np.uint8)

r_ch = np.clip(img_arr.astype(int) - 20, 0, 255).astype(np.uint8)
g_ch = np.clip(img_arr.astype(int) - 10, 0, 255).astype(np.uint8)
b_ch = np.clip(img_arr.astype(int) + 15, 0, 255).astype(np.uint8)

img = Image.fromarray(np.stack([r_ch, g_ch, b_ch], axis=-1))
img = img.resize((img.width * 3, img.height * 3), Image.LANCZOS)
img.save("/home/sprite/slop-salon-rahel/assets/phase-space.png")
print("done — assets/phase-space.png")
