import numpy as np
import matplotlib.pyplot as plt

def newton_step(z, a):
    """One Newton iteration for z² - a."""
    return 0.5 * (z + a / z)

def velocity_field(a=1.0, N=800, max_iter=64, eps=1e-10):
    """Newton convergence velocity for z² - a."""
    x = np.linspace(-3, 3, N)
    y = np.linspace(-3, 3, N)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    # Run Newton, track convergence
    z = Z.copy()
    steps = np.full_like(X, max_iter, dtype=int)
    converged = np.zeros_like(X, dtype=bool)

    root_plus = np.sqrt(a)
    root_minus = -np.sqrt(a)

    for i in range(1, max_iter + 1):
        z = newton_step(z, a)
        dist_plus = np.abs(z - root_plus)
        dist_minus = np.abs(z - root_minus)
        new_conv = ~converged & (np.minimum(dist_plus, dist_minus) < eps)
        steps[new_conv] = i
        converged |= new_conv

    # Velocity: -log(steps)/log(max_iter) for converged points
    # Higher = faster convergence
    valid = converged & (steps > 0)
    velocity = np.zeros_like(X)
    velocity[valid] = -np.log(steps[valid]) / np.log(max_iter)

    # Label by root
    labels = np.zeros_like(X, dtype=int)
    labels[converged & (dist_plus < dist_minus)] = 1   # +root
    labels[converged & (dist_minus < dist_plus)] = -1  # -root

    return X, Y, velocity, labels, z

def plot_velocity(a=1.0):
    X, Y, V, labels, final = velocity_field(a, N=800, max_iter=64)

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))

    # Velocity as mineral colors — where it rushes = amber, where it hesitates = deep violet
    im = ax.contourf(X, Y, V, levels=32, cmap='magma')

    # Separatrix (y-axis for real a>0) in luminous edge
    ax.axvline(0, color='white', linewidth=0.5, alpha=0.7)

    # Roots as white dots
    root_plus = np.sqrt(a)
    root_minus = -np.sqrt(a)
    ax.plot([root_plus, root_minus], [0, 0], 'wo', markersize=6)

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.set_xlabel('Re(z)')
    ax.set_ylabel('Im(z)')
    ax.set_title('Newton velocity for z²−a\nwhere convergence rushes = solid amber\nwhere it hesitates = deep violet')
    plt.colorbar(im, ax=ax, label='-log(steps)/log(max_iter)')
    plt.tight_layout()
    plt.savefig('assets/velocity-field.png', dpi=150, bbox_inches='tight', facecolor='black')
    plt.close()

    # Postable version: clean, no axes, no colorbar — just the field
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.set_facecolor('#0a0a0f')
    im = ax.contourf(X, Y, V, levels=32, cmap='magma')
    ax.axvline(0, color='white', linewidth=0.8, alpha=0.4)
    ax.plot([root_plus, root_minus], [0, 0], 'wo', markersize=8)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0, hspace=0, wspace=0)
    plt.savefig('assets/velocity-field-post.png', dpi=150, bbox_inches='tight', facecolor='#0a0a0f', pad_inches=0)
    plt.close()

if __name__ == '__main__':
    plot_velocity()
    print("Done. velocity-field.png + velocity-field-dark.png")
