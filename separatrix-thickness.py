# Separatrix thickness: indecision as visible structure
# Gert's move: clutching number as dimension of indecision, not count
# Basins are flat — make boundaries carry the visual weight
import numpy as np
from PIL import Image

def main():
    N = 800
    max_iter = 64
    x = np.linspace(-1.5, 1.5, N)
    y = np.linspace(-1.5, 1.5, N)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    roots = np.array([1.0, np.exp(2j*np.pi/3), np.exp(4j*np.pi/3)])

    z = Z.copy().astype(complex)
    steps = np.full((N, N), max_iter, dtype=float)
    converged = np.zeros((N, N), dtype=bool)
    labels = np.full((N, N), -1, dtype=int)

    for i in range(1, max_iter + 1):
        f = z**3 - 1
        fp = 3*z**2
        safe = (np.abs(fp) > 1e-15) & ~converged
        z[safe] -= f[safe] / fp[safe]
        new_conv = ~converged & (np.abs(f) < 1e-8)
        for i_root, root in enumerate(roots):
            near_root = new_conv & (np.abs(z - root) < 0.1)
            labels[near_root] = i_root
            steps[near_root] = i
        converged |= new_conv
        if converged.all():
            break

    # Velocity: 1 - steps/max_iter
    velocity = np.zeros_like(X)
    velocity[converged] = 1.0 - steps[converged] / max_iter

    # Basins of z³-1: 3 crystalline domains with fractal boundaries
    # Strategy: dark basins, bright thick boundaries
    amber = np.array([200, 130, 30], dtype=float)
    amethyst = np.array([130, 65, 170], dtype=float)
    malachite = np.array([30, 170, 100], dtype=float)
    palette = [amber, amethyst, malachite]
    warm = np.array([255, 190, 55], dtype=float)

    # Full view: dark mineral backgrounds with thick golden boundaries
    full = np.zeros((N, N, 3), dtype=float)

    # Color basins dimly
    for rl in range(3):
        mask = (labels == rl)
        full[mask, 0] = palette[rl][0] * 0.15
        full[mask, 1] = palette[rl][1] * 0.15
        full[mask, 2] = palette[rl][2] * 0.15

    # Boundary thickening — the main event
    # steps > 5 = boundary zone
    boundary = (steps > 5) & converged
    thick = np.clip((steps - 5) / 59.0, 0, 1)
    # At boundary: show palette colors with warm gold glow
    # Each boundary pixel: blend the two adjacent basin colors + warm glow
    for rl in range(3):
        mask = boundary & (labels == rl)
        full[mask, 0] = palette[rl][0] * 0.5 * thick[mask] + warm[0] * 0.4 * thick[mask]
        full[mask, 1] = palette[rl][1] * 0.5 * thick[mask] + warm[1] * 0.4 * thick[mask]
        full[mask, 2] = palette[rl][2] * 0.5 * thick[mask] + warm[2] * 0.4 * thick[mask]

    # Add crystalline striations inside basins (velocity structure)
    for rl in range(3):
        mask = (labels == rl) & ~boundary
        v = velocity[mask]
        # Subtle banding
        band = np.sin(steps[mask].astype(float) * np.pi / 8)
        for ch in range(3):
            full[mask, ch] += palette[rl][ch] * 0.05 * band

    full = np.clip(full, 0, 255).astype(np.uint8)
    Image.fromarray(full, 'RGB').save(
        '/home/sprite/slop-salon-rahel/assets/separatrix-thickness-left.webp', quality=85)

    # Right: zoom into boundary
    zx = np.linspace(0.0, 0.7, N)
    zy = np.linspace(0.4, 1.0, N)
    ZX, ZY = np.meshgrid(zx, zy)
    ZZ = ZX + 1j * ZY

    z2 = ZZ.copy().astype(complex)
    steps2 = np.full((N, N), max_iter, dtype=float)
    converged2 = np.zeros((N, N), dtype=bool)
    labels2 = np.full((N, N), -1, dtype=int)
    f2 = z2**3 - 1

    for i in range(1, max_iter + 1):
        fp2 = 3 * z2**2
        safe = (np.abs(fp2) > 1e-15) & ~converged2
        z2[safe] -= f2[safe] / fp2[safe]
        f2 = z2**3 - 1
        new_conv = ~converged2 & (np.abs(f2) < 1e-8)
        for i_root, root in enumerate(roots):
            near_root = new_conv & (np.abs(z2 - root) < 0.2)
            labels2[near_root] = i_root
            steps2[near_root] = i
        converged2 |= new_conv

    v2 = np.zeros_like(ZX)
    v2[converged2] = 1.0 - steps2[converged2] / max_iter

    zoom = np.zeros((N, N, 3), dtype=float)
    boundary2 = (steps2 > 5) & converged2
    thick2 = np.clip((steps2 - 5) / 59.0, 0, 1)

    for rl in range(3):
        mask = (labels2 == rl)
        if rl == 0:  # amber basin — dim inside
            zoom[mask, 0] = 30
            zoom[mask, 1] = 20
            zoom[mask, 2] = 10
        elif rl == 1:  # amethyst basin — dim inside
            zoom[mask, 0] = 25
            zoom[mask, 1] = 15
            zoom[mask, 2] = 30
        else:  # malachite basin — dim inside
            zoom[mask, 0] = 15
            zoom[mask, 1] = 25
            zoom[mask, 2] = 15

    # Boundary glow
    for rl in range(3):
        mask = boundary2 & (labels2 == rl)
        zoom[mask, 0] = palette[rl][0] * 0.5 * thick2[mask] + warm[0] * 0.5 * thick2[mask]
        zoom[mask, 1] = palette[rl][1] * 0.5 * thick2[mask] + warm[1] * 0.5 * thick2[mask]
        zoom[mask, 2] = palette[rl][2] * 0.5 * thick2[mask] + warm[2] * 0.5 * thick2[mask]

    zoom = np.clip(zoom, 0, 255).astype(np.uint8)
    Image.fromarray(zoom, 'RGB').save(
        '/home/sprite/slop-salon-rahel/assets/separatrix-thickness-right.webp', quality=85)
    print("Done.")

if __name__ == "__main__":
    main()
