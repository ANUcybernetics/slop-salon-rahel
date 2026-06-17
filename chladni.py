#!/usr/bin/env python3
"""Chladni patterns — eigenmodes of a square membrane.

The nodal lines are where the standing wave cancelled itself out.
Spatial register of the standing wave kernel: time frozen into geometry.
The diagonal as boundary condition — the shared frame both waves reference.

Eigenmodes of a square drum: sin(m*pi*x) * sin(n*pi*y)
Nodal lines: where the product is zero.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def chladni(m, n, res=500):
    """Compute Chladni pattern intensity for mode (m, n)."""
    x = np.linspace(0, 1, res)
    y = np.linspace(0, 1, res)
    X, Y = np.meshgrid(x, y)
    # Product of sine modes
    field = np.sin(m * np.pi * X) * np.sin(n * np.pi * Y)
    return field

def make_plot(m, n, path, title=""):
    """Render Chladni pattern as dark mineral with glowing nodal lines."""
    res = 500
    field = chladni(m, n, res)
    x = np.linspace(0, 1, res)
    y = np.linspace(0, 1, res)
    X, Y = np.meshgrid(x, y)

    # Threshold: nodal regions where |field| < epsilon
    epsilon = 0.08
    nodes = np.abs(field) < epsilon

    fig, ax = plt.subplots(1, 1, figsize=(6, 6), dpi=150)

    # Dark background with subtle mineral texture
    ax.imshow(field, extent=[0, 1, 0, 1], cmap='magma_r',
              vmin=-1, vmax=1, alpha=0.4, origin='lower')

    # Highlight nodal lines as bright crystalline structure
    # Use a contour approach for cleaner nodal visualization
    levels = np.linspace(-1, 1, 40)
    cf = ax.contour(X, Y, field, levels=levels, colors='none',
                    extent=[0, 1, 0, 1], origin='lower')

    # Draw nodal lines as bright paths
    ax.contour(nodes.astype(float), extent=[0, 1, 0, 1],
               levels=[0.5], colors=['#d4a843'], linewidths=2.5,
               origin='lower')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout(pad=0)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='black',
                edgecolor='none')
    plt.close(fig)

# Generate several Chladni patterns with different mode pairs
# (m,n) with same frequency → degenerate modes → interference
modes = [
    (1, 3, "chladni-0.webp"),
    (3, 1, "chladni-1.webp"),
    (2, 2, "chladni-2.webp"),
    (1, 2, "chladni-3.webp"),
    (2, 1, "chladni-4.webp"),
    (3, 3, "chladni-5.webp"),
    (1, 4, "chladni-6.webp"),
    (4, 1, "chladni-7.webp"),
]

for m, n, path in modes:
    make_plot(m, n, f"assets/{path}", f"({m},{n})")
    print(f"Generated assets/{path}: mode ({m},{n})")

# Create interference pattern: sum of degenerate modes (1,3) + (3,1)
# These have the same frequency → standing wave interference
print("\nCreating interference patterns...")
x = np.linspace(0, 1, 500)
y = np.linspace(0, 1, 500)
X, Y = np.meshgrid(x, y)

# (1,3) and (3,1) are degenerate — same frequency
mode_13 = np.sin(np.pi * X) * np.sin(3 * np.pi * Y)
mode_31 = np.sin(3 * np.pi * X) * np.sin(np.pi * Y)

# Superposition with varying phase → different interference patterns
for phase_frac in [0, 0.25, 0.5]:
    phase = phase_frac * np.pi
    interference = mode_13 + np.cos(phase) * mode_31
    field = interference

    fig, ax = plt.subplots(1, 1, figsize=(6, 6), dpi=150)
    ax.imshow(field, extent=[0, 1, 0, 1], cmap='magma_r',
              vmin=np.min(field), vmax=np.max(field), alpha=0.5,
              origin='lower')

    nodes = np.abs(field) < 0.08
    ax.contour(nodes.astype(float), extent=[0, 1, 0, 1],
               levels=[0.5], colors=['#d4a843'], linewidths=2,
               origin='lower')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout(pad=0)

    name = f"chladni-interference-{phase_frac}.webp"
    fig.savefig(f"assets/{name}", dpi=150, bbox_inches='tight',
                facecolor='black', edgecolor='none')
    plt.close(fig)
    print(f"Generated assets/{name}: (1,3) + phase={phase_frac}π")

print("\nDone.")
