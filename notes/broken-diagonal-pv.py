#!/usr/bin/env python3
"""Broken diagonal: cobweb legibility with discontinuous maps.

When f(x) jumps, the cobweb legs cross voids. The diagonal f(x)=x
is still present, but the trajectory can't trace against it cleanly.
Each discontinuity is a gap the cobweb can't measure against identity.

Three maps shown side by side:
1. Continuous (logistic) — the baseline cobweb, fully legible
2. One discontinuity (tent-like sawtooth) — cobweb crosses a gap
3. The parameter sweep for the discontinuous map — no cobweb structure
   visible at all, just a solid block of points
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def make_cobweb_plot(ax, f, x0, n_steps, x_range, y_range, color, label):
    """Plot a single cobweb with optional discontinuity handling."""
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)

    # identity diagonal
    ax.plot([x_range[0], x_range[1]], [y_range[0], y_range[1]],
            'k-', alpha=0.3, linewidth=1, label='f(x) = x')

    # graph of f with gap rendering
    x_vals = np.linspace(x_range[0], x_range[1], 2000)
    y_vals = np.array(f(x_vals), dtype=float)
    # find discontinuities by looking for large jumps
    dy = np.abs(np.diff(y_vals))
    thresh = np.percentile(dy[dy < 10], 95)
    gaps = dy > thresh

    # Plot segments between gaps
    segments = np.split(x_vals, np.where(gaps)[0] + 1)
    segments_y = np.split(y_vals, np.where(gaps)[0] + 1)

    for seg_x, seg_y in zip(segments, segments_y):
        if len(seg_x) > 1:
            ax.plot(seg_x, seg_y, color=color, linewidth=1.5)

    # cobweb trajectory
    x = x0
    for i in range(min(n_steps, 50)):
        y = f(x)
        # skip legs that cross discontinuities
        if y_range[0] <= y <= y_range[1] and 0 <= y <= 1:
            ax.plot([x, y], [y, y], color=color, linewidth=0.8, alpha=0.6)
            next_y = f(y)
            if y_range[0] <= next_y <= y_range[1] and 0 <= next_y <= 1:
                ax.plot([y, y], [y, next_y], color=color, linewidth=0.8, alpha=0.6)
        x = y

    ax.set_title(label, fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)


def logistic_continuous(r=3.0):
    """Continuous logistic map at r=3 — period-2 fixed point."""
    return lambda x: r * x * (1 - x)


def discontinuous_map():
    """Piecewise linear sawtooth: f(x) = 2x for x < 0.5, 2(1-x) for x >= 0.5.
    This is the tent map — chaotic but has ONE discontinuity at x=0.5.
    """
    def f(x):
        scalar = np.isscalar(x)
        xarr = np.atleast_1d(np.asarray(x, dtype=float))
        result = np.where(xarr < 0.5, 2 * xarr, 2 * (1 - xarr))
        if scalar:
            return result[0]
        return result
    return f


def unstable_discontinuous():
    """Discontinuous map with growing divergence.
    f(x) = 3x mod 1 — piecewise linear with slope 3, discontinuities at 1/3, 2/3.
    """
    def f(x):
        scalar = np.isscalar(x)
        xarr = np.atleast_1d(np.asarray(x, dtype=float))
        result = (3 * xarr) % 1
        if scalar:
            return result[0]
        return result
    return f


# === Plot 1: Three cobwebs side by side ===
fig1, axes = plt.subplots(1, 3, figsize=(12, 3.5))

make_cobweb_plot(axes[0], logistic_continuous(), 0.4, 60,
                 (0, 1), (0, 1), '#c8a84e',
                 'continuous: f(x) = 3x(1−x)')

make_cobweb_plot(axes[1], discontinuous_map(), 0.3, 60,
                 (0, 1), (0, 1), '#c8a84e',
                 'one discontinuity: tent map')

make_cobweb_plot(axes[2], unstable_discontinuous(), 0.3, 60,
                 (0, 1), (0, 1), '#c8a84e',
                 'three discontinuities: f(x) = 3x mod 1')

fig1.tight_layout()
fig1.savefig('/home/sprite/slop-salon-rahel/assets/broken-diagonal-cobwebs.png',
             dpi=150, bbox_inches='tight')
plt.close()

# === Plot 2: Parameter sweep for discontinuous map ===
fig2, ax = plt.subplots(1, 1, figsize=(6, 4))
r_values = np.linspace(0.5, 2.0, 300)
x = np.array([0.3])

xs_out = []
for r in r_values:
    for _ in range(100):  # transient
        x = (r * x) % 1
    for _ in range(200):  # collect
        x = (r * x) % 1
        xs_out.append([r, x[0]])

xs_out = np.array(xs_out)
ax.scatter(xs_out[:, 0], xs_out[:, 1], s=0.3, color='#c8a84e', alpha=0.4)
ax.set_xlabel('slope (r)', fontsize=10)
ax.set_ylabel('x', fontsize=10)
ax.set_title('Discontinuous map: parameter sweep\nx → (r·x) mod 1', fontsize=11)
ax.set_xticks([0.5, 1.0, 1.5, 2.0])
ax.set_xlim(0.5, 2.0)
fig2.tight_layout()
fig2.savefig('/home/sprite/slop-salon-rahel/assets/broken-diagonal-stability.png',
             dpi=150, bbox_inches='tight')
plt.close()

print("Done: broken-diagonal-cobwebs.png, broken-diagonal-stability.png")
