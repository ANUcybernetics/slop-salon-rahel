"""
Bundle theory opening sketch: transition function as visual distortion.
Two overlapping coordinate patches U_0, U_1 on S^1.
Transition function g_01: U_0 ∩ U_1 → O(1) = {+1, -1} for the Möbius strip.
The overlap region shows the coordinate "friction" — the same point viewed
from two different charts, with the twist visible as discontinuity.
"""
import numpy as np
import matplotlib.pyplot as plt

def make_transition_patch(ax, center_x, center_y, radius,
                          grid_n=20, color='C0', alpha=0.7,
                          distort_func=None, label="U_0"):
    """Draw a coordinate patch with grid lines, optionally distorted."""
    # Draw coordinate grid in the patch's own coordinates
    x = np.linspace(-radius, radius, grid_n)
    y = np.linspace(-radius, radius, grid_n)

    for v in x:
        if distort_func:
            pts = np.array([(u, v) for u in x])
            distorted = distort_func(pts)
            ax.plot(distorted[:, 0] + center_x, distorted[:, 1] + center_y,
                    color=color, alpha=alpha*0.4, lw=0.8)
        else:
            ax.axvline(v + center_x, ymin=0.2, ymax=0.8,
                       color=color, alpha=alpha*0.4, lw=0.8)

    for v in y:
        if distort_func:
            pts = np.array([(v, u) for u in y])
            distorted = distort_func(pts)
            ax.plot(distorted[:, 0] + center_x, distorted[:, 1] + center_y,
                    color=color, alpha=alpha*0.4, lw=0.8)
        else:
            ax.axhline(v + center_y, xmin=0.2, xmax=0.8,
                       color=color, alpha=alpha*0.4, lw=0.8)

    # Patch boundary circle
    circle = plt.Circle((center_x, center_y), radius, fill=False,
                        color=color, lw=2, alpha=0.9)
    ax.add_patch(circle)

    # Label
    ax.text(center_x, center_y + radius + 0.15, label,
            ha='center', va='bottom', fontsize=14, fontweight='bold',
            family='monospace')

