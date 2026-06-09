"""
The iteration is the shape of non-recognition.

Visualize the cobweb of f(x) = rx(1-x) but focus on what the diagonal DOESN'T intersect.
The fixed points are where the trajectory recognizes itself. The rest is non-recognition.
Plot the cobweb trajectory and color by distance from the diagonal.
Then: the density of where the trajectory spends its time (the invariant measure) IS the mineral.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def cobweb_path(xs):
    """Convert trajectory array to cobweb path segments."""
    path = []
    n = len(xs) - 1
    for i in range(n):
        path.append((xs[i], xs[i]))        # start at x_i on x-axis
        path.append((xs[i], xs[i+1]))       # vertical to f(x_i)
        path.append((xs[i+1], xs[i+1]))     # horizontal to diagonal
    return np.array(path)

def density_of(xs, bins=200):
    """Histogram of trajectory — the invariant measure approximation."""
    xs = np.array(xs[500:])  # discard transient
    counts, edges = np.histogram(xs, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    return centers, counts

fig, axes = plt.subplots(2, 2, figsize=(12, 12))

# --- Top-left: cobweb of chaotic orbit (r=4), first 150 segments ---
ax = axes[0, 0]
r = 4.0
f = lambda x: r * x * (1 - x)
xs = [0.3]
for i in range(2000):
    xs.append(f(xs[-1]))
xs = np.array(xs)

path = cobweb_path(xs)
segments = []
for i in range(len(path) // 2):
    start = path[2*i]
    end = path[2*i + 1] if 2*i + 1 < len(path) else path[2*i]
    segments.append(np.array([start, end]))

for i, seg in enumerate(segments):
    if i >= 150:
        break
    dist = abs(seg[1][1] - seg[1][0])
    from matplotlib.colors import LightSource
    lum = min(dist / 0.5, 0.49)
    color = matplotlib.colormaps['OrRd'](lum * 2)
    ax.plot(seg[:, 0], seg[:, 1], color=color,
            linewidth=0.8, alpha=0.8)

x = np.linspace(0, 1, 500)
ax.plot(x, f(x), 'k-', linewidth=2, alpha=0.6)
ax.plot(x, x, 'gray', linewidth=1, alpha=0.4, linestyle='--')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.set_title('chaotic orbit: first 150 cobweb segments', fontsize=11)
ax.set_xticks([])
ax.set_yticks([])

# --- Top-right: |f(x) - x| for several r values ---
ax = axes[0, 1]
for r_val in [3.2, 3.5, 3.9, 4.0]:
    f_val = r_val * x * (1 - x)
    dist = np.abs(f_val - x)
    unrecognized = dist > 0.01
    ax.plot(x[unrecognized], f_val[unrecognized], linewidth=2, alpha=0.7,
            label=f'r={r_val}')

ax.plot(x, x, 'k--', alpha=0.3, linewidth=1)
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.set_title('where the map does NOT recognize itself\n(|f(x) − x| > 0.01)', fontsize=11)
ax.legend(fontsize=9)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# --- Bottom-left: the mineral — invariant measure for r=4 ---
ax = axes[1, 0]
r_val = 4.0
f_full = lambda x: r_val * x * (1 - x)
xs_mineral = [0.3]
for i in range(50000):
    xs_mineral.append(f_full(xs_mineral[-1]))
center, density = density_of(xs_mineral)

ax.fill_between(center, 0, density, color='steelblue', alpha=0.6)
ax.plot(center, density, 'steelblue', linewidth=2)

# Analytic invariant: ρ(x) = 1/(π√(x(1-x)))
x_known = np.linspace(0.01, 0.99, 300)
invariant = 1.0 / (np.pi * np.sqrt(x_known * (1 - x_known)))
scale = np.trapezoid(density, center) / np.trapezoid(invariant, x_known)
ax.plot(x_known, invariant * scale, 'r--', linewidth=2, alpha=0.7, label='analytic: 1/(π√(x(1−x)))')
ax.legend(fontsize=9)
ax.set_xlabel('x')
ax.set_ylabel('density')
ax.set_title('the mineral: invariant measure\n(iteration as visible structure)', fontsize=11)
ax.set_xlim(0, 1)

# --- Bottom-right: |f(x) - x| as non-recognition function (r=3.2) ---
ax = axes[1, 1]
r_conv = 3.2
f_conv = lambda x: r_conv * x * (1 - x)
nonrec = np.abs(f_conv(x_conv := x) - x)
ax.plot(x, nonrec, 'crimson', linewidth=2.5)

fps = [0, (r_conv - 1) / r_conv]
for fp in fps:
    ax.axvline(fp, color='black', linestyle='--', alpha=0.4)
    ax.plot(fp, 0, 'ko', markersize=8)

ax.fill_between(x, 0, nonrec, alpha=0.3, color='crimson')
ax.set_xlabel('x')
ax.set_ylabel('|f(x) − x|')
ax.set_title(f'r={r_conv} (period-2)\nthe shape of non-recognition as a function', fontsize=11)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-rahel/assets/shape-of-non-recognition.png',
            dpi=150, bbox_inches='tight')
plt.close()
print("Saved shape-of-non-recognition.png")
