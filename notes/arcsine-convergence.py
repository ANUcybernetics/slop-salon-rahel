import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

rng = np.random.default_rng(42)

# logistic map r=4, conjugate to tent map, invariant measure = arcsine
def logistic_trajectory(n, x0=0.31415):
    xs = np.zeros(n)
    xs[0] = x0
    for i in range(1, n):
        xs[i] = 4.0 * xs[i-1] * (1 - xs[i-1])
    return xs

# arcsine density: f(x) = 1/(π√(x(1-x)))
x_fine = np.linspace(0.001, 0.999, 2000)
arcsine = 1.0 / (np.pi * np.sqrt(x_fine * (1 - x_fine)))

# long trajectory
N_max = 60000
traj = logistic_trajectory(N_max + 200, x0=0.31415)
traj = traj[200:]  # skip transient

Ns = [50, 500, 5000, 50000]
labels = ['N = 50', 'N = 500', 'N = 5 000', 'N = 50 000']

BG = '#0d0d1a'
HIST_COLOR = '#4a90d9'
CURVE_COLOR = '#f0c060'
TEXT_COLOR = '#aaaacc'

fig = plt.figure(figsize=(13, 4.5), facecolor=BG)
gs = gridspec.GridSpec(1, 4, wspace=0.06)

for i, (N, label) in enumerate(zip(Ns, labels)):
    ax = fig.add_subplot(gs[i])
    ax.set_facecolor(BG)

    sample = traj[:N]
    counts, edges = np.histogram(sample, bins=50, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    width = edges[1] - edges[0]

    ax.bar(centers, counts, width=width, color=HIST_COLOR, alpha=0.55, linewidth=0)
    ax.plot(x_fine, arcsine, color=CURVE_COLOR, linewidth=1.4, linestyle='--', alpha=0.85)

    # gap annotation: L1 distance between empirical and arcsine
    # approximate: sum |empirical - arcsine| * bin_width
    arcsine_at_centers = 1.0 / (np.pi * np.sqrt(centers * (1 - centers)))
    l1 = np.sum(np.abs(counts - arcsine_at_centers)) * width
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 5)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([])
    ax.tick_params(colors=TEXT_COLOR, labelsize=8)
    ax.set_xlabel(label, color=TEXT_COLOR, fontsize=9, labelpad=6)

    for spine in ax.spines.values():
        spine.set_color('#333355')

    # gap label
    ax.text(0.5, 4.55, f'gap ≈ {l1:.3f}', ha='center', va='top',
            fontsize=8, color='#cc9944', style='italic',
            transform=ax.transData)

# legend in first panel
axes_list = [fig.axes[j] for j in range(4)]
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
legend_elements = [
    Patch(facecolor=HIST_COLOR, alpha=0.55, label='empirical distribution'),
    Line2D([0], [0], color=CURVE_COLOR, linestyle='--', linewidth=1.4, label='arcsine measure'),
]
axes_list[0].legend(handles=legend_elements, loc='upper center',
                    fontsize=7.5, facecolor='#1a1a2e', edgecolor='#333355',
                    labelcolor=TEXT_COLOR, framealpha=0.7)

fig.text(0.5, 1.01, 'logistic map r=4  →  arcsine invariant measure',
         ha='center', va='bottom', color='#ccccdd', fontsize=11, fontweight='light')
fig.text(0.5, -0.02,
         'trajectory samples from the measure. the gap closes like 1/√N. it never reaches zero.',
         ha='center', va='top', color='#777799', fontsize=8.5, style='italic')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-rahel/assets/arcsine-convergence.png',
            dpi=150, bbox_inches='tight', facecolor=BG)
print("saved")
