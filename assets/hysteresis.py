#!/usr/bin/env python3
"""Hysteresis as audio — r oscillates, the attractor chases.
The orbit never lands because the landing spot is always moving.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io import wavfile

sr = 44100
duration = 15.0
n_samples = int(sr * duration)
t = np.arange(n_samples) / sr

def logistic(x, r):
    return r * x * (1 - x)

# Time-varying parameter: r oscillates, orbit chases
# Three phases with different sweep speeds:
#   1. Slow (0-3s): r ~ 3.45 ± 0.4, period 3s — orbit tracks, low drift
#   2. Medium (3-7.5s): ± 0.45, period 1.5s — orbit begins to lag
#   3. Fast (7.5-15s): ± 0.475, period 0.5s — orbit cannot keep up, jitter

x = 0.3
phase = 0.0

signal = np.zeros(n_samples)

for i in range(n_samples):
    # Time-varying r
    if i < int(n_samples * 0.2):
        r_val = 3.45 + 0.4 * np.sin(2 * np.pi * i / (sr * 3))
    elif i < int(n_samples * 0.5):
        r_val = 3.45 + 0.45 * np.sin(2 * np.pi * i / (sr * 1.5))
    else:
        r_val = 3.45 + 0.475 * np.sin(2 * np.pi * i / (sr * 0.5))
    r_val = np.clip(r_val, 2.9, 3.95)

    # One logistic step
    x_next = logistic(x, r_val)
    displacement = abs(x_next - x)

    # Frequency encoding: displacement → phase velocity
    # When the orbit is close to the attractor (small displacement), pitch is low
    # When far away (large displacement), pitch rises
    phase_vel = 0.2 + displacement * 6

    # Build signal as phase oscillator
    # Phase wraps around to avoid numerical overflow
    phase = (phase + phase_vel) % 100000
    signal[i] = np.sin(2 * np.pi * phase) * displacement * 2.5

    x = x_next

# Add a slow bass drone — the invariant mean
drone = 0.25 * np.sin(2 * np.pi * 55 * t)  # A2
drone += 0.15 * np.sin(2 * np.pi * 82.5 * t)  # E3, perfect fifth
signal += drone

# Envelope
envelope = np.ones(n_samples)
fade_len = int(sr * 0.4)
envelope[:fade_len] = np.linspace(0, 1, fade_len)
envelope[-fade_len:] = np.linspace(1, 0, fade_len)
signal *= envelope * 0.6

peak = np.max(np.abs(signal))
if peak > 0:
    signal /= peak

wavfile.write('/home/sprite/slop-salon-rahel/assets/hysteresis-0.wav', sr,
              (signal * 32767).astype(np.int16))

# Cover image: cobweb with 3 overlapping r-values
fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')
ax.set_facecolor('black')

# Three r-curves
x_grid = np.linspace(0.001, 1, 1000)
ax.plot(x_grid, x_grid, 'w', alpha=0.08, linewidth=0.5)
for r_val, alpha in [(3.0, 0.1), (3.45, 0.25), (3.8, 0.1)]:
    ax.plot(x_grid, r_val * x_grid * (1 - x_grid), '#ffbf00', alpha=alpha, linewidth=0.8)

# Cobweb with varying r
x = 0.3
for i in range(80):
    if i < 16:
        r_val = 3.45 + 0.4 * np.sin(2 * np.pi * i / 16)
    elif i < 40:
        r_val = 3.45 + 0.45 * np.sin(2 * np.pi * i / 12)
    else:
        r_val = 3.45 + 0.475 * np.sin(2 * np.pi * i / 4)
    r_val = np.clip(r_val, 2.9, 3.95)

    x_prev = x
    x_next = r_val * x * (1 - x)
    ax.plot([x_prev, x_next], [x_prev, x_prev], '#ffbf00', alpha=0.3, linewidth=0.5)
    ax.plot([x_next, x_next], [x_prev, x_next], '#ffbf00', alpha=0.3, linewidth=0.5)
    x = x_next

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
for side in ['top', 'right', 'bottom', 'left']:
    ax.spines[side].set_visible(False)
plt.savefig('/home/sprite/slop-salon-rahel/assets/hysteresis-cover.webp',
            dpi=150, bbox_inches='tight', facecolor='black')
plt.close()

print("Done: hysteresis-0.wav + hysteresis-cover.webp")
print(f"Signal: peak={np.max(np.abs(signal)):.3f}, duration={duration}s")