def make_overlap_visualization():
    """Show transition function g_ij as distortion field on overlap."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # ---- Panel 1: Two undistorted patches (trivial bundle) ----
    ax = axes[0]
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.axis('off')

    # Two overlapping patches, identity transition
    make_transition_patch(ax, -0.6, 0, 1.2, color='C0', label="U_0")
    make_transition_patch(ax, 0.6, 0, 1.2, color='C2', label="U_1")

    # Draw identity map lines in the overlap
    for y_val in np.linspace(-0.6, 0.6, 5):
        ax.plot([-0.6, 0.6], [y_val, y_val], 'k--', lw=0.5, alpha=0.3)

    ax.text(0, -1.7, "Trivial: g_01 = id", ha='center',
            fontsize=12, family='monospace', color='C0')

    # ---- Panel 2: Möbius twist (anti-identity in overlap) ----
    ax = axes[1]
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.axis('off')

    make_transition_patch(ax, -0.6, 0, 1.2, color='C0', label="U_0")
    make_transition_patch(ax, 0.6, 0, 1.2, color='C2', label="U_1")

    # Draw twist map: (x, y) -> (x, -y) in the overlap
    for y_val in np.linspace(-0.6, 0.6, 5):
        # From U_0 perspective: straight line
        # From U_1 perspective: flipped
        ax.plot([-0.6, -0.2], [y_val, y_val], 'C0--', lw=0.5, alpha=0.5)
        ax.plot([0.2, 0.6], [y_val, -y_val], 'C2--', lw=0.5, alpha=0.5)
        # Connection showing the flip
        ax.annotate('', xy=(0.15, -y_val), xytext=(-0.15, y_val),
                    arrowprops=dict(arrowstyle='<->', color='C4',
                                    lw=1.5, alpha=0.8))

    ax.text(0, -1.7, "Möbius: g_01 = -id on overlap", ha='center',
            fontsize=12, family='monospace', color='C0')

    # ---- Panel 3: Smooth distortion field (non-abelian flavor) ----
    ax = axes[2]
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.axis('off')

    # Patch U_0 with shear distortion
    def shear_left(pts):
        """Shear: x' = x + 0.3*y, y' = y"""
        xs, ys = pts[:, 0], pts[:, 1]
        return np.column_stack([xs + 0.3 * ys, ys])

    def shear_right(pts):
        """Inverse shear for the other patch"""
        xs, ys = pts[:, 0], pts[:, 1]
        return np.column_stack([xs - 0.3 * ys, ys])

    make_transition_patch(ax, -0.6, 0, 1.2, color='C0',
                          distort_func=shear_left, label="U_0")
    make_transition_patch(ax, 0.6, 0, 1.2, color='C2',
                          distort_func=shear_right, label="U_1")

    ax.text(0, -1.7, "Shear: g_01 ∈ SL(2,R)", ha='center',
            fontsize=12, family='monospace', color='C0')

    plt.tight_layout()
    plt.savefig('bundle-transition-0.png', dpi=150, bbox_inches='tight')
    plt.close()

def make_distortion_field():
    """Continuous visualization: the transition function as a gradient of distortion."""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Create a grid
    x = np.linspace(-3, 3, 30)
    y = np.linspace(-3, 3, 30)

    # Two overlapping patches
    patch1_center = np.array([-0.8, 0])
    patch2_center = np.array([0.8, 0])
    patch_radius = 1.5

    # Draw patch boundaries
    circle1 = plt.Circle(patch1_center, patch_radius, fill=False,
                         color='C0', lw=2.5, alpha=0.9)
    circle2 = plt.Circle(patch2_center, patch_radius, fill=False,
                         color='C2', lw=2.5, alpha=0.9)
    ax.add_patch(circle1)
    ax.add_patch(circle2)

    # Show how a single vector field looks in each patch's coordinates
    # in the overlap region
    X, Y = np.meshgrid(x, y)

    # Vector field: simple rotation (like holonomy)
    U = -Y
    V = X

    # Mask to show only overlap region clearly
    d1 = np.sqrt((X - patch1_center[0])**2 + (Y - patch1_center[1])**2)
    d2 = np.sqrt((X - patch2_center[0])**2 + (Y - patch2_center[1])**2)

    # In the overlap, show the transition "tension"
    # From patch 1 perspective (color by patch 1 norm)
    # From patch 2 perspective (color by patch 2 norm)

    # Quiver in patch 1 region
    mask1 = d1 < patch_radius
    ax.quiver(X[mask1], Y[mask1], U[mask1], V[mask1],
              alpha=0.3, color='C0', width=0.003)

    # Quiver in patch 2 region
    mask2 = d2 < patch_radius
    ax.quiver(X[mask2], Y[mask2], U[mask2], V[mask2],
              alpha=0.3, color='C2', width=0.003)

    # In the overlap, show the "flip" as a color gradient
    overlap_mask = (d1 < patch_radius) & (d2 < patch_radius)
    if np.any(overlap_mask):
        # Distance from each center normalized
        t = (d1 - d2) / (d1 + d2 + 1e-10)
        ax.scatter(X[overlap_mask], Y[overlap_mask],
                   c=t[overlap_mask], cmap='RdBu_r', s=20, alpha=0.6,
                   edgecolors='none')

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.set_xlabel('local chart coordinates', fontsize=12)

    # Labels
    ax.text(patch1_center[0], patch1_center[1] - patch_radius - 0.3,
            'U_0', ha='center', fontsize=16, fontweight='bold',
            family='monospace', color='C0')
    ax.text(patch2_center[0], patch2_center[1] - patch_radius - 0.3,
            'U_1', ha='center', fontsize=16, fontweight='bold',
            family='monospace', color='C2')

    ax.set_title('Transition function g₀₁ as coordinate tension',
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('bundle-transition-1.png', dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    make_overlap_visualization()
    make_distortion_field()
    print("Done: bundle-transition-0.png, bundle-transition-1.png")
