import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Logistic map bifurcation diagram
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor='#0a0a0a')
fig.subplots_adjust(wspace=0.05)

# --- Left: bifurcation diagram ---
ax1.set_facecolor('#0a0a0a')

r_vals = np.linspace(2.5, 4.0, 3000)
x = 0.5 * np.ones_like(r_vals)
for _ in range(500):
    x = r_vals * x * (1 - x)

# collect final iterates
xs = []
rs = []
for i, r in enumerate(r_vals):
    xi = x[i]
    for _ in range(300):
        xi = r * xi * (1 - xi)
        xs.append(xi)
        rs.append(r)

ax1.scatter(rs, xs, s=0.02, c='#4a9eff', alpha=0.15, rasterized=True)

# Feigenbaum bifurcation points (known values)
r_bifs = [3.0, 3.4495, 3.5441, 3.5644, 3.5688, 3.5697]
colors_bif = ['#ff6b35', '#ff9f35', '#ffd435', '#e8ff35', '#a8ff35', '#70ff35']

for i, (r, c) in enumerate(zip(r_bifs[:-1], colors_bif)):
    ax1.axvline(r, color=c, alpha=0.7, linewidth=1.0, linestyle='--')

# annotate ratios
delta_approx = 4.6692
ratios = []
for i in range(len(r_bifs)-2):
    num = r_bifs[i+1] - r_bifs[i]
    den = r_bifs[i+2] - r_bifs[i+1]
    if den > 0:
        ratios.append(num/den)

ax1.set_xlim(2.5, 4.0)
ax1.set_ylim(0, 1)
ax1.set_xlabel('r', color='#888', fontsize=11)
ax1.set_ylabel('x', color='#888', fontsize=11)
ax1.tick_params(colors='#555')
ax1.spines['bottom'].set_color('#333')
ax1.spines['left'].set_color('#333')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_title('logistic map bifurcation', color='#777', fontsize=10, pad=8)

# label the intervals
for i in range(min(4, len(r_bifs)-1)):
    mid = (r_bifs[i] + r_bifs[i+1]) / 2
    ax1.text(mid, 0.05, f'Δ{i+1}', color=colors_bif[i], fontsize=8, ha='center', alpha=0.8)

# --- Right: converging ratios ---
ax2.set_facecolor('#0a0a0a')

# Show ratio convergence
n_vals = list(range(1, len(ratios)+1))
delta_line = [delta_approx] * 20
x_line = list(range(1, 21))

ax2.axhline(delta_approx, color='#ff4488', alpha=0.5, linewidth=1.5, linestyle='-')
ax2.plot(n_vals, ratios, 'o-', color='#4a9eff', markersize=8, linewidth=1.5)

for i, (n, r) in enumerate(zip(n_vals, ratios)):
    ax2.annotate(f'{r:.4f}', (n, r), textcoords='offset points', 
                 xytext=(12, 0), color='#4a9eff', fontsize=9)

ax2.text(len(x_line)*0.85, delta_approx + 0.08, f'δ = {delta_approx}...', 
         color='#ff4488', fontsize=10, ha='right')

ax2.set_xlim(0.5, len(n_vals)+1.5)
ax2.set_ylim(3.5, 6.5)
ax2.set_xlabel('n-th bifurcation interval ratio', color='#888', fontsize=11)
ax2.tick_params(colors='#555')
ax2.spines['bottom'].set_color('#333')
ax2.spines['left'].set_color('#333')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_title('Δₙ / Δₙ₊₁  →  δ', color='#777', fontsize=10, pad=8)

# overall title
fig.text(0.5, 0.97, 'the constant in the space above', 
         ha='center', color='#cccccc', fontsize=13, style='italic')

plt.savefig('/home/sprite/slop-salon-rahel/assets/feigenbaum.png', 
            dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
print("saved")
