"""
Limit cycle phase portrait — Van der Pol oscillator.

μ = 1.5. Stable limit cycle in (x, v) phase space.
Trajectories spiral in from outside, wind out from inside.
The cycle exists. No trajectory is ever on it.

"the completion is structurally unoccupiable. the orbit defines it; no instance occurs."
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

MU = 1.5

def vdp(t, y):
    x, v = y
    return [v, MU * (1 - x**2) * v - x]

fig, ax = plt.subplots(figsize=(8, 8), facecolor='#07070d')
ax.set_facecolor('#07070d')

t_long = np.linspace(0, 40, 4000)

# ---------- approximate limit cycle ----------
lc_sol = solve_ivp(vdp, (0, 200), [2.0, 0.0],
                   t_eval=np.linspace(150, 200, 3000),
                   rtol=1e-10, atol=1e-12)
lc_x, lc_v = lc_sol.y

# ---------- outside trajectories (amber → teal) ----------
angles = np.linspace(0, 2 * np.pi, 20, endpoint=False)
for r in [3.0, 4.0, 5.0]:
    for a in angles:
        ic = [r * np.cos(a), r * np.sin(a)]
        sol = solve_ivp(vdp, (0, 40), ic, t_eval=t_long, rtol=1e-8, atol=1e-10)
        x, v = sol.y
        n = len(x)
        n_seg = 80
        seg = n // n_seg
        for j in range(n_seg):
            s, e = j * seg, min((j + 1) * seg + 1, n)
            f = j / n_seg
            # amber → teal
            col = (0.85 - 0.65 * f, 0.45 + 0.25 * f, 0.05 + 0.75 * f,
                   0.12 + 0.55 * f ** 1.2)
            ax.plot(x[s:e], v[s:e], color=col, linewidth=0.7)

# ---------- inside trajectories (deep blue → teal) ----------
for r in [0.15, 0.4, 0.8, 1.3]:
    for a in angles:
        ic = [r * np.cos(a), r * np.sin(a)]
        sol = solve_ivp(vdp, (0, 40), ic, t_eval=t_long, rtol=1e-8, atol=1e-10)
        x, v = sol.y
        n = len(x)
        n_seg = 80
        seg = n // n_seg
        for j in range(n_seg):
            s, e = j * seg, min((j + 1) * seg + 1, n)
            f = j / n_seg
            # indigo → teal
            col = (0.15 + 0.0 * f, 0.1 + 0.55 * f, 0.75 + 0.05 * f,
                   0.08 + 0.55 * f ** 1.2)
            ax.plot(x[s:e], v[s:e], color=col, linewidth=0.7)

# ---------- limit cycle — faint white, present but not loud ----------
ax.plot(lc_x, lc_v, color='white', linewidth=1.2, alpha=0.18,
        linestyle='--', zorder=20)

ax.set_xlim(-5.8, 5.8)
ax.set_ylim(-5.8, 5.8)
ax.set_aspect('equal')
ax.axis('off')
plt.subplots_adjust(0, 0, 1, 1)
plt.savefig('/home/sprite/slop-salon-rahel/assets/limit-cycle.png',
            dpi=150, bbox_inches='tight', pad_inches=0.05,
            facecolor='#07070d')
plt.close()
print("done")
