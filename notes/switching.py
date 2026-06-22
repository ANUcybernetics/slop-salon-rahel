"""Switching dynamics: r=2 (fixed point) ↔ r=4 (chaos).

The orbit alternates between settling and scattering.
The visual is a cobweb where color tracks r.
The audio maps per-step distance to frequency:
  close to diagonal → steady pulse
  far from diagonal → noise-like scatter"""

import numpy as np
import subprocess
import os

# ── Simulation ──

def logistic(x, r):
    return r * x * (1 - x)

N = 3000
swaps = 20  # number of switches total
t_per_regime = N // swaps
dt = 1.0 / swaps  # speed of switching (normalized)

x = 0.1
orbit = []
r_history = []

for i in range(N):
    regime = (i // t_per_regime) % 2
    r = 2.0 if regime == 0 else 4.0
    r_history.append(r)
    orbit.append((x, r))
    x = logistic(x, r)

# ── Visual: cobweb with color tracking r ──

from PIL import Image, ImageDraw

SIZE = 1024
img = Image.new('RGB', (SIZE, SIZE), (10, 10, 14))
draw = ImageDraw.Draw(img)

# Draw r=2 and r=4 curves
def curve(r):
    pts = []
    for px in range(SIZE + 1):
        xi = px / SIZE
        yo = r * xi * (1 - xi)
        py = int((1 - yo) * SIZE)
        pts.append((px, py))
    return pts

curve2 = curve(2.0)
curve4 = curve(4.0)

for pts in curve2:
    draw.point(pts, fill=(30, 50, 70))
for pts in curve4:
    draw.point(pts, fill=(60, 40, 50))

# Diagonal (faint)
for px in range(SIZE):
    py = SIZE - px
    draw.point((px, py), fill=(20, 20, 25))

# Cobweb
for i in range(len(orbit) - 1):
    x0, r0 = orbit[i]
    x1, r1 = orbit[i + 1]

    # Color: r=2 → cool blue, r=4 → warm red
    if r0 > 3:
        cr, cg, cb = int(140 + 115 * (1 - x0)), int(30 + 50 * (1 - x0)), int(20)
    else:
        cr, cg, cb = int(20 + 40 * x0), int(80 + 100 * x0), int(140 + 115 * x0)

    x0p = int(x0 * SIZE)
    y0p = int((1 - r0 * x0 * (1 - x0)) * SIZE)  # vertical from curve
    ydiag0 = int((1 - x0) * SIZE)                # diagonal projection
    x1p = int(x1 * SIZE)
    y1diag = int((1 - x1) * SIZE)

    # Vertical segment: curve → diagonal
    draw.line((x0p, y0p, x0p, ydiag0), fill=(cr, cg, cb), width=1)
    # Horizontal segment: diagonal → next x
    draw.line((x0p, ydiag0, x1p, y1diag), fill=(cr, cg, cb), width=1)

img.save('./assets/switching-cob.webp')

# ── Audio: per-step distance → frequency ──

SAMPLE_RATE = 44100
DURATION = 15.0
NUM_SAMPLES = int(SAMPLE_RATE * DURATION)

# Resample orbit to audio rate
step_size = N / NUM_SAMPLES
audio = np.zeros(NUM_SAMPLES, dtype=np.float32)

for i in range(NUM_SAMPLES):
    orbit_idx = int(i * step_size)
    if orbit_idx >= N:
        orbit_idx = N - 1
    xi, ri = orbit[orbit_idx]
    next_xi = orbit[min(orbit_idx + 1, N - 1)][0]

    # Per-step distance
    dist = abs(next_xi - xi)

    # Map distance to frequency: close → low steady, far → high modulated
    # r=2: dist small (~0) → low freq, steady
    # r=4: dist large (~0.5) → higher freq, more variation
    base_freq = 80 + 600 * dist

    # Phase accumulation
    phase = i * base_freq / SAMPLE_RATE

    # Amplitude: slightly higher during r=4 regime
    if ri > 3:
        amp = 0.3
    else:
        amp = 0.15

    audio[i] = amp * np.sin(2 * np.pi * phase)

# Normalize
audio = audio / (np.max(np.abs(audio)) + 1e-10)

# Write WAV
wav_path = './assets/switching-0.wav'
with open(wav_path, 'wb') as f:
    # Minimal WAV header
    import struct
    f.write(b'RIFF')
    f.write(struct.pack('<I', 36 + NUM_SAMPLES * 2))
    f.write(b'WAVE')
    f.write(b'fmt ')
    f.write(struct.pack('<I', 16))
    f.write(struct.pack('<H', 1))    # PCM
    f.write(struct.pack('<H', 1))    # mono
    f.write(struct.pack('<I', SAMPLE_RATE))
    f.write(struct.pack('<I', SAMPLE_RATE * 2))
    f.write(struct.pack('<H', 2))
    f.write(struct.pack('<H', 16))
    f.write(b'data')
    f.write(struct.pack('<I', NUM_SAMPLES * 2))
    for s in audio:
        f.write(struct.pack('<h', int(s * 32767)))

# Composite to video
ffmpeg_cmd = [
    'ffmpeg', '-y',
    '-loop', '1', '-t', '15',
    '-i', './assets/switching-cob.webp',
    '-i', wav_path,
    '-c:v', 'libx264', '-tune', 'stillimage',
    '-c:a', 'aac', '-b:a', '192k',
    '-pix_fmt', 'yuv420p',
    '-shortest',
    './assets/switching-0.mp4'
]
subprocess.run(ffmpeg_cmd, check=True)

# Cleanup WAV
os.remove(wav_path)

print("Done: switching-0.mp4, switching-cob.webp")
