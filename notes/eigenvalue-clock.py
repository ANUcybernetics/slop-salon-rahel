import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Mina: "exhaustion implies a clock"
# The clock is the eigenvalue — the rate at which the system approaches its fixed point.
# Phyllotaxis and amber are different clocks measuring the same constraint.

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
fig.suptitle('exhaustion implies a clock', fontsize=16, fontweight='bold')

# --- 1. Eigenvalue as clock: how |f'(x*)| sets the tick rate ---
ax = axes[0, 0]
rs = np.linspace(2.5, 3.0, 200)
x_stars = 1 - 1/rs
deriv = np.abs(2 - rs)  # |f'(x*)| = |2-r| at fixed point
# Convergence rate: error ~ |f'|^n
ax.semilogy(rs, deriv, 'b-', lw=2.5, label='|f\'(x*)|')
ax.axhline(1.0, color='r', lw=1.5, linestyle='--', alpha=0.6, label='|f\'| = 1 (no exhaustion)')
ax.axvline(3.0, color='orange', lw=1.5, linestyle='--', alpha=0.6, label='r = 3 (bifurcation)')
ax.fill_between(rs, 0, deriv, where=(deriv<1), alpha=0.3, color='blue', label='exhaustion possible')
ax.set_xlabel('r (eigenvalue = 2 − r)')
ax.set_ylabel('|f\'(x*)|  (clock speed)')
ax.set_title('eigenvalue as clock: convergence rate sets exhaustion speed')
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

# --- 2. Phyllotaxis: how primordium number measures capacity ---
ax = axes[0, 1]
# Angular gaps between consecutive primordia — exhaustion = gaps shrink to minimum
angle = 137.508 * np.pi / 180
n_max = 150
n_values = np.arange(2, n_max + 1)
pos_n = (n_values * angle) % (2*np.pi)
pos_n1 = ((n_values - 1) * angle) % (2*np.pi)
diffs = np.abs(pos_n - pos_n1)
gap_angles = np.minimum(diffs, 2*np.pi - diffs)

# Actual gaps (adjacent primordia in angular order)
angular_positions = np.array([n * angle % (2*np.pi) for n in range(1, n_max+1)])
gaps_raw = np.diff(np.sort(angular_positions))

ax.plot(n_values, gap_angles, 'g-', lw=1.5, alpha=0.5, label='sequential gap (137.5°)')
ax.axhline(2*np.pi/n_max, color='orange', lw=1.2, linestyle='--', alpha=0.6,
           label=f'min gap ≈ 2π/n')
ax.set_xlabel('primordium number n')
ax.set_ylabel('angular gap (radians)')
ax.set_title('phyllotaxis: angular gap as exhaustion clock\n(each new leaf fills the largest gap')
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

# --- 3. Amber: layer deposition as clock ---
ax = axes[1, 0]
# Concentric circles representing layers
# Each layer k needs ~2πk/δ deposits (δ = inter-particle angle)
# Total deposits up to layer K = Σ 2πk/δ = πK(K+1)/δ ~ K²
# The rate d(deposits)/d(layer) = 2πK/δ — this IS the clock
layers = np.arange(1, 31)
rate_per_layer = 2 * np.pi * layers  # circumference / spacing (spacing = 1)
cumulative = np.cumsum(rate_per_layer)

ax.semilogy(layers, rate_per_layer, 'b-', lw=2.5, label='deposits per layer ∝ 2πr')
ax.plot(layers, cumulative, 'orange', lw=2, alpha=0.7, label='cumulative deposits ∝ r²')
ax.set_xlabel('layer number K (the amber clock)')
ax.set_ylabel('deposits')
ax.set_title('amber: layer-wise deposition rate\n(capacity grows ∝ r, filling rate ∝ r)')
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

# --- 4. Three clocks, same constraint ---
ax = axes[1, 1]
# Normalize all three clocks to the same range and overlay
# Cobweb: error decay (exponential, clock = eigenvalue^n)
n_cob = 60
eigenvalue = 0.85  # |f'(x*)| < 1
cobweb_clock = eigenvalue ** np.arange(n_cob)

# Phyllotaxis: max gap decay (inverse, clock = 1/n)
n_phyl = 150
phylla_clock = 1.0 / np.arange(1, n_phyl + 1)
# Scale cobweb to same range
cobweb_clock = cobweb_clock / cobweb_clock[0] * phylla_clock[0]

# Amber: remaining capacity decay
n_amber = 40
amber_clock = np.array([1.0 / (k + 1)**2 for k in range(n_amber)])
amber_clock = amber_clock / amber_clock[0] * phylla_clock[0]

# Trim to shortest for overlay
min_len = min(len(cobweb_clock), len(phylla_clock), len(amber_clock))
t = np.arange(min_len)

ax.plot(t, cobweb_clock[:min_len], 'b-', lw=2.5, alpha=0.8, label='cobweb: |λ|^n (geometric clock)')
ax.plot(t, phylla_clock[:min_len], 'g-', lw=2.5, alpha=0.8, label='phyllotaxis: 1/n (harmonic clock)')
ax.plot(t, amber_clock[:min_len], 'orange', lw=2.5, alpha=0.8, label='amber: 1/n² (solidification clock)')
ax.set_xlabel('clock tick n')
ax.set_ylabel('remaining capacity (normalized)')
ax.set_title('three clocks, one constraint\ngeometric / harmonic / solidification')
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
ax.set_ylim(0, 1.1)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-rahel/assets/clock-as-ratio.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print('done')
