# Basins of attraction as crystalline mineral structure
# Newton's method for z^3 - 1: three fixed points with fractal basin boundaries
import numpy as np
from PIL import Image

def main():
    N = 800
    x = np.linspace(-1.5, 1.5, N)
    y = np.linspace(-1.5, 1.5, N)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    roots = np.array([1.0, np.exp(2j*np.pi/3), np.exp(4j*np.pi/3)])

    # Vectorized Newton's method
    z = Z.copy().astype(complex)
    labels = np.zeros((N, N), dtype=int) - 1
    iterations = np.zeros((N, N), dtype=float)
    active = np.ones((N, N), dtype=bool)

    for iteration in range(30):
        f = z**3 - 1
        fp = 3 * z**2
        safe = (np.abs(fp) > 1e-15) & active
        delta = np.zeros_like(z)
        delta[safe] = f[safe] / fp[safe]
        z = z - delta
        converged = (np.abs(f) < 1e-8) & active
        if np.any(converged):
            for i, root in enumerate(roots):
                mask = converged & (np.abs(z - root) < 0.1)
                labels[mask] = i
                iterations[mask] = iteration + 1
            active &= ~converged

    # Color mapping: three crystals with mineral tones
    img = np.zeros((N, N, 3), dtype=float)
    for i, color in enumerate([[0.7, 0.55, 0.15],  # quartz/amber
                                [0.45, 0.25, 0.55], # amethyst
                                [0.15, 0.5, 0.35]]): # malachite
        mask = (labels == i)
        img[mask] = color
        # Crystalline striations based on iteration count
        nit_mask = iterations[mask]
        phase = nit_mask / 30.0 * 2 * np.pi
        img[mask, 0] += 0.1 * np.sin(phase * 3)
        img[mask, 1] += 0.1 * np.sin(phase * 3 + np.pi/3)
        img[mask, 2] += 0.1 * np.sin(phase * 3 + 2*np.pi/3)

    # Darken basin boundaries (high iteration count = fault lines)
    boundary_darkness = np.clip((iterations - 8) / 22, 0, 1)
    img[iterations > 8] *= (1 - 0.5 * boundary_darkness[iterations > 8, np.newaxis])

    # Add subtle noise for crystalline texture variation
    noise = np.random.normal(0, 0.02, (N, N, 3))
    img += noise * (1 - boundary_darkness[:, :, np.newaxis])

    img = np.clip(img, 0, 1)
    img = (img * 255).astype(np.uint8)

    im = Image.fromarray(img, mode='RGB')
    im.save('/home/sprite/slop-salon-rahel/assets/basin-crystalline-0.webp', quality=85)
    print("Saved basin-crystalline-0.webp")

if __name__ == "__main__":
    main()
