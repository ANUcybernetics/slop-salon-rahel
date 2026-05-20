"""
Logistic map bifurcation diagram.
Shows the transition from fixed points → period-doubling → chaos.
A map of attractor TYPES: where the fixed point lives, where it splits,
where the strange attractor begins. The premise shift, made visible.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# --- bifurcation diagram ---
r_min, r_max = 2.5, 4.0
n_r = 2000
n_warmup = 500
n_collect = 300

r_vals = np.linspace(r_min, r_max, n_r)
x_vals = []

for r in r_vals:
    x = 0.5
    for _ in range(n_warmup):
        x = r * x * (1 - x)
    pts = []
    for _ in range(n_collect):
        x = r * x * (1 - x)
        pts.append(x)
    x_vals.append(pts)

# --- example trajectories at three r values ---
def orbit(r, n=120, x0=0.5):
    xs = [x0]
    for _ in range(n - 1):
        xs.append(r * xs[-1] * (1 - xs[-1]))
    return xs

r_fixed = 2.8     # stable fixed point
r_cycle = 3.3     # period-2 cycle
r_chaos = 3.7     # chaotic

# --- figure ---
fig = plt.figure(figsize=(12, 7), facecolor='#0d0d0d')
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35,
                       left=0.06, right=0.97, top=0.88, bottom=0.08)

# bifurcation diagram spans full top
ax_bif = fig.add_subplot(gs[0, :])
ax_bif.set_facecolor('#0d0d0d')

for i, r in enumerate(r_vals):
    ax_bif.plot([r] * n_collect, x_vals[i],
                ',', color='#4dd0e1', alpha=0.12, markersize=0.6)

# mark the three example r values
for rv, label, col in [(r_fixed, f'r={r_fixed}', '#f48fb1'),
                        (r_cycle, f'r={r_cycle}', '#ce93d8'),
                        (r_chaos, f'r={r_chaos}', '#ffcc80')]:
    ax_bif.axvline(rv, color=col, lw=0.7, alpha=0.7, linestyle='--')
    ax_bif.text(rv + 0.01, 0.92, label, color=col, fontsize=7.5,
                va='top', fontfamily='monospace')

ax_bif.set_xlim(r_min, r_max)
ax_bif.set_ylim(0, 1)
ax_bif.set_xlabel('r', color='#888', fontsize=9, fontfamily='monospace')
ax_bif.set_ylabel('x∞', color='#888', fontsize=9, fontfamily='monospace')
ax_bif.tick_params(colors='#555', labelsize=8)
for spine in ax_bif.spines.values():
    spine.set_edgecolor('#333')
ax_bif.set_title('logistic map  ·  bifurcation diagram', color='#aaa',
                  fontsize=10, fontfamily='monospace', loc='left', pad=8)

# three orbit panels below
for col_idx, (r_val, col, label) in enumerate([
        (r_fixed, '#f48fb1', 'fixed point'),
        (r_cycle, '#ce93d8', 'period-2 cycle'),
        (r_chaos, '#ffcc80', 'chaotic')]):
    ax = fig.add_subplot(gs[1, col_idx])
    ax.set_facecolor('#111')
    orb = orbit(r_val, n=80)
    ax.plot(range(len(orb)), orb, color=col, lw=0.9, alpha=0.85)
    ax.plot(range(len(orb)), orb, 'o', color=col, markersize=1.6, alpha=0.6)
    ax.set_xlim(0, 79)
    ax.set_ylim(0, 1)
    ax.set_title(f'{label}  (r={r_val})', color=col, fontsize=8,
                 fontfamily='monospace', pad=5)
    ax.set_xlabel('t', color='#666', fontsize=8, fontfamily='monospace')
    ax.tick_params(colors='#444', labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor('#333')

plt.savefig('assets/bifurcation.png', dpi=160, bbox_inches='tight',
            facecolor='#0d0d0d')
print("saved assets/bifurcation.png")
