#!/usr/bin/env python3
"""Coincidence as self-intersection.

A curve parameterized over time. The intersection point is not a destination —
it's where the curve meets itself. No clock needed; the geometry is the geometry.

Two visualizations:
1. A lemniscate (Bernoulli) — the simplest self-intersecting curve.
   The crossing is coincidence. The lobes are the same curve at different parameter values.
2. A cobweb of a curve that maps back to itself — not convergence, but coincidence.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Coincidence: self-intersection of a parameterized curve ---
t = np.linspace(0, 2*np.pi, 1000)

# Bernoulli lemniscate: (x^2 + y^2)^2 = 2a^2(x^2 - y^2)
a = 1.0
# Parametric form using tangent: x = a*cos(t)/(1 + sin(t)^2), y = a*sin(t)*cos(t)/(1 + sin(t)^2)
x = a * np.cos(t) / (1 + np.sin(t)**2)
y = a * np.sin(t) * np.cos(t) / (1 + np.sin(t)**2)

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), dpi=150)

# Left: the curve as coincidence
ax = axes[0]
ax.plot(x, y, 'white', linewidth=1.5, alpha=0.9)
# Mark the self-intersection point (origin)
ax.plot(0, 0, 'o', color='crimson', markersize=8, zorder=5)
ax.text(0.08, -0.05, 'coincidence', color='crimson', fontsize=10, fontweight='bold')
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-0.8, 0.8)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('self-intersection', fontsize=11, fontweight='bold', color='white')

# Middle: parameterized trajectory with "clock" — color by t
ax = axes[1]
sc = ax.scatter(x, y, c=t, cmap='coolwarm', s=1, alpha=0.7)
ax.plot(0, 0, 'o', color='white', markersize=6, zorder=5)
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-0.8, 0.8)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('the clock is just the label', fontsize=11, fontweight='bold', color='white')

# Right: what it looks like without parameterization — just the field
ax = axes[2]
ax.plot(x, y, 'white', linewidth=2, alpha=0.9)
# Add the vector field direction at sample points
n_samples = 80
sample_t = np.linspace(0, 2*np.pi, n_samples, endpoint=False)
sx = a * np.cos(sample_t) / (1 + np.sin(sample_t)**2)
sy = a * np.sin(sample_t) * np.cos(sample_t) / (1 + np.sin(sample_t)**2)
# Tangent vector (derivative of parametric form)
dx = -a * np.sin(sample_t) * (1 + np.sin(sample_t)**2) - a * np.cos(sample_t) * 2 * np.sin(sample_t) * np.cos(sample_t)
dy = (np.cos(sample_t)**2 - np.sin(sample_t)**2) * (1 + np.sin(sample_t)**2) - np.sin(sample_t)*np.cos(sample_t) * 2 * np.sin(sample_t) * np.cos(sample_t)
den = (1 + np.sin(sample_t)**2)**2
dx = dx / den
dy = dy / den
# Normalize
norm = np.sqrt(dx**2 + dy**2)
dx = dx / norm * 0.12
dy = dy / norm * 0.12
ax.quiver(sx, sy, dx, dy, alpha=0.5, color='crimson', width=0.003)
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-0.8, 0.8)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('the field has no clock', fontsize=11, fontweight='bold', color='white')

fig.patch.set_facecolor('black')
for ax in axes:
    ax.set_facecolor('black')

plt.tight_layout(pad=0.3)
plt.savefig('./assets/coincidence-01.png', dpi=150, bbox_inches='tight')
plt.close()

# --- Second image: coincidence as convergence of two paths with no meeting ---
# Two trajectories in the same field, same geometry, different parameterization
t1 = np.linspace(0, 4*np.pi, 1000)
t2 = np.linspace(2*np.pi, 6*np.pi, 1000)

# Spiral that intersects itself
r = np.linspace(0.1, 1.5, 1000)
theta1 = np.linspace(0, 4*np.pi, 1000)
theta2 = np.linspace(2*np.pi, 6*np.pi, 1000)

x1 = r * np.cos(theta1)
y1 = r * np.sin(theta1)
x2 = r * np.cos(theta2)
y2 = r * np.sin(theta2)

fig, ax = plt.subplots(1, 1, figsize=(8, 8), dpi=150)
ax.plot(x1, y1, 'white', linewidth=0.8, alpha=0.5, label='path 1')
ax.plot(x2, y2, 'white', linewidth=0.8, alpha=0.5, label='path 2')

# The "convergence" points are just where the parameterizations align
# They don't actually meet — they share the same space at different times
n_align = 20
for i in range(0, 1000, 50):
    ax.plot(x1[i], y1[i], '.', color='crimson', markersize=3, alpha=0.7)

ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

# Add annotation at the center
ax.text(0, 0, 'same space\ndifferent time', color='crimson', fontsize=10,
        fontweight='bold', ha='center', va='center', alpha=0.8)

plt.tight_layout()
plt.savefig('./assets/coincidence-02.png', dpi=150, bbox_inches='tight')
plt.close()
