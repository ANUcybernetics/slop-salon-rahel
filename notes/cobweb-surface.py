#!/usr/bin/env python3
"""
Cobweb surface: f(x) - x as a 3D surface over (x, r).
The diagonal y=x is the floor. f(x) is the ceiling.
Their intersection (height=0) traces the fixed point curves.
The slope condition |f'(x)|=1 marks stability boundaries.
"""

import numpy as np
import matplotlib.pyplot as plt

r_vals = np.linspace(1, 4, 400)
x_vals = np.linspace(0, 1, 400)
R, X = np.meshgrid(r_vals, x_vals)

# Cobweb surface: height of f(x) above the diagonal
Z = R * X * (1 - X) - X

# Fixed points
x_fp0 = np.zeros_like(r_vals)
x_fp1 = (r_vals - 1) / r_vals

# Stability boundary: |f'(x)| = |r(1-2x)| = 1
x_stab_pos = (R - 1) / (2 * R)

# --- Figure 1: 3D cobweb surface ---
fig = plt.figure(figsize=(14, 6))

ax = fig.add_subplot(1, 2, 1, projection='3d')
slice_r = r_vals <= 3.2
ax.plot_surface(R[:, slice_r], X[:, slice_r], Z[:, slice_r], cmap='viridis',
                alpha=0.8, edgecolor='none')
# Diagonal floor
ax.plot(r_vals[slice_r], np.zeros_like(r_vals[slice_r]),
        np.zeros_like(r_vals[slice_r]), color='gold', linewidth=2.5)
# Fixed point intersection
fp1_vals = (r_vals[slice_r] - 1) / r_vals[slice_r]
ax.plot(r_vals[slice_r], fp1_vals, np.zeros_like(fp1_vals),
        color='red', linewidth=3)
ax.set_xlabel('r (parameter)')
ax.set_ylabel('x (state)')
ax.set_zlabel('f(x) - x (cobweb height)')
ax.set_title('Cobweb surface: f(x) - x over (x, r)\n'
             'red curve: where cobweb meets diagonal (fixed points)', fontsize=11)
ax.view_init(elev=25, azim=45)

# --- Figure 2: 3D cobweb surface, full parameter range ---
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.plot_surface(R, X, Z, cmap='plasma', alpha=0.8, edgecolor='none')
# Diagonal
ax2.plot(r_vals, np.zeros_like(r_vals), np.zeros_like(r_vals),
        color='gold', linewidth=2)
# Fixed points
ax2.plot(r_vals, x_fp0, np.zeros_like(r_vals), color='red', linewidth=2, label='x=0')
ax2.plot(r_vals, x_fp1, np.zeros_like(r_vals), color='red', linewidth=2, label='x=(r-1)/r')
ax2.set_xlabel('r (parameter)')
ax2.set_ylabel('x (state)')
ax2.set_zlabel('f(x) - x')
ax2.set_title('Full parameter range: bifurcation as surface fold\n'
              'red lines: fixed points; surface meets diagonal', fontsize=11)
ax2.view_init(elev=30, azim=50)
ax2.legend(fontsize=8)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-rahel/assets/cobweb-surface.png', dpi=150, bbox_inches='tight')
print("Saved cobweb-surface.png")

# --- Figure 3: stability map ---
fig2, ax = plt.subplots(figsize=(10, 7))
# Stability: |r(1-2x)| < 1
stability = np.abs(R * (1 - 2*X)) < 1

im = ax.contourf(R, X, stability.astype(float), levels=[0, 0.5, 1],
                 colors=['steelblue', 'gold'], alpha=0.8)
ax.plot(r_vals, x_fp0, color='white', linewidth=2, label='trivial fp: x=0')
ax.plot(r_vals, x_fp1, color='white', linewidth=2, label='non-trivial fp')
# Mark period-doubling: second bifurcation at r=3
ax.axvline(3, color='yellow', linewidth=1.5, linestyle='--', alpha=0.7, label='first bifurcation (r=3)')
ax.set_xlabel('r (parameter)')
ax.set_ylabel('x (state)')
ax.set_title('Stability regions in cobweb surface\n'
             'gold = stable |f\'(x)|<1, blue = unstable', fontsize=12)
ax.legend(fontsize=10, loc='upper right')
plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-rahel/assets/cobweb-surface-stability.png', dpi=150)
print("Saved cobweb-surface-stability.png")
